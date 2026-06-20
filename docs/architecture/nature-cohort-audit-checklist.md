# Nature × 回顾性队列 · 投稿基础稿审核清单（说明）

> 目标期刊定为 **Nature**，研究类型 **回顾性队列**（曙光心衰）。
> 这是 [`manuscript-standard-methodology.md`](./manuscript-standard-methodology.md) 方法论编出的第一版
> 「完成定义」实例。机器可读清单：[`standards/nature-cohort.yaml`](../../standards/nature-cohort.yaml)。

---

## 一、清单概览

| | 数量 | 说明 |
|---|---|---|
| **硬闸门**（合格） | **29** | L1 期刊 15 · L2 STROBE 9 · L3 诚信 5；**全过才算可投** |
| 　└ 可自动探针 | 17 | 字数/标题/摘要/结构/图规格/各类声明/引用真实性… |
| 　└ 半自动 / 人工 | 4 / 8 | 范围契合、变量定义、署名、Reporting Summary… |
| **质量评分**（高质量） | 5 | 加权合计 1.0，阈值 0.8 |

**完成定义：** 29 条硬闸门**全绿** 且 质量分 **≥0.8** → 这就是科学循环的设定点+判据，也是这份清单作为
**客观验证器**的判定。

---

## 二、必须先讲的发现：第 1 条硬闸门就亮红灯

应用标准的第一价值，是在动笔前暴露问题：

> ⚠️ **`scope_fit`（范围契合度）**：单中心回顾性心衰队列**大概率不契合 Nature 旗舰刊**，
> 编辑部初筛即 desk-reject。建议改投更契合的 **Nature Medicine / Nature Cardiovascular Research /
> Nature Communications**——它们沿用同一套 Nature Portfolio 格式与报告标准，本清单的 L1/L2/L3 绝大部分**直接复用**，
> 只需替换该子刊的字数/版式细节。

这条不是"做不到"，而是标准在替我们做**投稿前的现实判断**——正是"先定义完成标准"的意义。

---

## 三、四层源头怎么落到这 29 条（你举的例子都归了位）

- **你说的"格式规范"** → L1：标题≤66字符无缩写、摘要~150词不引用、正文≤3500词、IMRAD 结构、参考≤50条上标制…（Nature 官网，硬约束）
- **你说的"图片标准"** → L1：90/180mm、TIFF/JPEG/PNG ≥300dpi、Arial/Helvetica、图注≤350词。
- **你说的"引用真实性"** → L3：每条引用真实存在 + DOI 指向正确版本 + 内容支持论点，**跨库核对、不靠模型记忆**。
- **你列不全的那些** → 已被 **L2 STROBE 9 条**（队列科学完整性：入排/失访人数/效应量+CI/局限性…）和
  **L1 政策项**（数据可得性声明、Reporting Summary、代码可得性、作者贡献、利益冲突）覆盖——
  这些恰是最易漏、却直接退稿的硬条目。

---

## 四、怎么变成科学循环的验证器（下一步）

每条硬闸门 = 一个 pass/fail 探针；质量项 = 一个评分器：

1. **17 条自动探针先落**（字数/标题/摘要/结构/图规格/声明段存在性/引用跨库核对/数字一致性）——
   纯解析 + 外部核对，**客观、不让模型自判**。
2. 跑在现有 `data→draft` 产物上 → 输出第一张**问题审核报告**（红/黄/绿 + 出处）。
3. 半自动/人工条目进入人在环里的复核位（对接现有 `quality-review` / `submission-toolkit`）。
4. 报告接回科学循环第 4 步：硬闸门有红 → 触发下一圈修订假设；全绿且质量达标 → **结束**。

> 复用而非另起：本清单是给现有 `journal-toolkit` / `quality-review` 一个**参数化、有出处、可机读**的标准底座。

---

## 五、维护

标准会过期。`standards/nature-cohort.yaml` 的 `meta.recheck` 规定：目标子刊作者须知定期重抓、
STROBE/ICMJE 版本变更时重编；每条带 `source` 与 `version`，可追溯。

来源：[Nature Formatting](https://www.nature.com/nature/for-authors/formatting-guide) ·
[Nature Initial submission](https://www.nature.com/nature/for-authors/initial-submission) ·
[Nature Reporting standards](https://www.nature.com/nature/editorial-policies/reporting-standards) ·
[EQUATOR/STROBE](https://www.equator-network.org/reporting-guidelines/strobe/) ·
[ICMJE](https://www.icmje.org/recommendations/browse/manuscript-preparation/preparing-for-submission.html)
