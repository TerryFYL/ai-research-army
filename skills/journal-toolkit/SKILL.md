---
name: journal-toolkit
description: "期刊工具包。支持 /journal match、/journal benchmark、/journal template。"
allowed-tools: Bash(*), Read, Write, Edit, Grep, Glob, WebSearch, WebFetch
---

# Journal Toolkit

## 子命令

### `/journal match`

- 目标：根据研究类型、样本量、方法复杂度和创新性给出梯度期刊建议
- 输出：`journal_recommendation.md`

### `/journal benchmark`

- 目标：拆解目标期刊或同领域标杆论文，提取结构与图表配方
- 输出：`journal_benchmark.md`

### `/journal template`

- 目标：整理目标期刊的格式要求、图表要求、参考文献体例
- 输出：`journal_requirements.md`

## 通用规则

1. 期刊推荐不是只看 IF，要同时看 scope、命中率、方法匹配和时间成本。
2. 对标不是复制，而是提取结构、问题链和图表组织方式。
3. 格式要求必须落成结构化文件，供 `quality-review` 和 `submit-package` 使用。
