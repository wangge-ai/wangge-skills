---
name: xiaohongshu-account-dissector
description: Use when analyzing Xiaohongshu accounts, AI/AIGC creators, 小红书博主, 笔记样本,
  account positioning, cover/title/content patterns, conversion paths, or when creating
  reusable teardown reports from Xiaohongshu pages, screenshots, exported notes, or
  public web sources.
license: MIT
---

# Xiaohongshu Account Dissector

## Overview

This skill turns Xiaohongshu account pages, note screenshots, exported text, or public sources into reusable creator teardown reports. The goal is not to copy a creator, but to identify positioning, content mechanics, trust signals, and transferable patterns for the user's own account.

## Evidence Modes

Use the strongest available evidence and label limits clearly.

1. **Chrome logged-in mode**: preferred for Xiaohongshu account pages, note grids, comments, and screenshots. Use when the user has logged in through Chrome or explicitly asks to use Chrome.
2. **User-provided mode**: use account links, screenshots, copied note text, exported HTML, CSV, or Markdown. Best when Chrome access is unavailable.
3. **Public-web mode**: use web search, official sites, third-party data pages, interviews, and case articles. Always cite sources and mark data as secondary when not from the account page.

Never inspect cookies, passwords, local storage, or private messages. Do not claim real-time follower/note metrics unless they were visible during this run.

## Capture Workflow

For each account, collect:

- Account name, handle/link when available, bio, visible follower/like/note counts, verification or identity signals.
- Top visible note grid: at least 12 recent or representative notes when possible.
- 3-5 high-performing or highly representative notes: title, cover style, topic, format, visible likes/saves/comments if available.
- Comment cues when visible: what users ask for, praise, challenge, or request next.
- Conversion clues: course, community, tool, consulting, store,公众号,资料包, link-in-bio, pinned notes.
- Screenshots or source URLs when useful. Save screenshots only when needed for later visual comparison.

If the page blocks access, record the block and switch to public-web mode instead of inventing data.

## Dissection Framework

Write each account teardown in this order:

1. **一句话定位**: what mindshare the account owns.
2. **账号人设**: expert, practitioner, designer, educator, tool curator, diary-style learner, IP/worldview account, or brand account.
3. **内容货架**: recurring columns and topic clusters.
4. **封面系统**: visual assets, typography, color, screenshots, result images, face/persona, layout density.
5. **标题模型**: recurring hooks such as pain point, result, comparison, warning, list, diary, tutorial, challenge.
6. **笔记结构**: how notes unfold: problem -> result -> steps -> template -> caveat -> CTA.
7. **爆款机制**: why users click, save, comment, or follow.
8. **信任机制**: proof of work, credentials, real tests, before/after, data, failures, personal story.
9. **转化路径**: how attention becomes follows, leads, paid products, communities, or external-platform traffic.
10. **可借鉴/别照搬**: separate transferable patterns from mismatched tactics.

## AI Account Type Tags

Use one or more labels to compare accounts:

- **热点解读型**: tracks model/product releases, wins through speed and judgment.
- **工具教程型**: step-by-step usage, templates, screenshots, high save value.
- **作品展示型**: AI images/videos/stories as the product; visual consistency matters most.
- **场景实战型**: uses AI in real work scenarios; trust comes from proof-of-work.
- **课程转化型**: education funnel; free notes build demand for paid learning.
- **资料包/清单型**: collectable resources, prompts, workflows, keywords.
- **个人日记型**: learning journey and experiments; relatability beats authority.
- **专业身份型**: designer, operator, teacher, developer, founder; authority comes from domain judgment.
- **AI教练课程型**: instructor-led AI education; authority, simplified tutorials, repeatable frameworks, and paid training/contact paths matter.
- **专业身份视觉型**: design/creative identity plus AI works; visual output, style consistency, licensing/custom collaboration, and portfolio proof matter.
- **入口IP型**: broad AI explainer or ecosystem connector; speed, naming power, cross-platform presence, and concept translation matter more than single-note templates.
- **AI视频实战日记型**: personal practice around AI video or creative tools; diary voice, repeated experiments, workflows, and before/after outputs matter.
- **AI设计笔记型**: design-oriented AI notes; prompts, cases, visual workflows, templates, and collectable learning notes matter.
- **机构课程矩阵型**: organization-backed education account; course system, teacher brand, content matrix, free lessons, live classes, and conversion assets matter.

## Output Template

```markdown
## 账号：{name}

### 1. 一句话定位
{positioning}

### 2. 账号基本盘
- 账号身份：
- 可见数据：
- 主要内容形态：
- 证据来源：

### 3. 内容货架
| 栏目/主题 | 典型笔记 | 用户为什么会看 |
|---|---|---|

### 4. 封面与标题
- 封面：
- 标题：
- 高频标题模型：

### 5. 爆款机制
{why it works}

### 6. 信任与转化
{trust and funnel}

### 7. 我们怎么学
- 可以借鉴：
- 不适合照搬：
- 适配到 目标公众号：
```

## Synthesis Across Accounts

After 2+ accounts, add a cross-account section:

- Common patterns across winners.
- Differences by account type.
- What the user should copy structurally, not stylistically.
- A 7-day or 30-day content experiment list if the user is planning to operate an account.

For `目标公众号`, prefer takeaways that support: first-person real use, 电商/职场 AI scenarios, templates, screenshots, caveats, and “普通人也能看懂”的教程感.

## Common Mistakes

- Do not rank accounts only by follower count.
- Do not copy titles without understanding the traffic intent.
- Do not treat AI visual accounts and AI tutorial accounts as the same model.
- Do not hide evidence gaps; say when data needs App verification.
- Do not overfit to one viral post. Look for repeatable columns.
- Do not turn the final report into platform gossip. Focus on reusable content mechanisms.
