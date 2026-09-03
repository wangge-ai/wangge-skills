# Search Playbook

Use this when running a GitHub social radar scan. Search broad topic keywords and known creator/account names together.

## Query Groups

### General

- `GitHub 开源项目 推荐 最近`
- `GitHub AI 工具 推荐`
- `GitHub 每周项目`
- `最近火的 GitHub 项目`
- `近一周比较火的 GitHub 仓库`
- `本周 GitHub 开源项目 推荐`
- `刚开源 GitHub 项目`
- `Star 暴涨 GitHub 项目`
- `不要错过 GitHub 开源项目`
- `宝藏 GitHub 开源项目`
- `AI 开源项目 推荐`
- `开源 AI 工具 GitHub`

### Agent And Coding

- `Claude Code GitHub 项目`
- `Codex GitHub 项目`
- `AI Agent GitHub 推荐`
- `MCP GitHub 项目`
- `RAG GitHub 工具`
- `Cursor GitHub 工具`
- `Agent Skills GitHub`

### Platform Specific

- `site:bilibili.com GitHub AI 工具`
- `site:bilibili.com GitHub 开源项目`
- `site:bilibili.com GitHub 一周热点`
- `site:bilibili.com 近一周 GitHub 开源项目`
- `site:douyin.com GitHub AI 工具`
- `site:douyin.com GitHub 开源项目`
- `site:douyin.com GitHub 一周热点`
- `微信公众号 GitHub AI 工具`
- `公众号 GitHub 开源项目 推荐`
- `搜狗微信 GitHub AI 工具`
- `site:mp.weixin.qq.com GitHub 开源项目 AI`
- `site:mp.weixin.qq.com 近一周 GitHub`
- `site:mp.weixin.qq.com 本周 GitHub 开源`
- `site:mp.weixin.qq.com Star 开源项目`
- `site:mp.weixin.qq.com Claude Code GitHub`

### Creator Seed Queries

Read `creator-seeds.md`, then combine account names with GitHub intent:

- `{creator} GitHub`
- `{creator} 开源项目`
- `{creator} AI 开源`
- `{creator} GitHub 一周热点`
- `{creator} Star`
- `{creator} Claude Code`
- `{creator} Skill`

Use profile pages, column pages, collection pages, and platform search results as source leads. A seed hit is valuable even when it only gives titles; mark evidence confidence honestly.

After each scan, update `creator-seeds.md`:

- Add confirmed useful public creators/sources to `Current Seeds` or `Trend / Utility Sources`.
- Add promising but uncertain sources to `Candidate Seeds`.
- Include scan date, visible evidence date, usefulness, and future search queries.
- Do not add a source as "recent" unless its visible publish/update date is actually recent.
- If the creator/source recommendation logic is clear, update `creator-patterns.md`.
- Classify repos with `repo-pain-taxonomy.md`.
- Use `repo-mining-playbook.md` to decide eye-opening candidates.
- If the scan changes our action queue or follows up a prior repo, update `repo-trial-outcomes.md`.
- Read and update `repo-appearance-log.md` so repeated repos are marked as new / repeated / cross-platform / multi-source / sustained.

### Ecommerce And Content

- `电商 AI GitHub`
- `AI 商品图 GitHub`
- `短视频 AI GitHub`
- `AIGC GitHub 项目 推荐`
- `客服 AI GitHub`

## Search Rules

- Do not default to a hard 15-day window. Prefer recent/hot 1-10 high-signal items per platform or creator.
- Use recency filters of 7-30 days when supported, but keep high-signal "本周/近一周/最近/刚开源/爆火" pages even when the exact date needs follow-up.
- Prefer source pages with visible dates.
- Prefer posts that include actual repo links, screenshots, demos, install commands, or usage examples.
- Treat reposted listicles as weak evidence unless they add their own testing or explanation.
- Record source URL even when only a summary is accessible.
- For WeChat, generic web search is often weak. Search known accounts directly and accept user-provided screenshots/links as valid leads when public post metadata is visible.
- When a platform search misses results, report the limitation as a search/access boundary, not as absence of content.
- When a useful new public creator/source is found, persist it to the seed library before finalizing.
- Do not output a repo list without pain categories and a trial/watch/skip recommendation.
- Do not treat a repo as "new" until it has been checked against `repo-appearance-log.md` and `repo-trial-outcomes.md`.
- Treat repeated appearance as a signal, not a conclusion: it can justify observation or short dissection, but it cannot prove the repo works.

## Repeated Appearance Rules

Use these rules after deduping by `owner/repo`:

- Same repo in B站 and 抖音 from the same account/episode: mark `跨平台重复出现`; count as 2 platforms, usually 1 source.
- Same repo from 2+ different creators/accounts/sources: mark `多账号重复出现`; this is a stronger signal than simple cross-posting.
- Same repo appears across 2+ radar dates: mark `持续出现`; compare with `repo-trial-outcomes.md` before recommending it again.
- If `mention_count >= 3` and the pain is clear: move to observation or short-dissect queue.
- If `source_count >= 2` and trial friction is low: consider priority A/B even when star count is not the largest.
- If the repo is already installed, quick-scanned, or rejected, say that status instead of presenting it as a fresh find.
- If the repo is risk-sensitive, repeated appearance only increases monitoring priority, not usage recommendation.

## Evidence Confidence

- High: source has date, author/account, repo link, and clear reason/demo.
- Medium: source has date and repo mention, but reason is brief or inferred from title/summary.
- Low: source has unclear date, no repo link, or only second-hand mention.
