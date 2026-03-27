---
name: data-forensics
description: "原始数据真伪与异常模式扫描。既支持 /data-forensics，也支持自然语言触发，如‘这份数据可信吗’。"
argument-hint: [数据文件路径]
allowed-tools: Bash(*), Read, Write, Edit, Grep, Glob
---

# Data Forensics

## 目标

在正式分析前，对原始数据做可信度与异常模式检查，输出风险评级和后续建议。

## 输入

- 原始数据文件
- 可选：`data_dictionary.md`

## 输出

- `forensics_report.md`
- 风险评级：`GREEN / YELLOW / RED`

## 执行步骤

1. 读取数据并识别变量类型、取值范围、样本量。
2. 扫描明显异常：
   - 末位数字异常集中
   - 不合理重复值或整列复制
   - 超出生理/业务常识范围的数值
   - 缺失模式异常整齐
3. 如果有汇总统计或论文声明值，检查与原始数据是否冲突。
4. 输出风险评级与理由。

## 评级规则

- `GREEN`: 未发现明显造假或结构性异常，可进入统计分析
- `YELLOW`: 发现可疑点，需要在报告中保留警示并人工复核
- `RED`: 异常强烈，不建议继续分析，除非先获得数据来源说明

## 边界

- 这不是统计分析
- 这不是稿件审稿
- 这也不代替 `data-profiler`
