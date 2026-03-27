---
name: delivery
description: "最终交付收口。把投稿包整理成可交付目录，补齐说明文件、清单和接收指引。既支持 /delivery，也支持自然语言触发，如‘把这些整理成最终交付目录’。"
argument-hint: [submission_package目录]
allowed-tools: Bash(*), Read, Write, Edit, Grep, Glob
---

# Delivery

## 目标

把 `submission_package/` 从“内部产物”变成“对外可交付结果”。

## 前置条件

- 已存在 `submission_package/`
- 已完成 `quality_report.md`
- `progress.md` 已走到投稿包阶段

## 输出

- `delivery/`
- `delivery/delivery_note.md`
- `delivery/delivery_manifest.md`
- `delivery/next_steps.md`

## 执行步骤

1. 检查 `submission_package/` 是否完整。
2. 在 `delivery/` 中复制或索引最终投稿包。
3. 生成 `delivery_note.md`，说明交付内容、适用范围、未完成事项。
4. 生成 `delivery_manifest.md`，列出所有文件及用途。
5. 生成 `next_steps.md`，告诉接收方下一步怎么用这些文件。
6. 更新 `progress.md`，标记最终交付完成。

## delivery_note.md 最小结构

```markdown
# 交付说明

## 本次交付包含什么
## 每个文件怎么用
## 当前边界与注意事项
## 建议的下一步
```

## 关键规则

1. `delivery/` 是最终终态，不再把 `submission_package/` 当最终交付口径。
2. 不增加新的学术内容，只做交付收口与说明。
3. 对外说明必须清楚“哪些文件可直接投稿、哪些文件是辅助材料”。
