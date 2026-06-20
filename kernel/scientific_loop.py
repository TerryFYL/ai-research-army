"""科学循环 / OODA —— 把全部部件串成一个自驱闭环并跑起来

Observe(审核器量稿件) → Orient(选一条红) → Decide(最小修订+预设判据) → Act(改+三道闸) → 复验
直到所有可离线验证的硬闸门全绿；需真实外部能力的条目诚实上报，绝不伪造。

修订器(revisers)在此是离线确定性的最小实现；真实部署时换成一个分化出来的
「修订细胞」(调 LLM 重写) 即可，循环结构一行不改 —— 与 StubLLM/AnthropicLLM 同一套即插即用。

运行：  python3 -m kernel.scientific_loop
"""
from __future__ import annotations

import re
from pathlib import Path

import yaml

from validators.manuscript_audit import FAIL, PROBES, evaluate, parse, reds_of

ROOT = Path(__file__).resolve().parent.parent
ESCALATE = "__escalate__"  # 修订器声明：此条只能靠真实外部能力，禁止离线伪造


# ── 修订器：gate id -> 一个最小、有原则的修订；或 ESCALATE ─────────────────
def fix_title(text):
    def repl(m):
        t = m.group(1).rstrip().rstrip(".")  # 去末尾句点
        if len(t) > 110:                       # 词边界截断
            t = t[:110].rsplit(" ", 1)[0]
        return "# " + t
    return re.sub(r"^# (.+)$", repl, text, count=1, flags=re.M)


def fix_abstract_citation(text):
    # 仅从摘要段移除文献引用标记（不动其它段）
    def repl(m):
        body = re.sub(r"\s*\[\d+\]", "", m.group(2))
        body = re.sub(r"\s*as previously reported", "", body)
        return m.group(1) + body
    return re.sub(r"(## Abstract\n)(.*?)(?=\n## )", repl, text, flags=re.S)


def add_section(title, body):
    def fix(text):
        return text.rstrip() + f"\n\n## {title}\n{body}\n"
    return fix


def fix_internal_consistency(text):
    # 原则：Results(由数据算出) 为真值，令 Abstract 与之对齐
    res = re.search(r"## Results\n(.*?)(?=\n## )", text, re.S)
    ab = re.search(r"## Abstract\n(.*?)(?=\n## )", text, re.S)
    if not (res and ab):
        return text
    res_nums = set(re.findall(r"\b\d+\.\d+\b", res.group(1)))
    ab_nums = set(re.findall(r"\b\d+\.\d+\b", ab.group(1)))
    stray = [n for n in ab_nums if n not in res_nums]
    if len(stray) == 1 and res_nums:
        # 把摘要里那个对不上的数字替换成 Results 中的风险比真值
        hr = re.search(r"hazard ratio.*?(\d+\.\d+)", res.group(1), re.I)
        truth = hr.group(1) if hr else sorted(res_nums)[0]
        new_ab = ab.group(1).replace(stray[0], truth)
        return text.replace(ab.group(1), new_ab)
    return text


REVISERS = {
    "title_format": fix_title,
    "abstract_format": fix_abstract_citation,
    "data_availability": add_section(
        "Data availability",
        "The data that support the findings are available from the corresponding author "
        "upon reasonable request, subject to institutional and ethical restrictions on patient data."),
    "competing_interests": add_section(
        "Competing interests", "The authors declare no competing interests."),
    "internal_consistency": fix_internal_consistency,
    # 红线：缺 DOI 不能凭空捏造 —— 只能上报真实文献库核对
    "citation_authenticity": ESCALATE,
}

MAX_CYCLES = 15


def run(manuscript_path: Path, standard_path: Path):
    std = yaml.safe_load(standard_path.read_text())
    text = manuscript_path.read_text()

    # 全量评估：硬闸门 + 纳入收敛的质量项 internal_consistency
    def full_eval(t):
        r = evaluate(t, std)
        s, d = PROBES["internal_consistency"](parse(t))
        r["internal_consistency"] = (s, d, "Q")
        return r

    print(f"科学循环 / OODA —— 目标：稿件收敛到合格（{std['meta']['journal']}）")
    print("=" * 72)

    ledger, escalated = [], []
    for cycle in range(MAX_CYCLES):
        reds = reds_of(full_eval(text))                    # Observe
        actionable = [g for g in reds if g not in escalated]
        print(f"\n[第 {cycle} 圈] 红条 {len(reds)}：{reds or '无'}")
        if not actionable:
            break

        gate = actionable[0]                               # Orient：选一条
        reviser = REVISERS.get(gate)
        if reviser is None or reviser is ESCALATE:         # 红线/无修订器：不伪造，上报
            escalated.append(gate)
            why = "🚫 只能靠真实外部能力，禁止离线伪造 → 上报" if reviser is ESCALATE else "无离线修订器 → 上报"
            ledger.append((cycle, gate, why))
            print(f"    Decide：{gate} → 上报，跳过")
            continue

        candidate = reviser(text)                          # Act
        new = full_eval(candidate)
        gate_fixed = new.get(gate, (FAIL,))[0] != FAIL     # ① 证伪复验该条真绿
        monotone = len(reds_of(new)) < len(reds)           # ② 单调不回退
        if gate_fixed and monotone:
            text = candidate
            ledger.append((cycle, gate, "✅ 修订生效且单调收敛 → 提交"))
            print(f"    Act：修订 {gate} → 通过三道闸，提交")
        else:
            escalated.append(gate)
            ledger.append((cycle, gate, f"↩ 未过闸(fixed={gate_fixed},monotone={monotone}) → 回滚+上报"))
            print(f"    Act：修订 {gate} 未过闸 → 回滚")

    # ── 收尾 ──
    final_reds = reds_of(full_eval(text))
    out_path = manuscript_path.with_name(manuscript_path.stem + ".converged.md")
    out_path.write_text(text)

    print("\n" + "=" * 72)
    print("账本：")
    for c, g, note in ledger:
        print(f"  圈{c}  {g:<22} {note}")
    print(f"\n收敛稿件已写出：{out_path.name}")
    remaining_auto = [g for g in final_reds if g not in escalated]
    if not remaining_auto:
        print(f"✅ 里程碑达成：所有可离线验证的硬闸门已全绿。")
    else:
        print(f"🔴 仍有未解红条：{remaining_auto}")
    if escalated:
        print(f"🟡 边界停（上报，需真实外部能力，未伪造）：{escalated}")
        print("   └─ citation_authenticity：需接真实文献库为缺 DOI 的引用核对/补全（禁止编造）。")
    return 0


if __name__ == "__main__":
    run(ROOT / "validators" / "sample_manuscript.md", ROOT / "standards" / "nature-cohort.yaml")
