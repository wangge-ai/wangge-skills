from __future__ import annotations

import argparse
import json
import math
import re
import unicodedata
from collections import Counter
from datetime import datetime
from difflib import SequenceMatcher
from pathlib import Path

import pandas as pd
from bs4 import BeautifulSoup


def normalize_title(value: object) -> str:
    text = "" if value is None or (isinstance(value, float) and math.isnan(value)) else str(value)
    text = unicodedata.normalize("NFKC", text).lower()
    text = text.replace("chatgpt", "chatgpt")
    return re.sub(r"[^\w\u4e00-\u9fff]+", "", text)


def parse_date(value: object) -> pd.Timestamp:
    if pd.isna(value):
        return pd.NaT
    text = str(value).strip()
    if re.fullmatch(r"\d{8}", text):
        return pd.to_datetime(text, format="%Y%m%d", errors="coerce")
    return pd.to_datetime(text, errors="coerce")


def yes_no(value: bool) -> str:
    return "是" if value else "否"


def read_tendency(path: Path) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    raw = pd.read_excel(path, header=None, dtype=object)

    daily_channel = raw.iloc[3:, [1, 2, 3]].copy()
    daily_channel.columns = ["date", "channel", "readers"]
    daily_channel = daily_channel.dropna(how="all")
    daily_channel = daily_channel[daily_channel["date"].notna() & daily_channel["channel"].notna()]
    daily_channel["date"] = daily_channel["date"].map(parse_date)
    daily_channel["readers"] = pd.to_numeric(daily_channel["readers"], errors="coerce").fillna(0).astype(int)
    daily_channel = daily_channel.sort_values(["date", "channel"]).reset_index(drop=True)

    daily_interactions = raw.iloc[3:, [5, 6, 7, 8, 9]].copy()
    daily_interactions.columns = ["date", "shares", "original_link_clicks", "favorites", "published_articles"]
    daily_interactions = daily_interactions.dropna(how="all")
    daily_interactions = daily_interactions[daily_interactions["date"].notna()]
    daily_interactions["date"] = daily_interactions["date"].map(parse_date)
    for col in ["shares", "original_link_clicks", "favorites", "published_articles"]:
        daily_interactions[col] = pd.to_numeric(daily_interactions[col], errors="coerce").fillna(0).astype(int)
    daily_interactions = daily_interactions.sort_values("date").reset_index(drop=True)

    article_source = raw.iloc[3:, [11, 12, 13, 14, 15]].copy()
    article_source.columns = ["source_channel", "publish_date", "title", "readers", "read_share"]
    article_source = article_source.dropna(how="all")
    article_source = article_source[article_source["title"].notna()]
    article_source["publish_date"] = article_source["publish_date"].map(parse_date)
    article_source["readers"] = pd.to_numeric(article_source["readers"], errors="coerce").fillna(0).astype(int)
    article_source["read_share"] = pd.to_numeric(article_source["read_share"], errors="coerce")
    article_source["title_norm"] = article_source["title"].map(normalize_title)
    article_source = article_source.sort_values(["publish_date", "source_channel", "readers"], ascending=[True, True, False])
    article_source = article_source.reset_index(drop=True)

    return daily_channel, daily_interactions, article_source


def read_user_analysis(path: Path) -> pd.DataFrame:
    html = path.read_text(encoding="utf-8", errors="replace")
    soup = BeautifulSoup(html, "lxml")
    rows: list[list[str]] = []
    for tr in soup.find_all("tr"):
        cells = [cell.get_text(strip=True) for cell in tr.find_all(["td", "th"])]
        if cells:
            rows.append(cells)
    data_rows = [row for row in rows if len(row) >= 5 and re.match(r"\d{4}-\d{2}-\d{2}", row[0])]
    df = pd.DataFrame(data_rows, columns=["date", "new_followers", "unfollows", "net_followers", "total_followers"])
    df["date"] = df["date"].map(parse_date)
    for col in ["new_followers", "unfollows", "net_followers", "total_followers"]:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)
    return df.sort_values("date").reset_index(drop=True)


def categorize_title(title: str) -> str:
    t = title.lower()
    if "电商" in title and any(k in title for k in ["skill", "SOP", "报告", "主图", "详情页", "竞品", "商品", "作图", "生图", "文案", "违禁词", "市场"]):
        return "AI+电商/可交付"
    if any(k.lower() in t for k in ["codex", "github", "n8n", "飞书", "workbuddy"]):
        return "Codex/GitHub/自动化"
    if any(k.lower() in t for k in ["gpt", "claude", "豆包", "coze", "openhuman", "hermes", "视频工具", "模型"]):
        return "模型/工具实测"
    if any(k in title for k in ["岗位", "普通人", "思维课", "作品集", "门槛"]):
        return "能力/岗位/认知"
    return "其他"


def title_signals(title: str) -> dict[str, object]:
    lower = title.lower()
    return {
        "has_number": bool(re.search(r"\d", title)),
        "has_from_zero": bool(re.search(r"从\s*0|从0", title)),
        "has_skill": "skill" in lower or "skills" in lower,
        "has_sop": "sop" in lower,
        "has_tutorial": any(k in title for k in ["教程", "攻略", "指南", "完整流程", "保姆级"]),
        "has_ecommerce": "电商" in title,
        "has_codex": "codex" in lower,
        "has_github": "github" in lower,
        "has_report": "报告" in title,
        "has_test": any(k in title for k in ["实测", "测了", "测试"]),
        "has_asset_promise": any(k in title for k in ["附", "免费", "分享", "完整", "拿来就可以用"]),
    }


def parse_visual_roles(path: Path) -> tuple[str, str, int]:
    if not path.exists():
        return "", "", 0
    text = path.read_text(encoding="utf-8", errors="replace")
    roles: list[str] = []
    in_table = False
    for line in text.splitlines():
        if line.startswith("| 图位 |"):
            in_table = True
            continue
        if in_table and line.startswith("|---"):
            continue
        if in_table and line.startswith("|"):
            cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
            if len(cells) >= 5 and cells[0].startswith("图位"):
                roles.append(cells[4])
        elif in_table and not line.startswith("|"):
            break
    first_role = roles[0] if roles else ""
    common_role = Counter(roles).most_common(1)[0][0] if roles else ""
    return first_role, common_role, len(roles)


def read_archive(archive_dir: Path) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for meta_path in sorted(archive_dir.glob("*/article_meta.json")):
        article_dir = meta_path.parent
        try:
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        stats = meta.get("stats", {})
        first_role, common_role, visual_rows = parse_visual_roles(article_dir / "visual_analysis.md")
        title = meta.get("title", "")
        row: dict[str, object] = {
            "archive_dir": str(article_dir),
            "date": parse_date(meta.get("pub_date", "")),
            "title": title,
            "title_norm": normalize_title(title),
            "account_name": meta.get("account_name", ""),
            "url": meta.get("article_url", ""),
            "char_count": int(stats.get("char_count") or 0),
            "paragraph_count": int(stats.get("paragraph_count") or 0),
            "image_count": int(stats.get("image_count") or 0),
            "emphasis_count": int(stats.get("emphasis_count") or 0),
            "first_image_role": first_role,
            "dominant_image_role": common_role,
            "visual_image_rows": visual_rows,
            "category": categorize_title(title),
        }
        row.update(title_signals(title))
        rows.append(row)
    df = pd.DataFrame(rows)
    if not df.empty:
        df["publish_day"] = df["date"].dt.normalize()
        df = df.sort_values("date").reset_index(drop=True)
    return df


def build_article_performance(article_source: pd.DataFrame) -> pd.DataFrame:
    totals = article_source[article_source["source_channel"].eq("全部")][
        ["publish_date", "title_norm"]
    ].drop_duplicates()
    totals["has_total_readers"] = True
    pivot = (
        article_source.pivot_table(
            index=["publish_date", "title_norm", "title"],
            columns="source_channel",
            values="readers",
            aggfunc="sum",
            fill_value=0,
        )
        .reset_index()
        .rename_axis(None, axis=1)
    )
    for col in ["全部", "推荐", "公众号主页", "公众号消息", "聊天会话", "朋友圈", "搜一搜", "其他"]:
        if col not in pivot.columns:
            pivot[col] = 0
    pivot = pivot.rename(
        columns={
            "全部": "total_readers",
            "推荐": "recommend_readers",
            "公众号主页": "homepage_readers",
            "公众号消息": "message_readers",
            "聊天会话": "chat_readers",
            "朋友圈": "moments_readers",
            "搜一搜": "search_readers",
            "其他": "other_readers",
        }
    )
    pivot = pivot.merge(totals, on=["publish_date", "title_norm"], how="left")
    pivot["has_total_readers"] = pivot["has_total_readers"].fillna(False).astype(bool)
    pivot.loc[~pivot["has_total_readers"], "total_readers"] = pd.NA
    share = article_source[article_source["source_channel"].eq("全部")][
        ["publish_date", "title_norm", "read_share"]
    ].drop_duplicates(["publish_date", "title_norm"])
    pivot = pivot.merge(share, on=["publish_date", "title_norm"], how="left")
    pivot["recommend_rate"] = pivot.apply(
        lambda row: row["recommend_readers"] / row["total_readers"] if row["total_readers"] else 0,
        axis=1,
    )
    pivot["homepage_rate"] = pivot.apply(
        lambda row: row["homepage_readers"] / row["total_readers"] if row["total_readers"] else 0,
        axis=1,
    )
    return pivot


def merge_archive_performance(archive: pd.DataFrame, performance: pd.DataFrame) -> pd.DataFrame:
    merged = archive.merge(
        performance,
        left_on=["publish_day", "title_norm"],
        right_on=["publish_date", "title_norm"],
        how="left",
        suffixes=("", "_metric"),
    )
    unmatched = merged[merged["total_readers"].isna()].copy()
    if unmatched.empty:
        return merged

    perf_by_date = {
        day: group.copy()
        for day, group in performance.groupby("publish_date")
    }
    for idx, row in unmatched.iterrows():
        candidates = perf_by_date.get(row["publish_day"])
        if candidates is None or candidates.empty:
            continue
        scores = candidates["title_norm"].map(lambda value: SequenceMatcher(None, row["title_norm"], value).ratio())
        best_idx = scores.idxmax()
        if scores.loc[best_idx] >= 0.74:
            for col in performance.columns:
                if col in {"publish_date", "title_norm"}:
                    continue
                merged.loc[idx, col] = candidates.loc[best_idx, col]
            merged.loc[idx, "publish_date"] = candidates.loc[best_idx, "publish_date"]
    return merged


def pct(value: float | int | None, digits: int = 1) -> str:
    if value is None or pd.isna(value):
        return "-"
    return f"{float(value) * 100:.{digits}f}%"


def int_text(value: float | int | None) -> str:
    if value is None or pd.isna(value):
        return "-"
    return f"{int(round(float(value))):,}"


def short_text(value: object, limit: int = 34) -> str:
    text = "" if value is None or pd.isna(value) else str(value)
    return text if len(text) <= limit else text[: limit - 1] + "…"


def table_md(df: pd.DataFrame, columns: list[str], rename: dict[str, str] | None = None, max_rows: int = 12) -> str:
    if df.empty:
        return "（无数据）"
    view = df.loc[:, columns].head(max_rows).copy()
    if rename:
        view = view.rename(columns=rename)
    return view.to_markdown(index=False)


def make_report(
    archive_perf: pd.DataFrame,
    daily_channel: pd.DataFrame,
    daily_interactions: pd.DataFrame,
    article_source: pd.DataFrame,
    followers: pd.DataFrame,
    archive_dir: Path,
    tendency_path: Path,
    user_path: Path,
) -> str:
    total_daily_reads = daily_channel[daily_channel["channel"].eq("全部")]["readers"].sum()
    period_start = daily_channel["date"].min().date()
    period_end = daily_channel["date"].max().date()
    article_start = archive_perf["date"].min().date()
    article_end = archive_perf["date"].max().date()
    follower_start = followers["date"].min().date() if not followers.empty else None
    follower_end = followers["date"].max().date() if not followers.empty else None

    matched_total = archive_perf["has_total_readers"].fillna(False).sum()
    matched_any_source = archive_perf[
        [
            "recommend_readers",
            "homepage_readers",
            "message_readers",
            "chat_readers",
            "moments_readers",
            "search_readers",
            "other_readers",
        ]
    ].fillna(0).sum(axis=1).gt(0).sum()
    exported_total_articles = article_source[article_source["source_channel"].eq("全部")][
        ["publish_date", "title_norm"]
    ].drop_duplicates().shape[0]

    top_articles = archive_perf[archive_perf["has_total_readers"].fillna(False)].sort_values("total_readers", ascending=False).copy()
    top_articles["推荐占比"] = top_articles["recommend_rate"].map(pct)
    top_articles["主页占比"] = top_articles["homepage_rate"].map(pct)
    top_articles["阅读人数"] = top_articles["total_readers"].map(int_text)
    top_articles["日期"] = top_articles["publish_day"].dt.strftime("%Y-%m-%d")

    source_no_total = article_source[~article_source["source_channel"].eq("全部")]
    source_summary = source_no_total.groupby("source_channel", as_index=False)["readers"].sum()
    source_summary["占已列渠道比例"] = source_summary["readers"] / source_summary["readers"].sum()
    source_summary = source_summary.sort_values("readers", ascending=False)
    source_summary["阅读人数"] = source_summary["readers"].map(int_text)
    source_summary["占比"] = source_summary["占已列渠道比例"].map(pct)

    top_days_read = daily_channel[daily_channel["channel"].eq("全部")].sort_values("readers", ascending=False).head(10).copy()
    top_days_read["日期"] = top_days_read["date"].dt.strftime("%Y-%m-%d")
    top_days_read["阅读人数"] = top_days_read["readers"].map(int_text)

    top_followers = followers.sort_values("net_followers", ascending=False).head(10).copy()
    if not top_followers.empty:
        top_followers["日期"] = top_followers["date"].dt.strftime("%Y-%m-%d")

    top_shares = daily_interactions.sort_values("shares", ascending=False).head(10).copy()
    top_shares["日期"] = top_shares["date"].dt.strftime("%Y-%m-%d")
    top_favorites = daily_interactions.sort_values("favorites", ascending=False).head(10).copy()
    top_favorites["日期"] = top_favorites["date"].dt.strftime("%Y-%m-%d")

    metric_articles = archive_perf[archive_perf["has_total_readers"].fillna(False)].copy()
    category_summary = (
        metric_articles.groupby("category")
        .agg(
            articles=("title", "count"),
            avg_readers=("total_readers", "mean"),
            median_readers=("total_readers", "median"),
            avg_recommend_rate=("recommend_rate", "mean"),
            avg_images=("image_count", "mean"),
            avg_chars=("char_count", "mean"),
        )
        .reset_index()
        .sort_values("avg_readers", ascending=False)
    )
    category_summary["平均阅读"] = category_summary["avg_readers"].map(int_text)
    category_summary["中位阅读"] = category_summary["median_readers"].map(int_text)
    category_summary["平均推荐占比"] = category_summary["avg_recommend_rate"].map(pct)
    category_summary["平均图片数"] = category_summary["avg_images"].map(lambda x: f"{x:.1f}")
    category_summary["平均字数"] = category_summary["avg_chars"].map(int_text)

    feature_rows = []
    feature_specs = [
        ("has_skill", "标题含 Skill/Skills"),
        ("has_sop", "标题含 SOP"),
        ("has_report", "标题含 报告"),
        ("has_ecommerce", "标题含 电商"),
        ("has_codex", "标题含 Codex"),
        ("has_github", "标题含 GitHub"),
        ("has_from_zero", "标题含 从0"),
        ("has_asset_promise", "标题含 附/完整/免费/分享"),
        ("has_tutorial", "标题含 教程/攻略/指南"),
        ("has_test", "标题含 实测/测试"),
    ]
    for col, label in feature_specs:
        group = metric_articles[metric_articles[col].eq(True)]
        if group.empty:
            continue
        avg_readers = group["total_readers"].mean()
        feature_rows.append(
            {
                "信号": label,
                "篇数": len(group),
                "avg_readers_num": avg_readers,
                "平均阅读": int_text(avg_readers),
                "中位阅读": int_text(group["total_readers"].median()),
                "平均推荐占比": pct(group["recommend_rate"].mean()),
            }
        )
    feature_summary = pd.DataFrame(feature_rows)
    if not feature_summary.empty:
        feature_summary = feature_summary.sort_values("avg_readers_num", ascending=False).drop(columns=["avg_readers_num"])

    visual_metric = metric_articles[metric_articles["visual_image_rows"].fillna(0).gt(0)].copy()
    visual_top = top_articles.head(10).copy()
    visual_top["短标题"] = visual_top["title"].map(lambda value: short_text(value, 30))
    visual_top["图片数"] = visual_top["image_count"].astype(int)
    visual_top["首图角色"] = visual_top["first_image_role"].fillna("").replace("", "无")
    visual_top["主导图位"] = visual_top["dominant_image_role"].fillna("").replace("", "无")
    visual_role_summary = pd.DataFrame()
    if not visual_metric.empty:
        visual_role_summary = (
            visual_metric.groupby("first_image_role")
            .agg(
                articles=("title", "count"),
                avg_readers=("total_readers", "mean"),
                avg_recommend_rate=("recommend_rate", "mean"),
            )
            .reset_index()
            .sort_values("avg_readers", ascending=False)
        )
        visual_role_summary["平均阅读"] = visual_role_summary["avg_readers"].map(int_text)
        visual_role_summary["平均推荐占比"] = visual_role_summary["avg_recommend_rate"].map(pct)

    if not followers.empty:
        follower_net = followers["net_followers"].sum()
        follower_new = followers["new_followers"].sum()
        follower_cancel = followers["unfollows"].sum()
        follower_final = followers["total_followers"].iloc[-1]
    else:
        follower_net = follower_new = follower_cancel = follower_final = 0

    daily_join = daily_channel[daily_channel["channel"].eq("全部")][["date", "readers"]].merge(
        followers[["date", "net_followers"]], on="date", how="inner"
    )
    read_follow_corr = daily_join["readers"].corr(daily_join["net_followers"]) if len(daily_join) >= 3 else float("nan")

    top_article_titles = "\n".join(
        f"{i + 1}. {row['日期']}｜{row['title']}｜{row['阅读人数']} 阅读｜推荐占比 {row['推荐占比']}｜图 {int(row['image_count'])}｜{row['category']}"
        for i, row in top_articles.head(10).reset_index(drop=True).iterrows()
    )

    lines = [
        "# 目标公众号：文章 HTML + 后台导出数据联合分析",
        "",
        f"- 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"- 文章档案：`{archive_dir}`",
        f"- 阅读趋势表：`{tendency_path}`",
        f"- 用户增长表：`{user_path}`",
        f"- 文章档案范围：{article_start} 至 {article_end}，共 {len(archive_perf)} 篇",
        f"- 后台阅读趋势范围：{period_start} 至 {period_end}",
        f"- 用户增长范围：{follower_start} 至 {follower_end}" if follower_start else "- 用户增长范围：无",
        "",
        "## 一句话结论",
        "",
        "这批数据已经足够做第一版“公众号内容复盘 skill”：能把文章标题、字数、图片/图位节奏、文章类型，与阅读来源、推荐流表现、日关注增长放在一起看。它现在最适合回答“什么题材和标题形态更容易被推荐流放大”“哪些文章像资产而不是单篇内容”“下一周应该押哪类选题”。",
        "",
        "但它还不够做严格的“单篇转化归因”：当前导出的互动数据是按天汇总，缺少每篇文章的分享、收藏、点赞、在看、读后关注、完读率，所以多篇文章或老文章长尾阅读会混在同一天里。这个边界要写进后续 skill。",
        "",
        "## 数据够不够",
        "",
        f"- 够：已抓取文章 {len(archive_perf)} 篇，后台来源榜里有 {exported_total_articles} 篇文章带“全部阅读”数据；本地档案中 {matched_total} 篇匹配到总阅读，{matched_any_source} 篇至少匹配到一个来源渠道。",
        f"- 够：趋势表拆出了 {len(daily_channel)} 条“日期 x 渠道”阅读记录、{len(daily_interactions)} 天分享/收藏/原文点击数据。",
        f"- 够：用户增长表拆出了 {len(followers)} 天关注增长记录，区间净增 {int_text(follower_net)}，总新关注 {int_text(follower_new)}，取关 {int_text(follower_cancel)}，期末累计 {int_text(follower_final)}。",
        "- 不够：缺每篇文章级别的分享、收藏、赞/在看、读后关注、完读率、评论互动。没有这些，只能做“强相关/弱归因”，不能说某篇文章精确带来多少关注。",
        "- 可以近似：因为你这个号大多数日期是一天一篇，日分享/日收藏可以和当天首发文章做近似关联；但遇到推荐流爆发和老文回流时，要标记为“可能受长尾影响”。",
        "",
        "## 顶部表现文章",
        "",
        top_article_titles,
        "",
        "## 文章来源结构",
        "",
        table_md(source_summary, ["source_channel", "阅读人数", "占比"], {"source_channel": "传播渠道"}),
        "",
        "这组数据的核心信号非常清楚：推荐流是主要放大器。头部文章里，推荐占比普遍在 78%-86% 左右，说明标题和首屏必须面向“不认识你的推荐流用户”，不能只服务老粉。",
        "",
        "## 题材表现",
        "",
        table_md(
            category_summary,
            ["category", "articles", "平均阅读", "中位阅读", "平均推荐占比", "平均图片数", "平均字数"],
            {"category": "题材", "articles": "篇数"},
        ),
        "",
        "当前最强的组合不是泛 AI 新闻，而是“AI+电商场景 + 具体交付物 + 可复制 SOP/Skill”。Codex/GitHub/n8n 这类文章适合建立账号壁垒，但阅读爆发往往要和电商结果、报告、图像、数据中台等可感知产出绑定。",
        "",
        "## 标题信号",
        "",
        table_md(feature_summary, ["信号", "篇数", "平均阅读", "中位阅读", "平均推荐占比"], max_rows=20),
        "",
        "从标题侧看，读者和推荐流都更吃“可判断收益”的表达：数字、从 0、完整教程、报告、SOP、Skill、附资料。注意不是堆关键词，而是让读者在列表页就知道点开后能拿到什么。",
        "",
        "## HTML/视觉线索",
        "",
        table_md(
            visual_top,
            ["短标题", "阅读人数", "图片数", "首图角色", "主导图位"],
            max_rows=10,
        ),
        "",
        "首图角色汇总：",
        "",
        table_md(
            visual_role_summary,
            ["first_image_role", "articles", "平均阅读", "平均推荐占比"],
            {"first_image_role": "首图角色", "articles": "篇数"},
            max_rows=10,
        ),
        "",
        "这部分来自爬虫保留下来的 HTML/图位拆解，不是后台数据。它能帮我们解释“为什么读者愿意继续看”：结果预览、报告截图、流程图、证据表，比纯封面或装饰图更值得优先放到首屏。",
        "",
        "## 阅读峰值日期",
        "",
        table_md(top_days_read, ["日期", "阅读人数"], max_rows=10),
        "",
        "## 关注增长峰值",
        "",
        table_md(
            top_followers,
            ["日期", "new_followers", "unfollows", "net_followers", "total_followers"],
            {"new_followers": "新关注", "unfollows": "取关", "net_followers": "净增", "total_followers": "累计"},
            max_rows=10,
        ),
        "",
        f"阅读人数和净增关注在重合日期上的相关系数约为 {read_follow_corr:.2f}。这只能作为方向信号，不建议当成严格因果。",
        "",
        "## 分享和收藏峰值",
        "",
        "分享峰值：",
        "",
        table_md(top_shares, ["日期", "shares", "favorites", "published_articles"], {"shares": "分享", "favorites": "收藏", "published_articles": "发文数"}, max_rows=10),
        "",
        "收藏峰值：",
        "",
        table_md(top_favorites, ["日期", "favorites", "shares", "published_articles"], {"favorites": "收藏", "shares": "分享", "published_articles": "发文数"}, max_rows=10),
        "",
        "这两张表后面可以做“资产感”判断：阅读高但收藏/分享弱，可能只是推荐流点击；阅读不一定最高但收藏/分享强，可能更适合沉淀成资料包、课程、skill 或 n8n 节点。",
        "",
        "## 内容机制判断",
        "",
        "1. 爆发型：`GPT-image-2 搭建电商主图详情页`、`500 张电商图反推提示词 SOP`、`电商数据分析 skill`。共同点是结果具体、任务明确、可复制、标题里有资产承诺。",
        "2. 壁垒型：`Codex + 飞书小数据中台`、`Codex 蒸馏同行竞品`、`Codex + GitHub 仓库跑通电商作图 SOP`。共同点是账号长期能力强，但要把“工具链”翻译成业务成果，否则新读者门槛偏高。",
        "3. 认知型：岗位、普通人路线、模型选择、工具比较类可以做信任铺垫，但需要和可执行路径绑定，单纯观点很难稳定放大。",
        "4. 视觉侧：高阅读不等于图片越多越好。强文章的图片作用是证明结果、展示报告/流程/截图，而不是凑图。后续分析应看“首图是不是结果锚点”和“每屏有没有反馈点”。",
        "",
        "## 后续 Skill 草案",
        "",
        "建议做成一个 `wechat-account-data-review` skill，输入一个周期文件夹，自动跑以下流程：",
        "",
        "1. 读取文章档案：`article_meta.json`、`layout.md`、`visual_analysis.md`、长截图路径。",
        "2. 读取后台导出：趋势表、用户增长表、可选的单篇明细表。",
        "3. 清洗表格：识别真 Excel、HTML 伪 xls、横向多表、日期格式、标题归一化。",
        "4. 合并文章：按发布日期 + 标题归一化匹配，失败时用同日模糊匹配。",
        "5. 输出四层结论：账号总览、头部文章复盘、题材/标题/视觉信号、下周期选题建议。",
        "6. 标记数据边界：每篇互动缺失时，只输出相关性，不输出精确归因。",
        "",
        "## 每周/月建议你固定导出的数据",
        "",
        "1. `数据趋势/来源分析`：也就是这次的 `tendency`，保留渠道阅读、分享、收藏、原文点击、文章来源榜。",
        "2. `用户分析/用户增长`：也就是这次的 `user_analysis`，保留每日新增、取关、净增、累计。",
        "3. `单篇内容分析`（如果后台能导）：每篇文章阅读、分享、收藏、赞/在看、读后关注、完读率、评论。这个是下一步最关键的数据。",
        "4. `文章 HTML 档案`：爬虫继续保留 HTML、图片、长截图、视觉拆解。它负责解释“为什么这篇像这个样子”，后台数据负责解释“读者怎么反应”。",
        "",
        "## 这轮清洗出的文件",
        "",
        "- `wechat-clean-daily-channel-reads.csv`：每日分渠道阅读",
        "- `wechat-clean-daily-interactions.csv`：每日分享、收藏、原文点击、发文数",
        "- `wechat-clean-article-source-reads.csv`：文章 x 来源渠道阅读",
        "- `wechat-clean-daily-followers.csv`：每日关注增长",
        "- `wechat-account-article-metrics.csv`：文章 HTML 特征 + 阅读来源表现合并表",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tendency", required=True, type=Path)
    parser.add_argument("--user-analysis", required=True, type=Path)
    parser.add_argument("--archive-dir", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)

    daily_channel, daily_interactions, article_source = read_tendency(args.tendency)
    followers = read_user_analysis(args.user_analysis)
    archive = read_archive(args.archive_dir)
    performance = build_article_performance(article_source)
    archive_perf = merge_archive_performance(archive, performance)

    daily_channel.to_csv(args.output_dir / "wechat-clean-daily-channel-reads.csv", index=False, encoding="utf-8-sig")
    daily_interactions.to_csv(args.output_dir / "wechat-clean-daily-interactions.csv", index=False, encoding="utf-8-sig")
    article_source.to_csv(args.output_dir / "wechat-clean-article-source-reads.csv", index=False, encoding="utf-8-sig")
    followers.to_csv(args.output_dir / "wechat-clean-daily-followers.csv", index=False, encoding="utf-8-sig")
    archive_perf.to_csv(args.output_dir / "wechat-account-article-metrics.csv", index=False, encoding="utf-8-sig")

    report = make_report(
        archive_perf=archive_perf,
        daily_channel=daily_channel,
        daily_interactions=daily_interactions,
        article_source=article_source,
        followers=followers,
        archive_dir=args.archive_dir,
        tendency_path=args.tendency,
        user_path=args.user_analysis,
    )
    (args.output_dir / "wechat-account-data-analysis.md").write_text(report, encoding="utf-8")

    print(f"archive_articles={len(archive_perf)}")
    print(f"daily_channel_rows={len(daily_channel)}")
    print(f"daily_interaction_days={len(daily_interactions)}")
    print(f"article_source_rows={len(article_source)}")
    print(f"follower_days={len(followers)}")
    print(f"matched_articles={archive_perf['total_readers'].notna().sum()}")
    print(args.output_dir / "wechat-account-data-analysis.md")


if __name__ == "__main__":
    main()
