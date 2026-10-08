#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build a standalone HTML tutorial report from a generated Markdown file."""

from __future__ import annotations

import argparse
import html
import re
import sys
from pathlib import Path


HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
ORDERED_RE = re.compile(r"^\d+\.\s+(.+?)\s*$")
UNORDERED_RE = re.compile(r"^[-*]\s+(.+?)\s*$")
FENCE_RE = re.compile(r"^```(\w+)?\s*$")


def inline_markup(text: str) -> str:
    escaped = html.escape(text, quote=True)
    escaped = re.sub(r"`([^`]+)`", r"<code>\1</code>", escaped)
    escaped = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", escaped)
    escaped = re.sub(
        r"\[([^\]]+)\]\((https?://[^)]+)\)",
        r'<a href="\2" target="_blank" rel="noopener noreferrer">\1</a>',
        escaped,
    )
    return escaped


def slugify(title: str, used: set[str]) -> str:
    chapter_match = re.search(r"第\s*(\d+)\s*章", title)
    ascii_words = re.findall(r"[A-Za-z0-9]+", title)
    if chapter_match:
        prefix = f"chapter-{chapter_match.group(1)}"
        suffix = "-".join(word.lower() for word in ascii_words if not word.isdigit())
        base = f"{prefix}-{suffix}" if suffix else prefix
    elif ascii_words:
        base = "-".join(word.lower() for word in ascii_words)
    else:
        base = "section"

    candidate = base
    n = 2
    while candidate in used:
        candidate = f"{base}-{n}"
        n += 1
    used.add(candidate)
    return candidate


def close_list(lines: list[str], list_type: str | None) -> str | None:
    if list_type:
        lines.append(f"</{list_type}>")
    return None


def is_table_row(line: str) -> bool:
    stripped = line.strip()
    return stripped.startswith("|") and stripped.endswith("|") and stripped.count("|") >= 2


def split_table_row(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def is_table_separator(line: str) -> bool:
    if not is_table_row(line):
        return False
    cells = split_table_row(line)
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells)


def render_table(header: list[str], rows: list[list[str]]) -> str:
    head = "".join(f"<th>{inline_markup(cell)}</th>" for cell in header)
    body_rows = []
    for row in rows:
        padded = row + [""] * max(0, len(header) - len(row))
        body_rows.append(
            "<tr>"
            + "".join(f"<td>{inline_markup(cell)}</td>" for cell in padded[: len(header)])
            + "</tr>"
        )
    return (
        '<div class="table-scroll"><table>\n<thead><tr>'
        + head
        + "</tr></thead>\n<tbody>\n"
        + "\n".join(body_rows)
        + "\n</tbody>\n</table></div>"
    )


def render_markdown(markdown_text: str) -> tuple[str, list[tuple[int, str, str]]]:
    html_lines: list[str] = []
    toc: list[tuple[int, str, str]] = []
    used_slugs: set[str] = set()
    in_code = False
    code_lang = ""
    code_lines: list[str] = []
    list_type: str | None = None

    source_lines = markdown_text.splitlines()
    i = 0
    while i < len(source_lines):
        raw_line = source_lines[i]
        line = raw_line.rstrip()

        fence = FENCE_RE.match(line)
        if fence:
            if in_code:
                escaped_code = html.escape("\n".join(code_lines), quote=False)
                lang_attr = f' data-lang="{html.escape(code_lang)}"' if code_lang else ""
                html_lines.append(f"<pre{lang_attr}><code>{escaped_code}</code></pre>")
                code_lines = []
                code_lang = ""
                in_code = False
            else:
                list_type = close_list(html_lines, list_type)
                in_code = True
                code_lang = fence.group(1) or ""
            i += 1
            continue

        if in_code:
            code_lines.append(raw_line)
            i += 1
            continue

        if not line.strip():
            list_type = close_list(html_lines, list_type)
            i += 1
            continue

        if i + 1 < len(source_lines) and is_table_row(line) and is_table_separator(source_lines[i + 1]):
            list_type = close_list(html_lines, list_type)
            header = split_table_row(line)
            rows: list[list[str]] = []
            i += 2
            while i < len(source_lines) and is_table_row(source_lines[i]):
                rows.append(split_table_row(source_lines[i]))
                i += 1
            html_lines.append(render_table(header, rows))
            continue

        heading = HEADING_RE.match(line)
        if heading:
            list_type = close_list(html_lines, list_type)
            level = len(heading.group(1))
            title = heading.group(2).strip()
            slug = slugify(title, used_slugs)
            toc.append((level, slug, title))
            html_lines.append(
                f'<h{level} id="{slug}">{inline_markup(title)}</h{level}>'
            )
            i += 1
            continue

        ordered = ORDERED_RE.match(line)
        if ordered:
            if list_type != "ol":
                list_type = close_list(html_lines, list_type)
                html_lines.append("<ol>")
                list_type = "ol"
            html_lines.append(f"<li>{inline_markup(ordered.group(1))}</li>")
            i += 1
            continue

        unordered = UNORDERED_RE.match(line)
        if unordered:
            if list_type != "ul":
                list_type = close_list(html_lines, list_type)
                html_lines.append("<ul>")
                list_type = "ul"
            html_lines.append(f"<li>{inline_markup(unordered.group(1))}</li>")
            i += 1
            continue

        if line.startswith(">"):
            list_type = close_list(html_lines, list_type)
            html_lines.append(f"<blockquote>{inline_markup(line.lstrip('> '))}</blockquote>")
            i += 1
            continue

        list_type = close_list(html_lines, list_type)
        html_lines.append(f"<p>{inline_markup(line)}</p>")
        i += 1

    if in_code:
        escaped_code = html.escape("\n".join(code_lines), quote=False)
        html_lines.append(f"<pre><code>{escaped_code}</code></pre>")
    close_list(html_lines, list_type)
    return "\n".join(html_lines), toc


def build_toc(toc: list[tuple[int, str, str]]) -> str:
    items = []
    for level, slug, title in toc:
        if level <= 3:
            indent_class = " toc-sub" if level == 3 else ""
            items.append(
                f'<a class="toc-item{indent_class}" href="#{slug}">{inline_markup(title)}</a>'
            )
    return "\n".join(items)


def build_html(title: str, content: str, toc_html: str, toc: list[tuple[int, str, str]]) -> str:
    safe_title = html.escape(title, quote=True)
    chapter_count = sum(1 for level, _, heading in toc if level == 2 and "第" in heading and "章" in heading)
    chapter_label = f"{chapter_count} 章" if chapter_count else "完整"
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{safe_title}</title>
  <style>
    /* warm editorial tutorial report */
    :root {{
      --bg-a: hsl(42, 38%, 91%);
      --bg-b: hsl(31, 34%, 88%);
      --bg-c: hsl(76, 18%, 88%);
      --surface: hsl(42, 34%, 97%);
      --surface-soft: hsl(38, 30%, 94%);
      --surface-strong: hsl(35, 32%, 90%);
      --ink: hsl(28, 22%, 15%);
      --ink-2: hsl(30, 13%, 35%);
      --muted: hsl(32, 10%, 50%);
      --line: hsla(30, 18%, 34%, 0.16);
      --line-strong: hsla(30, 18%, 28%, 0.26);
      --accent: hsl(25, 58%, 42%);
      --accent-2: hsl(38, 52%, 47%);
      --accent-3: hsl(92, 22%, 38%);
      --accent-soft: hsla(34, 58%, 72%, 0.22);
      --code-bg: hsl(28, 24%, 16%);
      --code-ink: hsl(42, 30%, 90%);
      --hero-ink: hsl(42, 34%, 94%);
      --hero-muted: hsl(42, 22%, 82%);
      --hero-soft: hsl(42, 18%, 78%);
      --hero-panel: hsla(42, 28%, 92%, 0.12);
      --hero-stroke: hsla(42, 28%, 92%, 0.18);
      --hero-stroke-strong: hsla(42, 28%, 92%, 0.24);
      --code-stroke: hsla(42, 22%, 88%, 0.08);
      --toc-divider: hsla(30, 18%, 34%, 0.12);
      --glow: hsla(36, 48%, 58%, 0.24);
      --gradient-page: radial-gradient(circle at 12% 10%, var(--glow), transparent 30%), linear-gradient(135deg, var(--bg-a), var(--bg-b), var(--bg-c));
      --gradient-hero: radial-gradient(circle at 84% 18%, hsla(44, 70%, 68%, 0.28), transparent 34%), linear-gradient(135deg, hsl(20, 38%, 28%), hsl(28, 42%, 38%), hsl(75, 24%, 34%));
      --gradient-card: linear-gradient(145deg, var(--surface), var(--surface-soft));
      --gradient-line: linear-gradient(90deg, var(--accent), var(--accent-2), var(--accent-3));
      --shadow-sm: 0 10px 24px hsla(28, 24%, 16%, 0.08);
      --shadow-md: 0 24px 70px hsla(28, 24%, 16%, 0.14);
      --radius-sm: 8px;
      --radius-md: 12px;
      --radius-lg: 18px;
      --space-1: 4px;
      --space-2: 8px;
      --space-3: 12px;
      --space-4: 16px;
      --space-5: 20px;
      --space-6: 24px;
      --space-8: 32px;
      --space-10: 40px;
      --space-12: 48px;
      --text-sm: 14px;
      --text-base: 16px;
      --text-lg: 18px;
      --text-xl: 22px;
      --text-2xl: 28px;
      --text-3xl: 40px;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      background: var(--gradient-page);
      color: var(--ink);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Microsoft YaHei", sans-serif;
      line-height: 1.78;
    }}
    body::before {{
      content: "";
      position: fixed;
      inset: 0;
      pointer-events: none;
      background-image: linear-gradient(var(--line) 1px, transparent 1px), linear-gradient(90deg, var(--line) 1px, transparent 1px);
      background-size: 56px 56px;
      opacity: .18;
    }}
    .shell {{
      display: grid;
      grid-template-columns: minmax(236px, 292px) minmax(0, 860px);
      gap: var(--space-8);
      max-width: 1240px;
      margin: 0 auto;
      padding: var(--space-8) var(--space-6) 64px;
      position: relative;
    }}
    .toc {{
      position: sticky;
      top: var(--space-6);
      align-self: start;
      max-height: calc(100vh - 48px);
      overflow: auto;
      padding: var(--space-5);
      background: var(--gradient-card);
      border: 1px solid var(--line);
      border-radius: var(--radius-lg);
      box-shadow: var(--shadow-sm);
    }}
    .toc-title {{
      margin: 0 0 var(--space-3);
      font-size: var(--text-base);
      font-weight: 700;
      color: var(--ink);
    }}
    .toc-item {{
      display: block;
      padding: 8px 0;
      color: var(--muted);
      text-decoration: none;
      font-size: var(--text-sm);
      border-bottom: 1px solid var(--toc-divider);
    }}
    .toc-item:hover {{
      color: var(--accent);
    }}
    .toc-sub {{
      padding-left: var(--space-4);
      font-size: 13px;
    }}
    .content {{
      min-width: 0;
    }}
    .hero {{
      min-height: 330px;
      display: flex;
      flex-direction: column;
      justify-content: flex-end;
      gap: var(--space-6);
      margin-bottom: var(--space-8);
      padding: var(--space-10);
      color: var(--code-ink);
      background: var(--gradient-hero);
      border: 1px solid var(--line-strong);
      border-radius: 24px;
      box-shadow: var(--shadow-md);
      overflow: hidden;
      position: relative;
    }}
    .hero::after {{
      content: "";
      position: absolute;
      left: var(--space-10);
      right: var(--space-10);
      bottom: 0;
      height: 5px;
      background: var(--gradient-line);
      border-radius: 99px 99px 0 0;
    }}
    .eyebrow {{
      width: fit-content;
      padding: 6px 12px;
      border: 1px solid var(--hero-stroke-strong);
      border-radius: 999px;
      background: var(--hero-panel);
      color: var(--code-ink);
      font-size: 12px;
      letter-spacing: 0;
    }}
    .hero h1 {{
      max-width: 760px;
      margin: 0;
      font-size: clamp(34px, 5vw, 58px);
      line-height: 1.08;
      color: var(--hero-ink);
      letter-spacing: 0;
    }}
    .hero p {{
      max-width: 680px;
      margin: 0;
      color: var(--hero-muted);
      font-size: var(--text-lg);
    }}
    .hero-kpis {{
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: var(--space-3);
      max-width: 720px;
    }}
      .hero-kpi {{
      padding: var(--space-4);
      background: var(--hero-panel);
      border: 1px solid var(--hero-stroke);
      border-radius: var(--radius-md);
    }}
    .hero-kpi strong {{
      display: block;
      margin-bottom: var(--space-1);
      color: var(--hero-ink);
      font-size: var(--text-xl);
      line-height: 1.2;
    }}
    .hero-kpi span {{
      color: var(--hero-soft);
      font-size: 13px;
    }}
    main {{
      background: var(--gradient-card);
      border: 1px solid var(--line);
      border-radius: 22px;
      padding: var(--space-10) min(5vw, 58px);
      box-shadow: var(--shadow-md);
    }}
    h1 {{
      margin: 0 0 16px;
      font-size: clamp(30px, 5vw, 44px);
      line-height: 1.18;
      letter-spacing: 0;
    }}
    h2 {{
      margin-top: var(--space-12);
      padding-top: var(--space-6);
      border-top: 1px solid var(--line);
      font-size: var(--text-2xl);
      letter-spacing: 0;
      position: relative;
    }}
    h2::before {{
      content: "";
      display: block;
      width: 72px;
      height: 4px;
      margin-bottom: var(--space-4);
      background: var(--gradient-line);
      border-radius: 99px;
    }}
    h3 {{
      margin-top: var(--space-8);
      font-size: var(--text-xl);
      letter-spacing: 0;
      color: var(--ink-2);
    }}
    p, li, blockquote {{
      font-size: var(--text-base);
    }}
    p {{
      max-width: 38em;
    }}
    blockquote {{
      margin: var(--space-5) 0;
      padding: var(--space-4) var(--space-5);
      background: var(--accent-soft);
      border-left: 4px solid var(--accent);
      border-radius: var(--radius-md);
      color: var(--ink-2);
    }}
    code {{
      padding: 2px 6px;
      border-radius: 6px;
      background: var(--surface-strong);
      font-family: Consolas, "SFMono-Regular", monospace;
      font-size: .92em;
    }}
    pre {{
      overflow-x: auto;
      padding: var(--space-5);
      border-radius: var(--radius-md);
      background: var(--code-bg);
      color: var(--code-ink);
      box-shadow: inset 0 0 0 1px var(--code-stroke);
    }}
    pre code {{
      padding: 0;
      background: transparent;
      color: inherit;
      font-size: var(--text-sm);
    }}
    .table-scroll {{
      width: 100%;
      overflow-x: auto;
      margin: var(--space-6) 0;
      border: 1px solid var(--line);
      border-radius: var(--radius-md);
      box-shadow: var(--shadow-sm);
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      min-width: 620px;
      background: var(--surface);
    }}
    th, td {{
      padding: 12px 14px;
      border: 1px solid var(--line);
      text-align: left;
      vertical-align: top;
      font-size: 15px;
    }}
    th {{
      background: var(--gradient-hero);
      color: var(--code-ink);
      font-weight: 700;
    }}
    tbody tr:nth-child(even) {{
      background: var(--surface-soft);
    }}
    tbody tr:hover {{
      background: var(--accent-soft);
    }}
    a {{
      color: var(--accent);
      overflow-wrap: anywhere;
    }}
    @media (max-width: 860px) {{
      .shell {{
        display: block;
        padding: var(--space-4) var(--space-3) var(--space-10);
      }}
      .toc {{
        position: static;
        margin-bottom: var(--space-4);
        max-height: none;
      }}
      .hero {{
        min-height: 0;
        padding: var(--space-6);
      }}
      .hero-kpis {{
        grid-template-columns: 1fr;
      }}
      main {{
        padding: var(--space-6) var(--space-4);
      }}
    }}
  </style>
</head>
<body>
  <div class="shell">
    <aside class="toc">
      <p class="toc-title">目录</p>
      {toc_html}
    </aside>
    <div class="content">
      <section class="hero">
        <div class="eyebrow">PRODUCT TUTORIAL</div>
        <div>
          <h1>{safe_title}</h1>
          <p>按章节阅读操作步骤、示例和检查方法，完成教程中给出的练习。</p>
        </div>
        <div class="hero-kpis">
          <div class="hero-kpi"><strong>{chapter_label}</strong><span>教程结构</span></div>
          <div class="hero-kpi"><strong>MD + HTML</strong><span>双格式交付</span></div>
          <div class="hero-kpi"><strong>本地可打开</strong><span>适合分享预览</span></div>
        </div>
      </section>
      <main>
        {content}
      </main>
    </div>
  </div>
</body>
</html>
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convert a generated tutorial Markdown file to a standalone HTML report."
    )
    parser.add_argument("--input", required=True, help="Markdown input path")
    parser.add_argument("--output", required=True, help="HTML output path")
    parser.add_argument("--title", default=None, help="HTML title")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    input_path = Path(args.input)
    output_path = Path(args.output)
    if not input_path.exists():
        print(f"[error] input file not found: {input_path}", file=sys.stderr)
        return 2

    markdown_text = input_path.read_text(encoding="utf-8")
    title = args.title
    if not title:
        first_heading = next(
            (line[2:].strip() for line in markdown_text.splitlines() if line.startswith("# ")),
            input_path.stem,
        )
        title = first_heading

    body, toc = render_markdown(markdown_text)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(build_html(title, body, build_toc(toc), toc), encoding="utf-8")
    print(f"[ok] HTML report written: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
