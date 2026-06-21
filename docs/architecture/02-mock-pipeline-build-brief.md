# 任务简报 · 用模拟数据打通 M2 全自动管线

> 给"新会话"的自包含执行指令。在同一个仓库(ai-research-army)、同一分支
> `claude/model-viability-check-355c96` 上执行。无需 API Key —— 全程离线、确定性、可复现。

## 0. 先读(按序,建立上下文)
1. `docs/architecture/00-charter.md` —— 总纲(方向/目标/方法论/准则)
2. `docs/architecture/01-execution-doctrine.md` —— 执行原则、OODA 循环、三道闸、停止条件、**红线**
3. `docs/architecture/manuscript-standard-methodology.md` 与 `nature-cohort-audit-checklist.md` —— 完成定义
4. 浏览 `kernel/`(core, backends, orchestrator, scientific_loop, emergence, demo)与 `validators/manuscript_audit.py`
5. 标准文件:`standards/nature-cohort.yaml`(29 硬闸门)

## 1. 现状
分化/组合算子、神经编排(按契约 consumes/produces 自动装配)、科学循环(审核→修订→单调收敛)、
客观审核器都已跑通。**缺口**:科学循环目前从一份**预写的** `validators/sample_manuscript.md` 起步——
缺前半段:**从数据自动生成稿件**。本任务补齐它,让全链路端到端打通。

## 2. 目标
用**模拟数据 + 离线确定性 MockLLM**,把 M2 **全自动管线**端到端打通,**无人工断点**:

```
模拟队列数据 → 统计分析(真算) → 生成投稿基础稿 → 审核 → 自修订收敛到合格
```

## 3. 要建什么(必须沿用现有 kernel 范式:分化/组合/编排,不要另写孤立脚本)
1. **模拟数据集**:合成一个曙光式 HFpEF 回顾队列(~800 例:分组 arm、人口学、合并症、实验室含 NT-proBNP、
   超声含 LVEF、随访结局 再入院/全因死亡/随访月数)。放 `data/` 或 `kernel/backends.py`。确定性、可复现(固定随机种子)。
2. **统计器官**:在 `stem_compute` 上**分化**出 `table1` / `cox` / `km` 细胞(**真算**;可用纯 Python 简化实现,
   但必须真算、主结果给**效应量 + 95% CI**)。**组合**成"分析器官",输出结构化结果。
3. **MockLLM**:扩展现有 `StubLLM` 思路新增 `MockLLM`,**接口与 `AnthropicLLM` 完全一致**(`complete(prompt)->str`),
   把"研究元数据 + 统计结果"模板化成各稿件章节。从语言干细胞**分化**出 `draft_*` 细胞
   (Title / Abstract / Introduction / Methods / Results[含 Table1 与 效应量+CI] / Discussion / 必备声明)。
4. **写作器官**:**组合** draft 细胞 → 产出完整 `manuscript.md`(markdown,章节用 `## 标题`,符合 `manuscript_audit` 的解析格式)。
5. **全管线入口** `kernel/pipeline.py`:用 `Orchestrator` 按契约自动装配 data→stats→draft 产出稿件,
   再交给 `kernel/scientific_loop` 跑 audit→revise 收敛。打印谱系/执行轨迹 + 最终审核结论。**无人工断点**。

## 4. 红线(必须守,违反即失败)
- **不伪装真实性**:MockLLM、模拟数据在命名/注释里明确标注是合成的,**不得伪装成真实曙光数据或真实文献**。
- **引用不伪造**:mock 参考文献用**明确占位 DOI**(如 `10.0000/mock.NNN`)或标 synthetic;
  `citation_authenticity` 仍按红线 **escalate / NEEDS-REVIEW,不得伪绿 PASS**。
- **统计真算可复现**:正文每个数字必须由分析代码算出,**不得手写编造**;审核器复验数字一致性。
- **客观验证**:完成与否由 `manuscript_audit` 判定,不让模型自判。
- **即插即用**:MockLLM 与 AnthropicLLM 接口一致,将来有 Key 直接替换,**管线结构一行不改**。

## 5. 完成定义(done)
- `python3 -m kernel.pipeline` 一条命令,从模拟数据端到端跑出稿件并自修订收敛;
- 用 `python3 -m validators.manuscript_audit <生成稿>` **独立复验**:所有可离线硬闸门全绿,
  仅 `citation_authenticity`(及需外部计算的项)被**诚实 escalate**;
- 全程**无人工断点、离线、确定性可复现**;谱系/执行轨迹可见;
- 现有 `python3 -m kernel.demo`、`kernel.emergence`、`kernel.scientific_loop` 不回归;
- 在 `docs/architecture/` 加一页说明并更新 `00-charter.md` 索引。

## 6. Git
- 在分支 **`claude/model-viability-check-355c96`** 上开发。
- 清晰提交;`git push origin claude/model-viability-check-355c96`;**PR #1 已存在,补充提交即可,不必新建 PR**。
- 提交信息末尾保留项目约定尾注(参照已有提交的 Co-Authored-By / Claude-Session 行)。

## 7. 验证命令
```
python3 -m kernel.pipeline                                  # 端到端收敛
python3 -m validators.manuscript_audit <生成的稿件路径>       # 独立复验
python3 -m kernel.demo && python3 -m kernel.emergence        # 无回归
```
