from __future__ import annotations

import argparse
import datetime as dt
import json
import re
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit


URL_RE = re.compile(r"https?://[^\s<>\"'）】]+", re.IGNORECASE)
URL_FIELDS = ("resolved_url", "resolvedUrl", "canonical_url", "url", "href", "link", "source_url")


def read_input(path: Path) -> list[object]:
    text = path.read_text(encoding="utf-8-sig")
    if path.suffix.lower() == ".jsonl":
        return [json.loads(line) for line in text.splitlines() if line.strip()]
    data = json.loads(text)
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        for key in ("items", "links", "records", "documents"):
            if isinstance(data.get(key), list):
                return data[key]
        return [data]
    raise ValueError("Input must be a JSON array/object or JSONL records")


def extract_url(record: object) -> str:
    if isinstance(record, str):
        match = URL_RE.search(record)
        return match.group(0) if match else ""
    if not isinstance(record, dict):
        return ""
    for field in URL_FIELDS:
        value = record.get(field)
        if isinstance(value, str) and value.startswith(("http://", "https://")):
            return value
    for field in ("text", "content", "context", "message"):
        value = record.get(field)
        if isinstance(value, str):
            match = URL_RE.search(value)
            if match:
                return match.group(0)
    return ""


def canonicalize(value: str) -> tuple[str, str]:
    value = value.strip().rstrip(".,;!?，。；！？")
    parsed = urlsplit(value)
    host = parsed.hostname.lower() if parsed.hostname else ""
    if parsed.port:
        host += f":{parsed.port}"
    # Paths and business query values can distinguish articles and product IDs.
    # Remove credentials and tracking, rather than merging every /s or item.htm URL.
    path = parsed.path or "/"
    private = {"token", "access_token", "auth", "authorization", "cookie", "password", "session", "sessionid", "sid"}
    tracking = {"fbclid", "gclid", "from", "isappinstalled"}
    query = sorted((key, val) for key, val in parse_qsl(parsed.query, keep_blank_values=True)
                   if key.lower() not in private | tracking and not key.lower().startswith("utm_"))
    canonical = urlunsplit((parsed.scheme.lower() or "https", host, path, urlencode(query), ""))
    return canonical, canonical


def classify(url: str) -> str:
    parsed = urlsplit(url)
    host, path = parsed.netloc.lower(), parsed.path.lower()
    if host.endswith(("feishu.cn", "larksuite.com")):
        if "/wiki/" in path:
            return "feishu-wiki"
        if "/docx/" in path or "/docs/" in path:
            return "feishu-doc"
        if "/base/" in path:
            return "feishu-base"
        return "feishu-other"
    if host == "mp.weixin.qq.com" and path.startswith("/s"):
        return "wechat-article"
    if host.endswith(("taobao.com", "tmall.com")):
        return "taobao-tmall"
    if host.endswith("jd.com"):
        return "jd"
    if host.endswith("pinduoduo.com"):
        return "pinduoduo"
    if host.endswith("xiaohongshu.com"):
        return "xiaohongshu"
    return "web"


def compact_context(record: object) -> dict:
    if not isinstance(record, dict):
        return {}
    result = {}
    for key in ("title", "context_title", "author", "topic_id", "source_topic_id", "source_page_url", "position"):
        value = record.get(key)
        if isinstance(value, (str, int, float)) and str(value).strip():
            if key == "source_page_url" and isinstance(value, str):
                value = canonicalize(value)[0]
            result[key] = value
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Normalize and deduplicate a browser-discovered link queue.")
    parser.add_argument("input")
    parser.add_argument("output")
    parser.add_argument("--kind", default="", help="Keep only one classified kind, for example feishu-wiki.")
    args = parser.parse_args()

    input_path = Path(args.input).resolve()
    output_path = Path(args.output).resolve()
    raw = read_input(input_path)
    items = []
    duplicate_rows = []
    invalid_rows = []
    seen: dict[str, int] = {}
    for raw_index, record in enumerate(raw, start=1):
        found = extract_url(record)
        if not found:
            invalid_rows.append({"input_index": raw_index, "reason": "no_http_url"})
            continue
        canonical, key = canonicalize(found)
        kind = classify(canonical)
        if args.kind and kind != args.kind:
            continue
        if key in seen:
            duplicate_rows.append({"input_index": raw_index, "duplicate_of": seen[key], "canonical_url": canonical})
            continue
        sequence = len(items) + 1
        seen[key] = sequence
        context = compact_context(record)
        items.append(
            {
                "id": f"link-{sequence:04d}",
                "sequence": sequence,
                "discovered_url": canonical,
                "canonical_url": canonical,
                "kind": kind,
                "context": context,
                "status": "pending",
                "attempts": 0,
                "resolved_url": "",
                "output_root": "",
                "failure_reason": "",
            }
        )

    output = {
        "schema": "web-collection-link-queue/v1",
        "generated_at": dt.datetime.now().astimezone().isoformat(),
        "input_file": str(input_path),
        "counts": {"raw": len(raw), "unique": len(items), "duplicates": len(duplicate_rows), "invalid": len(invalid_rows)},
        "items": items,
        "duplicates": duplicate_rows,
        "invalid": invalid_rows,
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"output": str(output_path), **output["counts"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
