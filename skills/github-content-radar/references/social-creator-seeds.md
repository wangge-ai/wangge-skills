# Creator Seeds

Last updated: 2026-06-19

Public creators/accounts that repeatedly share GitHub repositories. Use these as search seeds before or alongside broad keyword discovery. Keep only public account names and public source hints.

This file is a living seed library. Every GitHub Social Radar run should update it when new useful public sources are found.

## Current Seeds

| 平台 | 作者/账号 | 线索类型 | 推荐搜索词 | 证据/备注 |
|---|---|---|---|---|
| 公众号 | 逛逛GitHub | 高频 GitHub / AI 开源项目推荐 | `逛逛GitHub GitHub`；`逛逛GitHub 开源项目`；`逛逛GitHub AI 开源`；`逛逛GitHub Claude Code`；`site:mp.weixin.qq.com 逛逛GitHub GitHub`；`Wechat-ggGitHub Awesome-GitHub-Repo` | 用户截图显示该账号近期持续发布 GitHub 开源项目推荐，含阅读/赞数据。公开检索还命中其整理仓库 `Wechat-ggGitHub/Awesome-GitHub-Repo` 及多篇转载样本，公众号原文仍需链接核验。 |
| B站 | IT咖啡馆 | GitHub 一周热点视频 | `IT咖啡馆 GitHub 一周热点`；`site:bilibili.com IT咖啡馆 GitHub`；`IT咖啡馆 AI 开源项目` | 本轮检索命中“GitHub 一周热点 115”。 |
| B站 | 宝藏挖掘机 / IT咖啡馆 | GitHub 一周热点视频，B站页面常显示“宝藏挖掘机，分享AI工具、IT知识、开源项目” | `宝藏挖掘机 GitHub 一周热点`；`site:bilibili.com 宝藏挖掘机 GitHub`；`Github一周热点115期 OpenHuman CodeGraph` | 2026-06-05 复扫命中 B站 2026-05-23「Github一周热点115期」，含 OpenHuman、CodeGraph、CloakBrowser、CLI-Anything、LingBot-Map。和 IT咖啡馆视作同一来源线索，避免重复统计。 |
| 抖音 | IT咖啡馆 | GitHub 一周热点短视频/专题页 | `IT咖啡馆 GitHub 一周热点 抖音`；`site:douyin.com IT咖啡馆 GitHub`；`IT咖啡馆 GitHub 一周热点 116` | 本轮检索命中“GitHub 一周热点 116”专题页摘要。 |
| 公众号/头条/知乎/GitHub | 开源推荐官 / OpenGithub | 每周 GitHub 飙升榜与开源项目排行 | `开源推荐官 GitHub 周榜`；`OpenGithubs github-weekly-rank`；`site:github.com/OpenGithubs github-weekly-rank`；`开源推荐官 Understand-Anything` | 公开仓库 `OpenGithubs/github-weekly-rank` 显示 2026-05-31 周榜，含项目、周增长、月增长和社区入口，适合我们做实际选型初筛。 |
| 抖音 | 每日AI评论 | Agent 工程与热门项目拆解 | `每日AI评论 GitHub`；`每日AI评论 Agent 项目`；`每日AI评论 Skills GitHub`；`site:jingxuan.douyin.com 每日AI评论 Github` | 抖音精选页显示最近 4-9 天连续发布 Agent 工程、PPT Master Agent、Skills、Trading Agent 等内容，适合找可实测项目。 |
| B站 | LLM张老师 | AI Agent / Claude Code / 开源项目实战教程 | `LLM张老师 GitHub`；`LLM张老师 Claude Code`；`LLM张老师 Shannon GitHub`；`site:bilibili.com LLM张老师 GitHub` | 检索命中 2026-02-17 Shannon 开源实践视频，发布时间偏旧；保留为工程教程型种子，不作为“最近热门”证据。 |

## Trend / Utility Sources

These are not social creators, but they are useful for our own daily discovery and validation.

| 类型 | 名称 | 用途 | 推荐搜索词 | 证据/备注 |
|---|---|---|---|---|
| 周榜源 | OpenGithubs/github-weekly-rank | 每周飙升榜，含周增长/月增长 | `OpenGithubs github-weekly-rank` | 2026-05-31 周榜可见，适合优先发现增长猛的仓库。 |
| 趋势源 | 极客日志 GitHub 精选 | 本周热门、每日精选、语言榜单 | `极客日志 GitHub 精选`；`zeeklog GitHub featured` | 页面显示 2026-05-25 本周热门和 2026-05-29 每日精选。 |
| 趋势源 | HubLens | GitHub + HN 每日排行，AI 中英摘要 | `HubLens GitHub 趋势`；`hublens AI 摘要 GitHub` | 页面显示实时 24h 涨幅、今日趋势、新项目、主题浏览，适合实际选型和发现新仓库。 |
| 趋势源 | GitTrend | GitHub 当日/本周/本月趋势，含 topic、今日增长和 repo 描述 | `GitTrend AI Agent`；`GitTrend Rising AI`；`gittrend codegraph headroom` | 2026-06-03 检索命中当日趋势榜，适合快速发现新冒头仓库，如 `headroom`、`codegraph`、`Understand-Anything`。 |
| 趋势源 | GitSoso | 中文 GitHub 热点页，按今日/本周/用途筛选 | `GitSoso GitHub 热点`；`gitsoso AI智能 GitHub`；`GitHub 热点 每日更新` | 2026-06-03 检索命中，页面声明数据来自 GitHub Trending 和 GitHub API；适合作为中文趋势辅助源。 |
| 趋势源 | TrendingRepo | 单仓库 momentum、Star History 和多渠道传播信号 | `TrendingRepo repo momentum`；`trendingrepo knowledge-work-plugins`；`TrendingRepo AI GitHub` | 2026-06-03 检索命中 `anthropics/knowledge-work-plugins` momentum 页面，可用于判断一个仓库是否在社媒/GitHub/HN 同时发酵。 |
| 趋势源 | Trendshift | GitHub live trending 替代源，按 Daily/Weekly/Monthly/Yearly 展示正在上升的仓库和 live mentions，适合补 GitHub 官方 Trending 的早期动量信号。 | `Trendshift GitHub trending AI`；`Trendshift live trending repositories`；`trendshift AI agent GitHub`；`trendshift weekly GitHub repositories` | 2026-06-19 检索命中，页面显示 Today(UTC) live trending repos，如 `Fullive-AI/Anima`、`yaojingang/yao-meta-skill`、`DietrichGebert/ponytail`，可作为趋势交叉验证源。 |
| 趋势/资讯源 | 程序员 AI 热点雷达 / itdog.org | AI 热点、Agent、AI 编程、本地模型和开源项目入口 | `itdog AI GitHub`；`程序员 AI 热点雷达 GitHub`；`itdog AI Agent GitHub` | 2026-06-03 检索命中，页面更新时间为 2026-05-26，适合补充“今天 AI 圈在关注什么”的上下文，但不能替代 GitHub 事实核验。 |
| 趋势源 | dimexplore GitHub 开源项目学习站 | OpenGithubs 周榜/月榜静态镜像与学习项目导航，适合快速查看历史周榜第一名和学习类仓库 | `dimexplore GitHub 开源项目排行榜`；`github.dimexplore.com AI`；`GitHub 开源项目学习站 周榜` | 2026-06-04 检索命中，页面显示最后同步 2026-06-01 08:30，并标注数据来自 OpenGithubs。可作快速入口，仓库事实仍回 GitHub/OpenGithubs 核验。 |

## Candidate Seeds

Promising sources that should be checked again before being promoted to Current Seeds.

| 平台/类型 | 作者/来源 | 为什么可能有用 | 推荐搜索词 | 状态/备注 |
|---|---|---|---|---|
| 待补充 | 待补充 | 新扫描发现但证据不足时先放这里 | 待补充 | 待核验 |
| 博客/镜像 | AI I024 / l024.net | 公开页面能访问到“逛逛GitHub”风格的 AI GitHub 推荐合集，含仓库地址、截图位和推荐理由 | `site:l024.net GitHub开源项目推荐 AI`；`AI I024 GitHub 开源项目推荐`；`l024 本周高关注AI与编程工具` | 2026-06-04 检索命中 2026-05-17 文章，适合作为社媒推荐理由参考；是否为稳定原创/镜像来源仍待核验。 |
| 文章/公众号风格公开源 | WeFound | 公开可访问 AI/工具/开源项目文章，能提供项目用途、风险边界和使用场景 | `WeFound GitHub AI 开源项目`；`site:wefound.cc Claude for Legal GitHub`；`wefound AI Agent 开源项目` | 2026-06-05 检索命中 2026-05-13 Claude for Legal 文章。可作公众号风格素材和来源补充，但不是微信原文，需标注清楚。 |
| 文章/公众号风格公开源 | 苏米客 | 公开可访问 AI开源项目文章，能补充“为什么值得关注”的普通人解释 | `苏米客 GitHub AI 开源项目`；`xmsumi knowledge-work-plugins`；`苏米客 Claude 插件 GitHub` | 2026-06-05 检索命中 knowledge-work-plugins 文章，页面显示“1周前”，但不是微信原文；适合作为中文文章源候选。 |

## 2026-06-05 Image Generation / GPT-Image-2 Seeds

| 平台/类型 | 作者/来源 | 为什么有用 | 推荐搜索语 | 状态/备注 |
|---|---|---|---|---|
| B站 | code秘密花园 / ConardLi | 2026-04-29 发布 GPT-Image2 完全指南，公开关联案例站和 `ConardLi/garden-skills`，适合追踪 Skill、Agent 出图、可复现提示词。 | `code秘密花园 GPT-Image2 Skill`；`ConardLi garden-skills gpt-image-2`；`site:bilibili.com ConardLi GPT-Image2` | 当前种子；本轮命中 B站视频与 GitHub 仓库。 |
| B站 | Xuan_酱 | 2026-04-25 发布 GPT Image 2 实用玩法总结，覆盖 PPT、广告、短剧等传播型案例，适合做玩法侧素材观察。 | `Xuan_酱 GPT Image 2 玩法`；`site:bilibili.com GPT Image 2 全网最实用的玩法`；`GPT Image 2 广告 PPT 短剧` | 候选种子；偏玩法热度，需回到可用仓库或提示词库补证据。 |
| B站 | 无用の阿杰 | 2026-05-20 发布 GPT-image2 提示词/插件/工作流内容，标题和摘要含电商、ComfyUI、提示词反推优化，适合补电商视觉工作流线索。 | `无用の阿杰 GPT-image2 电商`；`AJbeckliy Comfyui_SynVow_api GPT-image2`；`GPT-image2 提示词 优化 插件 电商` | 候选种子；本轮命中 `AJbeckliy/Comfyui_SynVow_api`。 |
| 博客/工具库 | 123AI | 连续整理 GPT Image 2、Codex、Skill、提示词模板和公众号封面/产品图案例，适合找文章结构和标题素材。 | `123AI GPT Image 2 Codex`；`site:123ai.org GPT Image 2 产品图`；`site:123ai.org Codex Skill 生图` | 工具/表达种子；用于选题表达，不替代官方/GitHub事实。 |
| 提示词库 | 上码 Upma | 提供 GPT Image 2 案例分类，含商品与电商、海报、UI、信息可视化，适合作为提示词和配图方向素材池。 | `Upma GPT Image 2 商品与电商`；`upma image prompts GPT Image 2`；`上码 GPT Image 2 提示词库 电商` | 工具种子；用于案例方向和素材分类。 |
| 博客/案例库 | KnightLi GPT-Image 2 提示词宝库 | 按电商主图等分类整理案例，保留原案例、作者、生成图和完整提示词，适合补电商主图提示词样本。 | `KnightLi GPT-Image 2 电商主图`；`awesome-gpt-image-2-prompts ecommerce cases`；`GPT-Image 2 提示词宝库 电商主图` | 工具种子；用于提示词样本，需注意案例来源授权与品牌词替换。 |

## Add/Update Rule

Add a creator when at least one of these is true:

- They repeatedly post GitHub repo roundups or list-style recommendations.
- They include concrete repo names, repo links, screenshots, demos, or install/usage notes.
- Their post titles clearly map to AI/GitHub discovery, such as `近一周火的 GitHub 仓库`, `本周开源项目`, `Star 暴涨`, `Claude Code Skill`, or `AI Agent 开源项目`.

For each new creator, record platform, public account name, why it is useful, and 3-6 search queries. Do not store cookies, private IDs, personal data, or non-public profile metadata.

## Living Update Protocol

On every radar run:

1. Read this file before searching.
2. Search both existing seeds and broad keywords.
3. When a useful public creator/source is found, update this file before final response.
4. Confirm visible publish/update dates. Do not treat an old page with a "近一周" title as recent.
5. Promote sources to `Current Seeds` only when they are public, repeatable, and useful for finding GitHub repos we may actually use.
6. Put uncertain but promising sources in `Candidate Seeds`.
7. Update existing rows instead of creating duplicates.
8. Record scan date/evidence date in the evidence note when possible.

## 2026-06-05 Seed Addendum

These public sources appeared useful during the strict 15-day GitHub radar scan. They should be checked again before promotion if exact original links or dates are incomplete.

| Platform / Type | Creator / Source | Why useful | Future search queries | Status / Evidence |
|---|---|---|---|---|
| Douyin | 每日AI评论 | Frequently explains AI agent, model, memory, and coding-agent projects with clear pain framing. | `每日AI评论 GitHub`; `每日AI评论 DeepSeek-Reasonix`; `site:jingxuan.douyin.com 每日AI评论 GitHub`; `每日AI评论 AI Agent 开源` | Candidate seed. 2026-06-05 scan found DeepSeek-Reasonix item published 2026-05-27. |
| Bilibili | 程序员晓刘 | Publishes hands-on GitHub/open-source tutorials; useful for low-cost trial angle and installation friction. | `程序员晓刘 GitHub`; `程序员晓刘 DeepSeek-Reasonix`; `site:bilibili.com 程序员晓刘 GitHub`; `程序员晓刘 Claude Code` | Candidate seed. 2026-06-05 scan found DeepSeek-Reasonix tutorial result dated 2026-05-28. |
| Bilibili | GitHub星探 | Daily/weekly GitHub rank-style videos; useful for fast trend spotting, but repo list must be verified. | `GitHub星探 GitHub 涨星榜`; `GitHub星探 GitHub 今日排行`; `site:bilibili.com GitHub星探`; `GitHub星探 AI 开源` | Candidate seed. 2026-06-05 scan found recent 05-30 and 06-01 rank results. |
| Bilibili | 游手好闲的满大人 | Daily GitHub ranking videos; useful as a lightweight source for "what changed today." | `游手好闲的满大人 GitHub 今日排行`; `site:bilibili.com 游手好闲的满大人 GitHub`; `6月1日 GitHub 今日排行` | Candidate seed. 2026-06-05 scan found recent GitHub daily ranking result. |
| Bilibili | 夜时雨_ | Appeared with "本周 GitHub 热门开源项目：AI 工作流工具精选"; may be useful for AI workflow repos. | `夜时雨_ GitHub 热门开源项目`; `site:bilibili.com 夜时雨_ GitHub`; `本周 GitHub 热门开源项目 AI 工作流工具精选` | Candidate seed. 2026-06-05 scan found recent result, repo list not yet extracted. |
| Bilibili | 小北AI开源 | AI/Linux/open-source focused account; useful for general AI open-source discovery, but not always GitHub list format. | `小北AI开源 GitHub`; `小北AI开源 AI 开源项目`; `site:bilibili.com 小北AI开源 GitHub` | Candidate seed. 2026-06-05 scan found account profile in AI open-source search results. |
| Trend source | Allhot GitHub boards | Aggregates GitHub day/week/month lists with timestamps; useful for repeated appearance and current trend cross-check. | `allhot GitHub 周榜`; `allhot GitHub 日榜 AI`; `全网热点 GitHub 周榜` | Utility source. 2026-06-05 page showed GitHub day/week/month boards updated within hours. |

## 2026-06-21 Utility Source Addendum

| Platform / Type | Creator / Source | Why useful | Future search queries | Status / Evidence |
|---|---|---|---|---|
| Trend source | OSSInsight Trending AI | Real-time AI GitHub trend page covering AI agents, LLM tools, MCP, RAG, coding agents, and related AI developer repositories. Useful as a cross-check alongside GitHub API and Trendshift. | `OSSInsight trending AI GitHub`; `ossinsight trending ai repositories`; `Trending AI Repositories on GitHub OSSInsight` | Utility source. 2026-06-21 scan found the public page and used it only as trend context; repo facts still verified via GitHub API. |

## 2026-06-21 Social Source Addendum

These sources were added after the user corrected the scan route from GitHub-first to social/web-first. Use them for Bilibili/Douyin/Chinese-article discovery before any GitHub trend-source scan.

| Platform / Type | Creator / Source | Why useful | Future search queries | Status / Evidence |
|---|---|---|---|---|
| Bilibili | 热带猫AI资讯 | Posts GitHub daily/weekly hot-project videos with concrete repo names, visible dates, and AI/Skill/Agent emphasis. Useful for finding non-ITCafe social signals. | `热带猫AI资讯 GitHub AI`; `site:bilibili.com 热带猫AI资讯 GitHub`; `GitHub今日7大爆款 AI工具狂飙`; `GitHub 周榜TOP7 AI Agent 工具链` | Candidate seed. 2026-06-21 scan found a 2026-06-08 Bilibili video listing last30days-skill, taste-skill, hermes-agent, open-notebook, AiToEarn, goose. |
| Douyin | 前端布洛芬的Agent实验室 | Publishes short AI/Skills GitHub trend items; useful for Skill-centric repo discovery, but item details may require browser/platform follow-up. | `前端布洛芬的Agent实验室 GitHub`; `每日AI Skills 热门项目速览`; `site:douyin.com 前端布洛芬 Agent GitHub`; `前端布洛芬 skills GitHub` | Candidate seed. 2026-06-21 scan found a 2026-06-06 Douyin result for "每日AI / Skills 热门项目速览". |
| Chinese article / mirror | GitCode / AtomGit AI open-source articles | Publicly accessible Chinese articles often mirror WeChat-style repo explainers and include dates, repo links, install notes, and pain framing. Useful when mp.weixin pages are not searchable or accessible. | `site:gitcode.csdn.net 2026 年 6 月 AI Agent GitHub`; `site:gitcode.csdn.net Odysseus 自托管AI工作空间`; `site:gitcode.csdn.net 开源 AI Agent 项目 GitHub` | Utility source. 2026-06-21 scan found 2026-06-09 Odysseus article and 2026-06-11 "7 open-source AI Agent projects" article. Treat as article evidence, not original WeChat proof. |

## 2026-08-05 AI Data Analysis Utility Source Addendum

| Platform / Type | Creator / Source | Why useful | Future search queries | Status / Evidence |
|---|---|---|---|---|
| Benchmark / leaderboard | UC Berkeley EPIC Data Lab — DataAgentBench | Provides realistic multi-database data-agent questions, executable validators, required execution traces, and a public Pass@1 leaderboard. Useful for replacing vague AI-data-analysis examples with measurable cases. | `DataAgentBench data agent benchmark`; `site:ucbepic.github.io/DataAgentBench query explorer`; `github ucbepic DataAgentBench`; `data agent benchmark execution traces` | Utility source. Verified 2026-08-05 from the official GitHub repository and benchmark site; 12 datasets, 54 queries, 9 domains, 4 DBMSes. |
| Research landscape | HKUSTDial — awesome-data-agents | Maintains a data-agent capability taxonomy and a current list of systems, papers, report-generation work, and benchmarks. Useful for systematic repository discovery rather than keyword-only search. | `HKUSTDial awesome-data-agents`; `data agents survey benchmark`; `LLM data agent report generation`; `data agent taxonomy GitHub` | Utility source. Verified 2026-08-05 from the official GitHub repository, which was updated the same day. |
