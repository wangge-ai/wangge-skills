---
name: github-wechat-curation
description: Use when the user wants to discover, screen, dissect, or turn GitHub repositories into Chinese WeChat Official Account article material, including trending AI repos, fast-growing projects, repo URLs, owner/repo strings, GitHub weekly lists, project selection, title angles, screenshot planning, and publishable素材卡.
---

# GitHub WeChat Curation

把 GitHub 仓库从“开源项目”转成中文 AI 实战类公众号可用的素材。目标不是复述 README，而是建立这条链路：

`趋势发现/高潜力挖掘 -> 项目筛选 -> 仓库拆解 -> 公众号素材卡 -> 文章角度/标题/截图位/边界`

## Use This With

- 用户给 GitHub 仓库 URL 或 `owner/repo`。
- 用户问“今天/本周有哪些热门 AI GitHub 仓库”。
- 用户要判断某个仓库能不能写公众号。
- 用户要把仓库整理成素材卡、选题卡、标题方向、截图位。
- 用户要做 GitHub 工具合集、单项目实测文、趋势观察文。

## Core Rules

1. **先验事实**：Star、fork、license、release、更新时间、README、Demo、安装方式必须来自 GitHub/API/README/官方文档，不要脑补。
2. **先筛再写**：仓库分数低于 18/30，默认不建议写正式文章，只进观察池。
3. **痛点优先**：先回答“谁会遇到这个麻烦、这个仓库帮他少做哪一步、这个麻烦是不是足够常见”，再看 Star 和热度。
4. **不是 README 翻译**：必须回答“它帮谁省了哪一步”。
5. **截图是证据**：每个可写仓库都要给截图位，优先仓库首页、Demo、功能效果、安装命令、运行结果。
6. **实测边界**：没跑过就写“资料拆解 / README 声称 / Demo 显示”，不要写“我实测稳定可用”。
7. **账号匹配**：优先 AI 应用、Agent、Skill、MCP、内容生产、知识库、浏览器自动化、Codex / Claude / Gemini / GLM / Cursor 相关项目。
8. **合规优先**：爬虫、安全、账号检索、反检测类仓库只讲合法用途和风险，不提供违规操作路径。

## Workflow

### 1. Discover

如果用户问趋势或热门仓库，优先查：

- GitHub Trending
- OpenGithubs 月度飙升榜
- HelloGitHub / GitHubDaily / 逛逛GitHub
- Hacker News
- Product Hunt
- X/Twitter 开发者圈

输出候选仓库时，每个候选只给一句话、可信信号、为什么适合/不适合本号。

### 1.5 Mine High-Potential Repos

当用户问“挖高质量仓库 / 高潜力仓库 / 值得写的 GitHub 项目”时，先区分：

- **高质量**：README 完整、有 Demo/截图、有 Quick Start、最近维护、能现在用。
- **高潜力**：Star 可能还不高，但上 Trending、增长快、作者/品牌强、和 AI 热点强相关、有清晰传播点。

先按痛点分组，再看项目热度。常见痛点包括：

- 看不懂仓库：README 英文多、命令多、普通用户不知道怎么开始。
- 用 AI 编程太乱：上下文、成本、代码审查、任务拆分没人管。
- Agent 接工具太麻烦：MCP、浏览器、文件、数据库、自动化流程连接成本高。
- 本地知识/数据处理费劲：RAG、文档解析、向量库、隐私和本地运行。
- 内容和视觉产出慢：图片、视频、网页、PPT、卡片、短内容要反复改。
- 评测和监控缺失：模型效果、token 成本、工具调用、任务结果没法对比。

候选仓库如果说不清“解决哪个痛点”，即使 Star 高，也先放观察池。

常用命令：

```powershell
python <skills-root>/github-repo-dissector/scripts/github_repo_stats.py --trending --since daily --limit 20
```

```powershell
python <skills-root>/github-repo-dissector/scripts/github_repo_stats.py --trending --since weekly --language typescript --limit 20
```

```powershell
python <skills-root>/github-repo-dissector/scripts/github_repo_stats.py https://github.com/owner/repo --trend-days 7
```

候选输出先用轻格式：

```markdown
## 候选仓库：owner/repo
- 来源：
- 当前信号：
- 目标用户：
- 解决的痛点：
- 一句话：
- 为什么可能值得写：
- 截图/Demo：
- 风险：
- 初筛分：
- 处理建议：写 / 合集 / 观察 / 放弃
```

### 2. Quick Scan

对单仓库先收集：

- repo name / URL
- description
- stars / forks / issues
- language / license
- created / pushed / release
- README 核心描述
- Demo / docs / screenshots
- install / quick start

可以优先调用已有 `github-repo-dissector` 的快速扫描脚本：

```powershell
python <skills-root>/github-repo-dissector/scripts/github_repo_stats.py https://github.com/owner/repo --fast
```

### 3. Score

满分 30 分：

| 维度 | 分值 |
|---|---:|
| 痛点匹配 | 5 |
| 截图证据 | 5 |
| 热度信号 | 5 |
| 使用门槛 | 4 |
| 账号匹配 | 5 |
| 可实测性 | 3 |
| 边界清晰 | 3 |

判断：

- `<18`：观察池，不建议写。
- `18-23`：可做轻素材或合集一项。
- `24+`：适合正式文章或实测文。

### 4. Material Card

默认输出这个结构：

```markdown
# GitHub 公众号素材卡：owner/repo

## 1. 一句话
## 2. 基础数据
## 3. 为什么值得关注
## 4. 它解决什么问题
## 5. 小白怎么理解
## 6. 核心亮点
## 7. 使用门槛
## 8. 适合我们怎么写
## 9. 标题方向
## 10. 截图位
## 11. 风险和边界
## 12. 是否建议写
```

### 5. Article Angles

输出至少 3 类角度：

- 单项目实测 / 拆解文
- GitHub 合集文中的一项
- AI 工作流改造文

标题优先：

`实体词 + 具体任务 + 结果/判断`

少用“神级、杀疯了、火火火、YYDS、顶啊”。

## Output Style

- 写中文。
- 面向公众号素材，不面向纯开发者文档。
- 先给结论，再给证据。
- 不要长篇解释技术术语；首次出现时翻译成工作动作。
- 每个结论尽量带来源：GitHub metadata、README、Demo、release、docs。

## References

需要更详细规则时读取：

- `wechat-github_article_rules.md`：文章结构、选题评分、标题和截图规则。
- `wechat-high_potential_mining.md`：高质量 / 高潜力 GitHub 仓库挖掘方法。
- `wechat-material_card_template.md`：可复制素材卡模板。
## 2026-06-03 Weekly Repo Publishing Update

Use this section when the user asks for GitHub weekly lists, AI repo roundups, AI+ecommerce repo lists, or says an article has been published and the flow should be updated.

### Public Article Principle

Do not expose internal writing plans in the public article. Readers do not need to see:

- why we want to make a fixed GitHub column
- that this is a process test
- that we may later turn the flow into a skill
- our internal screening logic in long form

Translate the work into reader-facing value:

- what problem this repo solves
- who should look at it
- why it is worth saving
- how to try it with the lowest effort

### Weekly Flow

1. Search recent AI repos and AI+ecommerce repos.
2. Group by reader pain first, not by Star first.
3. Check published records before selecting. If a repo was already covered, skip it unless there is a clear new update.
4. Shortlist 5-7 candidates for the user to choose from.
5. After the user chooses, make short repo cards before writing the article.
6. For each repo, output a screenshot-friendly HTML card with a different palette/layout.
7. Assemble the article using concise repo sections and the card screenshots.
8. Generate a WeChat cover. If image generation creates unrelated objects or wrong text, switch to local HTML/CSS cover.
9. Update the publish record after the article goes out.

### AI+Ecommerce Priority

AI+ecommerce repos are fewer than general AI repos, so do not force a full list when quality is weak. Prefer 3 strong repos over 8 weak ones.

Useful categories:

- platform agent plugins, such as Shopify official plugin
- store operation skills, such as Shopify admin skills
- seller skills, such as Amazon keyword/listing/PPC workflows
- product image or product content workflows
- ecommerce context/protocol repos, such as CommerceTXT-like projects
- customer service, review analysis, ads, inventory, product research, listing optimization

### Repo Short Card Format

Each card should answer only:

```markdown
仓库：
一句话：
解决的问题：
适合谁：
先怎么试：
GitHub：
```

For visual HTML cards:

- one repo per HTML file
- different palette and composition per repo
- no author/account label
- no public-account writing process
- no "screening logic" block
- no internal skill/method explanation
- avoid wide tables that require dragging
- make the screenshot useful by itself

### Article Section Rule

For roundup articles, each repo section should be short:

1. repo name and short title
2. 2-3 paragraphs maximum
3. one card screenshot or repo screenshot
4. GitHub URL

If a repo needs long technical explanation, save it for a separate deep-dive article.
