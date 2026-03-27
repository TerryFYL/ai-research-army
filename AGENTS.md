# AI 科研军团 · Codex / 通用 Agent 入口

本仓库是 AI 科研军团的公开完整版内核，面向 `Codex`、`Claude Code`、`Gemini CLI`、`Cursor` 等可读 Markdown 指令的 agent 运行器。

## 公开版边界

公开版包含：
- 11 Agent 角色定义
- 模块顺序与硬约束
- Skills、模板、质量门控骨架
- 可公开的方法论与交付规范

公开版不包含：
- 客户数据、真实项目产物、数据库、日志
- 商业运营自动循环、收款与获客 SOP
- 私有 API Key、私有网关、服务器部署细节

## 启动时先读

1. `TEAM.md`
2. `modules/MODULE_INDEX.md`
3. `modules/constraints.yaml`
4. `agents/registry.yaml`
5. `system/capability-registry.yaml`

## 核心原则

1. 从最终交付物倒推执行顺序，不跳步骤。
2. 需求未锁定，不启动编排。
3. 原始数据到手时，先 `data-profiler`，再 `data-forensics`。
4. `research-design` 必须经过 Priya + Kenji 收敛。
5. `statistics` 之后才能出图、做完整文献、写稿。
6. `quality-review` 是阻塞门控，不可跳过。
7. 交付终态是 `delivery/`，其中包含 `submission_package/` 和交付说明，不是一个 Markdown 草稿。

## 推荐流程

`intake → data-explore → data-forensics → research-design → statistics → figures → literature → manuscript → review → submission → delivery`

## 执行姿态

- 默认自主推进，不在普通阶段边界停下来请示。
- 真正需要用户输入时才暂停：缺数据、缺期刊偏好、伦理信息缺失、需求根本冲突。
- 每个阶段要留下明确产物，作为下游输入。

## 公开版安全红线

- 不编造数据、不编造引用、不 P-hacking。
- 不把客户数据、真实个人信息、凭证写入仓库。
- 不把本仓库当成“论文代写黑箱”；研究问题、学术判断、投稿决策仍由研究者负责。
