---
name: ref-manager
description: "文献检索与引用管理。检索、筛选、验证学术文献。触发词：'文献检索'、'找文献'、'引用验证'、'ref verify'。"
argument-hint: [研究主题或manuscript文件]
allowed-tools: Bash(*), Read, Write, Edit, Grep, Glob, WebSearch, WebFetch, Agent
---

# 文献管理 - Jing 的图书馆

## 概述
负责科研军团全流程的文献支撑：检索相关文献、筛选高质量引用、跨数据库验证引用准确性。确保论文中的每一条引用都真实、准确、可追溯。以 Jing 的视角执行（参考 ~/.claude/agents/jing.md）。

## 子命令

| 命令 | 用法 | 功能 |
|------|------|------|
| search | `/ref-manager search [主题]` | 基于 PICOS 检索文献 |
| verify | `/ref-manager verify [ref_pool.md]` | 跨数据库验证引用 |
| insert | `/ref-manager insert [manuscript.md]` | 将引用插入论文 |

## 流程

### Step 1: 文献检索（search 子命令）

#### 1.1 构建检索策略
从 `research_plan.md` 提取关键要素，构建 PICOS 检索框架：

```markdown
## 检索策略
- P (人群): [MeSH 词 + 自由词]
- I (干预/暴露): [MeSH 词 + 自由词]
- C (对照): [MeSH 词 + 自由词]
- O (结局): [MeSH 词 + 自由词]
- S (设计): [研究类型限定]
- 布尔组合: P AND (I OR C) AND O
- 时间限定: 近 10 年优先
- 语言限定: English
```

#### 1.2 多源检索
通过 WebSearch 和 WebFetch 检索以下来源：
- **PubMed**：核心医学文献
- **Google Scholar**：扩大覆盖范围
- **CrossRef**：DOI 验证和元数据获取

#### 1.3 文献筛选
按层级筛选：
1. 标题筛选：排除明显不相关
2. 摘要筛选：评估相关性和质量
3. 全文评估（如可获取）：确认纳入

筛选标准：
- 与研究主题的相关性
- 研究设计质量（优先纳入 RCT、队列、Meta 分析）
- 期刊影响力
- 发表时间（近 5 年优先，经典文献例外）

### Step 2: 引用验证（verify 子命令）🚧 基础版

当前版本提供基础验证：通过 PubMed 检索确认每条引用的标题和作者是否存在。

> **完整版引用验证（开发中）** 将支持多源交叉验证、自动修正和门控拦截。

### Step 3: 引用插入（insert 子命令）

1. 读取 `manuscript.md`
2. 扫描所有 `[VERIFY]` 标记和引用位置
3. 从 `verified_ref_pool.md` 匹配合适文献
4. 插入格式化引用 (Author, Year)
5. 生成参考文献列表
6. 最终编号排序

## 输出
- `verified_ref_pool.md` — 经过验证的文献池，格式：
  ```markdown
  ## 已验证文献池

  ### [1] verified
  作者: Smith J, et al.
  标题: Title of the paper
  期刊: Journal Name. 2024;12(3):45-52.
  DOI: 10.1234/xxxxx
  PMID: 12345678
  用途: [引言背景/方法依据/结果对比/讨论支撑]

  ### [2] warning
  ...
  ```
- `search_strategy.md` — 检索策略记录（供方法学报告用）
- 更新 `progress.md` 中文献调研阶段状态

## 关键规则
1. **不伪造引用**：宁可少引一篇，不可编造一条不存在的文献。AI 生成的引用尤其需要验证
2. **标注用途**：每条文献必须标注在论文中的具体用途，避免"凑数引用"
3. **检索可复现**：检索策略、检索词、筛选流程完整记录，供方法学部分撰写
4. **大文件处理**：如果 Write 工具因文件过大失败，立即用 Bash (cat << 'EOF' > file) 分块写入。不要询问用户——直接执行
