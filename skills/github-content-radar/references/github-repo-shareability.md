---
name: github-repo-shareability
description: Use when the user wants to judge whether a GitHub repository is worth sharing, packaging for ordinary readers, turning into a lightweight HTML share page, WeChat/Bilibili/Douyin topic, viral title, public-account material, or "10-second understandable" content. Trigger on GitHub repo URLs plus words like 分享、传播、公众号、选题、标题、爆款、普通人、轻量页、转发、为什么火、值不值得写.
---

# GitHub Repo Shareability

## Core Principle

GitHub 项目传播的核心，不是“这个项目技术多强”，而是：

> 普通人能不能在 10 秒内理解它解决了什么问题，并愿意把它转给某个有这个痛点的人。

This skill evaluates a GitHub repo as **content material**, not only as software. It answers: can this repo become a shareable post, light HTML page, WeChat article, Bilibili video, Douyin short, or topic card?

## Relationship To github-repo-dissector

Use this skill after or alongside `github-repo-dissector`.

- `github-repo-dissector`: what the repo is, how to use it, whether to clone/run/deep-analyze it.
- `github-repo-shareability`: whether ordinary readers understand it, why they care, who they share it with, and how to package it.

Default: do **not** clone, do **not** run, do **not** scan full star history. Use low-cost evidence first: GitHub metadata, README first screen, screenshots/demo, release, quickstart, topics.

## Default Output Modes

Choose the lightest mode that satisfies the user.

| User intent | Output |
|---|---|
| User shares a GitHub repo URL / says “测试一下”“看一下这个仓库” | Quick HTML Share Page |
| “这个适合分享吗” | Shareability Verdict |
| “给别人分享” / “轻量页” | Lightweight Share Card / HTML outline |
| “快速拆解成 HTML” / “简短 HTML 报告” | Quick HTML Share Page |
| “公众号选题” | Public Account Topic Pack |
| “标题怎么写” | 5-10 title candidates by formula |
| “为什么火” | Virality Diagnosis |
| “平台怎么发” | WeChat / Bilibili / Douyin adaptation |
| “完整拆解” | Shareability Report, still content-first |

## 10-Second Test

Every repo must pass these four questions before it is treated as good share material:

1. **一句话能不能讲清楚？**  
   If not, simplify before writing anything.
2. **读者会转给谁？**  
   If no obvious recipient exists, the repo is weak for传播.
3. **有没有截图、Demo、最终效果、对比图？**  
   If no visual proof exists, it is harder to share.
4. **和当下哪个热点或真实痛点有关？**  
   AI, Claude, Cursor, design, ecommerce, video, office, privacy, free alternative, workflow automation, etc.

If two or more answers are weak, recommend “not a priority” or “only suitable for technical deep-dive.”

## Shareability Scoring

Score each item 0-5, then give a concise verdict.

| Dimension | What to check |
|---|---|
| Pain clarity | Can ordinary readers understand the problem in one sentence? |
| Share recipient | Can the reader think “I should send this to X”? |
| Visual proof | Screenshots, demo, GIF, before/after, final output, live site |
| Timeliness | Trending, recent release, fast star growth, linked to AI/news/social topic |
| Practicality | Can someone use it soon, or at least understand the result without setup? |
| Scarcity | Free/open-source alternative to paid or closed product |
| Trust signal | Stars, forks, author/org, releases, docs, issues, community |
| Friction | Install complexity, API key, Docker, GPU, CLI, paid dependency |

Verdict bands:

- **35-40**: Strong share candidate. Make a share page or topic immediately.
- **28-34**: Good candidate. Needs a clearer angle or visual proof.
- **20-27**: Niche candidate. Better for technical readers or合集.
- **Below 20**: Not worth sharing broadly unless tied to a hot event.

Always include friction in the verdict. A powerful repo with high setup friction may be good for a long article but bad for quick sharing.

## Repo Content Categories

Classify the repo by传播形态, not just technical type.

| Category | Reader hook | Typical title angle |
|---|---|---|
| Practical tool | “I can use this today” | “这个工具解决了 X” |
| Free alternative | “I found a free/open version” | “开源版 X 来了” |
| AI workflow | “This changes how work gets done” | “不是提示词，是工作流” |
| Black horse | “I’m early to this” | “7 天涨 X Star” |
| Visual/demo project | “Show me the effect” | “一句话生成 X” |
| Fun/weird project | “Send this to friends” | “小众但有趣” |
| Learning resource | “I can learn/practice” | “适合练手/入门” |
| Dev infrastructure | “This helps serious builders” | “让 Agent/代码/部署更高效” |

## Evidence Gathering Order

Keep it fast:

1. GitHub metadata: stars, forks, issues, language, license, updated/release.
2. README first 20-40 lines: one-liner, badges, screenshots, claims.
3. Demo/screenshot/video links: prioritize first-screen visual proof.
4. Quickstart: identify minimum setup friction.
5. Release/announcement/discussion: identify news hook.

Avoid by default:

- Full clone.
- Full README translation.
- Full issue mining.
- Long trend scan.
- Source architecture analysis.

## Shareability Verdict Format

```markdown
## 传播价值判断

- 一句话解释：
- 普通人 10 秒能不能懂：
- 读者会转给谁：
- 为什么最近值得看：
- 最大传播钩子：
- 最大使用门槛：
- 适合平台：
- 是否值得做轻量分享页：
- 是否值得写公众号长文：
- 不要夸大的地方：
```

## Lightweight Share Page Structure

Use when the user says “给别人分享”, “轻量页”, or “别搞复杂”.

Only include:

1. 它是什么
2. 为什么火
3. 适合谁
4. 怎么最低成本试
5. 不要夸大的地方
6. 可直接转发的一段话

Skip:

- Full architecture.
- Deep code analysis.
- Full local trial.
- Competitive landscape.
- Long evidence board.
- Star history scan unless the user asks.

## Quick HTML Share Page

Use when the user asks for fast repo dissection that still produces an HTML report. This is the visual version of a quick share card, not a full repo report.

Hard limits:

- One local `.html` file.
- 1 hero + 3-5 content sections + final verdict.
- No full clone, no full README translation, no source architecture, no long trend scan.
- Prefer one official screenshot/banner/demo image if available.
- Do not show internal process labels in the public page: no `Quick HTML Snapshot`, elapsed seconds, `not cloned`, raw API/source method, or evidence timing in the hero/body. Mention them only in the assistant's final reply when useful.

Required sections:

1. **Hero**: repo name, full GitHub repository URL, repo intro, official visual if available, 4 KPI cards.
2. **它是什么**: 2-3 cards in ordinary-reader language. Start from a repo intro using usage mode + content shape.
3. **为什么值得看/为什么火**: pain, trend, social proof.
4. **适合谁**: suitable / not suitable.
5. **怎么最低成本试**: one path only.
6. **不要夸大**: clear boundaries.

Repo intro formula:

```text
这是一个[usage mode]的[content shape]。
```

Use this formula in the hero or first "它是什么" card. Good examples:

- 这是一个可以直接用的素材库 / Prompt 库。
- 这是一个需要接入到 Agent 的 Skill / Prompt 模板库。
- 这是一个需要本地运行的 CLI 工具 / 代码分析项目。
- 这是一个主要供学习参考的教程文档 / 案例仓库。

For HTML pages, visually highlight the `[content shape]` part only. Example: in `这是一个主要供学习参考的教程文档 / 案例仓库。`, highlight `教程文档 / 案例仓库`; in `这是一个需要接入到前端 / Node 项目的 npm 库 / Mermaid 渲染工具。`, highlight `npm 库 / Mermaid 渲染工具`.

Common usage modes: 可以直接用、需要本地运行、需要接入到 Agent/平台、需要私有化部署、主要供学习参考。
Common content shapes: 素材库、Prompt 库、Skill、插件、MCP 工具、CLI 工具、Web 应用、模板、脚手架、自动化工作流、教程文档、awesome 清单、数据集、模型项目。

## Visual Style For Quick HTML

Keep the page light, clean, and readable, but not pale or overly plain. It should feel like a shareable tech magazine card with a soft tech palette, not a harsh high-contrast dashboard.

Color workflow:

1. Choose a main hue from the repo category; default to soft blue/blue-cyan when unsure.
2. Pick gradient colors from adjacent hues, not random colors.
3. Keep gradient hue shift around 20-45 degrees; never exceed 60 degrees.
4. Define all colors, alpha colors, gradients, shadows, radii, spacing, and type in `:root`.
5. Component CSS must use `var(...)`.
6. Avoid gendered purple/pink defaults for design/image repos unless the source brand clearly uses them.
7. Avoid high-contrast red/green blocks; use muted amber, blue, cyan, slate, or low-saturation status colors.

Theme map:

| Repo angle | Main tone | Gradient |
|---|---|---|
| AI coding / code graph / agent tooling | indigo or blue-violet | indigo → blue / violet-blue |
| AI design / image / creative product | soft blue or blue-cyan | blue → cyan / blue-gray |
| Video / media / AIGC | blue | blue → cyan |
| Data / analytics / repo intelligence | blue | blue → teal |
| Productivity / automation / office | teal-blue | teal-blue → cyan |
| Privacy / local-first / security | deep teal | teal → slate-blue |
| Business / finance / executive | muted amber | amber → soft gold |

Visual ingredients:

- Strong first-viewport visual anchor: full-page theme gradient, light gradient hero, tinted title band, soft KPI strip, or large official demo image.
- Rich but controlled surfaces: one tinted background, white cards, muted badges, layered shadows.
- Avoid all-pale blue-white layouts, but keep contrast gentle; prefer depth and hierarchy over loud colors. The outer page canvas/body should also carry the theme gradient, not just the central card.
- Avoid rainbow gradients, unrelated hue jumps, large red/green blocks, and purple-pink defaults unless the repo's own brand requires them.
- Do not put cards inside cards.

## Public Account Material Block

When preparing material for “AI 应用实战派 Pro” or WeChat writing, output:

```markdown
## 公众号素材：传播角度

### 1. 一句话值不值得看
普通人可理解，不要说“强大的开源项目”。

### 2. 读者为什么关心
痛点、转发对象、工作场景。

### 3. 最强开头素材
截图/Demo/Star 数/增长/对比/一句真实痛点。

### 4. 三个可写角度
- 角度：
- 标题：
- 主线：
- 需要补的实测证据：

### 5. 不能写太满
哪些是 README 声称，哪些需要本地实测。
```

## Title Formulas

Generate 5-10 candidates, not one. Mix formulas.

| Formula | Use when |
|---|---|
| `GitHub 狂揽 X Star！一句话描述项目` | Star count is strong |
| `X 天涨 Y Star，[赛道]又杀出一匹黑马` | Growth is the story |
| `开源版 [paid/closed product] 来了` | Free alternative |
| `[Claude/Cursor/Figma/Notion] 用户注意` | Known-product hook |
| `推荐 N 个 [小众但有趣/近期爆火] 项目` | Collection post |
| `不用 X，也能 Y` | Pain-removal hook |
| `不是 X，而是 Y` | Workflow/paradigm shift |

Title rules:

- WeChat: keep the strongest meaning in the first ~20 Chinese characters.
- Bilibili: title can be longer, but cover must show project name + big number/result.
- Douyin: title is secondary; first 3 seconds must show result.
- Avoid claims like “彻底替代”, “生产可用”, “稳定无敌” unless verified.

## Platform Adaptation

| Platform | Best structure | Key requirement |
|---|---|---|
| WeChat | 800-2000 words, screenshots, clear link | First paragraph must explain value fast |
| Bilibili | 5-15 min demo or weekly roundup | First 30 seconds show effect |
| Douyin | 15 sec-3 min result-first short | First 3 seconds hook; show outcome, not repo page |
| Zhihu/Juejin | Pain story + explanation + usage | More background and reasoning allowed |

## Quality Checklist

Before finalizing share content:

- Is the first sentence understandable to a non-programmer?
- Is there a clear “send this to X” recipient?
- Is there at least one visual proof or suggested screenshot?
- Is the setup friction stated honestly?
- Are README claims marked as claims unless tested?
- Is the title specific, not generic?
- Does the content say what the repo helps people do, not only what tech it uses?
- Are legal/ethical risks handled carefully?

## Common Mistakes

- Starting with technical architecture before explaining the user pain.
- Treating stars as enough reason to share.
- Making a full HTML report when the user asked for a shareable page.
- Over-reading README and losing speed.
- Ignoring setup friction.
- Saying “替代某产品” too strongly when it is only an open-source attempt.
- No screenshot/demo plan.
- No clear platform adaptation.
## Roundup Screenshot Card Rule

When several repos will be shared in one article, do not force every repo into the same long article template. Make short independent cards first.

Each card should pass the 10-second test:

- Can the reader see what the repo is?
- Can the reader see who should use it?
- Can the reader see why it is worth saving?
- Can the reader see the lowest-effort next step?

Avoid:

- internal screening criteria
- public-account writing notes
- author/account labels
- long technical installation details
- repeated identical card layouts

Use different visual styles for different repos when screenshots will be placed in the same article.
