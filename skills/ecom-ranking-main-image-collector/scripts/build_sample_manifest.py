#!/usr/bin/env python3
"""Build a numbered ecommerce main-image sample package from a raw image folder."""

from __future__ import annotations

import argparse
import csv
import re
import shutil
from pathlib import Path

try:
    from PIL import Image, ImageDraw
except Exception as exc:  # pragma: no cover
    raise SystemExit("Pillow is required. Install with: pip install pillow") from exc


IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".avif"}


def rank_from_name(path: Path, fallback: int) -> int:
    match = re.match(r"^(\d{1,4})", path.stem)
    return int(match.group(1)) if match else fallback


def fit_image(img: Image.Image, size: int) -> Image.Image:
    img = img.convert("RGB")
    img.thumbnail((size, size), Image.LANCZOS)
    canvas = Image.new("RGB", (size, size), "white")
    x = (size - img.width) // 2
    y = (size - img.height) // 2
    canvas.paste(img, (x, y))
    return canvas


def make_contact_sheet(rows: list[dict[str, str]], out_path: Path, thumb_size: int = 220, cols: int = 5) -> None:
    label_h = 34
    gap = 16
    margin = 20
    count = len(rows)
    sheet_rows = (count + cols - 1) // cols
    width = margin * 2 + cols * thumb_size + (cols - 1) * gap
    height = margin * 2 + sheet_rows * (thumb_size + label_h) + (sheet_rows - 1) * gap
    sheet = Image.new("RGB", (width, height), "#f7f8fa")
    draw = ImageDraw.Draw(sheet)

    for idx, row in enumerate(rows):
        r = idx // cols
        c = idx % cols
        x = margin + c * (thumb_size + gap)
        y = margin + r * (thumb_size + label_h + gap)
        with Image.open(row["normalized_path"]) as img:
            thumb = fit_image(img, thumb_size)
        sheet.paste(thumb, (x, y))
        draw.rectangle((x, y, x + thumb_size, y + thumb_size), outline="#d8dee8", width=1)
        label = f"{row['sample_id']} | rank {row['rank']}"
        draw.text((x + 8, y + thumb_size + 8), label, fill="#1f2937")

    sheet.save(out_path, quality=92)


def write_analysis_prompt(path: Path, platform: str, keyword: str, sample_note: str, sample_count: int) -> None:
    path.write_text(
        f"""# Codex 爆款主图样本分析提示词

平台：{platform}
关键词/类目：{keyword}
样本说明：{sample_note}
样本数量：{sample_count}

你现在是电商主图视觉拆解助手。

我给你一组商品主图样本。请不要评价品牌，也不要照抄任何文案。

请按下面维度逐张分析：
1. 产品主体占比
2. 主体位置和构图
3. 背景类型
4. 主文案数量
5. 核心卖点是否唯一
6. 是否使用数字、规格、价格或利益点
7. 是否有场景、人物、手部或使用动作
8. 是否有前后对比、痛点对比或效果暗示
9. 颜色数量和强调色
10. 搜索页 0.5 秒内最容易被看到的元素

然后输出：
- 逐图拆解表
- 出现频率最高的视觉规律
- 可以学习的结构
- 不能照抄的元素
- 适合写进公众号文章的 6-8 条爆款主图规律
- 一张“主图自检表”
""",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Build an ecommerce main-image sample manifest and contact sheet.")
    parser.add_argument("--input", required=True, help="Folder containing raw main images.")
    parser.add_argument("--output", required=True, help="Output folder.")
    parser.add_argument("--keyword", default="", help="Search keyword or category.")
    parser.add_argument("--platform", default="", help="Platform name, such as Tmall, Taobao, JD, PDD.")
    parser.add_argument("--sample-note", default="", help="Sampling note or source description.")
    args = parser.parse_args()

    input_dir = Path(args.input)
    output_dir = Path(args.output)
    normalized_dir = output_dir / "normalized_images"
    output_dir.mkdir(parents=True, exist_ok=True)
    normalized_dir.mkdir(parents=True, exist_ok=True)

    images = sorted([p for p in input_dir.iterdir() if p.suffix.lower() in IMAGE_EXTS])
    if not images:
        raise SystemExit(f"No images found in {input_dir}")

    rows: list[dict[str, str]] = []
    for idx, src in enumerate(images, start=1):
        rank = rank_from_name(src, idx)
        sample_id = f"S{idx:03d}"
        dst = normalized_dir / f"{sample_id}_rank{rank:03d}{src.suffix.lower()}"
        shutil.copy2(src, dst)
        with Image.open(src) as img:
            width, height = img.size
        rows.append(
            {
                "sample_id": sample_id,
                "rank": str(rank),
                "platform": args.platform,
                "keyword": args.keyword,
                "source_file": str(src),
                "normalized_path": str(dst),
                "width": str(width),
                "height": str(height),
                "sample_note": args.sample_note,
                "analysis_status": "pending",
            }
        )

    manifest_path = output_dir / "sample_manifest.csv"
    with manifest_path.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    contact_sheet_path = output_dir / "sample_contact_sheet.jpg"
    make_contact_sheet(rows, contact_sheet_path)
    prompt_path = output_dir / "codex_analysis_prompt.md"
    write_analysis_prompt(prompt_path, args.platform, args.keyword, args.sample_note, len(rows))

    print(f"images: {len(rows)}")
    print(f"manifest: {manifest_path}")
    print(f"contact_sheet: {contact_sheet_path}")
    print(f"prompt: {prompt_path}")


if __name__ == "__main__":
    main()
