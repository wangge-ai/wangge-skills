#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build-search-queries.py

为 beginner-tutorial-writer Skill 生成按权重分配好的搜索查询任务清单。

用法:
    python3 build-search-queries.py --product "WorkBuddy"
    python3 build-search-queries.py --product "Coze" --vendor "字节"
    python3 build-search-queries.py --product "Dify" --weights '{"wechat_official_accounts":50,"bilibili":20,"official":30}'
    python3 build-search-queries.py --product "Notion" --total-queries 40

输出: JSON 数组，每个元素 = {"source": "...", "query": "...", "priority": int}
Agent 可以直接消费这份清单去并行调度搜索 API。
"""

from __future__ import annotations

import argparse
import json
import math
import os
import sys
from pathlib import Path

try:
    import yaml  # type: ignore
except ImportError:
    print(
        "[error] 缺少 PyYAML，请先安装：pip install pyyaml",
        file=sys.stderr,
    )
    sys.exit(2)


DEFAULT_CONFIG_PATH = (
    Path(__file__).resolve().parent.parent / "templates" / "search-config.yaml"
)


def load_config(path: Path) -> dict:
    if not path.exists():
        print(f"[error] 配置文件不存在: {path}", file=sys.stderr)
        sys.exit(2)
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def merge_weights(default: dict, override: dict | None) -> dict:
    """用户传入的 weights 覆盖默认权重；未覆盖的来源保持默认。"""
    if not override:
        return dict(default)
    merged = dict(default)
    for k, v in override.items():
        if k not in merged:
            # 允许用户引入新来源（哪怕没有 query 模板，也会被记录）
            merged[k] = v
        else:
            merged[k] = v
    return merged


def normalize_weights(weights: dict) -> dict:
    total = sum(weights.values())
    if total <= 0:
        raise ValueError("所有权重之和必须 > 0")
    return {k: v / total for k, v in weights.items()}


def allocate_quota(
    norm_weights: dict, total_queries: int
) -> dict:
    """按比例分配每个来源的查询数；用最大余数法兜底凑齐总数。"""
    raw = {k: w * total_queries for k, w in norm_weights.items()}
    floor = {k: math.floor(v) for k, v in raw.items()}
    used = sum(floor.values())
    remainder = total_queries - used
    # 把剩余名额分给小数部分最大的来源
    remainders = sorted(
        ((k, raw[k] - floor[k]) for k in raw), key=lambda x: x[1], reverse=True
    )
    for k, _ in remainders[:remainder]:
        floor[k] += 1
    return floor


def build_queries(
    product: str,
    vendor: str | None,
    quota: dict,
    query_templates: dict,
) -> list[dict]:
    out: list[dict] = []
    q_value = product if not vendor else f"{product} {vendor}"
    for source, n in quota.items():
        if n <= 0:
            continue
        templates = query_templates.get(source, [f"{{q}}"])
        # 轮流挑模板，凑足 n 条
        for i in range(n):
            tmpl = templates[i % len(templates)]
            rendered = tmpl.replace("{q}", q_value).strip()
            out.append(
                {
                    "source": source,
                    "query": rendered,
                    "priority": i + 1,
                }
            )
    return out


def main() -> int:
    parser = argparse.ArgumentParser(
        description="为新手教程生成按权重分配的搜索查询任务清单",
    )
    parser.add_argument("--product", required=True, help="产品名（必填）")
    parser.add_argument("--vendor", default=None, help="出品方（可选）")
    parser.add_argument(
        "--weights",
        default=None,
        help='覆盖默认权重的 JSON 字符串，例如 \'{"wechat_official_accounts":50}\'',
    )
    parser.add_argument(
        "--total-queries",
        type=int,
        default=30,
        help="总查询次数（默认 30；建议 20–60）",
    )
    parser.add_argument(
        "--config",
        default=str(DEFAULT_CONFIG_PATH),
        help=f"配置文件路径，默认: {DEFAULT_CONFIG_PATH}",
    )
    parser.add_argument(
        "--pretty",
        action="store_true",
        help="美化 JSON 输出",
    )
    args = parser.parse_args()

    config = load_config(Path(args.config))
    default_weights = config.get("default_weights", {})
    query_templates = config.get("query_templates", {})

    override = None
    if args.weights:
        try:
            override = json.loads(args.weights)
        except json.JSONDecodeError as e:
            print(f"[error] --weights 不是合法 JSON: {e}", file=sys.stderr)
            return 2

    weights = merge_weights(default_weights, override)
    norm = normalize_weights(weights)
    quota = allocate_quota(norm, args.total_queries)
    queries = build_queries(
        product=args.product,
        vendor=args.vendor,
        quota=quota,
        query_templates=query_templates,
    )

    indent = 2 if args.pretty else None
    payload = {
        "product": args.product,
        "vendor": args.vendor,
        "total_queries": args.total_queries,
        "weights_used": weights,
        "quota_per_source": quota,
        "queries": queries,
    }
    print(json.dumps(payload, ensure_ascii=False, indent=indent))
    return 0


if __name__ == "__main__":
    sys.exit(main())
