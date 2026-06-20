"""能力内核 · 基建后端

两类后端，都通过 Context 注入，对内核透明：
  1. LLM 后端 —— 语言细胞的执行器。StubLLM（离线确定性）/ AnthropicLLM（真实，即插即用）。
  2. 计算函数表 —— 计算细胞的执行器。纯 Python、无第三方依赖、可复现。
"""
from __future__ import annotations

import json
import math
import re


# ── LLM 后端 ──────────────────────────────────────────────────────────────
def _tag(prompt: str, key: str) -> str:
    m = re.search(rf"^{key}:\s*(.*)$", prompt, re.MULTILINE)
    return m.group(1).strip() if m else ""


def _num(pattern: str, text: str):
    m = re.search(pattern, text)
    return int(m.group(1)) if m else None


class StubLLM:
    """离线确定性 LLM 替身。

    读 TASK 标签来模拟"已被分化条件特化"后的行为，从而无网络也能跑通机制。
    真实部署时换成 AnthropicLLM 即可，语言细胞（stem_llm）一行都不用改。
    """

    def complete(self, prompt: str) -> str:
        task = _tag(prompt, "TASK")
        payload = json.loads(_tag(prompt, "PAYLOAD") or "{}")

        if task == "extract_baseline":
            t = payload.get("case_text", "")
            return json.dumps(
                {"baseline": {
                    "age": _num(r"(\d+)\s*岁", t),
                    "sex": "女" if "女" in t else ("男" if "男" in t else "未知"),
                    "lvef": _num(r"LVEF[^\d]*(\d+)", t),
                }},
                ensure_ascii=False,
            )

        if task == "extract_endpoint":
            t = payload.get("case_text", "")
            return json.dumps(
                {"endpoint": {
                    "rehospitalization": "再入院" in t,
                    "followup_months": _num(r"随访[^\d]*(\d+)", t),
                }},
                ensure_ascii=False,
            )

        if task == "interpret":
            c = payload.get("comparison", {})
            p = c.get("p_value")
            sig = p is not None and p < 0.05
            return json.dumps(
                {"interpretation": (
                    f"{c.get('group_a')}组与{c.get('group_b')}组 LVEF 中位数分别为 "
                    f"{c.get('median_a')} 与 {c.get('median_b')}，Mann-Whitney p={p}，"
                    f"差异{'具有' if sig else '不具有'}统计学意义。"
                )},
                ensure_ascii=False,
            )

        if task == "summarize":
            b = payload.get("baseline", {})
            e = payload.get("endpoint", {})
            it = payload.get("interpretation", "")
            return json.dumps(
                {"clinical_summary": (
                    f"患者 {b.get('age')} 岁{b.get('sex')}性，基线 LVEF {b.get('lvef')}%；"
                    f"随访 {e.get('followup_months')} 个月，"
                    f"再入院：{'是' if e.get('rehospitalization') else '否'}。"
                    f"队列层面：{it}"
                )},
                ensure_ascii=False,
            )

        return json.dumps({"result": "stub-noop"}, ensure_ascii=False)


class AnthropicLLM:
    """真实 LLM 后端。需要 anthropic SDK + ANTHROPIC_API_KEY。

    接口与 StubLLM 完全一致（complete(prompt) -> str），可直接替换。
    模型按 evolution.md「原则4 分层模型使用」选取：分析/写作用均衡档，审查档可上调。
    """

    def __init__(self, model: str = "claude-sonnet-4-6", max_tokens: int = 1024):
        import anthropic  # 延迟导入：离线环境不受影响

        self._client = anthropic.Anthropic()
        self._model = model
        self._max_tokens = max_tokens

    def complete(self, prompt: str) -> str:
        msg = self._client.messages.create(
            model=self._model,
            max_tokens=self._max_tokens,
            messages=[{"role": "user", "content": prompt}],
        )
        return msg.content[0].text


# ── 计算函数表（基建：确定性、可复现） ──────────────────────────────────────
DATASETS = {
    # 心衰演示队列：治疗组 vs 对照组的 LVEF（%）
    "heartfailure_demo": [
        {"arm": "治疗", "lvef": 45}, {"arm": "治疗", "lvef": 48}, {"arm": "治疗", "lvef": 50},
        {"arm": "治疗", "lvef": 42}, {"arm": "治疗", "lvef": 47}, {"arm": "治疗", "lvef": 52},
        {"arm": "对照", "lvef": 35}, {"arm": "对照", "lvef": 38}, {"arm": "对照", "lvef": 40},
        {"arm": "对照", "lvef": 33}, {"arm": "对照", "lvef": 37}, {"arm": "对照", "lvef": 41},
    ],
}


def _median(xs):
    s = sorted(xs)
    n = len(s)
    if n == 0:
        return None
    mid = n // 2
    return s[mid] if n % 2 else (s[mid - 1] + s[mid]) / 2


def _phi(x):  # 标准正态 CDF
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


def _avg_ranks(sorted_vals):
    """对已排序的值赋平均秩（处理并列）。"""
    ranks = [0.0] * len(sorted_vals)
    i = 0
    while i < len(sorted_vals):
        j = i
        while j + 1 < len(sorted_vals) and sorted_vals[j + 1] == sorted_vals[i]:
            j += 1
        avg = (i + 1 + j + 1) / 2
        for k in range(i, j + 1):
            ranks[k] = avg
        i = j + 1
    return ranks


def _mann_whitney_p(a, b):
    """Mann-Whitney U，双侧 p（正态近似，纯 Python，无 scipy）。"""
    combined = sorted([(v, 0) for v in a] + [(v, 1) for v in b], key=lambda x: x[0])
    ranks = _avg_ranks([v for v, _ in combined])
    r1 = sum(r for r, (_, g) in zip(ranks, combined) if g == 0)
    n1, n2 = len(a), len(b)
    u1 = r1 - n1 * (n1 + 1) / 2
    u = min(u1, n1 * n2 - u1)
    mu = n1 * n2 / 2
    sigma = math.sqrt(n1 * n2 * (n1 + n2 + 1) / 12)
    if sigma == 0:
        return 1.0
    z = (u - mu) / sigma
    return max(0.0, min(1.0, 2 * (1 - _phi(abs(z)))))


def _skewness(xs):
    n = len(xs)
    if n < 3:
        return 0.0
    m = sum(xs) / n
    var = sum((x - m) ** 2 for x in xs) / n
    if var == 0:
        return 0.0
    s = var ** 0.5
    return (sum((x - m) ** 3 for x in xs) / n) / (s ** 3)


def fn_load_dataset(payload, cond):
    name = cond.get("name") or payload.get("dataset")
    data = DATASETS.get(name)
    if data is None:
        raise KeyError(f"未知数据集: {name!r}")
    return {"table": data, "dataset": name}


def fn_group_compare(payload, cond):
    table = payload["table"]
    gk, vk = cond.get("group_key", "arm"), cond.get("value_key", "lvef")
    groups: dict = {}
    for row in table:
        groups.setdefault(row[gk], []).append(row[vk])
    keys = list(groups)
    a, b = groups[keys[0]], groups[keys[1]]
    return {"comparison": {
        "group_a": keys[0], "group_b": keys[1],
        "n_a": len(a), "n_b": len(b),
        "median_a": _median(a), "median_b": _median(b),
        "p_value": round(_mann_whitney_p(a, b), 4),
        "method": "Mann-Whitney U (正态近似)",
    }}


def fn_normality(payload, cond):
    vk = cond.get("value_key", "lvef")
    vals = [r[vk] for r in payload["table"]]
    sk = _skewness(vals)
    return {"normality": {
        "skewness": round(sk, 3),
        "roughly_normal": abs(sk) < 1.0,
        "note": "启发式：|偏度|<1 视为近似正态",
    }}


# 基建函数表：计算细胞分化时用 fn=<key> 选取
COMPUTE_FNS = {
    "load_dataset": fn_load_dataset,
    "group_compare": fn_group_compare,
    "normality": fn_normality,
}
