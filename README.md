<div align="center">

# AI Research Army

**一行命令，把医学生、医生、医学科研工作者最耗时的科研机械流程，压缩成一套可复用的 9 Agent 研究流水线。**

从需求结晶、数据画像、统计分析、图表、文献、写稿，到投稿包和最终交付，不再靠零散 prompt 和手工拼接。

[![Stars](https://img.shields.io/github/stars/TerryFYL/ai-research-army?style=social)](https://github.com/TerryFYL/ai-research-army/stargazers)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude_Code-Skills-blueviolet)](https://docs.anthropic.com/en/docs/claude-code)
[![Multi-CLI](https://img.shields.io/badge/CLI_Engines-8_supported-orange)]()
[![Public Core](https://img.shields.io/badge/public_core-full-green.svg)]()

中文 | [English](README_EN.md)

</div>

---

## 这套产品的价值

如果你是医学生、医生或医学科研工作者，这个项目的价值不是“帮你生成几段文字”，而是把一整条科研流水线标准化：

- 少走弯路：先锁需求、再摸数据、再定方案，不再一上来就盲跑
- 少返工：图表、正文、引用和统计结果按同一套产物契约接力
- 少碎片化：不是十几个 prompt 东拼西凑，而是 11 个角色分工协作
- 更可复制：你能把这套流程嵌入自己的课题组、实验室或个人科研流程

---

## 它解决什么问题

科研真正有价值的部分，是提出好问题、解释发现、做学术判断。

但大量时间并不花在这里，而是花在：

- 清洗数据
- 跑统计
- 画图和调格式
- 核对引用
- 把分析结果组织成稿件

AI Research Army 自动化的是这条机械链路，而不是替你做学术判断。

你给数据和研究方向，它可以产出：

| 交付物 | 说明 |
|--------|------|
| `data_profile_report.md` | 数据画像（分布、缺失、异常值） |
| `research_plan.md` | 研究设计 + 统计方案 |
| `analysis_results.md` | 结构化统计结果 |
| `figures/` | 出版级图表 |
| `verified_ref_pool.md` | 已验证文献池 |
| `manuscript.md` | IMRAD 初稿 |
| `quality_report.md` | 八层质控报告 |
| `submission_package/` | 投稿包 |
| `delivery/` | 最终交付目录 |

> 研究问题、结果解释、临床意义、投稿决策，仍然是你的责任。

---

## 这次开源的是什么

这不是最早那个“只有少量角色 + 几个 skill 的简化展示版”了。

这个仓库现在定位为 **AI 科研军团的公开完整版内核（public core）**，包含：

- 9 Agent 角色体系
- 完整模块顺序与硬约束
- 全流程入口 `/start-army`
- 单模块 Skills
- 模板、注册表、基础门控脚本
- 面向 Claude Code / Codex / Gemini 的多入口说明
- 多 CLI 引擎适配说明

为了安全和可持续维护，以下内容不在公开仓库里：

- 客户数据、真实项目产物、数据库、日志
- 私有 API Key、私有网关、服务器部署细节
- 商业运营自动循环、获客 SOP、收款流程

换句话说：**开源的是“军团引擎内核”，不是“整套商业后台”。**

---

## 30 秒看效果

以下图表由 AI Research Army 生成（示例数据）：

<table>
<tr>
<td width="50%"><img src="docs/showcase/fig1_forest_plot.png" alt="Forest Plot"/><br/><sub>效应量森林图</sub></td>
<td width="50%"><img src="docs/showcase/fig2_correlation_heatmap.png" alt="Heatmap"/><br/><sub>相关性热图</sub></td>
</tr>
<tr>
<td width="50%"><img src="docs/showcase/fig3_survival_curves.png" alt="KM Curves"/><br/><sub>Kaplan-Meier 生存曲线</sub></td>
<td width="50%"><img src="docs/showcase/fig4_roc_curves.png" alt="ROC"/><br/><sub>ROC 曲线</sub></td>
</tr>
</table>

---

## 快速开始

```bash
git clone https://github.com/TerryFYL/ai-research-army.git
cd ai-research-army
bash install.sh
```

打开 Claude Code：

```text
/start-army "探究 NHANES 2017-2020 数据中久坐行为与心血管疾病风险的关联"
```

更符合日常使用的方式，其实是直接说自然语言任务：

```text
我有一份 NHANES 数据，想研究久坐行为和心血管风险的关系，帮我从数据探查、研究设计、统计分析一路推进到初稿和交付目录
```

也可以单独调用模块：

```text
/data-profiler
/data-forensics
/research-design
/stat-analysis
/journal match
/quality-review
/delivery
```

单模块也可以直接自然语言触发，例如：

```text
先帮我看看这份数据长什么样，做一个完整的数据画像
帮我设计研究方案，重点考虑临床意义和统计可行性
帮我审这篇稿子，重点看统计和引用问题
```

前置条件：

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) 或兼容的 Markdown skill 运行器
- 基本命令行环境
- 研究者自己负责研究问题、伦理判断与最终学术决策

---

## 不只是提示词模板

|  | 一般 Skill 模板 | AI Research Army |
|---|---|---|
| **方法论** | 无 | 有完整研究流程方法论 |
| **质量门控** | AI 自评 | 八层审查 + 引用验证 + P-hacking 防护 |
| **交付物** | Markdown 报告 | 统计结果 + 图表 + IMRAD 初稿 + 投稿包 + 交付目录 |
| **数据溯源** | 弱 | 每张图、每个数字可追溯 |
| **报告合规** | 无 | STROBE / CONSORT 等检查 |
| **断点恢复** | 弱 | 可按阶段恢复 |
| **执行引擎** | 单一 | 多 CLI 适配 |

---

## 公开版流水线

`intake → data-explore → data-forensics → research-design → statistics → figures → literature → manuscript → review → submission → delivery`

核心门控：

- `data-profiler` 先于所有分析
- 原始数据项目的 `data-forensics` 不可跳过
- `statistics` 先于 `figures`、`literature`、`manuscript`
- `quality-review` 是阻塞门控
- `submission_package/` 不是终态，终态是 `delivery/`

完整规则见：

- `modules/MODULE_INDEX.md`
- `modules/constraints.yaml`

---

## 仓库结构

```text
agents/        9 个 Agent 角色定义
skills/        全流程与单模块 Skills
modules/       模块顺序与硬约束
system/        能力注册表
templates/     项目模板与编排模板
validators/    基础门控脚本
AGENTS.md      Codex / 通用 Agent 入口
CLAUDE.md      Claude Code 入口
GEMINI.md      Gemini CLI 入口
TEAM.md        团队角色与协作关系
```

---

## 9 Agent 角色

| Agent | 角色 | 主要职责 |
|------|------|---------|
| Wei | 编排者 | 调度、优先级、节奏控制 |
| Priya | 需求翻译官 | 需求结晶、研究设计 |
| Ming | 数据工程师 | 数据画像、清洗、鉴伪 |
| Kenji | 生物统计师 | 主分析、敏感性分析 |
| Lena | 学术可视化 | 投稿级图表、图表对账 |
| Jing | 文献研究员 | 检索、文献池、引用验证 |
| Hao | 学术写手 | IMRAD 初稿、修稿 |
| Alex | 审查官 | 八层审查、学术诚信 |
| Devil | 红队挑战者 | 关键节点反驳与替代解释 |

---

## 当前公开技能

| Skill | 命令 | 说明 |
|------|------|------|
| 全流程入口 | `/start-army` | 自动串联公开版 pipeline |
| 数据画像 | `/data-profiler` | 变量扫描、数据字典、质量概览 |
| 数据鉴伪 | `/data-forensics` | 异常模式与风险评级 |
| 研究设计 | `/research-design` | 问题定义、分析计划 |
| 统计分析 | `/stat-analysis` | 主分析、亚组、敏感性分析 |
| 学术图表 | `/academic-figure` | 投稿级图表生成 |
| 文献管理 | `/ref-manager` | 文献池与引用验证 |
| 期刊工具 | `/journal match` 等 | 选刊、对标、格式要求 |
| 论文撰写 | `/manuscript-draft` | IMRAD 初稿 |
| 质量审查 | `/quality-review` | 八层质控与打回 |
| 投稿打包 | `/submit-package` | 生成投稿包 |
| 最终交付 | `/delivery` | 生成对外可交付目录 |

> 上表是“显式命令入口”。日常使用中，更推荐直接用自然语言描述任务。

---

## 多引擎适配

不锁定单一 CLI。每位 Agent 可以运行在最适合的执行引擎上，利用不同模型的差异化能力。

| 引擎 | 命令 | 默认适配角色 | 优势 |
|------|------|-------------|------|
| Claude Code | `claude` | Wei, Kenji, Ming, Hao | 深度推理、代码生成、MCP 生态 |
| Codex CLI | `codex` | Alex | 代码审查、方法审计、沙箱执行 |
| Gemini CLI | `gemini` | Lena, Jing | 多模态审图、长上下文 |
| OpenCode / Cursor / Cline / Amp / Aider | 见各自命令 | 灵活分配 | 适配不同团队偏好 |

> 默认用 Claude Code 就能跑。多引擎是进阶选项，适合追求认知多样性和交叉验证的团队。

---

## 适合的用户群体

### 1. 医学生

- 适合毕业论文、课题训练、科研入门
- 重点价值是学完整流程，而不是只拿到一篇初稿

### 2. 医生

- 适合有临床问题和真实数据，但没有太多时间手工跑完整流程的人
- 重点价值是把时间从机械操作转回临床判断

### 3. 医学科研工作者

- 适合持续产出论文、管理课题、带学生的研究者
- 重点价值是把团队中的机械流程标准化、模块化

### 不太适合的人群

- 完全没有数据、只想“一键代写论文”的用户
- 不愿意自己承担研究问题、伦理和结论责任的用户
- 需要封闭式商业 SaaS 成品而不是可改造开源内核的用户

---

## 这不是“论文代写黑箱”

本项目的定位是 **科研流程自动化与标准化**，不是替代研究者做学术判断。

你仍然需要自己负责：

- 研究问题是否值得做
- 数据是否有伦理与授权问题
- 结论是否成立
- 是否投稿以及投向何处

## License

[Apache-2.0](LICENSE)
