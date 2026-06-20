"""能力内核 · 跑通演示

两幕，对照着看，正好是发育程序里那个**质变**：

  第一幕（Stage 4 形态发生）：我手工把细胞接成一条固定管线。能跑，但只会这一条。
  第二幕（Stage 5 神经涌现）：编排器拿到不同目标，从**同一池细胞**自己装配出
                              不同通路 —— 没有任何预写管线。这就是"能完成各种各样任务"。

运行：  python3 -m kernel.demo
"""
from __future__ import annotations

import json

from .backends import COMPUTE_FNS, StubLLM
from .core import Context, Registry, compose, differentiate, sequential, stem_compute, stem_llm
from .orchestrator import Orchestrator

SAMPLE_CASE = "患者女，67岁，诊断慢性心力衰竭，入院 LVEF 38%，随访 12 个月，期间因心衰再入院一次。"


def build(reg: Registry) -> dict:
    """长出一池细胞，并给每个细胞声明契约（consumes/produces），供神经系统自动装配。"""
    llm = stem_llm(reg)
    comp = stem_compute(reg)

    cells = {}

    def diff(base, name, cond, consumes, produces, desc=""):
        cap = differentiate(reg, base, name, cond, desc=desc)
        cap.consumes, cap.produces = set(consumes), set(produces)
        cells[produces[0]] = cap  # 用主产物当索引名
        return cap

    # 语言干细胞 -> 四个专门语言细胞
    diff(llm, "extract_baseline·抽取基线",
         {"task": "extract_baseline", "instruction": "抽取年龄/性别/LVEF"},
         consumes=["case_text"], produces=["baseline"])
    diff(llm, "extract_endpoint·抽取终点",
         {"task": "extract_endpoint", "instruction": "抽取再入院与随访时长"},
         consumes=["case_text"], produces=["endpoint"])
    diff(llm, "interpret·结果解读",
         {"task": "interpret", "instruction": "解读组间比较"},
         consumes=["comparison"], produces=["interpretation"])
    diff(llm, "summarize·临床小结",
         {"task": "summarize", "instruction": "整合个体与队列层面"},
         consumes=["baseline", "endpoint", "interpretation"], produces=["clinical_summary"])

    # 计算干细胞 -> 两个专门计算细胞
    diff(comp, "load_cohort·载入队列",
         {"fn": "load_dataset", "name": "heartfailure_demo"},
         consumes=[], produces=["table"])
    diff(comp, "group_compare·组间比较",
         {"fn": "group_compare", "group_key": "arm", "value_key": "lvef"},
         consumes=["table"], produces=["comparison"])

    return cells


def act_one_handwired(reg: Registry, cells: dict, ctx: Context) -> None:
    print("第一幕 · Stage 4：手工接成的固定管线（只会这一条）")
    print("-" * 60)
    organ = compose(reg, "profile_cohort·队列分析器官",
                    [cells["table"], cells["comparison"]], sequential)
    system = compose(reg, "case_to_finding·病例到结论系统",
                     [cells["baseline"], cells["endpoint"], organ, cells["interpretation"]],
                     sequential)
    out = system.run({"case_text": SAMPLE_CASE, "dataset": "heartfailure_demo"}, ctx)
    print(f"  组间比较真算：p = {out['comparison']['p_value']}")
    print(f"  解读：{out['interpretation']}")


def act_two_orchestrated(reg: Registry, ctx: Context) -> None:
    print("\n第二幕 · Stage 5：神经系统按目标自动装配（同一池细胞，不同任务）")
    print("-" * 60)
    brain = Orchestrator(reg)
    payload = {"case_text": SAMPLE_CASE, "dataset": "heartfailure_demo"}

    for goal in ("baseline", "interpretation", "clinical_summary"):
        plan, state = brain.achieve(goal, payload, ctx)
        path = " → ".join(c.name.split("·")[0] for c in plan)
        print(f"\n  目标「{goal}」")
        print(f"    自动装配通路：{path}")
        print(f"    产出：{json.dumps(state[goal], ensure_ascii=False)}")


def main() -> None:
    reg = Registry()
    cells = build(reg)
    ctx = Context(llm=StubLLM(), compute=COMPUTE_FNS)

    act_one_handwired(reg, cells, ctx)
    act_two_orchestrated(reg, ctx)

    print("\n" + "=" * 60)
    print("看点：第二幕里我没写任何管线。三个目标，三条不同通路，")
    print("都是神经系统从同一池细胞按契约现场推理装配出来的 —— 这就是通用性的胚胎。")


if __name__ == "__main__":
    main()
