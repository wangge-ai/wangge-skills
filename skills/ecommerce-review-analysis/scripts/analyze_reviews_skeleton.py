#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
电商用户评论分析 - 通用骨架（7 步管线）
========================================
复用方式：
  1. 把本文件复制到工作目录；
  2. 在下方「词表区」用目标品类的真实词替换示例（儿童牙膏仅为示范）；
  3. 用 --text-column 指定评论列；用 --lexicon 指定词表 JSON；
  4. 运行：python analyze_reviews_skeleton.py --input reviews.csv --output-dir output

本骨架实现可复用的核心机制：
  - neg_aware() 否定感知助手（防"不辣嘴"误判负面）
  - 每条评论每主题唯一计数（防重复计数）
  - 主分类 + 多标签 + 情感四档（Step 3）
  - 合并母表（Step 7 的核心）
Chart 生成、Step 1/2/4/5/6 的具体逻辑请参照 references/keyword_calibration.md 同套范式实现。
"""

import re
import argparse
import csv
import json
from collections import Counter
from pathlib import Path

# ============ 配置 ============

# ============ 词表区（★ 必须按目标品类重写，以下仅为儿童牙膏示范） ============
MAIN_CATS = {
    "质量": ["黑点", "牙黄", "变白", "防蛀", "龋齿", "蛀牙", "牙渍"],
    "使用体验": ["味道", "口味", "草莓", "孩子爱刷", "抢着刷", "不抗拒", "温和", "不辣", "吞咽"],
    "价格": ["价格", "便宜", "划算", "性价比", "贵", "实惠", "分量", "量少"],
    "包装": ["包装", "泵头", "按压", "礼盒", "外观"],
    "售后服务": ["客服", "退换", "换货", "物流异常", "漏发", "少发"],
}
POS_WORDS = ["满意", "喜欢", "推荐", "回购", "赞", "不错", "好用", "很好", "值得",
             "惊喜", "放心", "安心", "温和", "不辣", "不抗拒", "有效", "改善"]
NEG_WORDS = ["辣嘴", "偏辣", "分量少", "量少", "太少", "失望", "后悔", "踩雷",
             "退货", "差评", "没效果", "抗拒", "不满意"]
MIX_WORDS = ["但", "不过", "但是", "唯一", "美中不足", "除了", "稍", "略微", "有点", "略"]
PRIORITY = {"质量": 5, "使用体验": 4, "价格": 3, "包装": 2, "售后服务": 1}


# ============ 核心：否定感知助手 ============
def neg_aware(text, phrases):
    """返回首个未被否定前缀修饰的短语命中；否则 None。"""
    for p in phrases:
        for m in re.finditer(re.escape(p), text):
            pre = text[max(0, m.start() - 2):m.start()]
            if not re.search(r"[不没无别未]", pre):
                return p
    return None


def has_any(text, words):
    return any(w in text for w in words)


def classify_row(text):
    """Step 3：主分类 + 多标签 + 情感倾向。"""
    # 主分类/多标签（每条评论每个主题唯一）
    hits = {}
    for cat, kws in MAIN_CATS.items():
        c = sum(1 for k in kws if k in text)
        if c > 0:
            hits[cat] = c
    if not hits:
        main, multi = "其他", "其他"
    else:
        main = sorted(hits.items(), key=lambda x: (-x[1], -PRIORITY.get(x[0], 0)))[0][0]
        multi = ";".join(sorted(hits.keys(), key=lambda x: -hits[x]))

    # 情感四档
    has_pos = neg_aware(text, POS_WORDS) is not None
    has_neg = neg_aware(text, NEG_WORDS) is not None
    has_mix = has_any(text, MIX_WORDS)
    if has_pos and (has_neg or has_mix):
        sent = "混合"
    elif has_neg and not has_pos:
        sent = "负面"
    elif has_pos and not has_neg:
        sent = "正面"
    else:
        sent = "其他"
    return main, multi, sent


def read_rows(path):
    if path.suffix.lower() == ".csv":
        with path.open(encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fields = reader.fieldnames or []
            return fields, list(reader)
    if path.suffix.lower() == ".xlsx":
        try:
            import openpyxl
        except ImportError as exc:
            raise ValueError("读取 XLSX 需要安装 openpyxl；也可先导出 UTF-8 CSV。") from exc
        workbook = openpyxl.load_workbook(path, read_only=True, data_only=True)
        try:
            records = iter(workbook.active.values)
            fields = [str(v) if v is not None else "" for v in next(records, ())]
            rows = [dict(zip(fields, ["" if v is None else str(v) for v in row]))
                    for row in records]
            return fields, rows
        finally:
            workbook.close()
    raise ValueError("输入格式只支持 CSV 或 XLSX。")


def main():
    parser = argparse.ArgumentParser(description="评论分类骨架：保留原列，添加主题及情感列；不自动完成七步分析。")
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--text-column", default="评论内容")
    parser.add_argument("--lexicon", type=Path, help="JSON 可覆盖 MAIN_CATS/POS_WORDS/NEG_WORDS/MIX_WORDS/PRIORITY；默认仅为儿童牙膏示范。")
    args = parser.parse_args()
    try:
        if args.lexicon:
            config = json.loads(args.lexicon.read_text(encoding="utf-8-sig"))
            for key in ("MAIN_CATS", "POS_WORDS", "NEG_WORDS", "MIX_WORDS", "PRIORITY"):
                if key in config:
                    value = config[key]
                    expected = dict if key in ("MAIN_CATS", "PRIORITY") else list
                    if not isinstance(value, expected):
                        raise ValueError(f"词表 {key} 应为 {expected.__name__}。")
                    globals()[key] = value
        fields, rows = read_rows(args.input)
        if args.text_column not in fields:
            raise ValueError(f"未找到评论列：{args.text_column}")
        derived = ["主分类", "多标签分类", "情感倾向"]
        if any(name in fields for name in derived):
            raise ValueError("输入已有派生分类列，请改用原始评论文件，避免覆盖已有分析。")
        output = args.output_dir / "classified-reviews.csv"
        summary_path = args.output_dir / "summary.json"
        if args.input.resolve() in (output.resolve(), summary_path.resolve()):
            raise ValueError("输出不能覆盖输入文件。")
        for row in rows:
            row.update(zip(derived, classify_row(row.get(args.text_column) or "")))
        args.output_dir.mkdir(parents=True, exist_ok=True)
        with output.open("w", encoding="utf-8-sig", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fields + derived)
            writer.writeheader()
            writer.writerows(rows)
        summary = {
            "rows": len(rows),
            "categories": dict(Counter(row["主分类"] for row in rows)),
            "sentiments": dict(Counter(row["情感倾向"] for row in rows)),
            "limitations": "词表规则分类骨架，仅实现分类和母表合并；须按品类校准，未自动执行完整七步。XLSX 已丢失的数字精度无法恢复。",
        }
        summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(json.dumps({"rows": len(rows), "output": str(output), "summary": str(summary_path)}, ensure_ascii=False))
    except (OSError, ValueError, csv.Error) as exc:
        parser.error(str(exc))


if __name__ == "__main__":
    main()
