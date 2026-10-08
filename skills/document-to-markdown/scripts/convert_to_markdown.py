#!/usr/bin/env python
from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlparse


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")


SUPPORTED_EXTENSIONS = {
    ".pdf",
    ".docx",
    ".pptx",
    ".xlsx",
    ".xls",
    ".csv",
    ".html",
    ".htm",
    ".txt",
    ".json",
    ".xml",
    ".md",
    ".jpg",
    ".jpeg",
    ".png",
    ".gif",
    ".bmp",
    ".tiff",
    ".tif",
    ".wav",
    ".mp3",
    ".m4a",
    ".mp4",
}

SENTENCE_END_RE = re.compile(r"[\.\!\?\;\:\)\]\}\"'\u3002\uff01\uff1f\uff1b\uff1a\uff09\u3011\u300d\u300f\u201d\u2019\u300b\u2026]$")
LIST_MARKER_RE = re.compile(r"^(\d+[\.\)]|\d+\u3001|[-*+])\s*")
TAIL_MARKER_RE = re.compile(
    r"(\u6240\u6709\u7684\u4ed8\u8d39\u6587\u7ae0|\u559c\u6b22\u4f5c\u8005|\u70b9\u8d5e|\u5199\u7559\u8a00|\u4f5c\u8005\u63d0\u793a)"
)


class ChineseArgumentParser(argparse.ArgumentParser):
    def format_usage(self) -> str:
        return super().format_usage().replace("usage:", "用法：", 1)

    def format_help(self) -> str:
        return super().format_help().replace("usage:", "用法：", 1)


def is_url(value: str) -> bool:
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def slug_from_source(value: str) -> str:
    if is_url(value):
        parsed = urlparse(value)
        raw = f"{parsed.netloc}-{parsed.path.strip('/') or 'index'}"
    else:
        raw = Path(value).stem
    slug = re.sub(r"[^\w\-.]+", "-", raw, flags=re.UNICODE).strip("-_.")
    return slug or "转换结果"


def output_for(source: str, output: Path | None, source_count: int) -> Path:
    if output is None:
        if is_url(source):
            return Path.cwd() / f"{slug_from_source(source)}.md"
        return Path(source).with_suffix(".md")

    if source_count == 1 and output.suffix.lower() == ".md":
        return output

    return output / f"{slug_from_source(source)}.md"


def expand_sources(values: list[str], recursive: bool) -> list[str]:
    expanded: list[str] = []
    for value in values:
        if is_url(value):
            expanded.append(value)
            continue

        path = Path(value).expanduser()
        if path.is_dir():
            iterator = path.rglob("*") if recursive else path.glob("*")
            for child in sorted(iterator):
                if child.is_file() and child.suffix.lower() in SUPPORTED_EXTENSIONS:
                    expanded.append(str(child))
            continue

        expanded.append(str(path))
    return expanded


def should_clean(source: str, clean_mode: str) -> bool:
    if clean_mode == "always":
        return True
    if clean_mode == "never":
        return False
    if is_url(source):
        return False
    return Path(source).suffix.lower() == ".pdf"


def ends_sentence(line: str) -> bool:
    return bool(SENTENCE_END_RE.search(line.rstrip()))


def should_join(previous: str, current: str) -> bool:
    prev = previous.rstrip()
    cur = current.lstrip()
    if not prev or not cur:
        return False
    if ends_sentence(prev):
        return False
    if LIST_MARKER_RE.match(cur) and len(prev) < 24:
        return False
    if len(prev) <= 12 and len(cur) <= 20 and not LIST_MARKER_RE.match(prev):
        return False
    return True


def join_lines(previous: str, current: str) -> str:
    if re.search(r"[A-Za-z0-9]$", previous) and re.search(r"^[A-Za-z0-9]", current):
        return f"{previous} {current}"
    return f"{previous}{current}"


def clean_pdf_markdown(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n").replace("\x0c", "\n")
    lines = [line.strip() for line in text.split("\n")]
    lines = [line for line in lines if line]
    if not lines:
        return ""

    tail_start = len(lines)
    for index, line in enumerate(lines):
        if TAIL_MARKER_RE.search(line):
            tail_start = index
            break

    tail_lines = lines[tail_start:]
    lines = lines[:tail_start]

    body_start = 0
    for index, line in enumerate(lines):
        if len(line) >= 8 and ends_sentence(line):
            body_start = index
            break

    paragraphs: list[str] = []
    paragraphs.extend(lines[:body_start])

    current = ""
    for line in lines[body_start:]:
        if not current:
            current = line
            continue
        if should_join(current, line):
            current = join_lines(current, line)
        else:
            paragraphs.append(current)
            current = line

    if current:
        paragraphs.append(current)

    paragraphs.extend(tail_lines)

    return "\n\n".join(paragraphs).strip() + "\n"


def run_markitdown(markitdown: str, source: str, output: Path) -> tuple[int, str, str]:
    output.parent.mkdir(parents=True, exist_ok=True)
    command = [markitdown, source, "-o", str(output)]
    completed = subprocess.run(
        command,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        text=True,
    )
    return completed.returncode, completed.stdout, completed.stderr


def convert_one(markitdown: str, source: str, output: Path, clean_mode: str, keep_raw: bool) -> int:
    clean = should_clean(source, clean_mode)
    raw_output = output.with_suffix(".raw.md") if clean and keep_raw else output

    code, stdout, stderr = run_markitdown(markitdown, source, raw_output)
    if stdout.strip():
        print(stdout.strip())
    if stderr.strip():
        print(stderr.strip(), file=sys.stderr)
    if code != 0:
        return code

    if clean:
        raw_text = raw_output.read_text(encoding="utf-8", errors="replace")
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(clean_pdf_markdown(raw_text), encoding="utf-8")

    print(f"[完成] {source} -> {output}")
    return 0


def parse_args() -> argparse.Namespace:
    parser = ChineseArgumentParser(
        description="使用 MarkItDown 将文档和网页文件转换为 Markdown。",
        add_help=False,
    )
    parser._positionals.title = "位置参数"
    parser._optionals.title = "选项"
    parser.add_argument("sources", metavar="源", nargs="+", help="要转换的文件、文件夹或 URL。")
    parser.add_argument("-h", "--help", action="help", help="显示帮助信息并退出。")
    parser.add_argument("-o", "--output", metavar="输出路径", type=Path, help="单个源文件时可填输出 .md 路径；批量转换时填写输出文件夹。")
    parser.add_argument("--recursive", action="store_true", help="转换文件夹时递归处理子文件夹。")
    parser.add_argument("--clean", choices=["auto", "always", "never"], default="auto", help="断行清理模式。")
    parser.add_argument("--no-clean", action="store_true", help="等同于 --clean never，保留原始转换结果。")
    parser.add_argument("--keep-raw", action="store_true", help="清理前额外保留一份 .raw.md 原始转换稿。")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    clean_mode = "never" if args.no_clean else args.clean
    markitdown = shutil.which("markitdown")
    if not markitdown:
        managed_markitdown = (
            Path.home()
            / ".codex"
            / "tool-runtimes"
            / "markitdown"
            / "Scripts"
            / "markitdown.exe"
        )
        if managed_markitdown.is_file():
            markitdown = str(managed_markitdown)
    if not markitdown:
        print('未找到 markitdown。可用这个命令安装：python -m pip install "markitdown[all]"', file=sys.stderr)
        return 127

    sources = expand_sources(args.sources, args.recursive)
    if not sources:
        print("没有找到可转换的输入文件。", file=sys.stderr)
        return 2

    if len(sources) > 1 and args.output and args.output.suffix.lower() == ".md":
        print("转换多个源文件时，--output 必须是文件夹。", file=sys.stderr)
        return 2

    failures = 0
    for source in sources:
        if not is_url(source) and not Path(source).exists():
            print(f"源文件不存在：{source}", file=sys.stderr)
            failures += 1
            continue
        destination = output_for(source, args.output, len(sources))
        code = convert_one(markitdown, source, destination, clean_mode, args.keep_raw)
        if code != 0:
            failures += 1

    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
