# Skill 开发指南

> 本目录存放 Claude Code Skills。每个 Skill 是一个独立目录，包含一个 `SKILL.md` 文件。

## 什么是 Skill

Skill 是 Claude Code 的扩展能力。一个 Skill 就是一个 Markdown 文件（`SKILL.md`），定义了：

- **触发条件**: 什么时候激活这个 Skill（斜杠命令或自然语言）
- **执行指令**: AI 应该按什么步骤执行
- **输出规范**: 产出什么格式的结果

Skill 安装到 `~/.claude/skills/` 后，可以通过斜杠命令显式调用，也可以通过自然语言任务描述被自动路由触发。

## 目录结构

```
  skills/
  start-army/
    SKILL.md          # Skill 定义文件（必须）
  data-forensics/
    SKILL.md
  data-profiler/
    SKILL.md
  research-design/
    SKILL.md
  stat-analysis/
    SKILL.md
  academic-figure/
    SKILL.md
  ref-manager/
    SKILL.md
  journal-toolkit/
    SKILL.md
  manuscript-draft/
    SKILL.md
  quality-review/
    SKILL.md
  submit-package/
    SKILL.md
  delivery/
    SKILL.md
```

## SKILL.md 模板

```markdown
# Skill 名称

## 触发条件
- 用户输入 `/your-command`
- 或者自然语言描述触发场景

## 前置条件
[需要什么输入？依赖哪些前序阶段的产出？]

## 执行步骤
1. [第一步]
2. [第二步]
3. [第三步]
...

## 输出规范
[输出什么文件？什么格式？放在哪里？]

## 质量检查
[完成前需要自检什么？]
```

## 编写 Skill 的原则

1. **一个 Skill 做一件事** — 不要把多个能力塞进一个 Skill
2. **指令要具体** — "分析数据"太模糊，"使用加权逻辑回归分析暴露变量与结局变量的关联"才有用
3. **定义清楚输入和输出** — AI 需要知道从哪里读输入，把结果写到哪里
4. **包含质量自检** — 每个 Skill 应该在完成前做自检，而不是全部依赖 quality-review
5. **考虑断点续跑** — 如果 Skill 执行中断，应该能从中间恢复

## 安装

编写完成后，运行根目录的 `install.sh`：

```bash
bash install.sh
```

这会将 `skills/` 中的所有 Skill 目录复制到 `~/.claude/skills/`。

## 测试

安装后，在 Claude Code 中测试：

```
claude

# 测试单个 skill
> /your-command

# 或直接自然语言
> 先帮我做数据画像
```

建议先用简单的测试数据验证 Skill 能正常工作，再用到正式项目中。
