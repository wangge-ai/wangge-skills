import argparse
import csv
import json
import re
from pathlib import Path


HERE = Path(__file__).resolve().parent

GENERIC_KEYWORDS = {
    "经济",
    "国家",
    "增长",
    "排行",
    "排名",
    "数据",
    "全球",
    "中国",
    "城市",
    "热度",
}


def split_pipe(value: str) -> list[str]:
    return [item.strip() for item in str(value or "").split("|") if item.strip()]


def default_candidates(filename: str) -> list[Path]:
    candidates = [
        HERE.parent / "references" / filename,
        HERE.parent / "references" / filename.replace("hotspot-to-video-routing", "热点到数据视频路由表"),
        HERE.parent / "references" / filename.replace("official-data-source-library", "官方专业数据源库"),
    ]
    if len(HERE.parents) >= 3:
        project_root = HERE.parents[2]
        candidates.extend(
            [
                project_root / "outputs" / filename,
                project_root / "outputs" / filename.replace("hotspot-to-video-routing", "热点到数据视频路由表"),
                project_root / "outputs" / filename.replace("official-data-source-library", "官方专业数据源库"),
            ]
        )
    candidates.extend(
        [
            Path.cwd() / filename,
            Path.cwd() / filename.replace("hotspot-to-video-routing", "热点到数据视频路由表"),
            Path.cwd() / filename.replace("official-data-source-library", "官方专业数据源库"),
        ]
    )
    return candidates


def first_existing(candidates: list[Path]) -> Path:
    for path in candidates:
        if path.exists():
            return path
    joined = "\n".join(str(path) for path in candidates)
    raise FileNotFoundError(f"No route/source file found. Checked:\n{joined}")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def match_route(row: dict[str, str], hotspot: str) -> tuple[int, list[str]]:
    haystack = hotspot.lower()
    matched = []
    score = 0
    for keyword in split_pipe(row.get("trigger_keywords", "")):
        if keyword.lower() in haystack:
            matched.append(keyword)
            score += 1 if keyword in GENERIC_KEYWORDS else 4
    topic_type = str(row.get("hot_topic_type", ""))
    if topic_type and topic_type.lower() in haystack:
        score += 2
    for word in re.findall(r"[\w\u4e00-\u9fff]+", topic_type):
        if word and word.lower() in haystack:
            score += 1
    return score, matched


def source_score(row: dict[str, str], names: list[str], keywords: list[str]) -> int:
    source_name = str(row.get("source_name", "")).lower()
    hot_keywords = str(row.get("hot_keywords", "")).lower()
    hot_tokens = {item.lower() for item in split_pipe(row.get("hot_keywords", ""))}
    score = 0
    for name in names:
        low = name.lower()
        if low and (low in source_name or source_name in low):
            score += 6
    for keyword in keywords:
        low = keyword.lower()
        if re.fullmatch(r"[a-z0-9]+", low):
            matched = low in hot_tokens
        else:
            matched = low in hot_keywords
        if matched:
            score += 2
    return score


def pick_sources(source_rows: list[dict[str, str]], route: dict[str, str], matched_keywords: list[str], limit: int) -> list[dict[str, str]]:
    preferred_names = split_pipe(route.get("preferred_sources", ""))
    keywords = matched_keywords + split_pipe(route.get("trigger_keywords", ""))
    scored = []
    for row in source_rows:
        score = source_score(row, preferred_names, keywords)
        if score:
            scored.append((score, row))
    if any(score >= 6 for score, _ in scored):
        scored = [(score, row) for score, row in scored if score >= 6]
    scored.sort(key=lambda item: item[0], reverse=True)
    return [
        {
            "category": row.get("category", ""),
            "source_name": row.get("source_name", ""),
            "official_level": row.get("official_level", ""),
            "home_url": row.get("home_url", ""),
            "api_or_download": row.get("api_or_download", ""),
            "typical_metrics": row.get("typical_metrics", ""),
            "notes": row.get("notes", ""),
            "last_reviewed": row.get("last_reviewed", ""),
            "refresh_cadence": row.get("refresh_cadence", ""),
            "source_mode": row.get("source_mode", ""),
            "live_search_query": row.get("live_search_query", ""),
        }
        for _, row in scored[:limit]
    ]


def generic_live_queries(hotspot: str) -> list[str]:
    return [
        f"{hotspot} 官方 数据 API CSV 下载",
        f"{hotspot} official data API csv dataset",
        f"{hotspot} statistics official source download",
        f"{hotspot} 数据源 官方 统计 公开数据",
    ]


def live_search_plan(hotspot: str) -> dict:
    return {
        "hotspot": hotspot,
        "topic_type": "未命中本地路由，需要联网搜索补源",
        "matched_keywords": [],
        "recommended_video_format": "先按搜到的数据形态选择：动态排行、快照榜、对比图、结构图、地图或指标卡",
        "expected_data_shape": "unknown until live source discovery",
        "preferred_sources": [],
        "backup_sources": [],
        "source_candidates": [],
        "needs_live_source_search": True,
        "live_search_required_when": "本地路由和种子数据源没有覆盖该热点",
        "live_search_queries": generic_live_queries(hotspot),
        "example_titles": [],
        "quality_gate": "必须先找到可复查的官方或专业来源；只找到二手截图、营销稿或无口径网页时不要制作",
        "next_steps": [
            "联网搜索官方/国际机构/专业数据库，优先找 API、CSV、下载页或方法论页面。",
            "记录新来源的发布机构、链接、口径、单位、更新时间和限制。",
            "把确认可用的新来源回写到 official-data-source-library.csv，并补充热点路由表。",
            "再根据数据形态选择视频模板，不要硬套动态年度排行。",
        ],
    }


def build_plan(hotspot: str, route: dict[str, str], matched_keywords: list[str], source_rows: list[dict[str, str]], source_limit: int) -> dict:
    preferred_sources = split_pipe(route.get("preferred_sources", ""))
    backup_sources = split_pipe(route.get("backup_sources", ""))
    source_candidates = pick_sources(source_rows, route, matched_keywords, source_limit) if source_rows else []
    route_queries = split_pipe(route.get("live_search_queries", "")) or generic_live_queries(hotspot)
    needs_live_source_search = not source_candidates
    return {
        "hotspot": hotspot,
        "topic_type": route.get("hot_topic_type", ""),
        "matched_keywords": matched_keywords,
        "recommended_video_format": route.get("default_video_format", ""),
        "expected_data_shape": route.get("data_shape", ""),
        "preferred_sources": preferred_sources,
        "backup_sources": backup_sources,
        "source_candidates": source_candidates,
        "needs_live_source_search": needs_live_source_search,
        "source_mode": route.get("source_mode", "先查种子库；不命中、过期或口径不合适时必须联网搜索补源"),
        "live_search_required_when": route.get(
            "live_search_required_when",
            "热点未命中本表|首选来源不可用|来源超过刷新周期|数据没有所需时间/地区/对象|只有二手截图或无法复查",
        ),
        "live_search_queries": route_queries,
        "example_titles": split_pipe(route.get("example_titles", "")),
        "quality_gate": route.get("quality_gate", ""),
        "next_steps": [
            "确认热点是否适合数据化：是否有可复查数据、是否能做排名/趋势/对比。",
            "先核对 source_candidates 的链接和刷新规则；不可用或不覆盖时，按 live_search_queries 联网补源。",
            "记录链接、单位、口径、抓取日期和来源类型，并把新增来源回写到数据源库。",
            "按 expected_data_shape 清洗成 Date + entity columns 或事件表。",
            "按 recommended_video_format 选择动态排行、快照榜、对比图、结构图、地图或指标卡模板。",
        ],
    }


def route_hotspot(hotspot: str, routes: list[dict[str, str]], source_rows: list[dict[str, str]], limit: int, source_limit: int) -> list[dict]:
    scored = []
    for row in routes:
        score, matched_keywords = match_route(row, hotspot)
        if score >= 3:
            scored.append((score, row, matched_keywords))
    if not scored:
        return [live_search_plan(hotspot)]
    scored.sort(key=lambda item: item[0], reverse=True)
    return [build_plan(hotspot, row, matched, source_rows, source_limit) for _, row, matched in scored[:limit]]


def read_hotspots(args: argparse.Namespace) -> list[str]:
    hotspots = list(args.hotspot or [])
    if args.hotspots_file:
        path = Path(args.hotspots_file)
        hotspots.extend([line.strip() for line in path.read_text(encoding="utf-8-sig").splitlines() if line.strip()])
    return hotspots


def main() -> int:
    parser = argparse.ArgumentParser(description="Route hot topics to official data sources and video formats.")
    parser.add_argument("--hotspot", action="append", help="Hot topic title or keywords. Can be passed multiple times.")
    parser.add_argument("--hotspots-file", help="UTF-8 text file with one hotspot per line.")
    parser.add_argument("--route-table", help="CSV route table. Defaults to references/ or outputs/ hotspot route table.")
    parser.add_argument("--source-library", help="CSV source library. Defaults to references/ or outputs/ official source library.")
    parser.add_argument("--limit", type=int, default=3, help="Route matches to return per hotspot.")
    parser.add_argument("--source-limit", type=int, default=6, help="Source candidates to return per route.")
    parser.add_argument("--json-out", help="Optional path to write the JSON plan.")
    args = parser.parse_args()

    hotspots = read_hotspots(args)
    if not hotspots:
        parser.error("Pass --hotspot or --hotspots-file.")

    route_path = Path(args.route_table) if args.route_table else first_existing(default_candidates("hotspot-to-video-routing.csv"))
    source_path = Path(args.source_library) if args.source_library else first_existing(default_candidates("official-data-source-library.csv"))
    routes = read_csv(route_path)
    source_rows = read_csv(source_path)

    payload = {
        "route_table": str(route_path),
        "source_library": str(source_path),
        "plans": [route_hotspot(hotspot, routes, source_rows, args.limit, args.source_limit) for hotspot in hotspots],
    }
    text = json.dumps(payload, ensure_ascii=False, indent=2)
    if args.json_out:
        Path(args.json_out).write_text(text, encoding="utf-8")
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
