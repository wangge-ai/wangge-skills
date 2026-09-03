---
name: github-social-radar
description: Use when the user asks to find, monitor, collect, deduplicate, or summarize GitHub repositories recently or currently popular on Chinese social platforms such as WeChat official accounts, Bilibili, and Douyin; triggers include "最近/本周比较火的 GitHub 仓库", "公众号/B站/抖音推荐的 GitHub", "每周好用 GitHub 分享", "GitHub 社媒情报", "每天看 GitHub 分享整理", "去重这些平台提到的仓库", "近一周火的 AI 开源项目", or requests to build a daily/weekly GitHub radar for a Chinese AI practice account.
---

# GitHub Social Radar

Find GitHub repositories recently or currently popular on social platforms, deduplicate them by `owner/repo`, preserve the original sharer's reason, verify GitHub facts, and output a daily or weekly intelligence table for our own tool discovery, trial runs, repo dissection, and optional WeChat article planning.

This skill is for practical discovery and curation. The primary goal is to find repositories we may actually use, install, test, or learn from. WeChat/公众号 writing material is secondary. Use `github-repo-dissector` after this skill when the user chooses a repo for quick HTML dissection, deep clone analysis, or a visual report.

Core principle:

> Do not only collect "hot repos". Translate every repo into: who recommended it, why that creator would notice it, what pain it solves, how it was discovered, and whether it is worth our own trial.

## Default Scope

- Time window: hot-first, not fixed. By default collect the most recent/high-signal 1-10 relevant posts per platform or creator. Use 7-30 day recency filters when the search tool supports them, but do not hard-exclude a good "本周/近一周/最近/刚开源/爆火/Star 暴涨" source only because the query wording does not contain an exact date. If the user gives a strict range, obey it.
- Platforms: WeChat official accounts, Bilibili, Douyin.
- Topic focus: AI, LLM, Agent, Claude Code, Codex, MCP, RAG, workflow, automation, data tools, ecommerce AI, visual/AIGC tools, and developer productivity.
- Output language: Chinese.
- Default output: Markdown intelligence report. Create HTML only when the user asks for HTML/report/view/page/screenshot.

Always show exact scan date and any confirmed publish dates. If a source only says "今天/昨天/本周/近一周" without an absolute date, convert it when possible from the page context; otherwise mark `日期待确认`.

## Creator Seed Library

Read `social-creator-seeds.md` before searching. It records public creators/accounts that repeatedly share GitHub repositories.

This seed library is living memory, not static documentation. Whenever a scan discovers a useful new public creator, account, weekly ranking source, trend source, or project-curation source, update `social-creator-seeds.md` in the same turn before the final answer.

Also read these references when the user asks why creators recommend repos, how to mine eye-catching repos, or what we should try next:

- `social-creator-patterns.md`: creator/source recommendation logic.
- `social-repo-pain-taxonomy.md`: pain-first repo classification.
- `social-repo-mining-playbook.md`: how to discover eye-catching repos.
- `social-repo-trial-outcomes.md`: our own trial feedback and watchlist.
- `social-repo-appearance-log.md`: cross-run appearance frequency, dedup history, and repeated-social-signal tracking.

Use two lanes every time:

1. Broad discovery: search by topic and title patterns to find new posts and new creators.
2. Seeded creator search: search known creators directly, such as `账号名 GitHub`, `账号名 开源项目`, `账号名 AI 开源`, and platform-specific profile/content pages.

After a scan, update the seed library only when the creator/source is public and useful for future GitHub discovery. Add creators when they repeatedly share GitHub repos, share list-style GitHub recommendations, or provide clear project reasons. Add utility/trend sources when they provide current GitHub rankings, growth signals, AI summaries, or direct repo links we can use for our own trial selection.

### Living Seed Update Protocol

Use this protocol on every radar run:

1. Before searching, read `social-creator-seeds.md`.
2. During search, record every new public creator/source that appears useful.
3. Verify the visible publish date or last-updated date when possible. A title saying "近一周" is not enough if the page was published months ago.
4. If the creator/source is clearly useful, add or update it under `Current Seeds` or `Trend / Utility Sources`.
5. If it is promising but date, identity, or repeatability is uncertain, add it under `Candidate Seeds` with `待核验`.
6. Update existing rows instead of duplicating the same creator under slightly different names.
7. Write the scan date, evidence date, why it is useful, and 3-6 future search queries.
8. Do not store private user info, cookies, account tokens, internal IDs, or non-public identifiers.

If a user asks to "再搜几个作者", "更新来源", "以后也要新增进去", or similar, treat it as a seed-library update task and persist the change.

## Workflow

### 1. Build Search Plan

Read `social-search-playbook.md` when you need query templates.

Search broadly and search known creators. Do not rely on one keyword family.

1. Run broad queries for recent/hot GitHub sharing patterns.
2. Run creator-seed queries from `social-creator-seeds.md`.
3. Search the wider web for platform-indexed pages if native platform search is unavailable.
4. Extract all GitHub URLs, repo names, and unresolved project names.
5. Keep a source log before deduplication.

If a platform blocks search, login, transcript, or full content, do not bypass it. Mark the source as "无法完整访问" and continue with accessible evidence. If WeChat public search misses results, do not conclude "公众号没有"; say "本轮公开检索未命中可核验原文" and suggest seed-account/profile/manual-link follow-up.

### 2. Source Record Extraction

For every social post/video/article, capture:

- Platform
- Author/account
- Title
- Publish date
- Source URL
- Mentioned GitHub repo(s)
- Author's recommendation reason
- Visible engagement if public and useful: reads, likes, views, coins, comments, favorites, etc.
- Features or demo shown by the author
- Evidence type: title / summary / full text / video intro / transcript / screenshot / demo
- Confidence: high / medium / low

Keep "author's reason" separate from "our judgment". Do not turn your own analysis into the author's words.

### 2.5 Creator Logic Extraction

For every known or new creator/source, infer and record:

- Why this creator/source would recommend this kind of repo.
- Which audience or pain they appear to target.
- Their preferred repo shapes: hot list, official release, Skill, Agent tool, tutorial, SaaS alternative, demo-heavy project, weekly growth item, etc.
- Their discovery method when visible: growth ranking, GitHub Trending, official announcement, demo screenshot, issue/discussion, repo collection, platform buzz, or own test.
- Whether the source is useful for us: `high / medium / low`.

If the pattern is stable or newly discovered, update `social-creator-patterns.md` before final response.

### 3. Normalize And Deduplicate Repos

Use canonical key `owner/repo`.

Rules:

- Convert any `github.com/owner/repo` URL to `owner/repo`.
- Remove URL suffixes such as `/tree/main`, `/blob/...`, `/issues/...`, `?tab=readme`.
- If only a project name appears, search GitHub to resolve it. If uncertain, mark `待确认` rather than guessing.
- Merge duplicate mentions into one repo card.
- Preserve all source records under that repo.
- Mark `多平台重复出现` when at least two platforms mention the same repo.

### 3.5 Cross-Run Dedup And Appearance Frequency

Before final prioritization, read `social-repo-appearance-log.md` when it exists.

Track repeated appearances as a weak but useful signal:

- `mention_count`: every recorded source record or historical scan mention. This is a lower-bound count from our own radar, not global popularity.
- `platform_count`: distinct public platforms/surfaces, such as B站, 抖音, 公众号/文章源, GitHub trend source, HN/GitHub trend source.
- `source_count`: distinct creators/accounts/sources. If the same account cross-posts the same episode to B站 and 抖音, count 2 platforms but usually 1 source.
- `scan_dates`: distinct radar dates where the repo appeared.
- `status`: new / repeated / warming / already quick-scanned / installed / smoke-tested / watch / risk.

Priority rules:

- A repo appearing across 2+ platforms should be marked `跨平台重复出现`.
- A repo appearing across 2+ distinct accounts/sources should be marked `多账号重复出现`.
- A repo appearing on 2+ scan dates should be marked `持续出现`.
- Repeated appearance can raise a repo's priority by one level only when the pain is clear and trial cost is reasonable.
- Repeated appearance is not proof that the repo works. Do not write “稳定可用” unless it was actually tested.

After each scan, update `repo-appearance-log.md` with new source records, last seen date, lower-bound counts, and current action status. Do this before the final answer.

### 4. Verify GitHub Facts

For each deduped repo, verify low-cost facts:

- GitHub URL
- Description / README one-line positioning
- Stars, forks, open issues
- Primary language
- License
- Latest release if visible
- Last pushed/updated date
- Demo/docs/screenshots if visible
- Install or lowest-cost try path
- Requirements: API key, paid model, Docker, GPU, login, browser extension, local app

Prefer the existing stats script when available:

```powershell
python <skills-root>/github-repo-dissector/scripts/github_repo_stats.py https://github.com/owner/repo --fast
```

If GitHub API is rate-limited, use accessible repo page/README facts and state the limit. Do not invent metrics.

### 4.5 Pain-First Classification

Before scoring, classify each repo using `social-repo-pain-taxonomy.md`.

Every candidate must answer:

- It solves which pain?
- Who feels that pain?
- What work step does it remove or compress?
- Is it a tool, workflow, Skill/template, learning resource, model, infrastructure, dataset, or content asset?
- Can we use it in Codex, ecommerce, content production, data analysis, or internal workflow?

If a repo cannot be mapped to a real pain, downgrade it to watchlist even if its star count is high.

### 5. Score And Prioritize

Use two scores:

1. **Practical Priority Score**: decide whether we should short-dissect, trial, or watch.
2. **Eye-Opening Index**: decide whether the repo represents a surprising useful direction.

Practical Priority Score, 35 points:

| Dimension | Max |
|---|---:|
| Source evidence quality | 5 |
| Creator/source usefulness | 5 |
| Pain clarity | 5 |
| Workflow relevance to us | 5 |
| Demo/README/quickstart clarity | 5 |
| GitHub repo health | 5 |
| Trial friction | 5 |
| Risk/boundary clarity | 5 |

Eye-Opening Index, 25 points:

| Dimension | Max |
|---|---:|
| Clear pain in one sentence | 5 |
| New workflow or new category | 5 |
| Visible demo/result/screenshot | 5 |
| Low enough trial cost | 5 |
| Fits our Codex/ecommerce/content/data workflow | 5 |

Priority labels:

- `A`: worth short dissection or trial now.
- `B`: useful watchlist or later comparison.
- `C`: weak evidence, unclear pain, stale, or high-risk.
- `Risk`: only discuss/observe boundaries, do not provide misuse workflow.

Use `social-repo-mining-playbook.md` when deciding why a repo is eye-catching.

### 5.5 Trial Feedback Loop

When a repo from this radar is later quick-dissected, installed, smoke-tested, rejected, or adopted, update `social-repo-trial-outcomes.md`.

Record:

- Repo and source.
- Why it was selected.
- Pain category.
- Action taken: quick scan / short HTML / clone / install / smoke test / adopted / rejected / watch.
- Result and blockers.
- Whether it should influence future mining.

Do not claim trial success in radar reports unless `repo-trial-outcomes.md` or the current run records a real trial.

### 6. Output Report

Use `social-output-template.md` for the full template.

Default sections:

1. Scan Overview
2. Source Log
3. Creator Recommendation Logic
4. Pain Map
5. Deduped Repository Table
6. Eye-Opening Candidates
7. Our Trial Queue
8. Repeated Appearance Signals
9. Creator Seed Hits And New Creators
10. Suggested Next Actions
11. Data Boundaries
12. Seed Library Updates
13. Trial Outcome Updates

When the user wants a daily dashboard, save it with a date in the filename:

```text
YYYY-MM-DD_GitHub热点仓库社媒雷达.md
```

When the user wants HTML, use `html-color-system` and do not expose internal collection mechanics in the public-facing page. Reader-facing HTML should show what the repos are, who shared them, why people are sharing them, what they can do, and what should not be exaggerated.

HTML hero rules:

- Do not title the report as "最近 15 天" unless the user explicitly asks for that time window.
- Prefer titles such as `GitHub 热点仓库社媒雷达` or `最近中文社媒在分享哪些 AI GitHub 仓库`.
- Keep the first-screen title readable and contained: max hero title size should usually be 56-64px on desktop, with responsive `clamp()` and line-height that prevents overflow.
- Show creator/account names as useful source signals.
- Keep data boundaries visible but not dominant.

## Boundaries

- Do not claim full coverage of WeChat/Bilibili/Douyin unless search access is complete.
- Do not say a platform has no relevant posts just because a generic query failed. Prefer "本轮公开检索未命中可核验原文".
- Do not include posts outside a user-specified strict window unless clearly marked as contextual/background.
- Do not include posts without a confirmable publish date as time-sensitive evidence unless clearly marked as `日期待确认`.
- Do not treat platform likes/views as proof that the repo works.
- Do not say a repo is stable, production-ready, or safe unless it was actually tested and evidence supports it.
- Do not bypass login, captcha, anti-bot, paywall, or platform restrictions.
- Do not quote long passages from articles or transcripts.
- Do not publish private cookies, tokens, local paths, or account identifiers.
- Do not let the seed library drift into a stale note. If new useful public sources are found, persist them.

## Handoff To Other Skills

- Use `github-repo-dissector` for a selected repo's quick HTML report, deep clone mode, trial run, or architecture analysis.
- Use `github-wechat-curation` when turning the radar results into WeChat article angles, title options, screenshot positions, or publication material.
- Use `html-color-system` for any generated HTML page.
- When `github-repo-dissector` finishes a real trial or rejection of a radar candidate, update `social-repo-trial-outcomes.md`.
