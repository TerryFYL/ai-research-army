---
name: start-army
description: "AI科研军团全流程入口。从数据到投稿级论文的自主执行流水线。触发词：'启动军团'、'全流程'、'帮我写论文'、'start army'。支持自然语言描述研究需求。"
argument-hint: [研究需求描述]
allowed-tools: Bash(*), Read, Write, Edit, Grep, Glob, WebSearch, WebFetch, Agent
---

# AI 科研军团 - 全流程编排器

## 概述
科研军团的中枢调度系统，串联从需求结晶到投稿包组装的九个阶段。全程自主执行，仅在缺少关键信息时停下请示用户。支持断点续跑——上下文窗口耗尽后重新启动即可从中断处继续。

## 常量

```
AUTO_PROCEED = true          # 阶段间自动推进，不等待用户确认
MAX_REVIEW_ROUNDS = 3        # 质量审查最多迭代 3 轮
QUALITY_GATE_SCORE = 70      # 质量审查通过线（B 级）
PROJECT_ROOT = ./             # 所有产出物相对此目录
```

## 流程

### Step 0: 断点检测与恢复
1. 检查当前目录是否存在 `progress.md`
2. 若存在，读取并解析各阶段完成状态
3. 定位到第一个未完成阶段（标记为 `[ ]` 或 `← 当前阶段`）
4. 从该阶段恢复执行，跳过已完成阶段
5. 若不存在 `progress.md`，从 Step 1 开始全新流程

### Step 1: 需求结晶（协调者 Wei）
- 读取 `~/.claude/agents/wei.md` 理解协调者视角
- 以 Wei 的视角执行（参考 ~/.claude/agents/wei.md）
- 与用户进行**最多 3 轮**结构化问询，聚焦：
  - 研究目的与核心问题
  - 可用数据描述（来源、样本量、变量类型）
  - 目标期刊层次与投稿时间线
  - 特殊约束（伦理审批、数据脱敏等）
- 产出：`requirement_v1.md`
- 更新 `progress.md`

### Step 2: 数据探查
- 调用 `/data-profiler [数据文件路径]`
- 以 Ming 的视角执行（参考 ~/.claude/agents/ming.md）
- 产出：`data_dictionary.md` + `data_profile_report.md`
- 生成清洁的分析就绪数据集
- 更新 `progress.md`

### Step 3: 研究设计
- 调用 `/research-design [研究方向]`
- Priya（选题）+ Kenji（可行性）协作执行
- 以 Priya 的视角执行（参考 ~/.claude/agents/priya.md）
- 产出：`research_plan.md` + `narrative_thread.md`
- 更新 `progress.md`

### Step 4: 统计分析
- 调用 `/stat-analysis [research_plan.md]`
- 以 Kenji 的视角执行（参考 ~/.claude/agents/kenji.md）
- 产出：`analysis_results.md` + 统计表格 + 分析代码
- 更新 `progress.md`

### Step 5: 学术图表
- 调用 `/academic-figure [analysis_results.md]`
- 以 Lena 的视角执行（参考 ~/.claude/agents/lena.md）
- 产出：`figures/` 目录（TIFF + 图例文本）
- 更新 `progress.md`

### Step 6: 文献调研
- 调用 `/ref-manager search [研究主题]`
- 以 Jing 的视角执行（参考 ~/.claude/agents/jing.md）
- 产出：`verified_ref_pool.md`
- 更新 `progress.md`

### Step 7: 论文撰写
- 调用 `/manuscript-draft [分析结果 + 文献]`
- 以 Hao 的视角执行（参考 ~/.claude/agents/hao.md）
- 产出：`manuscript.md`
- 更新 `progress.md`

### Step 8: 引用验证（🚧 开发中）
- **此功能正在开发中，完整版将支持跨数据库（CrossRef + PubMed + Google Scholar）逐条自动验证**
- 当前版本请手动检查论文中的引用准确性
- 建议：对每条引用至少在 Google Scholar 中搜索确认标题和作者
- 更新 `progress.md`

### Step 9: 质量审查（自动迭代）
- 调用 `/quality-review [manuscript.md]`
- 以 Alex 的视角执行（参考 ~/.claude/agents/alex.md）
- 自动循环：审查 → 修复 → 重审，最多 MAX_REVIEW_ROUNDS 轮
- 通过条件：得分 >= QUALITY_GATE_SCORE 或达到最大轮数
- 产出：`quality_report.md` + `REVIEW_STATE.json`
- 更新 `progress.md`

### Step 10: 投稿包组装（可选）
- 调用 `/submit-package [manuscript.md + 目标期刊]`
- 产出：`submission_package/` 目录
- 包含：论文 Word 版 + 图表 + Cover Letter + 报告清单 + 作者声明
- 更新 `progress.md` 标记全流程完成

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
- [ ] 研究设计 <- 当前阶段
- [ ] 统计分析
- [ ] 学术图表
- [ ] 文献调研
- [ ] 论文撰写
- [ ] 引用验证
- [ ] 质量审查
- [ ] 投稿包组装

## 关键决策记录
- [时间戳] [决策内容]

## 阻塞与风险
- [如有]
```

## 输出
- `requirement_v1.md` — 结晶后的研究需求
- `progress.md` — 实时进度（支持断点恢复）
- 各阶段产出物（详见各 skill 说明）
- `submission_package/` — 最终投稿包

## 关键规则
1. **全流程自主执行**：AUTO_PROCEED=true 时，阶段间不停顿。唯一停止条件：缺少用户才能提供的关键信息
2. **断点恢复**：每次启动先检查 `progress.md`，有则续跑，无则新建
3. **Agent 角色切换**：每个阶段开始时读取对应 agent 文件，切换思维模式
4. **进度实时更新**：每完成一个阶段立即写入 `progress.md`，确保中断后可恢复
5. **不频繁请示用户**：用户是甲方不是调试伙伴，中间探索/试错/调试全是军团自己的事
6. **大文件处理**：如果 Write 工具因文件过大失败，立即用 Bash (cat << 'EOF' > file) 分块写入。不要询问用户——直接执行
7. **时间标注**：所有数据引用标注月份，阶段记录标注具体时间
