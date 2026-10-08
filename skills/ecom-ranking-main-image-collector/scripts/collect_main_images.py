#!/usr/bin/env python3
"""Collect public ecommerce main-image candidates from category ranking/search pages."""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import ipaddress
import socket
import html
import json
import mimetypes
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


IMAGE_ATTRS = (
    "src",
    "data-src",
    "data-original",
    "data-lazy-img",
    "data-lazyload",
    "data-img",
    "data-image",
    "data-url",
)

BLOCK_MARKERS = (
    "captcha",
    "验证码",
    "访问受限",
    "安全验证",
    "risk",
    "risk-control",
    "blocked",
    "anti-spider",
    "滑块验证",
)

SKIP_IMAGE_MARKERS = (
    "sprite",
    "logo",
    "icon",
    "avatar",
    "blank",
    "loading",
    "pixel",
    "transparent",
    "beacon",
    "qrcode",
    "54b887",
    "56a0a994",
    "56a89b8",
)

ITEM_ID_RE = re.compile(r"(?:[?&](?:id|itemId|item_id|auctionId)=|[\"'](?:id|itemId|item_id|auctionId|nid)[\"']\s*:\s*[\"']?)(\d{8,16})", re.I)
PRICE_RE = re.compile(r"(?:¥|￥|&yen;|\\u00a5)\s*(\d+(?:\.\d+)?)", re.I)
VOLUME_RE = re.compile(r"(\d+(?:\.\d+)?\s*万?\+?\s*(?:人付款|付款|人已买|已售|销量|评价|条评价))")



def validate_public_http_url(url: str, allowed_local_origin: str | None = None) -> str:
    """Reject local, private, credential-bearing, and non-HTTP targets."""
    parsed = urllib.parse.urlsplit(url.strip())
    if parsed.scheme not in {"http", "https"}:
        raise ValueError("only http:// and https:// product URLs are allowed")
    if not parsed.hostname:
        raise ValueError("product URL must include a hostname")
    if parsed.username or parsed.password:
        raise ValueError("product URL must not include embedded credentials")

    hostname = parsed.hostname.rstrip(".").lower()
    if allowed_local_origin:
        origin = urllib.parse.urlsplit(allowed_local_origin)
        try:
            loopback = ipaddress.ip_address(hostname).is_loopback
        except ValueError:
            loopback = False
        if loopback and (parsed.scheme, hostname, parsed.port) == (origin.scheme, origin.hostname, origin.port):
            return urllib.parse.urlunsplit(parsed)

    if hostname == "localhost" or hostname.endswith(".localhost"):
        raise ValueError("local or private network URLs are not allowed")

    try:
        addresses = {ipaddress.ip_address(hostname)}
    except ValueError:
        try:
            addresses = {
                ipaddress.ip_address(item[4][0])
                for item in socket.getaddrinfo(hostname, parsed.port or 443, type=socket.SOCK_STREAM)
            }
        except socket.gaierror as exc:
            raise ValueError(f"product URL hostname could not be resolved: {hostname}") from exc

    if not addresses or any(not address.is_global for address in addresses):
        raise ValueError("local, private, reserved, or non-routable network URLs are not allowed")
    return urllib.parse.urlunsplit(parsed)


class PublicOnlyRedirectHandler(urllib.request.HTTPRedirectHandler):
    """Apply the same public-network checks to every redirect target."""

    def __init__(self, allowed_local_origin=None):
        super().__init__()
        self.allowed_local_origin = allowed_local_origin

    def redirect_request(self, req, fp, code, msg, headers, newurl):  # noqa: ANN001, D102
        safe_url = validate_public_http_url(newurl, self.allowed_local_origin)
        return super().redirect_request(req, fp, code, msg, headers, safe_url)



def slugify(text: str, max_len: int = 60) -> str:
    original = text.strip()
    text = re.sub(r"\s+", "-", original.lower())
    text = re.sub(r"[^a-z0-9._-]+", "-", text)
    text = re.sub(r"-{2,}", "-", text).strip("-")
    if not text:
        digest = hashlib.sha1(original.encode("utf-8", errors="ignore")).hexdigest()[:10]
        text = f"u{digest}"
    return text[:max_len] or "item"


def build_candidate_urls(category: str, platform: str) -> list[tuple[str, str]]:
    q = urllib.parse.quote(category)
    candidates: dict[str, list[tuple[str, str]]] = {
        "jd": [
            (f"https://search.jd.com/Search?keyword={q}&enc=utf-8&psort=3", "sales-sorted search result"),
        ],
        "taobao": [
            (f"https://s.taobao.com/search?q={q}&sort=sale-desc", "sales-sorted search result"),
        ],
        "tmall": [
            (f"https://list.tmall.com/search_product.htm?q={q}&sort=s", "sales-sorted search result"),
        ],
        "pdd": [],
        "douyin": [],
    }
    if platform == "mixed":
        urls: list[tuple[str, str]] = []
        for key in ("jd", "taobao", "tmall"):
            urls.extend(candidates.get(key, []))
        return urls
    return candidates.get(platform.lower(), [])


def read_url(url: str, timeout: int, user_agent: str) -> tuple[str | None, str | None]:
    try:
        url = validate_public_http_url(url)
    except ValueError as exc:
        return None, str(exc)
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": user_agent,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.6",
        },
    )
    try:
        with urllib.request.build_opener(PublicOnlyRedirectHandler()).open(req, timeout=timeout) as resp:
            charset = resp.headers.get_content_charset() or "utf-8"
            raw = resp.read()
            return raw.decode(charset, errors="replace"), None
    except urllib.error.HTTPError as exc:
        return None, f"HTTP {exc.code}"
    except urllib.error.URLError as exc:
        return None, f"URL error: {exc.reason}"
    except TimeoutError:
        return None, "timeout"


def normalize_image_url(value: str, base_url: str) -> str | None:
    if not value:
        return None
    value = html.unescape(value).strip().strip("'\"")
    value = value.replace("\\/", "/")
    if value.startswith("data:"):
        return None
    if value.startswith("//"):
        value = "https:" + value
    if value.startswith("/"):
        value = urllib.parse.urljoin(base_url, value)
    parsed = urllib.parse.urlparse(value)
    if parsed.scheme not in ("http", "https"):
        return None
    value = upgrade_product_image_url(urllib.parse.urlunparse(parsed._replace(fragment="")))
    parsed = urllib.parse.urlparse(value)
    return urllib.parse.urlunparse(parsed._replace(fragment=""))


def upgrade_product_image_url(url: str) -> str:
    """Prefer product-analysis sized JD images over tiny thumbnails when URL shape allows it."""
    if "360buyimg.com" not in url:
        return url
    url = re.sub(r"/n\d+/(s\d+x\d+_)?jfs/", "/n1/jfs/", url)
    url = re.sub(r"/shaidan/s\d+x\d+_", "/shaidan/", url)
    return url


def is_probable_product_image(url: str) -> bool:
    lower = url.lower()
    if any(marker in lower for marker in SKIP_IMAGE_MARKERS):
        return False
    if "360buyimg.com/shaidan/" in lower:
        return False
    if not re.search(r"\.(jpg|jpeg|png|webp)(\?|$)", lower):
        product_cdns = ("360buyimg", "alicdn", "tbcdn", "pinduoduo", "douyinpic", "byteimg")
        return any(host in lower for host in product_cdns)
    return True


def clean_visible_text(value: str, max_len: int = 240) -> str:
    value = re.sub(r"<script\b.*?</script>", " ", value or "", flags=re.I | re.S)
    value = re.sub(r"<style\b.*?</style>", " ", value, flags=re.I | re.S)
    value = re.sub(r"<[^>]+>", " ", value)
    value = html.unescape(value)
    value = value.replace("\\/", "/")
    if "\\u" in value:
        try:
            value = value.encode("utf-8").decode("unicode_escape")
        except Exception:
            pass
    value = re.sub(r"\s+", " ", value).strip()
    return value[:max_len]


def js_string(value: str) -> str:
    value = html.unescape(value or "").strip().strip("'\"")
    value = value.replace("\\/", "/")
    if "\\u" in value:
        try:
            value = value.encode("utf-8").decode("unicode_escape")
        except Exception:
            pass
    return value


def jsonish_field(block: str, names: tuple[str, ...]) -> str:
    for name in names:
        match = re.search(rf'["\']{re.escape(name)}["\']\s*:\s*["\'](.*?)["\']', block, flags=re.I | re.S)
        if match:
            return js_string(match.group(1))
    return ""


def extract_item_id(value: str) -> str:
    match = ITEM_ID_RE.search(value or "")
    return match.group(1) if match else ""


def canonical_item_url(item_id: str, source_url: str, raw_url: str = "") -> str:
    if not item_id:
        return ""
    host_blob = f"{source_url} {raw_url}".lower()
    host = "https://detail.tmall.com/item.htm" if "tmall" in host_blob else "https://item.taobao.com/item.htm"
    return f"{host}?id={item_id}"


def normalize_item_url(value: str, source_url: str, item_id: str = "") -> str:
    href = js_string(value)
    if href.startswith("//"):
        href = "https:" + href
    elif href.startswith("/"):
        href = urllib.parse.urljoin(source_url, href)
    if href and not href.startswith("http"):
        href = ""
    item = item_id or extract_item_id(href)
    return canonical_item_url(item, source_url, href) if item else href.split("#")[0]


def parse_price_text(value: str) -> tuple[str, str]:
    match = PRICE_RE.search(value or "")
    if not match:
        # Common JSON fields store only the numeric part.
        numeric = re.search(r'["\'](?:view_price|price|salePrice|promotionPrice|priceShow)["\']\s*:\s*["\']?(\d+(?:\.\d+)?)', value or "", flags=re.I)
        if not numeric:
            return "", ""
        price_num = numeric.group(1)
    else:
        price_num = match.group(1)
    return f"¥{price_num}", price_num


def extract_volume_text(value: str) -> str:
    match = VOLUME_RE.search(clean_visible_text(value, 1200))
    return match.group(1).replace(" ", "") if match else ""


def extract_shop_name(value: str) -> str:
    for names in (("nick", "shopName", "shop_name", "sellerNick"),):
        found = jsonish_field(value, names)
        if found:
            return clean_visible_text(found, 80)
    text = clean_visible_text(value, 900)
    match = re.search(r"([\w\u4e00-\u9fff·（）() -]{2,40}(?:旗舰店|专营店|专卖店|官方店|店))", text)
    return match.group(1).strip() if match else ""


def clean_title_candidate(value: str) -> str:
    value = clean_visible_text(value, 260)
    value = PRICE_RE.sub(" ", value)
    value = VOLUME_RE.sub(" ", value)
    value = re.sub(r"([\w\u4e00-\u9fff·（）() -]{2,40}(?:旗舰店|专营店|专卖店|官方店|店))", " ", value)
    value = re.sub(r"\s+", " ", value).strip()
    return value[:180]


def infer_title(segment: str, anchor_text: str = "") -> str:
    for attr in ("title", "alt", "aria-label"):
        found = extract_attr(segment, attr)
        if found:
            candidate = clean_title_candidate(found)
            if candidate:
                return candidate
    for candidate in (
        clean_title_candidate(anchor_text),
        clean_title_candidate(jsonish_field(segment, ("raw_title", "title", "name", "itemTitle", "productName"))),
    ):
        if candidate:
            return candidate
    text = clean_visible_text(segment, 600)
    text = re.sub(r"(?:¥|￥)\s*\d+(?:\.\d+)?", " ", text)
    text = re.sub(r"\d+(?:\.\d+)?\s*万?\+?\s*(?:人付款|付款|人已买|已售|销量|评价|条评价)", " ", text)
    parts = [part.strip() for part in re.split(r"\s{2,}|[|｜]", text) if len(part.strip()) >= 4]
    return parts[0][:180] if parts else ""


def extract_terms_from_title(title: str) -> str:
    terms = []
    for token in re.split(r"[\s,，、/|｜;；]+", title or ""):
        token = token.strip()
        if len(token) >= 2 and not re.fullmatch(r"\d+(?:\.\d+)?", token):
            terms.append(token)
    return "|".join(list(dict.fromkeys(terms))[:8])


def card_record_from_segment(segment: str, source_url: str, source_type: str, href: str = "", anchor_text: str = "") -> dict[str, str] | None:
    blob = f"{href} {anchor_text} {segment}"
    item_id = extract_item_id(blob)
    images = extract_images(segment, source_url)
    image_url = images[0]["image_url"] if images else ""
    title = infer_title(segment, anchor_text)
    price, price_num = parse_price_text(segment)
    item_url = normalize_item_url(href or jsonish_field(segment, ("detail_url", "itemUrl", "url")), source_url, item_id)
    if not item_id and item_url:
        item_id = extract_item_id(item_url)
    if not (item_id or image_url or price):
        return None
    return {
        "image_url": image_url,
        "product_name": title,
        "title": title,
        "price": price,
        "price_num": price_num,
        "volume": extract_volume_text(segment),
        "shop_name": extract_shop_name(segment),
        "item_id": item_id,
        "item_url": canonical_item_url(item_id, source_url, href) if item_id else item_url,
        "is_ad": "yes" if re.search(r"广告|ad_|xxc=ad|ali_trackid|ali_refid", blob, flags=re.I) else "",
        "terms": extract_terms_from_title(title),
        "source_url": source_url,
        "source_type": f"{source_type}; product card",
    }


def extract_product_cards(text: str, source_url: str, source_type: str) -> list[dict[str, str]]:
    records: list[dict[str, str]] = []

    anchor_re = re.compile(r"<a\b([^>]*\bhref\s*=\s*(?:\"([^\"]+)\"|'([^']+)'|([^\s>]+))[^>]*)>(.*?)</a>", flags=re.I | re.S)
    for match in anchor_re.finditer(text or ""):
        href = match.group(2) or match.group(3) or match.group(4) or ""
        if not re.search(r"(?:item\.htm|detail\.tmall|item\.taobao|[?&](?:id|itemId|auctionId)=)", href, flags=re.I):
            continue
        start = max(0, match.start() - 900)
        end = min(len(text), match.end() + 900)
        segment = text[start:end]
        record = card_record_from_segment(segment, source_url, source_type, href, match.group(5) or "")
        if record:
            records.append(record)

    object_re = re.compile(
        r"\{[^{}]{0,2600}(?:nid|itemId|item_id|auctionId|raw_title|view_price|price|pic_url|picUrl|item_pic)[^{}]{0,2600}\}",
        flags=re.I | re.S,
    )
    for match in object_re.finditer(text or ""):
        block = match.group(0)
        item_id = extract_item_id(block) or jsonish_field(block, ("nid", "itemId", "item_id", "auctionId"))
        href = jsonish_field(block, ("detail_url", "itemUrl", "url"))
        image = jsonish_field(block, ("pic_url", "picUrl", "item_pic", "image", "imageUrl", "mainPic"))
        image_url = normalize_image_url(image, source_url) or ""
        title = infer_title(block)
        price, price_num = parse_price_text(block)
        if not (item_id or image_url or price):
            continue
        records.append(
            {
                "image_url": image_url,
                "product_name": title,
                "title": title,
                "price": price,
                "price_num": price_num,
                "volume": extract_volume_text(block),
                "shop_name": extract_shop_name(block),
                "item_id": item_id,
                "item_url": canonical_item_url(item_id, source_url, href) if item_id else normalize_item_url(href, source_url),
                "is_ad": "yes" if re.search(r"广告|ad_|xxc=ad|ali_trackid|ali_refid", block, flags=re.I) else "",
                "terms": extract_terms_from_title(title),
                "source_url": source_url,
                "source_type": f"{source_type}; embedded product data",
            }
        )

    deduped: list[dict[str, str]] = []
    seen: set[str] = set()
    for record in records:
        key = record.get("item_id") or record.get("item_url") or record.get("image_url") or record.get("title")
        if not key or key in seen:
            continue
        seen.add(key)
        deduped.append(record)
    return deduped


def extract_attr(tag: str, attr: str) -> str:
    match = re.search(rf'\b{re.escape(attr)}\s*=\s*(".*?"|\'.*?\'|[^\s>]+)', tag, flags=re.I | re.S)
    if not match:
        return ""
    return match.group(1).strip("'\"")


def extract_images(text: str, source_url: str) -> list[dict[str, str]]:
    records: list[dict[str, str]] = []

    for tag_match in re.finditer(r"<img\b[^>]*>", text, flags=re.I | re.S):
        tag = tag_match.group(0)
        image_url = ""
        for attr in IMAGE_ATTRS:
            image_url = extract_attr(tag, attr)
            if image_url:
                break
        normalized = normalize_image_url(image_url, source_url)
        if not normalized or not is_probable_product_image(normalized):
            continue
        product_name = extract_attr(tag, "alt") or extract_attr(tag, "title")
        records.append(
            {
                "image_url": normalized,
                "product_name": html.unescape(product_name).strip(),
                "source_url": source_url,
                "source_type": "img tag",
            }
        )

    for match in re.finditer(r'background-image\s*:\s*url\((.*?)\)', text, flags=re.I | re.S):
        normalized = normalize_image_url(match.group(1), source_url)
        if normalized and is_probable_product_image(normalized):
            records.append(
                {
                    "image_url": normalized,
                    "product_name": "",
                    "source_url": source_url,
                    "source_type": "css background",
                }
            )

    for match in re.finditer(r'["\'](?:pic_url|image|imageUrl|img|mainPic|pic)\s*["\']\s*:\s*["\']([^"\']+)["\']', text, flags=re.I):
        normalized = normalize_image_url(match.group(1), source_url)
        if normalized and is_probable_product_image(normalized):
            records.append(
                {
                    "image_url": normalized,
                    "product_name": "",
                    "source_url": source_url,
                    "source_type": "embedded data",
                }
            )

    # Visible product-card links often carry the real image while img.src is a lazy-load placeholder.
    for match in re.finditer(r'\b(?:imgUrl|imageUrl|mainPic|pic|image)=([^&"\'\s<>]+)', text, flags=re.I):
        raw_value = urllib.parse.unquote(match.group(1))
        normalized = normalize_image_url(raw_value, source_url)
        if normalized and is_probable_product_image(normalized):
            records.append(
                {
                    "image_url": normalized,
                    "product_name": "",
                    "source_url": source_url,
                    "source_type": "card link parameter",
                }
            )

    deduped: list[dict[str, str]] = []
    seen: set[str] = set()
    for record in records:
        key = record["image_url"].split("?")[0]
        if key in seen:
            continue
        seen.add(key)
        deduped.append(record)
    return deduped


def extension_from_response(url: str, content_type: str | None) -> str:
    if content_type:
        guessed = mimetypes.guess_extension(content_type.split(";")[0].strip())
        if guessed:
            return ".jpg" if guessed == ".jpe" else guessed
    path = urllib.parse.urlparse(url).path.lower()
    for ext in (".jpg", ".jpeg", ".png", ".webp"):
        if path.endswith(ext):
            return ext
    return ".jpg"


def download_image(url: str, path_without_ext: Path, timeout: int, user_agent: str) -> tuple[str, str]:
    try:
        url = validate_public_http_url(url)
    except ValueError as exc:
        return "", str(exc)
    req = urllib.request.Request(url, headers={"User-Agent": user_agent, "Accept": "image/avif,image/webp,image/apng,image/*,*/*;q=0.8"})
    try:
        with urllib.request.build_opener(PublicOnlyRedirectHandler()).open(req, timeout=timeout) as resp:
            content_type = resp.headers.get("Content-Type", "")
            if content_type and "image" not in content_type.lower():
                return "", f"not image content-type: {content_type}"
            data = resp.read()
            if len(data) < 2048:
                return "", "image too small"
            size_note = inspect_image_size(data)
            if size_note:
                return "", size_note
            ext = extension_from_response(url, content_type)
            target = path_without_ext.with_suffix(ext)
            target.write_bytes(data)
            return str(target), ""
    except Exception as exc:  # noqa: BLE001 - command-line collector should record and continue.
        return "", str(exc)


def inspect_image_size(data: bytes) -> str:
    try:
        from PIL import Image
        import io

        with Image.open(io.BytesIO(data)) as img:
            width, height = img.size
        if width < 180 or height < 180:
            return f"image dimensions too small: {width}x{height}"
    except Exception:
        return ""
    return ""


def write_manifest(records: list[dict[str, str]], out_dir: Path) -> None:
    fields = [
        "category",
        "sub_category",
        "platform",
        "source_url",
        "source_type",
        "rank",
        "item_id",
        "item_url",
        "product_name",
        "title",
        "price",
        "price_num",
        "volume",
        "shop_name",
        "is_ad",
        "terms",
        "sort_selected",
        "price_label",
        "raw_text",
        "image_index",
        "image_url",
        "local_path",
        "status",
        "note",
        "collected_at",
    ]
    with (out_dir / "manifest.csv").open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for record in records:
            writer.writerow({field: record.get(field, "") for field in fields})
    (out_dir / "manifest.json").write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")


def write_contact_sheet(records: list[dict[str, str]], out_dir: Path) -> None:
    cards = []
    for record in records:
        if record.get("status") != "downloaded":
            continue
        rel = os.path.relpath(record["local_path"], out_dir).replace("\\", "/")
        title = html.escape(record.get("product_name") or f"rank {record.get('rank')}")
        note = html.escape(f"{record.get('platform')} · rank {record.get('rank')} · {record.get('source_type')}")
        cards.append(
            f'<figure><img src="{rel}" alt="{title}"><figcaption>{note}<br>{title}</figcaption></figure>'
        )
    page = f"""<!doctype html>
<html lang="zh-CN">
<meta charset="utf-8">
<title>Ecommerce main image contact sheet</title>
<style>
body{{font-family:Arial,'Microsoft YaHei',sans-serif;margin:24px;color:#17212b;background:#f7f8fa}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:16px}}
figure{{margin:0;padding:10px;background:#fff;border:1px solid #d8dee8;border-radius:8px}}
img{{width:100%;aspect-ratio:1/1;object-fit:contain;background:#f2f4f7}}
figcaption{{font-size:12px;line-height:1.5;margin-top:8px;word-break:break-all}}
</style>
<h1>Collected ecommerce main images</h1>
<p>{len(cards)} downloaded image candidates. Check manifest.csv for source URLs and status.</p>
<div class="grid">{''.join(cards)}</div>
</html>"""
    (out_dir / "contact_sheet.html").write_text(page, encoding="utf-8")


def build_sample_package(out_dir: Path, image_dir: Path, category: str, platform: str, sample_note: str) -> None:
    if not image_dir.exists() or not any(image_dir.iterdir()):
        return
    script_path = Path(__file__).with_name("build_sample_manifest.py")
    if not script_path.exists():
        return
    subprocess.run(
        [
            sys.executable,
            str(script_path),
            "--input",
            str(image_dir),
            "--output",
            str(out_dir / "outputs"),
            "--keyword",
            category,
            "--platform",
            platform,
            "--sample-note",
            sample_note,
        ],
        check=False,
    )


def enrich_sample_manifest(out_dir: Path, source_records: list[dict[str, str]]) -> None:
    sample_path = out_dir / "outputs" / "sample_manifest.csv"
    if not sample_path.exists():
        return
    with sample_path.open("r", encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        return

    by_rank: dict[str, dict[str, str]] = {}
    for record in source_records:
        if record.get("status") != "downloaded":
            continue
        rank = str(int(record.get("rank") or "0")) if str(record.get("rank") or "").isdigit() else str(record.get("rank") or "")
        by_rank[rank] = record

    extra_fields = [
        "product_name",
        "title",
        "price",
        "price_num",
        "volume",
        "shop_name",
        "item_id",
        "item_url",
        "source_url",
        "source_type",
        "image_url",
        "is_ad",
        "terms",
        "sort_selected",
        "price_label",
        "raw_text",
    ]
    fieldnames = list(rows[0].keys())
    for field in extra_fields:
        if field not in fieldnames:
            fieldnames.append(field)

    for row in rows:
        rank = str(int(row.get("rank") or "0")) if str(row.get("rank") or "").isdigit() else str(row.get("rank") or "")
        source = by_rank.get(rank)
        if not source:
            continue
        for field in extra_fields:
            if source.get(field):
                row[field] = source.get(field, "")

    with sample_path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def load_structured_products(path: Path) -> list[dict[str, str]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(payload, dict) and isinstance(payload.get("data"), dict):
        value = payload["data"].get("value")
        if isinstance(value, str):
            payload = json.loads(value)
    if isinstance(payload, list):
        products = payload
        meta: dict[str, object] = {}
    elif isinstance(payload, dict):
        products = payload.get("products", [])
        meta = payload
    else:
        return []
    if not isinstance(products, list):
        return []

    records: list[dict[str, str]] = []
    for index, product in enumerate(products, start=1):
        if not isinstance(product, dict):
            continue
        title = str(product.get("title") or product.get("product_name") or "").strip()
        records.append(
            {
                **{str(key): str(value) for key, value in product.items() if value is not None},
                "rank": str(product.get("rank") or index),
                "item_id": str(product.get("item_id") or ""),
                "item_url": str(product.get("item_url") or product.get("href") or ""),
                "product_name": title,
                "title": title,
                "image_url": str(product.get("image_url") or ""),
                "source_url": str(product.get("source_url") or meta.get("url") or ""),
                "source_type": str(
                    product.get("source_type")
                    or "Kimi WebBridge structured browser evidence; page-order sample"
                ),
                "sort_selected": str(product.get("sort_selected") or meta.get("sort_selected") or ""),
            }
        )
    return records


def has_product_evidence(record: dict[str, str]) -> bool:
    has_identity = bool(record.get("item_id") or record.get("item_url"))
    has_title = bool(record.get("title") or record.get("product_name"))
    return bool(record.get("image_url") and has_identity and has_title)


def load_source_list(path: str | None) -> list[str]:
    if not path:
        return []
    text = Path(path).read_text(encoding="utf-8")
    return [line.strip() for line in text.splitlines() if line.strip() and not line.strip().startswith("#")]


def main() -> int:
    parser = argparse.ArgumentParser(description="Collect public ecommerce main-image candidates by category.")
    parser.add_argument("--category", required=True, help="Category keyword, e.g. 牙膏")
    parser.add_argument("--platform", default="mixed", choices=["mixed", "jd", "taobao", "tmall", "pdd", "douyin"], help="Platform label/source preset")
    parser.add_argument("--sub-category", default="", help="Optional subcategory label")
    parser.add_argument("--source-url", action="append", default=[], help="Public ranking/search URL; repeatable")
    parser.add_argument("--source-list", help="Text file containing public source URLs")
    parser.add_argument("--html-dir", help="Directory of saved .html/.htm files to parse")
    parser.add_argument("--structured-json", action="append", default=[], help="Structured product JSON or Kimi WebBridge response; repeatable")
    parser.add_argument("--limit", type=int, default=30, help="Maximum downloaded image candidates")
    parser.add_argument("--images-per-product", type=int, default=1, help="Reserved for manifest compatibility; generic parser uses first N image candidates")
    parser.add_argument("--out", default="outputs/main-image-samples", help="Output root directory")
    parser.add_argument("--timeout", type=int, default=20, help="Network timeout seconds")
    parser.add_argument("--sleep", type=float, default=0.6, help="Delay between image downloads")
    parser.add_argument("--dry-run", action="store_true", help="Parse sources and write manifest without downloading images")
    parser.add_argument("--skip-sample-package", action="store_true", help="Do not build normalized_images/contact sheet/prompt after download")
    parser.add_argument("--user-agent", default="Mozilla/5.0 (compatible; CodexPublicImageCollector/1.0; no-login)", help="Plain public-fetch user agent")
    args = parser.parse_args()

    timestamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    run_slug = f"{timestamp}_{slugify(args.platform)}_{slugify(args.category)}"
    out_dir = Path(args.out) / run_slug
    image_dir = out_dir / "raw_images"
    image_dir.mkdir(parents=True, exist_ok=True)

    sources: list[tuple[str, str, str | None]] = []
    for url in args.source_url + load_source_list(args.source_list):
        sources.append((url, "user-provided public URL", None))
    if not sources and not args.html_dir and not args.structured_json:
        for url, source_type in build_candidate_urls(args.category, args.platform):
            sources.append((url, source_type, None))

    if args.html_dir:
        for path in sorted(Path(args.html_dir).glob("*.htm*")):
            sources.append((path.resolve().as_uri(), "saved HTML", str(path)))

    if not sources and not args.structured_json:
        print("No public source URLs, saved HTML, or structured JSON found. Provide --source-url, --html-dir, or --structured-json.", file=sys.stderr)
        return 2

    collected_at = dt.datetime.now(dt.timezone.utc).isoformat()
    manifest: list[dict[str, str]] = []
    candidates: list[dict[str, str]] = []

    for structured_path in args.structured_json:
        try:
            candidates.extend(load_structured_products(Path(structured_path)))
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            manifest.append(
                {
                    "category": args.category,
                    "sub_category": args.sub_category,
                    "platform": args.platform,
                    "source_url": str(structured_path),
                    "source_type": "structured JSON",
                    "status": "blocked",
                    "note": f"structured JSON error: {exc}",
                    "collected_at": collected_at,
                }
            )

    for source_url, source_type, local_html in sources:
        if local_html:
            text = Path(local_html).read_text(encoding="utf-8", errors="replace")
            error = None
        else:
            text, error = read_url(source_url, args.timeout, args.user_agent)
        if error:
            manifest.append(
                {
                    "category": args.category,
                    "sub_category": args.sub_category,
                    "platform": args.platform,
                    "source_url": source_url,
                    "source_type": source_type,
                    "rank": "",
                    "product_name": "",
                    "image_index": "",
                    "image_url": "",
                    "local_path": "",
                    "status": "blocked",
                    "note": error,
                    "collected_at": collected_at,
                }
            )
            continue
        if text and any(marker.lower() in text[:50000].lower() for marker in BLOCK_MARKERS):
            manifest.append(
                {
                    "category": args.category,
                    "sub_category": args.sub_category,
                    "platform": args.platform,
                    "source_url": source_url,
                    "source_type": source_type,
                    "rank": "",
                    "product_name": "",
                    "image_index": "",
                    "image_url": "",
                    "local_path": "",
                    "status": "blocked",
                    "note": "login/captcha/risk-control marker detected; no bypass attempted",
                    "collected_at": collected_at,
                }
            )
            continue
        product_cards = extract_product_cards(text or "", source_url, source_type)
        if product_cards:
            candidates.extend(product_cards)
        else:
            extracted = extract_images(text or "", source_url)
            for record in extracted:
                record["source_type"] = source_type if record.get("source_type") == "img tag" else f"{source_type}; {record.get('source_type')}"
            candidates.extend(extracted)

    seen_images: set[str] = set()
    seen_items: set[str] = set()
    rank = 0
    for candidate in candidates:
        if not has_product_evidence(candidate):
            manifest.append(
                {
                    "category": args.category,
                    "sub_category": args.sub_category,
                    "platform": args.platform,
                    "source_url": candidate.get("source_url", ""),
                    "source_type": candidate.get("source_type", ""),
                    "rank": "",
                    "product_name": candidate.get("product_name", ""),
                    "title": candidate.get("title", ""),
                    "image_index": "",
                    "image_url": candidate.get("image_url", ""),
                    "local_path": "",
                    "status": "insufficient_evidence",
                    "note": "image lacks product identity/title evidence; not counted as a ranking main-image sample",
                    "collected_at": collected_at,
                }
            )
            continue
        image_url = candidate.get("image_url", "")
        item_id = candidate.get("item_id", "")
        image_key = image_url.split("?")[0] if image_url else ""
        if item_id and item_id in seen_items:
            continue
        if image_key and image_key in seen_images:
            continue
        if item_id:
            seen_items.add(item_id)
        if image_key:
            seen_images.add(image_key)
        rank += 1
        product_name = candidate.get("product_name") or f"{args.category} product {rank}"
        base_name = f"{rank:03d}_{slugify(args.platform)}_{slugify(args.category)}_{slugify(product_name, 36)}"
        record = {
            "category": args.category,
            "sub_category": args.sub_category,
            "platform": args.platform,
            "source_url": candidate["source_url"],
            "source_type": candidate["source_type"],
            "rank": str(rank),
            "item_id": item_id,
            "item_url": candidate.get("item_url", ""),
            "product_name": product_name,
            "title": candidate.get("title", "") or product_name,
            "price": candidate.get("price", ""),
            "price_num": candidate.get("price_num", ""),
            "volume": candidate.get("volume", ""),
            "shop_name": candidate.get("shop_name", ""),
            "is_ad": candidate.get("is_ad", ""),
            "terms": candidate.get("terms", ""),
            "sort_selected": candidate.get("sort_selected", ""),
            "price_label": candidate.get("price_label", ""),
            "raw_text": candidate.get("raw_text", ""),
            "image_index": "1",
            "image_url": image_url,
            "local_path": "",
            "status": "parsed",
            "note": "",
            "collected_at": collected_at,
        }
        if not image_url:
            record["status"] = "parsed"
            record["note"] = "product card parsed without image_url"
        elif not args.dry_run:
            local_path, note = download_image(image_url, image_dir / base_name, args.timeout, args.user_agent)
            if local_path:
                record["local_path"] = local_path
                record["status"] = "downloaded"
            else:
                record["status"] = "skipped"
                record["note"] = note
            time.sleep(max(args.sleep, 0))
        manifest.append(record)
        if len([r for r in manifest if r.get("status") in ("downloaded", "parsed")]) >= args.limit:
            break

    write_manifest(manifest, out_dir)
    write_contact_sheet(manifest, out_dir)
    if not args.dry_run and not args.skip_sample_package:
        source_summary = "; ".join(sorted({r.get("source_type", "") for r in manifest if r.get("status") == "downloaded"}))
        sample_note = f"{platform_label(args.platform)} {args.category} public sample; route={source_summary or 'unknown'}; no login/cookie/captcha bypass."
        build_sample_package(out_dir, image_dir, args.category, platform_label(args.platform), sample_note)
        enrich_sample_manifest(out_dir, manifest)

    downloaded = len([r for r in manifest if r.get("status") == "downloaded"])
    parsed = len([r for r in manifest if r.get("status") == "parsed"])
    blocked = len([r for r in manifest if r.get("status") == "blocked"])
    skipped = len([r for r in manifest if r.get("status") == "skipped"])
    insufficient = len([r for r in manifest if r.get("status") == "insufficient_evidence"])
    print(f"Output: {out_dir}")
    print(f"downloaded={downloaded} parsed={parsed} blocked={blocked} skipped={skipped} insufficient_evidence={insufficient}")
    print(f"manifest={out_dir / 'manifest.csv'}")
    print(f"preview={out_dir / 'contact_sheet.html'}")
    if (out_dir / "outputs" / "sample_contact_sheet.jpg").exists():
        print(f"sample_contact_sheet={out_dir / 'outputs' / 'sample_contact_sheet.jpg'}")
    return 0 if downloaded or parsed else 1


def platform_label(platform: str) -> str:
    return {
        "jd": "京东",
        "taobao": "淘宝",
        "tmall": "天猫",
        "pdd": "拼多多",
        "douyin": "抖音",
        "mixed": "混合平台",
    }.get(platform, platform)


if __name__ == "__main__":
    raise SystemExit(main())
