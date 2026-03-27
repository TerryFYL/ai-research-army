# 模块索引

> 公开完整版速查表。详细门控规则见 `constraints.yaml`。

## 总流程

```
intake
  → data-explore
  → data-forensics
  → research-design
  → statistics
  → figures
  → literature
  → manuscript
  → review
  → submission
  → delivery
```

## 模块定义

### 1. intake

- 角色：Priya + Wei
- 目标：把模糊需求结晶成 `requirement_v1.md`
- 终态：需求锁定，可执行

### 2. data-explore

- 角色：Ming
- 输入：原始数据
- 输出：`data_dictionary.md`、`data_profile_report.md`
- 说明：任何分析之前必须先认识数据

### 3. data-forensics

- 角色：Ming + Alex
- 输入：原始数据
- 输出：`forensics_report.md`
- 说明：原始数据项目的真伪与异常模式扫描

### 4. research-design

- 角色：Priya + Kenji
- 输入：需求文档、数据画像
- 输出：`research_plan.md`
- 说明：临床意义、统计可行性、期刊野心三者收敛

### 5. statistics

- 角色：Kenji
- 输入：清洗后数据、研究设计
- 输出：`analysis_results.md`、统计表格、分析脚本

### 6. figures

- 角色：Lena
- 输入：统计结果
- 输出：`figures/`
- 说明：每张图都必须和统计结果对账

### 7. literature

- 角色：Jing
- 输入：研究设计、统计结果
- 输出：`literature_summary.md`、`verified_ref_pool.md`

### 8. manuscript

- 角色：Hao
- 输入：统计结果、图表、文献池
- 输出：`manuscript.md`

### 9. review

- 角色：Alex + Devil
- 输入：完整稿件与图表
- 输出：`quality_report.md`
- 说明：阻塞式门控，不通过不交付

### 10. submission

- 角色：Hao + Alex
- 输入：审查通过稿件
- 输出：`submission_package/`

### 11. delivery

- 角色：Tom
- 输入：投稿包
- 输出：`delivery/`（含交付说明、清单、最终打包结果）

## 最小门控清单

- `data-explore` 在所有分析之前
- 原始数据项目 `data-forensics` 不可跳过
- `statistics` 先于 `figures`、`literature`、`manuscript`
- `review` 先于 `submission`
- `submission` 先于 `delivery`
