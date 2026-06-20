# Nature Cardiovascular Research × 回顾性队列 · 完成定义与验证器

> 目标期刊：**Nature Cardiovascular Research（NCVR，Nature Portfolio）**；研究类型：回顾性队列（曙光心衰）。
> 由 [`manuscript-standard-methodology.md`](./manuscript-standard-methodology.md) 方法论编出的第一版「完成定义」实例。
> 机器可读标准：[`standards/nature-cohort.yaml`](../../standards/nature-cohort.yaml)；
> 验证器：[`validators/manuscript_audit.py`](../../validators/manuscript_audit.py)。

---

## 一、为什么是 NCVR（范围红旗已解）

上一版目标定 Nature 旗舰刊时，`scope_fit` 第一条硬闸门即亮红——旗舰刊几乎不收单中心回顾性临床队列。
改投 **NCVR** 后红旗解除，依据（已查证）：

- NCVR 范围**明确涵盖临床与公共卫生研究**，不止基础/转化；
- NCVR **明确要求观察性研究（队列/病例对照/横断面）按 STROBE 报告**——正是我们的研究类型，且 L2 已编好；
- 正文 ≤**4,500** 词、摘要 ≤**150** 词。
- 仍高度选择，需突出新颖性/临床意义；**更易接收的同门备选 = Communications Medicine**（沿用同套标准）。

> NCVR 沿用 Nature Portfolio 的格式/报告标准，所以本清单的 L1（图规格、各类声明）、L2、L3 绝大部分直接复用；
> 标 `(inherited)` 的少数版式细节以 Nature 通用值暂填，需在 NCVR 投稿指南页最终核实。

---

## 二、清单概览

| | 数量 | 说明 |
|---|---|---|
| **硬闸门**（合格） | **29** | L1 期刊 15 · L2 STROBE 9 · L3 诚信 5；全过才算可投 |
| 　└ 已实现自动探针 | **18** | 字数/标题/摘要/结构/显示项/各类声明存在性/引用 DOI/数字一致性… |
| 　└ 人工 / 未实现 | 11 | scope、变量定义、署名、Reporting Summary、figure_specs… |
| **质量评分**（高质量） | 5 | 加权合计 1.0，阈值 0.8 |

**完成定义：** 29 条硬闸门全绿 且 质量分 ≥0.8。这就是科学循环的设定点+判据。

---

## 三、验证器已跑通（`python3 -m validators.manuscript_audit`）

标准驱动：读 YAML → 逐条跑探针 → 红/黄/绿报告 + 合格判定。在一份样例稿上，18/29 条硬闸门自动判定，
逮出 5 条红：

| 红条 | 抓到的问题 |
|------|-----------|
| `title_format` | 标题 126 字符、含缩写、末尾句点 |
| `abstract_format` | 摘要内含文献引用 `[12]` |
| `data_availability` | 缺数据可得性声明 |
| `competing_interests` | 缺利益冲突声明 |
| `citation_authenticity` | 参考 #2 缺规范 DOI |
| （质量项）`internal_consistency` | **摘要 HR=1.85 与结果 HR=2.10 不一致** |

最后一条尤其说明问题：一个人眼极易漏、却致命的数字前后不一致，被客观探针逮住。

**红线落实**：`citation_authenticity` 只判 DOI 是否规范存在，**引用内容是否支持论点/是否撤稿**明确标
`NEEDS-REVIEW`（需跨库核对），绝不伪绿；`stats_reproducible` 等需外部计算的同样不自判。
程序不替人/模型宣布"完成"。

---

## 四、接入科学循环

- 报告有红 → 触发下一圈**修订假设**（每条红就是一个明确的最小修订目标）。
- 全绿且质量分达标 → **结束**（这才是"高质量完成"，而非"流程跑完"）。
- 人工/半自动条目进入人在环里复核位（对接现有 `quality-review` / `submission-toolkit`）。
- 未实现的探针（figure_specs、participant_flow、stats_reproducible）是后续补强项。

---

## 五、维护

`standards/nature-cohort.yaml` 的 `meta.recheck`：NCVR 投稿指南定期重抓、STROBE/ICMJE 改版时重编；
每条带 `source`/`version`，可追溯。

来源：[NCVR Aims](https://www.nature.com/natcardiovascres/aims) ·
[NCVR 投稿格式](https://www.nature.com/natcardiovascres/submission-guidelines/aip-and-formatting) ·
[NCVR 临床研究政策](https://www.nature.com/natcardiovascres/editorial-policies/clinical-research) ·
[Nature Reporting standards](https://www.nature.com/nature/editorial-policies/reporting-standards) ·
[EQUATOR/STROBE](https://www.equator-network.org/reporting-guidelines/strobe/) ·
[ICMJE](https://www.icmje.org/recommendations/browse/manuscript-preparation/preparing-for-submission.html)
