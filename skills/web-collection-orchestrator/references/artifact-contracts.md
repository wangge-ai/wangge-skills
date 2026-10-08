# Artifact contracts

## Discovery JSONL record

Write one UTF-8 JSON object per discovered source item:

```json
{
  "source_page_url": "https://example.com/feed",
  "topic_id": "stable-source-id",
  "position": 17,
  "title": "visible context title",
  "author": "visible author",
  "url": "https://example.feishu.cn/wiki/document-token",
  "expanded": true,
  "collected_at": "2026-08-20T12:34:56+08:00"
}
```

Do not store cookies, request headers, access tokens, local storage, or session-bearing query strings.

## Link queue

`normalize_link_queue.py` produces `web-collection-link-queue/v1`. Update these fields in place after each attempt:

```json
{
  "id": "link-0001",
  "sequence": 1,
  "discovered_url": "original visible URL",
  "canonical_url": "query-free URL",
  "resolved_url": "final browser URL",
  "kind": "feishu-wiki",
  "status": "pending|collecting|verified|failed|skipped_duplicate",
  "attempts": 0,
  "output_root": "",
  "failure_reason": ""
}
```

## Per-document JSON

Keep at least:

```json
{
  "index": 1,
  "title": "document title",
  "author": "visible author",
  "source_url": "discovered URL",
  "resolved_url": "final URL",
  "source_topic_id": "source feed item",
  "collected_at": "ISO-8601",
  "block_count": 120,
  "textLength": 9000,
  "imageCount": 12,
  "text": "plain text",
  "html_file": "html/001-title.html",
  "local_assets": {
    "source-asset-id": "assets/001/file.png"
  },
  "status": "verified"
}
```

## Final manifest

Record:

- discovery raw count;
- collected success, failed, and skipped counts;
- within-batch and cross-batch duplicates;
- unique union;
- per-document source URL, resolved URL, source identity, HTML, Markdown, assets, status, and failure reason;
- actual resource count and bytes;
- deliverable filenames, bytes, SHA-256, template count, and embedded asset count;
- first-open, representative-document, console, and mobile QA results.

Counts in the manifest are authoritative. User estimates are targets to investigate, not values to force.
