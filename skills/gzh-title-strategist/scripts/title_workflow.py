from __future__ import annotations

import argparse
import csv
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable


FORMULA_NAMES = {
    "sample_teardown": "样本拆解交付型",
    "input_output": "输入输出自动化型",
    "from_zero": "从零教程型",
    "first_person": "一人实操复盘型",
    "priority_judgment": "优先级判断型",
}

CHECKS = [
    ("clear_entity", "明确实体"),
    ("real_task", "真实任务"),
    ("deliverable", "可交付结果"),
    ("clear_takeaway", "一眼知道拿走什么"),
    ("tool_not_overpowering", "工具没有压过业务结果"),
    ("outsider_readable", "推荐流陌生人能看懂"),
    ("proof_visual_possible", "首屏有图可证明"),
]

ENTITY_TERMS = [
    "公众号",
    "后台数据",
    "文章",
    "标题",
    "电商",
    "商品",
    "评论",
    "GitHub",
    "Skill",
    "Codex",
    "Claude",
    "GPT",
    "n8n",
    "Dify",
]

TASK_TERMS = [
    "输入",
    "输出",
    "自动生成",
    "生成",
    "搭",
    "搭建",
    "拆",
    "拆解",
    "整理",
    "回看",
    "复盘",
    "诊断",
    "分析",
    "评分",
    "筛",
    "判断",
    "做出",
    "跑通",
]

DELIVERABLE_TERMS = [
    "报告",
    "表",
    "清单",
    "公式",
    "SOP",
    "Skill",
    "工作流",
    "教程",
    "地图",
    "资料包",
    "模板",
    "规则",
]

PROOF_TERMS = [
    "报告",
    "表",
    "图",
    "截图",
    "流程",
    "数据",
    "评分",
    "复盘",
    "清单",
    "公式",
]

TOOL_TERMS = ["AI", "Codex", "Claude", "GPT", "n8n", "Dify", "Skill", "工具"]
VAGUE_TERMS = ["分享一个", "这个", "那个", "又来了", "升级了", "太强了"]
STOP_WORDS = {"一个", "一套", "这个", "那个", "我们", "自己的", "工作流"}


@dataclass(frozen=True)
class Candidate:
    title: str
    formula_id: str
    formula_name: str
    source_note: str


@dataclass(frozen=True)
class ScoreResult:
    title: str
    score: int
    checks: dict[str, bool]
    notes: list[str]


def generate_candidates(topic: str, context: str = "", count: int = 10) -> list[Candidate]:
    topic = topic.strip()
    context = context.strip()
    if not topic:
        raise ValueError("topic is required")

    sample_phrase = _extract_sample_phrase(context) or "文章材料"
    subject = _infer_subject(topic, context)
    deliverable = _infer_deliverable(topic, context)
    asset = _infer_asset(topic, context)
    tool = _infer_tool(topic, context)
    compact_topic = _compact_topic(topic)

    templates = [
        ("sample_teardown", f"拆解{sample_phrase}：怎样整理{deliverable}", "需核对真实材料及交付物。"),
        ("sample_teardown", f"{compact_topic}怎么复盘？先核对样本和判断依据", "不预设已经得到的发现。"),
        ("input_output", f"从{subject}到{deliverable}，流程怎么设计", "核对输入、过程和输出。"),
        ("input_output", f"用{tool}整理{subject}，先明确要输出什么", "工具只作为方法选择。"),
        ("from_zero", f"从0开始做{compact_topic}，先准备哪些材料", "核对入门前置条件。"),
        ("from_zero", f"{compact_topic}入门：把任务拆成可检查的步骤", "核对正文是否提供步骤。"),
        ("first_person", f"做{compact_topic}时，怎样检查结果是否可靠", "由作者真实经历补充细节，不默认亲测。"),
        ("first_person", f"用{tool}做{compact_topic}，哪些地方仍需人工核对", "核对工具能力与人工边界。"),
        ("priority_judgment", f"做{compact_topic}前，先检查资料够不够", "核对资料与目标。"),
        ("priority_judgment", f"{compact_topic}别只看工具，先明确交付结果", "核对读者任务与交付物。"),
        ("sample_teardown", f"{compact_topic}的判断依据，怎样变成可复用清单", "不虚构公式数量。"),
        ("input_output", f"给AI准备{subject}时，怎样保留证据来源", "核对证据与输入条件。"),
        ("from_zero", f"搭{compact_topic}工作流，先写清输入和验收", "核对流程是否真实可操作。"),
        ("priority_judgment", f"{compact_topic}能不能复用？从这些条件开始检查", "条件必须由正文明确列出。"),
    ]

    candidates = [
        Candidate(title=title, formula_id=formula_id, formula_name=FORMULA_NAMES[formula_id], source_note=note)
        for formula_id, title, note in templates
    ]
    return _unique_candidates(candidates)[: max(1, count)]


def score_title(title: str, topic: str = "", context: str = "") -> ScoreResult:
    normalized = _normalize(title)

    clear_entity = _contains_any(title, ENTITY_TERMS) or _contains_topic_keyword(title, topic)
    real_task = _contains_any(title, TASK_TERMS)
    deliverable = _contains_any(title, DELIVERABLE_TERMS)
    clear_takeaway = deliverable or bool(re.search(r"\d+\s*(个|条|项|套|张|篇)", title)) or "拿走" in title
    tool_not_overpowering = not _tool_overpowers_business(title, real_task=real_task, deliverable=deliverable)
    outsider_readable = _is_outsider_readable(title, clear_entity=clear_entity, real_task=real_task, deliverable=deliverable)
    proof_visual_possible = _contains_any(title, PROOF_TERMS)

    checks = {
        "clear_entity": clear_entity,
        "real_task": real_task,
        "deliverable": deliverable,
        "clear_takeaway": clear_takeaway,
        "tool_not_overpowering": tool_not_overpowering,
        "outsider_readable": outsider_readable,
        "proof_visual_possible": proof_visual_possible,
    }
    score = sum(1 for passed in checks.values() if passed)
    notes = _score_notes(checks, normalized)
    return ScoreResult(title=title, score=score, checks=checks, notes=notes)


def build_rows(candidates: Iterable[Candidate], topic: str, context: str = "") -> list[dict[str, str]]:
    rows = []
    for candidate in candidates:
        score = score_title(candidate.title, topic=topic, context=context)
        passed_labels = [label for key, label in CHECKS if score.checks[key]]
        rows.append(
            {
                "title": candidate.title,
                "formula_id": candidate.formula_id,
                "formula_name": candidate.formula_name,
                "score": str(score.score),
                "score_label": f"{score.score}/7",
                "passed_checks": "、".join(passed_labels),
                "notes": "需核对正文事实、经历与交付物；" + "；".join(score.notes),
                "source_note": candidate.source_note,
                **{key: "1" if score.checks[key] else "0" for key, _label in CHECKS},
            }
        )

    rows.sort(key=lambda row: (-int(row["score"]), _formula_order(row["formula_id"]), row["title"]))
    for index, row in enumerate(rows, start=1):
        row["rank"] = str(index)
    return rows


def export_results(topic: str, rows: list[dict[str, str]], output_dir: Path) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    markdown_path = output_dir / "title-candidates.md"
    csv_path = output_dir / "title-candidates.csv"

    markdown_path.write_text(_render_markdown(topic, rows), encoding="utf-8")
    _write_csv(csv_path, rows)
    return markdown_path, csv_path


def run(topic: str, context: str = "", count: int = 10, output_dir: str | Path = "outputs") -> tuple[Path, Path, list[dict[str, str]]]:
    candidates = generate_candidates(topic=topic, context=context, count=count)
    rows = build_rows(candidates, topic=topic, context=context)
    markdown_path, csv_path = export_results(topic=topic, rows=rows, output_dir=Path(output_dir))
    return markdown_path, csv_path, rows


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate and score WeChat article titles.")
    parser.add_argument("--topic", required=True, help="Topic or brief, for example: 公众号数据复盘工作流")
    parser.add_argument("--context", default="", help="Optional extra facts, samples, or constraints.")
    parser.add_argument("--count", type=int, default=10, help="Number of candidates to export.")
    parser.add_argument("--output-dir", default="outputs", help="Directory for title-candidates.md/csv.")
    args = parser.parse_args(argv)

    markdown_path, csv_path, rows = run(
        topic=args.topic,
        context=args.context,
        count=args.count,
        output_dir=args.output_dir,
    )
    print(f"generated={len(rows)}")
    print(f"markdown={markdown_path}")
    print(f"csv={csv_path}")
    return 0


def _extract_sample_phrase(context: str) -> str:
    match = re.search(
        r"(\d+)\s*(多|余)?\s*(篇|个|条|份)\s*(文章|标题|样本|数据|记录|素材|案例|链接|评论|笔记|报告)?",
        context,
    )
    if not match:
        return ""
    number, suffix, unit, noun = match.groups()
    number_text = f"{number}{suffix or ''}"
    noun = noun or ""
    if unit == "篇" and "文章" not in noun:
        noun = "文章"
    if unit == "个" and not noun:
        noun = "样本"
    return f"{number_text} {unit}{noun}".strip()


def _infer_subject(topic: str, context: str) -> str:
    text = topic + context
    if "公众号" in text:
        return "公众号后台数据"
    if "商品链接" in text:
        return "商品链接"
    if "电商" in text or "商品" in text:
        return "电商样本数据"
    if "GitHub" in text:
        return "GitHub 项目链接"
    if "评论" in text:
        return "用户评论数据"
    return _compact_topic(topic)


def _infer_deliverable(topic: str, context: str) -> str:
    text = topic + context
    if "复盘" in text:
        return "选题复盘报告"
    if "标题" in text:
        return "标题评分表"
    if "工作流" in text:
        return "自动化工作流"
    if "评论" in text:
        return "评论洞察报告"
    return "分析报告"


def _infer_asset(topic: str, context: str) -> str:
    text = topic + context
    if "标题" in text or "公众号" in text:
        return "标题评分表"
    if "工作流" in text:
        return "流程SOP"
    return "判断清单"


def _infer_tool(topic: str, context: str) -> str:
    text = topic + context
    for tool in ["Codex", "Claude", "Dify", "n8n", "GPT"]:
        if tool.lower() in text.lower():
            return tool
    return "Codex"


def _compact_topic(topic: str) -> str:
    topic = re.sub(r"\s+", "", topic)
    return topic or "内容分析流程"


def _unique_candidates(candidates: Iterable[Candidate]) -> list[Candidate]:
    seen = set()
    unique = []
    for candidate in candidates:
        key = _normalize(candidate.title)
        if key in seen:
            continue
        seen.add(key)
        unique.append(candidate)
    return unique


def _contains_any(text: str, terms: Iterable[str]) -> bool:
    folded = text.lower()
    return any(term.lower() in folded for term in terms)


def _contains_topic_keyword(title: str, topic: str) -> bool:
    tokens = re.findall(r"[A-Za-z0-9]+|[一-龥]{2,}", topic)
    useful_tokens = [token for token in tokens if token not in STOP_WORDS and len(token) >= 2]
    return any(token in title for token in useful_tokens)


def _tool_overpowers_business(title: str, real_task: bool, deliverable: bool) -> bool:
    has_tool = _contains_any(title, TOOL_TERMS)
    if not has_tool:
        return False
    starts_with_tool = bool(re.match(r"^\s*(AI|Codex|Claude|GPT|n8n|Dify|Skill|工具)", title, flags=re.I))
    vague_tool_share = "分享一个" in title and "工具" in title
    return (starts_with_tool or vague_tool_share) and not (real_task and deliverable)


def _is_outsider_readable(title: str, clear_entity: bool, real_task: bool, deliverable: bool) -> bool:
    if len(title.strip()) < 8:
        return False
    if _contains_any(title, VAGUE_TERMS) and not (real_task and deliverable):
        return False
    return clear_entity and (real_task or deliverable)


def _score_notes(checks: dict[str, bool], normalized: str) -> list[str]:
    notes = []
    if not checks["clear_entity"]:
        notes.append("补上具体对象，比如公众号、商品链接、评论或后台数据")
    if not checks["real_task"]:
        notes.append("补上动作，比如输入、拆解、复盘、生成或筛选")
    if not checks["deliverable"]:
        notes.append("补上交付物，比如报告、表、清单、SOP或工作流")
    if not checks["clear_takeaway"]:
        notes.append("让读者一眼知道能拿走什么")
    if not checks["tool_not_overpowering"]:
        notes.append("不要只喊工具名，把业务结果放到标题后半句")
    if not checks["outsider_readable"]:
        notes.append("降低内部黑话，改成陌生人也懂的任务表达")
    if not checks["proof_visual_possible"]:
        notes.append("最好让标题承诺能用首图、表格或截图证明")
    if "分享一个" in normalized:
        notes.append("弱化“分享一个”，改成输入输出或结果承诺")
    return notes


def _formula_order(formula_id: str) -> int:
    order = {
        "input_output": 1,
        "sample_teardown": 2,
        "from_zero": 3,
        "first_person": 4,
        "priority_judgment": 5,
    }
    return order.get(formula_id, 99)


def _render_markdown(topic: str, rows: list[dict[str, str]]) -> str:
    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines = [
        f"# 标题候选与评分：{topic}",
        "",
        f"- 生成时间：{generated_at}",
        f"- 候选数量：{len(rows)}",
        "- 这些是模板候选，尚未核对正文，不代表作者已经操作、交付附件或得到结果。",
        "- 评分口径：7项检查，每项1分，优先选择 6 分以上且能配首图证明的标题。",
        "",
        "## 候选排序",
        "",
        "| 排名 | 标题 | 公式 | 得分 | 命中项 | 修改建议 |",
        "|---:|---|---|---:|---|---|",
    ]
    for row in rows:
        lines.append(
            "| {rank} | {title} | {formula_name} | {score_label} | {passed_checks} | {notes} |".format(
                **{key: _escape_markdown_cell(value) for key, value in row.items()}
            )
        )
    lines.extend(
        [
            "",
            "## 使用方式",
            "",
            "1. 先从 6-7 分标题里选 2-3 个。",
            "2. 检查首图或正文截图是否能证明标题里的承诺。",
            "3. 如果标题只是在说工具，改成“输入什么，输出什么”。",
            "4. 如果标题只是在讲方法，补上样本数量、对象或交付物。",
        ]
    )
    return "\n".join(lines) + "\n"


def _write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    fieldnames = [
        "rank",
        "title",
        "formula_id",
        "formula_name",
        "score",
        "score_label",
        "passed_checks",
        "notes",
        "source_note",
        *[key for key, _label in CHECKS],
    ]
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def _escape_markdown_cell(value: str) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def _normalize(text: str) -> str:
    return re.sub(r"\s+", "", text)


if __name__ == "__main__":
    raise SystemExit(main())
