#!/usr/bin/env python3
"""Normalize RPA run logs and surface replay and unfinished-RUN candidates.

Accepted input is CSV/TSV, JSON Lines, or plain text. Output is JSON and never
modifies the source. Item identifiers are taken only from explicit safe fields
or sequence-number patterns; credentials should be redacted before use.
"""

from __future__ import annotations

import argparse
import csv
import io
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable


TIME_KEYS = ("timestamp", "time", "datetime", "时间")
MESSAGE_KEYS = ("message", "content", "msg", "log", "内容")
ITEM_KEYS = ("item_seq", "shop_seq", "item_id", "safe_item_id", "店铺序号")
PASS_KEYS = ("pass", "batch_pass", "retry_pass", "补跑轮次")
STATUS_KEYS = ("status", "state", "状态")
STAGE_KEYS = ("stage", "阶段")
EVENT_KEYS = ("event", "事件")
ERROR_KEYS = ("error_code", "error", "code", "错误码")

ITEM_PATTERNS = (
    re.compile(r"(?:item_seq|shop_seq|item|店铺序号)\s*[=:]\s*([A-Za-z0-9_.-]+)", re.I),
)
PASS_PATTERN = re.compile(r"(?:batch_pass|retry_pass|pass|补跑轮次)\s*[=:]\s*(\d+(?:/\d+)?)", re.I)
STATUS_PATTERN = re.compile(
    r"(?:status|state|状态)\s*[=:]\s*"
    r"(RUN|SKIP|RETRY|START|SUCCESS|NO_DATA|FAILED|CAPTCHA_FAILED|CREDENTIAL_FAILED|RUNNING)",
    re.I,
)
ERROR_PATTERN = re.compile(r"(?:error_code|error|code|错误码)\s*[=:]\s*([A-Za-z0-9_.-]+)", re.I)
STAGE_PATTERN = re.compile(r"(?:stage|阶段)\s*[=:]\s*([A-Za-z0-9_.-]+)", re.I)
EVENT_PATTERN = re.compile(r"(?:event|事件)\s*[=:]\s*([A-Za-z0-9_.-]+)", re.I)

TERMINAL_INVOCATION_STATUSES = {
    "SKIP",
    "SUCCESS",
    "NO_DATA",
    "FAILED",
    "CAPTCHA_FAILED",
    "CREDENTIAL_FAILED",
}


def _read_text(path: Path) -> str:
    last_error: UnicodeDecodeError | None = None
    for encoding in ("utf-8-sig", "utf-8", "gb18030"):
        try:
            return path.read_text(encoding=encoding)
        except UnicodeDecodeError as exc:
            last_error = exc
    assert last_error is not None
    raise last_error


def _first(mapping: dict[str, Any], keys: Iterable[str]) -> Any:
    lowered = {str(key).strip().lower(): value for key, value in mapping.items()}
    for key in keys:
        value = lowered.get(key.lower())
        if value not in (None, ""):
            return value
    return None


def _extract(pattern: re.Pattern[str], text: str) -> str | None:
    match = pattern.search(text)
    return match.group(1) if match else None


def normalize_record(record: dict[str, Any], line_no: int) -> dict[str, Any]:
    message_value = _first(record, MESSAGE_KEYS)
    message = str(message_value if message_value is not None else "").strip()
    if not message:
        message = " ".join(
            str(value).strip() for value in record.values() if value not in (None, "")
        )

    item = _first(record, ITEM_KEYS)
    if item is None:
        for pattern in ITEM_PATTERNS:
            item = _extract(pattern, message)
            if item is not None:
                break

    pass_value = _first(record, PASS_KEYS)
    if pass_value is None:
        pass_value = _extract(PASS_PATTERN, message)

    status_value = _first(record, STATUS_KEYS)
    if status_value is None:
        status_value = _extract(STATUS_PATTERN, message)
    status = str(status_value).strip().upper() if status_value not in (None, "") else None

    error_value = _first(record, ERROR_KEYS)
    if error_value is None:
        error_value = _extract(ERROR_PATTERN, message)

    stage_value = _first(record, STAGE_KEYS)
    if stage_value is None:
        stage_value = _extract(STAGE_PATTERN, message)
    event_value = _first(record, EVENT_KEYS)
    if event_value is None:
        event_value = _extract(EVENT_PATTERN, message)

    return {
        "line": line_no,
        "timestamp": _first(record, TIME_KEYS),
        "item": str(item).strip() if item not in (None, "") else None,
        "pass": str(pass_value).strip() if pass_value not in (None, "") else None,
        "status": status,
        "stage": str(stage_value).strip() if stage_value not in (None, "") else None,
        "event": str(event_value).strip() if event_value not in (None, "") else None,
        "error_code": str(error_value).strip() if error_value not in (None, "") else None,
        "message": message,
    }


def parse_jsonl(text: str) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for line_no, line in enumerate(text.splitlines(), 1):
        if not line.strip():
            continue
        value = json.loads(line)
        if not isinstance(value, dict):
            raise ValueError(f"JSONL line {line_no} is not an object")
        records.append(normalize_record(value, line_no))
    return records


def parse_delimited(text: str) -> list[dict[str, Any]]:
    sample = text[:4096]
    try:
        dialect = csv.Sniffer().sniff(sample, delimiters=",\t;")
    except csv.Error:
        dialect = csv.excel
    reader = csv.DictReader(io.StringIO(text), dialect=dialect)
    if not reader.fieldnames:
        raise ValueError("Delimited log has no header")
    return [normalize_record(dict(row), line_no) for line_no, row in enumerate(reader, 2)]


def parse_text(text: str) -> list[dict[str, Any]]:
    return [
        normalize_record({"message": line.strip()}, line_no)
        for line_no, line in enumerate(text.splitlines(), 1)
        if line.strip()
    ]


def parse_log(path: Path, input_format: str = "auto") -> list[dict[str, Any]]:
    text = _read_text(path)
    chosen = input_format
    if chosen == "auto":
        suffix = path.suffix.lower()
        first = next((line.lstrip() for line in text.splitlines() if line.strip()), "")
        if suffix in {".jsonl", ".ndjson"} or first.startswith("{"):
            chosen = "jsonl"
        elif suffix in {".csv", ".tsv"}:
            chosen = "csv"
        else:
            chosen = "text"
    if chosen == "jsonl":
        return parse_jsonl(text)
    if chosen == "csv":
        return parse_delimited(text)
    return parse_text(text)


def summarize(records: list[dict[str, Any]]) -> dict[str, Any]:
    status_counts = Counter(record["status"] for record in records if record["status"])
    pass_counts = Counter(record["pass"] for record in records if record["pass"])
    item_events: dict[str, list[dict[str, Any]]] = defaultdict(list)
    batch_events: list[dict[str, Any]] = []
    for record in records:
        compact = {key: value for key, value in record.items() if value not in (None, "")}
        if record["item"] is None:
            batch_events.append(compact)
        else:
            item_events[record["item"]].append(compact)

    open_run_candidates: list[dict[str, Any]] = []
    items: dict[str, Any] = {}
    for item, events in item_events.items():
        statuses = [event.get("status") for event in events if event.get("status")]
        last_status = statuses[-1] if statuses else None
        if last_status in {"RUN", "RUNNING"}:
            open_run_candidates.append(
                {
                    "item": item,
                    "last_status": last_status,
                    "last_line": events[-1]["line"],
                    "reason": "last observed status is non-terminal; confirm against the state file",
                }
            )
        items[item] = {
            "last_status": last_status,
            "has_terminal_observation": any(
                status in TERMINAL_INVOCATION_STATUSES for status in statuses
            ),
            "events": events,
        }

    return {
        "record_count": len(records),
        "item_count": len(items),
        "status_counts": dict(sorted(status_counts.items())),
        "pass_counts": dict(sorted(pass_counts.items())),
        "open_run_candidates": open_run_candidates,
        "batch_events": batch_events,
        "items": items,
        "notes": [
            "An open RUN is a candidate, not proof of stale state; reconcile it with state and artifacts.",
            "SKIP describes this invocation and must be interpreted using the project's terminal-state policy.",
        ],
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("log", type=Path)
    parser.add_argument("--format", choices=("auto", "csv", "jsonl", "text"), default="auto")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--indent", type=int, default=2)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    result = summarize(parse_log(args.log, args.format))
    rendered = json.dumps(result, ensure_ascii=False, indent=args.indent)
    if args.output:
        args.output.write_text(rendered + "\n", encoding="utf-8")
    else:
        print(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
