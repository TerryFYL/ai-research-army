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

### 2) 真模型提示工程 + 脏输出兜底（draft 细胞指令已可直接喂真 Claude）
每个 draft 细胞的 `instruction`（见 `pipeline.py: build_pipeline`）已写成真模型可执行的指令：
「只写散文、禁止写任何数字/统计/引用、需要处插入指定 token、**只返回单键 JSON（键名即 `produces`）**」。
`MockLLM` 读 `TASK` 分派，真 Claude 读 `INSTRUCTION`——**同一批细胞，两套后端都跑得动**。

真模型不像离线桩必然吐干净 JSON，故 `core.coerce_llm_output` 逐级兜底：① ```json``` 围栏；
② 前后夹带散文；③ 单键 JSON 但字符串值含**裸换行**（多行 markdown 最常踩，标准 json 直接报错）；
④ 干脆只给正文 markdown。已离线用「脏输出模拟真模型」端到端验证：七种脏格式均逐字还原、
首稿仍 18/18 闸门全绿。这意味着真模型偶发的格式抖动不会让管线崩。

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

## 二·补) 三档写作后端（同一接口，环境变量切换）

`complete(prompt) -> str` 接口下挂三个可互换后端，管线结构一行不改：

| `LLM_BACKEND` | 后端 | 说明 |
|---|---|---|
| `mock`（默认） | `MockLLM` | 离线模板桩，确定性，用于结构/闸门回归 |
| `claude` | `ClaudeAuthoredLLM` | **本会话的 Claude 亲笔**按 draft 指令写的章节，捕获回放——**无需 key 即用真模型跑通全流程** |
| `api` | `AnthropicLLM` | 真实 API 实时调用（需 key+网络+SDK） |

```bash
LLM_BACKEND=claude python3 -m kernel.pipeline   # 真模型(本Claude)端到端：18/18 离线硬闸门全绿
```

> 推荐路径正是：先 `claude` 验证提示工程+数字归代码在真模型下成立 → 再 `api` 上线实时调用。
> 两者提示词、token 回填、审核闸门完全相同，唯一差别是「捕获回放」vs「逐次实时」。

## 三、本地拉取 + 跑真模型（你现在要做的）

### A) 把云端这条分支拉到本地
```bash
git fetch origin claude/model-viability-check-355c96
git checkout claude/model-viability-check-355c96     # 或 git switch
```

### B) 切到真 API —— **零改码，纯环境变量**
真模型后端 `AnthropicLLM` 的凭证/网关/模型全部读环境变量，配好本地大模型基建即可：
```bash
pip install anthropic
export ANTHROPIC_API_KEY=sk-...            # 凭证（或本地基建的 token）
export ANTHROPIC_BASE_URL=https://...      # 仅当走自建网关/本地代理时设
export ANTHROPIC_MODEL=claude-sonnet-4-6   # 可选，默认均衡档
LLM_BACKEND=api python3 -m kernel.pipeline # 真模型实时调用，端到端跑通
```
> 缺 SDK 会给出明确提示而非崩栈；脏输出由 `coerce_llm_output` 兜底（见 二·2）。

### C) 换真数据（合成 → 真实 CSV）：改 `build_pipeline` 里的 load 细胞
```python
load = diff(comp, "load_real·载入真实队列",
            {"fn": "load_cohort_csv", "path": "clients/shuguang_hfpef.csv",
             "exposure_arm": "GDT"},               # 暴露组标签按真数据填
            consumes=[], produces=["cohort"])
# 同时把 STUDY_META["synthetic"] 设为 False（叙事不再标 synthetic）
```

### D) 引用真实性（最后一项需外部能力）
接一个文献库核对细胞（产出 `verified_refs`），在 audit 前替换占位 DOI；
**补全前 `citation_authenticity` 继续诚实 escalate —— 绝不为过闸而编造 DOI。**

> 以上切换后，`build_tokens` 的"数字归代码"保护**全部保留**：真模型只写散文、碰不到数字；
> 真数据走同一套统计与审核闸门。

---

## 四、切换后仍会诚实 escalate 的项（不伪绿）

- `citation_authenticity`：未接文献库前，无论占位 DOI 还是真 DOI，**内容是否支持论点 / 是否撤稿**都需跨库核对 → 保持 NEEDS-REVIEW。
- 人工/半自动条目：`scope_fit`、`strobe_eligibility/variables/statmethods`、`authorship_icmje`、`reporting_summary`、`figure_specs` 等仍需人或外部能力，按现状标 MANUAL。

---

## 五、验证命令

```bash
python3 -m kernel.pipeline                    # 默认 mock：离线确定性收敛（回归基线）
LLM_BACKEND=claude python3 -m kernel.pipeline # 真模型(本Claude)亲笔，无需 key
LLM_BACKEND=api    python3 -m kernel.pipeline # 真 API 实时调用（配好上面 B) 的环境变量）
```
