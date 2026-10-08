#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build a privacy-safe local HTML review dashboard from group evidence and insight clusters."""

from __future__ import annotations

import argparse
import json
import re
from collections import OrderedDict
from pathlib import Path
from typing import Any


LOCAL_PATH = re.compile(r"(?i)(?:(?<![a-z])[a-z]:[\\/]|/users/[^/]+/|/home/[^/]+/)[^\s<>\"']*")
WECHAT_ID = re.compile(r"(?i)(?:wxid_[a-z0-9_-]+|gh_[a-z0-9_-]{6,}|\d+@chatroom)")
SECRET = re.compile(r"(?i)(?:sk-[a-z0-9_-]{12,}|bearer\s+[a-z0-9._-]{12,}|(?:api[_ -]?key|token)\s*[:=]\s*[a-z0-9._-]{12,})")
OPAQUE_ID = re.compile(r"(?i)\b[a-f0-9]{24,}\b")
PHONE = re.compile(r"(?<!\d)1[3-9]\d{9}(?!\d)")
EMAIL = re.compile(r"(?i)\b[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}\b")

ALLOWED_KINDS = {"question", "method", "case", "risk", "resource", "trend", "decision"}
ALLOWED_IMPORTANCE = {"high", "medium", "low"}
ALLOWED_CANDIDATES = {"none", "insight", "qa"}


def read_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(data, dict):
        raise ValueError(f"JSON root must be an object: {path}")
    return data


def text(value: Any, default: str = "") -> str:
    return str(value if value not in (None, "") else default).strip()


def integer(value: Any, default: int = 0) -> int:
    try:
        return max(0, int(value))
    except (TypeError, ValueError):
        return default


def redact(value: Any, analysis: dict[str, Any]) -> str:
    result = text(value)
    if "[引用" in result and len(result) > 240:
        result = result.split("[引用", 1)[0].rstrip() + " [引用内容已折叠]"
    result = re.sub(r"<[^>]{1,200}>", " ", result)
    for member_name in sorted((text(item) for item in analysis.get("memberNames", [])), key=len, reverse=True):
        if len(member_name) >= 2:
            result = result.replace(member_name, "[成员]")
    for platform_id in sorted((text(item) for item in analysis.get("platformIds", [])), key=len, reverse=True):
        if len(platform_id) >= 4:
            result = result.replace(platform_id, "[平台ID]")
    for pattern, replacement in (
        (LOCAL_PATH, "[本地路径]"),
        (WECHAT_ID, "[平台ID]"),
        (SECRET, "[凭据]"),
        (OPAQUE_ID, "[长标识符]"),
        (PHONE, "[手机号]"),
        (EMAIL, "[邮箱]"),
    ):
        result = pattern.sub(replacement, result)
    result = re.sub(r"\s+", " ", result).strip()
    return result if len(result) <= 360 else result[:357].rstrip() + "..."


def collect_evidence(analysis: dict[str, Any]) -> OrderedDict[str, dict[str, Any]]:
    records: OrderedDict[str, dict[str, Any]] = OrderedDict()
    pools: list[Any] = [analysis.get("questions", []), analysis.get("evidence", [])]
    pools.extend(analysis.get("topicEvidence", {}).values())
    fallback_number = 0
    speaker_aliases: dict[str, str] = {}

    for pool in pools:
        if not isinstance(pool, list):
            continue
        for row in pool:
            if not isinstance(row, dict):
                continue
            fallback_number += 1
            reference = text(row.get("ref"), f"E{fallback_number:06d}")
            if reference in records:
                continue
            speaker = text(row.get("speaker"), "未知成员")
            if speaker not in speaker_aliases:
                speaker_aliases[speaker] = f"成员{len(speaker_aliases) + 1:02d}"
            time_value = text(row.get("time"), "未知时间")
            records[reference] = {
                "ref": reference,
                "time": time_value,
                "date": time_value[:10] if re.match(r"^\d{4}-\d{2}-\d{2}", time_value) else "",
                "speaker": speaker_aliases[speaker],
                "type": text(row.get("type"), "unknown"),
                "text": redact(row.get("text"), analysis),
                "topics": [text(item) for item in row.get("topics", []) if text(item)],
                "question": bool(row.get("question")),
            }
    return records


def normalize_daily(analysis: dict[str, Any]) -> list[dict[str, Any]]:
    selected = analysis.get("selected", {})
    details = selected.get("dailyDetails")
    if isinstance(details, list) and details:
        result = []
        for row in details:
            if not isinstance(row, dict) or not text(row.get("date")):
                continue
            result.append({
                "date": text(row.get("date")),
                "messages": integer(row.get("effectiveMessages")),
                "questions": integer(row.get("questionLike")),
                "speakers": integer(row.get("activeSpeakers")),
                "topics": [[text(pair[0]), integer(pair[1])] for pair in row.get("topicCounts", []) if isinstance(pair, list) and len(pair) >= 2],
            })
        return sorted(result, key=lambda item: item["date"])

    return [
        {"date": text(pair[0]), "messages": integer(pair[1]), "questions": 0, "speakers": 0, "topics": []}
        for pair in selected.get("daily", [])
        if isinstance(pair, list) and len(pair) >= 2
    ]


def normalize_insights(
    raw: dict[str, Any], analysis: dict[str, Any], evidence: OrderedDict[str, dict[str, Any]]
) -> tuple[list[dict[str, Any]], list[str]]:
    source = raw.get("insights")
    if not isinstance(source, list):
        raise ValueError("Insight index must contain an 'insights' array")
    normalized: list[dict[str, Any]] = []
    warnings: list[str] = []
    seen_ids: set[str] = set()

    for position, item in enumerate(source, 1):
        if not isinstance(item, dict):
            warnings.append(f"Skipped non-object insight at position {position}")
            continue
        insight_id = text(item.get("id"), f"I{position:03d}")
        if insight_id in seen_ids:
            raise ValueError(f"Duplicate insight id: {insight_id}")
        seen_ids.add(insight_id)
        title = redact(item.get("title"), analysis)
        if not title:
            warnings.append(f"Skipped insight without title: {insight_id}")
            continue
        kind = text(item.get("kind"), "trend").lower()
        if kind not in ALLOWED_KINDS:
            kind = "trend"
        importance = text(item.get("importance"), "medium").lower()
        if importance not in ALLOWED_IMPORTANCE:
            importance = "medium"
        candidate = text(item.get("candidate"), "none").lower()
        if candidate not in ALLOWED_CANDIDATES:
            candidate = "none"

        refs = []
        for reference in item.get("evidenceRefs", []):
            key = text(reference)
            if key in evidence and key not in refs:
                refs.append(key)
            elif key:
                warnings.append(f"{insight_id} references missing evidence: {key}")
        evidence_rows = [evidence[key] for key in refs]
        dates = sorted({text(value) for value in item.get("dates", []) if text(value)})
        if not dates:
            dates = sorted({row["date"] for row in evidence_rows if row["date"]})
        topics = [redact(value, analysis) for value in item.get("topics", []) if text(value)]
        factors = item.get("importanceFactors") if isinstance(item.get("importanceFactors"), dict) else {}
        boundaries = [redact(value, analysis) for value in item.get("boundaries", []) if text(value)]
        if not evidence_rows:
            boundaries.append("当前线索未连接到可回查的证据序号")

        normalized.append({
            "id": insight_id,
            "title": title,
            "summary": redact(item.get("summary"), analysis),
            "kind": kind,
            "importance": importance,
            "candidate": candidate,
            "status": redact(item.get("status"), analysis) or "待判断",
            "action": redact(item.get("action"), analysis),
            "topics": topics,
            "dates": dates,
            "factors": {
                "repeatCount": integer(factors.get("repeatCount")),
                "speakerCount": integer(factors.get("speakerCount")),
                "crossDayCount": integer(factors.get("crossDayCount")),
                "unresolved": bool(factors.get("unresolved")),
                "actionability": text(factors.get("actionability"), "medium").lower(),
                "reason": redact(factors.get("reason"), analysis),
            },
            "boundaries": list(dict.fromkeys(boundaries)),
            "evidence": evidence_rows,
        })

    importance_order = {"high": 0, "medium": 1, "low": 2}
    normalized.sort(key=lambda item: (importance_order[item["importance"]], -item["factors"]["repeatCount"], item["id"]))
    return normalized, warnings


def build_payload(analysis: dict[str, Any], raw_insights: dict[str, Any]) -> dict[str, Any]:
    evidence = collect_evidence(analysis)
    insights, warnings = normalize_insights(raw_insights, analysis, evidence)
    selected = analysis.get("selected", {})
    media = analysis.get("media", {})
    group_name = text(analysis.get("group", {}).get("name"), "未命名群聊")
    return {
        "schemaVersion": 1,
        "group": group_name,
        "generatedAt": text(analysis.get("generatedAt")),
        "range": {"start": text(selected.get("dateStart")), "end": text(selected.get("dateEnd"))},
        "summary": {
            "messages": integer(selected.get("effectiveMessages")),
            "questions": integer(selected.get("questionLike")),
            "speakers": integer(selected.get("activeSpeakers")),
            "topFiveShare": float(selected.get("topFiveShare") or 0),
            "topics": [[text(pair[0]), integer(pair[1])] for pair in selected.get("topicCounts", []) if isinstance(pair, list) and len(pair) >= 2],
        },
        "media": {
            "voiceRecords": integer(media.get("voiceMessageRecords")),
            "voiceFiles": integer(media.get("voiceFiles")),
            "coverageWarning": bool(media.get("voiceCoverageWarning")),
        },
        "daily": normalize_daily(analysis),
        "insights": insights,
        "warnings": list(dict.fromkeys(warnings)),
    }


def build_html(payload: dict[str, Any], template_path: Path) -> str:
    template = template_path.read_text(encoding="utf-8")
    placeholder = "__GROUP_INSIGHT_DASHBOARD_DATA__"
    if placeholder not in template:
        raise ValueError(f"Dashboard template is missing placeholder: {placeholder}")
    encoded = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    return template.replace(placeholder, encoded)


def main() -> None:
    parser = argparse.ArgumentParser(description="Build the local group insight review dashboard")
    parser.add_argument("--analysis", required=True, help="Path to group_analysis.json")
    parser.add_argument("--insights", required=True, help="Path to insight_index.json")
    parser.add_argument("--output", required=True, help="Output standalone HTML path")
    parser.add_argument("--template", help="Optional dashboard template path")
    args = parser.parse_args()

    script_dir = Path(__file__).resolve().parent
    template_path = Path(args.template).expanduser().resolve() if args.template else script_dir.parent / "assets" / "dashboard-template.html"
    analysis_path = Path(args.analysis).expanduser().resolve()
    insights_path = Path(args.insights).expanduser().resolve()
    output_path = Path(args.output).expanduser().resolve()
    for path in (analysis_path, insights_path, template_path):
        if not path.is_file():
            raise SystemExit(f"Required file not found: {path}")

    payload = build_payload(read_json(analysis_path), read_json(insights_path))
    if not payload["insights"]:
        raise SystemExit("No valid insights remain after normalization")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(build_html(payload, template_path), encoding="utf-8")
    print(json.dumps({
        "ok": True,
        "output": str(output_path),
        "group": payload["group"],
        "days": len(payload["daily"]),
        "insights": len(payload["insights"]),
        "warnings": payload["warnings"],
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
