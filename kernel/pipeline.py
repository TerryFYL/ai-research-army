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

import os
from pathlib import Path

from . import scientific_loop
from .backends import (
    ALLOWED_TOKENS, COMPUTE_FNS, ClaudeAuthoredLLM, MockLLM,
    apply_tokens, build_tokens,
)
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


def make_narrative(meta: dict, stats: dict) -> dict:
    """从真算 stats 派生**定性**叙事方向（不含原始数字）——供写作细胞写对方向。"""
    cox = stats["cox"]["primary"]
    return {
        "exposure_label": meta.get("exposure", "the exposure"),
        "reference_label": "usual care",
        "outcome_label": meta.get("outcome", "the outcome"),
        "direction": "lower" if cox["hr"] < 1 else "higher",
        "significant": bool(cox["p"] < 0.05),
        "synthetic": bool(meta.get("synthetic")),
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
    """写作器官：写作细胞产「散文+token」(无数字)，代码侧用真算 stats 回填 token，再按 IMRAD 拼装。

    红线·数字归代码：稿件里每个数字都经 build_tokens/apply_tokens 由真算结果产生，
    写作细胞（含将来的真 Claude）从不接触原始数字 → 不可能篡改或编造。
    """
    meta, stats = payload["meta"], payload["stats"]
    nar = make_narrative(meta, stats)
    slim = {"meta": meta, "narrative": nar}
    for cell in members:
        slim.update(cell.run(slim, ctx))
    tokens = build_tokens(stats)
    parts = ["# " + apply_tokens(slim["sec_title"], tokens)]
    for key in SECTION_ORDER[1:]:
        parts.append(apply_tokens(slim[key], tokens))
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

    # 语言干细胞 → 七个 draft 写作细胞（只写「散文 + token」，数字由代码回填）
    # instruction 为**真模型可直接执行**的指令：MockLLM 读 task 分派；真 Claude 读 instruction。
    base_rule = (
        "You are drafting one section of a retrospective-cohort manuscript. Write only natural-language "
        "prose. Do NOT write, compute, estimate or invent any numbers, sample sizes, statistics, "
        "p-values, confidence intervals, percentages or citations. Where a number, the baseline table, "
        "or an effect estimate belongs, insert the EXACT literal placeholder token (e.g. {{N_TOTAL}}); "
        "verified computed values are substituted by code afterwards. Allowed tokens: "
        + ", ".join(ALLOWED_TOKENS) + ". ")
    draft_specs = [
        ("draft_title·标题", "draft_title", "sec_title",
         "Write a concise title (<=66 characters, no abbreviations except HFpEF/LVEF/NT-proBNP, no "
         "trailing period) that names the cohort design, exposure and outcome. Return only the title text."),
        ("draft_abstract·摘要", "draft_abstract", "sec_abstract",
         base_rule + "Write '## Abstract' then <=150 words, no reference markers; use tokens "
         "{{N_TOTAL}}, {{N_EVENTS}}, {{ABSTRACT_EFFECT}} for all quantitative claims."),
        ("draft_intro·引言", "draft_intro", "sec_intro",
         base_rule + "Write '## Introduction': background, knowledge gap, and study aim. No numbers."),
        ("draft_results·结果(含Table1+HR/CI)", "draft_results", "sec_results",
         base_rule + "Write '## Results'; place {{TABLE1}} for the baseline table and use {{N_TOTAL}}, "
         "{{N_EVENTS}}, {{MEDIAN_FU}}, {{LOGRANK}}, {{RESULTS_EFFECT}}; reference Table 1 and Figure 1."),
        ("draft_discussion·讨论", "draft_discussion", "sec_discussion",
         base_rule + "Write '## Discussion': interpretation, then an explicit limitations sentence; "
         "avoid causal language for an observational design. No numbers."),
        ("draft_methods·方法", "draft_methods", "sec_methods",
         base_rule + "Write '## Methods' (<=3000 words): design, exposure/outcome definitions, "
         "censoring, and the statistical tests (Welch t, Mann-Whitney, chi-square, Kaplan-Meier, "
         "log-rank, multivariable Cox with HR+95%CI). Use {{N_TOTAL}} for the cohort size only."),
        ("draft_declarations·必备声明", "draft_declarations", "sec_declarations",
         base_rule + "Emit '## Figure legends' (Figure 1 KM legend with {{LOGRANK}}), '## References' "
         "(numbered; every entry MUST carry a DOI; never fabricate a real DOI — use a clearly-marked "
         "placeholder if unknown), and the statements: Data availability, Code availability, Author "
         "contributions, Ethics, Funding."),
    ]
    draft_cells = []
    for name, task, produces, instruction in draft_specs:
        cell = diff(llm, name, {"task": task, "instruction": instruction},
                    consumes=["meta", "narrative"], produces=[produces],
                    desc="写作细胞：散文+token（数字归代码，SYNTHETIC）")
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

    # 写作后端可选：LLM_BACKEND=mock（默认离线桩）｜claude（本会话 Claude 亲笔，真模型跑通）｜
    # api（真实 AnthropicLLM，需 key+网络+SDK）。三者接口一致，管线结构一行不改。
    backend = os.environ.get("LLM_BACKEND", "mock").lower()
    if backend == "claude":
        llm_backend, tag = ClaudeAuthoredLLM(), "ClaudeAuthoredLLM（真模型亲笔·捕获回放）"
    elif backend == "api":
        from .backends import AnthropicLLM
        llm_backend, tag = AnthropicLLM(), "AnthropicLLM（真实 API·实时调用）"
    else:
        llm_backend, tag = MockLLM(), "MockLLM（离线模板桩）"
    print(f"写作后端：{tag}")

    reg = Registry()
    organs = build_pipeline(reg)
    ctx = Context(llm=llm_backend, compute=COMPUTE_FNS)

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
