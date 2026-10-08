import argparse
import base64
import datetime as dt
import html
import json
import re
import zipfile
from pathlib import Path

try:
    from PIL import Image
except ImportError as exc:
    raise SystemExit("Pillow is required. Install with: python -m pip install pillow") from exc


def safe_name(name: str, limit: int = 120) -> str:
    name = re.sub(r'[\\/:*?"<>|]', "_", name or "untitled")
    name = re.sub(r"\s+", " ", name).strip()
    return name[:limit].strip() or "untitled"


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def article_sort_key(path: Path) -> int:
    match = re.match(r"^(\d+)-", path.name)
    return int(match.group(1)) if match else 999999


def zip_dir(src: Path, zip_path: Path, exclude_names: set[str] | None = None) -> None:
    exclude_names = exclude_names or set()
    if zip_path.exists():
        zip_path.unlink()
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for file in src.rglob("*"):
            if file.is_file() and file.name not in exclude_names:
                zf.write(file, file.relative_to(src.parent))


def zip_single_file(src: Path, zip_path: Path) -> None:
    if zip_path.exists():
        zip_path.unlink()
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.write(src, src.name)


def detect_crop_mode(mode: str, articles: list[dict]) -> str:
    if mode != "auto":
        return mode
    urls = "\n".join(str(a.get("url", "")) for a in articles).lower()
    if "feishu.cn/wiki" in urls or "larksuite.com/wiki" in urls:
        return "feishu"
    return "none"


def image_data_uri(root: Path, rel_path: str) -> str:
    path = root / rel_path
    if not path.exists():
        return rel_path
    suffix = path.suffix.lower()
    mime = "image/png" if suffix == ".png" else "image/jpeg" if suffix in {".jpg", ".jpeg"} else "application/octet-stream"
    return f"data:{mime};base64,{base64.b64encode(path.read_bytes()).decode('ascii')}"


def crop_box_for(mode: str, width: int, height: int, data: dict | None = None) -> tuple[int, int, int, int]:
    if mode == "feishu" and width >= 1200 and height >= 500:
        visual_crop = (data or {}).get("visualCrop") or {}
        left = int(visual_crop.get("left") or 400)
        top = 64
        right = int(visual_crop.get("right") or (width - 10))
        left = max(0, min(left, width - 320))
        right = max(left + 320, min(right, width))
        return left, top, right, height
    return 0, 0, width, height


def stitch_page(root: Path, out_dir: Path, index: int, title: str, shots: list[str], data: dict, crop_mode: str) -> str:
    if not shots:
        return ""
    images = []
    for rel in shots:
        path = root / rel
        if path.exists():
            images.append(Image.open(path).convert("RGB"))
    if not images:
        return ""

    first = images[0]
    width, height = first.size
    left, top, right, bottom = crop_box_for(crop_mode, width, height, data)
    crop_w = right - left
    crop_h = bottom - top

    scroll = data.get("scroll") or {}
    max_top = int(scroll.get("maxTop") or max(0, crop_h * (len(images) - 1)))
    step = max(580, int(crop_h * 0.78))
    positions = []
    y = 0
    while y <= max_top:
        positions.append(y)
        y += step
    if not positions or positions[-1] != max_top:
        positions.append(max_top)
    if len(positions) != len(images):
        positions = [0] if len(images) == 1 else [round(max_top * i / (len(images) - 1)) for i in range(len(images))]

    canvas_h = max(pos + crop_h for pos in positions)
    canvas = Image.new("RGB", (crop_w, canvas_h), "white")
    for img, pos in zip(images, positions):
        if img.size != (width, height):
            img = img.resize((width, height))
        canvas.paste(img.crop((left, top, right, bottom)), (0, int(pos)))

    out_name = f"{index:03d}-{safe_name(title, 80)}.png"
    out_path = out_dir / out_name
    out_dir.mkdir(parents=True, exist_ok=True)
    canvas.save(out_path, optimize=True)
    return out_path.relative_to(root).as_posix()


def collect_articles(root: Path, crop_mode_arg: str) -> tuple[list[dict], str]:
    pages = root / "pages"
    shots_root = root / "screenshots"
    stitched = root / "stitched-hq"
    raw = []

    for json_file in sorted(pages.glob("*.json"), key=article_sort_key):
        data = read_json(json_file)
        index = int(data.get("index") or article_sort_key(json_file))
        title = re.sub(r"\s*-\s*飞书云文档\s*$", "", data.get("title") or json_file.stem).strip()
        text = str(data.get("text") or "").replace("\r\n", "\n").replace("\r", "\n")
        folder = shots_root / f"{index:03d}"
        shots = [
            p.relative_to(root).as_posix()
            for p in sorted(folder.glob(f"{index:03d}-*.jpg"))
            if re.fullmatch(rf"{index:03d}-\d+\.jpg", p.name, flags=re.IGNORECASE)
        ] if folder.exists() else []
        raw.append(
            {
                "index": index,
                "title": title,
                "url": data.get("url", ""),
                "lineCount": int(data.get("lineCount") or len([line for line in text.splitlines() if line.strip()])),
                "textLength": int(data.get("textLength") or len(text)),
                "imageCount": int(data.get("imageCount") or 0),
                "screenshotCount": len(shots),
                "text": text,
                "shots": shots,
                "_data": data,
            }
        )

    crop_mode = detect_crop_mode(crop_mode_arg, raw)
    articles = []
    for item in raw:
        stitched_rel = stitch_page(root, stitched, item["index"], item["title"], item["shots"], item["_data"], crop_mode)
        item = dict(item)
        item.pop("_data", None)
        item["stitched"] = stitched_rel
        articles.append(item)
    return articles, crop_mode


def build_markdown(root: Path, title: str, articles: list[dict]) -> None:
    clean_dir = root / "readable" / "clean-markdown"
    clean_dir.mkdir(parents=True, exist_ok=True)
    all_md = [f"# {title}", "", f"- 总篇数：{len(articles)}", ""]
    for article in articles:
        md_name = f"{article['index']:03d}-{safe_name(article['title'])}.md"
        md = "\n".join(
            [
                f"# {article['title']}",
                "",
                f"- 来源：{article['url']}",
                f"- 序号：{article['index']:03d}",
                f"- 文本行数：{article['lineCount']}",
                f"- 文本字符数：{article['textLength']}",
                f"- 原页面图片节点数：{article['imageCount']}",
                f"- 本地截图数：{article['screenshotCount']}",
                "",
                "## 正文",
                "",
                article["text"],
                "",
            ]
        )
        write_text(clean_dir / md_name, md)
        write_text(root / "pages" / md_name, md)
        all_md.extend(
            [
                f"## {article['index']:03d}. {article['title']}",
                "",
                f"- 来源：{article['url']}",
                f"- 本地截图数：{article['screenshotCount']}",
                "",
                article["text"],
                "",
                "---",
                "",
            ]
        )
    write_text(root / "readable" / f"{safe_name(title)}合集.md", "\n".join(all_md))


def build_shareable_articles(root: Path, articles: list[dict]) -> list[dict]:
    embedded = []
    for article in articles:
        item = dict(article)
        if item.get("stitched"):
            item["stitched"] = image_data_uri(root, item["stitched"])
        item["shots"] = [image_data_uri(root, src) for src in item.get("shots", [])]
        embedded.append(item)
    return embedded


def build_html(data_json: str, title: str, count: int, shareable: bool) -> str:
    page_title = f"{title}可分享单文件" if shareable else f"{title}本地阅读器"
    brand_note = f"单文件可分享版 · 共 {count} 篇 · 图片已内嵌" if shareable else f"本地归档阅读器 · 共 {count} 篇 · Markdown + 截图"
    original_note = "这是已内嵌到 HTML 的原貌长图，对方不需要本地图片目录也能查看。" if shareable else "这是由分屏截图拼接的正文长图，用来保留原网页视觉位置。"
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(page_title)}</title>
  <style>
    :root {{
      --bg-a: hsl(42, 36%, 91%);
      --bg-b: hsl(34, 34%, 88%);
      --bg-c: hsl(76, 18%, 88%);
      --surface: hsl(42, 34%, 97%);
      --surface-soft: hsl(38, 30%, 95%);
      --ink: hsl(28, 20%, 16%);
      --ink-2: hsl(30, 12%, 38%);
      --muted: hsl(32, 10%, 52%);
      --accent: hsl(26, 58%, 44%);
      --accent-light: hsl(35, 58%, 91%);
      --border: hsla(30, 20%, 28%, 0.16);
      --border-strong: hsla(30, 20%, 28%, 0.28);
      --shadow-sm: 0 1px 2px hsla(28, 20%, 16%, 0.06);
      --shadow-md: 0 14px 36px hsla(28, 20%, 16%, 0.12);
      --radius-sm: 6px;
      --radius-md: 8px;
      --radius-lg: 12px;
      --space-1: 4px;
      --space-2: 8px;
      --space-3: 12px;
      --space-4: 16px;
      --space-6: 24px;
      --space-8: 32px;
      --text-xs: 0.75rem;
      --text-sm: 0.875rem;
      --text-base: 1rem;
      --text-lg: 1.125rem;
      --text-xl: 1.25rem;
      --text-2xl: 1.5rem;
      --text-3xl: 1.875rem;
      --leading-tight: 1.25;
      --leading-normal: 1.5;
      --leading-relaxed: 1.78;
      --max-w-content: 860px;
      --max-w-original: 1680px;
      --gradient-page: radial-gradient(circle at 12% 8%, hsla(36, 48%, 60%, 0.20), transparent 28%), linear-gradient(135deg, var(--bg-a), var(--bg-b), var(--bg-c));
      --gradient-hero: linear-gradient(135deg, hsl(22, 42%, 38%), hsl(35, 46%, 45%), hsl(78, 25%, 38%));
    }}
    * {{ box-sizing: border-box; }}
    body {{ margin: 0; background: var(--gradient-page); color: var(--ink); font-family: "Microsoft YaHei", "PingFang SC", "Noto Sans SC", system-ui, sans-serif; font-size: var(--text-base); line-height: var(--leading-normal); }}
    .app {{ min-height: 100vh; display: grid; grid-template-columns: 340px minmax(0, 1fr); }}
    .sidebar {{ position: sticky; top: 0; height: 100vh; display: flex; flex-direction: column; background: var(--surface); border-right: 1px solid var(--border); box-shadow: var(--shadow-md); z-index: 2; }}
    .brand {{ padding: var(--space-6); background: var(--gradient-hero); color: var(--surface); }}
    .brand h1 {{ margin: 0 0 var(--space-3); font-size: var(--text-2xl); line-height: var(--leading-tight); letter-spacing: 0; }}
    .brand p {{ margin: 0; color: var(--surface); font-size: var(--text-sm); }}
    .tools {{ padding: var(--space-4); border-bottom: 1px solid var(--border); background: var(--surface-soft); }}
    .search {{ width: 100%; border: 1px solid var(--border); border-radius: var(--radius-md); padding: var(--space-3) var(--space-4); background: var(--surface); color: var(--ink); outline: none; font-size: var(--text-sm); }}
    .search:focus {{ border-color: var(--accent); box-shadow: 0 0 0 3px var(--accent-light); }}
    .nav {{ overflow: auto; padding: var(--space-3); }}
    .nav button {{ width: 100%; border: 0; border-radius: var(--radius-md); padding: var(--space-3); margin: 0 0 var(--space-2); background: transparent; color: var(--ink-2); text-align: left; cursor: pointer; font-size: var(--text-sm); line-height: var(--leading-normal); }}
    .nav button:hover {{ background: var(--surface-soft); color: var(--ink); }}
    .nav button.active {{ background: var(--accent-light); color: var(--accent); font-weight: 700; }}
    .main {{ min-width: 0; padding: var(--space-8); }}
    .hero {{ max-width: var(--max-w-content); margin: 0 auto var(--space-8); padding: var(--space-8); border-radius: var(--radius-lg); background: var(--surface); border: 1px solid var(--border); box-shadow: var(--shadow-md); }}
    .hero .eyebrow {{ margin: 0 0 var(--space-2); color: var(--accent); font-weight: 700; font-size: var(--text-sm); }}
    .hero h2 {{ margin: 0; font-size: var(--text-3xl); line-height: var(--leading-tight); letter-spacing: 0; }}
    .meta {{ display: flex; flex-wrap: wrap; gap: var(--space-2); margin-top: var(--space-4); }}
    .pill {{ display: inline-flex; align-items: center; border-radius: var(--radius-sm); border: 1px solid var(--border); background: var(--surface-soft); color: var(--ink-2); padding: var(--space-1) var(--space-3); font-size: var(--text-xs); }}
    .mode-tabs {{ max-width: var(--max-w-content); margin: 0 auto var(--space-4); display: flex; gap: var(--space-2); padding: var(--space-2); border: 1px solid var(--border); border-radius: var(--radius-lg); background: var(--surface); box-shadow: var(--shadow-sm); }}
    .mode-tabs button {{ flex: 1; border: 0; border-radius: var(--radius-md); padding: var(--space-3) var(--space-4); background: transparent; color: var(--ink-2); cursor: pointer; font-weight: 700; font-size: var(--text-sm); }}
    .mode-tabs button.active {{ background: var(--accent-light); color: var(--accent); }}
    .content {{ max-width: var(--max-w-original); margin: 0 auto; background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius-lg); box-shadow: var(--shadow-sm); overflow: hidden; }}
    .view-panel[hidden] {{ display: none; }}
    .original {{ padding: var(--space-6); background: var(--surface-soft); overflow-x: auto; }}
    .original-note {{ margin: 0 0 var(--space-4); color: var(--ink-2); font-size: var(--text-sm); }}
    .zoom-toolbar {{ display: flex; flex-wrap: wrap; gap: var(--space-2); align-items: center; margin: 0 0 var(--space-4); color: var(--ink-2); font-size: var(--text-sm); }}
    .zoom-toolbar button {{ border: 1px solid var(--border); border-radius: var(--radius-sm); background: var(--surface); color: var(--ink-2); padding: var(--space-2) var(--space-3); cursor: pointer; font-weight: 700; }}
    .zoom-toolbar button.active {{ background: var(--accent-light); color: var(--accent); border-color: var(--accent); }}
    .stitched-image {{ width: auto; max-width: none; min-width: 1280px; display: block; border-radius: var(--radius-md); border: 1px solid var(--border-strong); background: var(--surface); box-shadow: var(--shadow-sm); }}
    .article {{ padding: var(--space-8); }}
    .article-text {{ white-space: pre-wrap; color: var(--ink); font-size: var(--text-lg); line-height: var(--leading-relaxed); }}
    .source-link {{ display: inline-block; margin-top: var(--space-6); color: var(--accent); text-decoration: none; font-weight: 700; }}
    .shots {{ border-top: 1px solid var(--border); background: var(--surface-soft); padding: var(--space-6); }}
    .shots h3 {{ margin: 0 0 var(--space-4); font-size: var(--text-xl); }}
    .shot-list {{ display: grid; gap: var(--space-4); }}
    .shot-list img {{ width: 100%; max-width: 100%; border-radius: var(--radius-md); border: 1px solid var(--border-strong); box-shadow: var(--shadow-sm); background: var(--surface); }}
    .empty {{ color: var(--muted); padding: var(--space-6); text-align: center; }}
    @media (max-width: 1024px) {{ .app {{ grid-template-columns: 280px minmax(0, 1fr); }} .main {{ padding: var(--space-6); }} .hero, .article {{ padding: var(--space-6); }} }}
    @media (max-width: 768px) {{ .app {{ display: block; }} .sidebar {{ position: relative; height: auto; }} .nav {{ max-height: 45vh; }} .main {{ padding: var(--space-4); }} .article-text {{ font-size: var(--text-base); }} }}
  </style>
</head>
<body>
  <div class="app">
    <aside class="sidebar">
      <section class="brand"><h1>{html.escape(title)}</h1><p>{html.escape(brand_note)}</p></section>
      <section class="tools"><input id="search" class="search" type="search" placeholder="搜索标题或正文"></section>
      <nav id="nav" class="nav"></nav>
    </aside>
    <main class="main">
      <section class="hero"><p class="eyebrow" id="eyebrow"></p><h2 id="title"></h2><div id="meta" class="meta"></div></section>
      <section class="mode-tabs" aria-label="阅读模式"><button id="originalMode" class="active" type="button">原貌长图</button><button id="textMode" type="button">可复制正文</button></section>
      <section class="content">
        <section id="originalPanel" class="view-panel original">
          <p class="original-note">{html.escape(original_note)}</p>
          <div class="zoom-toolbar" aria-label="长图缩放"><span>长图缩放</span><button type="button" data-zoom="1">100%</button><button type="button" data-zoom="1.25" class="active">125%</button><button type="button" data-zoom="1.5">150%</button></div>
          <div id="stitched"></div>
        </section>
        <article id="textPanel" class="view-panel article" hidden><div id="articleText" class="article-text"></div><a id="source" class="source-link" target="_blank" rel="noreferrer">打开原网页</a></article>
        <section id="shotsPanel" class="view-panel shots"><h3>分屏截图备份</h3><div id="shots" class="shot-list"></div></section>
      </section>
    </main>
  </div>
  <script id="data" type="application/json">{data_json}</script>
  <script>
    const articles = JSON.parse(document.getElementById('data').textContent);
    const nav = document.getElementById('nav');
    const search = document.getElementById('search');
    const originalMode = document.getElementById('originalMode');
    const textMode = document.getElementById('textMode');
    const originalPanel = document.getElementById('originalPanel');
    const textPanel = document.getElementById('textPanel');
    const shotsPanel = document.getElementById('shotsPanel');
    let active = 0;
    let mode = 'original';
    let imageZoom = 1.25;
    function escapeText(value) {{ return String(value || '').replace(/[&<>"']/g, (ch) => ({{'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'}}[ch])); }}
    function filteredArticles() {{ const q = search.value.trim().toLowerCase(); return q ? articles.filter(a => (a.title + '\\n' + a.text).toLowerCase().includes(q)) : articles; }}
    function renderNav() {{ const current = articles[active] || articles[0]; nav.innerHTML = filteredArticles().map(a => `<button type="button" data-index="${{a.index}}" class="${{a.index === current.index ? 'active' : ''}}">${{String(a.index).padStart(3, '0')}} · ${{escapeText(a.title)}}</button>`).join(''); }}
    function renderArticle(index) {{
      const found = articles.findIndex(a => a.index === index);
      active = found >= 0 ? found : 0;
      const a = articles[active];
      document.getElementById('eyebrow').textContent = `第 ${{String(a.index).padStart(3, '0')}} 篇`;
      document.getElementById('title').textContent = a.title;
      document.getElementById('meta').innerHTML = `<span class="pill">文本 ${{a.textLength}} 字符</span><span class="pill">行数 ${{a.lineCount}}</span><span class="pill">原图节点 ${{a.imageCount}}</span><span class="pill">原貌长图 ${{a.stitched ? '1 张' : '无'}}</span><span class="pill">截图 ${{a.screenshotCount}} 张</span>`;
      document.getElementById('articleText').textContent = a.text;
      document.getElementById('source').href = a.url;
      const stitched = document.getElementById('stitched');
      if (a.stitched) {{ stitched.innerHTML = `<img class="stitched-image" loading="eager" src="${{escapeText(a.stitched)}}" alt="${{escapeText(a.title)}} 原貌长图">`; stitched.querySelector('img').addEventListener('load', () => applyImageZoom()); }} else {{ stitched.innerHTML = '<div class="empty">这一篇没有原貌长图。</div>'; }}
      document.getElementById('shots').innerHTML = a.shots.length ? a.shots.map((src, i) => `<img loading="lazy" src="${{escapeText(src)}}" alt="${{escapeText(a.title)}} 截图 ${{i + 1}}">`).join('') : '<div class="empty">这一篇没有截图文件。</div>';
      renderNav();
      applyMode(mode);
      window.scrollTo({{ top: 0, behavior: 'instant' }});
    }}
    function applyMode(nextMode) {{ mode = nextMode; const original = mode === 'original'; originalPanel.hidden = !original; shotsPanel.hidden = !original; textPanel.hidden = original; originalMode.classList.toggle('active', original); textMode.classList.toggle('active', !original); }}
    function applyImageZoom() {{ const img = document.querySelector('.stitched-image'); if (!img) return; img.style.width = `${{Math.round((img.naturalWidth || 1280) * imageZoom)}}px`; document.querySelectorAll('[data-zoom]').forEach(btn => btn.classList.toggle('active', Number(btn.dataset.zoom) === imageZoom)); }}
    nav.addEventListener('click', event => {{ const button = event.target.closest('button[data-index]'); if (button) renderArticle(Number(button.dataset.index)); }});
    originalMode.addEventListener('click', () => applyMode('original'));
    textMode.addEventListener('click', () => applyMode('text'));
    document.querySelectorAll('[data-zoom]').forEach(btn => btn.addEventListener('click', () => {{ imageZoom = Number(btn.dataset.zoom); applyImageZoom(); }}));
    search.addEventListener('input', renderNav);
    renderArticle(articles[0].index);
  </script>
</body>
</html>"""


def write_docs(root: Path, title: str, articles: list[dict], crop_mode: str, shareable_html: Path | None, shareable_zip: Path | None, archive_zip: Path | None) -> None:
    screenshot_count = sum(a["screenshotCount"] for a in articles)
    stitched_count = len([a for a in articles if a.get("stitched")])
    readme = [
        f"# {title}归档索引",
        "",
        "## 推荐入口",
        "",
        "- 本地阅读：`reader.html`",
    ]
    if shareable_html:
        readme.append(f"- 对外分享：`{shareable_html.name}`")
    if shareable_zip:
        readme.append(f"- 分享压缩包：`{shareable_zip}`")
    readme.extend(["", "## 页面清单", ""])
    for article in articles:
        readme.append(f"- {article['index']:03d}. {article['title']} | 文本 {article['textLength']} 字符 | 截图 {article['screenshotCount']} 张 | {article['url']}")
    write_text(root / "README.md", "\n".join(readme))

    usage = f"""# {title}归档使用说明

## 直接阅读

打开根目录下的 `reader.html`。

## 分享给别人

如果存在 `{safe_name(title)}-可分享单文件.html`，优先分享这个文件。它已经把图片嵌入 HTML，对方不需要本地图片目录。

## JSON 怎么用

JSON 是结构化源数据，适合重新生成 Markdown/HTML、导入数据库或知识库、搜索、摘要和分类。日常阅读不用打开 JSON。

## 文件数量

- 文章数：{len(articles)}
- 截图数：{screenshot_count}
- 原貌长图数：{stitched_count}
"""
    write_text(root / "README_使用说明.md", usage)

    verification = f"""# {title}归档验证

- 验证时间：{dt.datetime.now().astimezone().isoformat()}
- 输出目录：{root}
- 文章数量：{len(articles)}
- Markdown 文件数：{len(list((root / 'pages').glob('*.md')))}
- JSON 文件数：{len(list((root / 'pages').glob('*.json')))}
- 截图文件数：{screenshot_count}
- 原貌长图文件数：{stitched_count}
- 裁切模式：{crop_mode}
- 本地阅读器：{root / 'reader.html'}
- 可分享 HTML：{shareable_html or ''}
- 可分享 ZIP：{shareable_zip or ''}
- 完整归档 ZIP：{archive_zip or ''}

## 结论

- JSON 保留为结构化源数据。
- Markdown 和 HTML 是从 JSON/截图生成的阅读层。
- 原貌长图以 PNG 输出，避免二次 JPG 压缩。
- 可分享单文件 HTML 使用 data URI 内嵌图片，不依赖本地图片目录。
"""
    write_text(root / "VERIFICATION.md", verification)


def main() -> None:
    parser = argparse.ArgumentParser(description="Build readable/shareable HTML archive from WebBridge crawl output.")
    parser.add_argument("root", help="Archive root containing pages/*.json and optional screenshots/")
    parser.add_argument("--title", default="", help="Archive title")
    parser.add_argument("--title-file", default="", help="UTF-8 text file containing the archive title. Prefer this on Windows for Chinese titles.")
    parser.add_argument("--crop-mode", choices=["auto", "none", "feishu"], default="auto")
    parser.add_argument("--shareable", action="store_true", help="Build single-file HTML with embedded images")
    parser.add_argument("--zip", action="store_true", help="Build zip packages")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    if not (root / "pages").exists():
        raise SystemExit(f"Missing pages directory: {root / 'pages'}")

    title = args.title.strip()
    if args.title_file:
        title = Path(args.title_file).read_text(encoding="utf-8").strip()
    title = title or root.name
    articles, crop_mode = collect_articles(root, args.crop_mode)
    if not articles:
        raise SystemExit(f"No page JSON files found under {root / 'pages'}")

    build_markdown(root, title, articles)
    data_json = json.dumps(articles, ensure_ascii=False).replace("</", "<\\/")
    write_text(root / "reader.html", build_html(data_json, title, len(articles), shareable=False))

    shareable_html = None
    shareable_zip = None
    if args.shareable:
        embedded_json = json.dumps(build_shareable_articles(root, articles), ensure_ascii=False).replace("</", "<\\/")
        shareable_html = root / f"{safe_name(title)}-可分享单文件.html"
        write_text(shareable_html, build_html(embedded_json, title, len(articles), shareable=True))
        if args.zip:
            shareable_zip = root.parent / f"{safe_name(root.name)}-shareable-html.zip"
            zip_single_file(shareable_html, shareable_zip)

    archive_zip = None
    if args.zip:
        archive_zip = root.parent / f"{safe_name(root.name)}-readable.zip"
        exclude = {shareable_html.name} if shareable_html else set()
        zip_dir(root, archive_zip, exclude_names=exclude)

    write_docs(root, title, articles, crop_mode, shareable_html, shareable_zip, archive_zip)
    print(
        json.dumps(
            {
                "root": str(root),
                "title": title,
                "articles": len(articles),
                "screenshots": sum(a["screenshotCount"] for a in articles),
                "stitched": len([a for a in articles if a.get("stitched")]),
                "reader": str(root / "reader.html"),
                "shareable_html": str(shareable_html) if shareable_html else "",
                "shareable_zip": str(shareable_zip) if shareable_zip else "",
                "archive_zip": str(archive_zip) if archive_zip else "",
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
