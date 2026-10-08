from __future__ import annotations

import argparse
import base64
import hashlib
import html
import json
import mimetypes
import os
import re
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import unquote, urlsplit


OLD_ROOT = Path("__unset_legacy_root__")
NEW_ROOT = Path("__unset_rich_root__")
OUT_ROOT = Path("__unset_output_root__")
WORK_ROOT = Path("__unset_work_root__")

ASSET_REF_RE = re.compile(r"\.\./assets/[^\"']+")
OLD_TEXT_RE = re.compile(
    r'<section class="panel text-view"[^>]*>\s*(.*?)\s*</section>\s*</main>',
    re.DOTALL,
)
NEW_MAIN_RE = re.compile(r'(<main class="document-shell">.*?</main>)', re.DOTALL)


@dataclass
class Entry:
    index: int
    title: str
    author: str
    source_url: str
    html_path: Path
    kind: str
    screenshot_path: Path | None = None
    source_index: int | None = None


class HashWriter:
    def __init__(self, path: Path):
        self.path = path
        self.file = path.open("wb")
        self.sha = hashlib.sha256()
        self.size = 0

    def write_bytes(self, data: bytes) -> None:
        self.file.write(data)
        self.sha.update(data)
        self.size += len(data)

    def write(self, text: str) -> None:
        self.write_bytes(text.encode("utf-8"))

    def close(self) -> None:
        self.file.close()

    @property
    def hexdigest(self) -> str:
        return self.sha.hexdigest()


def normal_url(value: str) -> str:
    parsed = urlsplit(value or "")
    return (parsed.netloc.lower() + parsed.path.rstrip("/").lower()).strip()


def mime_for(path: Path) -> str:
    overrides = {
        ".svg": "image/svg+xml",
        ".webp": "image/webp",
        ".avif": "image/avif",
        ".mp4": "video/mp4",
        ".mov": "video/quicktime",
        ".m4v": "video/x-m4v",
        ".pdf": "application/pdf",
        ".md": "text/markdown",
    }
    return overrides.get(path.suffix.lower()) or mimetypes.guess_type(path.name)[0] or "application/octet-stream"


def write_data_uri(writer: HashWriter, path: Path) -> None:
    if not path.is_file():
        raise FileNotFoundError(path)
    writer.write(f"data:{mime_for(path)};base64,")
    with path.open("rb") as source:
        while True:
            chunk = source.read(3 * 1024 * 1024)
            if not chunk:
                break
            writer.write_bytes(base64.b64encode(chunk))


def load_old() -> list[Entry]:
    manifest = json.loads((OLD_ROOT / "final-manifest.json").read_text(encoding="utf-8"))
    entries: list[Entry] = []
    for raw in manifest["documents"]:
        entries.append(
            Entry(
                index=int(raw["index"]),
                title=raw["title"],
                author=raw.get("author") or "",
                source_url=raw.get("resolvedUrl") or raw.get("sourceUrl") or "",
                html_path=OLD_ROOT / raw["html"],
                screenshot_path=OLD_ROOT / raw["stitched"],
                kind="legacy",
                source_index=int(raw["index"]),
            )
        )
    return sorted(entries, key=lambda x: x.index)


def load_new() -> list[Entry]:
    entries: list[Entry] = []
    page_files = [p for p in sorted((NEW_ROOT / "pages").glob("*.json")) if p.stem.isdigit()]
    for page in page_files:
        raw = json.loads(page.read_text(encoding="utf-8"))
        index = int(raw.get("index") or page.stem)
        html_rel = raw.get("html_file")
        if html_rel:
            html_path = NEW_ROOT / html_rel
        else:
            matches = list((NEW_ROOT / "html").glob(f"{index:03d}-*.html"))
            if len(matches) != 1:
                raise RuntimeError(f"Cannot resolve HTML for page {index}: {matches}")
            html_path = matches[0]
        entries.append(
            Entry(
                index=index,
                title=raw.get("title") or html_path.stem,
                author=raw.get("author") or raw.get("source_author") or "",
                source_url=raw.get("resolved_url") or raw.get("source_url") or raw.get("url") or "",
                html_path=html_path,
                kind="rich",
                source_index=index,
            )
        )
    return sorted(entries, key=lambda x: x.index)


BASE_CSS = r"""
:root{--bg:#f7f8fa;--surface:#fff;--surface2:#f2f4f7;--text:#1f2329;--muted:#646a73;--border:#dee0e3;--accent:#3370ff;--accent-soft:#e8f0ff;--shadow:0 8px 30px rgba(31,35,41,.08);--font:"PingFang SC","Microsoft YaHei","Noto Sans CJK SC",sans-serif}
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:var(--bg);color:var(--text);font-family:var(--font);font-size:16px;line-height:1.75}button,input{font:inherit}button,a{touch-action:manipulation}a{color:var(--accent);text-underline-offset:3px}button:focus-visible,a:focus-visible,input:focus-visible{outline:3px solid #baceff;outline-offset:2px}.hidden,[hidden]{display:none!important}
.appbar{position:sticky;top:0;z-index:50;height:58px;display:flex;align-items:center;justify-content:space-between;gap:16px;padding:0 24px;border-bottom:1px solid var(--border);background:rgba(255,255,255,.96);backdrop-filter:blur(12px)}.brand{min-width:0;font-size:17px;font-weight:700;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.topmeta{color:var(--muted);font-size:13px;white-space:nowrap}.app{width:min(1180px,calc(100% - 40px));margin:0 auto;padding:34px 0 72px}.intro{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:24px;align-items:end;margin-bottom:22px}.eyebrow{margin:0 0 5px;color:var(--accent);font-size:13px;font-weight:700;letter-spacing:.08em}.intro h1{margin:0;font-size:30px;line-height:1.3;letter-spacing:-.02em}.intro p{max-width:780px;margin:8px 0 0;color:var(--muted)}.stats{display:flex;gap:9px;flex-wrap:wrap;justify-content:flex-end}.stat{padding:7px 10px;border:1px solid var(--border);border-radius:8px;background:var(--surface);color:var(--muted);font-size:13px}.stat strong{color:var(--text);font-size:15px}
.catalog-tools{position:sticky;top:58px;z-index:40;display:flex;gap:12px;align-items:center;padding:12px 0;background:linear-gradient(var(--bg) 78%,rgba(247,248,250,0))}.search{width:100%;height:44px;padding:0 14px 0 42px;border:1px solid var(--border);border-radius:8px;background:var(--surface) url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='18' height='18' viewBox='0 0 24 24' fill='none' stroke='%23646a73' stroke-width='2'%3E%3Ccircle cx='11' cy='11' r='8'/%3E%3Cpath d='m21 21-4.3-4.3'/%3E%3C/svg%3E") no-repeat 14px center;color:var(--text)}.result-count{min-width:84px;color:var(--muted);font-size:13px;text-align:right}.doc-list{overflow:hidden;border:1px solid var(--border);border-radius:10px;background:var(--surface)}.doc-row{width:100%;min-height:70px;display:grid;grid-template-columns:54px minmax(0,1fr) 24px;gap:10px;align-items:center;padding:12px 18px;border:0;border-bottom:1px solid var(--border);background:transparent;color:inherit;text-align:left;cursor:pointer}.doc-row:last-child{border-bottom:0}.doc-row:hover{background:#f7f9ff}.doc-no{font-variant-numeric:tabular-nums;color:#8f959e;font-size:13px}.doc-title{display:block;font-weight:650;line-height:1.45}.doc-meta{display:block;margin-top:3px;color:var(--muted);font-size:12px}.chevron{color:#8f959e;font-size:20px}.empty{padding:60px 20px;text-align:center;color:var(--muted)}
.reader-toolbar{position:sticky;top:58px;z-index:40;display:flex;align-items:center;justify-content:space-between;gap:14px;margin:-8px 0 18px;padding:10px 0;background:linear-gradient(var(--bg) 82%,rgba(247,248,250,0))}.toolbar-group{display:flex;align-items:center;gap:10px;min-width:0}.btn{min-height:42px;display:inline-flex;align-items:center;justify-content:center;padding:8px 14px;border:1px solid var(--border);border-radius:8px;background:var(--surface);color:var(--text);font-weight:600;text-decoration:none;cursor:pointer}.btn:hover{border-color:#b7bbc2;background:#fafafa}.btn.primary{border-color:var(--accent);background:var(--accent);color:#fff}.reader-position{max-width:460px;overflow:hidden;color:var(--muted);font-size:13px;text-overflow:ellipsis;white-space:nowrap}.reader-card{overflow:hidden;border:1px solid var(--border);border-radius:12px;background:var(--surface);box-shadow:var(--shadow)}.reader-inner{min-height:60vh}.modebar{display:flex;gap:8px;padding:14px 20px;border-bottom:1px solid var(--border);background:#fafbfc}.modebar button{min-height:38px;padding:6px 12px;border:1px solid var(--border);border-radius:7px;background:#fff;cursor:pointer}.modebar button.active{border-color:#abc4ff;background:var(--accent-soft);color:#245bdb;font-weight:700}.legacy-text{width:min(860px,calc(100% - 40px));margin:0 auto;padding:46px 0 76px}.legacy-image{padding:24px;background:#edf0f4;text-align:center}.legacy-image img{display:block;width:min(100%,1100px);height:auto;margin:0 auto;background:#fff;box-shadow:0 2px 14px rgba(0,0,0,.12)}
.legacy-text h1,.document-title{margin:0 0 18px;font-size:30px;line-height:1.35}.legacy-text h2{margin:1.7em 0 .6em;font-size:23px;line-height:1.45}.legacy-text h3{margin:1.5em 0 .5em;font-size:19px}.legacy-text p{margin:.72em 0}.legacy-text .meta,.document-meta{display:flex;gap:14px;flex-wrap:wrap;margin-bottom:30px;color:var(--muted);font-size:13px}.legacy-text .content{overflow-wrap:anywhere}.legacy-text .spacer{height:.7em}
.document-shell{width:min(860px,calc(100% - 40px));margin:0 auto;padding:48px 0 76px}.document-header{margin-bottom:34px}.document-content{overflow-wrap:anywhere}.doc-block{margin:0 0 12px}.document-content h1.doc-block,.document-content h2.doc-block,.document-content h3.doc-block{margin-top:1.55em;margin-bottom:.58em;line-height:1.4}.document-content h1.doc-block{font-size:30px}.document-content h2.doc-block{font-size:24px}.document-content h3.doc-block{font-size:20px}.rich-text code{padding:1px 4px;border-radius:4px;background:var(--surface2)}.list-row{display:grid;grid-template-columns:28px minmax(0,1fr);gap:8px;margin-bottom:8px}.table-wrap{max-width:100%;overflow-x:auto;margin:18px 0}.table-wrap table{border-collapse:collapse;min-width:100%}.table-wrap td,.table-wrap th{padding:9px 11px;border:1px solid var(--border);vertical-align:top}.doc-image{margin:20px auto;text-align:center}.doc-image img,.document-content img{max-width:100%;height:auto}.doc-image figcaption{color:var(--muted);font-size:13px}.document-content video{max-width:100%;height:auto}.document-content pre{max-width:100%;overflow:auto;padding:14px;border-radius:8px;background:#f5f6f7}.document-content blockquote{margin:18px 0;padding:4px 18px;border-left:4px solid #baceff;background:#f8faff;color:#4e5969}.document-content iframe{max-width:100%}.file-card,.attachment-card{padding:14px;border:1px solid var(--border);border-radius:8px;background:#fafbfc}
.dedupe-note{margin:0 0 18px;padding:12px 14px;border:1px solid #c6d6ff;border-radius:8px;background:#f2f6ff;color:#3c5688;font-size:13px}
@media(max-width:700px){.appbar{height:auto;min-height:56px;padding:10px 14px}.topmeta{display:none}.app{width:min(100% - 24px,1180px);padding:22px 0 52px}.intro{grid-template-columns:1fr}.stats{justify-content:flex-start}.intro h1{font-size:25px}.catalog-tools,.reader-toolbar{top:56px}.doc-row{grid-template-columns:42px minmax(0,1fr) 18px;padding:12px 12px}.reader-toolbar{align-items:flex-start}.toolbar-group:last-child{display:none}.reader-card{margin:0 -4px}.legacy-text,.document-shell{width:min(100% - 28px,860px);padding:30px 0 54px}.legacy-text h1,.document-title,.document-content h1.doc-block{font-size:25px}.legacy-image{padding:8px}.modebar{padding:10px 12px}.result-count{min-width:auto}}
"""


def source_document_css() -> str:
    """Preserve every renderer-specific block style without external CSS files."""
    tokens_path = NEW_ROOT / "styles" / "tokens.css"
    document_path = NEW_ROOT / "styles" / "document.css"
    if not tokens_path.is_file() or not document_path.is_file():
        return ""
    tokens = tokens_path.read_text(encoding="utf-8")
    document = document_path.read_text(encoding="utf-8")
    document = re.sub(r'@import\s+url\([^;]+;\s*', "", document, count=1)
    return tokens + "\n" + document


JS = r"""
const docs = __DOCS__;
const catalogView=document.getElementById('catalogView');
const readerView=document.getElementById('readerView');
const list=document.getElementById('docList');
const search=document.getElementById('search');
const resultCount=document.getElementById('resultCount');
const reader=document.getElementById('readerContent');
const readerPosition=document.getElementById('readerPosition');
const sourceLink=document.getElementById('sourceLink');
let activeIndex=null;
function renderList(){
  const q=search.value.trim().toLowerCase();
  const filtered=docs.filter(d=>(d.title+' '+d.author+' '+d.no).toLowerCase().includes(q));
  list.replaceChildren();
  filtered.forEach(d=>{
    const b=document.createElement('button'); b.className='doc-row'; b.type='button'; b.dataset.index=d.index;
    const no=document.createElement('span'); no.className='doc-no'; no.textContent=String(d.no).padStart(3,'0');
    const body=document.createElement('span');
    const title=document.createElement('span'); title.className='doc-title'; title.textContent=d.title;
    const meta=document.createElement('span'); meta.className='doc-meta'; meta.textContent=(d.author?d.author+' · ':'')+d.kindLabel;
    const chev=document.createElement('span'); chev.className='chevron'; chev.textContent='›';
    body.append(title,meta); b.append(no,body,chev); b.addEventListener('click',()=>openDoc(d.index)); list.append(b);
  });
  if(!filtered.length){const e=document.createElement('div');e.className='empty';e.textContent='没有找到匹配文档';list.append(e)}
  resultCount.textContent=filtered.length+' 篇';
}
function openDoc(index,push=true){
  const d=docs.find(x=>x.index===Number(index)); if(!d)return;
  const t=document.getElementById('article-'+d.index);
  if(!t){
    const waiting=document.createElement('div'); waiting.className='empty'; waiting.textContent='目录已经可用，正文资源仍在加载，请稍候…';
    reader.replaceChildren(waiting); activeIndex=d.index; readerPosition.textContent=String(d.no).padStart(3,'0')+' / '+docs.length+' · '+d.title;
    sourceLink.href=d.source||'#'; sourceLink.hidden=!d.source; catalogView.classList.add('hidden'); readerView.classList.remove('hidden');
    document.title=d.title+' · '+window.bundleTitle; if(push)history.pushState({doc:d.index},'', '#doc-'+d.index); window.scrollTo(0,0);
    document.addEventListener('DOMContentLoaded',()=>openDoc(d.index,false),{once:true}); return;
  }
  reader.replaceChildren(t.content.cloneNode(true));
  activeIndex=d.index; readerPosition.textContent=String(d.no).padStart(3,'0')+' / '+docs.length+' · '+d.title;
  sourceLink.href=d.source||'#'; sourceLink.hidden=!d.source;
  catalogView.classList.add('hidden'); readerView.classList.remove('hidden'); document.title=d.title+' · '+window.bundleTitle;
  if(push)history.pushState({doc:d.index},'', '#doc-'+d.index); window.scrollTo(0,0);
}
function showCatalog(push=true){
  activeIndex=null; reader.replaceChildren(); readerView.classList.add('hidden'); catalogView.classList.remove('hidden'); document.title=window.bundleTitle;
  if(push)history.pushState({},'',location.pathname+location.search); window.scrollTo(0,0); search.focus({preventScroll:true});
}
document.getElementById('backBtn').addEventListener('click',()=>showCatalog());
search.addEventListener('input',renderList);
reader.addEventListener('click',e=>{
  const b=e.target.closest('[data-legacy-mode]'); if(!b)return;
  const root=b.closest('.legacy-frame'); const showImage=b.dataset.legacyMode==='image';
  root.querySelector('.legacy-text').hidden=showImage; root.querySelector('.legacy-image').hidden=!showImage;
  root.querySelectorAll('[data-legacy-mode]').forEach(x=>x.classList.toggle('active',x===b)); window.scrollTo(0,0);
});
window.addEventListener('popstate',()=>{const m=location.hash.match(/^#doc-(\d+)$/);m?openDoc(Number(m[1]),false):showCatalog(false)});
window.bundleTitle=document.querySelector('.brand').textContent; renderList();
const initial=location.hash.match(/^#doc-(\d+)$/);
if(initial){document.addEventListener('DOMContentLoaded',()=>openDoc(Number(initial[1]),false),{once:true})}
document.addEventListener('DOMContentLoaded',()=>{const state=document.getElementById('loadState');if(state)state.textContent='单文件离线归档 · UTF-8 · 全部资源已加载'},{once:true});
"""


def write_fragment_with_assets(writer: HashWriter, fragment: str, asset_root: Path) -> tuple[int, set[Path]]:
    cursor = 0
    count = 0
    used: set[Path] = set()
    for match in ASSET_REF_RE.finditer(fragment):
        writer.write(fragment[cursor : match.start()])
        rel = html.unescape(unquote(match.group(0)[3:])).replace("/", os.sep)
        asset = (asset_root / rel).resolve()
        if not asset.is_relative_to(asset_root.resolve()):
            raise RuntimeError(f"Unsafe asset path: {match.group(0)}")
        write_data_uri(writer, asset)
        used.add(asset)
        count += 1
        cursor = match.end()
    writer.write(fragment[cursor:])
    return count, used


def safe_json(data: object) -> str:
    return json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")


def output_file(root: Path, name: str) -> Path:
    if Path(name).name != name or not re.fullmatch(r"[A-Za-z0-9._-]+\.html", name):
        raise SystemExit(f"Output filename must be an ASCII .html basename: {name!r}")
    return root / name


def build_bundle(path: Path, entries: list[Entry], title: str, eyebrow: str, note: str = "") -> dict:
    path.parent.mkdir(parents=True, exist_ok=True)
    writer = HashWriter(path)
    asset_refs = 0
    used_assets: set[Path] = set()
    docs_meta = [
        {
            "index": position,
            "no": entry.index,
            "title": entry.title,
            "author": entry.author,
            "source": entry.source_url,
            "kindLabel": "原貌长图 + 可复制正文" if entry.kind == "legacy" else "飞书正文 + 原始资源",
        }
        for position, entry in enumerate(entries, start=1)
    ]
    writer.write("<!doctype html><html lang=\"zh-CN\"><head><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">")
    writer.write(f"<title>{html.escape(title)}</title><style>{BASE_CSS}{source_document_css()}</style></head><body>")
    writer.write(f'<header class="appbar"><div class="brand">{html.escape(title)}</div><div id="loadState" class="topmeta">目录已就绪 · 正文资源加载中</div></header>')
    writer.write('<div class="app"><section id="catalogView">')
    writer.write(f'<div class="intro"><div><p class="eyebrow">{html.escape(eyebrow)}</p><h1>归档目录</h1><p>打开任意条目阅读正文；所有页面和本地资源已包含在本 HTML 中，可直接复制给他人离线查看。</p></div><div class="stats"><span class="stat"><strong>{len(entries)}</strong> 条归档</span><span class="stat">UTF-8</span><span class="stat">单文件</span></div></div>')
    if note:
        writer.write(f'<div class="dedupe-note">{html.escape(note)}</div>')
    writer.write('<div class="catalog-tools"><input id="search" class="search" type="search" placeholder="搜索标题、作者或序号" autocomplete="off"><span id="resultCount" class="result-count"></span></div><div id="docList" class="doc-list"></div></section>')
    writer.write('<section id="readerView" class="hidden"><div class="reader-toolbar"><div class="toolbar-group"><button id="backBtn" class="btn" type="button">← 返回目录</button><span id="readerPosition" class="reader-position"></span></div><div class="toolbar-group"><a id="sourceLink" class="btn primary" target="_blank" rel="noreferrer">打开来源</a></div></div><div class="reader-card"><div id="readerContent" class="reader-inner"></div></div></section></div>')

    # Bootstrap the catalog before the large embedded templates. On first open the
    # directory becomes usable while the browser continues parsing the asset tail.
    script = JS.replace("__DOCS__", safe_json(docs_meta))
    writer.write(f"<script>{script}</script>")

    for position, entry in enumerate(entries, start=1):
        if "\ufffd" in entry.title or "\ufffd" in entry.author:
            raise RuntimeError(f"Replacement character found in metadata: {entry.title}")
        source_html = entry.html_path.read_text(encoding="utf-8")
        if "\ufffd" in source_html:
            raise RuntimeError(f"Replacement character found in source HTML: {entry.html_path}")
        writer.write(f'<template id="article-{position}">')
        if entry.kind == "legacy":
            match = OLD_TEXT_RE.search(source_html)
            if not match:
                raise RuntimeError(f"Cannot extract legacy text: {entry.html_path}")
            writer.write('<div class="legacy-frame"><div class="modebar"><button class="active" type="button" data-legacy-mode="text">可复制正文</button><button type="button" data-legacy-mode="image">原貌长图</button></div><div class="legacy-text">')
            writer.write(match.group(1))
            writer.write('</div><div class="legacy-image" hidden><img loading="lazy" alt="原貌长图" src="')
            assert entry.screenshot_path is not None
            write_data_uri(writer, entry.screenshot_path)
            writer.write('"></div></div>')
            asset_refs += 1
            used_assets.add(entry.screenshot_path.resolve())
        else:
            match = NEW_MAIN_RE.search(source_html)
            if not match:
                raise RuntimeError(f"Cannot extract document main: {entry.html_path}")
            count, assets = write_fragment_with_assets(writer, match.group(1), NEW_ROOT)
            asset_refs += count
            used_assets.update(assets)
            asset_dir = NEW_ROOT / "assets" / f"{entry.source_index:03d}"
            extra_assets = []
            if asset_dir.is_dir():
                extra_assets = [
                    item
                    for item in sorted(asset_dir.iterdir())
                    if item.is_file() and item.name != "manifest.json" and item.resolve() not in assets
                ]
            if extra_assets:
                writer.write('<section class="document-shell"><h2>补充附件</h2><p>以下资源随源归档保存，但未直接显示在正文中。</p>')
                for extra in extra_assets:
                    writer.write(f'<p><a class="btn" download="{html.escape(extra.name, quote=True)}" href="')
                    write_data_uri(writer, extra)
                    writer.write(f'">下载 {html.escape(extra.name)}</a></p>')
                    asset_refs += 1
                    used_assets.add(extra.resolve())
                writer.write('</section>')
        writer.write('</template>')

    writer.write("</body></html>")
    writer.close()
    return {
        "path": str(path),
        "bytes": writer.size,
        "sha256": writer.hexdigest,
        "entries": len(entries),
        "asset_references": asset_refs,
        "unique_embedded_assets": len(used_assets),
    }


def verify_bundle(report: dict) -> dict:
    path = Path(report["path"])
    template_count = 0
    data_uri_count = 0
    legacy_refs = 0
    replacement_chars = 0
    tail = b""
    with path.open("rb") as source:
        while True:
            chunk = source.read(8 * 1024 * 1024)
            if not chunk:
                break
            scan = tail + chunk
            template_count += scan.count(b'<template id="article-')
            data_uri_count += scan.count(b"data:")
            legacy_refs += scan.count(b"../assets/") + scan.count(b"../stitched-hq/")
            replacement_chars += scan.count(b"\xef\xbf\xbd")
            tail = scan[-64:]
    head = path.open("rb").read(512).decode("utf-8")
    with path.open("rb") as source:
        source.seek(max(0, path.stat().st_size - 256))
        ending = source.read()
    checks = {
        "utf8_meta": '<meta charset="utf-8">' in head,
        "template_count": template_count == report["entries"],
        "data_uris_present": data_uri_count >= report["asset_references"],
        "no_external_local_refs": legacy_refs == 0,
        "no_replacement_chars": replacement_chars == 0,
        "complete_closing_tags": ending.endswith(b"</body></html>"),
    }
    return {**report, "observed_templates": template_count, "observed_data_uris": data_uri_count, "checks": checks, "passed": all(checks.values())}


def main() -> None:
    global OLD_ROOT, NEW_ROOT, OUT_ROOT, WORK_ROOT
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("legacy", "rich", "merged", "all"), required=True)
    parser.add_argument("--legacy-root", default="", help="Legacy archive with final-manifest.json, html/, and stitched-hq/.")
    parser.add_argument("--rich-root", default="", help="Rich archive with numeric pages/*.json, html/, assets/, and styles/.")
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--report", default="", help="Optional JSON verification report path.")
    parser.add_argument("--legacy-name", default="feishu-legacy-bundle.html")
    parser.add_argument("--rich-name", default="feishu-rich-bundle.html")
    parser.add_argument("--merged-name", default="feishu-all-deduplicated-bundle.html")
    parser.add_argument("--title-prefix", default="飞书")
    args = parser.parse_args()

    OUT_ROOT = Path(args.output_dir).resolve()
    WORK_ROOT = OUT_ROOT
    OLD_ROOT = Path(args.legacy_root).resolve() if args.legacy_root else Path("__unset_legacy_root__").resolve()
    NEW_ROOT = Path(args.rich_root).resolve() if args.rich_root else Path("__unset_rich_root__").resolve()
    need_legacy = args.mode in {"legacy", "merged", "all"}
    need_rich = args.mode in {"rich", "merged", "all"}
    if need_legacy and (not args.legacy_root or not (OLD_ROOT / "final-manifest.json").is_file()):
        raise SystemExit("--legacy-root must contain final-manifest.json for this mode")
    if need_rich and (not args.rich_root or not (NEW_ROOT / "pages").is_dir() or not (NEW_ROOT / "html").is_dir()):
        raise SystemExit("--rich-root must contain pages/ and html/ for this mode")

    old_entries = load_old() if need_legacy else []
    new_entries = load_new() if need_rich else []
    unique_new: list[Entry] = []
    seen: set[str] = set()
    duplicate_rows: list[dict] = []
    for entry in new_entries:
        key = normal_url(entry.source_url)
        if key in seen:
            duplicate_rows.append({"index": entry.index, "title": entry.title, "url": entry.source_url})
        else:
            seen.add(key)
            unique_new.append(entry)
    old_keys = {normal_url(x.source_url) for x in old_entries}
    overlap = len(old_keys & seen)
    merged_entries = list(unique_new)
    merged_seen = {normal_url(x.source_url) for x in merged_entries}
    for entry in old_entries:
        key = normal_url(entry.source_url)
        if key not in merged_seen:
            merged_seen.add(key)
            merged_entries.append(entry)
    reports: list[dict] = []
    targets = ("legacy", "rich", "merged") if args.mode == "all" else (args.mode,)
    if "legacy" in targets:
        reports.append(build_bundle(output_file(OUT_ROOT, args.legacy_name), old_entries, f"{args.title_prefix} {len(old_entries)} 篇归档", f"旧批次 · {len(old_entries)} 条"))
    if "rich" in targets:
        reports.append(build_bundle(output_file(OUT_ROOT, args.rich_name), new_entries, f"{args.title_prefix} {len(new_entries)} 条归档", f"新批次 · 保留原始 {len(new_entries)} 条"))
    if "merged" in targets:
        note = f"去重说明：两批共 {len(old_entries) + len(new_entries)} 条记录；跨批重合 {overlap} 条，新批次内部重复 {len(duplicate_rows)} 条；按来源 URL 去重后为 {len(merged_entries)} 篇唯一文档。"
        reports.append(build_bundle(output_file(OUT_ROOT, args.merged_name), merged_entries, f"{args.title_prefix}总归档 · {len(merged_entries)} 篇唯一文档", "两批合并 · 已去重", note))
    verified = [verify_bundle(x) for x in reports]
    result = {
        "source_counts": {"old": len(old_entries), "new": len(new_entries), "overlap": overlap, "new_internal_duplicates": len(duplicate_rows), "union_unique": len(merged_entries)},
        "duplicates": duplicate_rows,
        "bundles": verified,
    }
    WORK_ROOT.mkdir(parents=True, exist_ok=True)
    report_path = Path(args.report).resolve() if args.report else WORK_ROOT / "bundle-build-report.json"
    report_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=True, indent=2))
    if not all(x["passed"] for x in verified):
        raise SystemExit(2)


if __name__ == "__main__":
    main()
