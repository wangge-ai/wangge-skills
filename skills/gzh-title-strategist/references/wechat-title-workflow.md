---
name: wechat-title-workflow
description: Use when generating, scoring, comparing, or exporting WeChat Official Account / 微信公众号 article title candidates from a topic, brief, account data review, article HTML archive, or content workflow draft; also use when the user asks for 标题评分, 标题生成, 标题候选表, 选题标题筛选, 推荐流标题判断, n8n/Dify title node, or Codex content workflow title steps.
---

# WeChat Title Workflow

## Overview

Turn one topic or brief into a ranked title candidate table before drafting an article. Keep the workflow explainable: generate candidate titles, score them with the seven title checks, then export Markdown/CSV for human selection or automation.

## Quick Start

Use the bundled script when the user wants a title table or repeatable workflow output:

```powershell
$env:PYTHONIOENCODING='utf-8'
python "$env:USERPROFILE\.codex\skills\wechat-title-workflow\scripts\title_workflow.py" `
  --topic "公众号数据复盘工作流" `
  --context "导出公众号后台趋势表，结合48篇文章HTML做周/月复盘" `
  --count 12 `
  --output-dir outputs
```

Outputs:

- `title-candidates.md`
- `title-candidates.csv`

## Workflow

1. Collect the minimum brief: topic, target reader, source evidence, desired deliverable, and platform/tool constraints.
2. Prefer concrete title formulas over vague tool sharing:
   - sample teardown: `拆了 X 个样本，整理出 Y`
   - input/output automation: `输入 X，自动生成 Y`
   - from-zero tutorial: `从0开始用 X 搭建 Y（附 Z）`
   - first-person practice: `我用 X 做出 Y`
   - priority judgment: `别急着 X，先看 Y`
3. Score each title with the seven checks in [workflow-title-scoring-rubric.md](workflow-title-scoring-rubric.md).
4. Sort by score, then surface 2-3 best options with short reasoning.
5. Do not draft the article unless the user explicitly asks; this skill stops at title generation, scoring, and selection.

## Tooling

- Run [title_workflow.py](../scripts/title_workflow.py) `--help` for supported flags.
- Use `--context` for facts like article count, backend data exports, HTML archive quality, target reader, or whether the result should fit n8n/Dify.
- Use CSV when the next step is a spreadsheet, n8n, Dify, or batch review.
- Use Markdown when the next step is human review in chat or a writing brief.

## Common Mistakes

- Do not lead with `分享一个 AI 工具` unless the title also states the task and deliverable.
- Do not let a tool name overpower the business result.
- Do not treat a 7/7 score as automatic approval; the title still needs a matching first image or screenshot proof.
- Do not continue into article drafting when the user only asked for title analysis.
