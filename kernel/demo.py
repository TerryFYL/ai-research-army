"""能力内核 · 跑通演示

用医学科研域的一个最小真实切片，证明"分化 + 组合"机制成立：
  1. 两个干细胞（语言细胞 / 计算细胞）
  2. 分化：一个干细胞 -> 多个专门细胞（一生多）
  3. 组合：多个专门细胞 -> 器官 -> 系统（多合一，且递归嵌套）
  4. 端到端跑一遍，全程离线确定性。

运行：  python3 -m kernel.demo
"""
from __future__ import annotations

import json

from .backends import COMPUTE_FNS, StubLLM
from .core import Context, Registry, compose, differentiate, sequential, stem_compute, stem_llm

SAMPLE_CASE = "患者女，67岁，诊断慢性心力衰竭，入院 LVEF 38%，随访 12 个月，期间因心衰再入院一次。"


def build(reg: Registry):
    # ── 干细胞 ──
    llm = stem_llm(reg)
    comp = stem_compute(reg)

    # ── 分化：一个语言干细胞 -> 三个专门语言细胞 ──
    extract_baseline = differentiate(
        reg, llm, "extract_baseline·抽取基线",
        {"task": "extract_baseline", "instruction": "从病例文本抽取年龄/性别/LVEF"},
        desc="语言细胞 + 基线抽取条件")
    extract_endpoint = differentiate(
        reg, llm, "extract_endpoint·抽取终点",
        {"task": "extract_endpoint", "instruction": "抽取再入院与随访时长"},
        desc="语言细胞 + 终点抽取条件")
    interpret = differentiate(
        reg, llm, "interpret·结果解读",
        {"task": "interpret", "instruction": "用一句话解读组间比较结果"},
        desc="语言细胞 + 解读条件")

    # ── 分化：一个计算干细胞 -> 两个专门计算细胞 ──
    load = differentiate(
        reg, comp, "load_cohort·载入队列",
        {"fn": "load_dataset", "name": "heartfailure_demo"},
        desc="计算细胞 + 载入条件")
    compare = differentiate(
        reg, comp, "group_compare·组间比较",
        {"fn": "group_compare", "group_key": "arm", "value_key": "lvef"},
        desc="计算细胞 + 组间比较条件")

    # ── 组合：专门细胞 -> 器官 ──
    profile = compose(
        reg, "profile_cohort·队列分析器官", [load, compare], sequential,
        desc="载入 + 组间比较")

    # ── 组合：器官 + 语言细胞 -> 系统（递归：组合体里嵌套组合体）──
    system = compose(
        reg, "case_to_finding·病例到结论系统",
        [extract_baseline, extract_endpoint, profile, interpret], sequential,
        desc="抽取 + 队列分析 + 解读")

    return system


def lineage_report(reg: Registry) -> str:
    caps = reg.all()
    by_id = {c.id: c for c in caps}
    lines = ["能力谱系 (Capability Lineage)", "=" * 56]
    for s in (c for c in caps if c.kind == "stem"):
        lines.append(f"[干细胞] {s.name}")
        for k in (c for c in caps if c.kind == "differentiated" and s.id in c.parents):
            cond = ", ".join(f"{kk}={vv}" for kk, vv in k.conditions.items() if kk in ("task", "fn"))
            lines.append(f"   └─[分化] {k.name}  (+条件: {cond})")
    lines.append("")
    for c in (c for c in caps if c.kind == "composed"):
        members = " + ".join(by_id[p].name.split("·")[0] for p in c.parents)
        lines.append(f"[组合] {c.name}\n          ← {members}")
    return "\n".join(lines)


def main() -> None:
    reg = Registry()
    system = build(reg)

    print(lineage_report(reg))
    print("\n" + "=" * 56)
    print("端到端运行 (输入一段病例文本 + 一个队列数据集名)")
    print("=" * 56)

    ctx = Context(llm=StubLLM(), compute=COMPUTE_FNS)
    result = system.run({"case_text": SAMPLE_CASE, "dataset": "heartfailure_demo"}, ctx)

    for key in ("baseline", "endpoint", "comparison", "interpretation"):
        if key in result:
            print(f"\n· {key}:")
            print("  " + json.dumps(result[key], ensure_ascii=False, indent=2).replace("\n", "\n  "))

    print(f"\n执行轨迹：{len(ctx.trace)} 步")


if __name__ == "__main__":
    main()
