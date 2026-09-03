#!/usr/bin/env python3
"""Audit an RPA JSON state file without changing it."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterator


LEGAL_STATUSES = {
    "pending",
    "success",
    "no_data",
    "running",
    "captcha_failed",
    "login_failed",
    "failed",
    "credential_failed",
    "interrupted",
}
TERMINAL_STATUSES = {"success", "no_data"}
ARTIFACT_KEYS = ("artifact", "artifact_path", "output_file", "file")
UPDATED_KEYS = ("updated_at", "updated", "timestamp", "time")


def _walk(value: Any, path: tuple[str, ...] = ()) -> Iterator[tuple[tuple[str, ...], dict[str, Any]]]:
    if isinstance(value, dict):
        if "status" in value:
            yield path, value
        for key, child in value.items():
            yield from _walk(child, path + (str(key),))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from _walk(child, path + (str(index),))


def _safe_record_id(record: dict[str, Any], index: int) -> str:
    for key in ("safe_item_id", "item_seq", "shop_seq"):
        if record.get(key) not in (None, ""):
            return str(record[key])
    return f"item_{index:03d}"


def _path_hash(path: tuple[str, ...]) -> str:
    return hashlib.sha256("/".join(path).encode("utf-8")).hexdigest()[:12]


def _parse_time(value: Any) -> datetime | None:
    if value in (None, ""):
        return None
    text = str(value).strip().replace("Z", "+00:00")
    try:
        parsed = datetime.fromisoformat(text)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def _artifact_value(record: dict[str, Any]) -> str | None:
    for key in ARTIFACT_KEYS:
        value = record.get(key)
        if value not in (None, ""):
            return str(value)
    return None


def _updated_value(record: dict[str, Any]) -> Any:
    for key in UPDATED_KEYS:
        if record.get(key) not in (None, ""):
            return record[key]
    return None


def audit_state(
    data: Any,
    *,
    artifact_root: Path | None = None,
    stale_minutes: float = 30.0,
    now: datetime | None = None,
) -> dict[str, Any]:
    current = now or datetime.now(timezone.utc)
    if current.tzinfo is None:
        current = current.replace(tzinfo=timezone.utc)
    current = current.astimezone(timezone.utc)

    issues: list[dict[str, Any]] = []
    statuses: Counter[str] = Counter()
    records = list(_walk(data))
    composite_keys: dict[str, list[str]] = {}

    for index, (path, record) in enumerate(records, 1):
        record_id = _safe_record_id(record, index)
        location = _path_hash(path)
        raw_status = record.get("status")
        status = str(raw_status).strip().lower() if raw_status not in (None, "") else ""
        statuses[status or "<missing>"] += 1

        def add(code: str, severity: str, message: str) -> None:
            issues.append(
                {
                    "record_id": record_id,
                    "path_hash": location,
                    "code": code,
                    "severity": severity,
                    "message": message,
                }
            )

        if not status:
            add("missing_status", "error", "record has no status")
            continue
        if status not in LEGAL_STATUSES:
            add("illegal_status", "error", f"unsupported status: {status}")

        updated_raw = _updated_value(record)
        updated = _parse_time(updated_raw)
        if status == "running":
            if updated is None:
                add("running_without_time", "warning", "running record has no parseable update time")
            else:
                age_minutes = (current - updated).total_seconds() / 60
                if age_minutes > stale_minutes:
                    add(
                        "stale_running",
                        "error",
                        f"running record is {age_minutes:.1f} minutes old (limit {stale_minutes:g})",
                    )

        artifact = _artifact_value(record)
        if status == "success" and not artifact:
            add("success_without_artifact", "error", "success record has no artifact path")
        if status == "success" and artifact:
            artifact_path = Path(artifact)
            if not artifact_path.is_absolute() and artifact_root is not None:
                artifact_path = artifact_root / artifact_path
            if (artifact_path.is_absolute() or artifact_root is not None) and not artifact_path.exists():
                add("artifact_missing", "error", "success artifact does not exist at the resolved path")

        task_key = record.get("task_key")
        item_key = next(
            (
                record.get(key)
                for key in ("item_key", "safe_item_id", "item_seq", "shop_seq")
                if record.get(key) not in (None, "")
            ),
            None,
        )
        if task_key not in (None, "") and item_key not in (None, ""):
            canonical = json.dumps(
                {"task_key": task_key, "item_key": item_key},
                ensure_ascii=False,
                sort_keys=True,
            )
            composite_keys.setdefault(canonical, []).append(record_id)

        if status in TERMINAL_STATUSES and record.get("error_code"):
            add("terminal_with_error", "warning", "terminal record still carries an error_code")

    for ids in composite_keys.values():
        if len(ids) > 1:
            issues.append(
                {
                    "record_id": ",".join(ids),
                    "path_hash": None,
                    "code": "duplicate_task_item_key",
                    "severity": "warning",
                    "message": "multiple records share the same explicit task_key + item_key",
                }
            )

    errors = sum(issue["severity"] == "error" for issue in issues)
    warnings = sum(issue["severity"] == "warning" for issue in issues)
    return {
        "ok": errors == 0,
        "record_count": len(records),
        "status_counts": dict(sorted(statuses.items())),
        "error_count": errors,
        "warning_count": warnings,
        "issues": issues,
        "notes": [
            "Dictionary keys are not emitted; path_hash supports correlation without exposing account names.",
            "A success artifact is checked only when its path can be resolved safely.",
        ],
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("state", type=Path)
    parser.add_argument("--artifact-root", type=Path)
    parser.add_argument("--stale-minutes", type=float, default=30.0)
    parser.add_argument("--now", help="ISO-8601 timestamp; useful for deterministic audits")
    parser.add_argument("--output", type=Path)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        data = json.loads(args.state.read_text(encoding="utf-8-sig"))
        now = _parse_time(args.now) if args.now else None
        if args.now and now is None:
            raise ValueError("--now is not a valid ISO-8601 timestamp")
        result = audit_state(
            data,
            artifact_root=args.artifact_root,
            stale_minutes=args.stale_minutes,
            now=now,
        )
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(json.dumps({"ok": False, "fatal": str(exc)}, ensure_ascii=False, indent=2))
        return 2
    rendered = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        args.output.write_text(rendered + "\n", encoding="utf-8")
    else:
        print(rendered)
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
