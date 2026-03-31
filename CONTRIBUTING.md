# 贡献指南 · AI 科研军团

> 所有对本项目的开发，必须遵循以下规范。

---

## 分支策略

```
main        ← 永远可部署的稳定版本（受保护，禁止直接推送）
dev         ← 集成分支，日常开发汇入这里
feature/*   ← 具体功能开发（从 dev 切出）
hotfix/*    ← 线上紧急修复（从 main 切出，修完同时 merge 回 main 和 dev）
```

### 标准开发流程

```bash
# 1. 从 dev 切出功能分支
git checkout dev && git pull
git checkout -b feature/xxx

# 2. 开发 + 提交
git add <具体文件>
git commit -m "feat: 做了什么"

# 3. 推送并开 PR → dev
git push -u origin feature/xxx
# 在 GitHub 上开 PR，目标分支选 dev

# 4. dev 测试通过后，PR → main（打 Release Tag）
```

### 紧急修复流程

```bash
git checkout main && git pull
git checkout -b hotfix/xxx
# 修复...
git commit -m "fix: 修复了什么"
# 同时 PR → main 和 PR → dev
```

---

## Commit 规范（Conventional Commits）

格式：`<type>: <描述>`

| type | 用途 |
|------|------|
| `feat` | 新功能 |
| `fix` | Bug 修复 |
| `refactor` | 重构（不改功能、不修 bug） |
| `docs` | 文档更新 |
| `chore` | 构建/依赖/配置/脚本 |
| `test` | 测试相关 |
| `perf` | 性能优化 |

**原则：**
- 每个 commit 只做一件事（原子性）
- 描述用动词开头：「新增」「修复」「更新」「移除」
- 不堆叠多个不相关的变更

**示例：**
```
feat: Alex Soul 新增 Skill 调用表
fix: tmux-runner codex -q 参数兼容性问题
docs: CONTRIBUTING.md 初始化
chore: .github 模板文件添加
```

---

## PR 规范

1. **PR 必须关联 Issue**（如果来自 Issue 驱动）：`Closes #12`
2. **PR 描述清楚**：用 PR 模板填写（做了什么/为什么/测试方式）
3. **小 PR 优于大 PR**：单次 PR 变更控制在合理范围内，便于 review
4. **不直接 push main**：所有变更通过 PR 合并

---

## Release / Tag 规范

版本号遵循语义化版本：`vMAJOR.MINOR.PATCH`

| 变更类型 | 版本号变动 |
|---------|----------|
| 破坏性变更（架构重构）| MAJOR +1 |
| 新功能（向后兼容）| MINOR +1 |
| Bug 修复 | PATCH +1 |

```bash
# 打 tag 并推送
git tag v2.1.0 -m "feat: Agent Skill 绑定 + Wei 动态调度 v2"
git push origin v2.1.0
```

然后在 GitHub → Releases 创建 Release，写 changelog。

---

## 安全红线（绝对禁止提交）

- `.env` 文件或任何包含 API Key 的文件
- `clients/` 目录（客户数据，已在 .gitignore 中排除）
- `*.db` 数据库文件

---

## 里程碑记录

| Tag | 日期 | 描述 |
|-----|------|------|
| — | 2026-02 | v1 架构：固定管线模板 |
| — | 2026-03-11 | v2 架构验证通过：Wei 动态编排，24分钟全自主 |
| v2.1.0 | 2026-03-15 | Agent Skill 绑定 + Wei 动态调度协议 + /start-army 入口 |
