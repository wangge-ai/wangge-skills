---
name: aihot-topic-planner
description: Use when finding AI热点 from AIHot, NewsNow, 今日热榜, SoPilot, or similar feeds; screening topics for 目标公众号; planning公众号/小红书选题; or creating a立项 brief before any article is written.
---

# AIHot Topic Planner

Use this skill to turn daily AI/hotspot feeds into a shortlist of publishable topics. Stop at topic selection and project approval. Do **not** write the article, Xiaohongshu note, HTML page, cover, or full draft unless the user confirms a topic in a later step.

## Boundaries

- This skill handles: hotspot collection, screening, topic framing, platform fit, evidence needs, and立项 brief.
- This skill does not handle: writing正文, generating HTML, making images, rewriting for Xiaohongshu, or polishing article prose.
- If the user asks to write after selection, hand off to the relevant writing skill/workflow only after explicit confirmation.

## Source Rules

1. Browse live sources every time; 热点 are time-sensitive.
2. Record title, source URL, summary/recommendation, time/date, platform, and category tags when visible.
3. Open primary links when a topic may be selected, especially official docs, research papers, product pages, GitHub repos, X posts, or original articles.
4. Treat hotspot sites as discovery layers, not the only evidence.
5. Do not invent screenshots, usage results, user feedback, or personal experience. Mark missing evidence as `待补实测` or `待补截图`.

## Preferred AIHot Data Path

When the local `aihot` skill is installed, use it as the first data layer for AIHot because it calls the public REST API directly and is fresher/stabler than scraping the webpage.

Default combined workflow:

`aihot skill 拉精选热点 -> aihot-topic-planner 做选题筛选 -> WeChat Recommendation-Facing Check 判断标题/封面/证据 -> 用户确认 -> 再进入写作`

Division of labor:

- `aihot`: fetch current AIHot data, including selected items, daily reports, categories, keyword searches, and source URLs.
- `aihot-topic-planner`: judge whether an item is worth writing for 目标公众号.
- `wechat-article-dissector`: once a topic is confirmed, shape the article, title, structure, and WeChat presentation rules.

Use `aihot` first when the user asks:

- 今天 AI 热点
- AI 圈有什么
- AI 日报
- 最近 OpenAI / Anthropic / Google 发了什么
- 最近模型发布 / 产品发布 / 技巧观点 / 论文

Fallback:

- If `aihot` is not installed or fails, browse `https://aihot.virxact.com/` directly.
- If AIHot lacks enough context, cross-check NewsNow, 今日热榜, SoPilot, and original/official sources.
- If a selected topic is high-stakes, legal, medical, financial, or reputational, verify with original sources before recommending it.

## Source Stack

Use these sources according to the question. Prefer all four for a daily scan:

- **NewsNow**: 大盘入口. Use it to see what the broader internet is discussing and whether a topic has public emotion or social spread.
- **今日热榜/TopHub**: 趋势入口. Use tech/AI/product categories to see what industry, product, creator, and developer circles are repeatedly discussing.
- **AIHot**: AI 垂直入口. Use it for AI tools, model updates, agents, workflows, papers, GitHub repos, and AI creator angles.
- **SoPilot**: 表达入口. Use it to inspect X/Twitter传播结构: hook, emotional trigger, retweetable phrasing, creator angle, and whether a topic is easy to repackage.

Daily source order:

`NewsNow 看大盘 -> 今日热榜看趋势 -> AIHot 看垂直机会 -> SoPilot 看传播表达 -> primary source verification`

Cross-source signal:

- **Strong**: appears in 2+ sources or has one source plus strong official/original evidence.
- **Trend**: repeated across days, categories, or related items.
- **Expression-only**: hot on SoPilot/X but weak evidence; use as angle inspiration, not fact base.
- **Noise**: hot but unrelated to the account, impossible to verify, or only useful as gossip.

## Screening Criteria

Score each candidate from 1-5:

- **痛点强度**: does this solve an actual creator/e-commerce/AI workflow pain?
- **账号贴合**: can it connect to one-line e-commerce/content/AI implementation experience?
- **个人角度**: can the user add real workflow, comparison, or lessons instead of搬运新闻?
- **证据可得**: screenshots, docs, demo, repo, prompt, benchmark, or user-testable tool.
- **时效性**: is it new enough to ride, but not so raw that facts are thin?
- **双平台潜力**: can it become both a WeChat long-form and a Xiaohongshu carousel?
- **风险可控**: legal/compliance/accuracy risk low enough, or clearly caveated.
- **传播表达**: can the topic be framed with a clear hook, conflict, before/after, checklist, or practical scene?

## WeChat Recommendation-Facing Check

Use this check after normal hotspot screening. The user's feed will be personalized, but repeated WeChat 看一看 screenshots show common visible signals that are useful for公众号选题 and标题.

Do not select a topic just because it matches the user's interests. Prefer topics that also have:

- **实体清晰**: a concrete tool/model/company/platform/method readers recognize or can search, such as Codex, Claude Code, GPT-Image-2, Seedance, Gemini, NotebookLM, API中转站, Skill, MCP.
- **任务明确**: the topic maps to a real action, not only an announcement: install, compare, generate, automate, rewrite, visualize, publish, analyze, scrape, build, verify.
- **痛点直接**: the topic touches a practical friction: 限额、排队、不会装、成本高、图像不好看、工作流太乱、工具太多、不知道选哪个、怕踩坑.
- **证据可见**: it can produce screenshots, UI, before/after, output files, charts, workflow diagrams, tables, or demo results.
- **结果可交付**: it can end with a checklist, prompt, workflow, decision table, SOP, HTML preview, image set, or resource pack.
- **标题可压缩**: it can be expressed as `实体词 + 真实痛点/任务 + 结果承诺/判断`.
- **边界可说明**: it has clear limitations, risks, cost, access issues, or适用/不适用人群.

Fast rejection rule:

If a topic has only heat and no task, no evidence, no deliverable, or it would force fake personal experience, keep it in观察池.

Recommended title tests:

- `我用 X 做 Y，发现最难的不是 Z`
- `X 又出现了一个问题，我把工作流改成这样`
- `别急着用/装 X，先搞清这几类场景`
- `X 到底适合谁？我按真实工作流试了一遍`
- `普通人第一次用 X，先跑通这一件小事`

Reject topics when:

- It only has hype, no usable angle.
- It needs expertise the user cannot credibly claim.
- It is pure benchmark/ranking with no application path.
- It requires paid/private access and no public evidence.
- It would force fake personal experience.

## Topic Models

Use one of these models for each promising topic:

- **热点立意型**: event -> workplace/user pain -> broader judgment -> small practical conclusion.
- **工具实测型**: tool/update -> install/use path -> real use case -> limits -> who should try.
- **方法交付型**: recurring pain -> reusable framework/prompt/checklist -> example -> limits.
- **工作流升级型**: old way -> friction -> new format/process -> decision rule -> template.
- **合规避坑型**: policy/safety news -> who is affected -> what changes in daily work -> checklist.
- **资源整理型**: repo/prompt/list -> why useful -> scenarios -> how to use -> caveats.

## Output Format

When presenting a scan, use this shape:

```markdown
## AIHot 选题扫描

### 今日更值得看的方向
1. ...

### 来源交叉信号
- NewsNow 大盘：
- 今日热榜趋势：
- AIHot 垂直：
- SoPilot 表达：
- 交叉判断：

### 候选选题卡
#### 选题 A：...
- 来源：...
- 交叉信号：大盘 / 趋势 / 垂直 / 表达
- 类型：...
- 痛点：...
- 适合公众号吗：...
- 适合小红书吗：...
- 需要补的证据：...
- 风险/不写的原因：...
- 立项建议：强推 / 可写 / 观察 / 不建议

### 推荐立项
- 首选：...
- 为什么是它：...
- 先不写什么：...
- 你确认前我不会写正文。
```

For an approved topic, create a brief only:

```markdown
## 立项 Brief
- 暂定标题：
- 一句话立意：
- 用户痛点：
- 目标读者：
- 文章模型：
- 公众号结构草图：
- 小红书图文方向：
- 必须补的素材/截图：
- 事实风险：
- 下一步：等待用户确认是否进入写作。
```

## Quality Checks

Before finishing:

- Did you provide source links?
- Did you separate AIHot summary from your inference?
- Did you avoid writing正文?
- Did you include at least one `不建议写` or `观察` item when the scan has weak topics?
- Did you ask the user to confirm the selected topic before writing?
