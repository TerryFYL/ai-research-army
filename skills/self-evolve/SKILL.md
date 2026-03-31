# Self-Evolve — 自演化引擎

> 触发词: `/evolve retrospect`, `/evolve drill`, `/evolve benchmark`
> 负责人: Wei (编排) + Alex (质量评估)
> 设计文档: `evolution/self-evolution-design.md` v2.0
> 白名单: `evolution/changeset-whitelist.yaml`

## 概述

自演化引擎是 AI 科研军团的自我改进机制。每次 pipeline 完成后自动触发复盘，识别薄弱环节，生成改进提案。

**核心原则**: 自动进化的边界 = 可程序化验证的边界。

## 子命令

### `/evolve retrospect` — 自动复盘

**触发**: pipeline 完成后自动触发（E2 约束），或手动调用
**前置条件**: outputs/ 目录下存在各模块的 trace.json

**执行流程**:

#### Step 1: 收集 Trace

```
扫描 outputs/*/trace.json
汇总为 pipeline-trace-summary.json
若缺少必要 trace → 警告并记录缺失模块
```

#### Step 2: 自动诊断

对照以下 T1 指标检查 trace 数据:

| 指标 | 来源 | 阈值 | 计算方式 |
|------|------|------|---------|
| 引用验证通过率 | ref-manager/trace.json → metrics.ref_verified / metrics.ref_total | ≥0.90 | 精确除法 |
| 统计假设满足 | stat-analysis/trace.json → metrics.assumption_violations | = 0 | 精确计数 |
| 图表对账一致性 | academic-figure/trace.json → metrics.reconciliation_errors | = [] | 列表为空 |
| 格式合规性 | submit-package/trace.json → metrics.format_checks_passed / format_checks_total | = 1.0 | 精确除法 |

#### Step 3: 分层分类

对每个诊断发现执行分类:

```yaml
for each finding:
  if finding.has_ground_truth and finding.metric_type == "deterministic":
    tier = "T1"
  elif finding.has_rubric and finding.metric_type == "rule_based":
    tier = "T2"
  else:
    tier = "T3"
```

#### Step 4: 证据关联

对 T1/T2 发现:
- 读取 `evolution/evidence-log.json`
- 检查是否有跨项目复现（同类问题在 ≥2 个独立项目中出现）
- 若不满足归因门槛 → 仅记录证据，不触发进化
- 若满足 → 标记为 `evolution_ready`

#### Step 5: 生成输出

**输出文件**: `evolution/cycles/cycle-NNN/`

1. **retrospection.md**: 复盘报告
   ```markdown
   # Cycle NNN Retrospection
   Date: YYYY-MM-DD
   Project: project_id

   ## T1 发现（可验证）
   - [指标]: 当前值 vs 阈值, 证据数量, evolution_ready: yes/no

   ## T2 发现（可评估）
   - [指标]: 观察内容, 建议, 证据数量

   ## T3 观察（主观判断）
   - [维度]: 观察内容
   ```

2. **classified_findings.json**: 结构化分类结果
   ```json
   {
     "cycle": "NNN",
     "project_id": "xxx",
     "findings": [
       {
         "id": "F001",
         "tier": "T1",
         "metric": "ref_accuracy",
         "current_value": 0.85,
         "threshold": 0.90,
         "evidence_count": 2,
         "evolution_ready": true,
         "change_domain": "auto_safe"
       }
     ]
   }
   ```

3. **更新 evidence-log.json**: 追加本次发现
4. **更新 shadow-scores.csv**: 追加本次各指标分数
5. **追加 T3 到 observations.md**: 记录主观观察

---

### `/evolve drill [finding_id]` — 针对性训练

**前置条件**: 指定 finding 已标记 `evolution_ready`
**变更域检查**: 修复目标文件必须在 `auto_safe` 域内

**执行流程**:

#### Step 1: 加载 Drill 数据

从 `evolution/benchmarks/frozen-core/` 加载对应基准数据集:
- ref_accuracy → `ref_golden_set.json`
- stat_method → `stat_scenarios.json`
- figure_recon → figure_recon_cases/
- data_quality → dirty_data_cases/

#### Step 2: 执行 Drill

只跑目标 skill（不跑全 pipeline），用基准数据:
```
input: frozen benchmark test cases
execute: target skill only
output: drill_results.json with per-case pass/fail
```

#### Step 3: 分析错误模式

```
对比: expected vs actual for each test case
归类: 错误模式分布（格式/匹配/逻辑/外部API）
定位: 根因在 skill 的哪个步骤
```

#### Step 4: 生成修复提案

```
读取: 目标 skill 的 SKILL.md
定位: 需要修改的具体段落
生成: proposal.md 含:
  - 根因分析
  - 修改建议（精确到 SKILL.md 的行/段落）
  - 预期效果
```

**注意**: drill 阶段只生成提案，不自动修改文件。

#### Step 5: 输出

- `evolution/cycles/cycle-NNN/drill_results.json`
- `evolution/cycles/cycle-NNN/proposal.md`

---

### `/evolve benchmark` — 回归测试

**触发**: 进化提案被采纳（文件已修改）后手动或自动触发

**执行流程**:

#### Step 1: 加载 Frozen Core Suite

```
读取: evolution/benchmarks/frozen-core/ 下所有测试集
```

#### Step 2: 执行测试

对每个 benchmark:
- 确定性 benchmark（ref_golden, figure_recon）→ 单次执行，硬门槛
- 非确定性 benchmark（stat_scenarios）→ 3 次执行取中位数

#### Step 3: 结果判定

```yaml
for each benchmark:
  if deterministic:
    pass = (score >= threshold)
  else:
    scores = run 3 times
    pass = (median(scores) >= threshold)
```

#### Step 4: 输出

- `evolution/cycles/cycle-NNN/benchmark_results.json`:
  ```json
  {
    "cycle": "NNN",
    "timestamp": "...",
    "results": [
      {"benchmark": "B1_ref_golden", "score": 0.95, "threshold": 0.90, "pass": true},
      {"benchmark": "B2_stat_scenarios", "scores": [1.0, 1.0, 1.0], "median": 1.0, "threshold": 1.0, "pass": true}
    ],
    "overall_pass": true
  }
  ```
- 更新 `evolution/scores.csv`
- 如果 overall_pass = false → 生成 `failure.md` 说明哪个 benchmark 失败

---

## Trace 输出标准

每个 pipeline 模块在完成时必须输出 `outputs/<module>/trace.json`。

### 通用 Schema

```json
{
  "module": "<module-name>",
  "version": "1.0",
  "timestamp": "<ISO 8601>",
  "project_id": "<project-id>",
  "duration_seconds": 0,
  "metrics": {},
  "errors": [],
  "decisions": []
}
```

### 模块特定 metrics

**ref-manager**: ref_total, ref_verified, ref_failed, ref_failed_reasons
**stat-analysis**: methods_used, methods_considered, assumption_violations, analysis_chain_depth, analysis_chain
**quality-review**: total_score, breakdown (8层), review_rounds, block_issues
**academic-figure**: figures_total, reconciliation_passed, reconciliation_errors
**manuscript-draft**: narrative_thread_versions, word_count, sections_complete
**submit-package**: format_checks_passed, format_checks_total, files_generated

详细 schema 见 `evolution/self-evolution-design.md` §3.2。

---

## 安全约束

1. **不得修改 Immutable 域**: O1-O18, M1-M5, R1-R3, PROMPT.md, TEAM.md
2. **不得自动合入**: MVP 阶段所有提案需人类 approve (E10)
3. **不得使用客户原始数据做 benchmark**: frozen core 必须脱敏
4. **跨项目归因**: 单次项目失败不触发进化 (E5)
