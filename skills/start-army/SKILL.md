---
name: start-army
description: "AI科研军团公开完整版全流程入口。既支持 /start-army，也支持自然语言触发，例如‘帮我从数据探查一路推进到初稿和交付’。"
argument-hint: [研究需求描述]
allowed-tools: Bash(*), Read, Write, Edit, Grep, Glob, WebSearch, WebFetch, Agent
---

# AI 科研军团 · 全流程编排器

## 概述

这是公开版的中枢调度 Skill。它把公开仓库里的模块顺序、角色定义和质量门控串成一条完整 pipeline。

自然语言路由示例：

- “我有一份临床数据，帮我从数据探查做到初稿”
- “帮我完整推进这个研究任务，不要一步步问我”
- “从研究设计、统计分析到交付目录都做完”

启动前先读取：

1. `TEAM.md`
2. `modules/MODULE_INDEX.md`
3. `modules/constraints.yaml`
4. `agents/skill_registry.md`

## 常量

```
AUTO_PROCEED = true          # 阶段间自动推进，不等待用户确认
MAX_REVIEW_ROUNDS = 3        # 质量审查最多迭代 3 轮
QUALITY_GATE_SCORE = 70      # 质量审查通过线（B 级）
PROJECT_ROOT = ./             # 所有产出物相对此目录
```

## 流程

### Step 0: 断点检测与恢复
1. 检查是否存在 `progress.md` 或 `templates/state.yaml`
2. 若存在，则从第一个未完成阶段恢复
3. 若不存在，则从 Step 1 新建

### Step 1: 需求结晶

- 以 `Wei + Priya` 的视角执行
- 与用户最多进行 3 轮结构化问询
- 必须产出：`requirement_v1.md`
- 如果需求变更，新建 `requirement_v2.md`

### Step 2: 数据探查

- 调用 `/data-profiler`
- 产出：`data_dictionary.md`、`data_profile_report.md`
- 若数据文件明显有问题，直接记录风险

### Step 3: 数据鉴伪

- 对原始数据项目调用 `/data-forensics`
- 产出：`forensics_report.md`
- `RED` 评级时停止推进，要求人工解释数据来源

### Step 4: 研究设计

- 调用 `/research-design`
- Priya 提出方向，Kenji 校验统计可行性
- 必须产出：`research_plan.md`

### Step 5: 统计分析

- 调用 `/stat-analysis`
- 产出：`analysis_results.md`、统计表、分析代码

### Step 6: 学术图表

- 调用 `/academic-figure`
- 产出：`figures/`
- 图表中的数字必须回到统计结果逐项对账

### Step 7: 文献与期刊层

- 调用 `/ref-manager`
- 若目标期刊不明确，调用 `/journal match`
- 若格式要求不明确，调用 `/journal template`
- 产出：`verified_ref_pool.md`、`journal_requirements.md`

### Step 8: 论文撰写

- 调用 `/manuscript-draft`
- 产出：`manuscript.md`

### Step 9: 质量审查

- 调用 `/quality-review`
- 自动循环：审查 → 修复 → 重审
- 最多 `MAX_REVIEW_ROUNDS` 轮
- 产出：`quality_report.md`

### Step 10: 投稿打包

- 调用 `/submit-package`
- 产出：`submission_package/`

### Step 11: 最终交付

- 调用 `/delivery`
- 终态必须是 `delivery/`

## 进度追踪

每个阶段完成后，**必须**更新 `progress.md`，格式如下：

```markdown
# 科研军团执行进度

> 项目：[研究主题简述]
> 启动时间：[YYYY-MM-DD HH:MM]
> 最后更新：[YYYY-MM-DD HH:MM]

## 流水线状态
- [x] 需求结晶 (2026-03-18 10:00)
- [x] 数据探查 (2026-03-18 10:15)
- [x] 数据鉴伪
- [ ] 研究设计 <- 当前阶段
- [ ] 统计分析
- [ ] 学术图表
- [ ] 文献调研
- [ ] 论文撰写
- [ ] 期刊工具
- [ ] 质量审查
- [ ] 投稿包组装
- [ ] 最终交付

## 关键决策记录
- [时间戳] [决策内容]

## 阻塞与风险
- [如有]
```

## 输出
- `requirement_v1.md` — 结晶后的研究需求
- `progress.md` — 实时进度（支持断点恢复）
- 各阶段产出物（详见 `agents/skill_registry.md`）
- `delivery/` — 最终交付目录

## 关键规则
1. **全流程自主执行**：AUTO_PROCEED=true 时，阶段间不停顿。唯一停止条件：缺少用户才能提供的关键信息
2. **断点恢复**：每次启动先检查 `progress.md` 或 `state.yaml`
3. **遵守硬约束**：顺序和门控以 `modules/constraints.yaml` 为准
4. **阻塞即停**：`data-forensics = RED` 或 `quality-review = BLOCK` 时不继续推进
5. **不频繁请示用户**：除非缺失关键资料，否则内部自行判断并执行
