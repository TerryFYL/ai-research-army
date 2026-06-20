"""能力内核 · 临界质量实验（能力随"量"相变）

验证一个判断：复杂任务的可达性不是线性长出来的，而是**到了临界连通度才突然点亮**。
我们在自己的细胞图上量这条曲线，而不是借 LLM 的故事。

关键机制：一个细胞只有当它的输入（consumes）已经可达时才"活"。
所以有效的不是细胞的"数量"，是**连起来的数量**。量不够 / 没连起来 → 复杂目标一直是 0。

运行：  python3 -m kernel.emergence
"""
from __future__ import annotations

# 细胞契约：(显示名, 消费集, 产物)。这是一张论文生产的能力依赖图。
CELLS = {
    "clean":       ({"raw_data"},                                              "clean_data"),
    "profile":     ({"clean_data"},                                            "data_profile"),
    "table1":      ({"clean_data"},                                            "table1"),
    "hypo":        ({"data_profile"},                                          "hypotheses"),
    "method":      ({"hypotheses", "clean_data"},                             "method"),
    "results":     ({"method", "clean_data"},                                 "results"),
    "km":          ({"results"},                                              "km_curve"),
    "forest":      ({"results"},                                              "forest_plot"),
    "interpret":   ({"results"},                                              "interpretation"),
    "base":        ({"case_text"},                                            "baseline"),
    "search":      ({"topic"},                                                "lit_pool"),
    "verify":      ({"lit_pool"},                                             "refs"),
    "intro":       ({"refs", "topic"},                                        "intro_section"),
    "methods_sec": ({"method"},                                              "methods_section"),
    "results_sec": ({"results", "table1", "km_curve"},                       "results_section"),
    "discuss":     ({"interpretation", "refs"},                              "discussion_section"),
    "draft":       ({"intro_section", "methods_section",
                     "results_section", "discussion_section"},               "manuscript"),
    "submit":      ({"manuscript", "refs", "forest_plot"},                   "submission_package"),
}

INPUTS = {"raw_data", "case_text", "topic"}
ALL_GOALS = {produces for _, produces in CELLS.values()}


def reachable(present: "list[str]") -> set:
    """前向闭包：手头细胞能最终产出哪些东西（=哪些任务可达）。"""
    avail = set(INPUTS)
    changed = True
    while changed:
        changed = False
        for key in present:
            consumes, produces = CELLS[key]
            if consumes <= avail and produces not in avail:
                avail.add(produces)
                changed = True
    return avail & ALL_GOALS


def run_order(label: str, order: "list[str]") -> None:
    print(f"\n{label}")
    print(f"{'步':>2} {'+细胞':<12} {'活细胞':>4} {'可达任务':>6}  manuscript  submission")
    print("-" * 60)
    present: list = []
    for i, key in enumerate(order, 1):
        present.append(key)
        goals = reachable(present)
        # "活细胞"：输入已可达、真正贡献了产物的细胞数
        avail = set(INPUTS) | goals
        live = sum(1 for k in present if CELLS[k][0] <= avail)
        ms = "✅" if "manuscript" in goals else "·"
        sp = "✅" if "submission_package" in goals else "·"
        print(f"{i:>2} {key:<12} {live:>4} {len(goals):>6}      {ms:^6}      {sp:^6}")


def main() -> None:
    print("能力随『量』相变 —— 复杂目标(manuscript)在临界连通度才点亮")
    print(f"细胞总数 {len(CELLS)}，任务宇宙 {len(ALL_GOALS)} 个目标，起始输入 {INPUTS}")

    # A 乱长：先铺一堆叶子/旁支，主干上游(clean)很晚才到
    order_a = ["base", "table1", "km", "forest", "search", "profile", "interpret",
               "hypo", "method", "results", "verify", "intro", "methods_sec",
               "results_sec", "discuss", "draft", "clean", "submit"]
    # B 定向：沿通往 manuscript 的依赖闭包先铺主干
    order_b = ["clean", "profile", "hypo", "method", "results", "table1", "km",
               "interpret", "search", "verify", "intro", "methods_sec",
               "results_sec", "discuss", "draft", "forest", "submit", "base"]

    run_order("【A 乱长】量上去了，但没连起来 —— manuscript 迟迟不点亮", order_a)
    run_order("【B 沿依赖闭包定向生长】同样的细胞，复杂目标更早点亮", order_b)

    print("\n看点：")
    print("· A 里第 16 步已有 16 个细胞，manuscript 仍是 0 —— 因为上游 clean 没到，")
    print("  一大片细胞是『死』的（输入不可达）。第 17 步 clean 一到，级联点亮。")
    print("· 量不是越多越好，是要『连通的量』跨过临界点。复杂任务是相变出来的，不是攒出来的。")


if __name__ == "__main__":
    main()
