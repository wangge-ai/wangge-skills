#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Normalize a group-chat export and build a private evidence package."""

from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Iterable


CN_TZ = timezone(timedelta(hours=8))

TIME_FIELDS = ("timestamp", "time", "createTime", "create_time", "datetime", "date", "sendTime")
SENDER_FIELDS = ("accountName", "senderName", "nickname", "name", "speaker", "sender", "fromName")
SENDER_ID_FIELDS = ("senderId", "platformId", "userName", "wxid", "user_id", "from")
CONTENT_FIELDS = ("content", "text", "message", "msg", "body", "plainText")
TYPE_FIELDS = ("type", "msgType", "messageType", "kind", "mediaType")
SYSTEM_TYPES = {"80", "system", "notice", "revoke", "recall"}
VOICE_TYPES = {"4", "34", "voice", "audio"}

QUESTION_HINTS = (
    "?", "？", "怎么", "如何", "有没有", "能不能", "可以吗", "为什么", "哪里",
    "哪儿", "哪个", "请问", "求助", "推荐", "请教", "是不是", "是否", "怎么办",
    "啥意思", "多少钱", "咋", "吗", "么",
)

TOPICS = {
    "AI工具/模型/Agent": (
        "ai", "codex", "claude", "chatgpt", "gpt", "deepseek", "gemini", "kimi",
        "模型", "api", "agent", "智能体", "mcp", "skill", "插件", "提示词",
    ),
    "自动化/流程/采集": (
        "自动化", "rpa", "影刀", "采集", "爬虫", "抓取", "浏览器", "脚本", "批量",
        "监控", "定时", "上架", "工作流", "流程",
    ),
    "经营/数据/决策": (
        "经营", "店铺", "运营", "竞品", "销量", "流量", "转化", "投放", "广告",
        "诊断", "报表", "数据", "利润", "成本", "库存", "决策",
    ),
    "内容/图片/视频": (
        "主图", "详情页", "生图", "商品图", "产品图", "图片", "视频", "素材", "剪辑",
        "口播", "数字人", "分镜", "文章", "写作", "标题", "小红书", "抖音", "公众号",
    ),
    "知识/文档/协作": (
        "知识库", "rag", "文档", "资料", "飞书", "多维表格", "notebooklm", "检索",
        "案例库", "数据库", "归档", "总结", "协作",
    ),
    "学习/安装/排障": (
        "小白", "教程", "学习", "安装", "配置", "报错", "打不开", "不会", "入门",
        "环境", "部署", "终端", "命令行", "登录失败", "故障",
    ),
    "账号/费用/权限": (
        "账号", "会员", "额度", "订阅", "充值", "计费", "价格", "费用", "成本", "登录",
        "验证码", "套餐", "并发", "权限",
    ),
    "组织/客户/服务": (
        "企业", "公司", "团队", "客服", "老板", "员工", "组织", "业务", "客户", "落地",
        "管理", "岗位", "交付", "服务",
    ),
    "关系/生活/情绪": (
        "家人", "朋友", "孩子", "父母", "生活", "情绪", "压力", "焦虑", "开心", "难过",
        "关系", "沟通", "健康", "出行", "吃饭",
    ),
    "交易/消费/资源": (
        "购买", "付款", "转账", "消费", "预算", "报价", "订单", "商品", "资源", "渠道",
        "供应商", "交易", "钱",
    ),
    "安全/隐私/合规": (
        "安全", "隐私", "泄露", "敏感", "私有化", "合规", "风控", "封号", "刷单",
        "绕过", "授权", "保密",
    ),
}

MEDIA_EXTENSIONS = {
    "images": {".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp", ".heic", ".avif"},
    "videos": {".mp4", ".mov", ".avi", ".mkv", ".webm", ".m4v"},
    "voices": {".mp3", ".wav", ".m4a", ".amr", ".silk", ".ogg", ".opus", ".aac", ".flac"},
}

TXT_PATTERNS = (
    re.compile(r"^\[?(?P<time>\d{4}[-/]\d{1,2}[-/]\d{1,2}[ T]\d{1,2}:\d{2}(?::\d{2})?)\]?\s+(?P<sender>[^:：]{1,80})[:：]\s*(?P<text>.*)$"),
    re.compile(r"^(?P<time>\d{4}[-/]\d{1,2}[-/]\d{1,2}[ T]\d{1,2}:\d{2}(?::\d{2})?)\s*[-|]\s*(?P<sender>[^:：]{1,80})[:：]\s*(?P<text>.*)$"),
)


def read_text(path: Path) -> str:
    for encoding in ("utf-8-sig", "utf-8", "gb18030", "utf-16"):
        try:
            return path.read_text(encoding=encoding)
        except UnicodeError:
            continue
    raise ValueError(f"Cannot decode text file: {path}")


def parse_timestamp(value: Any) -> int:
    if value in (None, ""):
        return 0
    if isinstance(value, (int, float)):
        number = int(value)
        return number // 1000 if number > 10_000_000_000 else number
    text = str(value).strip().replace("/", "-").replace("T", " ")
    if text.isdigit():
        return parse_timestamp(int(text))
    text = re.sub(r"\s+[A-Z]{2,5}$", "", text)
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%d"):
        try:
            return int(datetime.strptime(text[:19], fmt).replace(tzinfo=CN_TZ).timestamp())
        except ValueError:
            continue
    return 0


def format_timestamp(value: int) -> str:
    if not value:
        return "未知"
    return datetime.fromtimestamp(value, CN_TZ).strftime("%Y-%m-%d %H:%M:%S")


def clean_text(value: Any) -> str:
    if isinstance(value, dict):
        for key in CONTENT_FIELDS:
            if value.get(key) not in (None, ""):
                value = value[key]
                break
        else:
            value = json.dumps(value, ensure_ascii=False)
    elif isinstance(value, list):
        value = " ".join(clean_text(item) for item in value)
    text = str(value or "").replace("\r", " ").replace("\n", " ")
    text = re.sub(r"https?://\S+", "[链接]", text)
    return re.sub(r"\s+", " ", text).strip()


def first_value(row: dict[str, Any], fields: Iterable[str]) -> Any:
    for key in fields:
        if row.get(key) not in (None, ""):
            return row[key]
    return None


def sender_name(row: dict[str, Any]) -> str:
    value = first_value(row, SENDER_FIELDS)
    if isinstance(value, dict):
        value = first_value(value, ("name", "nickname", "displayName", "accountName", "id"))
    return clean_text(value) or "未知成员"


def sender_id(row: dict[str, Any]) -> str:
    value = first_value(row, SENDER_ID_FIELDS)
    if isinstance(value, dict):
        value = first_value(value, ("id", "wxid", "userName", "platformId"))
    return str(value or "").strip()


def normalize_row(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "timestamp": parse_timestamp(first_value(row, TIME_FIELDS)),
        "speaker": sender_name(row),
        "sender_id": sender_id(row),
        "type": str(first_value(row, TYPE_FIELDS) or "unknown"),
        "text": clean_text(first_value(row, CONTENT_FIELDS)),
    }


def find_message_list(data: Any) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]]]:
    if isinstance(data, list):
        return {}, [], [item for item in data if isinstance(item, dict)]
    if not isinstance(data, dict):
        raise ValueError("JSON root must be an object or a list of message objects")
    meta = data.get("meta") if isinstance(data.get("meta"), dict) else {}
    members = data.get("members") or data.get("memberList") or data.get("participants") or []
    candidates = (
        data.get("messages"), data.get("messageList"), data.get("records"), data.get("items"), data.get("data")
    )
    messages: Any = None
    for candidate in candidates:
        if isinstance(candidate, list):
            messages = candidate
            break
        if isinstance(candidate, dict):
            nested = candidate.get("messages") or candidate.get("list") or candidate.get("items") or candidate.get("records")
            if isinstance(nested, list):
                messages = nested
                break
    if messages is None:
        raise ValueError("Cannot find a message list in the JSON object")
    return meta, members if isinstance(members, list) else [], [item for item in messages if isinstance(item, dict)]


def load_json(path: Path) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]], str]:
    data = json.loads(read_text(path))
    meta, members, rows = find_message_list(data)
    return meta, members, rows, "json"


def load_jsonl(path: Path) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]], str]:
    rows = []
    for line_number, line in enumerate(read_text(path).splitlines(), 1):
        if not line.strip():
            continue
        try:
            item = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid JSON on line {line_number}: {exc}") from exc
        if isinstance(item, dict):
            rows.append(item)
    return {}, [], rows, "jsonl"


def load_csv(path: Path) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]], str]:
    text = read_text(path)
    sample = text[:4096]
    try:
        dialect = csv.Sniffer().sniff(sample, delimiters=",\t;|")
    except csv.Error:
        dialect = csv.excel
    rows = list(csv.DictReader(text.splitlines(), dialect=dialect))
    return {}, [], [dict(row) for row in rows], "csv"


def load_txt(path: Path) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]], str]:
    rows: list[dict[str, Any]] = []
    unmatched = 0
    for raw_line in read_text(path).splitlines():
        line = raw_line.strip()
        if not line:
            continue
        match = next((pattern.match(line) for pattern in TXT_PATTERNS if pattern.match(line)), None)
        if match:
            rows.append({
                "time": match.group("time"),
                "senderName": match.group("sender").strip(),
                "content": match.group("text").strip(),
                "type": "text",
            })
        elif rows:
            rows[-1]["content"] = f"{rows[-1]['content']} {line}".strip()
        else:
            unmatched += 1
            rows.append({"content": line, "senderName": "未知成员", "type": "text"})
    return {"unmatchedLeadingLines": unmatched}, [], rows, "txt"


def load_input(path: Path) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]], str]:
    suffix = path.suffix.lower()
    if suffix == ".json":
        return load_json(path)
    if suffix in {".jsonl", ".ndjson"}:
        return load_jsonl(path)
    if suffix in {".csv", ".tsv"}:
        return load_csv(path)
    if suffix in {".txt", ".log"}:
        return load_txt(path)
    raise ValueError(f"Unsupported input format: {suffix or '<none>'}")


def derive_group_name(meta: dict[str, Any], source: Path, override: str | None) -> str:
    if override:
        return clean_text(override)
    for key in ("name", "title", "groupName", "chatName", "conversationName"):
        if meta.get(key):
            return clean_text(meta[key])
    return re.sub(r"^(群聊_|群聊-|group[_-])", "", source.stem, flags=re.I) or "未命名群聊"


def is_question(text: str) -> bool:
    lowered = text.lower()
    return len(text) >= 2 and any(hint in lowered for hint in QUESTION_HINTS)


def topic_hits(text: str) -> list[tuple[str, list[str]]]:
    lowered = text.lower()
    result = []
    for topic, keywords in TOPICS.items():
        matched = sorted({keyword for keyword in keywords if keyword.lower() in lowered})
        if matched:
            result.append((topic, matched))
    return result


def evidence_score(text: str, hits: list[tuple[str, list[str]]], question: bool, msg_type: str) -> int:
    score = min(len(text) // 28, 9)
    score += 5 if question else 0
    score += min(len(hits), 3) * 2
    score += 2 if msg_type.lower() in {"25", "quote", "reply"} else 0
    score += 2 if any(mark in text for mark in ("因为", "所以", "但是", "实际", "核心", "问题", "建议", "结果", "失败")) else 0
    return score


def classify_media(path: Path) -> str:
    if any("emoji" in part.lower() or "emoticon" in part.lower() for part in path.parts):
        return "emojis"
    for category, extensions in MEDIA_EXTENSIONS.items():
        if path.suffix.lower() in extensions:
            return category
    return "files"


def inventory_media(folder: Path) -> dict[str, Any]:
    roots = []
    media_root = folder / "media"
    if media_root.exists():
        roots.append(media_root)
    for name in ("images", "videos", "voices", "files", "emojis", "emoji", "attachments"):
        candidate = folder / name
        if candidate.exists() and candidate not in roots:
            roots.append(candidate)
    files = []
    for root in roots:
        files.extend(item for item in root.rglob("*") if item.is_file())
    counts: Counter[str] = Counter()
    sizes: Counter[str] = Counter()
    for item in files:
        category = classify_media(item)
        counts[category] += 1
        try:
            sizes[category] += item.stat().st_size
        except OSError:
            pass
    return {
        "roots": [str(root) for root in roots],
        "totalFiles": len(files),
        "totalBytes": sum(sizes.values()),
        "counts": dict(sorted(counts.items())),
        "bytesByType": dict(sorted(sizes.items())),
    }


def member_names(members: list[dict[str, Any]]) -> set[str]:
    names = set()
    for member in members:
        if not isinstance(member, dict):
            continue
        value = first_value(member, ("name", "nickname", "displayName", "accountName", "remark"))
        if clean_text(value):
            names.add(clean_text(value))
    return names


def member_ids(members: list[dict[str, Any]]) -> set[str]:
    ids = set()
    for member in members:
        if not isinstance(member, dict):
            continue
        value = first_value(member, ("platformId", "userName", "wxid", "id", "user_id"))
        if value not in (None, ""):
            ids.add(str(value).strip())
    return ids


def analyze(source: Path, cutoff: int, group_override: str | None) -> dict[str, Any]:
    meta, members, raw_rows, source_format = load_input(source)
    rows = [normalize_row(row) for row in raw_rows]
    rows.sort(key=lambda row: (row["timestamp"] == 0, row["timestamp"]))
    for position, row in enumerate(rows, 1):
        row["ref"] = f"M{position:06d}"
    timestamps = [row["timestamp"] for row in rows if row["timestamp"]]
    selected = [row for row in rows if (row["timestamp"] > cutoff if cutoff else True)]
    timeless_total = sum(1 for row in rows if not row["timestamp"])
    timeless_selected = sum(1 for row in selected if not row["timestamp"])

    speaker_counts: Counter[str] = Counter()
    speaker_questions: Counter[str] = Counter()
    speaker_topics: dict[str, Counter[str]] = defaultdict(Counter)
    topic_counts: Counter[str] = Counter()
    topic_rows: dict[str, list[dict[str, Any]]] = defaultdict(list)
    day_counts: Counter[str] = Counter()
    day_questions: Counter[str] = Counter()
    day_speakers: dict[str, set[str]] = defaultdict(set)
    day_topics: dict[str, Counter[str]] = defaultdict(Counter)
    type_counts: Counter[str] = Counter()
    questions = []
    evidence = []
    platform_ids = member_ids(members)
    names = member_names(members)
    system_count = 0

    for row in selected:
        msg_type = row["type"].lower()
        type_counts[msg_type] += 1
        if row["sender_id"]:
            platform_ids.add(row["sender_id"])
        if msg_type in SYSTEM_TYPES:
            system_count += 1
            continue
        text = row["text"]
        if not text:
            continue
        speaker = row["speaker"]
        names.add(speaker)
        hits = topic_hits(text)
        question = is_question(text)
        score = evidence_score(text, hits, question, msg_type)
        item = {
            "ref": row["ref"],
            "time": format_timestamp(row["timestamp"]),
            "timestamp": row["timestamp"],
            "speaker": speaker,
            "type": row["type"],
            "text": text,
            "question": question,
            "topics": [topic for topic, _ in hits],
            "matched": {topic: words for topic, words in hits},
            "score": score,
        }
        speaker_counts[speaker] += 1
        if row["timestamp"]:
            day = format_timestamp(row["timestamp"])[:10]
            day_counts[day] += 1
            day_speakers[day].add(speaker)
        if question:
            speaker_questions[speaker] += 1
            questions.append(item)
            if row["timestamp"]:
                day_questions[day] += 1
        for topic, _ in hits:
            topic_counts[topic] += 1
            speaker_topics[speaker][topic] += 1
            topic_rows[topic].append(item)
            if row["timestamp"]:
                day_topics[day][topic] += 1
        if score >= 5:
            evidence.append(item)

    effective = sum(speaker_counts.values())
    top_five = sum(count for _, count in speaker_counts.most_common(5))
    selected_timestamps = [row["timestamp"] for row in selected if row["timestamp"]]
    people = [
        {
            "speaker": speaker,
            "messages": count,
            "questions": speaker_questions[speaker],
            "topics": speaker_topics[speaker].most_common(6),
        }
        for speaker, count in speaker_counts.most_common()
    ]
    questions.sort(key=lambda item: (-item["score"], item["timestamp"]))
    evidence.sort(key=lambda item: (-item["score"], item["timestamp"]))
    media = inventory_media(source.parent)
    voice_records = sum(count for kind, count in type_counts.items() if kind in VOICE_TYPES)
    voice_files = media["counts"].get("voices", 0)
    daily_details = [
        {
            "date": day,
            "effectiveMessages": day_counts[day],
            "questionLike": day_questions[day],
            "activeSpeakers": len(day_speakers[day]),
            "topicCounts": day_topics[day].most_common(),
        }
        for day in sorted(day_counts)
    ]

    return {
        "schemaVersion": 3,
        "generatedAt": datetime.now(CN_TZ).strftime("%Y-%m-%d %H:%M:%S"),
        "source": {"path": str(source), "format": source_format},
        "group": {"name": derive_group_name(meta, source, group_override), "meta": meta},
        "baseline": {"cutoff": format_timestamp(cutoff), "cutoffTimestamp": cutoff},
        "totals": {
            "messages": len(rows),
            "membersMetadata": len(members),
            "dateStart": format_timestamp(min(timestamps)) if timestamps else "未知",
            "dateEnd": format_timestamp(max(timestamps)) if timestamps else "未知",
            "timelessMessages": timeless_total,
        },
        "selected": {
            "messages": len(selected),
            "systemMessages": system_count,
            "effectiveMessages": effective,
            "activeSpeakers": len(speaker_counts),
            "questionLike": len(questions),
            "dateStart": format_timestamp(min(selected_timestamps)) if selected_timestamps else "未知",
            "dateEnd": format_timestamp(max(selected_timestamps)) if selected_timestamps else "未知",
            "timelessMessages": timeless_selected,
            "topFiveShare": round(top_five / effective, 4) if effective else 0,
            "topicCounts": topic_counts.most_common(),
            "typeCounts": type_counts.most_common(),
            "daily": sorted(day_counts.items()),
            "dailyDetails": daily_details,
        },
        "media": {
            **media,
            "voiceMessageRecords": voice_records,
            "voiceFiles": voice_files,
            "voiceCoverageWarning": voice_records > voice_files,
        },
        "people": people,
        "memberNames": sorted(name for name in names if name and name != "未知成员"),
        "platformIds": sorted(value for value in platform_ids if value),
        "questions": questions[:400],
        "evidence": evidence[:600],
        "topicEvidence": {
            topic: sorted(items, key=lambda item: (-item["score"], item["timestamp"]))[:60]
            for topic, items in topic_rows.items()
        },
    }


def write_digest(data: dict[str, Any], output: Path) -> None:
    selected = data["selected"]
    media = data["media"]
    lines = [
        f"# {data['group']['name']}｜群聊证据摘要（本地私有）",
        "",
        f"- 输入格式：{data['source']['format']}",
        f"- 分析区间：{selected['dateStart']} 至 {selected['dateEnd']}",
        f"- 本次消息：{selected['messages']} 条；有效消息 {selected['effectiveMessages']} 条",
        f"- 成员元数据：{data['totals']['membersMetadata']} 名；实际发言者 {selected['activeSpeakers']} 名",
        f"- 疑问式消息：{selected['questionLike']} 条；前五位发言占比 {selected['topFiveShare']:.1%}",
        f"- 无时间消息：{selected['timelessMessages']} 条",
        f"- 媒体文件：{media['totalFiles']} 个；{json.dumps(media['counts'], ensure_ascii=False)}",
        f"- 语音覆盖：消息记录 {media['voiceMessageRecords']} 条，文件 {media['voiceFiles']} 个",
        "",
        "## 主题计数（仅用于定位证据）",
        "",
    ]
    lines.extend(f"- {topic}: {count}" for topic, count in selected["topicCounts"])
    lines.extend(["", "## 活跃成员（仅限本地证据定位）", ""])
    for person in data["people"][:30]:
        topics = "、".join(name for name, _ in person["topics"][:3]) or "未归类"
        lines.append(f"- {person['speaker']}: {person['messages']} 条，疑问式 {person['questions']} 条；{topics}")
    lines.extend(["", "## 高频疑问证据", ""])
    for row in data["questions"][:120]:
        lines.append(f"- {row['ref']}｜[{row['time']}] {row['speaker']}｜{row['text']}｜主题：{'、'.join(row['topics']) or '未归类'}")
    lines.extend(["", "## 高分证据", ""])
    for row in data["evidence"][:160]:
        lines.append(f"- {row['ref']}｜[{row['time']}] {row['speaker']}｜{row['text']}｜分数：{row['score']}")
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Prepare a group-chat export for two-report analysis")
    parser.add_argument("--input", required=True, help="JSON, JSONL, CSV, TXT, or LOG chat export")
    parser.add_argument("--outdir", required=True, help="Output directory for private evidence files")
    parser.add_argument("--cutoff", default="", help="Only select messages strictly after this timestamp")
    parser.add_argument("--group-name", help="Override the detected group name")
    args = parser.parse_args()

    source = Path(args.input).expanduser().resolve()
    if not source.is_file():
        raise SystemExit(f"Input file not found: {source}")
    cutoff = parse_timestamp(args.cutoff) if args.cutoff else 0
    output_dir = Path(args.outdir).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    analysis = analyze(source, cutoff, args.group_name)
    analysis_path = output_dir / "group_analysis.json"
    digest_path = output_dir / "evidence_digest.md"
    analysis_path.write_text(json.dumps(analysis, ensure_ascii=False, indent=2), encoding="utf-8")
    write_digest(analysis, digest_path)
    print(json.dumps({
        "ok": True,
        "analysis": str(analysis_path),
        "digest": str(digest_path),
        "group": analysis["group"]["name"],
        "selected": analysis["selected"],
        "media": analysis["media"],
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
