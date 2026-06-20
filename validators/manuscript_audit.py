#!/usr/bin/env python3
"""投稿基础稿 · 问题审核器（科学循环第 4 步的客观验证器）

由标准驱动：读 standards/<刊>-cohort.yaml，逐条硬闸门跑 pass/fail 探针，
对稿件给出红/黄/绿审核报告 + 合格判定。

设计红线：只做客观、可从稿件量出的检查；做不到的（如引用内容是否支持论点、
是否撤稿）明确标 NEEDS-REVIEW，绝不伪绿 —— 不让程序/模型自判自作业。

用法：  python3 -m validators.manuscript_audit [manuscript.md] [standard.yaml]
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent

# 状态
PASS, FAIL, REVIEW, MANUAL, NA = "🟢 PASS", "🔴 FAIL", "🟡 REVIEW", "⬜ MANUAL", "·  N/A"


# ── 解析稿件 ────────────────────────────────────────────────────────────
def parse(text: str) -> dict:
    title, sections, cur, buf = "", {}, None, []
    for ln in text.splitlines():
        if ln.startswith("## "):
            if cur is not None:
                sections[cur] = "\n".join(buf).strip()
            cur, buf = ln[3:].strip().lower(), []
        elif ln.startswith("# "):
            title = ln[2:].strip()
        elif cur is not None:
            buf.append(ln)
    if cur is not None:
        sections[cur] = "\n".join(buf).strip()
    return {"title": title, "sec": sections}


def sec(m, *names):
    for n in names:
        for k, v in m["sec"].items():
            if n in k:
                return v
    return None


def words(s):
    return len((s or "").split())


# ── 探针：gate id -> (status, 详情) ──────────────────────────────────────
def p_title_format(m):
    t = m["title"]
    if not t:
        return FAIL, "缺标题"
    issues = []
    if len(t) > 120:
        issues.append(f"过长 {len(t)} 字符")
    if re.search(r"\b[A-Z]{2,}\b", re.sub(r"\b(LVEF|HFpEF|HFrEF)\b", "", t)):
        issues.append("含缩写")
    if t.rstrip().endswith("."):
        issues.append("末尾有句点")
    return (FAIL, "；".join(issues)) if issues else (PASS, f"{len(t)} 字符、无缩写")


def p_abstract_format(m):
    a = sec(m, "abstract", "摘要")
    if a is None:
        return FAIL, "缺摘要"
    w = words(a)
    issues = []
    if w > 150:
        issues.append(f"{w} 词 >150")
    if re.search(r"\[\d+\]|\bet al\.?|（\d+）|\(\d{4}\)", a):
        issues.append("含文献引用")
    return (FAIL, "；".join(issues)) if issues else (PASS, f"{w} 词、无引用")


def p_imrad(m):
    order = ["introduction", "results", "discussion", "methods"]
    pos = [next((i for i, k in enumerate(m["sec"]) if o in k), -1) for o in order]
    missing = [o for o, p in zip(order, pos) if p < 0]
    if missing:
        return FAIL, "缺章节：" + ", ".join(missing)
    seen = [p for p in pos if p >= 0]
    return (PASS, "IMRAD 齐全且有序") if seen == sorted(seen) else (FAIL, "章节顺序不对")


def p_main_words(m):
    w = sum(words(sec(m, n) or "") for n in ("introduction", "results", "discussion"))
    return (PASS, f"{w} 词 ≤4500") if w <= 4500 else (FAIL, f"{w} 词 >4500")


def p_methods_words(m):
    w = words(sec(m, "methods") or "")
    return (PASS, f"{w} 词 ≤3000") if w <= 3000 else (FAIL, f"{w} 词 >3000")


def _legends(m):
    leg = sec(m, "figure legend", "legend", "图注") or ""
    return re.split(r"(?=\*\*(?:Figure|Fig|图)\s*\d+)", leg)[1:]


def p_display_items(m):
    body = "\n".join(m["sec"].values())
    figs = set(re.findall(r"\*\*(?:Figure|Fig|图)\s*(\d+)", body))
    tabs = set(re.findall(r"\*\*(?:Table|表)\s*(\d+)", body))
    n = len(figs) + len(tabs)
    return (PASS, f"图{len(figs)}+表{len(tabs)}={n} ≤6") if n <= 6 else (FAIL, f"{n} >6")


def p_refs(m):
    r = sec(m, "reference", "参考")
    if r is None:
        return FAIL, "缺参考文献"
    items = [ln for ln in r.splitlines() if re.match(r"\s*(\d+[\.\)]|-)\s", ln)]
    n = len(items)
    return (PASS, f"{n} 条 ≤50") if n <= 50 else (FAIL, f"{n} 条 >50")


def p_fig_legends(m):
    over = [i + 1 for i, lg in enumerate(_legends(m)) if words(lg) > 350]
    if not _legends(m):
        return REVIEW, "未找到图注段"
    return (PASS, "各图注 ≤350 词") if not over else (FAIL, f"图注超长：{over}")


def _has(m, *names, kw=()):
    s = sec(m, *names)
    if s is None:
        return None
    if kw and not any(k.lower() in s.lower() for k in kw):
        return False
    return True


def _present_probe(*names, kw=(), label=""):
    def probe(m):
        r = _has(m, *names, kw=kw)
        if r is None:
            return FAIL, f"缺『{label or names[0]}』段"
        if r is False:
            return FAIL, f"『{label or names[0]}』缺关键要素 {kw}"
        return PASS, "存在且要素齐全"
    return probe


def p_citation_auth(m):
    r = sec(m, "reference", "参考") or ""
    items = [ln for ln in r.splitlines() if re.match(r"\s*(\d+[\.\)]|-)\s", ln)]
    if not items:
        return FAIL, "无参考条目"
    no_doi = [i + 1 for i, ln in enumerate(items) if not re.search(r"10\.\d{4,9}/\S+", ln)]
    if no_doi:
        return FAIL, f"{len(no_doi)} 条缺规范 DOI：{no_doi[:8]}"
    return REVIEW, f"{len(items)} 条 DOI 格式合规；内容是否支持论点/是否撤稿需跨库核对（离线无法判定）"


def p_effect_ci(m):
    res = sec(m, "results") or ""
    return (PASS, "主结果含置信区间") if re.search(r"95%\s*CI|置信区间|confidence interval", res, re.I) \
        else (FAIL, "结果未见 95% CI/置信区间")


def p_table1(m):
    body = "\n".join(m["sec"].values())
    return (PASS, "存在 Table 1") if re.search(r"\*\*(?:Table|表)\s*1\b", body) \
        else (FAIL, "未见基线特征表 Table 1")


def p_design_named(m):
    t = (m["title"] + " " + (sec(m, "abstract") or "")).lower()
    return (PASS, "标题/摘要点明队列") if ("cohort" in t or "队列" in t) \
        else (FAIL, "标题/摘要未点明 cohort/队列")


def p_internal_consistency(m):
    ab, res = sec(m, "abstract") or "", sec(m, "results") or ""
    nums = set(re.findall(r"\b\d+\.\d+\b", ab))
    miss = [n for n in nums if n not in res]
    if not nums:
        return REVIEW, "摘要无可比对数字"
    return (PASS, "摘要数字均见于结果") if not miss else (FAIL, f"摘要数字未见于结果：{miss}")


PROBES = {
    "title_format": p_title_format,
    "abstract_format": p_abstract_format,
    "imrad_structure": p_imrad,
    "main_text_wordlimit": p_main_words,
    "methods_wordlimit": p_methods_words,
    "display_items": p_display_items,
    "references_count_style": p_refs,
    "figure_legends": p_fig_legends,
    "data_availability": _present_probe("data availability", "数据可得", label="Data availability",
                                        kw=("available", "request", "repository", "accession", "restrict", "contact")),
    "code_availability": _present_probe("code availability", "代码可得", label="Code availability"),
    "author_contributions": _present_probe("author contribution", "作者贡献", label="Author contributions"),
    "competing_interests": _present_probe("competing interest", "conflict", "利益冲突", label="Competing interests"),
    "ethics_statement": _present_probe("ethic", "irb", "institutional review", "伦理", label="Ethics",
                                       kw=("approv", "review board", "consent", "伦理", "豁免")),
    "strobe_funding": _present_probe("funding", "资金", "financial support", label="Funding"),
    "strobe_table1": p_table1,
    "strobe_design_named": p_design_named,
    "strobe_effect_ci": p_effect_ci,
    "citation_authenticity": p_citation_auth,
    "internal_consistency": p_internal_consistency,
}


# ── 跑审核 ──────────────────────────────────────────────────────────────
def audit(manuscript_path: Path, standard_path: Path) -> int:
    std = yaml.safe_load(standard_path.read_text())
    m = parse(manuscript_path.read_text())

    print(f"问题审核报告 · {std['meta']['journal']}")
    print(f"稿件：{manuscript_path.name}　标准：{standard_path.name} (v{std['meta']['version']})")
    print("=" * 72)

    reds, reviews = [], []
    print("\n【硬闸门】")
    for g in std["hard_gates"]:
        probe = PROBES.get(g["id"])
        if probe is None:
            status, detail = (MANUAL, "需人工") if g.get("check") == "manual" else (NA, "未实现探针")
        else:
            status, detail = probe(m)
        if status == FAIL:
            reds.append(g["id"])
        elif status == REVIEW:
            reviews.append(g["id"])
        print(f"  {status}  [{g['layer']}] {g['id']:<24} {detail}")

    print("\n【质量评分项】（多为人工/半自动，此处仅跑可自动项）")
    for q in std["quality_scores"]:
        probe = PROBES.get(q["id"])
        status, detail = probe(m) if probe else (MANUAL, "需人工评分")
        print(f"  {status}  {q['id']:<24} (权重{q['weight']}) {detail}")

    print("\n" + "=" * 72)
    auto_total = sum(1 for g in std["hard_gates"] if g["id"] in PROBES)
    if reds:
        verdict = f"🔴 不合格：{len(reds)} 条硬闸门未过 → {reds}"
    elif reviews:
        verdict = f"🟡 待外部/人工复核：自动探针全过，但 {len(reviews)} 条需跨库或人工核对 → {reviews}"
    else:
        verdict = "🟢 自动探针全过（人工/外部条目仍需复核后方可定『合格』）"
    print(f"结论：{verdict}")
    print(f"（已自动判定 {auto_total}/{len(std['hard_gates'])} 条硬闸门；其余为人工/半自动条目）")
    return 1 if reds else 0


def main():
    mp = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "validators" / "sample_manuscript.md"
    sp = Path(sys.argv[2]) if len(sys.argv) > 2 else ROOT / "standards" / "nature-cohort.yaml"
    sys.exit(audit(mp, sp))


if __name__ == "__main__":
    main()
