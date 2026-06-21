"""能力内核 (Capability Kernel)

把"分化"与"组合"两个动作形式化成可运行算子的最小底座。
详见 kernel/README.md。
"""

from .core import (
    Capability,
    Context,
    Registry,
    stem_llm,
    stem_compute,
    differentiate,
    compose,
    sequential,
)

__all__ = [
    "Capability",
    "Context",
    "Registry",
    "stem_llm",
    "stem_compute",
    "differentiate",
    "compose",
    "sequential",
]
