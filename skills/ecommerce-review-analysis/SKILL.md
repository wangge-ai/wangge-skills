---
name: ecommerce-review-analysis
description: 按数据质量、清洗、分类、人群、归因、参照物与报告七步分析评论。
license: MIT
metadata:
  source_pack: '19'
---

# E-commerce Review Analysis

## Overview

Turn a raw product-review export into a report-ready, board-friendly analysis and an
actionable master table. The workflow runs in seven sequential passes over the same
comment corpus and is built to survive the failure modes that silently corrupt naive
keyword classification (false-positive negatives from phrases like "不辣嘴", double-counted
themes, fabricated competitors).

This is a **workflow** skill. Each step produces a file the user can verify before the
next step runs, so the agent must pause for confirmation after steps that the user asked
to sign off on (the original flow confirmed the cleaning rules before deleting anything).

## When to Use

- User uploads `*.xlsx` / `*.csv` review data and asks for "评价分析 / 数据质量检查 /
  评论分类 / 人群分析 / 归因 / 参照物分析 / 可视化报告".
- User wants the full pipeline OR any single step (steps are independently runnable).
- User provides a numbered "提示词 N" matching this pipeline — map it to the steps below.

## Hard Rules (apply to every step)

These rules prevented the most damaging errors in real runs. Follow them without being
asked twice:

1. **Negative-perception calibration (否定感知校准).** Before counting any keyword as
   positive or negative, check the 1–2 characters immediately before it. If they contain
   `不 / 没 / 无 / 别 / 未`, the phrase is NEGATED and must NOT be counted as the sentiment
   you originally intended.
   - "不辣嘴" → 正面 (not negative "辣").
   - "刷掉黑点" / "黑点明显小了" → 正面 (not negative "小了").
   - "性价比高" → 正面 (not negative "性价比").
   - "怕又是智商税，结果真香" → 正面 (not negative "智商税").
   Implement a `neg_aware(text, phrases)` helper that returns the hit only when no negation
   prefix is present. See `references/keyword_calibration.md`.

2. **Use multi-character phrases, not bare single characters.** "黄 / 白 / 亮" alone
   match "明白 / 白天 / 亮了". For visual/whitening factors use phrases like
   `黑点, 牙黄, 牙齿白, 变白, 亮晶晶, 牙渍, 洁白`. This cut a whitening factor from a
   fabricated 53% down to its real 42%.

3. **Per-comment unique theme counting.** When a comment can match multiple phrases within
   one theme, count the *theme* at most once per comment. When a comment matches multiple
   themes, decide a priority order and pick a single "main" category; keep the rest as
   multi-label. This avoids inflating theme frequencies (e.g. "贵是贵了点" matching both
   "贵了" and "贵是贵").

4. **Do not fabricate competitors.** If no explicit competitor brand is named, write
   "未发现明确竞品品牌" — never invent names. Real brands only enter the output when they
   literally appear in a comment. Count fuzzy competitors ("其他牌子 / 之前用的牙膏") as a
   separate "模糊竞品" category.

5. **Verify before claiming.** After each classification pass, pull the raw comment text
   for every flagged theme and eyeball 5–10 samples. Drop or fix any theme whose samples
   contradict the label. This caught "换牙期→售后", "旧版=0", and "口味不符=0" in real runs.

6. **Preserve excluded-but-valuable data.** When cleaning, never silently drop follow-up
   comments (追评) attached to deleted default reviews. Keep a separate "追评子样本" sheet.
   If a short negative comment (e.g. the only 差评) is caught by a length rule, surface it
   to the user rather than deleting — they may want it kept.

## Workflow

Read `references/workflow_prompts.md` for the exact prompt templates that drive each step.
Steps 1 and 7 are gated by user confirmation in the canonical flow.

### Step 1 — Data Quality Check (提示词 1)
- Count raw rows vs valid comments; check completeness of content/author/time/SKU/rating.
- Flag empty comments, default templates ("该用户未填写评价内容"), cross-product/SKU leakage,
  and follow-up comments (追评).
- Output: `数据质量检查表.xlsx` with sheets 检查摘要 / 字段完整性 / 默认空评论明细 /
  疑似非目标商品 / 追评明细 / SKU分布 / 排除规则与有效样本口径 / 全量标记.
- **Pause and let the user confirm the exclusion rules before proceeding.**

### Step 2 — Cleaning (user-confirmed rules)
- Delete: default/template comments, suspected other-product/ultra-short meaningless
  comments, any missing-critical-field rows. Keep follow-up comments in a sub-sample.
- Output: `清洗后评价数据.xlsx` (有效评论 + 追评子样本) and `已删除评价数据.xlsx` (with reason).

### Step 3 — Structured Classification (提示词 3)
- For every valid comment output: 评论内容 / 主分类 / 多标签分类 / 情感倾向 / 判断依据 /
  评论时间 / 已购规格 / 评论人.
- Main category (pick ONE): 质量 / 价格 / 包装 / 使用体验 / 售后服务 / 其他.
- Multi-label: any combination, separated by `;`.
- Sentiment (4 levels): 正面 / 混合 / 负面 / 其他. When unsure → 其他 (do not guess).
- Output: `结构化分类结果.xlsx` (the "母表" for all later steps).

### Step 4 — Buyer & Scenario Profiling (提示词 4)
- Buyer identity: 妈妈 / 爸爸 / 祖辈 / 家长(未披露性别) / 其他(无法判断). Pie chart.
- Usage scenarios (multi-label, one comment may hit several): 防蛀护齿 / 口味吸引 / 含氟安全 /
  朋友口碑 / 牙医推荐 / 复购 / 解决抗拒刷牙 / 促销囤货 / 其他. Bar chart.
- Output: `购买人群与需求场景分析.xlsx` + 2 PNG charts. Every chart has a title, counts, and %.

### Step 5 — Attribution (提示词 5)
- **Positive attribution**: top satisfied factors with frequency, %, representative quotes,
  the product strength, and a "amplifiable brand expression".
- **Negative attribution**: top negative keywords with frequency, % of problem comments,
  quotes, real pain point, optimization opportunity.
- **Executable checklist**: (1) core word-of-mouth driver, (2) which negative issue is
  priority + which are trends vs isolated (define trend threshold explicitly, e.g.
  ≥8% of problem comments), (3) top 3 optimization directions.
- Output: `正面负面归因分析.xlsx` + 2 PNG charts. Charts embed in the final report.

### Step 6 — Reference / Competitor Analysis (提示词 6)
- Identify references users compare against: explicit competitor brands, fuzzy competitors,
  alternative categories, the product's OWN old version/spec, same-store other SKUs/price tiers.
- Count frequency, list Top references, extract representative quotes, judge which side users
  prefer and why, and derive differentiation entry points.
- Columns: 参照物类型 / 名称或描述 / 提及频次 / 对比维度 / 代表原话 / 用户倾向 / 差异化机会.
- Output: `参照物提及分析.xlsx` + 1 PNG. If no named brand appears, write
  "未发现明确竞品品牌" — never fabricate.

### Step 7 — Consolidated Visual Report + Master Table (提示词 7)
- Build a self-contained `用户评价分析报告.html` with 8 sections (执行摘要 / 分析口径 /
  分类与情感分布 / 购买对象与场景 / 正面归因 / 负面归因 / 参照物与差异化 / 全局总结),
  with charts embedded as base64 (offline-viewable) and every chart annotated with sample
  size +口径.
- Build `用户评价分析母表.xlsx`: one row per comment with ALL derived tags merged
  (情感 / 主分类 / 购买者身份 / 规格年龄段 / 动机 / 正面因素 / 负面关键词 / 命中参照物),
  plus 字段说明 and 统计汇总 sheets. This table must stay filterable/sortable.
- Reuse the SAME keyword logic from steps 3–6 so numbers reconcile with earlier deliverables.

## Tooling Notes

- Use `pandas` + `openpyxl` for Excel I/O; `matplotlib` (Agg backend) for charts. Install into
  the managed venv: `python -m venv .../envs/default && .../pip install pandas openpyxl matplotlib`.
- Chinese chart fonts: prefer `Microsoft YaHei` / `SimHei` in `plt.rcParams['font.sans-serif']`.
- Embed PNGs in HTML via base64 so the report is portable.
- Column for images in openpyxl is `from openpyxl.drawing.image import Image` — do NOT confuse
  it with `matplotlib.font_manager` (no `Font` class there).

## Resources

- `references/workflow_prompts.md` — the 7 prompt templates (提示词 1–7) to paste/adapt.
- `references/keyword_calibration.md` — `neg_aware()` reference, example calibrated lexicons
  per step, per-step output schemas, and the trend-threshold guidance.
- `scripts/analyze_reviews_skeleton.py` — a runnable CLI for Step 3 classification and master-table merging.
  CSV uses the standard library; XLSX additionally needs openpyxl. Pass `--input`, `--output-dir`,
  `--text-column` and optionally `--lexicon`. Replace the example dental lexicon for the target category.
  This scaffold does not perform the full seven-step workflow or generate the complete report.
