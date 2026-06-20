# M2 全自动管线 · 模拟数据端到端打通（离线确定性）

> 本页是 [`02-mock-pipeline-build-brief.md`](./02-mock-pipeline-build-brief.md) 的**交付说明**：
> 用**合成数据 + 离线确定性 MockLLM**，把 M2 全自动管线端到端打通——
> **模拟队列数据 → 统计分析(真算) → 生成投稿基础稿 → 审核 → 自修订收敛到合格**，
> 全程**无人工断点、无需任何 API Key、确定性可复现**。
> 归属：[`00-charter.md`](./00-charter.md) 北极星任务（M2）在离线条件下的首个端到端实例。

---

## 一、补齐了哪一段缺口

科学循环（[`01-execution-doctrine.md`](./01-execution-doctrine.md)）此前从一份**预写**的
`validators/sample_manuscript.md` 起步——缺前半段「**从数据自动生成稿件**」。
本次把前半段长出来：稿件不再手写，而是由**合成队列数据**经统计与写作器官**自动生成**，
再交给原有科学循环 audit→revise 收敛。一条命令贯通：

```
python3 -m kernel.pipeline
```

```
load_hfpef(合成队列) ──▶ analysis_organ(table1/cox/km 真算) ──▶ writing_organ(draft_* 模板化)
        │                                                              │
        └──────────────── Orchestrator 按契约自动装配 ────────────────┘
                                     │
                            生成首稿 manuscript.md
                                     │
        scientific_loop：audit → revise → 单调收敛 → 收敛稿件 + 审核结论
```

## 二、严格沿用现有 kernel 范式（非孤立脚本）

| 范式 | 落点 |
|------|------|
| **分化 differentiate** | 在 `stem_compute` 上分化出 `table1` / `cox` / `km` 统计细胞；在 `stem_llm` 上分化出七个 `draft_*` 写作细胞 |
| **组合 compose** | 统计细胞 → **分析器官**（产出结构化 `stats`）；写作细胞 → **写作器官**（产出 `manuscript.md`） |
| **神经编排 Orchestrator** | 给定目标 `manuscript`，按 `consumes/produces` 契约**反向链式**自动装配 `data→stats→draft`，无任何手工管线 |

新增文件：
- `kernel/synthetic_cohort.py` —— 确定性合成 HFpEF 回顾队列（~800 例，固定种子 `20260620`）。
- `kernel/biostats.py` —— 纯 Python 真算统计：Welch t / Mann–Whitney / χ²、**Cox 比例风险（Newton–Raphson，HR+95%CI）**、Kaplan–Meier + log-rank。
- `kernel/backends.py` —— 新增 `MockLLM`（接口与 `AnthropicLLM` 一致）+ 四个计算细胞函数（`load_hfpef_cohort` / `table1` / `cox` / `km`）。
- `kernel/pipeline.py` —— 全管线入口：编排装配 + 打印谱系/轨迹 + 交接科学循环 + 独立复验。

## 三、真算主结果（合成数据，可复现）

| 量 | 值 |
|----|----|
| 队列 | 800 例（GDT 405 / Usual 395），再入院事件 373 |
| **主结果：调整后 Cox HR（GDT vs Usual）** | **0.74（95% CI 0.60–0.91），P = 0.005** |
| Kaplan–Meier | log-rank P < 0.001；中位生存 GDT 32.1 vs Usual 18.0 个月 |

正文每个数字均由 `biostats` **真算**得到、可由固定种子复算一致；摘要数字与结果一致（`internal_consistency` 绿）。

## 四、完成判定（由审核器客观给出，不让模型自判）

`python3 -m validators.manuscript_audit out/hfpef_pipeline_manuscript.converged.md` 独立复验：

- **18/18 可离线硬闸门全绿**（标题/摘要/IMRAD/字数/显示项/各类声明/Table 1/效应量+CI/数字一致性…）。
- **仅 `citation_authenticity` 诚实 escalate（🟡 NEEDS-REVIEW）**：参考文献用**占位 DOI**
  `10.0000/mock.NNN` 并明确标注 synthetic，审核器据此判待跨库核对，**绝不伪绿 PASS**。
- 其余条目（scope、变量定义、署名、Reporting Summary、figure_specs、stats_reproducible…）为人工/半自动或需外部能力，按现状标 MANUAL / N/A。

## 五、守住的红线

- **不伪装真实性**：数据与文本在文件名、注释、稿件正文里均明确标注 **SYNTHETIC**，不冒充真实曙光数据或真实文献。
- **引用不伪造**：占位 DOI + synthetic 标注；`citation_authenticity` 保持 NEEDS-REVIEW。
- **统计真算可复现 + 数字归代码**：固定种子、纯 Python 真算；写作细胞**只产散文 + 占位 token**，
  一切数字由 `build_tokens/apply_tokens` 在代码侧回填——**写作模型从不接触原始数字，不可能篡改/编造**。
- **客观验证**：完成与否由 `manuscript_audit` 判定。
- **即插即用**：`MockLLM` 与 `AnthropicLLM` 接口一致——将来换真 Key 只需
  `Context(llm=MockLLM())` → `Context(llm=AnthropicLLM())`，**管线结构一行不改**（详见 `04-real-backend-handoff.md`）。

> **真后端就绪**：本次已把"接线准备"做到位——数字归代码、draft 细胞指令可直接喂真 Claude、
> 新增 `load_cohort_csv` 真数据适配器（与合成队列同形，已离线验证 Cox HR 逐位一致）。
> 换真 LLM/真数据只改三处，见 [`04-real-backend-handoff.md`](./04-real-backend-handoff.md)。

## 六、验证命令（无回归）

```bash
python3 -m kernel.pipeline                                              # 端到端收敛
python3 -m validators.manuscript_audit out/hfpef_pipeline_manuscript.converged.md  # 独立复验
python3 -m kernel.demo && python3 -m kernel.emergence && python3 -m kernel.scientific_loop  # 不回归
```

> 产出物（`out/`、`*.converged.md`）为**派生物**，已 gitignore；删库重跑可逐字节复现。
