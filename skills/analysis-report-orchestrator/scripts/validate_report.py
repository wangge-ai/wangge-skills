import argparse
import json
import re
from pathlib import Path


REQUIRED_SECTIONS = [
    "## 执行摘要",
    "## 任务与分析范围",
    "## 数据与方法",
    "## 关键发现",
    "## 原因或机制分析",
    "## 结论",
    "## 行动建议",
    "## 风险与未知项",
]
FINDING_LABELS = ["- 事实：", "- 证据：", "- 解释：", "- 边界："]
ACTION_HEADERS = ["动作", "依据", "优先级", "负责人", "时间", "指标", "风险", "后手"]
UNRESOLVED_MARKERS = ["稍后补写", "待完善", "待确认内容", "占位内容"]


def extract_section(text: str, heading: str) -> str | None:
    match = re.search(
        rf"^{re.escape(heading)}[ \t]*$\n?(.*?)(?=^## [^#]|\Z)",
        text,
        re.MULTILINE | re.DOTALL,
    )
    return match.group(1) if match else None


def parse_table_cells(line: str) -> list[str]:
    stripped = line.strip()
    if not stripped.startswith("|") or not stripped.endswith("|"):
        return []
    return [cell.strip() for cell in stripped[1:-1].split("|")]


def is_separator_row(cells: list[str]) -> bool:
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells)


def has_contiguous_action_table(section: str) -> bool:
    return action_table_issue(section) is None


def action_table_issue(section: str) -> str | None:
    lines = section.splitlines()
    for index, line in enumerate(lines):
        if parse_table_cells(line) != ACTION_HEADERS:
            continue
        if index + 1 >= len(lines):
            return "data"
        separator = parse_table_cells(lines[index + 1])
        if len(separator) != len(ACTION_HEADERS) or not is_separator_row(separator):
            return "structure"
        if index + 2 >= len(lines):
            return "data"
        data = parse_table_cells(lines[index + 2])
        if len(data) == len(ACTION_HEADERS):
            return None if all(data) else "data"
        if not lines[index + 2].strip():
            later_rows = (
                parse_table_cells(later_line)
                for later_line in lines[index + 3 :]
            )
            return "structure" if any(later_rows) else "data"
        return "structure"
    return "structure"


def validate(path: Path) -> dict:
    try:
        text = Path(path).read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        return {
            "passed": False,
            "errors": [f"无法读取报告：{exc}"],
            "warnings": [],
            "exit_code": 2,
        }

    errors = []
    warnings = []

    sections = {section: extract_section(text, section) for section in REQUIRED_SECTIONS}
    missing_sections = [section for section, content in sections.items() if content is None]
    if missing_sections:
        errors.append("缺少必需章节：" + "、".join(missing_sections))

    empty_sections = [
        section
        for section, content in sections.items()
        if content is not None and not content.strip()
    ]
    if empty_sections:
        errors.append("必需章节内容为空：" + "、".join(empty_sections))

    findings_section = sections["## 关键发现"]
    if findings_section is not None:
        finding_matches = list(
            re.finditer(
                r"^### 发现[^\n]*$\n?(.*?)(?=^### [^#]|\Z)",
                findings_section,
                re.MULTILINE | re.DOTALL,
            )
        )
        if not finding_matches:
            errors.append("关键发现至少需要一个发现块")
        for index, finding_match in enumerate(finding_matches, start=1):
            block = finding_match.group(1)
            for label in FINDING_LABELS:
                label_match = re.search(
                    rf"^{re.escape(label)}[ \t]*(.+?)?[ \t]*$",
                    block,
                    re.MULTILINE,
                )
                value = label_match.group(1).strip() if label_match and label_match.group(1) else ""
                if not value:
                    errors.append(f"关键发现 {index} 缺少或留空标签：{label}")

    action_section = sections["## 行动建议"]
    if action_section is not None:
        lines = action_section.splitlines()
        if not any(parse_table_cells(line) == ACTION_HEADERS for line in lines):
            errors.append("行动建议表头必须严格匹配八个标准字段")
        elif action_table_issue(action_section) == "data":
            errors.append("行动建议缺少非空数据行")
        elif not has_contiguous_action_table(action_section):
            errors.append("行动建议缺少有效的连续表格")

    if any(marker in text for marker in UNRESOLVED_MARKERS):
        errors.append("存在未处理占位标记")

    if re.search(r"(?<!\w)\d+(?:\.\d+)?%(?!\w)", text) and not re.search(
        r"(样本|分母|n=|基数)", text, re.I
    ):
        warnings.append("报告包含比例，但未检测到样本或分母说明")

    return {
        "passed": not errors,
        "errors": errors,
        "warnings": warnings,
        "exit_code": 0 if not errors else 1,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate analysis report structure")
    parser.add_argument("report")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = validate(Path(args.report))
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("PASS" if result["passed"] else "FAIL")
        for error in result["errors"]:
            print(f"ERROR: {error}")
        for warning in result["warnings"]:
            print(f"WARNING: {warning}")
    return result["exit_code"]


if __name__ == "__main__":
    raise SystemExit(main())
