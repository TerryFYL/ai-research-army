# AI 科研军团 · Claude Code 入口

你正在执行 AI 科研军团的公开完整版内核。

## 先读文件

1. `TEAM.md`
2. `modules/MODULE_INDEX.md`
3. `modules/constraints.yaml`
4. `agents/skill_registry.md`

## 默认行为

- 如果用户用自然语言描述完整研究任务，将其路由到 `start-army`
- 如果用户用自然语言描述单模块任务，路由到对应 skill
- 斜杠命令只是显式入口，不是唯一入口
- 阶段间自动推进，除非缺少用户独有信息

## 不可违反

- 不跳过 `data-profiler`
- 原始数据项目不跳过 `data-forensics`
- 不在无统计结果时写 Results
- 不在未审查前打包交付
- 不输出未验证引用作为最终结果
