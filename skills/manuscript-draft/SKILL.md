---
name: manuscript-draft
description: "学术论文撰写。基于统计结果和文献生成IMRAD格式论文。既支持 /manuscript-draft，也支持自然语言触发，如‘帮我写成论文初稿’。"
argument-hint: [分析结果和文献文件]
allowed-tools: Bash(*), Read, Write, Edit, Grep, Glob, WebSearch, WebFetch, Agent
---

# 论文撰写 - Hao 的写作间

## 概述
基于统计分析结果、验证文献池和叙事线，撰写完整的 IMRAD 格式学术论文。叙事驱动——所有章节围绕 narrative_thread.md 中的核心故事展开，确保论文不是数据堆砌而是一个有逻辑有说服力的故事。以 Hao 的视角执行（参考 ~/.claude/agents/hao.md）。

## 流程

### Step 1: 材料集结
撰写前必须读取并消化以下全部材料：

1. `narrative_thread.md` — 叙事骨架（最重要）
2. `research_plan.md` — 研究设计
3. `analysis_results.md` — 统计结果
4. `figures/figure_legends.md` — 图表及图例
5. `verified_ref_pool.md` — 已验证文献池
6. `data_dictionary.md` — 变量定义
7. `forensics_report.md` — 鉴伪结论（YELLOW 警告需在局限性中提及）

### Step 2: 论文框架搭建
按 IMRAD 结构搭建框架，每个章节的功能定位：

```
Title: [简洁、信息量大、含主要发现方向]
Abstract: [结构化摘要: 背景-目的-方法-结果-结论, ≤350词]

1. Introduction (引言)
   - 第一段: 钩子——临床问题的重要性 (来自 narrative_thread.md)
   - 第二段: 现有文献概述和知识缺口
   - 第三段: 本研究的目的和假设
   功能: 回答"为什么要做这个研究"

2. Methods (方法)
   - 2.1 研究设计与数据来源
   - 2.2 研究对象（纳入排除标准）
   - 2.3 变量定义（暴露、结局、协变量）
   - 2.4 统计分析
   - 2.5 伦理声明
   功能: 回答"怎么做的"，使研究可复现

3. Results (结果)
   - 3.1 研究对象流程图（引用 Figure 1）
   - 3.2 基线特征（引用 Table 1）
   - 3.3 主要分析结果（引用 Table 2 / Figure 2）
   - 3.4 亚组分析（引用 Figure 3 森林图）
   - 3.5 敏感性分析
   功能: 回答"发现了什么"，纯客观陈述

4. Discussion (讨论)
   - 第一段: 主要发现总结（一句话核心结论）
   - 中间段: 与既往研究对比 + 机制解释
   - 临床意义段: 处方化建议（来自 narrative_thread.md）
   - 优势段: 本研究的方法学优势
   - 局限性段: 诚实列出限制
   - 结论段: 收束 + 未来方向
   功能: 回答"这意味着什么"

References: [编号列表，来自 verified_ref_pool.md]
```

### Step 3: 逐章撰写

#### 写作原则
- **叙事连贯**：每一段的最后一句暗示下一段的内容，形成自然过渡
- **数据精确**：正文中的每个数字必须与 analysis_results.md 和图表完全一致
- **引用规范**：使用 (Author, Year) 格式，未验证的引用标记 [VERIFY]
- **语言克制**：避免过度解读，结果是结果，推测是推测，分开表述
- **主动语态优先**："We analyzed" 而非 "It was analyzed"

#### 写作顺序（非论文顺序）
1. Methods — 最客观，先写
2. Results — 对照 analysis_results.md 逐段转译
3. Discussion — 需要最多思考，放在中间
4. Introduction — 知道了全貌再写开头
5. Abstract — 最后写，浓缩全文
6. Title — 确认主要发现后再定

### Step 4: 文-图-表同步检查
撰写完成后执行强制对账：

1. 正文中提到的每个数字 → 追溯到 analysis_results.md 对应位置
2. 正文中引用的每张图表 → 确认图表存在且内容匹配
3. 正文中的引用 → 确认在 verified_ref_pool.md 中且标记为 verified
4. 发现不一致 → 以 analysis_results.md 为准修正正文

### Step 5: 格式规范化
- 段落间距统一
- 缩写首次出现时给出全称
- 统计报告格式统一：β = 1.23 (95% CI: 0.89-1.57, P = 0.032)
- 表格和图表编号连续且在正文中按顺序首次引用

## 输出
- `manuscript.md` — 完整 IMRAD 格式论文
- 更新 `progress.md` 中论文撰写阶段状态

## 关键规则
1. **叙事驱动**：论文是一个故事，不是分析报告的简单拼接。narrative_thread.md 是灵魂
2. **数字必须对账**：正文中每个数字都可追溯到 analysis_results.md，不可凭记忆写
3. **未验证引用标 [VERIFY]**：宁可标记等验证，不可放一条假引用
4. **不堆砌结果**：Results 章节围绕研究问题展开，不是把所有跑过的分析都塞进去
5. **局限性要诚实**：YELLOW 鉴伪警告、数据局限、方法局限都必须在讨论中提及
6. **发现可处方化**：讨论中的临床意义必须具体到"对谁、做什么、预期什么效果"
7. **大文件处理**：如果 Write 工具因文件过大失败，立即用 Bash (cat << 'EOF' > file) 分块写入。不要询问用户——直接执行
