"""能力内核 · 核心

设计理念（与人体一致）：
  干细胞(stem) --分化--> 专门细胞(differentiated) --组合--> 器官/系统(composed)

关键不变量：干细胞、分化细胞、组合器官 **都是同一个类型 Capability**。
正因为类型统一，一个组合器官可以再次被当作"干细胞"去分化、被当作"成员"去组合，
结构因此能够自相似地、递归地往上生长。

两个算子：
  differentiate(base, +条件)  —— 一生多（纵向特化）
  compose(members, wiring)    —— 多合一（横向聚合）
"""
from __future__ import annotations

import itertools
import json
from dataclasses import dataclass, field
from typing import Callable, Optional


# ── 运行期环境 ────────────────────────────────────────────────────────────
@dataclass
class Context:
    """承载基建后端（LLM、计算函数表）与执行轨迹。"""

    llm: Optional[object] = None
    compute: dict = field(default_factory=dict)
    trace: list = field(default_factory=list)

    def log(self, cap_id: str, note: str) -> None:
        self.trace.append((cap_id, note))


# runner: (载荷, 环境) -> 载荷
Runner = Callable[[dict, Context], dict]


# ── 能力体：宇宙中唯一的单元类型 ──────────────────────────────────────────
@dataclass
class Capability:
    id: str
    name: str
    kind: str  # "stem" | "differentiated" | "composed"
    runner: Runner
    parents: list = field(default_factory=list)  # 谱系：来源能力的 id
    conditions: dict = field(default_factory=dict)  # 分化时固化的附加条件
    desc: str = ""
    # 契约（"受体/配体"）：声明消费什么、产出什么 —— 让神经系统能自动装配
    consumes: set = field(default_factory=set)
    produces: set = field(default_factory=set)

    def run(self, payload: dict, ctx: Optional[Context] = None) -> dict:
        ctx = ctx or Context()
        ctx.log(self.id, f"run kind={self.kind}")
        return self.runner(dict(payload), ctx)


# ── 谱系注册表 ────────────────────────────────────────────────────────────
class Registry:
    """记录每个能力体及其来源，可还原成生长树。"""

    def __init__(self) -> None:
        self._caps: "dict[str, Capability]" = {}
        self._counter = itertools.count(1)

    def _new_id(self, name: str) -> str:
        slug = "".join(c if c.isalnum() else "_" for c in name).strip("_").lower()
        return f"{next(self._counter):02d}_{slug}"

    def add(self, name, kind, runner, parents=None, conditions=None, desc="") -> Capability:
        cap = Capability(
            id=self._new_id(name),
            name=name,
            kind=kind,
            runner=runner,
            parents=parents or [],
            conditions=conditions or {},
            desc=desc,
        )
        self._caps[cap.id] = cap
        return cap

    def get(self, cap_id: str) -> Capability:
        return self._caps[cap_id]

    def all(self) -> "list[Capability]":
        return list(self._caps.values())


# ── 干细胞：未特化的原始能力 ──────────────────────────────────────────────
def _build_prompt(task: str, instruction: str, payload: dict) -> str:
    """把任务/指令/载荷打包成提示词。
    真实 LLM 读 INSTRUCTION 完成任务；离线 StubLLM 读 TASK 标签确定性返回。"""
    visible = {k: v for k, v in payload.items() if not k.startswith("_")}
    return (
        f"TASK: {task}\n"
        f"INSTRUCTION: {instruction}\n"
        f"PAYLOAD: {json.dumps(visible, ensure_ascii=False)}\n"
        f"只返回 JSON。"
    )


def _parse_json(raw: str) -> dict:
    raw = raw.strip()
    i, j = raw.find("{"), raw.rfind("}")
    if i >= 0 and j > i:
        raw = raw[i : j + 1]
    return json.loads(raw)


def stem_llm(reg: Registry) -> Capability:
    """通用语言细胞：未特化的 LLM 理解/生成能力。
    本身什么都不"是"，靠分化时注入的 task / instruction 条件特化。"""

    def runner(payload: dict, ctx: Context) -> dict:
        cond = payload.get("_conditions", {})
        prompt = _build_prompt(cond.get("task", "generic"), cond.get("instruction", ""), payload)
        if ctx.llm is None:
            raise RuntimeError("语言细胞需要 ctx.llm 后端")
        return _parse_json(ctx.llm.complete(prompt))

    return reg.add("llm·通用语言细胞", "stem", runner, desc="未特化的 LLM 能力")


def stem_compute(reg: Registry) -> Capability:
    """通用计算细胞：未特化的确定性计算能力，背靠基建函数表 ctx.compute。
    靠分化时注入的 fn 条件特化成某个具体计算。"""

    def runner(payload: dict, ctx: Context) -> dict:
        cond = payload.get("_conditions", {})
        fn_name = cond.get("fn")
        fn = ctx.compute.get(fn_name)
        if fn is None:
            raise KeyError(f"未注册的计算函数: {fn_name!r}")
        return fn(payload, cond)

    return reg.add("compute·通用计算细胞", "stem", runner, desc="未特化的确定性计算能力")


# ── 算子一：分化（一生多） ────────────────────────────────────────────────
def differentiate(reg: Registry, base: Capability, name: str, conditions: dict, desc="") -> Capability:
    """分化算子：base 能力 + 附加条件 -> 一个新的专门能力。

    条件在分化时被**固化**进新能力，调用者无需再传 —— 这正是"干细胞加信号
    长成专门细胞"。对一个已分化的细胞再次分化时，更外层（更特化）的条件优先，
    内层只填补空缺，从而支持条件逐层累积。
    """

    def runner(payload: dict, ctx: Context) -> dict:
        merged = dict(payload)
        # 已存在的（来自更外层调用的）条件优先，本层固化条件填补空缺
        merged["_conditions"] = {**conditions, **payload.get("_conditions", {})}
        return base.run(merged, ctx)

    return reg.add(name, "differentiated", runner, parents=[base.id], conditions=conditions, desc=desc)


# ── 算子二：组合（多合一） ────────────────────────────────────────────────
def compose(reg: Registry, name: str, members: "list[Capability]", wiring, desc="") -> Capability:
    """组合算子：多个能力 -> 一个功能单元（器官/系统）。

    wiring(payload, members, ctx) 描述数据如何在成员间流动。
    返回值**仍是一个 Capability**，所以它能被继续组合、继续分化 —— 递归向上。
    """

    def runner(payload: dict, ctx: Context) -> dict:
        return wiring(payload, members, ctx)

    return reg.add(name, "composed", runner, parents=[m.id for m in members], desc=desc)


def sequential(payload: dict, members: "list[Capability]", ctx: Context) -> dict:
    """最简 wiring：成员顺序执行，共享并逐步累积一个状态字典。"""
    state = dict(payload)
    for cap in members:
        state.update(cap.run(state, ctx))
    return state
