"""能力内核 · M2 全自动管线入口（模拟数据 → 统计 → 生成稿件 → 审核 → 自修订收敛）

把缺的前半段补齐：科学循环过去从一份**预写**的 sample_manuscript 起步，
现在改由**合成队列数据**经「统计器官 → 写作器官」**自动生成**首稿，再交给科学循环收敛。

全程**离线、无 API Key、确定性可复现**（⚠️ 数据与文本均为 SYNTHETIC，非真实曙光数据/真实文献）。

装配方式严格沿用现有 kernel 范式：
  · 分化 differentiate：在 stem_compute 上分化出 table1/cox/km 统计细胞；
                        在 stem_llm 上分化出 draft_* 写作细胞。
  · 组合 compose：统计细胞 → 分析器官(产出 stats)；写作细胞 → 写作器官(产出 manuscript)。
  · 神经编排 Orchestrator：按契约 consumes/produces 反向链式自动装配 data→stats→draft，无手工管线。

即插即用：把 Context(llm=MockLLM()) 换成 Context(llm=AnthropicLLM()) 即接真实模型，管线结构一行不改。

运行：  python3 -m kernel.pipeline
"""
from __future__ import annotations

from pathlib import Path

from . import scientific_loop
from .backends import COMPUTE_FNS, MockLLM
from .core import Context, Registry, compose, differentiate, stem_compute, stem_llm
from .orchestrator import Orchestrator
from validators import manuscript_audit

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "out"

# 研究元数据（SYNTHETIC）：写作细胞模板化的非数值部分由此提供；数值一律取自真算 stats。
STUDY_META = {
    "journal": "Nature Cardiovascular Research",
    "study_type": "retrospective_cohort",
    "disease": "HFpEF",
    "exposure": "guideline-directed therapy",
    "outcome": "rehospitalization",
    "synthetic": True,
}


# ── 组合 wiring ───────────────────────────────────────────────────────────
def analysis_wiring(payload, members, ctx):
    """分析器官：顺序跑 table1/cox/km 统计细胞（各自消费 cohort），打包成结构化 stats。"""
    state = dict(payload)
    for cell in members:
        state.update(cell.run(state, ctx))
    stats = {
        "n_total": len(state["cohort"]),
        "table1": state["table1"],
        "cox": state["cox"],
        "km": state["km"],
    }
    return {"stats": stats}


SECTION_ORDER = [
    "sec_title", "sec_abstract", "sec_intro", "sec_results",
    "sec_discussion", "sec_methods", "sec_declarations",
]


def writing_wiring(payload, members, ctx):
    """写作器官：用 meta+stats 跑各 draft 细胞，按 IMRAD 顺序拼成 manuscript.md。"""
    slim = {"meta": payload["meta"], "stats": payload["stats"]}
    for cell in members:
        slim.update(cell.run(slim, ctx))
    title = slim["sec_title"]
    parts = ["# " + title]
    for key in SECTION_ORDER[1:]:
        parts.append(slim[key])
    manuscript = "\n\n".join(parts).rstrip() + "\n"
    return {"manuscript": manuscript}


# ── 生长细胞池 + 组合器官（带契约，供编排器自动装配） ──────────────────────
def build_pipeline(reg: Registry):
    comp = stem_compute(reg)
    llm = stem_llm(reg)

    def diff(base, name, cond, consumes, produces, desc=""):
        cap = differentiate(reg, base, name, cond, desc=desc)
        cap.consumes, cap.produces = set(consumes), set(produces)
        return cap

    # 计算干细胞 → 数据细胞 + 三个统计细胞（真算）
    load = diff(comp, "load_hfpef·载入合成队列", {"fn": "load_hfpef_cohort"},
                consumes=[], produces=["cohort"], desc="确定性生成合成 HFpEF 队列")
    c_table1 = diff(comp, "table1·基线描述表", {"fn": "table1"},
                    consumes=["cohort"], produces=["table1"], desc="基线/结局描述+组间检验")
    c_cox = diff(comp, "cox·比例风险", {"fn": "cox"},
                 consumes=["cohort"], produces=["cox"], desc="多变量 Cox，HR+95%CI")
    c_km = diff(comp, "km·生存分析", {"fn": "km"},
                consumes=["cohort"], produces=["km"], desc="Kaplan-Meier + log-rank")

    # 组合：三个统计细胞 → 分析器官（产出结构化 stats）
    analysis_organ = compose(reg, "analysis_organ·统计分析器官",
                             [c_table1, c_cox, c_km], analysis_wiring,
                             desc="组合统计细胞，输出 stats")
    analysis_organ.consumes, analysis_organ.produces = {"cohort"}, {"stats"}

    # 语言干细胞 → 七个 draft 写作细胞（模板化，数字取自 stats）
    draft_specs = [
        ("draft_title·标题", "draft_title", "sec_title"),
        ("draft_abstract·摘要", "draft_abstract", "sec_abstract"),
        ("draft_intro·引言", "draft_intro", "sec_intro"),
        ("draft_results·结果(含Table1+HR/CI)", "draft_results", "sec_results"),
        ("draft_discussion·讨论", "draft_discussion", "sec_discussion"),
        ("draft_methods·方法", "draft_methods", "sec_methods"),
        ("draft_declarations·必备声明", "draft_declarations", "sec_declarations"),
    ]
    draft_cells = []
    for name, task, produces in draft_specs:
        cell = diff(llm, name, {"task": task, "instruction": f"撰写 {produces} 章节"},
                    consumes=["meta", "stats"], produces=[produces],
                    desc="模板化生成稿件章节（SYNTHETIC）")
        draft_cells.append(cell)

    # 组合：七个写作细胞 → 写作器官（产出 manuscript）
    writing_organ = compose(reg, "writing_organ·写作器官",
                            draft_cells, writing_wiring, desc="组合 draft 细胞，输出 manuscript.md")
    writing_organ.consumes, writing_organ.produces = {"meta", "stats"}, {"manuscript"}

    return {"load": load, "analysis_organ": analysis_organ, "writing_organ": writing_organ}


# ── 打印谱系 / 执行轨迹 ────────────────────────────────────────────────────
def print_lineage(reg: Registry):
    print("谱系（细胞 → 器官，分化/组合的来源可追溯）")
    print("-" * 72)
    for cap in reg.all():
        parents = ", ".join(cap.parents) if cap.parents else "—"
        io = ""
        if cap.consumes or cap.produces:
            io = f"  [{','.join(sorted(cap.consumes)) or '∅'} → {','.join(sorted(cap.produces)) or '∅'}]"
        print(f"  {cap.id:<28} {cap.kind:<14} ←({parents}){io}")


def main():
    print("M2 全自动管线 —— 模拟数据 → 统计(真算) → 生成稿件 → 审核 → 自修订收敛")
    print("⚠️  数据与文本均为 SYNTHETIC（非真实曙光数据/真实文献）；离线确定性可复现。")
    print("=" * 72)

    reg = Registry()
    organs = build_pipeline(reg)
    ctx = Context(llm=MockLLM(), compute=COMPUTE_FNS)

    print()
    print_lineage(reg)

    # 神经编排：按契约自动装配 data→stats→draft，无手工管线
    brain = Orchestrator(reg)
    plan, state = brain.achieve("manuscript", {"meta": STUDY_META}, ctx)

    print("\n神经编排：目标『manuscript』→ 自动装配通路（按 consumes/produces 反向推理）")
    print("-" * 72)
    print("  " + " → ".join(c.name.split("·")[0] for c in plan))

    print("\n执行轨迹（trace）")
    print("-" * 72)
    for cap_id, note in ctx.trace:
        print(f"  {cap_id:<28} {note}")

    cox = state["stats"]["cox"]["primary"]
    print("\n真算主结果（写入稿件的数字均源于此）")
    print("-" * 72)
    print(f"  调整后 Cox HR(GDT vs Usual) = {cox['hr_s']} "
          f"(95% CI {cox['ci_low_s']}-{cox['ci_high_s']}), P {cox['p_phrase']}")
    print(f"  log-rank P {state['stats']['km']['logrank_p_phrase']}; "
          f"事件 {state['stats']['cox']['events']}/{state['stats']['n_total']}")

    # 写出自动生成的首稿
    OUT_DIR.mkdir(exist_ok=True)
    gen_path = OUT_DIR / "hfpef_pipeline_manuscript.md"
    gen_path.write_text(state["manuscript"])
    print(f"\n自动生成首稿已写出：{gen_path.relative_to(ROOT)}（{len(state['manuscript'].split())} 词）")

    # 交给科学循环：audit → revise 单调收敛
    print("\n" + "=" * 72)
    print("交接科学循环（OODA）：审核 → 自修订 → 单调收敛")
    print("=" * 72)
    std_path = ROOT / "standards" / "nature-cohort.yaml"
    scientific_loop.run(gen_path, std_path)

    # 独立复验（红线：完成与否由审核器判定，不让模型自判）
    converged = gen_path.with_name(gen_path.stem + ".converged.md")
    print("\n" + "=" * 72)
    print("独立复验：python3 -m validators.manuscript_audit " + str(converged.relative_to(ROOT)))
    print("=" * 72)
    rc = manuscript_audit.audit(converged, std_path)
    print("\n（citation_authenticity 为占位 DOI → 诚实 NEEDS-REVIEW，绝不伪绿；需接真实文献库跨库核对。）")
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
