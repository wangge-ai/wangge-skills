import argparse
import csv
import json
import math
import os
import shutil
import subprocess
import sys
import textwrap
import urllib.request
import wave
from dataclasses import dataclass
from datetime import date as date_cls
from pathlib import Path

import numpy as np
import pandas as pd
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
WORK_ROOT = Path(os.environ.get("WANGGE_VIDEO_OUTPUT", str(Path.cwd() / "outputs" / "data-video")))
WORK_DATA = WORK_ROOT / "data"
BUILD = WORK_ROOT / "build"
OUTPUTS = WORK_ROOT
VIDEOS = OUTPUTS / "videos"
COVERS = OUTPUTS / "covers"
STORYBOARDS = OUTPUTS / "storyboards"

STATCOUNTER_CHART = "https://gs.statcounter.com/chart.php"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"


TOPICS = {
    "ai_chatbots": {
        "index": "01",
        "title": "AI 聊天机器人份额 2025-2026",
        "subtitle": "ChatGPT 领先，但 Gemini、Perplexity、Copilot 正在追赶",
        "hook": "AI 工具大战，谁真正占据用户心智？",
        "source_page": "https://gs.statcounter.com/ai-chatbot-market-share",
        "source_label": "StatCounter Global Stats - AI Chatbot Market Share Worldwide",
        "stat": "ai_chatbot",
        "stat_display": "AI Chatbot Market Share",
        "from": "202504",
        "to": "202606",
        "include": [
            "ChatGPT",
            "Perplexity",
            "Google Gemini",
            "Microsoft Copilot",
            "Claude",
            "Deepseek",
            "Other",
        ],
        "top_n": 7,
        "duration": 42,
    },
    "search_engines": {
        "index": "02",
        "title": "全球搜索引擎份额 2009-2026",
        "subtitle": "AI 搜索很热，但传统搜索格局仍然极度集中",
        "hook": "从 Yahoo、Baidu 到 Bing，谁撼动过 Google？",
        "source_page": "https://gs.statcounter.com/search-engine-market-share",
        "source_label": "StatCounter Global Stats - Search Engine Market Share Worldwide",
        "stat": "search_engine",
        "stat_display": "Search Engine Market Share",
        "from": "200901",
        "to": "202606",
        "include": [
            "Google",
            "bing",
            "Yahoo!",
            "Baidu",
            "YANDEX",
            "DuckDuckGo",
            "Ask Jeeves",
            "AOL",
            "Naver",
            "Sogou",
        ],
        "top_n": 8,
        "duration": 48,
    },
    "social_media": {
        "index": "03",
        "title": "全球社交媒体份额 2009-2026",
        "subtitle": "老平台没有消失，新平台也在持续抢位",
        "hook": "十多年过去，社交平台的牌桌换了几轮？",
        "source_page": "https://gs.statcounter.com/social-media-stats",
        "source_label": "StatCounter Global Stats - Social Media Stats Worldwide",
        "stat": "social_media",
        "stat_display": "Social Media Stats",
        "from": "200901",
        "to": "202606",
        "include": [
            "Facebook",
            "Twitter",
            "Pinterest",
            "YouTube",
            "Instagram",
            "reddit",
            "Tumblr",
            "StumbleUpon",
            "Google+",
            "MySpace",
        ],
        "top_n": 8,
        "duration": 48,
    },
}


PALETTE = [
    "#00A1D6",
    "#FF6B6B",
    "#2EC4B6",
    "#FFB703",
    "#8338EC",
    "#3A86FF",
    "#FB5607",
    "#06D6A0",
    "#B5179E",
    "#6C757D",
]


def ensure_dirs() -> None:
    for path in [WORK_DATA, BUILD, OUTPUTS, VIDEOS, COVERS, STORYBOARDS]:
        path.mkdir(parents=True, exist_ok=True)


def find_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    candidates = [
        r"C:\Windows\Fonts\msyhbd.ttc" if bold else r"C:\Windows\Fonts\msyh.ttc",
        r"C:\Windows\Fonts\simhei.ttf",
        r"C:\Windows\Fonts\arialbd.ttf" if bold else r"C:\Windows\Fonts\arial.ttf",
    ]
    for item in candidates:
        if item and Path(item).exists():
            return ImageFont.truetype(item, size=size)
    return ImageFont.load_default()


FONTS = {
    "title": find_font(42, True),
    "subtitle": find_font(24, False),
    "body": find_font(24, False),
    "small": find_font(17, False),
    "rank_compact": find_font(21, True),
    "body_compact": find_font(21, False),
    "value_compact": find_font(21, True),
    "rank": find_font(26, True),
    "value": find_font(25, True),
    "date": find_font(62, True),
    "cover_title": find_font(58, True),
    "cover_subtitle": find_font(30, False),
}


def statcounter_url(topic: dict) -> str:
    chart_id = f"{topic['stat']}-ww-monthly-{topic['from']}-{topic['to']}"
    params = {
        "statType_hidden": topic["stat"],
        "region_hidden": "ww",
        "granularity": "monthly",
        "statDisplay": topic["stat_display"],
        "fromMonthYear": topic["from"],
        "toMonthYear": topic["to"],
        "csv": "1",
    }
    query = "&".join(f"{k}={urllib.parse.quote(str(v))}" for k, v in params.items())
    return f"{STATCOUNTER_CHART}?{chart_id}&{query}"


def download_csv(topic_key: str, topic: dict) -> Path:
    out = WORK_DATA / f"{topic_key}.csv"
    req = urllib.request.Request(
        statcounter_url(topic),
        headers={"User-Agent": USER_AGENT, "Referer": topic["source_page"]},
    )
    with urllib.request.urlopen(req, timeout=60) as response:
        data = response.read()
    text = data.decode("utf-8-sig")
    if not text.startswith('"Date"'):
        raise RuntimeError(f"Unexpected CSV response for {topic_key}: {text[:120]}")
    out.write_text(text, encoding="utf-8")
    return out


def clean_topic_data(topic_key: str, topic: dict, raw_path: Path) -> pd.DataFrame:
    df = pd.read_csv(raw_path)
    df = df.rename(columns={df.columns[0]: "Date"})
    df["Date"] = pd.to_datetime(df["Date"], format="%Y-%m")
    wanted = [col for col in topic["include"] if col in df.columns]
    if not wanted:
        numeric = [c for c in df.columns if c != "Date"]
        peaks = df[numeric].max(numeric_only=True).sort_values(ascending=False)
        wanted = list(peaks.head(topic["top_n"] + 2).index)
    cleaned = df[["Date"] + wanted].copy()
    for col in wanted:
        cleaned[col] = pd.to_numeric(cleaned[col], errors="coerce").fillna(0.0)
    cleaned.to_csv(WORK_DATA / f"{topic_key}_clean.csv", index=False, encoding="utf-8")
    return cleaned


def interp_rows(df: pd.DataFrame, frame_count: int) -> list[tuple[pd.Timestamp, dict[str, float]]]:
    value_cols = [c for c in df.columns if c != "Date"]
    if len(df) == 1:
        row = {c: float(df.iloc[0][c]) for c in value_cols}
        return [(df.iloc[0]["Date"], row) for _ in range(frame_count)]

    out = []
    max_pos = len(df) - 1
    for i in range(frame_count):
        pos = i * max_pos / max(1, frame_count - 1)
        lo = int(math.floor(pos))
        hi = min(max_pos, lo + 1)
        frac = pos - lo
        date = df.iloc[lo]["Date"] + (df.iloc[hi]["Date"] - df.iloc[lo]["Date"]) * frac
        vals = {}
        for col in value_cols:
            vals[col] = float(df.iloc[lo][col]) * (1 - frac) + float(df.iloc[hi][col]) * frac
        out.append((date, vals))
    return out


def draw_text_box(draw: ImageDraw.ImageDraw, xy: tuple[int, int], text: str, font, fill: str, max_width: int, line_gap: int = 6) -> int:
    x, y = xy
    lines = []
    current = ""
    for ch in text:
        probe = current + ch
        if draw.textlength(probe, font=font) <= max_width or not current:
            current = probe
        else:
            lines.append(current)
            current = ch
    if current:
        lines.append(current)
    for line in lines:
        draw.text((x, y), line, font=font, fill=fill)
        y += font.size + line_gap
    return y


def entity_colors(entities: list[str]) -> dict[str, str]:
    return {entity: PALETTE[i % len(PALETTE)] for i, entity in enumerate(entities)}


def draw_chart_frame(topic: dict, date, vals: dict[str, float], colors: dict[str, str], width: int, height: int) -> Image.Image:
    img = Image.new("RGB", (width, height), "#111827")
    draw = ImageDraw.Draw(img)

    # Background grid
    for x in range(0, width, 80):
        shade = "#182235" if (x // 80) % 2 == 0 else "#151E2F"
        draw.rectangle([x, 0, x + 80, height], fill=shade)

    draw.rectangle([0, 0, width, 96], fill="#0B1220")
    draw.text((44, 26), topic["title"], font=FONTS["title"], fill="#F8FAFC")
    draw.text((46, 74), topic["subtitle"], font=FONTS["small"], fill="#CBD5E1")

    date_label = pd.Timestamp(date).strftime("%Y-%m")
    date_w = draw.textlength(date_label, font=FONTS["date"])
    draw.text((width - date_w - 48, 20), date_label, font=FONTS["date"], fill="#E5E7EB")

    top_n = int(topic.get("top_n", 8))
    ranked = sorted(vals.items(), key=lambda item: item[1], reverse=True)[:top_n]
    max_value = max([v for _, v in ranked] + [1])
    left = 72
    top = 126
    chart_bottom = height - 82
    row_h = min(58, max(34, (chart_bottom - top) / max(1, top_n)))
    compact = row_h < 48
    rank_font = FONTS["rank_compact"] if compact else FONTS["rank"]
    label_font = FONTS["body_compact"] if compact else FONTS["body"]
    value_font = FONTS["value_compact"] if compact else FONTS["value"]
    label_left = left + 62
    label_max_width = 196
    bar_left = 350
    bar_right = width - 158
    bar_max = bar_right - bar_left
    bar_h = min(34, max(20, row_h * 0.58))
    text_y_offset = max(3, (row_h - label_font.size) / 2)
    bar_y_offset = max(4, (row_h - bar_h) / 2)

    for i, (name, value) in enumerate(ranked):
        y = top + i * row_h
        color = colors.get(name, PALETTE[i % len(PALETTE)])
        draw.text((left, y + text_y_offset), f"{i + 1:02d}", font=rank_font, fill="#94A3B8")
        label = fit_text(draw, name, label_font, label_max_width)
        draw.text((label_left, y + text_y_offset), label, font=label_font, fill="#F8FAFC")
        bar_w = int(bar_max * (value / max_value))
        bar_top = y + bar_y_offset
        bar_bottom = bar_top + bar_h
        draw.rounded_rectangle([bar_left, bar_top, bar_left + bar_w, bar_bottom], radius=7, fill=color)
        draw.rounded_rectangle([bar_left, bar_top, bar_right, bar_bottom], radius=7, outline="#334155", width=1)
        value_text = format_value(topic, value)
        value_w = draw.textlength(value_text, font=value_font)
        value_x = min(bar_left + bar_w + 12, width - value_w - 44)
        draw.text((value_x, y + text_y_offset), value_text, font=value_font, fill="#F8FAFC")

    draw.line([44, height - 54, width - 44, height - 54], fill="#334155", width=1)
    draw.text((44, height - 38), f"Source: {topic['source_label']} | Generated {date_cls.today().isoformat()}", font=FONTS["small"], fill="#94A3B8")
    footer = "workflow demo"
    footer_w = draw.textlength(footer, font=FONTS["small"])
    draw.text((width - footer_w - 44, height - 38), footer, font=FONTS["small"], fill="#64748B")
    return img


def format_value(topic: dict, value: float) -> str:
    divisor = float(topic.get("value_divisor", 1))
    precision = int(topic.get("value_precision", 2))
    suffix = topic.get("value_suffix", "%")
    scaled = value / divisor
    return f"{scaled:.{precision}f}{suffix}"


def fit_text(draw: ImageDraw.ImageDraw, text: str, font, max_width: int) -> str:
    if draw.textlength(text, font=font) <= max_width:
        return text
    ellipsis = "..."
    out = text
    while out and draw.textlength(out + ellipsis, font=font) > max_width:
        out = out[:-1]
    return (out.rstrip() + ellipsis) if out else ellipsis


def draw_title_card(topic: dict, width: int, height: int, colors: dict[str, str]) -> Image.Image:
    img = Image.new("RGB", (width, height), "#0B1220")
    draw = ImageDraw.Draw(img)
    for i, color in enumerate(list(colors.values())[:8]):
        x0 = int(width * (i / 8))
        draw.rectangle([x0, height - 96, x0 + width // 8 + 4, height], fill=color)
    draw.text((58, 72), "动态数据排行", font=FONTS["subtitle"], fill="#38BDF8")
    y = draw_text_box(draw, (58, 128), topic["title"], FONTS["cover_title"], "#F8FAFC", width - 116, 10)
    draw_text_box(draw, (62, y + 18), topic["hook"], FONTS["cover_subtitle"], "#CBD5E1", width - 124, 8)
    draw.text((62, height - 152), "公开数据 + 本地脚本生成 | 非搬运素材", font=FONTS["body"], fill="#E2E8F0")
    return img


def generate_bgm(path: Path, duration: float, sr: int = 44100) -> None:
    t = np.linspace(0, duration, int(sr * duration), endpoint=False)
    chords = [
        (220.0, 277.18, 329.63),
        (196.0, 246.94, 293.66),
        (174.61, 220.0, 261.63),
        (164.81, 207.65, 246.94),
    ]
    audio = np.zeros_like(t)
    seg = 4.0
    for i, freqs in enumerate(chords * int(math.ceil(duration / (seg * len(chords))))):
        start = int(i * seg * sr)
        end = min(len(t), int((i + 1) * seg * sr))
        if start >= len(t):
            break
        local_t = t[: end - start]
        wave_part = sum(np.sin(2 * np.pi * f * local_t) for f in freqs) / len(freqs)
        env = np.linspace(0.15, 0.8, end - start)
        env *= np.linspace(1.0, 0.35, end - start)
        audio[start:end] += wave_part * env
    beat = (np.sin(2 * np.pi * 2.0 * t) > 0.985).astype(float)
    audio += beat * 0.05
    audio = audio / max(1e-6, np.max(np.abs(audio))) * 0.16
    samples = np.int16(audio * 32767)
    with wave.open(str(path), "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(sr)
        wav.writeframes(samples.tobytes())


def render_video(topic_key: str, topic: dict, df: pd.DataFrame, fps: int = 15, width: int = 1280, height: int = 720) -> dict:
    slug = f"{topic['index']}_{topic_key}"
    frames_dir = BUILD / slug / "frames"
    if frames_dir.exists():
        shutil.rmtree(frames_dir)
    frames_dir.mkdir(parents=True)

    entities = [c for c in df.columns if c != "Date"]
    colors = entity_colors(entities)
    duration = int(topic["duration"])
    total_frames = duration * fps
    title_frames = 3 * fps
    chart_frames = max(1, total_frames - title_frames)

    title_card = draw_title_card(topic, width, height, colors)
    for frame_idx in range(title_frames):
        title_card.save(frames_dir / f"frame_{frame_idx:05d}.png")

    rows = interp_rows(df, chart_frames)
    last_img = None
    for idx, (date, vals) in enumerate(rows, start=title_frames):
        img = draw_chart_frame(topic, date, vals, colors, width, height)
        img.save(frames_dir / f"frame_{idx:05d}.png")
        last_img = img

    cover_path = COVERS / f"{slug}_cover.png"
    cover = draw_title_card(topic, width, height, colors)
    if last_img:
        # Small final-rank preview strip on cover.
        preview = last_img.crop((0, 108, width, 610)).resize((520, 204))
        cover.paste(preview, (width - 580, 326))
        ImageDraw.Draw(cover).rounded_rectangle([width - 590, 316, width - 48, 542], radius=10, outline="#334155", width=2)
    cover.save(cover_path)

    audio_path = BUILD / slug / "bgm.wav"
    generate_bgm(audio_path, duration)

    video_path = VIDEOS / f"{slug}.mp4"
    ffmpeg = shutil.which("ffmpeg") or "ffmpeg"
    cmd = [
        ffmpeg,
        "-y",
        "-framerate",
        str(fps),
        "-i",
        str(frames_dir / "frame_%05d.png"),
        "-i",
        str(audio_path),
        "-c:v",
        "libx264",
        "-pix_fmt",
        "yuv420p",
        "-c:a",
        "aac",
        "-b:a",
        "128k",
        "-shortest",
        str(video_path),
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    storyboard_path = STORYBOARDS / f"{slug}_storyboard.csv"
    write_storyboard(topic, df, storyboard_path, duration)

    return {
        "slug": slug,
        "video": str(video_path),
        "cover": str(cover_path),
        "storyboard": str(storyboard_path),
        "clean_csv": str(WORK_DATA / f"{topic_key}_clean.csv"),
        "duration_seconds": duration,
        "fps": fps,
        "source_page": topic["source_page"],
    }


def write_storyboard(topic: dict, df: pd.DataFrame, path: Path, duration: int) -> None:
    latest = df.iloc[-1].drop(labels=["Date"]).sort_values(ascending=False).head(5)
    def stamp(seconds):
        seconds = max(0, min(int(seconds), max(0, duration - 1)))
        return f"{seconds // 60:02d}:{seconds % 60:02d}"

    beats = [
        (stamp(0), "标题钩子", topic["hook"], "原创轻 BGM 起"),
        (stamp(3), "动态排行开始", f"从 {df.iloc[0]['Date'].strftime('%Y-%m')} 开始播放月度份额变化", "保持稳定节奏"),
        (stamp(duration / 3), "中段观察", "关注排名变化、追赶者和突然上升的平台", "可加解说"),
        (stamp(duration * 2 / 3), "末段冲刺", f"最新 Top5: {', '.join(latest.index)}", "音乐稍增强"),
        (stamp(duration - 4), "结尾定格", "显示最新月份排名和数据来源", "收尾"),
    ]
    with path.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["timecode", "scene", "visual_state", "audio_note"])
        writer.writerows(beats)


def ffprobe_video(path: str) -> dict:
    ffprobe = shutil.which("ffprobe") or "ffprobe"
    cmd = [
        ffprobe,
        "-v",
        "error",
        "-show_entries",
        "format=duration:stream=codec_type,width,height,r_frame_rate",
        "-of",
        "json",
        path,
    ]
    result = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return json.loads(result.stdout)


def main() -> int:
    parser = argparse.ArgumentParser(description="Build TOP10stats-style data ranking videos.")
    parser.add_argument("--topics", nargs="*", default=list(TOPICS.keys()), choices=list(TOPICS.keys()))
    parser.add_argument("--skip-fetch", action="store_true")
    parser.add_argument("--fps", type=int, default=15)
    args = parser.parse_args()

    ensure_dirs()
    manifest = {
        "generated_at": date_cls.today().isoformat(),
        "workflow": "fetch StatCounter CSV -> clean data -> draw frames -> synthesize original BGM -> ffmpeg MP4",
        "topics": [],
    }

    for topic_key in args.topics:
        topic = TOPICS[topic_key]
        raw_path = WORK_DATA / f"{topic_key}.csv"
        if not args.skip_fetch or not raw_path.exists():
            raw_path = download_csv(topic_key, topic)
        df = clean_topic_data(topic_key, topic, raw_path)
        item = render_video(topic_key, topic, df, fps=args.fps)
        item["probe"] = ffprobe_video(item["video"])
        manifest["topics"].append(item)

    manifest_path = OUTPUTS / "video_production_manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(manifest, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
