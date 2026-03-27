#!/bin/bash
# ============================================================
# AI 科研军团 (AI Research Army) — 安装脚本
# 将 skills 复制到 Claude Code 全局 skills 目录
# ============================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILLS_DIR="$HOME/.claude/skills"
INSTALLED=0
SKIPPED=0

echo ""
echo "  AI 科研军团 — 安装中..."
echo "  ================================"
echo ""

# 检查 Claude Code 是否已安装
if ! command -v claude &> /dev/null; then
    echo "  [警告] 未检测到 Claude Code CLI。"
    echo "  请先安装: npm install -g @anthropic-ai/claude-code"
    echo ""
    echo "  继续安装 skill 文件..."
    echo ""
fi

# 创建 skills 目录
mkdir -p "$SKILLS_DIR"

# 检查 skills 目录是否有内容
if [ ! -d "$SCRIPT_DIR/skills" ] || [ -z "$(ls -A "$SCRIPT_DIR/skills/" 2>/dev/null)" ]; then
    echo "  [提示] skills/ 目录为空或不存在。"
    echo ""
    echo "  本项目开源的是方法论和框架。"
    echo "  你需要基于 methodology/ 和 templates/ 中的理念，"
    echo "  编写自己的 SKILL.md 文件放到 skills/ 目录中。"
    echo ""
    echo "  参考: skills/README.md 中的 Skill 开发指南"
    echo ""
    exit 0
fi

# 复制 agents 到 ~/.claude/agents/（skill 中会引用这些角色定义）
AGENTS_DIR="$HOME/.claude/agents"
mkdir -p "$AGENTS_DIR"
if [ -d "$SCRIPT_DIR/agents" ]; then
    for agent_file in "$SCRIPT_DIR"/agents/*.md; do
        [ -f "$agent_file" ] || continue
        agent_name=$(basename "$agent_file")
        [ "$agent_name" = "README.md" ] && continue
        if [ -f "$AGENTS_DIR/$agent_name" ]; then
            echo "  [已存在] agent/$agent_name — 跳过"
        else
            cp "$agent_file" "$AGENTS_DIR/$agent_name"
            echo "  [已安装] agent/$agent_name"
        fi
    done
    echo ""
fi

# 复制 skills
for skill_dir in "$SCRIPT_DIR"/skills/*/; do
    # 跳过非目录项
    [ -d "$skill_dir" ] || continue

    skill_name=$(basename "$skill_dir")

    # 跳过 README 等非 skill 文件
    [ "$skill_name" = "README.md" ] && continue

    # 检查目录中是否有 SKILL.md
    if [ ! -f "$skill_dir/SKILL.md" ]; then
        echo "  [跳过] $skill_name — 缺少 SKILL.md 文件"
        SKIPPED=$((SKIPPED + 1))
        continue
    fi

    target_dir="$SKILLS_DIR/$skill_name"

    if [ -d "$target_dir" ]; then
        echo "  [已存在] $skill_name — 跳过（如需更新请先删除 $target_dir）"
        SKIPPED=$((SKIPPED + 1))
    else
        cp -r "$skill_dir" "$target_dir"
        echo "  [已安装] $skill_name"
        INSTALLED=$((INSTALLED + 1))
    fi
done

echo ""
echo "  ================================"
echo "  安装完成！"
echo "  已安装: $INSTALLED 个 skill"
[ $SKIPPED -gt 0 ] && echo "  已跳过: $SKIPPED 个"
echo ""
echo "  使用方法:"
echo "    1. 打开 Claude Code: claude"
echo "    2. 输入: /start-army \"你的研究需求\""
echo "    3. 或单独调用: /data-forensics /journal match /quality-review /delivery"
echo ""
echo "  提示:"
echo "    - 首次使用建议用 /data-profiler 单独测试数据探查"
echo "    - 原始数据项目建议先跑 /data-forensics"
echo "    - 期刊格式建议先跑 /journal template"
echo "    - Agent 角色定义在 $SCRIPT_DIR/agents/ 目录"
echo "    - 方法论文档在 $SCRIPT_DIR/methodology/ 目录"
echo "    - 项目模板在 $SCRIPT_DIR/templates/ 目录"
echo ""
