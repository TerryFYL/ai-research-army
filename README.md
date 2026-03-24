<div align="center">

# AI Research Army

**一行命令 → 6张出版级图表 · 完整统计报告 · 引用验证的IMRAD初稿**

把科研中80%的机械劳动交给 AI，你专注提问题、做判断、讲故事。

[![Stars](https://img.shields.io/github/stars/TerryFYL/ai-research-army?style=social)](https://github.com/TerryFYL/ai-research-army/stargazers)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude_Code-Skills-blueviolet)](https://docs.anthropic.com/en/docs/claude-code)
[![Multi-CLI](https://img.shields.io/badge/CLI_Engines-8_supported-orange)]()
[![Dependencies](https://img.shields.io/badge/dependencies-zero-brightgreen)]()

中文 | [English](README_EN.md)

</div>

---

## 它解决什么问题

科研的价值在于**提出好问题、解读发现、推动转化**——但你 80% 的时间花在数据清洗、跑统计、画图、调格式、核对引用上。

AI Research Army 自动化这些机械环节。你给数据和研究方向，它交付：

| 交付物 | 说明 |
|--------|------|
| `data_profile_report.md` | 数据画像（分布、缺失、异常值） |
| `research_plan.md` | 研究设计 + 假设 + 统计方案 |
| `results/*.csv` | 完整统计结果表（可复现） |
| `figures/*.png/.tiff` | 6 张出版级图表（300 DPI，色盲友好） |
| `verified_ref_pool.md` | 文献池（PubMed 验证状态标记） |
| `manuscript.md` | ~6000 词 IMRAD 初稿（你来审阅和修改） |
| `quality_report.md` | 8 层审查报告（含迭代记录） |

> **你的角色没有变**：定义研究问题、审阅结果、做学术判断、决定是否投稿。AI 处理的是从数据到初稿之间的机械环节。

---

## 30 秒看效果

以下图表由 AI Research Army 自主生成（NSCLC 化疗反应模拟数据，N=186）：

<table>
<tr>
<td width="50%"><img src="docs/showcase/fig1_forest_plot.png" alt="Forest Plot"/><br/><sub>效应量森林图（12 标志物，FDR 校正）</sub></td>
<td width="50%"><img src="docs/showcase/fig2_correlation_heatmap.png" alt="Heatmap"/><br/><sub>标志物-结局相关性热图</sub></td>
</tr>
<tr>
<td width="50%"><img src="docs/showcase/fig3_survival_curves.png" alt="KM Curves"/><br/><sub>Kaplan-Meier 生存曲线（含风险表）</sub></td>
<td width="50%"><img src="docs/showcase/fig4_roc_curves.png" alt="ROC"/><br/><sub>ROC 预测效能曲线（AUC 0.76-0.96）</sub></td>
</tr>
</table>

---

## 快速开始

```bash
git clone https://github.com/TerryFYL/ai-research-army.git
cd ai-research-army && bash install.sh
```

打开 Claude Code：

```
/start-army "探究 NHANES 2017-2020 数据中久坐行为与心血管疾病风险的关联"
```

> **前置条件**: [Claude Code](https://docs.anthropic.com/en/docs/claude-code)（`npm install -g @anthropic-ai/claude-code`）

---

## 不只是提示词模板

|  | 一般 Skill 模板 | AI Research Army |
|---|---|---|
| **方法论** | 无 | 5 项经实战沉淀的科研方法论 |
| **质量门控** | AI 自评打分 | 8 层审查 + 引用验证 + P-hacking 防护 |
| **交付物** | Markdown 报告 | 统计表 + 出版级图表 + IMRAD 初稿 |
| **数据溯源** | 不可追溯 | 每张图、每个数字可追溯到源表 |
| **报告合规** | 无 | STROBE / CONSORT 检查清单 |
| **断点恢复** | 从头开始 | 任意阶段可断点续跑 |
| **执行引擎** | 锁定单一 CLI | 8 种 CLI 引擎热切换 |

---

## 9 阶段流水线

8 位 AI 专家各司其职，不是一个 AI 切换角色：

```
/start-army "研究需求"
       │
       ▼
 ┌──────────┐   ┌──────────┐   ┌──────────────┐   ┌──────────────┐
 │ 需求结晶  │──▶│ 数据探查  │──▶│  研究设计     │──▶│  统计分析     │
 │ (Priya)  │   │ (Ming)   │   │(Priya+Kenji) │   │  (Kenji)     │
 └──────────┘   └──────────┘   └──────────────┘   └──────────────┘
                                                          │
       ┌──────────────────────────────────────────────────┘
       ▼
 ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────────┐
 │ 学术图表  │──▶│ 文献调研  │──▶│ 论文撰写  │──▶│  引用验证     │
 │ (Lena)   │   │ (Jing)   │   │  (Hao)   │   │   (Jing)     │
 └──────────┘   └──────────┘   └──────────┘   └──────────────┘
                                                      │
                                                      ▼
                                               ┌──────────────┐
                                               │  质量审查     │
                                               │ (Alex, 3轮)  │
                                               └──────────────┘
                                                      │
                                                      ▼
                                                  [ 交付 ]
```

**两个门控**：
- **引用验证** — 基础 PubMed 验证（完整多源交叉验证开发中）
- **质量审查** — 8 层检查 × 最多 3 轮，不达标不交付

---

## 团队

| 成员 | 角色 | 核心能力 |
|------|------|---------|
| **Wei** | 领航者 | 项目编排、风险直觉、成本控制 |
| **Priya** | 需求翻译官 | 需求结晶、研究设计、叙事线播种 |
| **Ming** | 数据工程师 | 数据清洗、变量标准化、数据画像 |
| **Kenji** | 生物统计师 | 假设检验、效应量解读、P-hacking 防护 |
| **Hao** | 学术写手 | IMRAD 撰写、叙事弧、读者心智建模 |
| **Lena** | 可视化设计师 | 出版级图表、数据对账、色盲友好 |
| **Alex** | 审查官 | 8 层审查、数字溯源、学术诚信一票否决 |
| **Jing** | 文献研究员 | PICOS 检索、PRISMA 合规、引用验证 |

---

## 方法论

从实战中沉淀，不是空中楼阁。详见 `methodology/`：

| 原则 | 含义 |
|------|------|
| **先有故事，再有分析** | 叙事脊柱先于统计设计，分析服务于故事 |
| **分析串联递进** | 像剥洋葱——每层答案催生下一层问题 |
| **标杆解剖先于写稿** | 先解剖 3-5 篇同领域顶刊，提取配方再动手 |
| **发现必须"可处方"** | 每个发现翻译成临床医生能直接用的行动建议 |
| **质量是设计出来的** | 审查是安全网，真正的质量来自每个阶段做好本职 |

---

## 适用领域

默认配置面向临床医学研究，但架构通用——替换 Agent 定义即可适配。

**已验证**：临床医学 · 公共卫生 · 精神医学

**可适配**：心理学 · 护理学 · 教育学 · 流行病学 · 社会学 · 经济学 — 任何有结构化数据的学科

详见下方"自定义"。

---

## 所有 Skills（可独立使用）

| Skill | 命令 | 说明 |
|-------|------|------|
| 全流程 | `/start-army "需求"` | 一键全程 |
| 数据探查 | `/data-profiler` | 数据画像 + 字典 |
| 研究设计 | `/research-design` | 方案 + 叙事线 + STROBE/CONSORT |
| 统计分析 | `/stat-analysis` | 假设驱动 + 多路径 |
| 学术图表 | `/academic-figure` | 出版级 + 对账 + 色盲友好 |
| 文献管理 | `/ref-manager` | PICOS 检索 + 引用插入 |
| 论文撰写 | `/manuscript-draft` | IMRAD + 叙事驱动 |
| 引用验证 | `/ref-manager verify` | PubMed 验证 |
| 质量审查 | `/quality-review` | 8 层审查 + 自动迭代（最多 3 轮） |
| 投稿包 | `/submit-package` | 期刊可上传材料 |

每个 Skill 都可独立使用：

```
/data-profiler                                    # 只做数据探查
/ref-manager "sedentary behavior cardiovascular"  # 只做文献检索
/academic-figure review                           # 只做图表审查
```

---

## 模型推荐

| 角色 | 推荐 | 最低 | 说明 |
|------|------|------|------|
| 主力执行 | Claude Opus | Claude Sonnet | Opus 推理更深 |
| 统计分析 | Claude Opus | Claude Sonnet | 需要强逻辑能力 |
| 质量审查（可选） | GPT-5.x / Codex | 同一模型自审 | 跨模型审稿效果更佳 |
| 文献 / 图表 | 任意 | 任意 | 主要依赖工具执行 |

> 单模型方案完全可行，加审稿模型锦上添花。

---

## 多引擎适配

不锁定单一 CLI。每位 Agent 可运行在最适合的执行引擎上，利用不同模型的差异化能力：

| 引擎 | 命令 | 适配角色 | 差异化优势 |
|------|------|---------|-----------|
| **Claude Code** | `claude` | Wei, Kenji, Ming, Hao | 深度推理、代码生成、MCP 生态 |
| **Codex CLI** | `codex` | Alex | 代码审查、方法审计、沙箱执行 |
| **Gemini CLI** | `gemini` | Lena, Jing | 多模态审图、100 万 token 长上下文 |
| **OpenCode** | `opencode` | 灵活分配 | 多模型后端切换、服务器模式 |
| **Cursor Agent** | `cursor` | 灵活分配 | IDE 级代码理解、全项目索引 |
| **Cline** | `cline` | 灵活分配 | 多 provider 支持、计划模式 |
| **Amp** | `amp` | 灵活分配 | Sourcegraph 代码搜索增强 |
| **Aider** | `aider` | 灵活分配 | Git 原生 diff 编辑、多模型 |

**为什么需要多引擎？**

> 同一模型既当选手又当裁判，盲区一致。让 GPT-5 审 Claude 写的稿、Gemini 审 GPT 画的图——不同模型的认知盲区不同，交叉审查发现的问题更多。

切换方式：

```bash
# 在 agents/registry.yaml 中配置 Agent → CLI 映射
agents:
  alex:
    cli_tool: codex      # Alex 用 Codex 审稿
  lena:
    cli_tool: gemini     # Lena 用 Gemini 审图

# tmux-runner: 按映射启动
tmux-runner.sh review codex ~/ai-research-army task.txt

# parallel-army: 环境变量全局切换
ARMY_CLI=gemini ./parallel-army.sh --all

# autoloop: 第 4 参数指定引擎
autoloop.sh ~/task-dir 20 10 codex
```

> **默认全部用 Claude Code 即可正常运行。** 多引擎是进阶选项，适合追求认知多样性和交叉验证的场景。

---

## 自定义

修改 `agents/*.md` 自定义角色，添加 `skills/your-skill/SKILL.md` 后运行 `bash install.sh`。

| 组件 | 医学默认值 | 适配方向 |
|------|-----------|---------|
| `agents/ming.md` | NHANES / CHARLS | 替换为目标领域数据源 |
| `agents/kenji.md` | 临床统计方法 | 替换为领域常用方法 |
| `quality-review` | STROBE / CONSORT | 替换为领域报告规范 |
| `ref-manager` | PubMed / CNKI | 替换为领域文献数据库 |

---

## FAQ

**开箱即用吗？**
是。`bash install.sh` → `/start-army "你的需求"` → 等交付。

**需要什么基础？**
命令行 + Claude Code + 基本科研素养（知道 p 值和置信区间是什么）。

**非医学领域能用吗？**
能。替换 Agent 定义和检查清单即可，详见"自定义"。

**这是论文代写工具吗？**
不是。它自动化的是数据处理、统计分析、格式排版、引用核验等机械环节，产出初稿供研究者审阅修改。研究问题的提出、结果的学术判断、临床意义的解读——这些仍然是也应该是人的工作。

---

## 致谢

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) — 主执行引擎
- [Codex CLI](https://github.com/openai/codex) · [Gemini CLI](https://github.com/google-gemini/gemini-cli) · [OpenCode](https://opencode.ai) · [Cursor](https://cursor.com) · [Cline](https://cline.bot) · [Amp](https://ampcode.com) · [Aider](https://aider.chat) — 可选执行引擎
- [NHANES](https://www.cdc.gov/nchs/nhanes/index.htm) — 示例数据源

## 贡献

欢迎 PR！特别欢迎：新领域 Agent 定义、质量检查清单、方法论补充。

## License

[Apache-2.0](LICENSE) · Copyright 2026 AI Research Army Contributors
