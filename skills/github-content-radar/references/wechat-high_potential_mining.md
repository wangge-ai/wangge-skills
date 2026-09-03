# 高质量 / 高潜力 GitHub 仓库挖掘

## 1. 高质量 vs 高潜力

高质量项目：现在就能用，README、Demo、Quick Start、维护、release、issue 处理都比较完整。

高潜力项目：还没完全成熟，但增长、作者、热点、场景、传播信号正在出现，适合提前观察或抢先写。

## 2. 信息源

每日：

- GitHub Trending daily
- GitHub Trending AI / Python / TypeScript
- Hacker News
- Product Hunt
- 竞品公众号

每周：

- GitHub Trending weekly
- OpenGithubs 月度飙升榜
- HelloGitHub
- GitHubDaily

关键词：

- Claude Code
- Codex
- Cursor
- Gemini CLI
- GLM
- DeepSeek
- Agent
- Skill
- MCP
- RAG
- memory
- knowledge graph
- code graph
- browser automation
- HTML artifact

## 3. 搜索语法

```text
ai agent stars:>100 pushed:>2026-05-01
"Claude Code" stars:>50 pushed:>2026-05-01
Codex stars:>50 pushed:>2026-05-01
MCP server stars:>100 pushed:>2026-05-01
knowledge graph codebase stars:>100 pushed:>2026-05-01
```

搜索只负责找候选，不代表能写。

## 4. 挖掘命令

Trending：

```powershell
python <skills-root>/github-repo-dissector/scripts/github_repo_stats.py --trending --since daily --limit 20
```

语言榜：

```powershell
python <skills-root>/github-repo-dissector/scripts/github_repo_stats.py --trending --since weekly --language typescript --limit 20
```

单仓库 7 日趋势：

```powershell
python <skills-root>/github-repo-dissector/scripts/github_repo_stats.py https://github.com/owner/repo --trend-days 7
```

## 5. 候选池字段

- 日期
- 来源
- repo
- 一句话用途
- 当前 Star
- 增长信号
- Demo / 截图
- 账号匹配
- 使用门槛
- 风险
- 初筛分
- 状态：写 / 合集 / 观察 / 放弃

## 6. 处理建议

- 高热度 + 高匹配 + 可实测：正式文章
- 高潜力 + 强 Demo + 竞品未写：优先观察或抢先写
- 大品牌 / 名人 / 官方仓库：趋势文
- 免费替代付费工具：合集或实测
- 纯开发者工具但能接 Codex / Claude Code：工作流文
## 7. AI+电商仓库挖掘补充

AI+电商仓库数量少，质量差异大，不能为了凑数量硬写。

优先搜索方向：

```text
shopify ai agent
shopify skills agent
amazon seller ai skills
ecommerce ai agent
commerce agent protocol
product content ai workflow
listing optimization ai
review analysis ai ecommerce
inventory ai agent
ads roi ai ecommerce
```

筛选时先问：

- 这个仓库解决的是店铺、卖家、商品、客服、广告、库存、内容里的哪一个问题？
- 小白能不能在 10 秒内理解它帮谁省了哪一步？
- 有没有 README、截图、Demo、示例命令或具体 Skills 清单？
- 它只是概念，还是已经能被 Agent 使用？

推荐输出数量：

- 3 个强仓库：可以写一篇精简周榜。
- 4-5 个中高质量仓库：适合完整周榜。
- 质量不够时，宁可混合通用 AI 仓库 + AI 电商仓库，不要硬凑 AI 电商。
