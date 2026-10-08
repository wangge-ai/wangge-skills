---
name: wechat-account-data-review
description: Use when reviewing WeChat Official Account backend exports, 公众号后台数据,
  weekly/monthly account performance, tendency*.xls, user_analysis.xls, article archives,
  scraped WeChat HTML, visual_analysis.md, or when preparing n8n/Dify/Codex workflows
  for公众号文章数据复盘.
license: MIT
---

# WeChat Account Data Review

## Overview

Use this skill to combine WeChat backend exports with locally archived article HTML. Treat backend numbers as performance evidence and archived HTML/visual analysis as mechanism evidence.

Core rule: separate **confirmed article metrics**, **daily aggregate signals**, and **qualitative HTML/visual clues**. Never turn missing article-level metrics into zero or exact attribution.

## Quick Start

Run the bundled parser when the user provides backend exports plus an article archive:

```powershell
$env:PYTHONIOENCODING='utf-8'
python "scripts/analyze_wechat_exports.py" `
  --tendency "./inputs/tendency.xls" `
  --user-analysis "./inputs/user_analysis.xls" `
  --archive-dir "./inputs/article-archives" `
  --output-dir "./outputs/wechat\account-review\2026-06-20\outputs"
```

Use PowerShell `Resolve-Path` or environment variables for Chinese paths if inline Python path literals become garbled. Resolve the current Python runtime first; this computer does not assume `python` is on PATH.

## Expected Inputs

| Input | Required | Notes |
|---|---:|---|
| `tendency*.xls` | yes | WeChat data trend export. Often old binary Excel with three horizontal tables. |
| `user_analysis.xls` | yes | WeChat user growth export. Often HTML disguised as `.xls`. |
| article archive directory | yes | Directory containing per-article `article_meta.json`, `visual_analysis.md`, `layout.md`, images, and screenshots. |
| single-article detail export | optional | Strongly preferred if available: per-article shares, favorites, likes, read-after-follow, completion rate. |

If parsing fails or a new export shape appears, read `references/export-data-contract.md`.

## Workflow

1. Parse backend exports first.
2. Parse article archive metadata and visual roles.
3. Normalize titles with date + punctuation-insensitive title matching.
4. Merge article metrics by publish date and normalized title; use same-day fuzzy matching only when exact match fails.
5. Produce a Markdown account report and cleaned CSVs.
6. Explain data sufficiency before drawing conclusions.
7. For writing-model analysis, use the merged metrics first, then apply `wechat-article-dissector` to the top and bottom article groups.

## Interpretation Contract

Use these labels consistently:

| Evidence | Safe conclusion |
|---|---|
| Article has `全部` source row | Confirmed total article readers for the export range. |
| Article has only channel rows, no `全部` row | Partial source evidence only; do not compute total readers. |
| Daily shares/favorites | Daily account-level interaction signal; approximate article signal only on single-article days. |
| Daily followers | Account-level growth signal; do not claim exact per-article follower conversion. |
| `visual_analysis.md` first image role | HTML/visual clue about first-screen promise and proof. |
| Article HTML/image count | Layout and evidence-density clue, not a standalone success cause. |

Write “相关/可能推动/方向信号” when attribution is approximate. Reserve “带来/导致/转化” for confirmed article-level metrics.

## Output Contract

The parser writes these files to the output directory:

| File | Purpose |
|---|---|
| wechat-account-data-analysis.md | Main account review report. |
| `wechat-account-article-metrics.csv` | Article metadata + source readers + visual features. |
| `wechat-clean-daily-channel-reads.csv` | Daily channel reads. |
| `wechat-clean-daily-interactions.csv` | Daily shares, favorites, original-link clicks, article count. |
| `wechat-clean-article-source-reads.csv` | Article/source/channel reader rows. |
| `wechat-clean-daily-followers.csv` | Daily follower growth. |

Mention both the report and the CSVs in the final response. Link output files only when they are in the current thread `outputs` directory.

## Review Heuristics

Prioritize these lenses:

- Recommendation dependency: what share of listed source reads comes from `推荐`.
- Repeatable topic engine: which categories repeatedly perform, not which single article was lucky.
- Offer clarity: whether title promises a concrete output, report, SOP, Skill, tutorial, comparison, or asset.
- First-screen proof: whether the first visual proves the result before the article explains background.
- Asset value: compare reading with daily shares/favorites to identify articles worth turning into资料包, skill, workflow, course, or follow-up series.
- Boundary: identify what cannot be concluded without single-article detail exports.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Treating missing `全部` reads as 0 | Keep as unknown and exclude from average-reader calculations. |
| Reading `user_analysis.xls` with only `pd.read_excel` | Parse as HTML table when Excel format detection fails. |
| Summing source rows and calling it total reads | Use `全部` row for total; use channel rows for source structure. |
| Claiming one article caused follower spikes | Say follower growth correlates with the date/range unless single-article follow data exists. |
| Doing text-only article analysis | Use `visual_analysis.md`, image count, first image role, and long screenshot paths to explain layout and proof. |
| Letting n8n/Dify auto-write conclusions | Keep attribution labels and missing-data warnings in the prompt/output schema. |

## Automation Notes

For n8n or Dify, split the workflow into visible human-participation checkpoints:

1. Upload/export folder and choose review range.
2. Run parser script.
3. Show data sufficiency summary for human confirmation.
4. Select articles for deep qualitative dissection.
5. Generate weekly/monthly account review.
6. Generate next-period topic plan.

Do not hide the whole process behind one opaque “generate content” node. The user wants to learn the workflow.
