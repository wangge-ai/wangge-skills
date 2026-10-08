#!/usr/bin/env python3
"""Render exact title text onto a WeChat Official Account cover image."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps


DEFAULT_SIZE = (900, 383)


def parse_size(value: str) -> tuple[int, int]:
    match = re.fullmatch(r"(\d+)x(\d+)", value.strip().lower())
    if not match:
        raise argparse.ArgumentTypeError("size must look like 900x383")
    width, height = int(match.group(1)), int(match.group(2))
    if width < 320 or height < 160:
        raise argparse.ArgumentTypeError("size is too small for a readable cover")
    return width, height


def parse_hex(value: str) -> tuple[int, int, int]:
    value = value.strip()
    if not re.fullmatch(r"#?[0-9a-fA-F]{6}", value):
        raise argparse.ArgumentTypeError("color must be a 6-digit hex value")
    value = value.lstrip("#")
    return tuple(int(value[i : i + 2], 16) for i in (0, 2, 4))


def find_font(bold: bool = True) -> str | None:
    candidates = [
        r"C:\Windows\Fonts\msyhbd.ttc" if bold else r"C:\Windows\Fonts\msyh.ttc",
        r"C:\Windows\Fonts\simhei.ttf",
        r"C:\Windows\Fonts\simsun.ttc",
        r"C:\Windows\Fonts\arialbd.ttf" if bold else r"C:\Windows\Fonts\arial.ttf",
    ]
    for candidate in candidates:
        if candidate and Path(candidate).exists():
            return candidate
    return None


def load_font(size: int, bold: bool = True) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    font_path = find_font(bold)
    if font_path:
        return ImageFont.truetype(font_path, size=size)
    return ImageFont.load_default(size=size)


def text_size(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont, stroke_width: int = 0) -> tuple[int, int]:
    bbox = draw.textbbox((0, 0), text, font=font, stroke_width=stroke_width)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]


def tokenize_line(text: str) -> list[str]:
    """Keep ASCII words like GitHub together while allowing CJK character wrapping."""
    tokens: list[str] = []
    index = 0
    while index < len(text):
        char = text[index]
        if char.isspace():
            tokens.append(char)
            index += 1
            continue
        if re.match(r"[A-Za-z0-9_.+/#-]", char):
            end = index + 1
            while end < len(text) and re.match(r"[A-Za-z0-9_.+/#-]", text[end]):
                end += 1
            tokens.append(text[index:end])
            index = end
            continue
        tokens.append(char)
        index += 1
    return tokens


def wrap_text(draw: ImageDraw.ImageDraw, title: str, font: ImageFont.ImageFont, max_width: int) -> list[str]:
    explicit_lines = [line.strip() for line in title.replace("\\n", "\n").splitlines() if line.strip()]
    lines: list[str] = []
    for source_line in explicit_lines or [title.strip()]:
        current = ""
        for token in tokenize_line(source_line):
            trial = current + token
            if current and text_size(draw, trial, font)[0] > max_width:
                lines.append(current.rstrip())
                current = token.lstrip()
            else:
                current = trial
        if current.strip():
            lines.append(current.strip())
    return lines


def fit_title(
    draw: ImageDraw.ImageDraw,
    title: str,
    max_width: int,
    max_height: int,
    max_font: int,
    min_font: int,
) -> tuple[ImageFont.ImageFont, list[str], int]:
    fallback: tuple[ImageFont.ImageFont, list[str], int] | None = None
    for size in range(max_font, min_font - 1, -2):
        font = load_font(size, bold=True)
        lines = wrap_text(draw, title, font, max_width)
        line_gap = max(6, int(size * 0.18))
        heights = [text_size(draw, line, font, stroke_width=2)[1] for line in lines]
        total_height = sum(heights) + line_gap * max(0, len(lines) - 1)
        widest = max((text_size(draw, line, font, stroke_width=2)[0] for line in lines), default=0)
        if total_height <= max_height and widest <= max_width:
            candidate = (font, lines, line_gap)
            if fallback is None:
                fallback = candidate
            has_orphan = any(len(line.strip()) <= 2 for line in lines[1:])
            if not has_orphan:
                return candidate
    if fallback is not None:
        return fallback
    font = load_font(min_font, bold=True)
    return font, wrap_text(draw, title, font, max_width), max(6, int(min_font * 0.18))


def average_luma(image: Image.Image, box: tuple[int, int, int, int]) -> float:
    crop = image.crop(box).resize((1, 1)).convert("RGB")
    r, g, b = crop.getpixel((0, 0))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def rounded_panel(size: tuple[int, int], radius: int, color: tuple[int, int, int, int]) -> Image.Image:
    panel = Image.new("RGBA", size, (0, 0, 0, 0))
    mask = Image.new("L", size, 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.rounded_rectangle((0, 0, size[0] - 1, size[1] - 1), radius=radius, fill=255)
    color_layer = Image.new("RGBA", size, color)
    panel.alpha_composite(color_layer)
    panel.putalpha(mask)
    return panel


def add_soft_panel(
    cover: Image.Image,
    box: tuple[int, int, int, int],
    radius: int,
    color: tuple[int, int, int, int],
    blur: int,
) -> None:
    overlay = Image.new("RGBA", cover.size, (0, 0, 0, 0))
    mask = Image.new("L", cover.size, 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.rounded_rectangle(box, radius=radius, fill=color[3])
    mask = mask.filter(ImageFilter.GaussianBlur(radius=blur))
    color_layer = Image.new("RGBA", cover.size, (*color[:3], 0))
    color_layer.putalpha(mask)
    overlay.alpha_composite(color_layer)
    cover.alpha_composite(overlay)


def draw_cover(args: argparse.Namespace) -> None:
    width, height = args.size
    source = Image.open(args.background).convert("RGB")
    cover = ImageOps.fit(source, (width, height), method=Image.Resampling.LANCZOS, centering=(0.5, 0.5)).convert("RGBA")

    safe_x = int(width * 0.07)
    safe_y = int(height * 0.11)
    block_width = int(width * args.block_ratio)
    if args.position == "center":
        block_width = int(width * 0.72)
        x = (width - block_width) // 2
    elif args.position == "right":
        x = width - safe_x - block_width
    else:
        x = safe_x

    kicker_height = int(height * 0.11) if args.kicker else 0
    max_title_height = height - safe_y * 2 - kicker_height
    probe = ImageDraw.Draw(cover)
    font, lines, line_gap = fit_title(
        probe,
        args.title,
        block_width,
        max_title_height,
        max_font=int(height * 0.16),
        min_font=max(24, int(height * 0.07)),
    )

    line_metrics = [text_size(probe, line, font, stroke_width=2) for line in lines]
    title_height = sum(h for _, h in line_metrics) + line_gap * max(0, len(lines) - 1)
    content_height = title_height + kicker_height
    y = (height - content_height) // 2

    panel_pad_x = int(width * 0.035)
    panel_pad_y = int(height * 0.055)
    actual_title_width = max((metric[0] for metric in line_metrics), default=block_width)
    panel_content_width = min(block_width, actual_title_width)
    panel_box = (
        max(0, x - panel_pad_x),
        max(0, y - panel_pad_y),
        min(width, x + panel_content_width + panel_pad_x),
        min(height, y + content_height + panel_pad_y),
    )

    theme = args.theme
    if theme == "auto":
        theme = "dark" if average_luma(cover, panel_box) < 128 else "light"

    panel_style = "none" if args.no_panel else args.panel_style
    if theme == "dark":
        text_color = (255, 255, 255)
        stroke_color = (8, 13, 22)
        panel_color = (2, 8, 18, 96 if panel_style == "soft" else 150)
        kicker_color = args.accent
    else:
        text_color = (18, 24, 38)
        stroke_color = (255, 255, 255)
        panel_color = (255, 255, 255, 138 if panel_style == "soft" else 178)
        kicker_color = args.accent

    if panel_style == "soft":
        add_soft_panel(
            cover,
            panel_box,
            radius=max(20, int(height * 0.07)),
            color=panel_color,
            blur=max(10, int(height * 0.035)),
        )
    elif panel_style == "card":
        panel_w = panel_box[2] - panel_box[0]
        panel_h = panel_box[3] - panel_box[1]
        panel = rounded_panel((panel_w, panel_h), radius=max(14, int(height * 0.04)), color=panel_color)
        panel = panel.filter(ImageFilter.GaussianBlur(radius=0.15))
        cover.alpha_composite(panel, (panel_box[0], panel_box[1]))

    draw = ImageDraw.Draw(cover)
    if args.kicker:
        kicker_font = load_font(max(18, int(height * 0.045)), bold=True)
        tag_pad_x = 16
        tag_pad_y = 8
        kw, kh = text_size(draw, args.kicker, kicker_font)
        tag_box = (x, y, x + kw + tag_pad_x * 2, y + kh + tag_pad_y * 2)
        tag_fill = (*kicker_color, 226)
        draw.rounded_rectangle(tag_box, radius=10, fill=tag_fill)
        draw.text((x + tag_pad_x, y + tag_pad_y - 1), args.kicker, font=kicker_font, fill=(255, 255, 255))
        y += kh + tag_pad_y * 2 + int(height * 0.035)

    accent_bar_width = max(5, int(width * 0.007))
    draw.rounded_rectangle(
        (x - int(width * 0.022), y + 4, x - int(width * 0.022) + accent_bar_width, y + title_height - 2),
        radius=accent_bar_width,
        fill=(*args.accent, 245),
    )

    current_y = y
    stroke_width = 1 if panel_style == "soft" else 2
    for idx, line in enumerate(lines):
        _, line_h = line_metrics[idx]
        draw.text(
            (x, current_y),
            line,
            font=font,
            fill=text_color,
            stroke_width=stroke_width,
            stroke_fill=stroke_color,
        )
        current_y += line_h + line_gap

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    cover.convert("RGB").save(out, quality=95)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--background", required=True, help="Path to the generated background image.")
    parser.add_argument("--title", required=True, help="Exact title text to render.")
    parser.add_argument("--out", required=True, help="Output image path.")
    parser.add_argument("--size", type=parse_size, default=DEFAULT_SIZE, help="Output size, default 900x383.")
    parser.add_argument("--position", choices=["left", "center", "right"], default="left", help="Title block position.")
    parser.add_argument("--theme", choices=["auto", "light", "dark"], default="auto", help="Text color theme.")
    parser.add_argument("--accent", type=parse_hex, default=(34, 197, 94), help="Accent color hex, default #22c55e.")
    parser.add_argument("--kicker", default="", help="Optional small label above the title.")
    parser.add_argument("--no-panel", action="store_true", help="Disable translucent readability panel.")
    parser.add_argument(
        "--panel-style",
        choices=["soft", "card"],
        default="soft",
        help="Title backing style. Use soft by default so text blends into the image.",
    )
    parser.add_argument(
        "--block-ratio",
        type=float,
        default=0.5,
        help="Maximum title block width as a fraction of cover width, default 0.5.",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    draw_cover(args)


if __name__ == "__main__":
    main()
