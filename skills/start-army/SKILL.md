---
name: start-army
description: >
  AI 科研军团统一入口。用户投入任何科研任务→Wei 读取任务→查阅 Skill 注册表→动态调度各角色。
  触发条件: 用户说"/start-army"、"启动军团"、"接单"、"开始项目"，或提供数据文件+研究需求。
domain: 科研管线编排
triggers:
  - /start-army
  - 启动军团
  - 接单
  - 开始项目
  - 启动科研任务
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Agent
---

# Start Army — 统一任务入口

> 这是整个军团的启动按钮。任何科研任务，从这里进。

## 核心定位

**用户不需要知道管线细节。** 用户只需要：
1. 描述任务（或提供数据文件路径 + 研究目的）
2. 说 `/start-army`

剩下的由 Wei 接管：读取任务 → 查阅 Skill 注册表 → 规划调度序列 → 逐步推进 → 产出交付物。

---

## 执行流程

### Phase 0：任务接收

**收集原始信息（有则用，无则留空）：**

```
必须项:
  - 任务描述（客户说了什么）
  - 数据文件路径（如果有）

可选项:
  - 目标期刊或期刊层级（如有）
  - 截止时间（如有）
  - 已有产出物路径（继续任务时）
```

---

### Phase 0.5：需求结晶（v3.0 新增，不可跳过）

> **在 Wei 编排之前，必须先让 Priya 完成需求结晶。没有锁定的需求文档，不允许进入编排阶段。**

**Priya 执行以下操作：**

1. **阅读原始材料**：数据文件（如有）+ 客户描述 → 形成初步认知
2. **主动问询**（最多 3 轮）：
   - 第 1 轮 — 研究目标与动机
   - 第 2 轮 — 数据情况与约束
   - 第 3 轮 — 产出期望与时间线
3. **草拟需求文档**：按 `templates/requirement.md` 模板输出 `clients/<project_id>/requirement_v1.md`
4. **客户确认**：提交给客户确认或修改
5. **锁定**：确认后，初始化 `clients/<project_id>/state.yaml`（详见 Phase 1）

**提前结束条件：**
- 3 轮问完仍不清楚的点 → 做假设写入文档的"团队假设"章节
- 客户明确说"就按你们理解的做" → 直接锁定当前版本

**任务分类（Priya 在结晶过程中同步完成）：**

| 关键词 | 类型 | Wei 调度策略 |
|--------|------|------------|
| "数据" + "论文"/"发表"/"稿件" | 全流程 | 从 data-forensics 开始 |
| "统计分析"/"跑一下数据" | 单模块：统计 | statistical-analysis |
| "文献综述"/"meta 分析" | 单模块：文献 | reference-manager /ref review |
| "修改图表"/"重新出图" | 单模块：图表 | academic-figure-engine |
| "审稿意见"/"修改稿" | 单模块：修稿 | paper-revision → quality-gate |
| "验证引用"/"检查文献" | 单模块：验证 | reference-manager /ref verify |
| "数据造假"/"数据真伪" | 单模块：鉴伪 | data-forensics |

**交接给 Wei：**
```
clients/<project_id>/requirement_v1.md  ← 锁定的需求
clients/<project_id>/state.yaml         ← 初始化的状态文件
```

---

### Phase 1：Wei 初始化

**Wei 执行以下操作：**

1. **读取需求文档**：`clients/<project_id>/requirement_v1.md`（或 state.yaml 指向的最新版本）— 这是执行基准，不可跳过
2. 读取 `agents/skill_registry.md` — 加载可用技能清单
3. 读取 `system/capability-registry.yaml` — 能力匹配检查（需求 vs 现有能力）
4. 读取 `modules/constraints.yaml` — 加载硬约束
5. 确认项目路径：`clients/<project_id>/`
6. 能力匹配结果写入 orchestration_plan.md（全匹配/部分匹配/有缺口）
7. 生成 `orchestration_plan.md`，格式如下：

```markdown
# 编排计划 — [项目名称]
**任务类型**: 全流程 / 单模块
**需求文档**: requirement_v1.md（已锁定）
**目标期刊层级**: [A/B/C/待定]
**预计产出**: [交付物列表]

## 能力匹配
**匹配结果**: 全匹配 / 部分匹配 / 有缺口
**缺口说明**: [如有缺口，列出缺什么能力]
**处理方案**: [直接编排 / 临时组合 / 创建新能力（需走治理门）]

## 调度序列
| 步骤 | 角色 | Skill | 子命令 | 输入文件 | 输出文件 |
|------|------|-------|--------|---------|---------|
| 1    | Ming | data-forensics | /forensics | raw_data.* | forensics_report.md |
| 2    | Ming | data-profiler | /profile | raw_data.* | data_dictionary.md |
| ...  | ...  | ...   | ...    | ...     | ...     |

## 硬性检查点
- [ ] CP-0: forensics GREEN/YELLOW
- [ ] CP-2: analysis_results.md 存在 + /ref research 启动
- [ ] CP-Final: /ref verify 通过 + /qa review 通过

## 风险预案
- 若 forensics RED → 暂停，通知创始人
- 若统计结果不显著 → Priya 评估是否调整分析策略
```

---

### Phase 2：逐步推进

**Wei 按编排计划，逐步：**
- 启动对应角色（通过 tmux-runner.sh 或 Agent 工具）
- 确认每步输出文件存在
- 将产出文件路径传递给下游角色
- **每步完成后更新 `state.yaml`**：`completed_steps += 当前步骤`，`current_phase = 下一步`
- 记录每个决策到 `orchestration_log.md`

**需求版本检查（每个节点开始前）：**
```
Wei 读取 state.yaml → 检查 current_requirement 是否与编排时的版本一致
  - 一致 → 继续执行
  - 不一致（客户修改了需求）→ 评估影响范围：
    a. 变更不影响已完成工作 → 更新 orchestration_plan，继续
    b. 变更影响已完成节点 → 标记受影响节点，重做对应节点
    c. 变更颠覆研究方向 → 回到需求结晶阶段重新对齐
```

**中间状态提示（向用户）：**

```
进度示例:
✅ Step 1 完成: 数据鉴伪 GREEN（样本量 N=312，无异常模式）
✅ Step 2 完成: 数据画像生成（26 变量，缺失率 <5%）
⏳ Step 3 进行中: Priya 研究设计...
```

---

### Phase 3：检查点决策 + 迭代闭环

**Wei 在每个检查点做决策：**

- **CP-0（接单门控）**：forensics 结果 → 决定继续/拒单/要求补充材料
- **CP-2（统计后）**：analysis_results.md → 评估结果质量 → 触发期刊升级评估（联动 Priya+Kenji+Alex）
- **CP-Final（投稿前）**：所有验证通过 → 打交付包

**迭代闭环（v3.0 新增）：**

当 Alex 质控完成后，Wei 读取审查报告末尾的**结构化摘要**（YAML 块）：

```
verdict: PASS → 进入交付阶段（Phase 4）
verdict: WARN → Wei 评估风险是否可接受
  - 可接受 → 交付（附风险说明）
  - 不可接受 → 当 BLOCK 处理

verdict: BLOCK → 迭代修复流程：
  1. 读取 failed_nodes 列表 → 只重做失败节点，不重跑全流程
  2. 递增 state.yaml 的 iteration_count
  3. 检查 iteration_count vs max_iterations(3)：
     - 未超限 → 对应 Agent 重做 → 再次提交 Alex 质控
     - 已超限 → 停止自动迭代，更新 state.yaml:
         status: "needs_human_review"
         pause_reason: "iteration_limit"
  4. 更新 state.yaml 的 quality_history（记录每次迭代结果）
```

**迭代示例：**
```
第 1 次 Alex 审查 → BLOCK: [manuscript] Table 2 数值与分析报告不一致
  → Wei 调度 Hao 重做 manuscript 节点
  → iteration_count: 1

第 2 次 Alex 审查 → WARN: [figures] Figure 3 标签字号偏小
  → Wei 判断风险可接受 → 交付
  → state.yaml: status=completed, iteration_count=1
```

---

### Phase 4：交付

**delivery/ 文件夹标准构成：**

```
delivery/
├── manuscript_final.docx    ← 主稿（含图注+格式化参考文献）
├── figure1_*.tiff           ← 出版级图（300 DPI，投稿用）
├── figure1_*.png            ← 预览图（客户核对用，不上传）
├── figure2_*.tiff
├── figure2_*.png
├── ethics_approval.jpg      ← 伦理批件（如适用）
└── 投稿说明.md              ← 操作指引（EVISE步骤+Cover Letter要点+备选期刊）
```

**投稿说明.md 必须包含：**
1. 每个文件的用途和对应投稿系统的文件类型选项
2. 投稿系统的 URL
3. 哪些文件上传、哪些仅供预览
4. Cover Letter 3-5 个要点
5. 备选期刊表（含 IF + 预估成功率）

---

## 快速启动示例

```
用户: /start-army
      客户：施雪斐，HFpEF综述，87条参考文献待验证
      数据路径: clients/shuguang/outputs/final/

→ Wei: 任务类型=单模块（引用验证）
→ Wei: 调度 Jing 执行 /ref verify
→ Jing: 运行 verify_references.py → verification_report.json
→ Alex: 确认 MISMATCH 项修正
→ Wei: 完成，提示修正结果
```

```
用户: /start-army
      收到新客户数据：heart_failure_data.csv，要做预后分析，争取发核心期刊

→ Priya: 需求结晶（Phase 0.5）
  → 阅读 heart_failure_data.csv → 主动问询 3 轮 → requirement_v1.md
  → 客户确认锁定 → 初始化 state.yaml
→ Wei: 读 requirement_v1.md → 能力匹配（全匹配）→ 任务类型=全流程
→ Wei: 生成 orchestration_plan.md（12步序列）
→ Ming: /forensics → GREEN
→ Ming: /profile → data_dictionary.md
→ Priya: /research idea → /research design → D1 讨论 → research_plan_decision.md
→ Kenji: /stat analyze
→ [... 全程自动推进 ...]
→ Alex: /qa review → PASS → delivery/ 交付包
```

---

*Skill: start-army*
*Version: 2.0 — 新增需求结晶阶段（Phase 0.5）*
*Created: 2026-03-14*
*Updated: 2026-03-15*
*Owner: Priya（需求结晶）→ Wei（编排）*
