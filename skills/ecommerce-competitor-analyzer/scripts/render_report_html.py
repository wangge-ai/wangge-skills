#!/usr/bin/env python3
"""Render a Markdown ecommerce report into a standalone HTML report."""

from __future__ import annotations

import argparse
import html
import re
from pathlib import Path


CSS = """
:root {
  color-scheme: light;
  --bg: #f6f7fb;
  --paper: #ffffff;
  --ink: #172033;
  --muted: #667085;
  --line: #d9e0ea;
  --brand: #2563eb;
  --brand-soft: #eaf1ff;
  --accent: #f97316;
}
* { box-sizing: border-box; }
body {
  margin: 0;
  padding: 36px 18px;
  background: var(--bg);
  color: var(--ink);
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Microsoft YaHei", sans-serif;
  line-height: 1.78;
}
.report {
  max-width: 1040px;
  margin: 0 auto;
  background: var(--paper);
  border: 1px solid var(--line);
  border-radius: 18px;
  box-shadow: 0 18px 50px rgba(23, 32, 51, 0.08);
  overflow: hidden;
}
.hero {
  padding: 42px 44px 34px;
  color: #fff;
  background: linear-gradient(135deg, #10172a 0%, #17335f 58%, #0f766e 100%);
}
.hero .eyebrow {
  margin: 0 0 12px;
  color: #93c5fd;
  font-size: 12px;
  letter-spacing: 0.24em;
  text-transform: uppercase;
}
.hero h1 {
  margin: 0;
  max-width: 820px;
  font-size: 34px;
  line-height: 1.28;
}
.content {
  padding: 32px 44px 46px;
}
h2 {
  margin: 34px 0 14px;
  padding-left: 12px;
  border-left: 4px solid var(--brand);
  font-size: 22px;
  line-height: 1.35;
}
h3 {
  margin: 26px 0 10px;
  font-size: 18px;
}
p { margin: 10px 0; }
ul, ol { padding-left: 24px; }
li { margin: 6px 0; }
table {
  width: 100%;
  margin: 16px 0 24px;
  border-collapse: collapse;
  font-size: 14px;
}
th {
  background: var(--brand-soft);
  color: #17335f;
  font-weight: 700;
}
th, td {
  padding: 10px 12px;
  border: 1px solid var(--line);
  vertical-align: top;
}
tr:nth-child(even) td { background: #fbfcff; }
code {
  padding: 2px 5px;
  border-radius: 5px;
  background: #eef2f7;
  color: #0f172a;
  font-family: Consolas, Monaco, monospace;
  font-size: 0.92em;
}
pre {
  padding: 16px;
  overflow-x: auto;
  border-radius: 12px;
  background: #111827;
  color: #e5e7eb;
}
pre code {
  padding: 0;
  background: transparent;
  color: inherit;
}
.note {
  margin-top: 34px;
  padding: 14px 16px;
  border: 1px solid #fed7aa;
  border-radius: 12px;
  background: #fff7ed;
  color: #9a3412;
  font-size: 14px;
}
@media (max-width: 720px) {
  body { padding: 16px 10px; }
  .report { border-radius: 12px; }
  .hero { padding: 30px 22px 26px; }
  .hero h1 { font-size: 26px; }
  .content { padding: 22px 18px 30px; }
  table { display: block; overflow-x: auto; white-space: nowrap; }
}
""".strip()


def inline_markdown(text: str) -> str:
    escaped = html.escape(text)
    escaped = re.sub(r"`([^`]+)`", r"<code>\1</code>", escaped)
    escaped = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", escaped)
    return escaped


def is_table_separator(line: str) -> bool:
    cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", cell or "") for cell in cells)


def parse_table(lines: list[str], start: int) -> tuple[str, int]:
    rows: list[list[str]] = []
    index = start
    while index < len(lines) and lines[index].strip().startswith("|") and lines[index].strip().endswith("|"):
        if not (index == start + 1 and is_table_separator(lines[index])):
            rows.append([cell.strip() for cell in lines[index].strip().strip("|").split("|")])
        index += 1

    if not rows:
        return "", index

    header = rows[0]
    body = rows[1:]
    parts = ["<table>", "<thead><tr>"]
    parts.extend(f"<th>{inline_markdown(cell)}</th>" for cell in header)
    parts.append("</tr></thead>")
    if body:
        parts.append("<tbody>")
        for row in body:
            parts.append("<tr>")
            padded = row + [""] * (len(header) - len(row))
            parts.extend(f"<td>{inline_markdown(cell)}</td>" for cell in padded[: len(header)])
            parts.append("</tr>")
        parts.append("</tbody>")
    parts.append("</table>")
    return "\n".join(parts), index


def markdown_to_html(markdown: str) -> tuple[str, str]:
    lines = markdown.splitlines()
    output: list[str] = []
    title = "电商数据分析报告"
    paragraph: list[str] = []
    list_stack: list[str] = []
    in_code = False
    code_lines: list[str] = []

    def flush_paragraph() -> None:
        nonlocal paragraph
        if paragraph:
            output.append(f"<p>{inline_markdown(' '.join(paragraph).strip())}</p>")
            paragraph = []

    def close_lists() -> None:
        while list_stack:
            output.append(f"</{list_stack.pop()}>")

    index = 0
    while index < len(lines):
        raw = lines[index]
        line = raw.rstrip()

        if line.strip().startswith("```"):
            if in_code:
                output.append("<pre><code>" + html.escape("\n".join(code_lines)) + "</code></pre>")
                code_lines = []
                in_code = False
            else:
                flush_paragraph()
                close_lists()
                in_code = True
            index += 1
            continue

        if in_code:
            code_lines.append(line)
            index += 1
            continue

        if not line.strip():
            flush_paragraph()
            close_lists()
            index += 1
            continue

        if line.strip().startswith("|") and index + 1 < len(lines) and is_table_separator(lines[index + 1]):
            flush_paragraph()
            close_lists()
            table_html, next_index = parse_table(lines, index)
            output.append(table_html)
            index = next_index
            continue

        heading = re.match(r"^(#{1,6})\s+(.+)$", line)
        if heading:
            flush_paragraph()
            close_lists()
            level = min(len(heading.group(1)), 3)
            text = heading.group(2).strip()
            if level == 1 and title == "电商数据分析报告":
                title = re.sub(r"<[^>]+>", "", inline_markdown(text))
            output.append(f"<h{level}>{inline_markdown(text)}</h{level}>")
            index += 1
            continue

        bullet = re.match(r"^\s*[-*]\s+(.+)$", line)
        ordered = re.match(r"^\s*\d+[.)]\s+(.+)$", line)
        if bullet or ordered:
            flush_paragraph()
            tag = "ul" if bullet else "ol"
            if not list_stack or list_stack[-1] != tag:
                close_lists()
                output.append(f"<{tag}>")
                list_stack.append(tag)
            output.append(f"<li>{inline_markdown((bullet or ordered).group(1).strip())}</li>")
            index += 1
            continue

        close_lists()
        paragraph.append(line.strip())
        index += 1

    flush_paragraph()
    close_lists()
    return title, "\n".join(output)


def render(markdown: str) -> str:
    title, body = markdown_to_html(markdown)
    safe_title = html.escape(title)
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{safe_title}</title>
  <style>{CSS}</style>
</head>
<body>
  <article class="report">
    <header class="hero">
      <p class="eyebrow">ECOMMERCE DATA REPORT</p>
      <h1>{safe_title}</h1>
    </header>
    <main class="content">
{body}
      <div class="note">本 HTML 由本地 Markdown 报告渲染生成，只负责展示已有报告内容，不额外补充平台实时数据。</div>
    </main>
  </article>
</body>
</html>
"""


def main() -> None:
    parser = argparse.ArgumentParser(description="Render a Markdown report into standalone HTML.")
    parser.add_argument("--input", required=True, help="Input Markdown report path")
    parser.add_argument("--out", required=True, help="Output HTML path")
    args = parser.parse_args()

    input_path = Path(args.input)
    out_path = Path(args.out)
    markdown = input_path.read_text(encoding="utf-8")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(render(markdown), encoding="utf-8")
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
