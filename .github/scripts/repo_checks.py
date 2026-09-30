#!/usr/bin/env python3
"""Repository checks for CI.

Usage:
    python .github/scripts/repo_checks.py                 # 全仓检查（push 到 main）
    python .github/scripts/repo_checks.py --base <ref>    # PR 模式：只对改动部分严格

规则：
- 语法类（Python / Shell / YAML / JSON）和禁止入库文件：全仓检查，失败即报错。
- 密钥：PR 新增的行命中即报错；仓库里已有的只报警告（打码显示）。
- SKILL.md frontmatter、Markdown 相对链接：PR 改动的文件报错，其余只报警告。
  删除或重命名文件导致其他文件的链接失效，也报错。
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote

import yaml

ERRORS: list[str] = []
WARNINGS: list[str] = []

SECRET_PATTERNS = [
    re.compile(r"sk-ant-[A-Za-z0-9_-]{20,}"),
    re.compile(r"sk-[A-Za-z0-9]{32,}"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"gh[pousr]_[A-Za-z0-9]{36}"),
    re.compile(r"github_pat_[A-Za-z0-9_]{50,}"),
    re.compile(r"xox[baprs]-[A-Za-z0-9-]{10,}"),
    re.compile(r"AIza[0-9A-Za-z_-]{35}"),
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
]

FORBIDDEN = [
    (re.compile(r"(^|/)\.env$"), ".env 文件"),
    (re.compile(r"^clients/"), "客户数据目录 clients/"),
    (re.compile(r"\.db(-shm|-wal)?$"), "数据库文件"),
]

LINK_RE = re.compile(r"!?\[[^\]]*\]\(\s*<?([^)\s>]+)>?(?:\s+\"[^\"]*\")?\s*\)")
FENCE_RE = re.compile(r"^(```|~~~).*?^\1", re.S | re.M)


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], text=True)


def annotate(level: str, path: str, line: int | None, msg: str) -> None:
    loc = f"file={path}" + (f",line={line}" if line else "")
    text = f"{path}{f':{line}' if line else ''}: {msg}"
    print(f"::{level} {loc}::{msg}")
    (ERRORS if level == "error" else WARNINGS).append(text)


def mask(secret: str) -> str:
    return secret[:6] + "****"


def check_syntax(tracked: list[str]) -> None:
    for f in tracked:
        if f.endswith(".py"):
            try:
                compile(Path(f).read_bytes(), f, "exec")
            except SyntaxError as e:
                annotate("error", f, e.lineno, f"Python 语法错误: {e.msg}")
        elif f.endswith(".sh"):
            r = subprocess.run(["bash", "-n", f], capture_output=True, text=True)
            if r.returncode:
                annotate("error", f, None, f"Shell 语法错误: {r.stderr.strip()}")
        elif f.endswith((".yaml", ".yml")):
            try:
                with open(f, encoding="utf-8") as fh:
                    list(yaml.safe_load_all(fh))
            except yaml.YAMLError as e:
                line = e.problem_mark.line + 1 if getattr(e, "problem_mark", None) else None
                annotate("error", f, line, f"YAML 解析失败: {getattr(e, 'problem', e)}")
        elif f.endswith(".json"):
            try:
                with open(f, encoding="utf-8") as fh:
                    json.load(fh)
            except json.JSONDecodeError as e:
                annotate("error", f, e.lineno, f"JSON 解析失败: {e.msg}")


def check_forbidden(tracked: list[str]) -> None:
    for f in tracked:
        for pattern, label in FORBIDDEN:
            if pattern.search(f):
                annotate("error", f, None, f"禁止入库：{label}（见 CONTRIBUTING.md 安全红线）")


def added_lines(base: str) -> dict[str, list[tuple[int, str]]]:
    """PR 中新增的行：{文件: [(行号, 内容)]}。"""
    out: dict[str, list[tuple[int, str]]] = {}
    current = None
    lineno = 0
    for raw in git("diff", "--unified=0", "--no-color", f"{base}...HEAD").splitlines():
        if raw.startswith("+++ "):
            current = raw[6:] if raw.startswith("+++ b/") else None
        elif raw.startswith("@@"):
            m = re.search(r"\+(\d+)", raw)
            lineno = int(m.group(1)) if m else 0
        elif current and raw.startswith("+") and not raw.startswith("+++"):
            out.setdefault(current, []).append((lineno, raw[1:]))
            lineno += 1
    return out


def check_secrets(tracked: list[str], base: str | None) -> None:
    new = added_lines(base) if base else {}
    flagged = {(f, n) for f, lines in new.items() for n, _ in lines}
    for f, lines in new.items():
        for n, text in lines:
            for p in SECRET_PATTERNS:
                m = p.search(text)
                if m:
                    annotate("error", f, n, f"新增内容疑似包含密钥 {mask(m.group(0))}，请删除并作废该密钥")
    for f in tracked:
        try:
            content = Path(f).read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for n, text in enumerate(content.splitlines(), 1):
            if (f, n) in flagged:
                continue
            for p in SECRET_PATTERNS:
                m = p.search(text)
                if m:
                    annotate("warning", f, n, f"仓库中已有疑似密钥 {mask(m.group(0))}，建议作废并改用环境变量")


def check_skill_frontmatter(path: str, strict: bool) -> None:
    level = "error" if strict else "warning"
    text = Path(path).read_text(encoding="utf-8")
    body = re.sub(r"\A\s*(<!--.*?-->\s*)*", "", text, flags=re.S)
    m = re.match(r"---\n(.*?)\n---\s*\n", body, re.S)
    if not m:
        annotate(level, path, 1, "SKILL.md 缺少 YAML frontmatter（需要 name 和 description）")
        return
    try:
        fm = yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError as e:
        annotate(level, path, 1, f"SKILL.md frontmatter 解析失败: {e}")
        return
    missing = [k for k in ("name", "description") if not fm.get(k)]
    if missing:
        annotate(level, path, 1, f"SKILL.md frontmatter 缺少字段: {', '.join(missing)}")
    elif fm["name"] != Path(path).parent.name:
        annotate(level, path, 1, f"frontmatter name '{fm['name']}' 与目录名 '{Path(path).parent.name}' 不一致")


def check_links(path: str, strict: bool, known: set[str], deleted: set[str]) -> None:
    text = Path(path).read_text(encoding="utf-8")
    # 代码块内容替换为空格，保留行号
    text = FENCE_RE.sub(lambda m: re.sub(r"[^\n]", " ", m.group(0)), text)
    for m in LINK_RE.finditer(text):
        target = m.group(1)
        if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", target) or target.startswith(("#", "/")):
            continue
        rel = unquote(target.split("#")[0].split("?")[0])
        if not rel:
            continue
        resolved = os.path.normpath(str(Path(path).parent / rel))
        if resolved in known:
            continue
        line = text.count("\n", 0, m.start()) + 1
        if strict or resolved in deleted:
            annotate("error", path, line, f"链接目标不存在: {target}")
        else:
            annotate("warning", path, line, f"链接目标不存在: {target}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", help="PR 的 base commit；不传则按全仓模式运行")
    args = parser.parse_args()

    tracked = [f for f in git("ls-files").splitlines() if Path(f).is_file()]
    known = set(tracked) | {str(p) for f in tracked for p in Path(f).parents if str(p) != "."}

    changed: set[str] = set()
    deleted: set[str] = set()
    if args.base:
        for row in git("diff", "--name-status", "-M", f"{args.base}...HEAD").splitlines():
            parts = row.split("\t")
            status = parts[0]
            if status.startswith("D"):
                deleted.add(parts[1])
            elif status.startswith("R"):
                deleted.add(parts[1])
                changed.add(parts[2])
            else:
                changed.add(parts[-1])

    check_syntax(tracked)
    check_forbidden(tracked)
    check_secrets(tracked, args.base)
    for f in tracked:
        if re.fullmatch(r"skills/[^/]+/SKILL\.md", f):
            check_skill_frontmatter(f, strict=f in changed)
        if f.endswith(".md"):
            check_links(f, strict=f in changed, known=known, deleted=deleted)

    print(f"\n检查完成：{len(ERRORS)} 个错误，{len(WARNINGS)} 个警告"
          + (f"（PR 改动文件 {len(changed)} 个）" if args.base else "（全仓模式）"))
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        with open(summary, "a", encoding="utf-8") as fh:
            fh.write(f"## 仓库检查\n\n错误 {len(ERRORS)} 个，警告 {len(WARNINGS)} 个\n\n")
            for label, items in (("错误", ERRORS), ("警告", WARNINGS)):
                if items:
                    fh.write(f"### {label}\n\n" + "".join(f"- {i}\n" for i in items) + "\n")
    return 1 if ERRORS else 0


if __name__ == "__main__":
    sys.exit(main())
