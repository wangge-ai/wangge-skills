#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Validate structure and privacy before group reports are published."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


LOCAL_PATH = re.compile(r"(?i)(?:[a-z]:[\\/]|/users/[^/]+/|/home/[^/]+/)")
WECHAT_ID = re.compile(r"(?i)(?:wxid_[a-z0-9_-]+|\d+@chatroom)")
SECRET = re.compile(r"(?i)(?:sk-[a-z0-9_-]{16,}|bearer\s+[a-z0-9._-]{16,}|(?:api[_ -]?key|token)\s*[:=]\s*[a-z0-9._-]{16,})")
PHONE = re.compile(r"(?<!\d)1[3-9]\d{9}(?!\d)")
EMAIL = re.compile(r"(?i)\b[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}\b")
Q_HEADING = re.compile(r"(?m)^#{2,4}\s*Q(\d+)[:：]")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def privacy_findings(content: str, analysis: dict[str, Any], strict_names: bool) -> tuple[list[str], list[str]]:
    failures: list[str] = []
    warnings: list[str] = []
    group_name = str(analysis.get("group", {}).get("name") or "")
    scan_text = content.replace(group_name, "") if group_name else content

    patterns = (
        (LOCAL_PATH, "contains a local filesystem path"),
        (WECHAT_ID, "contains a WeChat/platform ID"),
        (SECRET, "contains a credential-like token"),
        (PHONE, "contains a possible mobile phone number"),
        (EMAIL, "contains a possible email address"),
    )
    for pattern, label in patterns:
        if pattern.search(scan_text):
            failures.append(label)

    for platform_id in analysis.get("platformIds", []):
        value = str(platform_id)
        if len(value) >= 6 and value in scan_text:
            failures.append(f"contains platform ID: {value[:4]}...")

    for name in analysis.get("memberNames", []):
        value = str(name).strip()
        if len(value) < 2 or value == group_name:
            continue
        if value in scan_text:
            warnings.append(f"contains possible member name: {value}")

    if strict_names and warnings:
        failures.extend(warnings)
    return sorted(set(failures)), sorted(set(warnings))


def structure_findings(internal: str, qa: str, incremental: bool) -> tuple[list[str], dict[str, Any]]:
    failures = []
    title_pattern = r"(?m)^#{1,2}\s+.+" if incremental else r"(?m)^#\s+.+"
    if not re.search(title_pattern, internal):
        failures.append("internal report has no valid title heading")
    if not re.search(title_pattern, qa):
        failures.append("Q&A report has no valid title heading")
    if len(internal.strip()) < 800:
        failures.append("internal report is too short for an evidence-backed analysis")
    if not re.search(r"\d{4}-\d{2}-\d{2}", internal):
        failures.append("internal report has no explicit analysis or update date")
    numbers = [int(value) for value in Q_HEADING.findall(qa)]
    if len(numbers) < 3:
        failures.append("Q&A report contains fewer than 3 numbered questions")
    if len(numbers) != len(set(numbers)):
        failures.append("Q&A report contains duplicate question numbers")
    if numbers and numbers != sorted(numbers):
        failures.append("Q&A question numbers are not in ascending order")
    return failures, {"questionCount": len(numbers), "firstQuestion": numbers[0] if numbers else None, "lastQuestion": numbers[-1] if numbers else None}


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate two group-report Markdown files")
    parser.add_argument("--analysis", required=True)
    parser.add_argument("--internal", required=True)
    parser.add_argument("--qa", required=True)
    parser.add_argument("--strict-names", action="store_true")
    parser.add_argument("--incremental", action="store_true", help="Allow H2 section fragments instead of full H1 documents")
    args = parser.parse_args()

    analysis = json.loads(read(Path(args.analysis)))
    internal = read(Path(args.internal))
    qa = read(Path(args.qa))
    structure_failures, metrics = structure_findings(internal, qa, args.incremental)
    internal_failures, internal_warnings = privacy_findings(internal, analysis, args.strict_names)
    qa_failures, qa_warnings = privacy_findings(qa, analysis, args.strict_names)
    failures = structure_failures + internal_failures + qa_failures
    payload = {
        "ok": not failures,
        "structure": metrics,
        "failures": failures,
        "warnings": sorted(set(internal_warnings + qa_warnings)),
        "strictNames": args.strict_names,
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    raise SystemExit(0 if payload["ok"] else 2)


if __name__ == "__main__":
    main()
