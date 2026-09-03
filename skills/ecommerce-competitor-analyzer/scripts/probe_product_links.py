#!/usr/bin/env python3
"""Probe ecommerce product links and record whether public product data is extractable."""

from __future__ import annotations

import argparse
import csv
import html
import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


DESKTOP_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/125.0 Safari/537.36"
)
MOBILE_UA = (
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) "
    "AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148"
)


def item_id_from_url(url: str) -> str:
    parsed = urllib.parse.urlparse(url)
    query = urllib.parse.parse_qs(parsed.query)
    for key in ("id", "itemId", "item_id", "itemNumId"):
        if query.get(key):
            return query[key][0]
    match = re.search(r"(\d{8,})", url)
    return match.group(1) if match else ""


def platform_from_url(url: str) -> str:
    host = urllib.parse.urlparse(url).netloc.lower()
    if "tmall" in host:
        return "tmall"
    if "taobao" in host:
        return "taobao"
    if "jd." in host or "jd.com" in host:
        return "jd"
    if "yangkeduo" in host or "pinduoduo" in host:
        return "pdd"
    return "unknown"


def build_routes(url: str) -> list[tuple[str, str, str]]:
    platform = platform_from_url(url)
    item_id = item_id_from_url(url)
    routes = [("original", url, DESKTOP_UA)]
    if platform in {"tmall", "taobao"} and item_id:
        routes.extend(
            [
                ("taobao_h5", f"https://h5.m.taobao.com/awp/core/detail.htm?id={item_id}", MOBILE_UA),
                ("tmall_mobile", f"https://detail.m.tmall.com/item.htm?id={item_id}", MOBILE_UA),
                (
                    "taobao_detailskip",
                    f"https://detailskip.taobao.com/service/getData/1/p1/item/detail/sib.htm?itemId={item_id}",
                    MOBILE_UA,
                ),
            ]
        )
    return routes


def fetch(url: str, user_agent: str, timeout: int) -> dict:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": user_agent,
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            raw = response.read()
            content_type = response.headers.get("content-type", "")
            encoding = response.headers.get_content_charset() or "utf-8"
            text = raw.decode(encoding, errors="replace")
            return {
                "ok": True,
                "status": response.status,
                "final_url": response.geturl(),
                "content_type": content_type,
                "text": text,
                "bytes": len(raw),
            }
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace") if exc.fp else ""
        return {
            "ok": False,
            "status": exc.code,
            "final_url": url,
            "content_type": exc.headers.get("content-type", "") if exc.headers else "",
            "text": body,
            "bytes": len(body.encode("utf-8", errors="ignore")),
            "error": str(exc),
        }
    except Exception as exc:  # noqa: BLE001 - diagnostic script should record all failures.
        return {
            "ok": False,
            "status": "",
            "final_url": url,
            "content_type": "",
            "text": "",
            "bytes": 0,
            "error": str(exc),
        }


def strip_text(raw_html: str) -> str:
    text = re.sub(r"(?is)<script.*?</script>", " ", raw_html)
    text = re.sub(r"(?is)<style.*?</style>", " ", text)
    text = re.sub(r"(?s)<[^>]+>", " ", text)
    text = html.unescape(text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def extract_title(raw_html: str) -> str:
    match = re.search(r"(?is)<title[^>]*>(.*?)</title>", raw_html)
    if not match:
        return ""
    return re.sub(r"\s+", " ", html.unescape(match.group(1))).strip()


def extract_labels(raw_html: str) -> list[str]:
    labels = []
    for match in re.finditer(r'aria-label=(?:"([^"]+)"|([^\s>]+))', raw_html):
        labels.append(html.unescape(match.group(1) or match.group(2)).strip().strip('"'))
    for match in re.finditer(r"(?is)<span[^>]*>(.*?)</span>", raw_html):
        value = re.sub(r"(?s)<[^>]+>", "", match.group(1))
        value = re.sub(r"\s+", " ", html.unescape(value)).strip()
        if value:
            labels.append(value)
    seen = set()
    output = []
    for label in labels:
        if label not in seen:
            seen.add(label)
            output.append(label)
    return output


def classify(raw_html: str, visible_text: str, final_url: str, title: str) -> tuple[str, str]:
    combined = " ".join([raw_html[:10000], visible_text, final_url, title]).lower()
    if any(token in combined for token in ["login.taobao.com", "login.m.taobao.com", "havanaone/login", '"action": "login"']):
        return "blocked_login", "route returned a Taobao/Tmall login jump"
    if any(token in combined for token in ["rgv587_flag", "x5sec", "滑块", "验证码", "安全验证"]):
        return "blocked_security", "route returned risk-control or verification markers"

    labels = extract_labels(raw_html)
    label_text = " ".join(labels)
    weak_shell_terms = {"店铺", "客服", "收藏", "加入购物车", "立即购买"}
    has_only_shell = bool(labels) and set(labels).issubset(weak_shell_terms | {x for x in labels if x.startswith("立即购买")})
    has_product_signal = bool(re.search(r"(商品名称|宝贝标题|sku|库存|销量|月销|评价|价格|￥|¥)", visible_text + label_text, re.I))
    has_title = bool(title and title not in {"商品详情页", "登录"})

    if has_title and has_product_signal:
        return "extractable", "route contains title and product-like signals"
    if has_product_signal and not has_only_shell:
        return "partial_visible", "route contains partial product-like visible text"
    if title == "商品详情页" or has_only_shell:
        return "generic_shell", "route loaded a generic mobile detail shell without product facts"
    if visible_text:
        return "partial_visible", "route returned visible text, but product fields are incomplete"
    return "empty", "route returned no visible product text"


def probe_url(url: str, out_dir: Path, timeout: int) -> list[dict]:
    records = []
    platform = platform_from_url(url)
    item_id = item_id_from_url(url)
    for route_name, route_url, ua in build_routes(url):
        fetched = fetch(route_url, ua, timeout)
        raw_html = fetched.get("text", "")
        title = extract_title(raw_html)
        visible = strip_text(raw_html)
        labels = extract_labels(raw_html)
        status, note = classify(raw_html, visible, fetched.get("final_url", route_url), title)
        safe_id = item_id or re.sub(r"\W+", "_", url)[:40]
        html_path = out_dir / f"{safe_id}_{route_name}.html"
        html_path.write_text(raw_html, encoding="utf-8")
        records.append(
            {
                "input_url": url,
                "platform": platform,
                "item_id": item_id,
                "route": route_name,
                "route_url": route_url,
                "http_status": fetched.get("status", ""),
                "final_url": fetched.get("final_url", ""),
                "title": title,
                "probe_status": status,
                "note": fetched.get("error") or note,
                "bytes": fetched.get("bytes", 0),
                "labels": " | ".join(labels[:20]),
                "text_sample": visible[:500],
                "saved_html": str(html_path),
            }
        )
        time.sleep(0.2)
    return records


def main() -> None:
    parser = argparse.ArgumentParser(description="Probe ecommerce product URLs for publicly extractable evidence.")
    parser.add_argument("--url", action="append", required=True, help="Product URL. Pass multiple --url values.")
    parser.add_argument("--out", required=True, help="Output folder")
    parser.add_argument("--timeout", type=int, default=20, help="Request timeout in seconds")
    args = parser.parse_args()

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    all_records = []
    for url in args.url:
        all_records.extend(probe_url(url, out_dir, args.timeout))

    csv_path = out_dir / "link_probe.csv"
    json_path = out_dir / "link_probe.json"
    fields = [
        "input_url",
        "platform",
        "item_id",
        "route",
        "route_url",
        "http_status",
        "final_url",
        "title",
        "probe_status",
        "note",
        "bytes",
        "labels",
        "text_sample",
        "saved_html",
    ]
    with csv_path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(all_records)
    json_path.write_text(json.dumps(all_records, ensure_ascii=False, indent=2), encoding="utf-8")

    counts: dict[str, int] = {}
    for record in all_records:
        counts[record["probe_status"]] = counts.get(record["probe_status"], 0) + 1
    print(f"Wrote {csv_path}")
    print(f"Wrote {json_path}")
    print(json.dumps(counts, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
