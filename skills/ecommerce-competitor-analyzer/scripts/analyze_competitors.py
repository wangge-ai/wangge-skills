#!/usr/bin/env python3
"""Build a first-pass ecommerce competitor report from CSV or JSON evidence."""

from __future__ import annotations

import argparse
import csv
import json
import math
import re
from collections import Counter, defaultdict
from pathlib import Path


FIELD_ALIASES = {
    "evidence_id": ["evidence_id", "sample_id", "证据编号"],
    "rank": ["rank", "位置", "页面顺序"],
    "product_name": ["product_name", "name", "title", "商品", "商品名", "产品名", "标题"],
    "brand": ["brand", "品牌"],
    "platform": ["platform", "平台"],
    "price": ["price", "价格", "售价"],
    "sales_signal": ["sales_signal", "volume", "销量", "月销", "销售", "销量信号"],
    "rating_or_review_signal": ["rating_or_review_signal", "评价", "评分", "评论"],
    "selling_points": ["selling_points", "卖点", "核心卖点", "claims", "利益点"],
    "negative_reviews": ["negative_reviews", "差评", "负面评价", "投诉", "痛点"],
    "source_url": ["source_url", "url", "链接"],
    "image_path": ["image_path", "图片", "主图", "local_path", "normalized_path"],
    "price_scope": ["price_scope", "price_label", "价格口径", "价格标签"],
    "is_ad": ["is_ad", "广告", "广告标记"],
    "sort_selected": ["sort_selected", "排序", "排序口径"],
    "source_type": ["source_type", "来源类型"],
    "raw_text": ["raw_text", "原始文本"],
    "notes": ["notes", "备注", "note"],
}


def norm_key(key: str) -> str:
    return re.sub(r"\s+", "", str(key).strip().lower())


def canonicalize_row(row: dict) -> dict:
    normalized = {norm_key(k): v for k, v in row.items()}
    output = {}
    for target, aliases in FIELD_ALIASES.items():
        value = ""
        for alias in aliases:
            key = norm_key(alias)
            if key in normalized and str(normalized[key]).strip():
                value = str(normalized[key]).strip()
                break
        output[target] = value
    return output


def read_rows(path: Path) -> list[dict]:
    if path.suffix.lower() == ".json":
        data = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(data, dict):
            data = data.get("items") or data.get("records") or data.get("data") or []
        if not isinstance(data, list):
            raise ValueError("JSON input must be a list or contain items/records/data list")
        return [canonicalize_row(x) for x in data if isinstance(x, dict)]

    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        return [canonicalize_row(row) for row in reader]


def parse_price(value: str) -> float | None:
    if not value:
        return None
    cleaned = value.replace(",", "")
    match = re.search(r"(\d+(?:\.\d+)?)", cleaned)
    return float(match.group(1)) if match else None


def split_terms(value: str) -> list[str]:
    if not value:
        return []
    parts = re.split(r"[,，/、;；|｜\n]+", value)
    return [p.strip() for p in parts if p.strip()]


def price_bucket(price: float) -> str:
    if price < 50:
        return "50元以下"
    if price < 100:
        return "50-99元"
    if price < 200:
        return "100-199元"
    if price < 500:
        return "200-499元"
    return "500元以上"


def markdown_table(headers: list[str], rows: list[list[str]]) -> str:
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(cell).replace("\n", " ") for cell in row) + " |")
    return "\n".join(lines)


def build_facts(rows: list[dict], category: str) -> dict:
    rows = [row for row in rows if any(row.values())]
    ads = sum(1 for row in rows if row["is_ad"].strip().lower() in {"yes", "true", "1", "是"})
    organic = sum(1 for row in rows if row["is_ad"].strip().lower() in {"no", "false", "0", "否"})
    items = []
    for index, row in enumerate(rows, 1):
        items.append({
            "evidence_id": row["evidence_id"] or f"ROW_{index:03d}",
            "page_position": row["rank"] or None,
            "product_name": row["product_name"] or None,
            "platform": row["platform"] or None,
            "price_display": row["price"] or None,
            "price_value": parse_price(row["price"]),
            "price_scope": row["price_scope"] or "未标注",
            "sales_display": row["sales_signal"] or None,
            "is_ad": row["is_ad"].strip().lower() in {"yes", "true", "1", "是"},
            "source_type": row["source_type"] or None,
            "source_url": row["source_url"] or None,
            "sort_selected": row["sort_selected"] or None,
            "review_signal": row["rating_or_review_signal"] or None,
        })
    missing_fields = []
    if not any(row["rating_or_review_signal"] or row["negative_reviews"] for row in rows):
        missing_fields.append("reviews")
    if not any(row["selling_points"] for row in rows):
        missing_fields.append("structured_selling_points")
    if not any(row["price_scope"] for row in rows):
        missing_fields.append("price_scope")
    return {
        "category": category,
        "denominator": {"total": len(rows), "organic": organic, "ads": ads},
        "items": items,
        "missing_fields": missing_fields,
        "allowed_inference": {
            "sample_comparison": True,
            "market_share": False,
            "true_sales": False,
            "conversion_rate": False,
            "official_ranking": False,
        },
    }


def build_report(rows: list[dict], category: str, own_product: str = "") -> str:
    rows = [r for r in rows if any(r.values())]
    facts = build_facts(rows, category)
    denominator = facts["denominator"]
    platforms = Counter(r["platform"] or "未提供" for r in rows)
    prices = [parse_price(r["price"]) for r in rows]
    numeric_prices = [p for p in prices if p is not None and not math.isnan(p)]
    buckets: dict[str, list[dict]] = defaultdict(list)
    for row, price in zip(rows, prices):
        if price is not None:
            buckets[price_bucket(price)].append(row)

    term_counter = Counter()
    negative_counter = Counter()
    for row in rows:
        term_counter.update(split_terms(row["selling_points"]))
        negative_counter.update(split_terms(row["negative_reviews"]))

    lines: list[str] = []
    lines.append(f"# {category} 竞品拆解报告")
    lines.append("")
    lines.append(
        f"分析范围：总样本 {denominator['total']} 条；自然样本 {denominator['organic']} 条；"
        f"广告样本 {denominator['ads']} 条"
    )
    source_types = sorted({row["source_type"] for row in rows if row["source_type"]})
    lines.append(f"数据来源：{'；'.join(source_types) if source_types else '用户提供的 CSV/JSON 表格'}")
    if own_product:
        lines.append(f"我方产品：{own_product}")
    lines.append("样本说明：页面顺序样本只用于样本内比较；广告与自然位分开计数。页面顺序不等于官方榜单名次。")
    lines.append("")

    lines.append("## 1. 先看结论")
    if numeric_prices:
        price_evidence = "、".join(f"[{item['evidence_id']}]" for item in facts["items"] if item["price_value"] is not None)
        lines.append(f"- 样本展示价格从 {min(numeric_prices):.2f} 元到 {max(numeric_prices):.2f} 元（证据：{price_evidence}）；不同价格标签不可直接视为同一成交口径。")
    if term_counter:
        top_terms = "、".join(t for t, _ in term_counter.most_common(5))
        lines.append(f"- 高频卖点集中在：{top_terms}。")
    if negative_counter:
        top_neg = "、".join(t for t, _ in negative_counter.most_common(5))
        lines.append(f"- 差评或顾虑集中在：{top_neg}。")
    lines.append(f"- 当前缺失项：{'、'.join(facts['missing_fields']) or '无整列缺失'}；缺失字段不做外推。")
    lines.append("")

    lines.append("## 2. 证据与分母")
    platform_rows = [[platform, str(count)] for platform, count in platforms.most_common()]
    lines.append(markdown_table(["平台", "样本数"], platform_rows or [["未提供", "0"]]))
    lines.append("")
    lines.append("销量字段仅保留页面原文，例如“人收货”或“本月行业热销”；它是页面展示信号，不等于真实成交量、销售额或市场份额。")
    lines.append("")

    lines.append("## 3. 样本展示价格分布")
    lines.append("以下只描述输入样本的展示价格，不代表类目市场价格带。广告样本不进入自然样本价格区间。")
    lines.append("")
    lines.append("### 价格口径分布（自然样本）")
    scope_groups: dict[str, list[float]] = defaultdict(list)
    for row in rows:
        if row["is_ad"].strip().lower() in {"yes", "true", "1", "是"}:
            continue
        value = parse_price(row["price"])
        if value is not None:
            scope_groups[row["price_scope"] or "未标注"].append(value)
    scope_rows = [
        [scope, str(len(values)), f"{min(values):.2f}", f"{max(values):.2f}"]
        for scope, values in sorted(scope_groups.items())
    ]
    lines.append(markdown_table(["价格口径", "自然样本数", "最低展示价", "最高展示价"], scope_rows or [["未提供", "0", "未提供", "未提供"]]))
    lines.append("")
    lines.append("### 全部样本展示价格区间")
    price_rows = []
    for bucket, bucket_rows in sorted(buckets.items()):
        examples = "；".join((r["product_name"] or "未命名") for r in bucket_rows[:3])
        points = Counter()
        for r in bucket_rows:
            points.update(split_terms(r["selling_points"]))
        price_rows.append([bucket, str(len(bucket_rows)), examples, "、".join(t for t, _ in points.most_common(3))])
    lines.append(markdown_table(["价格带", "样本数", "代表商品", "常见卖点"], price_rows or [["未提供", "0", "", ""]]))
    lines.append("")

    lines.append("## 4. 竞品证据对比表")
    matrix_rows = []
    for r in rows[:30]:
        matrix_rows.append([
            f"[{r['evidence_id'] or f'ROW_{len(matrix_rows) + 1:03d}'}]",
            r["rank"] or "未提供",
            r["product_name"] or "未提供",
            r["platform"] or "未提供",
            r["price"] or "未提供",
            r["price_scope"] or "未标注",
            r["sales_signal"] or "未提供",
            "广告" if r["is_ad"].strip().lower() in {"yes", "true", "1", "是"} else "自然/未标广告",
        ])
    lines.append(markdown_table(["证据", "页面位置", "商品", "平台", "展示价格", "价格口径", "销量展示", "广告边界"], matrix_rows))
    lines.append("")

    lines.append("## 5. 可执行结论与待验证项")
    lines.append("- 定价：先按相同价格标签重算自然样本价格带；首单价、补贴后、优惠后与未标注价不可混为结算价。")
    lines.append("- 广告：广告样本只能说明付费位置中出现了该商品，不用于推断自然排序表现。")
    lines.append("- 商品页事实：本输入是搜索结果页证据；规格、到手价、评价与详情页信任证据仍需逐链接核验。")
    lines.append("- 销量：保留页面销量文案，不换算成交额，不据此计算市场份额。")
    lines.append("")

    lines.append("## 6. 限制说明")
    lines.append("本报告基于用户提供的页面样本生成。不得外推真实销量、成交额、转化率、市场份额或官方排名；缺失的评论、SKU、结算价与商品页事实保持未知。")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Build an ecommerce competitor report from CSV/JSON evidence.")
    parser.add_argument("--input", required=True, help="CSV or JSON evidence table")
    parser.add_argument("--out", required=True, help="Output Markdown report path")
    parser.add_argument("--category", required=True, help="Category name")
    parser.add_argument("--own-product", default="", help="Optional own product name")
    parser.add_argument("--json-out", default="", help="Optional structured facts JSON path")
    args = parser.parse_args()

    input_path = Path(args.input)
    out_path = Path(args.out)
    rows = read_rows(input_path)
    report = build_report(rows, args.category, args.own_product)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(report, encoding="utf-8")
    if args.json_out:
        json_path = Path(args.json_out)
        json_path.parent.mkdir(parents=True, exist_ok=True)
        json_path.write_text(json.dumps(build_facts(rows, args.category), ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {out_path} from {len(rows)} rows")


if __name__ == "__main__":
    main()
