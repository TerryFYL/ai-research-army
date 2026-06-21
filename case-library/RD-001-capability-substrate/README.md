# 案例卡 · RD-001 能力体系自底向上

- **一句话**：从裸的大模型 API 出发，自底向上、用「分化 / 组合」两个最小算子、照人体蓝图，长出一套能自我建造、最终完成各种复杂任务的能力体系；并把"完成"定义成可客观验证的标准。
- **标签**：架构 / 自底向上 / 涌现 / 能力体系 / 科学循环 / 完成定义 / 医学科研管线
- **时间**：2026-06-20 ~ 进行中
- **参与**：创始人（fyltzx）× Claude（架构 + 实现）
- **状态**：🟡 进行中 —— **离线全自动管线已跑通**（合成数据→统计真算→生成稿件→审核→自修订收敛，`python3 -m kernel.pipeline`）；待接真实数据 / 真实文献库走完 M2 最后一公里。

## 产出
**思想文档**（`docs/architecture/`）
- `00-charter.md` 体系纲领（总纲） · `01-execution-doctrine.md` 自治执行契约
- `capability-substrate.md` 两算子+五层 · `human-body-correspondence.md` 人体同构映射
- `genesis-developmental-program.md` 0→1 九阶段 · `emergence-critical-mass.md` 量的相变
- `manuscript-standard-methodology.md` 标准方法论 · `nature-cohort-audit-checklist.md` NCVR 完成定义
- `02-mock-pipeline-build-brief.md` 模拟数据打通管线的下一步简报

**可运行机制**（`kernel/` · `validators/`）
- `kernel/core.py` 分化/组合算子 + 谱系 · `kernel/orchestrator.py` 按契约运行时自动装配
- `kernel/emergence.py` 临界质量相变实验 · `kernel/scientific_loop.py` OODA 自修订闭环
- `kernel/pipeline.py` 全管线入口（data→stats→draft 自动装配 + 交科学循环收敛）
- `kernel/synthetic_cohort.py` 合成队列 · `kernel/biostats.py` 真算统计 · 后端 StubLLM/MockLLM/ClaudeAuthoredLLM/AnthropicLLM（接口一致）
- `validators/manuscript_audit.py` 标准驱动的客观审核器 · `standards/nature-cohort.yaml` 29 硬闸门
- 文档：`03-mock-pipeline-e2e.md`（已跑通）· `04-real-backend-handoff.md`（真后端接线）

**承载 PR**：TerryFYL/ai-research-army #1

## 开放线索
1. ✅（已由后续会话落地）用合成数据 + Mock 后端打通全自动管线 → 见 `kernel/pipeline.py` / `03-mock-pipeline-e2e.md`。
2. 接**真实曙光数据**（真数据 CSV 适配器已备，见 `04-real-backend-handoff.md`）。
3. 有 API Key 后把 Mock 换成 `AnthropicLLM`（接口已对齐；亦已备 `ClaudeAuthoredLLM` 用会话 Claude 当真模型）。
4. 接真实文献库，解掉 `citation_authenticity` 的 escalate。
5. 把谱系/进度做成"可达任务仪表盘"，按依赖闭包定向生长把第一条主管线推过临界。

## 五件套
[01-思想](./01-思想.md) · [02-过程](./02-过程.md) · [03-机制](./03-机制.md) · [04-经验](./04-经验.md) · [05-采访记录](./05-采访记录.md)
