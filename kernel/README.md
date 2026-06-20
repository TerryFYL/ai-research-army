# kernel —— 能力内核（分化 / 组合机制的可运行底座）

把"分化"和"组合"两个动作形式化成可运行算子的最小内核。
完整设计见 [`docs/architecture/capability-substrate.md`](../docs/architecture/capability-substrate.md)。

## 核心思想

一切单元——干细胞、分化细胞、组合器官——**都是同一个类型 `Capability`**。
正因类型统一，器官能被当成新干细胞去分化、当成成员去组合，结构得以递归向上生长。

```
干细胞(stem) --differentiate(+条件)--> 专门细胞 --compose(wiring)--> 器官 → 系统 → 个体
```

## 文件

| 文件 | 作用 |
|------|------|
| `core.py` | `Capability` 类型、`Registry` 谱系表、两个算子 `differentiate` / `compose`、干细胞构造器 |
| `backends.py` | 可插拔后端：`StubLLM`（离线确定性）/ `AnthropicLLM`（真实，接口一致即插即用）；纯 Python 统计计算 |
| `demo.py` | 端到端演示 |

## 运行

```bash
python3 -m kernel.demo
```

无第三方依赖、无需网络、结果可复现。

## 接真实 LLM

把 `Context(llm=StubLLM())` 换成 `Context(llm=AnthropicLLM())`（需 `pip install anthropic` + `ANTHROPIC_API_KEY`），
语言细胞代码一行都不用改。
