#!/usr/bin/env python3
"""Fetch compact GitHub repository stats for github-repo-dissector.

Uses only the Python standard library. Set GITHUB_TOKEN to raise API limits.
"""

from __future__ import annotations

import argparse
import datetime as dt
from html.parser import HTMLParser
import http.client
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from typing import Any


API = "https://api.github.com"
AI_KEYWORDS = (
    "ai",
    "agent",
    "agents",
    "agentic",
    "llm",
    "mcp",
    "claude",
    "codex",
    "cursor",
    "gemini",
    "openai",
    "gpt",
    "rag",
    "prompt",
    "prompts",
    "skill",
    "skills",
    "model",
    "models",
    "inference",
    "embedding",
    "vector",
    "diffusion",
    "image generation",
    "computer use",
    "browser automation",
    "voice",
    "tts",
)
NON_REPO_PATH_PREFIXES = {
    "account",
    "apps",
    "collections",
    "customer-stories",
    "enterprise",
    "events",
    "explore",
    "features",
    "github",
    "login",
    "marketplace",
    "new",
    "notifications",
    "orgs",
    "pricing",
    "sponsors",
    "topics",
    "trending",
}

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")


def parse_repo(value: str) -> tuple[str, str]:
    value = value.strip().rstrip("/")
    if value.startswith("http"):
        parsed = urllib.parse.urlparse(value)
        if parsed.scheme not in {"http", "https"} or parsed.hostname not in {"github.com", "www.github.com"}:
            raise SystemExit(f"Repository URL must use github.com: {value}")
        if parsed.username or parsed.password:
            raise SystemExit("Repository URL must not include embedded credentials")
        parts = [p for p in parsed.path.split("/") if p]
        if len(parts) != 2:
            raise SystemExit(f"Cannot parse repository from URL: {value}")
        return parts[0], parts[1].removesuffix(".git")
    if re.match(r"^[^/\s]+/[^/\s]+$", value):
        owner, repo = value.split("/", 1)
        return owner, repo.removesuffix(".git")
    raise SystemExit("Repository must be a GitHub URL or owner/repo")


def is_repo_path(path: str) -> bool:
    if not re.match(r"^/[^/\s]+/[^/\s]+$", path):
        return False
    owner, repo = path.strip("/").split("/", 1)
    if owner in NON_REPO_PATH_PREFIXES:
        return False
    if repo in {"followers", "following", "repositories", "sponsors"}:
        return False
    return True


def headers(accept: str = "application/vnd.github+json") -> dict[str, str]:
    h = {
        "Accept": accept,
        "User-Agent": "codex-github-repo-dissector",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        h["Authorization"] = f"Bearer {token}"
    return h


def request_json(url: str, accept: str = "application/vnd.github+json") -> tuple[Any, dict[str, str]]:
    req = urllib.request.Request(url, headers=headers(accept))
    last_error: Exception | None = None
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=25) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                return data, dict(resp.headers)
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")
            raise SystemExit(f"GitHub API error {exc.code} for {url}\n{body}") from exc
        except (urllib.error.URLError, http.client.RemoteDisconnected, TimeoutError) as exc:
            last_error = exc
            time.sleep(1.5 * (attempt + 1))
    raise SystemExit(f"GitHub API connection failed for {url}\n{last_error}") from last_error


def request_text(url: str) -> str:
    req = urllib.request.Request(
        url,
        headers={
            "Accept": "text/html,application/xhtml+xml",
            "User-Agent": "codex-github-repo-dissector",
        },
    )
    last_error: Exception | None = None
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=25) as resp:
                return resp.read().decode("utf-8", errors="replace")
        except (urllib.error.URLError, http.client.RemoteDisconnected, TimeoutError) as exc:
            last_error = exc
            time.sleep(1.5 * (attempt + 1))
    raise SystemExit(f"GitHub page request failed for {url}\n{last_error}") from last_error


class TrendingParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.items: list[dict[str, Any]] = []
        self.current: dict[str, Any] | None = None
        self.collect: str | None = None
        self.buffer: list[str] = []

    @staticmethod
    def attr(attrs: list[tuple[str, str | None]], name: str) -> str:
        for key, value in attrs:
            if key == name and value:
                return value
        return ""

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        classes = self.attr(attrs, "class")
        if tag == "article" and "Box-row" in classes:
            self.current = {}
            return

        if self.current is None:
            return

        if tag == "a":
            href = self.attr(attrs, "href")
            if "repo" not in self.current and is_repo_path(href):
                self.current["repo"] = href.strip("/")
                self.current["url"] = f"https://github.com{href}"
        elif tag == "p" and ("color-fg-muted" in classes or "col-9" in classes):
            self.collect = "description"
            self.buffer = []
        elif tag == "span" and self.attr(attrs, "itemprop") == "programmingLanguage":
            self.collect = "language"
            self.buffer = []

    def handle_data(self, data: str) -> None:
        if self.current is None:
            return
        text = " ".join(data.split())
        if not text:
            return
        if self.collect:
            self.buffer.append(text)
        elif "stars today" in text or "stars this week" in text or "stars this month" in text:
            self.current["trending_stars_text"] = text

    def handle_endtag(self, tag: str) -> None:
        if self.current is None:
            return
        if self.collect and tag in {"p", "span"}:
            self.current[self.collect] = " ".join(self.buffer).strip()
            self.collect = None
            self.buffer = []
        elif tag == "article":
            if self.current.get("repo"):
                self.items.append(self.current)
            self.current = None
            self.collect = None
            self.buffer = []


def fetch_trending_candidates(since: str = "daily", language: str = "") -> list[dict[str, Any]]:
    if since not in {"daily", "weekly", "monthly"}:
        raise SystemExit("--since must be daily, weekly, or monthly")
    language_path = urllib.parse.quote(language.strip().lower()) if language.strip() else ""
    base = f"https://github.com/trending/{language_path}" if language_path else "https://github.com/trending"
    url = f"{base}?since={since}"
    parser = TrendingParser()
    parser.feed(request_text(url))
    for item in parser.items:
        item["trending_url"] = url
        item["trending_since"] = since
        item["trending_language"] = language or "all"
    return parser.items


def ai_related(item: dict[str, Any]) -> bool:
    text = " ".join(str(item.get(key, "")) for key in ("repo", "description", "language")).lower()
    return any(keyword in text for keyword in AI_KEYWORDS)


def trend_window(stats: dict[str, Any], key: str) -> dict[str, Any]:
    return ((stats.get("recent_stars") or {}).get("star_windows") or {}).get(key, {})


def parse_link_last_page(link: str | None) -> int | None:
    if not link:
        return None
    for part in link.split(","):
        if 'rel="last"' in part:
            match = re.search(r"[?&]page=(\d+)", part)
            if match:
                return int(match.group(1))
    return None


def iso_to_dt(value: str | None) -> dt.datetime | None:
    if not value:
        return None
    text = value.replace("Z", "+00:00")
    try:
        return dt.datetime.fromisoformat(text)
    except ValueError:
        return None


def github_dt(value: str | None) -> str:
    if not value:
        return "none"
    parsed = iso_to_dt(value)
    if not parsed:
        return value
    return parsed.date().isoformat()


def classify_repo_type(repo_data: dict[str, Any]) -> dict[str, str]:
    name = str(repo_data.get("name") or "").lower()
    description = str(repo_data.get("description") or "").lower()
    topics = [str(topic).lower() for topic in (repo_data.get("topics") or [])]
    language = str(repo_data.get("language") or "").lower()
    text = " ".join([name, description, language, *topics])

    rules = [
        ("模型/推理项目", ("model", "inference", "checkpoint", "diffusion", "llm")),
        ("数据集/语料库", ("dataset", "corpus", "benchmark", "data")),
        ("图库/提示词/内容资源", ("gallery", "prompt", "prompts", "image library", "awesome")),
        ("教程/文档/课程", ("tutorial", "course", "docs", "guide", "book", "learning")),
        ("桌面应用/安装包", ("desktop", "electron", "tauri", "windows", "macos", "installer", "release")),
        ("插件/连接器/Skill", ("plugin", "extension", "mcp", "connector", "skill", "skills")),
        ("模板/脚手架", ("template", "boilerplate", "starter")),
        ("基础设施/部署工具", ("deploy", "docker", "kubernetes", "terraform", "infra")),
        ("代码应用/AI 工具", ("app", "tool", "engine", "platform", "api", "web", "video")),
    ]

    for label, keywords in rules:
        if any(keyword in text for keyword in keywords):
            return {
                "label": label,
                "method": "metadata keywords",
                "confidence": "medium",
            }

    if language and language != "none":
        return {
            "label": "代码库/工具库",
            "method": "primary language present",
            "confidence": "low",
        }

    return {
        "label": "未确认",
        "method": "insufficient metadata",
        "confidence": "low",
    }


def bucket_by_day(dates: list[dt.datetime], days: int = 14) -> list[dict[str, Any]]:
    today = dt.datetime.now(dt.timezone.utc).date()
    counts: dict[dt.date, int] = {}
    for value in dates:
        day = value.date()
        if (today - day).days < days:
            counts[day] = counts.get(day, 0) + 1
    result = []
    for offset in range(days - 1, -1, -1):
        day = today - dt.timedelta(days=offset)
        result.append({"date": day.isoformat(), "stars": counts.get(day, 0)})
    return result


def sample_daily_buckets(buckets: list[dict[str, Any]], interval: int = 5) -> list[dict[str, Any]]:
    """Return a compact chronological sample for visual reports."""
    if not buckets:
        return []
    sampled: list[dict[str, Any]] = []
    last_index = len(buckets) - 1
    for index, item in enumerate(buckets):
        if index == 0 or index == last_index or index % interval == 0:
            sampled.append(item)
    return sampled


def bucket_by_week(dates: list[dt.datetime], weeks: int = 8) -> list[dict[str, Any]]:
    today = dt.datetime.now(dt.timezone.utc).date()
    this_monday = today - dt.timedelta(days=today.weekday())
    counts: dict[dt.date, int] = {}
    for value in dates:
        day = value.date()
        monday = day - dt.timedelta(days=day.weekday())
        if 0 <= ((this_monday - monday).days // 7) < weeks:
            counts[monday] = counts.get(monday, 0) + 1
    result = []
    for offset in range(weeks - 1, -1, -1):
        monday = this_monday - dt.timedelta(weeks=offset)
        result.append({"week_start": monday.isoformat(), "stars": counts.get(monday, 0)})
    return result


def recommend_trend_display(windows: dict[int, dict[str, Any]]) -> dict[str, str]:
    thirty = windows.get(30, {})
    if thirty.get("coverage") == "complete":
        return {
            "mode": "30d_sampled",
            "reason": "30d coverage is complete; show a roughly 5-day interval sample.",
        }
    return {
        "mode": "7d",
        "reason": "30d coverage is incomplete or expensive; show the faster and more reliable 7d trend.",
    }


def unavailable_recent_stars(reason: str) -> dict[str, Any]:
    empty_window = {"count": 0, "avg_per_day": 0, "coverage": "unavailable"}
    return {
        "star_windows": {f"{days}d": dict(empty_window) for days in (7, 30, 90, 365)},
        "growth_label": "实时增长无法确认",
        "trend_display": {
            "mode": "unavailable",
            "reason": reason,
        },
        "stargazer_pages_checked": 0,
        "stargazer_pages_total": None,
        "stargazer_coverage": "unavailable",
        "trend_days_target": None,
        "earliest_stargazer_seen": None,
        "latest_stargazer_seen": None,
        "recent_stargazer_samples": [],
        "daily_buckets_14d": [],
        "daily_buckets_30d": [],
        "sampled_buckets_30d": [],
        "weekly_buckets_8w": [],
        "star_history_url": None,
        "note": reason,
    }


def label_growth(windows: dict[int, dict[str, Any]]) -> str:
    seven = windows.get(7, {})
    thirty = windows.get(30, {})
    seven_count = int(seven.get("count", 0))
    thirty_count = int(thirty.get("count", 0))
    seven_complete = seven.get("coverage") == "complete"
    thirty_complete = thirty.get("coverage") == "complete"

    if seven_count >= 500:
        return "爆发增长" if seven_complete else "爆发增长（下限）"
    if seven_count >= 100 or thirty_count >= 500:
        return "快速增长" if seven_complete or thirty_complete else "快速增长（下限）"
    if thirty_count >= 100:
        return "稳定增长" if thirty_complete else "稳定增长（下限）"
    if thirty_count > 0:
        return "缓慢增长"
    return "近期增长不明显或数据不足"


def collect_recent_stars(
    owner: str,
    repo: str,
    max_pages: int,
    full_stars: bool = False,
    trend_days: int = 7,
) -> dict[str, Any]:
    first_url = f"{API}/repos/{owner}/{repo}/stargazers?per_page=100&page=1"
    _, first_headers = request_json(first_url, "application/vnd.github.star+json")
    last_page = parse_link_last_page(first_headers.get("Link")) or 1

    today = dt.datetime.now(dt.timezone.utc)
    samples: list[dict[str, str]] = []
    starred_dates: list[dt.datetime] = []
    pages_checked = 0
    pages_to_check = last_page if full_stars else min(max_pages, last_page)

    for page in range(last_page, max(0, last_page - pages_to_check), -1):
        url = f"{API}/repos/{owner}/{repo}/stargazers?per_page=100&page={page}"
        data, _ = request_json(url, "application/vnd.github.star+json")
        pages_checked += 1
        if not isinstance(data, list) or not data:
            continue
        for item in data:
            starred_at = item.get("starred_at")
            starred_dt = iso_to_dt(starred_at)
            if not starred_dt:
                continue
            starred_dates.append(starred_dt)
            if len(samples) < 5:
                user = item.get("user") or {}
                samples.append(
                    {
                        "login": user.get("login", ""),
                        "starred_at": starred_at,
                    }
                )
        if starred_dates and not full_stars:
            if min(starred_dates) <= today - dt.timedelta(days=trend_days):
                break

    starred_dates.sort()
    earliest = starred_dates[0] if starred_dates else None
    latest = starred_dates[-1] if starred_dates else None
    windows: dict[int, dict[str, Any]] = {}
    for days in (7, 30, 90, 365):
        cutoff = today - dt.timedelta(days=days)
        count = sum(1 for value in starred_dates if value >= cutoff)
        complete = pages_checked >= last_page or (earliest is not None and earliest <= cutoff)
        windows[days] = {
            "count": count,
            "avg_per_day": round(count / days, 2),
            "coverage": "complete" if complete else "lower_bound",
        }

    coverage = "complete" if pages_checked >= last_page else f"recent {pages_checked} of {last_page} pages"
    star_history_url = f"https://star-history.com/#/{owner}/{repo}&Date"
    daily_buckets_14d = bucket_by_day(starred_dates, 14)
    daily_buckets_30d = bucket_by_day(starred_dates, 30)

    return {
        "star_windows": {f"{days}d": data for days, data in windows.items()},
        "growth_label": label_growth(windows),
        "trend_display": recommend_trend_display(windows),
        "stargazer_pages_checked": pages_checked,
        "stargazer_pages_total": last_page,
        "stargazer_coverage": coverage,
        "trend_days_target": trend_days,
        "earliest_stargazer_seen": earliest.isoformat() if earliest else None,
        "latest_stargazer_seen": latest.isoformat() if latest else None,
        "recent_stargazer_samples": samples,
        "daily_buckets_14d": daily_buckets_14d,
        "daily_buckets_30d": daily_buckets_30d,
        "sampled_buckets_30d": sample_daily_buckets(daily_buckets_30d),
        "weekly_buckets_8w": bucket_by_week(starred_dates, 8),
        "star_history_url": star_history_url,
        "note": "Counts are exact only when coverage is complete for that window; lower_bound means more older pages may still fall inside the window.",
    }


def get_latest_release(owner: str, repo: str) -> dict[str, Any] | None:
    url = f"{API}/repos/{owner}/{repo}/releases/latest"
    try:
        data, _ = request_json(url)
    except SystemExit:
        return None
    if not isinstance(data, dict):
        return None
    return {
        "tag_name": data.get("tag_name"),
        "name": data.get("name"),
        "published_at": data.get("published_at"),
        "html_url": data.get("html_url"),
    }


def get_hot_issues(owner: str, repo: str) -> list[dict[str, Any]]:
    query = urllib.parse.quote(f"repo:{owner}/{repo} is:issue sort:comments-desc")
    url = f"{API}/search/issues?q={query}&per_page=5"
    try:
        data, _ = request_json(url)
    except SystemExit:
        return []
    items = data.get("items", []) if isinstance(data, dict) else []
    result = []
    for item in items[:5]:
        result.append(
            {
                "number": item.get("number"),
                "title": item.get("title"),
                "state": item.get("state"),
                "comments": item.get("comments"),
                "html_url": item.get("html_url"),
            }
        )
    return result


def fetch_stats(
    repo_value: str,
    max_star_pages: int,
    full_stars: bool = False,
    trend_days: int = 7,
    skip_star_history: bool = False,
    skip_hot_issues: bool = False,
) -> dict[str, Any]:
    owner, repo = parse_repo(repo_value)
    repo_data, repo_headers = request_json(f"{API}/repos/{owner}/{repo}")
    latest_release = get_latest_release(owner, repo)
    if skip_star_history:
        recent_stars = unavailable_recent_stars("Skipped by --skip-star-history for fast or rate-limit-safe analysis.")
    else:
        try:
            recent_stars = collect_recent_stars(owner, repo, max_star_pages, full_stars, trend_days)
        except SystemExit as exc:
            recent_stars = unavailable_recent_stars(f"Stargazer timestamp scan unavailable: {exc}")
    hot_issues = [] if skip_hot_issues else get_hot_issues(owner, repo)

    reset = repo_headers.get("X-RateLimit-Reset")
    rate_reset_at = None
    if reset and reset.isdigit():
        rate_reset_at = dt.datetime.fromtimestamp(int(reset), dt.timezone.utc).isoformat()

    return {
        "repo": f"{owner}/{repo}",
        "html_url": repo_data.get("html_url"),
        "description": repo_data.get("description"),
        "stars": repo_data.get("stargazers_count"),
        "forks": repo_data.get("forks_count"),
        "watchers": repo_data.get("subscribers_count"),
        "open_issues": repo_data.get("open_issues_count"),
        "language": repo_data.get("language"),
        "license": (repo_data.get("license") or {}).get("spdx_id"),
        "topics": repo_data.get("topics"),
        "repo_type": classify_repo_type(repo_data),
        "created_at": repo_data.get("created_at"),
        "updated_at": repo_data.get("updated_at"),
        "pushed_at": repo_data.get("pushed_at"),
        "default_branch": repo_data.get("default_branch"),
        "archived": repo_data.get("archived"),
        "disabled": repo_data.get("disabled"),
        "latest_release": latest_release,
        "hot_issues": hot_issues,
        "recent_stars": recent_stars,
        "rate_limit_remaining": repo_headers.get("X-RateLimit-Remaining"),
        "rate_limit_reset_at": rate_reset_at,
        "fetched_at": dt.datetime.now(dt.timezone.utc).isoformat(),
    }


def print_markdown(stats: dict[str, Any]) -> None:
    release = stats.get("latest_release") or {}
    stars = stats.get("recent_stars") or {}
    windows = stars.get("star_windows") or {}
    seven = windows.get("7d", {})
    thirty = windows.get("30d", {})
    ninety = windows.get("90d", {})
    year = windows.get("365d", {})
    print(f"# GitHub Stats: {stats['repo']}")
    print()
    print(f"- URL: {stats.get('html_url')}")
    print(f"- Description: {stats.get('description') or 'none'}")
    print(f"- Stars / forks / open issues: {stats.get('stars')} / {stats.get('forks')} / {stats.get('open_issues')}")
    print(f"- Language / license: {stats.get('language') or 'unknown'} / {stats.get('license') or 'unknown'}")
    repo_type = stats.get("repo_type") or {}
    print(f"- Repository type: {repo_type.get('label', 'unknown')} ({repo_type.get('confidence', 'unknown')}, {repo_type.get('method', 'unknown')})")
    print(f"- Created / pushed / updated: {github_dt(stats.get('created_at'))} / {github_dt(stats.get('pushed_at'))} / {github_dt(stats.get('updated_at'))}")
    print(f"- Latest release: {release.get('tag_name') or 'none'} ({github_dt(release.get('published_at'))})")
    print(f"- Growth label: {stars.get('growth_label')}")
    print(
        "- Recent stars: "
        f"7d={seven.get('count', 0)} ({seven.get('coverage')}, {seven.get('avg_per_day', 0)}/day), "
        f"30d={thirty.get('count', 0)} ({thirty.get('coverage')}, {thirty.get('avg_per_day', 0)}/day), "
        f"90d={ninety.get('count', 0)} ({ninety.get('coverage')}), "
        f"365d={year.get('count', 0)} ({year.get('coverage')})"
    )
    print(f"- Stargazer coverage: {stars.get('stargazer_coverage')}")
    display = stars.get("trend_display") or {}
    if display:
        print(f"- Trend display suggestion: {display.get('mode')} ({display.get('reason')})")
    print(f"- Star history: {stars.get('star_history_url')}")
    print(f"- Fetched at: {stats.get('fetched_at')}")
    print()
    if stars.get("daily_buckets_14d"):
        print("## Daily star buckets (last 14 days, scanned pages only)")
        for item in stars["daily_buckets_14d"]:
            if item["stars"]:
                print(f"- {item['date']}: +{item['stars']}")
        print()
    if stats.get("hot_issues"):
        print("## Hot issues")
        for item in stats["hot_issues"]:
            print(f"- #{item.get('number')} {item.get('title')} ({item.get('comments')} comments): {item.get('html_url')}")


def fetch_trending_report(
    since: str,
    language: str,
    limit: int,
    max_star_pages: int,
    ai_filter: bool,
    trend_days: int,
    skip_star_history: bool,
    skip_hot_issues: bool,
) -> dict[str, Any]:
    candidates = fetch_trending_candidates(since, language)
    filtered = [item for item in candidates if ai_related(item)] if ai_filter else candidates
    selected = filtered[:limit]
    results: list[dict[str, Any]] = []

    for item in selected:
        try:
            stats = fetch_stats(
                item["repo"],
                max_star_pages,
                trend_days=trend_days,
                skip_star_history=skip_star_history,
                skip_hot_issues=skip_hot_issues,
            )
        except SystemExit as exc:
            results.append({"candidate": item, "error": str(exc)})
            continue
        results.append({"candidate": item, "stats": stats})
        time.sleep(0.2)

    return {
        "source": "GitHub Trending",
        "since": since,
        "language": language or "all",
        "ai_filter": ai_filter,
        "candidate_count": len(candidates),
        "filtered_count": len(filtered),
        "limit": limit,
        "results": results,
        "fetched_at": dt.datetime.now(dt.timezone.utc).isoformat(),
    }


def print_trending_markdown(report: dict[str, Any]) -> None:
    print(f"# GitHub Trending First: {report['since']} / {report['language']}")
    print()
    print(
        f"- Source: GitHub Trending ({report['candidate_count']} candidates, "
        f"{report['filtered_count']} after AI filter)"
    )
    print(f"- Fetched at: {report['fetched_at']}")
    print("- Note: GitHub Trending is used only as the fast candidate source; growth numbers come from stargazer timestamps.")
    print()
    print("| Rank | Repo | Stars | 7d growth | 30d growth | Label | Why it matters |")
    print("|---:|---|---:|---:|---:|---|---|")
    sortable = []
    for result in report["results"]:
        stats = result.get("stats")
        if not stats:
            continue
        seven = trend_window(stats, "7d")
        thirty = trend_window(stats, "30d")
        sortable.append((int(seven.get("count", 0)), result))
    sortable.sort(key=lambda item: item[0], reverse=True)

    for rank, (_, result) in enumerate(sortable, 1):
        stats = result["stats"]
        candidate = result["candidate"]
        seven = trend_window(stats, "7d")
        thirty = trend_window(stats, "30d")
        label = (stats.get("recent_stars") or {}).get("growth_label", "")
        desc = stats.get("description") or candidate.get("description") or ""
        if len(desc) > 90:
            desc = desc[:87].rstrip() + "..."
        print(
            f"| {rank} | [{stats['repo']}]({stats.get('html_url')}) | {stats.get('stars')} | "
            f"{seven.get('count', 0)} {seven.get('coverage', '')} | "
            f"{thirty.get('count', 0)} {thirty.get('coverage', '')} | "
            f"{label} | {desc} |"
        )

    errors = [result for result in report["results"] if result.get("error")]
    if errors:
        print()
        print("## Errors")
        for result in errors:
            candidate = result["candidate"]
            print(f"- {candidate.get('repo')}: {result.get('error')}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch compact GitHub repository stats.")
    parser.add_argument("repo", nargs="?", help="GitHub URL or owner/repo")
    parser.add_argument("--trending", action="store_true", help="use GitHub Trending as the candidate source")
    parser.add_argument("--since", choices=["daily", "weekly", "monthly"], default="daily", help="GitHub Trending period")
    parser.add_argument("--language", default="", help="optional GitHub Trending language path, e.g. python or typescript")
    parser.add_argument("--limit", type=int, default=10, help="number of trending candidates to analyze")
    parser.add_argument("--no-ai-filter", action="store_true", help="do not filter trending candidates by AI keywords")
    parser.add_argument("--max-star-pages", type=int, default=8, help="recent stargazer pages to inspect; default is fast and 7d-first")
    parser.add_argument("--trend-days", type=int, default=7, choices=[7, 30, 90, 365], help="target window to fully cover before stopping")
    parser.add_argument("--skip-star-history", action="store_true", help="skip stargazer timestamp scan for faster, rate-limit-safe metadata")
    parser.add_argument("--skip-hot-issues", action="store_true", help="skip issue search for faster, rate-limit-safe metadata")
    parser.add_argument("--fast", action="store_true", help="fast metadata mode: skip stargazer timestamps and hot issue search")
    parser.add_argument("--full-stars", action="store_true", help="scan all stargazer pages; slow and may hit rate limits")
    parser.add_argument("--json", action="store_true", help="print JSON instead of markdown")
    args = parser.parse_args()

    if args.fast:
        args.skip_star_history = True
        args.skip_hot_issues = True

    if args.trending:
        report = fetch_trending_report(
            since=args.since,
            language=args.language,
            limit=args.limit,
            max_star_pages=args.max_star_pages,
            ai_filter=not args.no_ai_filter,
            trend_days=args.trend_days,
            skip_star_history=args.skip_star_history,
            skip_hot_issues=args.skip_hot_issues,
        )
        if args.json:
            print(json.dumps(report, ensure_ascii=False, indent=2))
        else:
            print_trending_markdown(report)
        return

    if not args.repo:
        parser.error("repo is required unless --trending is used")

    stats = fetch_stats(
        args.repo,
        args.max_star_pages,
        args.full_stars,
        args.trend_days,
        args.skip_star_history,
        args.skip_hot_issues,
    )
    if args.json:
        print(json.dumps(stats, ensure_ascii=False, indent=2))
    else:
        print_markdown(stats)


if __name__ == "__main__":
    main()
