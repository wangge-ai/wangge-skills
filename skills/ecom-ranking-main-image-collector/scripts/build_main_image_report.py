#!/usr/bin/env python3
"""Build a standalone HTML report from ecommerce main-image sample manifests."""

from __future__ import annotations

import argparse
import csv
import html
import json
import re
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from urllib.parse import quote


TEXT_FIELDS = (
    "title",
    "product_name",
    "name",
    "terms",
    "age_terms",
    "ip_terms",
    "trust_terms",
    "promo_terms",
    "sample_note",
    "note",
)
IMAGE_FIELDS = ("image_rel", "normalized_path", "local_path", "image_path")
STOP_WORDS = {
    "jd",
    "tmall",
    "taobao",
    "http",
    "https",
    "com",
    "item",
    "html",
    "png",
    "jpg",
    "jpeg",
    "webp",
}


def esc(value: object) -> str:
    return html.escape("" if value is None else str(value), quote=True)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def first_value(row: dict[str, str], fields: tuple[str, ...]) -> str:
    for field in fields:
        value = (row.get(field) or "").strip()
        if value:
            return value
    return ""


def to_number(value: str) -> float | None:
    value = (value or "").replace(",", "").strip()
    if not value:
        return None
    match = re.search(r"-?\d+(?:\.\d+)?", value)
    if not match:
        return None
    try:
        return float(match.group(0))
    except ValueError:
        return None


def rank_key(row: dict[str, str]) -> tuple[str, int, int]:
    platform = (row.get("platform") or "").strip()
    rank = to_number(row.get("rank", "")) or 999999
    return platform, int(rank), 0


def split_terms(value: str) -> list[str]:
    if not value:
        return []
    tokens = re.split(r"[\s,;|/，、；]+", value)
    cleaned = []
    for token in tokens:
        token = token.strip().strip("[]()（）\"'")
        if not token or token.lower() in STOP_WORDS:
            continue
        if len(token) == 1 and token.isascii():
            continue
        cleaned.append(token)
    return cleaned


def collect_terms(rows: list[dict[str, str]], limit: int = 18) -> list[tuple[str, int]]:
    counter: Counter[str] = Counter()
    for row in rows:
        for field in TEXT_FIELDS:
            if field.endswith("_terms") or field == "terms":
                counter.update(split_terms(row.get(field, "")))
    return counter.most_common(limit)


def platform_counts(rows: list[dict[str, str]]) -> dict[str, int]:
    counts: defaultdict[str, int] = defaultdict(int)
    for row in rows:
        counts[(row.get("platform") or "unknown").strip() or "unknown"] += 1
    return dict(counts)


def resolve_asset(path_text: str, asset_root: Path, out_path: Path) -> str:
    if not path_text:
        return ""
    raw = Path(path_text)
    if raw.is_absolute():
        candidate = raw
    else:
        candidate = asset_root / raw
    try:
        rel = candidate.resolve().relative_to(out_path.parent.resolve())
        return quote(rel.as_posix(), safe="/.:_-")
    except Exception:
        return candidate.resolve().as_uri()


def row_image(row: dict[str, str], asset_root: Path, out_path: Path) -> str:
    image = first_value(row, IMAGE_FIELDS)
    return resolve_asset(image, asset_root, out_path)


def stat_price(rows: list[dict[str, str]]) -> str:
    values = []
    for row in rows:
        value = to_number(row.get("price_num", "") or row.get("price", ""))
        if value is not None:
            values.append(value)
    if not values:
        return "未采集"
    values.sort()
    median = values[len(values) // 2]
    return f"¥{median:.1f}"


def top_rows_by_platform(rows: list[dict[str, str]], per_platform: int = 20) -> list[dict[str, str]]:
    groups: defaultdict[str, list[dict[str, str]]] = defaultdict(list)
    for row in sorted(rows, key=rank_key):
        groups[(row.get("platform") or "unknown").strip() or "unknown"].append(row)
    selected: list[dict[str, str]] = []
    for platform in sorted(groups):
        selected.extend(groups[platform][:per_platform])
    return selected


def is_ad_row(row: dict[str, str]) -> bool:
    return (row.get("is_ad") or "").strip().lower() in {"yes", "true", "1", "ad", "广告"}


def build_card(row: dict[str, str], asset_root: Path, out_path: Path) -> str:
    image = row_image(row, asset_root, out_path)
    platform = row.get("platform") or "unknown"
    rank = row.get("rank") or "-"
    title = first_value(row, ("title", "product_name", "name")) or "未命名商品"
    price = row.get("price") or row.get("price_num") or ""
    volume = row.get("volume") or row.get("volume_num") or ""
    terms = []
    for field in ("age_terms", "ip_terms", "trust_terms", "promo_terms", "terms"):
        terms.extend(split_terms(row.get(field, "")))
    chips = "".join(f"<span>{esc(term)}</span>" for term in list(dict.fromkeys(terms))[:5])
    sample_type = "广告位" if is_ad_row(row) else "自然位"
    sample_class = "sample-type ad" if is_ad_row(row) else "sample-type organic"
    return f"""
      <article class="sample-card">
        <div class="sample-img">{f'<img src="{image}" alt="{esc(title)}">' if image else '<div class="img-missing">no image</div>'}</div>
        <div class="sample-body">
          <div class="rank-line"><b>{esc(platform)} · 位置 {esc(rank)}</b><span class="{sample_class}">{sample_type}</span></div>
          <h3>{esc(title)}</h3>
          <p>{esc(price)}{(' · ' + esc(volume)) if volume else ''}</p>
          <div class="chips">{chips}</div>
        </div>
      </article>
    """


def build_table(rows: list[dict[str, str]]) -> str:
    body = []
    for row in rows:
        body.append(
            "<tr>"
            f"<td>{esc(row.get('platform') or '')}</td>"
            f"<td>{esc(row.get('rank') or '')}</td>"
            f"<td>{'广告位' if is_ad_row(row) else '自然位'}</td>"
            f"<td>{esc(first_value(row, ('title', 'product_name', 'name')))}</td>"
            f"<td>{esc(row.get('price') or row.get('price_num') or '')}</td>"
            f"<td>{esc(row.get('volume') or row.get('volume_num') or '')}</td>"
            f"<td>{esc(row.get('sort_selected') or '')}</td>"
            "</tr>"
        )
    return "\n".join(body)


def build_html(args: argparse.Namespace, rows: list[dict[str, str]]) -> str:
    out_path = Path(args.out)
    asset_root = Path(args.asset_root).resolve() if args.asset_root else Path(args.manifest).resolve().parent
    category = args.category or infer_category(args, rows)
    selected = top_rows_by_platform(rows, args.per_platform)
    counts = platform_counts(rows)
    ad_count = sum(1 for row in selected if is_ad_row(row))
    organic_count = len(selected) - ad_count
    identified_count = sum(
        1
        for row in selected
        if (row.get("item_id") or row.get("item_url"))
        and first_value(row, IMAGE_FIELDS + ("image_url",))
    )
    identity_coverage = round(identified_count * 100 / len(selected)) if selected else 0
    sort_values = sorted({(row.get("sort_selected") or "").strip() for row in selected if (row.get("sort_selected") or "").strip()})
    sort_label = "、".join(sort_values) or "未标注"
    sort_context = sort_label if sort_label == "未标注" or sort_label.endswith("排序") else f"{sort_label}排序"
    price_label_counts = Counter((row.get("price_label") or "未标注").strip() or "未标注" for row in selected)
    price_label_summary = "、".join(f"{label} {count}" for label, count in price_label_counts.most_common())
    terms = collect_terms(selected)
    cards = "\n".join(build_card(row, asset_root, out_path) for row in selected[: args.max_cards])
    table = build_table(selected[: args.max_table_rows])
    term_tags = "".join(f"<span><b>{esc(term)}</b>{count}</span>" for term, count in terms)
    counts_json = json.dumps(counts, ensure_ascii=False)
    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M")
    source_note = args.source_note or "公开搜索/榜单页面可见样本；遇到登录、验证或风控页面时应在 README 记录并切换路线。"
    readme_note = args.readme_note or "技术细节、踩坑和阻塞记录放 README，不放公众号正文。"
    contact = resolve_asset(args.contact_sheet, asset_root, out_path) if args.contact_sheet else ""
    contact_html = (
        f'<figure class="contact"><img src="{contact}" alt="样本总览"><figcaption>样本总览图</figcaption></figure>'
        if contact
        else ""
    )

    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(args.title)}</title>
  <style>
    :root {{
      --bg-a: hsl(42, 36%, 91%);
      --bg-b: hsl(34, 34%, 88%);
      --bg-c: hsl(76, 18%, 88%);
      --surface: hsl(42, 34%, 97%);
      --surface-soft: hsl(38, 30%, 95%);
      --surface-line: hsla(30, 24%, 28%, 0.14);
      --ink: hsl(28, 20%, 16%);
      --ink-2: hsl(30, 12%, 38%);
      --muted: hsl(32, 10%, 52%);
      --accent: hsl(26, 58%, 44%);
      --accent-2: hsl(36, 50%, 48%);
      --success: hsl(142, 38%, 36%);
      --warning: hsl(40, 72%, 45%);
      --info: hsl(198, 36%, 40%);
      --danger: hsl(8, 60%, 48%);
      --glow: hsla(36, 48%, 60%, 0.18);
      --hero-ink: hsl(42, 34%, 94%);
      --hero-muted: hsl(42, 28%, 82%);
      --hero-surface: hsla(42, 34%, 94%, 0.1);
      --hero-border: hsla(42, 34%, 94%, 0.18);
      --chip-bg: hsl(38, 28%, 92%);
      --warning-soft: hsl(40, 64%, 91%);
      --success-soft: hsl(142, 28%, 91%);
      --table-head: hsl(28, 20%, 18%);
      --table-head-ink: hsl(42, 34%, 94%);
      --row-alt: hsla(38, 32%, 94%, 0.62);
      --gradient-page: radial-gradient(circle at 12% 10%, var(--glow), transparent 30%), linear-gradient(135deg, var(--bg-a), var(--bg-b), var(--bg-c));
      --gradient-dark: radial-gradient(circle at 78% 16%, var(--glow), transparent 38%), linear-gradient(135deg, hsl(18, 42%, 38%), hsl(30, 45%, 45%), hsl(78, 25%, 38%));
      --gradient-card: linear-gradient(135deg, hsl(42, 34%, 98%), hsl(38, 30%, 94%));
      --gradient-number: linear-gradient(90deg, var(--accent), var(--accent-2));
      --shadow-sm: 0 8px 18px hsla(28, 24%, 18%, 0.08);
      --shadow-md: 0 20px 46px hsla(28, 24%, 18%, 0.14);
      --radius-sm: 6px;
      --radius-md: 8px;
      --radius-lg: 12px;
      --space-1: 4px;
      --space-2: 8px;
      --space-3: 12px;
      --space-4: 16px;
      --space-5: 20px;
      --space-6: 24px;
      --space-8: 32px;
      --space-10: 40px;
      --space-12: 48px;
      --space-16: 64px;
      --text-xs: 0.75rem;
      --text-sm: 0.875rem;
      --text-base: 1rem;
      --text-lg: 1.125rem;
      --text-xl: 1.25rem;
      --text-2xl: 1.5rem;
      --text-3xl: 1.875rem;
      --text-4xl: 2.25rem;
      --leading-tight: 1.25;
      --leading-normal: 1.5;
      --leading-relaxed: 1.75;
      --max-w-full: 1180px;
    }}
    * {{ box-sizing: border-box; }}
    html, body {{ max-width: 100%; }}
    body {{
      margin: 0;
      font-family: "Microsoft YaHei", "PingFang SC", Arial, sans-serif;
      color: var(--ink);
      background: var(--gradient-page);
      line-height: var(--leading-normal);
    }}
    main {{ width: 100%; max-width: var(--max-w-full); margin: 0 auto; padding: var(--space-8) var(--space-6) var(--space-16); }}
    .hero {{
      width: 100%;
      max-width: 100%;
      min-height: 300px;
      color: var(--hero-ink);
      background: var(--gradient-dark);
      border-radius: var(--radius-lg);
      padding: var(--space-10);
      box-shadow: var(--shadow-md);
      display: grid;
      grid-template-columns: 1.15fr 0.85fr;
      gap: var(--space-8);
      align-items: end;
    }}
    .hero > *, .metrics, .metric, .grid > *, .samples > *, .sample-body {{ min-width: 0; }}
    .eyebrow {{ font-size: var(--text-sm); color: var(--hero-muted); margin: 0 0 var(--space-3); letter-spacing: 0; }}
    h1 {{ margin: 0; max-width: 760px; font-size: clamp(2.25rem, 5vw, 3.75rem); line-height: 1.08; letter-spacing: 0; overflow-wrap: anywhere; word-break: break-all; }}
    .hero p {{ color: var(--hero-muted); font-size: var(--text-lg); max-width: 680px; overflow-wrap: anywhere; word-break: break-all; }}
    .metrics {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: var(--space-3); }}
    .metric {{ background: var(--hero-surface); border: 1px solid var(--hero-border); border-radius: var(--radius-md); padding: var(--space-4); }}
    .metric b {{ display: block; font-size: var(--text-3xl); line-height: var(--leading-tight); }}
    .metric span {{ display: block; color: var(--hero-muted); font-size: var(--text-sm); margin-top: var(--space-2); }}
    section {{ margin-top: var(--space-12); }}
    h2 {{ font-size: var(--text-2xl); margin: 0 0 var(--space-4); }}
    .lead {{ max-width: 820px; color: var(--ink-2); font-size: var(--text-lg); }}
    .grid {{ display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: var(--space-4); }}
    .panel, .sample-card {{ background: var(--gradient-card); border: 1px solid var(--surface-line); border-radius: var(--radius-md); box-shadow: var(--shadow-sm); }}
    .panel {{ padding: var(--space-5); }}
    .panel b {{ display: block; font-size: var(--text-3xl); background: var(--gradient-number); color: transparent; -webkit-background-clip: text; background-clip: text; }}
    .panel span {{ color: var(--muted); }}
    .term-cloud {{ display: flex; flex-wrap: wrap; gap: var(--space-2); }}
    .term-cloud span, .chips span {{ display: inline-flex; gap: var(--space-1); align-items: center; border-radius: 999px; background: var(--chip-bg); color: var(--ink-2); padding: var(--space-2) var(--space-3); font-size: var(--text-sm); }}
    .term-cloud b {{ color: var(--accent); margin-right: var(--space-1); }}
    .samples {{ display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: var(--space-4); }}
    .sample-card {{ overflow: hidden; }}
    .sample-img {{ aspect-ratio: 1 / 1; background: var(--surface-soft); display: grid; place-items: center; }}
    .sample-img img {{ width: 100%; height: 100%; object-fit: contain; display: block; }}
    .img-missing {{ color: var(--muted); font-size: var(--text-sm); }}
    .sample-body {{ padding: var(--space-4); }}
    .rank-line {{ display: flex; justify-content: space-between; gap: var(--space-2); color: var(--muted); font-size: var(--text-sm); }}
    .rank-line b {{ color: var(--accent); }}
    .sample-type {{ display: inline-flex; align-items: center; border-radius: var(--radius-sm); padding: var(--space-1) var(--space-2); font-weight: 700; }}
    .sample-type.ad {{ color: var(--warning); background: var(--warning-soft); }}
    .sample-type.organic {{ color: var(--success); background: var(--success-soft); }}
    h3 {{ margin: var(--space-3) 0 var(--space-2); font-size: var(--text-base); line-height: var(--leading-normal); min-height: 3em; }}
    .sample-body p {{ color: var(--muted); margin: 0 0 var(--space-3); }}
    .chips {{ display: flex; flex-wrap: wrap; gap: var(--space-2); min-height: 32px; }}
    .contact {{ margin: var(--space-6) 0 0; }}
    .contact img {{ width: 100%; border-radius: var(--radius-md); border: 1px solid var(--surface-line); box-shadow: var(--shadow-sm); }}
    figcaption {{ color: var(--muted); font-size: var(--text-sm); margin-top: var(--space-2); }}
    .table-scroll {{ overflow-x: auto; border-radius: var(--radius-md); border: 1px solid var(--surface-line); background: var(--surface); box-shadow: var(--shadow-sm); }}
    table {{ width: 100%; border-collapse: collapse; min-width: 920px; }}
    th {{ background: var(--table-head); color: var(--table-head-ink); text-align: left; padding: var(--space-3); font-size: var(--text-sm); }}
    td {{ border-bottom: 1px solid var(--surface-line); padding: var(--space-3); color: var(--ink-2); vertical-align: top; }}
    tr:nth-child(even) td {{ background: var(--row-alt); }}
    .decision-list {{ display: grid; gap: var(--space-3); margin: 0; padding-left: var(--space-6); color: var(--ink-2); }}
    .boundary {{ border-left: 4px solid var(--warning); background: var(--warning-soft); padding: var(--space-4); color: var(--ink-2); }}
    .notes {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: var(--space-4); }}
    .notes p {{ margin: var(--space-2) 0 0; color: var(--ink-2); }}
    code {{ background: var(--chip-bg); padding: 0 var(--space-1); border-radius: var(--radius-sm); overflow-wrap: anywhere; }}
    @media (max-width: 920px) {{
      main {{ padding: var(--space-4); }}
      .hero {{ grid-template-columns: 1fr; padding: var(--space-8) var(--space-5); }}
      .grid, .samples, .notes {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
    }}
    @media (max-width: 560px) {{
      .grid, .samples, .metrics, .notes {{ grid-template-columns: 1fr; }}
      .hero {{ min-height: auto; padding: var(--space-6) var(--space-5); gap: var(--space-5); }}
      h1 {{ font-size: 2rem; line-height: 1.12; }}
      .lead {{ font-size: var(--text-base); }}
    }}
  </style>
</head>
<body>
  <main>
    <header class="hero">
      <div>
        <p class="eyebrow">10 秒事实层 · 榜单主图采集</p>
        <h1>{esc(args.title)}</h1>
        <p>先确认样本是否真实、完整、可用，再决定哪些图片进入后续主图诊断；页面位置不直接冒充官方榜单名次。</p>
      </div>
      <div class="metrics">
        <div class="metric"><b>{len(selected)}</b><span>有效商品主图</span></div>
        <div class="metric"><b>{organic_count}</b><span>自然位样本</span></div>
        <div class="metric"><b>{ad_count}</b><span>广告位样本</span></div>
        <div class="metric"><b>{identity_coverage}%</b><span>商品身份 + 图片覆盖</span></div>
      </div>
    </header>

    <section>
      <h2>10 秒事实层</h2>
      <p class="lead">当前样本来自 {esc(sort_context)}搜索页，清单已把商品、页面位置、主图、商品 ID、广告属性和价格标签对齐。先看覆盖与边界，再看图片。</p>
      <div class="grid">
        <div class="panel"><b>{esc(category)}</b><span>关键词 / 类目</span></div>
        <div class="panel"><b>{esc(", ".join(counts.keys()))}</b><span>平台</span></div>
        <div class="panel"><b>{esc(sort_label)}</b><span>页面排序</span></div>
        <div class="panel"><b>{esc(price_label_summary)}</b><span>页面价格标签分布</span></div>
      </div>
      <p class="boundary"><b>边界：</b>{esc(source_note)} 广告位与自然位分开计数；本页的“位置”仅表示这次采集时的页面顺序，不等同于官方榜单。</p>
      {contact_html}
    </section>

    <section>
      <h2>运营使用层</h2>
      <p class="lead">这一步只决定样本怎么用，不替代下一项主图诊断。</p>
      <ol class="decision-list">
        <li><b>自然位分母：</b>用 {organic_count} 个自然位样本观察常见构图、信息密度和品牌露出；不要把 {ad_count} 个广告位混入自然排名结论。</li>
        <li><b>广告参考：</b>广告位单独用于观察付费创意、促销标签和强转化表达，不用于证明自然搜索表现。</li>
        <li><b>稳定性验证：</b>若要判断“长期前排”，应在不同时间重复采集并比较位置变化；单次页面顺序不能外推为稳定榜单。</li>
        <li><b>下一步：</b>把规范化图片和清单交给主图诊断 Skill，逐张判断缩略图可读性、卖点层级和同质化风险。</li>
      </ol>
    </section>

    <section>
      <h2>已提供的结构化标签</h2>
      <div class="term-cloud">{term_tags or '<span>当前清单未提供视觉元素标签；保留给主图诊断阶段生成</span>'}</div>
    </section>

    <section>
      <h2>前排主图样本</h2>
      <div class="samples">{cards}</div>
    </section>

    <section>
      <h2>样本明细</h2>
      <div class="table-scroll">
        <table>
          <thead><tr><th>平台</th><th>位置</th><th>类型</th><th>标题</th><th>页面价格</th><th>销量/热度</th><th>排序</th></tr></thead>
          <tbody>{table}</tbody>
        </table>
      </div>
    </section>

    <section class="notes">
      <div class="panel">
        <h2>采集说明</h2>
        <p>{esc(source_note)}</p>
        <p>平台计数：<code>{esc(counts_json)}</code></p>
      </div>
      <div class="panel">
        <h2>交付说明</h2>
        <p>{esc(readme_note)}</p>
        <p>生成时间：{esc(generated_at)}</p>
      </div>
    </section>
  </main>
</body>
</html>
"""


def infer_category(args: argparse.Namespace, rows: list[dict[str, str]]) -> str:
    if args.category:
        return args.category
    for row in rows:
        for field in ("category", "keyword", "sub_category"):
            value = (row.get(field) or "").strip()
            if value:
                return value
    return "电商主图"


def main() -> None:
    parser = argparse.ArgumentParser(description="Build a standalone HTML report from a main-image manifest CSV.")
    parser.add_argument("--manifest", required=True, help="CSV manifest, such as sample_manifest.csv or top20_combined.csv.")
    parser.add_argument("--out", required=True, help="Output HTML path.")
    parser.add_argument("--title", default="爆款主图拆解报告", help="Report title.")
    parser.add_argument("--category", default="", help="Category or keyword shown in the report.")
    parser.add_argument("--asset-root", default="", help="Folder used to resolve relative image/contact-sheet paths.")
    parser.add_argument("--contact-sheet", default="", help="Optional contact sheet image path relative to asset root.")
    parser.add_argument("--source-note", default="", help="Sampling/source note shown in the report.")
    parser.add_argument("--readme-note", default="", help="README/pitfall note shown in the report.")
    parser.add_argument("--per-platform", type=int, default=20, help="Rows selected per platform.")
    parser.add_argument("--max-cards", type=int, default=40, help="Maximum image cards shown.")
    parser.add_argument("--max-table-rows", type=int, default=80, help="Maximum table rows shown.")
    args = parser.parse_args()

    manifest = Path(args.manifest)
    out_path = Path(args.out)
    rows = read_csv(manifest)
    if not rows:
        raise SystemExit(f"No rows found in {manifest}")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(build_html(args, rows), encoding="utf-8")
    print(f"rows: {len(rows)}")
    print(f"report: {out_path}")


if __name__ == "__main__":
    main()
