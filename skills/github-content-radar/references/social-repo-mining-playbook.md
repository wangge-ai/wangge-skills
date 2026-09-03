# Repo Mining Playbook

Last updated: 2026-06-03

This playbook explains how to find eye-catching GitHub repositories: not just popular repos, but repos that reveal a useful new workflow or solve a painful task.

## Discovery Lanes

| 路径 | 看什么 | 适合发现什么 | 注意 |
|---|---|---|---|
| Growth lists | 周增长、月增长、24h 涨幅、Trending | 突然变热的新项目 | 增长不是可用性证明 |
| Creator seeds | 逛逛GitHub、IT咖啡馆、每日AI评论等 | 中文圈正在转发、讲解、拆解的项目 | 要核真实发布时间 |
| Official releases | Anthropic、DeepSeek、OpenBMB、HeyGen、Google、Microsoft 等 | 官方背书、范式变化、行业模板 | 官方发布不等于低门槛 |
| Demo-heavy repos | README 首屏截图、在线 demo、视频、before/after | 适合快速理解和试用的工具 | Demo 可能只展示最佳效果 |
| Keyword sweeps | Agent、Skill、MCP、Claude Code、Codex、workflow、RAG、local-first | 新工作流和新接口层 | 关键词容易噪音高 |
| Our own pain list | HTML 报告、封面、爬虫、代码理解、飞书、电商图文 | 真正能嵌入我们工作的项目 | 不要被无关热点带跑 |

## Eye-Opening Formula

Score each repo 0-25:

| Dimension | Max | Question |
|---|---:|---|
| Pain clarity | 5 | 一句话能否说清它解决什么麻烦？ |
| New workflow | 5 | 它是不是把旧工作换成新流程？ |
| Visible proof | 5 | README 是否有截图、Demo、视频、输出样例？ |
| Trial cost | 5 | 我们能否低成本试一下？ |
| Workflow fit | 5 | 是否能进入 Codex、电商、内容、数据、培训或部署流程？ |

Interpretation:

- `20-25`: 立刻短拆或试跑。
- `15-19`: 进入观察或合集候选。
- `10-14`: 只有特定场景再看。
- `<10`: 暂时跳过。

## Mining Workflow

1. Start with sources, not random search:
   - `creator-seeds.md`
   - OpenGithub weekly rank
   - HubLens
   - 极客日志精选
   - GitHub Trending / Star History when needed
2. Extract repo names and source reasons.
3. Verify real date:
   - Do not trust a "近一周" title if the page was published months ago.
   - Mark `日期待确认` if no date is visible.
4. Map each repo to `repo-pain-taxonomy.md`.
5. Score Eye-Opening Index.
6. Put only 3-7 repos into today's action queue.
7. Send chosen repos to `github-repo-dissector`.
8. After trial, update `repo-trial-outcomes.md`.

## Signals That A Repo May Be Worth Trying

- It compresses a task we already do manually.
- It has a first-screen demo or screenshot.
- It has a clear quickstart.
- It integrates with tools we use: Codex, Claude Code, browser, Python, Node, Docker, GitHub, Feishu, ecommerce assets.
- It is not just a library; it creates an output we can inspect.
- It represents a category shift: prompt -> skill, chat -> workflow, code search -> code graph, HTML -> video, software UI -> Agent interface.

## Red Flags

- Title is hot but publish date is old.
- Star count is high but README has no quickstart.
- Project requires heavy infra before any value is visible.
- It solves a problem we do not have.
- It is mostly hype around a model without usable scripts/demo.
- It touches anti-bot, scraping, security, credentials, or bypass behavior without a clear lawful use case.

## Daily Output Shape

Prefer this over long lists:

```markdown
## 今日值得看

1. 立刻短拆：
2. 值得安装：
3. 先观察：
4. 放弃/风险：

## 为什么是它们

- 来源：
- 痛点：
- 眼前一亮点：
- 最小试用动作：
```
