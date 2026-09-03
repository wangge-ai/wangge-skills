#!/usr/bin/env python3
"""Create a portable before/after visual comparison page from screenshots."""

from __future__ import annotations

import argparse
import html
import json
import os
from pathlib import Path


def parse_pair(value: str) -> dict[str, str]:
    parts = value.split("|", 2)
    if len(parts) != 3 or not all(part.strip() for part in parts):
        raise argparse.ArgumentTypeError("pair must be LABEL|BEFORE|AFTER")
    return {"label": parts[0].strip(), "before": parts[1].strip(), "after": parts[2].strip()}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build a tabbed before/after screenshot comparator.")
    parser.add_argument("--output", required=True, help="Path to the generated HTML file.")
    parser.add_argument("--title", default="Visual comparison", help="Page title.")
    parser.add_argument("--pair", action="append", type=parse_pair, help="Repeat: LABEL|BEFORE|AFTER")
    parser.add_argument("--manifest", help="JSON file with {title?, pairs:[{label,before,after}]}.")
    args = parser.parse_args()
    if bool(args.pair) == bool(args.manifest):
        parser.error("provide either one or more --pair values, or --manifest")
    return args


def is_url(value: str) -> bool:
    return value.startswith(("data:", "http://", "https://", "file://"))


def relative_asset(value: str, output_dir: Path) -> str:
    if is_url(value):
        return value
    return Path(os.path.relpath(Path(value).resolve(), output_dir.resolve())).as_posix()


def load_pairs(args: argparse.Namespace, output_dir: Path) -> tuple[str, list[dict[str, str]]]:
    title = args.title
    pairs = args.pair
    if args.manifest:
        data = json.loads(Path(args.manifest).read_text(encoding="utf-8"))
        title = data.get("title", title)
        pairs = data.get("pairs", [])
    normalized = []
    for pair in pairs:
        if not all(key in pair and str(pair[key]).strip() for key in ("label", "before", "after")):
            raise ValueError("each pair needs label, before, and after")
        normalized.append(
            {
                "label": str(pair["label"]),
                "before": relative_asset(str(pair["before"]), output_dir),
                "after": relative_asset(str(pair["after"]), output_dir),
            }
        )
    if not normalized:
        raise ValueError("at least one comparison pair is required")
    return title, normalized


def build_html(title: str, pairs: list[dict[str, str]]) -> str:
    payload = json.dumps(pairs, ensure_ascii=False).replace("</", "<\\/")
    safe_title = html.escape(title)
    return f"""<!doctype html>
<html lang=\"zh-CN\">
<head>
  <meta charset=\"utf-8\">
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
  <title>{safe_title}</title>
  <style>
    :root {{
      --canvas: #FEFDFC;
      --surface: #FCF9F5;
      --surface-2: #F4EDE3;
      --text: #2A241E;
      --muted: #756A5F;
      --border: #E2D7C7;
      --accent: #B98A6E;
      --accent-soft: #E8CDBB;
      --focus: #7A4E37;
      --space-1: 4px;
      --space-2: 8px;
      --space-3: 12px;
      --space-4: 16px;
      --space-5: 24px;
      --space-6: 32px;
      --radius: 8px;
      --font: \"PingFang SC\", \"Microsoft YaHei UI\", sans-serif;
      --mono: \"Cascadia Mono\", Consolas, monospace;
    }}
    * {{ box-sizing: border-box; }}
    body {{ margin: 0; color: var(--text); background: var(--canvas); font-family: var(--font); }}
    main {{ width: min(100%, 1600px); margin: 0 auto; padding: var(--space-6); }}
    .eyebrow {{ margin: 0; color: var(--muted); font-family: var(--mono); font-size: 12px; letter-spacing: 0.12em; text-transform: uppercase; }}
    h1 {{ margin: var(--space-3) 0 0; font-size: 36px; font-weight: 500; line-height: 1.2; }}
    .tabs {{ display: flex; flex-wrap: wrap; gap: var(--space-2); margin-top: var(--space-5); border-bottom: 1px solid var(--border); padding-bottom: var(--space-3); }}
    .tab {{ min-height: 44px; border: 1px solid var(--border); border-radius: var(--radius); padding: 0 var(--space-4); color: var(--text); background: var(--surface); font: inherit; cursor: pointer; }}
    .tab[aria-selected=\"true\"] {{ border-color: var(--accent); background: var(--accent-soft); font-weight: 700; }}
    .tab:focus-visible {{ outline: 2px solid var(--focus); outline-offset: 2px; }}
    .comparison {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: var(--space-5); margin-top: var(--space-5); }}
    figure {{ min-width: 0; margin: 0; border: 1px solid var(--border); border-radius: var(--radius); overflow: hidden; background: var(--surface); }}
    figcaption {{ display: flex; align-items: center; min-height: 48px; padding: 0 var(--space-4); border-bottom: 1px solid var(--border); color: var(--muted); font-family: var(--mono); font-size: 12px; letter-spacing: 0.08em; text-transform: uppercase; }}
    figure.after figcaption {{ color: var(--focus); background: var(--accent-soft); }}
    img {{ display: block; width: 100%; height: auto; background: var(--surface-2); }}
    @media (max-width: 48rem) {{ main {{ padding: var(--space-4); }} h1 {{ font-size: 28px; }} .comparison {{ grid-template-columns: 1fr; }} }}
  </style>
</head>
<body>
  <main>
    <p class=\"eyebrow\">Visual QA / before and after</p>
    <h1>{safe_title}</h1>
    <div class=\"tabs\" role=\"tablist\" aria-label=\"Comparison pages\"></div>
    <section class=\"comparison\" aria-live=\"polite\"></section>
  </main>
  <script>
    const pairs = {payload};
    const tabs = document.querySelector('.tabs');
    const comparison = document.querySelector('.comparison');
    function imagePanel(label, source, after) {{
      const figure = document.createElement('figure');
      if (after) figure.className = 'after';
      const caption = document.createElement('figcaption');
      caption.textContent = label;
      const image = document.createElement('img');
      image.src = source;
      image.alt = label;
      image.loading = 'eager';
      figure.append(caption, image);
      return figure;
    }}
    function select(index) {{
      const pair = pairs[index];
      comparison.replaceChildren(imagePanel('Before', pair.before, false), imagePanel('After', pair.after, true));
      [...tabs.children].forEach((tab, tabIndex) => tab.setAttribute('aria-selected', String(tabIndex === index)));
    }}
    pairs.forEach((pair, index) => {{
      const tab = document.createElement('button');
      tab.className = 'tab';
      tab.type = 'button';
      tab.role = 'tab';
      tab.textContent = pair.label;
      tab.addEventListener('click', () => select(index));
      tabs.append(tab);
    }});
    select(0);
  </script>
</body>
</html>
"""


def main() -> None:
    args = parse_args()
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    title, pairs = load_pairs(args, output.parent)
    output.write_text(build_html(title, pairs), encoding="utf-8")
    print(f"Created {output}")


if __name__ == "__main__":
    main()
