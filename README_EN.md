# AI Research Army ⚔️🔬

> Turn Claude Code into your medical research team. 10 AI specialists collaborate autonomously — from raw data to submission-ready manuscripts.

[中文](README.md) | English

---

## Features

- **Medical research focused** — optimized for clinical studies (STROBE/CONSORT compliance, data forensics, P-hacking prevention)
- **10 AI specialists** — not one AI switching hats, but 10 virtual researchers with distinct personas, expertise, and thinking patterns
- **Fully autonomous** — one prompt triggers 11 pipeline stages; resume from breakpoints if interrupted
- **Quality loop** — 8-layer review + up to 3 auto-iteration rounds until the manuscript passes
- **Model-agnostic** — runs on Claude Opus/Sonnet/Haiku; better model = better output, but all work
- **Pure Markdown** — zero dependencies, zero lock-in; every skill is just a `SKILL.md` file

---

## Real Output

The following figures were autonomously generated from a **130-participant x 265-variable** clinical dataset, with zero human intervention:

### Forest Plot of Group Differences

17 emotional granularity indices showing MDD vs HC differences, sorted by effect size, FDR-corrected:

![Forest Plot](docs/showcase/fig1_forest_plot.png)

### State-Trait Dissociation Heatmap

Which EG dimensions predict state depression (S-DEP) vs trait depression (T-DEP) — dissociation pattern at a glance:

![State-Trait Heatmap](docs/showcase/fig2_state_trait_heatmap.png)

### Mediation Path Analysis

Asymmetric mediation: EG -> S-DEP -> T-DEP (full mediation) vs EG -> T-DEP -> S-DEP (partial mediation), revealing directional mechanisms:

![Mediation Paths](docs/showcase/fig4_mediation_paths.png)

### ROC Curves

EG indices for MDD classification (AUC 0.67-0.71), with clinical scale benchmarks:

![ROC Curves](docs/showcase/fig5_roc_curves.png)

### Full Deliverables

Output from a single `/start-army` run:

| Deliverable | Description |
|--------|------|
| `requirement_v1.md` | Structured requirement specification |
| `forensics_report.md` | Data forensics report with GREEN/YELLOW/RED quality gate |
| `data_dictionary.md` | Complete dictionary for 265 variables |
| `data_profile_report.md` | Data profile (distributions, missing patterns, outliers) |
| `research_plan.md` | Research design + hypotheses + statistical plan |
| `analysis_results.md` | Complete results from 5 analyses |
| `results/*.csv` | 7 reproducible statistical result tables |
| `figures/*.png/.tiff` | 6 publication-grade figures at 300 DPI |
| `verified_ref_pool.md` | Reference pool with verification status |
| `manuscript.md` | ~6000-word IMRAD submission-ready draft |
| `quality_report.md` | 8-layer review report with iteration log |
| `REVIEW_STATE.json` | Review state for resume capability |

> Fully automated from raw Excel to submission-ready manuscript. Quality review improved from 67 (Grade C) to 79 (Grade B) through 2 auto-iteration rounds.

---

## Quick Start

### 1. Clone

```bash
git clone https://github.com/TerryFYL/ai-research-army.git
cd ai-research-army
```

### 2. Install

```bash
bash install.sh
```

Copies all skills and agent definitions to `~/.claude/skills/` and `~/.claude/agents/`.

### 3. Run

Open Claude Code and type:

```
/start-army "Investigate the association between sedentary behavior and cardiovascular risk in NHANES 2017-2020"
```

Then sit back and wait for your submission package.

> **Prerequisite**: [Claude Code](https://docs.anthropic.com/en/docs/claude-code) installed (`npm install -g @anthropic-ai/claude-code`)

---

## Model Recommendations

| Role | Recommended | Minimum | Notes |
|------|---------|---------|------|
| Main execution | Claude Opus | Claude Sonnet | Opus has deeper reasoning |
| Statistical analysis | Claude Opus | Claude Sonnet | Stats need strong logic |
| Quality review (optional) | GPT-5.x / Codex | Same model | Cross-model review is better, but not required |
| Literature search | Any | Any | Relies on WebSearch |
| Figure generation | Any | Any | Relies on code execution |

> **Budget tip**: Single-model setup works fine. Adding a review model (via Codex MCP) improves quality if budget allows.

---

## Pipeline

11-stage pipeline, each stage executed by a specialized agent:

```
/start-army "research request"
       |
       v
 +-----------+     +-----------+     +-----------+     +----------------+
 | Require.  | --> | Forensics | --> | Profiling | --> | Research       |
 | Crystal.  |     |           |     |           |     | Design         |
 | (Priya)   |     | (Ming)    |     | (Ming)    |     | (Priya+Kenji)  |
 +-----------+     +-----------+     +-----------+     +----------------+
                     |GATE|                                     |
                     |RED=STOP|                                 v
                                                       +----------------+
                                                       | Statistical    |
                                                       | Analysis       |
                                                       | (Kenji)        |
                                                       +----------------+
                                                               |
       +-------------------------------------------------------+
       v
 +-----------+     +-----------+     +-----------+     +----------------+
 | Figures   | --> | Literature| --> | Manuscript| --> | Reference      |
 |           |     | Search    |     | Drafting  |     | Verification   |
 | (Lena)    |     | (Jing)    |     | (Hao)     |     | (Jing)         |
 +-----------+     +-----------+     +-----------+     +----------------+
                                                               |
                                                               v
                                                       +----------------+
                                                       | Quality Review |
                                                       | (Alex, 3 rds) |
                                                       +----------------+
                                                               |
                                                               v
                                                       +----------------+
                                                       | Submission     |
                                                       | Package        |
                                                       +----------------+
                                                               |
                                                               v
                                                          [ Delivery ]
```

**Three gates**:
- **Data Forensics**: RED = terminate project; YELLOW = requires confirmation
- **Reference Verification**: Basic PubMed check (full multi-source cross-validation in development)
- **Quality Review**: 8-layer check, up to 3 rounds, no pass = no delivery

---

## The Team

| Member | Role | Core Capability |
|------|------|---------|
| **Wei** | Coordinator | Orchestration, risk sensing, cost control |
| **Priya** | Requirement Analyst | Requirement crystallization, research design, narrative seeding |
| **Ming** | Data Engineer | Data forensics (7 tests), cleaning, variable standardization |
| **Kenji** | Biostatistician | Hypothesis testing, effect size interpretation, P-hacking prevention |
| **Hao** | Academic Writer | IMRAD drafting, narrative arc, reader mental modeling |
| **Lena** | Visualization Designer | Publication-grade figures, data reconciliation, colorblind-safe |
| **Alex** | Quality Reviewer | 8-layer review, number tracing, academic integrity veto |
| **Jing** | Literature Researcher | PICOS search, PRISMA compliance, citation verification |
| **Sarah** | Content Marketer | Pain-point content, channel operations, conversion funnel |
| **Tom** | Operations Manager | Pricing strategy, unit economics, funnel management |

> Wei orchestrates but doesn't write. Sarah and Tom handle business — they don't participate in the research pipeline.

---

## All Skills

| Skill | Command | Description |
|-------|------|------|
| Full Pipeline | `/start-army "request"` | End-to-end, one command |
| Data Forensics | `/data-forensics` | 7 tests + GREEN/YELLOW/RED gate |
| Data Profiling | `/data-profiler` | Data profile + dictionary |
| Research Design | `/research-design` | Plan + narrative + STROBE/CONSORT |
| Statistics | `/stat-analysis` | Hypothesis-driven + multi-path explorer |
| Figures | `/academic-figure` | Publication-grade + reconciliation + colorblind-safe |
| Literature | `/ref-manager` | PICOS search + citation insertion |
| Drafting | `/manuscript-draft` | IMRAD + narrative-driven |
| Ref Verification | `/ref-manager verify` | Basic PubMed check (full version in development) |
| Quality Review | `/quality-review` | 8-layer + auto-iteration (max 3 rounds) |
| Submission | `/submit-package` | Journal-ready upload package |

Each skill works standalone:

```
/data-profiler                                    # profile only
/ref-manager "sedentary behavior cardiovascular"  # literature search only
/academic-figure review                           # figure review only
```

---

## Methodology

> We open-source the philosophy, not the implementation — because principles help you build your own system.

See `methodology/` directory for details.

- **Story Before Analysis** — design the narrative spine before running analyses; analyses serve the story
- **Serial Chain Analysis** — peel the onion; each layer's answer spawns the next question
- **Benchmark Anatomy Before Writing** — dissect 3-5 top-journal papers in your field; extract their recipe
- **Findings Must Be Prescribable** — every finding must translate to something a clinician can act on
- **Quality Is Designed In** — the 8-layer review is the safety net; real quality comes from every stage doing its job

---

## Customization

Edit `agents/*.md` to customize any role. Create `skills/your-skill/SKILL.md` and run `bash install.sh` to add new capabilities.

Adapt to other fields by replacing:

| Component | Medical Default | Adaptation |
|------|-----------|---------|
| `agents/ming.md` | NHANES/CHARLS | Replace with your data sources |
| `agents/kenji.md` | Clinical statistics | Replace with domain methods |
| `quality-review` | STROBE/CONSORT | Replace with domain reporting standard |
| `ref-manager` | PubMed/CNKI | Replace with domain databases |

---

## Comparison with ARIS

[ARIS](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep) is another excellent Claude Code research project. The two are complementary, not competing.

| Dimension | ARIS | AI Research Army |
|------|------|-----------|
| Domain | ML/CS (arXiv, GPU) | Medical/Clinical (NHANES, STROBE) |
| Core | Cross-model review loop | Multi-agent + narrative-driven |
| Experiments | GPU deployment | Data analysis + statistical tests |
| Quality | Score >= 6/10 | 8-layer review + number traceability |
| Output | LaTeX paper | Word submission package |
| Dependencies | Python + LaTeX + GPU | Pure Markdown, zero deps |

> For ML/CS research, check out ARIS. For medical/clinical/public health, try AI Research Army.

---

## FAQ

**Does it run out of the box?** Yes. After `bash install.sh`, run `/start-army "your request"`. Agent personas are simplified — customize as needed.

**Prerequisites?** Command line + Claude Code + basic research literacy (p-values, confidence intervals).

**Cost per paper?** 200K-500K tokens. ~$3-$8 with Opus end-to-end.

**Works for non-medical fields?** Yes, but you'll need to adapt agents and checklists. See "Customization."

---

## Acknowledgments

- [ARIS](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep) — inspired the skills architecture
- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) — execution engine
- [NHANES](https://www.cdc.gov/nchs/nhanes/index.htm) — commonly used data source

## Contributing

PRs welcome! Especially: agent definitions for new domains (sociology, economics, psychology), quality checklists, methodology additions.

## License

[Apache-2.0](LICENSE) · Copyright 2026 AI Research Army Contributors
