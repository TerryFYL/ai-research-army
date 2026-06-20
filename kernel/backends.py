"""能力内核 · 基建后端

两类后端，都通过 Context 注入，对内核透明：
  1. LLM 后端 —— 语言细胞的执行器。StubLLM（离线确定性）/ AnthropicLLM（真实，即插即用）。
  2. 计算函数表 —— 计算细胞的执行器。纯 Python、无第三方依赖、可复现。
"""
from __future__ import annotations

import json
import math
import re

from . import biostats, synthetic_cohort


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


# ── 数字格式化（基建：稿件正文与摘要共用，保证数字一致性） ──────────────────
def _f1(x):
    return f"{x:.1f}"


def _f2(x):
    return f"{x:.2f}"


def _p_str(p):
    """p 值（表格内）：<0.001 或三位小数。"""
    if p != p:  # NaN
        return "NA"
    return "<0.001" if p < 0.001 else f"{p:.3f}"


def _p_phrase(p):
    """p 值（正文）：< 0.001 或 = 0.005。"""
    if p != p:  # NaN
        return "= NA"
    return "< 0.001" if p < 0.001 else f"= {p:.3f}"


def _pct(k, n):
    return f"{(100.0 * k / n):.1f}" if n else "NA"


# ── 数字归代码：统计量 → token 渲染（写作细胞碰不到原始数字，故无法篡改/编造） ──
def render_table1_md(t1: dict) -> str:
    """把真算 Table 1 渲染成 markdown 表（数字唯一真源）。"""
    a, b = t1["arms"][0], t1["arms"][1]
    head = f"| Characteristic | {a} (n={t1['n'][a]}) | {b} (n={t1['n'][b]}) | P |"
    sep = "| --- | --- | --- | --- |"
    body = "\n".join(
        f"| {r['label']} | {r[a]} | {r[b]} | {r['p']} |" for r in t1["rows"])
    return "\n".join([
        "**Table 1.** Baseline characteristics, treatment and outcomes by group.",
        "", head, sep, body])


def build_tokens(stats: dict) -> dict:
    """构造 token→真值映射。所有进入稿件的数字**只**经此处产生（红线：真算可复现，不编造）。"""
    cox = stats["cox"]["primary"]
    km = stats["km"]
    return {
        "{{N_TOTAL}}": str(stats["n_total"]),
        "{{N_EVENTS}}": str(stats["cox"]["events"]),
        "{{MEDIAN_FU}}": km["median_followup_s"],
        "{{TABLE1}}": render_table1_md(stats["table1"]),
        "{{ABSTRACT_EFFECT}}": (
            f"an adjusted hazard ratio of {cox['hr_s']} "
            f"(95% CI {cox['ci_low_s']}-{cox['ci_high_s']})"),
        "{{RESULTS_EFFECT}}": (
            f"adjusted hazard ratio {cox['hr_s']}, "
            f"95% CI {cox['ci_low_s']}-{cox['ci_high_s']}; P {cox['p_phrase']}"),
        "{{LOGRANK}}": f"log-rank P {km['logrank_p_phrase']}",
    }


def apply_tokens(text: str, tokens: dict) -> str:
    for k, v in tokens.items():
        text = text.replace(k, v)
    return text


# 真模型可用的 token 清单（写进 draft 细胞指令；真 Claude 只许写散文 + 插入这些 token）
ALLOWED_TOKENS = [
    "{{N_TOTAL}}", "{{N_EVENTS}}", "{{MEDIAN_FU}}", "{{TABLE1}}",
    "{{ABSTRACT_EFFECT}}", "{{RESULTS_EFFECT}}", "{{LOGRANK}}",
]


class MockLLM:
    """离线确定性「写作」LLM 替身（⚠️ SYNTHETIC：模板化散文，非真实模型创作）。

    数字归代码：本类**只产散文 + token 占位符**（如 {{TABLE1}}、{{RESULTS_EFFECT}}），
    一切真实数字由 build_tokens/apply_tokens 在代码侧回填——写作细胞从不接触原始统计量，
    因此**无法篡改或编造数字**（医学零容错红线）。占位 DOI 由 declarations 细胞输出，
    审核器据此判 citation_authenticity = NEEDS-REVIEW，绝不伪绿。

    即插即用：接口与 AnthropicLLM 完全一致（complete(prompt) -> str，返回 JSON 字符串）。
    与 StubLLM 同构——读 TASK 分派、读 PAYLOAD（meta + narrative，**不含原始数字**）、按 produces 键回填。
    换真 Key：Context(llm=MockLLM()) → Context(llm=AnthropicLLM())，语言细胞代码一行不改；
    真模型读 INSTRUCTION（见 pipeline 的 draft 指令）写同样"散文+token"，数字仍由代码回填。
    """

    def complete(self, prompt: str) -> str:
        task = _tag(prompt, "TASK")
        payload = json.loads(_tag(prompt, "PAYLOAD") or "{}")
        meta = payload.get("meta", {})
        nar = payload.get("narrative", {})
        handler = getattr(self, f"_t_{task}", None)
        if handler is None:
            return json.dumps({"result": "mock-noop"}, ensure_ascii=False)
        key, text = handler(meta, nar)
        return json.dumps({key: text}, ensure_ascii=False)

    # 每个 _t_<task>(meta, narrative) 返回 (produces_key, 含 token 的散文)；不含任何原始数字
    def _t_draft_title(self, meta, nar):
        disease = meta.get("disease", "the cohort")
        # 末尾故意留一个句点（拟真首稿瑕疵）→ 交给科学循环 fix_title 收敛
        return "sec_title", (
            f"A retrospective cohort study of {nar.get('exposure_label', 'the exposure')} "
            f"and {nar.get('outcome_label', 'outcomes')} in patients with {disease}.")

    def _t_draft_abstract(self, meta, nar):
        syn = "synthetic " if nar.get("synthetic") else ""
        exp = nar.get("exposure_label", "the exposure")
        out = nar.get("outcome_label", "the outcome")
        caveat = (" These synthetic findings illustrate an end-to-end analytic pipeline and "
                  "should not be interpreted as clinical evidence." if nar.get("synthetic") else "")
        # 故意夹一个文献标记 [1]（拟真首稿瑕疵）→ 交给 fix_abstract_citation 收敛。
        text = (
            f"Heart failure with preserved ejection fraction is common and carries a high "
            f"{out} burden. In this {syn}retrospective cohort study we analysed {{{{N_TOTAL}}}} "
            f"patients with HFpEF to evaluate whether {exp} was associated with {out}-free "
            f"survival [1]. Patients were grouped by treatment strategy and followed for up to "
            f"thirty-six months, with {{{{N_EVENTS}}}} {out} events observed. After adjustment for "
            f"age, sex, comorbidities, natriuretic peptide and ejection fraction, {exp} was "
            f"associated with a {nar.get('direction', 'different')} hazard of {out}, with "
            f"{{{{ABSTRACT_EFFECT}}}}.{caveat}")
        return "sec_abstract", "## Abstract\n" + text

    def _t_draft_intro(self, meta, nar):
        tail = ("In this work we use a fully synthetic, deterministically generated cohort to "
                "demonstrate an automated analytic pipeline that proceeds from cohort data to a "
                "submission-ready manuscript; the clinical narrative is illustrative only."
                if nar.get("synthetic") else
                "Here we report a retrospective cohort analysis addressing this question.")
        text = (
            "Heart failure with preserved ejection fraction (HFpEF) accounts for approximately half "
            "of all heart failure cases and is associated with frequent hospital readmission and poor "
            "quality of life. Risk stratification at discharge remains difficult, and the prognostic "
            "value of routinely available variables such as natriuretic peptides and ejection fraction "
            "is incompletely characterised in real-world cohorts. Whether guideline-directed therapy is "
            "associated with a lower burden of rehospitalization in HFpEF is of particular interest "
            "because management options have historically been limited. " + tail)
        return "sec_intro", "## Introduction\n" + text

    def _t_draft_results(self, meta, nar):
        exp = nar.get("exposure_label", "the exposure")
        ref = nar.get("reference_label", "the comparator")
        out = nar.get("outcome_label", "the outcome")
        text = (
            f"Among {{{{N_TOTAL}}}} patients with HFpEF, {{{{N_EVENTS}}}} {out} events were observed "
            f"over a median follow-up of {{{{MEDIAN_FU}}}} months. Baseline characteristics by "
            f"treatment group are summarised in **Table 1**.\n\n"
            f"{{{{TABLE1}}}}\n\n"
            f"In the Kaplan-Meier analysis, {out}-free survival was higher in the {exp} group than in "
            f"the {ref} group ({{{{LOGRANK}}}}; **Figure 1**). In the multivariable Cox "
            f"proportional-hazards model, {exp} was independently associated with a "
            f"{nar.get('direction', 'different')} hazard of {out} ({{{{RESULTS_EFFECT}}}}). Higher "
            f"baseline natriuretic peptide and chronic kidney disease were associated with higher "
            f"hazards (Table 1).")
        return "sec_results", "## Results\n" + text

    def _t_draft_discussion(self, meta, nar):
        if nar.get("synthetic"):
            text = (
                "In this synthetic retrospective cohort, guideline-directed therapy was associated with "
                "longer rehospitalization-free survival after adjustment for major prognostic factors. "
                "The direction and magnitude of the association are consistent with the data-generating "
                "process and serve to validate the analytic pipeline end to end. Because the cohort is "
                "entirely synthetic, the findings carry no clinical implication and are not generalisable "
                "to real patients. Limitations include the single synthetic data source, the absence of "
                "real-world measurement error and missingness, potential residual confounding inherent to "
                "observational designs, and the use of a simplified proportional-hazards data-generating "
                "model that may bias toward the assumed effect direction. Prospective validation on real "
                "data is required before any inference can be drawn.")
        else:
            text = (
                "In this retrospective cohort, guideline-directed therapy was associated with longer "
                "rehospitalization-free survival after adjustment for major prognostic factors. "
                "Limitations include the retrospective single-source design, potential residual "
                "confounding, and the absence of randomisation; associations should not be interpreted "
                "as causal. Prospective validation is warranted.")
        return "sec_discussion", "## Discussion\n" + text

    def _t_draft_methods(self, meta, nar):
        if nar.get("synthetic"):
            origin = ("a fully synthetic HFpEF dataset comprising {{N_TOTAL}} patients generated "
                      "deterministically in software with a fixed random seed; no real patients, "
                      "hospitals or medical records were involved")
        else:
            origin = ("an HFpEF retrospective cohort comprising {{N_TOTAL}} patients assembled from "
                      "the source registry")
        text = (
            f"This was a retrospective cohort analysis of {origin}. The exposure of interest was "
            f"guideline-directed therapy (versus usual care). The primary outcome was rehospitalization, "
            f"analysed as time to first event with administrative censoring at thirty-six months and "
            f"censoring at death or loss to follow-up. Baseline characteristics were compared between "
            f"groups using Welch t tests for approximately normal continuous variables, the Mann-Whitney "
            f"U test for skewed variables (natriuretic peptide), and Pearson chi-square tests for "
            f"categorical variables. Rehospitalization-free survival was estimated with the Kaplan-Meier "
            f"method and compared with the log-rank test. A multivariable Cox proportional-hazards model "
            f"(Breslow approximation for ties) adjusted for age, sex, diabetes, atrial fibrillation, "
            f"chronic kidney disease, natriuretic peptide and ejection fraction; effect sizes are "
            f"reported as hazard ratios with 95% confidence intervals. All statistics were computed in "
            f"dependency-free Python and are exactly reproducible from the released code and seed.")
        return "sec_methods", "## Methods\n" + text

    def _t_draft_declarations(self, meta, nar):
        syn = nar.get("synthetic")
        data_avail = (
            "This study is a methodological pipeline demonstration built on a fully synthetic cohort "
            "generated deterministically by code with a fixed random seed; no real patient data were "
            "used. The synthetic dataset and the code that generates it are openly available in the "
            "project repository and can be regenerated exactly by running the released pipeline."
            if syn else
            "The data that support the findings are available from the corresponding author upon "
            "reasonable request, subject to institutional and ethical restrictions on patient data.")
        ethics = (
            "This study used a fully synthetic, computer-generated cohort; no human participants, tissue "
            "or identifiable data were involved, so institutional review board approval and informed "
            "consent were not applicable and were waived."
            if syn else
            "The study was approved by the institutional review board; informed consent was waived for "
            "this retrospective analysis of de-identified records.")
        blocks = [
            "## Figure legends",
            "**Figure 1.** Kaplan-Meier curves for rehospitalization-free survival by treatment group "
            "(guideline-directed therapy versus usual care), with the number-at-risk table below each "
            "curve; {{LOGRANK}}.",
            "",
            "## References",
            # 占位 DOI（10.0000/mock.NNN）+ 明确标注 synthetic：审核器据此判 NEEDS-REVIEW，绝不伪绿。
            "1. Author A, et al. Synthetic placeholder reference on HFpEF epidemiology (not a real "
            "publication). J Synthetic Cardiol. 2024. https://doi.org/10.0000/mock.001",
            "2. Author B, et al. Synthetic placeholder reference on natriuretic peptides (not a real "
            "publication). J Synthetic Cardiol. 2023. https://doi.org/10.0000/mock.002",
            "3. Author C, et al. Synthetic placeholder reference on cohort methodology (not a real "
            "publication). J Synthetic Methods. 2022. https://doi.org/10.0000/mock.003",
            "4. Author D, et al. Synthetic placeholder reference on guideline-directed therapy (not a "
            "real publication). J Synthetic Cardiol. 2024. https://doi.org/10.0000/mock.004",
            "",
            "## Data availability",
            data_avail,
            "",
            "## Code availability",
            "All analysis code (cohort generation, statistics and manuscript assembly) is custom and is "
            "openly available in the project repository; results are reproducible from the fixed seed.",
            "",
            "## Author contributions",
            "The automated pipeline assembled the cohort, performed the statistical analysis and drafted "
            "the manuscript; a human investigator supervised and is responsible for the final content.",
            "",
            "## Ethics",
            ethics,
            "",
            "## Funding",
            "This work received no specific external funding.",
        ]
        return "sec_declarations", "\n".join(blocks)


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


# ── HFpEF 合成队列：载入 + 真算统计（table1 / cox / km），供统计器官分化/组合 ──
def fn_load_hfpef_cohort(payload, cond):
    """计算细胞：确定性生成合成 HFpEF 回顾队列（⚠️ SYNTHETIC，非真实曙光数据）。"""
    seed = cond.get("seed", synthetic_cohort.SEED)
    n = cond.get("n", synthetic_cohort.N)
    rows = synthetic_cohort.generate_cohort(seed=seed, n=n)
    return {"cohort": rows, "dataset": "synthetic_hfpef_cohort", "seed": seed}


# 真实队列 CSV schema：列名 → 类型（真后端接线时，把曙光导出的 CSV 对齐到这些列即可）
COHORT_CSV_SCHEMA = {
    "pid": "str", "arm": "str", "age": "num", "sex": "str",
    "hypertension": "bool", "diabetes": "bool", "af": "bool", "ckd": "bool",
    "lvef": "num", "ntprobnp": "num",
    "rehospitalization": "bool", "death": "bool", "followup_months": "num",
}
_TRUE = {"1", "true", "yes", "y", "t", "是"}


def _coerce(val, typ):
    s = str(val).strip()
    if typ == "bool":
        return s.lower() in _TRUE
    if typ == "num":
        f = float(s)
        return int(f) if f.is_integer() else f
    return s


def fn_load_cohort_csv(payload, cond):
    """计算细胞：从真实队列 CSV 载入（真后端用；与合成队列**同形**，故管线下游一行不改）。

    用法：分化时给 fn=load_cohort_csv + path=<csv路径>；CSV 列须覆盖 COHORT_CSV_SCHEMA。
    sex 取值 'female'/'male'；arm 为任意两类标签（暴露组可在统计细胞用 exposure_arm 指定）。
    ⚠️ 真实患者数据敏感：放 clients/（已 gitignore），绝不入库。
    """
    import csv
    path = cond.get("path") or payload.get("cohort_csv")
    if not path:
        raise KeyError("fn_load_cohort_csv 需要 cond['path'] 或 payload['cohort_csv']")
    rows = []
    with open(path, newline="", encoding="utf-8") as fh:
        for raw in csv.DictReader(fh):
            missing = [c for c in COHORT_CSV_SCHEMA if c not in raw]
            if missing:
                raise ValueError(f"CSV 缺列：{missing}（需符合 COHORT_CSV_SCHEMA）")
            rows.append({c: _coerce(raw[c], t) for c, t in COHORT_CSV_SCHEMA.items()})
    if not rows:
        raise ValueError(f"CSV 无数据行：{path}")
    return {"cohort": rows, "dataset": f"real_cohort_csv:{path}"}


def _split_by_arm(cohort, exposure=None):
    """按 arm 分两组（label-agnostic：真实数据可用任意两类标签）。
    exposure 指定则置于首位（=Cox 暴露、Table 1 首列）；否则按字典序。"""
    distinct = sorted({r["arm"] for r in cohort})
    if len(distinct) != 2:
        raise ValueError(f"需要恰好两个 arm，实际：{distinct}")
    if exposure and exposure in distinct:
        other = [x for x in distinct if x != exposure][0]
        arms = [exposure, other]
    else:
        arms = distinct
    groups = {a: [r for r in cohort if r["arm"] == a] for a in arms}
    return arms, groups


def fn_table1(payload, cond):
    """计算细胞：基线/结局描述表（真算，含组间检验 p）。"""
    cohort = payload["cohort"]
    arms, g = _split_by_arm(cohort, cond.get("exposure_arm"))
    a, b = arms
    labels = cohort
    rows = []

    def cont_row(label, key, p_fn):
        va, vb = [r[key] for r in g[a]], [r[key] for r in g[b]]
        p = p_fn([r[key] for r in cohort if r["arm"] == a],
                 [r[key] for r in cohort if r["arm"] == b])
        return {"label": label,
                a: f"{_f1(biostats.mean(va))} ({_f1(biostats.sd(va))})",
                b: f"{_f1(biostats.mean(vb))} ({_f1(biostats.sd(vb))})",
                "p": _p_str(p)}

    def median_row(label, key):
        va, vb = [r[key] for r in g[a]], [r[key] for r in g[b]]
        p = biostats.mann_whitney_p(va, vb)
        def fmt(vals):
            return (f"{_f1(biostats.median(vals))} "
                    f"[{_f1(biostats.quantile(vals, 0.25))}-{_f1(biostats.quantile(vals, 0.75))}]")
        return {"label": label, a: fmt(va), b: fmt(vb), "p": _p_str(p)}

    def cat_row(label, pred):
        flags = [bool(pred(r)) for r in cohort]
        glab = [r["arm"] for r in cohort]
        ka = sum(1 for r in g[a] if pred(r))
        kb = sum(1 for r in g[b] if pred(r))
        p = biostats.chi2_p(flags, glab)
        return {"label": label,
                a: f"{ka} ({_pct(ka, len(g[a]))})",
                b: f"{kb} ({_pct(kb, len(g[b]))})",
                "p": _p_str(p)}

    rows.append(cont_row("Age, years, mean (SD)", "age", biostats.welch_t_p))
    rows.append(cat_row("Female sex, n (%)", lambda r: r["sex"] == "female"))
    rows.append(cat_row("Hypertension, n (%)", lambda r: r["hypertension"]))
    rows.append(cat_row("Diabetes, n (%)", lambda r: r["diabetes"]))
    rows.append(cat_row("Atrial fibrillation, n (%)", lambda r: r["af"]))
    rows.append(cat_row("Chronic kidney disease, n (%)", lambda r: r["ckd"]))
    rows.append(cont_row("LVEF, %, mean (SD)", "lvef", biostats.welch_t_p))
    rows.append(median_row("NT-proBNP, pg/mL, median [IQR]", "ntprobnp"))
    rows.append(cat_row("Rehospitalization, n (%)", lambda r: r["rehospitalization"]))
    rows.append(cat_row("All-cause death, n (%)", lambda r: r["death"]))
    rows.append(median_row("Follow-up, months, median [IQR]", "followup_months"))

    return {"table1": {
        "arms": arms,
        "n": {a: len(g[a]), b: len(g[b])},
        "rows": rows,
    }}


def _zscore(vals):
    m, s = biostats.mean(vals), biostats.sd(vals)
    s = s or 1.0
    return [(v - m) / s for v in vals], m, s


def fn_cox(payload, cond):
    """计算细胞：多变量 Cox 比例风险（真算，主结果给 HR + 95% CI）。"""
    cohort = payload["cohort"]
    time_key = cond.get("time_key", "followup_months")
    event_key = cond.get("event_key", "rehospitalization")
    arms, _ = _split_by_arm(cohort, cond.get("exposure_arm"))
    exposure = arms[0]
    times = [r[time_key] for r in cohort]
    events = [1 if r[event_key] else 0 for r in cohort]
    age_z, _, _ = _zscore([r["age"] for r in cohort])
    lognt_z, _, _ = _zscore([math.log(r["ntprobnp"]) for r in cohort])
    lvef_z, _, _ = _zscore([r["lvef"] for r in cohort])
    arm_name = f"arm_{exposure}"
    X = []
    for i, r in enumerate(cohort):
        X.append([
            1.0 if r["arm"] == exposure else 0.0,   # 暴露 vs 参照
            age_z[i],
            1.0 if r["sex"] == "female" else 0.0,
            1.0 if r["diabetes"] else 0.0,
            1.0 if r["af"] else 0.0,
            1.0 if r["ckd"] else 0.0,
            lognt_z[i],
            lvef_z[i],
        ])
    names = [arm_name, "age_z", "female", "diabetes", "af", "ckd", "lognt_z", "lvef_z"]
    label_map = {
        arm_name: f"{exposure} (vs {arms[1]})",
        "age_z": "Age (per SD)", "female": "Female sex",
        "diabetes": "Diabetes", "af": "Atrial fibrillation",
        "ckd": "Chronic kidney disease", "lognt_z": "log NT-proBNP (per SD)",
        "lvef_z": "LVEF (per SD)",
    }
    fit = biostats.cox_ph(times, events, X, names)
    pr = fit[arm_name]
    primary = {
        "name": arm_name, "exposure": exposure, "reference": arms[1],
        "hr": pr["hr"], "ci_low": pr["ci_low"], "ci_high": pr["ci_high"], "p": pr["p"],
        "hr_s": _f2(pr["hr"]), "ci_low_s": _f2(pr["ci_low"]),
        "ci_high_s": _f2(pr["ci_high"]), "p_s": _p_str(pr["p"]), "p_phrase": _p_phrase(pr["p"]),
    }
    covariates = [{
        "name": nm, "label": label_map[nm],
        "hr_s": _f2(fit[nm]["hr"]),
        "ci_s": f"{_f2(fit[nm]['ci_low'])}-{_f2(fit[nm]['ci_high'])}",
        "p_s": _p_str(fit[nm]["p"]),
    } for nm in names]
    return {"cox": {
        "model": "Cox proportional hazards (Breslow)",
        "n": len(cohort), "events": sum(events),
        "primary": primary, "covariates": covariates,
    }}


def fn_km(payload, cond):
    """计算细胞：Kaplan-Meier 生存 + log-rank（真算）。"""
    cohort = payload["cohort"]
    time_key = cond.get("time_key", "followup_months")
    event_key = cond.get("event_key", "rehospitalization")
    arms, _ = _split_by_arm(cohort, cond.get("exposure_arm"))
    times = [r[time_key] for r in cohort]
    events = [1 if r[event_key] else 0 for r in cohort]
    groups = [r["arm"] for r in cohort]
    by_arm = {}
    for arm in arms:
        idx = [i for i, gname in enumerate(groups) if gname == arm]
        steps = biostats.kaplan_meier([times[i] for i in idx], [events[i] for i in idx])
        med = biostats.km_median(steps)
        by_arm[arm] = {
            "median_survival": None if med is None else round(med, 1),
            "s12": round(biostats.km_survival_at(steps, 12), 3),
            "s24": round(biostats.km_survival_at(steps, 24), 3),
        }
    chi2, p = biostats.logrank_p(times, events, groups)
    return {"km": {
        "by_arm": by_arm,
        "logrank_chi2": round(chi2, 3), "logrank_p": p, "logrank_p_s": _p_str(p),
        "logrank_p_phrase": _p_phrase(p),
        "median_followup": round(biostats.median(times), 1),
        "median_followup_s": _f1(biostats.median(times)),
        "n_events": sum(events),
    }}


# 基建函数表：计算细胞分化时用 fn=<key> 选取
COMPUTE_FNS = {
    "load_dataset": fn_load_dataset,
    "group_compare": fn_group_compare,
    "normality": fn_normality,
    # HFpEF 合成队列 + 真算统计
    "load_hfpef_cohort": fn_load_hfpef_cohort,
    "load_cohort_csv": fn_load_cohort_csv,   # 真后端：从真实队列 CSV 载入（同形即插即用）
    "table1": fn_table1,
    "cox": fn_cox,
    "km": fn_km,
}
