# 真后端接线 · 最后一公里交接

> 离线管线（[`03-mock-pipeline-e2e.md`](./03-mock-pipeline-e2e.md)）已端到端跑通。
> 本页是 [`01-execution-doctrine.md`](./01-execution-doctrine.md) 说的「边界停·上报」交接单：
> 把 MockLLM/合成数据换成**真实 LLM + 真实曙光数据 + 真实文献库**所需的全部步骤，
> 以及为此已在离线侧做好的「接线准备」。**这一公里需要人提供凭证/数据，不擅自越线。**

---

## 一、你需要提供的三样东西

| # | 需要 | 用途 | 现状 |
|---|------|------|------|
| 1 | `ANTHROPIC_API_KEY` + `pip install anthropic` + 网络出口 | 把写作细胞从 MockLLM 换成真 Claude | ❌ 本环境无 key/SDK/网络 |
| 2 | 真实曙光 HFpEF 队列 CSV（列对齐 `COHORT_CSV_SCHEMA`） | 把合成队列换成真数据 | ❌ 仓库无（敏感数据放 `clients/`，已 gitignore） |
| 3 | 真实文献库 API（Crossref/PubMed 等） | 给 `citation_authenticity` 跨库核对、补真 DOI | ❌ 无；当前诚实 escalate |

---

## 二、已做好的接线准备（离线即完成，换上即用）

### 1) 数字归代码（红线焊死：真模型碰不到数字 → 不可能编造）
写作细胞（`MockLLM` 与将来的真 Claude）**只产「散文 + 占位 token」**（`{{TABLE1}}`、
`{{RESULTS_EFFECT}}`、`{{N_TOTAL}}` …）；一切真实数字由 `backends.build_tokens()` 从
**真算 `stats`** 渲染、`apply_tokens()` 在代码侧回填（见 `kernel/pipeline.py: writing_wiring`）。
因此真模型即使产生幻觉也改不动正文数字——`stats_reproducible` 由架构保证，而非靠模型自律。

### 2) 真模型提示工程（draft 细胞指令已可直接喂真 Claude）
每个 draft 细胞的 `instruction`（见 `pipeline.py: build_pipeline`）已写成真模型可执行的指令：
「只写散文、禁止写任何数字/统计/引用、需要处插入指定 token、按 JSON 返回」。
`MockLLM` 读 `TASK` 分派，真 Claude 读 `INSTRUCTION`——**同一批细胞，两套后端都跑得动**。

### 3) 真数据加载适配器（与合成队列同形）
新增计算细胞 `load_cohort_csv`（`fn=load_cohort_csv`），按 `COHORT_CSV_SCHEMA` 读真实 CSV，
产出与合成队列**完全同形**的 `cohort`，故下游统计/写作器官**一行不改**。
已离线验证：合成队列写出 CSV→读回，Cox HR 逐位一致；且 arm 标签任意（`exposure_arm` 指定暴露组）。

**`COHORT_CSV_SCHEMA`（真数据需对齐的列）：**
```
pid, arm, age, sex(female/male),
hypertension, diabetes, af, ckd            # 布尔：1/0/true/false/是
lvef, ntprobnp,                            # 数值
rehospitalization, death, followup_months  # 结局
```

---

## 三、切换到真后端：改这三处（管线结构其余一行不改）

```python
# kernel/pipeline.py —— 真后端版（示意，复制即用）
from kernel.backends import AnthropicLLM            # 1) 真模型

# 1) LLM 后端：MockLLM() → AnthropicLLM()（需 key/SDK/网络）
ctx = Context(llm=AnthropicLLM(model="claude-sonnet-4-6"), compute=COMPUTE_FNS)

# 2) 数据细胞：合成 → 真实 CSV（在 build_pipeline 里把 load 细胞改成）
load = diff(comp, "load_real·载入真实队列",
            {"fn": "load_cohort_csv", "path": "clients/shuguang_hfpef.csv",
             "exposure_arm": "GDT"},               # 暴露组标签按真数据填
            consumes=[], produces=["cohort"])
# 同时把 STUDY_META["synthetic"] 设为 False（叙事不再标 synthetic）

# 3) 引用真实性：接一个文献库核对细胞（产出 verified_refs），在 audit 前替换占位 DOI；
#    在补全前，citation_authenticity 继续诚实 escalate —— 绝不为过闸而编造 DOI。
```

> 切换后 `MockLLM`、合成队列、`build_tokens` 的"数字归代码"保护**全部保留**：
> 真 Claude 依旧只写散文、碰不到数字；真数据走同一套统计与审核闸门。

---

## 四、切换后仍会诚实 escalate 的项（不伪绿）

- `citation_authenticity`：未接文献库前，无论占位 DOI 还是真 DOI，**内容是否支持论点 / 是否撤稿**都需跨库核对 → 保持 NEEDS-REVIEW。
- 人工/半自动条目：`scope_fit`、`strobe_eligibility/variables/statmethods`、`authorship_icmje`、`reporting_summary`、`figure_specs` 等仍需人或外部能力，按现状标 MANUAL。

---

## 五、验证命令

```bash
python3 -m kernel.pipeline       # 当前：合成数据离线端到端收敛
# 真后端：完成三处切换 + 提供 key/数据后，同一条命令即跑真数据真模型
```
