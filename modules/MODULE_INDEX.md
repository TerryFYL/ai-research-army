# 模块索引

> 速查手册。详细约束见 `constraints.yaml`，角色详情见 `agents/<name>.md`

## 管线总览

```
intake → data-explore → data-forensics
    → research-design → D1讨论 → CP-1
        → statistics → CP-2
        → figures
        → literature(/ref research)
        → manuscript → review → CP-3
        → submission → delivery
```

---

## 模块详情

### 1. intake — 接单评估

| 项目 | 内容 |
|------|------|
| 角色 | Tom + Priya |
| 输入 | 客户问卷 |
| 输出 | 评估报告 + 报价 |
| 说明 | 评估数据质量、项目可行性、工作量，给出报价。决定接不接这单 |

### 2. data-explore — 数据探查

| 项目 | 内容 |
|------|------|
| 角色 | Ming |
| 输入 | 原始数据文件 |
| 输出 | data_dictionary.md, cohort_definition.md |
| 说明 | 摸清数据家底：变量类型、缺失率、分布、样本量、数据结构。全管线基础输入 |
| 约束 | **M1 强制执行**，O1 必须在所有分析模块之前 |

### 3. data-forensics — 数据鉴伪

| 项目 | 内容 |
|------|------|
| 角色 | Ming + Alex |
| 输入 | 原始数据 |
| 输出 | 鉴伪报告（GREEN / YELLOW / RED） |
| 说明 | 检测数据是否存在伪造、篡改、不合理模式。RED = 拒单或要求证明 |
| 约束 | **M3 客户提供数据时强制执行**，O2 必须在 statistics 之前 |

### 4. research-design — 研究设计

| 项目 | 内容 |
|------|------|
| 角色 | Priya → Priya + Kenji 讨论(D1) |
| 输入 | 数据字典 + 客户需求 |
| 输出 | 候选方向 → research_plan_decision.md（主方案 + 备选 + 排除记录） |
| 说明 | Priya 基于数据边界和临床意义提出候选研究方向，然后与 Kenji 双向收敛确认统计可行性 |
| 约束 | O7 候选方向必须经 D1 讨论确认后方可进入 CP-1 |

### 5. risk-assess — 风险评估

| 项目 | 内容 |
|------|------|
| 角色 | Priya + Kenji |
| 输入 | 研究设计 |
| 输出 | 应急预案表 |
| 说明 | 识别项目风险点（统计假设不满足、样本量边界、审稿人可能攻击点），制定预案 |

### 6. statistics — 统计分析

| 项目 | 内容 |
|------|------|
| 角色 | Kenji (+ Ming) |
| 输入 | 数据 + research_plan_decision.md |
| 输出 | 统计结果总表 + Table 1 + 分析脚本 |
| 说明 | 执行 D1 确认的分析方案。Multi-Path Explorer 自动匹配方法，Kenji 审核验证 |
| 约束 | O2 鉴伪之后，O3 写稿之前，O5 出图之前，O6 文献之前 |

### 7. figures — 学术出图

| 项目 | 内容 |
|------|------|
| 角色 | Lena |
| 输入 | 统计结果 + 期刊规范 |
| 输出 | Figure 1-N + 图注 |
| 说明 | 基于统计结果生成投稿级图表，符合目标期刊格式要求 |
| 约束 | O5 必须在 statistics 之后 |

### 8. literature — 文献调研

| 项目 | 内容 |
|------|------|
| 角色 | Jing |
| 输入 | 统计结果 + 研究设计 + CP-2 decision.md |
| 输出 | 领域深度调研报告 + 文献综述 + 引用列表 + 学术演进图 |
| 说明 | 两层架构：Layer 1 Deep Research（认知层，学术判断）+ Layer 2 API 验证（证据层，CrossRef/SS 元数据）。从统计结果提取 T1-T5 主题，结果驱动的文献检索 |
| 约束 | **O6 必须在 statistics 完成且 CP-2 通过之后** |
| 工具 | `/ref research` → `/ref review` → `/ref download` → `/ref insert` → `/ref verify` |

### 9. manuscript — 初稿撰写

| 项目 | 内容 |
|------|------|
| 角色 | Hao (+ Jing) |
| 输入 | 统计结果 + 图表 + 文献 |
| 输出 | manuscript_draft.md |
| 说明 | 基于统计结果、图表和文献知识地基撰写投稿级初稿 |
| 约束 | O3 必须在 statistics 之后 |

### 10. review — 质量审查

| 项目 | 内容 |
|------|------|
| 角色 | Alex (+ Devil) |
| 输入 | 完整稿件 |
| 输出 | 审查报告（通过 / 打回） |
| 说明 | 终审关卡。数字溯源、学术诚信、逻辑一致性全面检查。Alex 有一票否决权 |
| 约束 | **M2 强制执行**，O4 必须在 delivery 之前 |

### 11. submission — 投稿准备

| 项目 | 内容 |
|------|------|
| 角色 | Hao + Alex |
| 输入 | 审查通过的稿件 |
| 输出 | submission_package/ |
| 说明 | 按目标期刊要求打包：Cover Letter、格式调整、补充材料、作者声明等 |

### 12. delivery — 交付

| 项目 | 内容 |
|------|------|
| 角色 | Tom |
| 输入 | 投稿包 |
| 输出 | 交付说明 + ZIP |
| 说明 | 面向客户的最终交付。包含使用说明、修改建议、后续支持 |
| 约束 | O4 必须在 review 之后 |

---

## 检查点与讨论

| ID | 类型 | 时机 | 参与者 | 产出物 |
|----|------|------|--------|--------|
| D1 | 必要讨论 | research-design 产出候选方向后 | Priya + Kenji | research_plan_decision.md |
| CP-1 | Devil 红队 | D1 完成后 | Devil | 挑战研究方案 |
| CP-2 | Devil 红队 | statistics 方法选定后 | Devil | 挑战统计方法 |
| CP-3 | Devil 红队 | manuscript 核心结论成型后 | Devil | 挑战论文结论 |

## 硬约束速查

| ID | 规则 |
|----|------|
| O1 | data-explore 先于一切分析 |
| O2 | data-forensics 先于 statistics |
| O3 | statistics 先于 manuscript |
| O4 | review 先于 delivery，不可跳过 |
| O5 | figures 在 statistics 之后 |
| O6 | literature 在 statistics + CP-2 之后 |
| O7 | research-design 须经 D1 讨论确认方可进 CP-1 |
| M1 | data-explore 所有项目强制 |
| M2 | review 所有交付项目强制 |
| M3 | data-forensics 有原始数据时强制 |
| R1 | 每个数字可溯源到统计结果 |
| R2 | 不捏造数据、不编造引用、不 P-hacking |
| R3 | 鉴伪 RED → 拒单或要求证明 |
