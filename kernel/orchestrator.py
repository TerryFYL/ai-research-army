"""能力内核 · 神经系统胚胎（运行时自动装配）

这是从"几条预写好的管线"跨到"一套能应付各种任务的体系"的那个**涌现时刻**。

编排器不持有任何手工接好的管线。给它一个**目标**和**手头已有的信息**，
它在能力池里按契约（consumes/produces）做**反向推理**，自己装配出一条
达成目标所需的最小通路。同一池细胞，不同目标 → 不同通路。

这正是"分化/组合"从设计期算子，变成神经系统**运行时操作**的一刻。
"""
from __future__ import annotations

from .core import Capability, Context, Registry


class Orchestrator:
    def __init__(self, reg: Registry) -> None:
        self.reg = reg

    def _producer(self, key: str) -> "Capability | None":
        for cap in self.reg.all():
            if key in cap.produces:
                return cap
        return None

    def assemble(self, goal: str, available: set) -> "list[Capability]":
        """反向链式推理：要产出 goal，需要谁；它又需要谁……直到落到已有信息。"""
        plan: "list[Capability]" = []
        done: set = set()

        def visit(key: str, stack: frozenset) -> None:
            if key in available:
                return
            cap = self._producer(key)
            if cap is None:
                raise RuntimeError(f"能力池里没有谁能产出 {key!r}")
            if cap.id in stack:
                raise RuntimeError(f"检测到循环依赖：{cap.name}")
            for need in sorted(cap.consumes):
                visit(need, stack | {cap.id})
            if cap.id not in done:
                done.add(cap.id)
                plan.append(cap)

        visit(goal, frozenset())
        return plan

    def achieve(self, goal: str, payload: dict, ctx: Context) -> "tuple[list[Capability], dict]":
        plan = self.assemble(goal, set(payload))
        state = dict(payload)
        for cap in plan:
            state.update(cap.run(state, ctx))
        return plan, state
