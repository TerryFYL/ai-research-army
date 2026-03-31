#!/usr/bin/env python3
"""
期刊投稿指南爬取器
==================
自动获取目标期刊的 submission guidelines 页面，提取结构化格式要求。
处理重定向、JS 渲染等常见问题。

用法:
    python3 fetch_guidelines.py <journal_name_or_url> [-o output_path]

输出:
    结构化 Markdown 文件，包含所有投稿格式要求。
    退出码: 0=成功, 1=部分成功(需人工补充), 2=失败
"""

import argparse
import json
import re
import sys
import urllib.request
import urllib.error
from pathlib import Path
from datetime import datetime

# 常见期刊的投稿指南 URL 映射
JOURNAL_URLS = {
    "bmc psychiatry": [
        "https://bmcpsychiatry.biomedcentral.com/submission-guidelines/preparing-your-manuscript/research-article",
        "https://bmcpsychiatry.biomedcentral.com/submission-guidelines",
    ],
    "frontiers in psychiatry": [
        "https://www.frontiersin.org/journals/psychiatry/for-authors/author-guidelines",
    ],
    "journal of affective disorders": [
        "https://www.elsevier.com/journals/journal-of-affective-disorders/0165-0327/guide-for-authors",
    ],
    "psychiatry research": [
        "https://www.elsevier.com/journals/psychiatry-research/0165-1781/guide-for-authors",
    ],
    "comprehensive psychiatry": [
        "https://www.elsevier.com/journals/comprehensive-psychiatry/0010-440x/guide-for-authors",
    ],
    "jad reports": [
        "https://www.elsevier.com/journals/journal-of-affective-disorders-reports/2666-9153/guide-for-authors",
    ],
}

# 结构化提取模板
REQUIREMENTS_TEMPLATE = """# {journal_name} — 投稿格式要求

> 抓取日期: {date}
> 来源: {source_url}
> 文章类型: Research Article

---

## 1. 稿件结构

### 必需章节（按顺序）
{sections}

### 标题页要求
{title_page}

## 2. 摘要
- **字数限制**: {abstract_limit}
- **结构**: {abstract_structure}
- **其他**: {abstract_notes}

## 3. 正文
- **字数限制**: {word_limit}
- **章节标题格式**: {heading_format}

## 4. 参考文献
- **引用格式**: {citation_style}
- **文献列表格式**: {reference_format}
- **示例**: {reference_example}

## 5. 图表
- **图片格式**: {figure_formats}
- **分辨率**: {figure_dpi}
- **尺寸限制**: {figure_size}
- **图注位置**: {caption_position}

## 6. 声明部分 (Declarations)
{declarations}

## 7. 补充材料
{supplementary}

## 8. 文件格式
- **主稿**: {manuscript_format}
- **图片**: {figure_upload}

## 9. Reporting Guidelines
{reporting_guidelines}

## 10. 其他特殊要求
{special_requirements}

---

## 合规检查清单

{checklist}
"""


def fetch_url(url: str, max_redirects: int = 5) -> tuple[str, str]:
    """获取 URL 内容，处理重定向。返回 (content, final_url)"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
    }

    current_url = url
    for i in range(max_redirects):
        req = urllib.request.Request(current_url, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                final_url = resp.geturl()
                content = resp.read().decode("utf-8", errors="replace")
                return content, final_url
        except urllib.error.HTTPError as e:
            if e.code in (301, 302, 303, 307, 308):
                redirect_url = e.headers.get("Location", "")
                if redirect_url:
                    if redirect_url.startswith("/"):
                        from urllib.parse import urlparse
                        parsed = urlparse(current_url)
                        redirect_url = f"{parsed.scheme}://{parsed.netloc}{redirect_url}"
                    current_url = redirect_url
                    continue
            raise
    raise Exception(f"Too many redirects (>{max_redirects})")


def html_to_text(html: str) -> str:
    """简单的 HTML → 纯文本转换"""
    # 移除 script/style
    html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)
    html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL | re.IGNORECASE)
    # 段落和换行
    html = re.sub(r'<br\s*/?>', '\n', html, flags=re.IGNORECASE)
    html = re.sub(r'</(p|div|li|h[1-6])>', '\n', html, flags=re.IGNORECASE)
    html = re.sub(r'<(h[1-6])[^>]*>', '\n## ', html, flags=re.IGNORECASE)
    html = re.sub(r'<li[^>]*>', '- ', html, flags=re.IGNORECASE)
    # 移除所有标签
    html = re.sub(r'<[^>]+>', '', html)
    # 清理空行
    html = re.sub(r'\n{3,}', '\n\n', html)
    # 解码 HTML 实体
    html = html.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
    html = html.replace('&nbsp;', ' ').replace('&#8217;', "'").replace('&#8220;', '"').replace('&#8221;', '"')
    return html.strip()


def fetch_guidelines(journal_name: str, custom_url: str = None) -> tuple[str, str]:
    """获取期刊投稿指南原始文本"""
    urls = []
    if custom_url:
        urls = [custom_url]
    else:
        key = journal_name.lower().strip()
        urls = JOURNAL_URLS.get(key, [])

    if not urls:
        print(f"WARNING: No known URL for '{journal_name}'. Please provide URL with -u flag.", file=sys.stderr)
        return "", ""

    for url in urls:
        try:
            print(f"Fetching: {url}", file=sys.stderr)
            html, final_url = fetch_url(url)
            text = html_to_text(html)
            if len(text) > 500:  # 有实质内容
                return text, final_url
            print(f"  Content too short ({len(text)} chars), trying next URL...", file=sys.stderr)
        except Exception as e:
            print(f"  Failed: {e}", file=sys.stderr)

    return "", ""


def generate_empty_template(journal_name: str, source_url: str = "") -> str:
    """生成空模板供人工填写"""
    return REQUIREMENTS_TEMPLATE.format(
        journal_name=journal_name,
        date=datetime.now().strftime("%Y-%m-%d"),
        source_url=source_url or "[需人工填写]",
        sections="[需人工填写: 如 Background, Methods, Results, Discussion, Conclusions]",
        title_page="[需人工填写]",
        abstract_limit="[需人工填写: 如 ≤350 words]",
        abstract_structure="[需人工填写: 如 Background/Methods/Results/Conclusions]",
        abstract_notes="[需人工填写]",
        word_limit="[需人工填写: 如 无限制 / ≤5000 words]",
        heading_format="[需人工填写]",
        citation_style="[需人工填写: 如 编号[1] / Author-Date (Author, Year)]",
        reference_format="[需人工填写]",
        reference_example="[需人工填写]",
        figure_formats="[需人工填写: 如 TIFF, PNG, PDF, EPS]",
        figure_dpi="[需人工填写: 如 ≥300 DPI]",
        figure_size="[需人工填写]",
        caption_position="[需人工填写]",
        declarations="[需人工填写]",
        supplementary="[需人工填写]",
        manuscript_format="[需人工填写: 如 Word (.docx) / LaTeX]",
        figure_upload="[需人工填写]",
        reporting_guidelines="[需人工填写: 如 STROBE for observational studies]",
        special_requirements="[需人工填写]",
        checklist="- [ ] 各项待确认",
    )


def main():
    parser = argparse.ArgumentParser(description="期刊投稿指南爬取器")
    parser.add_argument("journal", help="期刊名称 (如 'BMC Psychiatry') 或 'list' 查看支持列表")
    parser.add_argument("-u", "--url", help="自定义投稿指南 URL")
    parser.add_argument("-o", "--output", help="输出文件路径")
    parser.add_argument("--raw", action="store_true", help="输出原始爬取文本（不做结构化）")
    args = parser.parse_args()

    if args.journal.lower() == "list":
        print("支持的期刊:")
        for name in sorted(JOURNAL_URLS.keys()):
            print(f"  - {name}")
        sys.exit(0)

    # 爬取
    text, final_url = fetch_guidelines(args.journal, args.url)

    if not text:
        print(f"\nERROR: 无法自动获取 '{args.journal}' 的投稿指南。", file=sys.stderr)
        print("生成空模板供人工填写...", file=sys.stderr)
        result = generate_empty_template(args.journal, args.url or "")
        exit_code = 1
    elif args.raw:
        result = f"# Raw Guidelines: {args.journal}\n# Source: {final_url}\n# Date: {datetime.now().strftime('%Y-%m-%d')}\n\n{text}"
        exit_code = 0
    else:
        # 输出原始文本 + 空模板（让 AI 来填充）
        result = f"""# {args.journal} — 投稿指南原始文本

> 抓取日期: {datetime.now().strftime('%Y-%m-%d')}
> 来源: {final_url}

---

## 原始内容

{text[:15000]}

---

## 结构化要求（需 AI 从上方原始文本提取填充）

{generate_empty_template(args.journal, final_url)}
"""
        exit_code = 1  # 需要 AI 进一步处理

    # 输出
    if args.output:
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)
        Path(args.output).write_text(result, encoding="utf-8")
        print(f"Saved to: {args.output}", file=sys.stderr)
    else:
        print(result)

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
