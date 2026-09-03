#!/usr/bin/env python3
"""Analyze a multi-platform ecommerce dataset with trend, ranking, review, and alert dimensions."""

from __future__ import annotations

import argparse
import csv
import json
import math
import re
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from statistics import mean


FIELD_ALIASES = {
    "snapshot_date": ["snapshot_date", "date", "日期", "采集日期"],
    "platform": ["platform", "平台"],
    "category": ["category", "类目"],
    "product_id": ["product_id", "sku", "商品id", "商品 ID", "id"],
    "product_name": ["product_name", "name", "title", "商品", "商品名", "标题"],
    "brand": ["brand", "品牌"],
    "shop": ["shop", "店铺", "店铺名"],
    "rank": ["rank", "排名", "搜索排名", "类目排名"],
    "price": ["price", "价格", "售价", "到手价"],
    "original_price": ["original_price", "原价", "划线价"],
    "sales_volume": ["sales_volume", "销量", "销售件数", "月销", "销量信号"],
    "sales_amount": ["sales_amount", "销售额", "GMV", "成交额"],
    "rating": ["rating", "评分"],
    "review_count": ["review_count", "评论数", "评价数"],
    "positive_rate": ["positive_rate", "好评率", "正评率"],
    "negative_rate": ["negative_rate", "差评率", "负评率"],
    "keyword": ["keyword", "关键词", "搜索词"],
    "keyword_rank": ["keyword_rank", "关键词排名", "搜索词排名"],
    "traffic_index": ["traffic_index", "流量指数", "流量"],
    "conversion_rate": ["conversion_rate", "转化率"],
    "selling_points": ["selling_points", "卖点", "核心卖点", "claims"],
    "negative_reviews": ["negative_reviews", "差评", "负面评价", "投诉", "痛点"],
    "promo_tag": ["promo_tag", "促销", "活动", "优惠"],
    "source_url": ["source_url", "url", "链接"],
    "notes": ["notes", "备注", "note"],
}


def norm_key(value: str) -> str:
    return re.sub(r"\s+", "", str(value).strip().lower())


def canonicalize_row(row: dict) -> dict:
    normalized = {norm_key(k): v for k, v in row.items()}
    output: dict[str, str] = {}
    for target, aliases in FIELD_ALIASES.items():
        output[target] = ""
        for alias in aliases:
            key = norm_key(alias)
            if key in normalized and str(normalized[key]).strip():
                output[target] = str(normalized[key]).strip()
                break
    return output


def read_rows(path: Path) -> list[dict]:
    if path.suffix.lower() == ".json":
        data = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(data, dict):
            data = data.get("items") or data.get("records") or data.get("data") or []
        if not isinstance(data, list):
            raise ValueError("JSON input must be a list or contain items/records/data list")
        return [canonicalize_row(row) for row in data if isinstance(row, dict)]

    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return [canonicalize_row(row) for row in csv.DictReader(f)]


def parse_float(value: str) -> float | None:
    if not value:
        return None
    cleaned = str(value).replace(",", "").replace("%", "").strip()
    match = re.search(r"-?\d+(?:\.\d+)?", cleaned)
    return float(match.group()) if match else None


def parse_int(value: str) -> int | None:
    parsed = parse_float(value)
    return int(parsed) if parsed is not None else None


def parse_date(value: str) -> datetime | None:
    if not value:
        return None
    for fmt in ("%Y-%m-%d", "%Y/%m/%d", "%Y.%m.%d"):
        try:
            return datetime.strptime(value.strip(), fmt)
        except ValueError:
            pass
    return None


def split_terms(value: str) -> list[str]:
    if not value:
        return []
    parts = re.split(r"[,，/、;；|｜\n]+", value)
    return [part.strip() for part in parts if part.strip()]


def markdown_table(headers: list[str], rows: list[list[object]]) -> str:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(cell).replace("\n", " ") for cell in row) + " |")
    return "\n".join(lines)


def product_key(row: dict) -> str:
    return row["product_id"] or f'{row["platform"]}:{row["brand"]}:{row["product_name"]}'


def latest_rows(rows: list[dict]) -> list[dict]:
    by_product: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        by_product[product_key(row)].append(row)
    latest = []
    for group in by_product.values():
        latest.append(sorted(group, key=lambda r: parse_date(r["snapshot_date"]) or datetime.min)[-1])
    return latest


def price_bucket(price: float | None) -> str:
    if price is None:
        return "未提供"
    if price < 30:
        return "30元以下"
    if price < 60:
        return "30-59元"
    if price < 100:
        return "60-99元"
    if price < 200:
        return "100-199元"
    return "200元以上"


def safe_pct(new: float | None, old: float | None) -> float | None:
    if new is None or old in (None, 0):
        return None
    return (new - old) / old * 100


def linear_slope(xs: list[float], ys: list[float]) -> float | None:
    if len(xs) < 3 or len(xs) != len(ys):
        return None
    x_mean = mean(xs)
    y_mean = mean(ys)
    denom = sum((x - x_mean) ** 2 for x in xs)
    if denom == 0:
        return None
    return sum((x - x_mean) * (y - y_mean) for x, y in zip(xs, ys)) / denom


def elasticity_for_group(group: list[dict]) -> float | None:
    xs: list[float] = []
    ys: list[float] = []
    for row in group:
        price = parse_float(row["price"])
        sales = parse_float(row["sales_volume"])
        if price and price > 0 and sales and sales > 0:
            xs.append(math.log(price))
            ys.append(math.log(sales))
    return linear_slope(xs, ys)


def describe_elasticity(value: float | None) -> str:
    if value is None:
        return "样本不足"
    if value <= -1.2:
        return "价格敏感明显"
    if value < -0.2:
        return "价格敏感中等"
    if value <= 0.2:
        return "价格变化影响不明显"
    return "销量与价格同向，可能受流量/活动干扰"


def previous_latest_pairs(rows: list[dict]) -> list[tuple[dict, dict]]:
    pairs: list[tuple[dict, dict]] = []
    by_product: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        by_product[product_key(row)].append(row)
    for group in by_product.values():
        ordered = sorted(group, key=lambda r: parse_date(r["snapshot_date"]) or datetime.min)
        if len(ordered) >= 2:
            pairs.append((ordered[-2], ordered[-1]))
    return pairs


def build_report(rows: list[dict], category: str, source_note: str, price_alert_pct: float, rank_alert_change: int) -> str:
    rows = [row for row in rows if any(row.values())]
    latest = latest_rows(rows)
    pairs = previous_latest_pairs(rows)
    platforms = Counter(row["platform"] or "未提供" for row in latest)
    dates = sorted({row["snapshot_date"] for row in rows if row["snapshot_date"]})

    lines: list[str] = []
    lines.append(f"# {category} 电商数据分析报告")
    lines.append("")
    lines.append(f"数据行数：{len(rows)}")
    lines.append(f"商品数：{len(latest)}")
    lines.append(f"平台：{'、'.join(platform for platform, _ in platforms.most_common()) or '未提供'}")
    if dates:
        lines.append(f"时间范围：{dates[0]} 至 {dates[-1]}")
    lines.append(f"数据说明：{source_note}")
    lines.append("限制说明：本报告只分析输入表格里的字段；监控、预测、价格弹性、预警均基于已有快照或用户导出数据，不代表实时平台数据。")
    lines.append("")

    lines.append("## 1. 总览")
    overview_rows = []
    for platform, count in platforms.most_common():
        platform_rows = [row for row in latest if (row["platform"] or "未提供") == platform]
        prices = [parse_float(row["price"]) for row in platform_rows]
        prices = [price for price in prices if price is not None]
        sales = [parse_float(row["sales_volume"]) for row in platform_rows]
        sales = [item for item in sales if item is not None]
        overview_rows.append([
            platform,
            count,
            f'{mean(prices):.1f}' if prices else "未提供",
            f'{sum(sales):.0f}' if sales else "未提供",
        ])
    lines.append(markdown_table(["平台", "商品数", "最新均价", "最新销量合计"], overview_rows))
    lines.append("")

    lines.append("## 2. 价格带和销量")
    bucket_rows = []
    buckets: dict[str, list[dict]] = defaultdict(list)
    for row in latest:
        buckets[price_bucket(parse_float(row["price"]))].append(row)
    for bucket, bucket_rows_data in sorted(buckets.items()):
        sales = [parse_float(row["sales_volume"]) for row in bucket_rows_data]
        sales = [item for item in sales if item is not None]
        names = "；".join((row["product_name"] or "未命名") for row in bucket_rows_data[:3])
        bucket_rows.append([bucket, len(bucket_rows_data), f"{sum(sales):.0f}" if sales else "未提供", names])
    lines.append(markdown_table(["价格带", "商品数", "最新销量合计", "代表商品"], bucket_rows))
    lines.append("")

    lines.append("## 3. 价格趋势和预警候选")
    alert_rows = []
    trend_rows = []
    for prev, current in pairs:
        price_change = safe_pct(parse_float(current["price"]), parse_float(prev["price"]))
        sales_change = safe_pct(parse_float(current["sales_volume"]), parse_float(prev["sales_volume"]))
        rank_prev = parse_int(prev["rank"])
        rank_current = parse_int(current["rank"])
        rank_change = rank_current - rank_prev if rank_prev is not None and rank_current is not None else None
        trend_rows.append([
            current["platform"] or "未提供",
            current["product_name"] or "未命名",
            f'{price_change:.1f}%' if price_change is not None else "未提供",
            f'{sales_change:.1f}%' if sales_change is not None else "未提供",
            rank_change if rank_change is not None else "未提供",
        ])
        reasons = []
        if price_change is not None and price_change <= -abs(price_alert_pct):
            reasons.append(f"降价 {abs(price_change):.1f}%")
        if rank_change is not None and rank_change >= rank_alert_change:
            reasons.append(f"排名后退 {rank_change} 位")
        if reasons:
            alert_rows.append([current["platform"], current["product_name"], "；".join(reasons), current["promo_tag"] or ""])
    lines.append(markdown_table(["平台", "商品", "价格变化", "销量变化", "排名变化"], trend_rows[:20]))
    lines.append("")
    lines.append("预警候选：")
    lines.append(markdown_table(["平台", "商品", "触发原因", "活动/备注"], alert_rows or [["无", "无", "未触发阈值", ""]]))
    lines.append("")

    lines.append("## 4. 价格弹性粗算")
    elasticity_rows = []
    groups: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        groups[product_key(row)].append(row)
    for group in groups.values():
        ordered = sorted(group, key=lambda r: parse_date(r["snapshot_date"]) or datetime.min)
        current = ordered[-1]
        elasticity = elasticity_for_group(ordered)
        elasticity_rows.append([
            current["platform"] or "未提供",
            current["product_name"] or "未命名",
            f"{elasticity:.2f}" if elasticity is not None else "样本不足",
            describe_elasticity(elasticity),
        ])
    lines.append(markdown_table(["平台", "商品", "弹性估算", "解释"], elasticity_rows[:20]))
    lines.append("说明：价格弹性这里只做快照表粗算；如果同时有大促、投流、排名变化，需要结合流量字段看，不能单独当定价结论。")
    lines.append("")

    lines.append("## 5. 关键词和排名")
    keyword_groups: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for row in rows:
        if row["keyword"]:
            keyword_groups[(row["platform"] or "未提供", row["keyword"])].append(row)
    keyword_rows = []
    for (platform, keyword), group in keyword_groups.items():
        ranks = [parse_float(row["keyword_rank"]) for row in group]
        ranks = [rank for rank in ranks if rank is not None]
        traffic = [parse_float(row["traffic_index"]) for row in group]
        traffic = [item for item in traffic if item is not None]
        latest_group = sorted(group, key=lambda r: parse_date(r["snapshot_date"]) or datetime.min)[-1]
        keyword_rows.append([
            platform,
            keyword,
            f"{mean(ranks):.1f}" if ranks else "未提供",
            f"{mean(traffic):.0f}" if traffic else "未提供",
            latest_group["product_name"] or "未命名",
        ])
    keyword_rows.sort(key=lambda row: float(row[2]) if str(row[2]).replace(".", "", 1).isdigit() else 9999)
    lines.append(markdown_table(["平台", "关键词", "平均关键词排名", "平均流量指数", "最新代表商品"], keyword_rows[:20] or [["未提供", "未提供", "未提供", "未提供", ""]]))
    lines.append("")

    lines.append("## 6. 评论情感和 VOC")
    term_counter = Counter()
    neg_counter = Counter()
    sentiment_rows = []
    for row in latest:
        term_counter.update(split_terms(row["selling_points"]))
        neg_counter.update(split_terms(row["negative_reviews"]))
        sentiment_rows.append([
            row["platform"] or "未提供",
            row["product_name"] or "未命名",
            row["rating"] or "未提供",
            row["review_count"] or "未提供",
            row["positive_rate"] or "未提供",
            row["negative_rate"] or "未提供",
            row["negative_reviews"] or "未提供",
        ])
    lines.append(markdown_table(["平台", "商品", "评分", "评论数", "好评率", "差评率", "差评/VOC"], sentiment_rows[:20]))
    lines.append("")
    lines.append(f"高频卖点：{'、'.join(term for term, _ in term_counter.most_common(8)) or '未提供'}")
    lines.append(f"高频负面词：{'、'.join(term for term, _ in neg_counter.most_common(8)) or '未提供'}")
    lines.append("")

    lines.append("## 7. 流量和转化")
    traffic_rows = []
    for row in sorted(latest, key=lambda r: parse_float(r["traffic_index"]) or 0, reverse=True):
        traffic_rows.append([
            row["platform"] or "未提供",
            row["product_name"] or "未命名",
            row["traffic_index"] or "未提供",
            row["conversion_rate"] or "未提供",
            row["sales_volume"] or "未提供",
        ])
    lines.append(markdown_table(["平台", "商品", "流量指数", "转化率", "销量"], traffic_rows[:20]))
    lines.append("")

    lines.append("## 8. 可行动建议")
    lines.append("- 商品链接/截图类材料：先转成证据表，不要直接写结论。")
    lines.append("- 有历史快照时：重点看价格变化、排名变化、销量变化是否同向。")
    lines.append("- 有关键词字段时：优先盯平均排名靠前但转化偏低的词，检查主图和标题承接。")
    lines.append("- 有评论字段时：把差评词和卖点放在一起看，找详情页 FAQ、主图信任背书和产品改款入口。")
    lines.append("- 有监控需求时：本脚本先给预警候选；真正的定时监控要接入授权数据源和定时任务。")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze a multi-platform ecommerce dataset.")
    parser.add_argument("--input", required=True, help="CSV or JSON ecommerce dataset")
    parser.add_argument("--out", required=True, help="Output Markdown report path")
    parser.add_argument("--category", required=True, help="Category name")
    parser.add_argument("--source-note", default="用户提供的表格", help="Source note shown in the report")
    parser.add_argument("--price-alert-pct", type=float, default=5.0, help="Price drop threshold for alert candidates")
    parser.add_argument("--rank-alert-change", type=int, default=5, help="Rank worsening threshold for alert candidates")
    args = parser.parse_args()

    input_path = Path(args.input)
    out_path = Path(args.out)
    rows = read_rows(input_path)
    report = build_report(rows, args.category, args.source_note, args.price_alert_pct, args.rank_alert_change)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(report, encoding="utf-8")
    print(f"Wrote {out_path} from {len(rows)} rows")


if __name__ == "__main__":
    main()
