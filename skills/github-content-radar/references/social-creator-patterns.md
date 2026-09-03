# Creator Patterns

Last updated: 2026-06-03

This file records why creators or trend sources tend to recommend certain GitHub repositories. Use it to infer the selection logic behind recommendations, not just the repo list.

## Pattern Table

| 来源 | 来源类型 | 偏好的仓库形态 | 推荐逻辑 | 常见发现路径 | 对我们有什么用 | 边界 |
|---|---|---|---|---|---|---|
| 逛逛GitHub | 公众号 / 项目推荐 | 普通人能听懂、有标题钩子、有 Star/官方背书、有截图或案例的项目 | 把技术仓库翻译成“这个工具帮你少做哪一步” | GitHub 热榜、官方开源、读者转发、开源项目库、转载样本 | 适合发现中文圈正在关心的项目，尤其是可讲清楚痛点的仓库 | 原文不易公开检索时，需用户截图或链接补证据 |
| IT咖啡馆 | B站 / 抖音热点视频 | 一周热点、Agent、Claude Code、AI 工具链、能做标题列表的项目 | 把多个项目串成“本周值得看”的视频清单 | GitHub Trending、周榜、社媒热度、官方发布、项目 demo | 适合快速扫一批项目名，再交给我们做短拆/试跑 | 视频摘要不等于实测，需要回到 GitHub 核验 |
| 宝藏挖掘机 / IT咖啡馆 | B站视频账号别名 | GitHub 一周热点，偏“5 个项目一组”的开发者效率/AI Agent/可视化/工具链组合 | 用项目名 + 一句话功能 + GitHub 链接做快节奏推荐 | GitHub 周榜、Trending、开源发布、AI 工具热点 | 适合做中文社媒雷达的主力来源，尤其能发现 OpenHuman、CodeGraph、CLI-Anything 这种传播性强的项目 | 账号名和系列名可能在不同平台显示不同，需要按 URL 去重；视频推荐不是安装验证 |
| OpenGithub / 开源推荐官 | 周榜 / 数据源 | 周增长、月增长、开源时间和介绍清楚的仓库 | 用增长数据找正在起势的项目 | GitHub star 增长榜、周榜、月榜 | 适合发现“突然变热”的项目，优先做趋势初筛 | 增长高不等于能用，仍需看 README 和安装成本 |
| 每日AI评论 | 抖音工程拆解 | Agent 工程、Skills、行业 Agent、PPT/Trading/自动化类项目 | 关注能解释工程范式或工作流变化的项目 | 热门 AI 项目、Agent 工程案例、平台热点 | 适合理解“为什么这个项目值得试”，补充实战视角 | 有时只给概念和视频标题，需要再找 repo 原链 |
| 极客日志 GitHub 精选 | 趋势/精选页 | 小而具体、可点击、可安装、近期上榜的仓库 | 用每日精选/本周热门降低发现成本 | GitHub 精选页、语言榜单、主题榜 | 适合我们每天挑 1-2 个低成本短拆 | 不是作者实测，不代表稳定可用 |
| HubLens | 趋势/AI 摘要 | 24h 涨幅、新项目、HN/GitHub 同时热的仓库 | 用实时趋势 + AI 摘要缩短第一轮阅读 | GitHub Trending、HN、主题榜、AI 摘要 | 适合找今天可能值得装或观察的新仓库 | 趋势源没有完整上下文，需二次核验 |
| GitTrend | 趋势/增长页 | 当日、本周、本月趋势；带 topic、语言、star、今日增长 | 用“今日增长 + 项目描述 + topic”快速发现刚冒头的项目 | GitHub engagement、topic 聚合、Rising/Gems 页面 | 适合快速补充 OpenGithub 周榜之外的当天变化，尤其是 Agent 工具、代码知识图谱、上下文压缩类项目 | engagement 不是可用性证明，仍需回 GitHub README/API 核验 |
| GitSoso | 中文趋势页 | 中文可读的 GitHub 今日/本周热点和用途筛选 | 把 GitHub Trending/API 结果转成中文入口，便于快速扫榜 | GitHub Trending、GitHub API | 适合做中文雷达的辅助来源，快速找“今日最热/本周热门” | 页面可能动态加载，公开检索只能拿到部分信息 |
| TrendingRepo | 单仓库 momentum 页 | 单个仓库的传播势能、Star History、多渠道提及 | 用多渠道信号判断仓库是否只是 GitHub 内热，还是社媒也在传播 | GitHub、HN、Bluesky、Reddit、X 等聚合信号 | 适合验证某个仓库为什么突然火，给趋势判断补证据 | 不能把 momentum 当成真实试用效果 |
| 程序员 AI 热点雷达 / itdog.org | AI 热点/资讯入口 | Agent、AI 编程、本地模型、开源项目混合资讯 | 先用通俗热点判断今天 AI 圈关注的主题，再回 GitHub 找对应项目 | AI 资讯、官方发布、GitHub topic、工具入口 | 适合补“为什么这些仓库最近被提起”的背景，帮助我们选题和试用排序 | 更新时间可能滞后；不适合作为仓库 star/可用性事实来源 |
| WeFound | 文章/公众号风格公开源 | AI 工具、开源项目、行业插件/Agent 案例 | 把 GitHub 仓库翻译成具体行业工作流，并补边界说明 | 官方 GitHub、产品发布、项目 README | 适合补普通读者理解和风险边界，尤其是 legal/finance/knowledge-work 这类业务插件 | 不是微信原文；流量和社媒热度不能直接等同公众号传播 |
| 苏米客 | 文章/公众号风格公开源 | AI 开源项目、Claude/Anthropic 插件、业务工具 | 重点解释“这个项目为什么对职场/公司工作流有意义” | 官方 GitHub、项目 README、中文文章再加工 | 适合做公众号素材的二次理解参考，帮助把插件/Skill讲成岗位手册 | 需要回 GitHub 核验 star、fork、安装命令；文章日期有相对时间时要谨慎 |
| LLM张老师 | B站工程教程 | AI Agent、Claude Code、开源项目实战教程 | 通过教程讲项目使用和工程思路 | B站教程、开源实践、工具演示 | 适合作为学习源和补操作路径 | 发布时间可能偏旧，不作为近期热度证据 |

## Recommendation Logic Checklist

## 2026-06-05 Image Generation Pattern Notes

| 来源 | 来源类型 | 偏好的仓库形态 | 推荐逻辑 | 常见发现路径 | 对我们有什么用 | 限制 |
|---|---|---|---|---|---|---|
| code秘密花园 / ConardLi | B站教程 + GitHub Skill 集合 | Agent Skill、提示词案例站、可复现演示 | 用完整教程把 GPT-Image-2 玩法变成可安装/可复用 Skill | B站视频、GitHub 仓库、案例站 | 适合找 Codex/Agent 生图主线，尤其是“让 Agent 自动出图”的文章角度 | 视频热度不等于仓库适合普通读者，需要实测安装成本 |
| 123AI | 博客/公众号式素材源 | 提示词模板、Codex/Skill 实操、公众号封面/产品图案例 | 把模型能力拆成可复制模板和标题化场景 | 站内 GPT Image 2 / Codex 标签、搜索结果 | 适合补公众号标题、结构、读者痛点和提示词模板 | 需要回到官方文档/GitHub核验事实 |
| 上码 Upma / KnightLi 案例库 | 提示词/案例库 | 按电商、海报、UI、信息图分类的案例墙 | 用大量可视化案例降低选题和配图成本 | 搜索引擎、案例分类页、原案例链接 | 适合快速筛选“电商主图/商品广告/详情页”示例，辅助文章配图方向 | 案例可用性和版权/品牌词需要二次处理 |
| 无用の阿杰 / AJbeckliy | B站教程 + ComfyUI 节点仓库 | ComfyUI 工作流、插件节点、批量提示词生成 | 用节点化流程解决提示词反推、优化、详情页长图拼接 | B站视频、GitHub changelog、工作流下载 | 适合电商详情页、批量出图、长图拼接等深一点的实操选题 | 对小白门槛较高，可能更适合作为进阶素材 |

When analyzing a creator recommendation, answer:

1. 这个作者是在追热点、做实测、讲教程，还是搬运增长榜？
2. 这个仓库为什么适合这个作者的受众？
3. 标题钩子来自哪里：Star 暴涨、官方开源、替代付费工具、解决常见痛点、Demo 很直观，还是新范式？
4. 作者有没有给出真实使用理由，还是只列项目名？
5. 这个来源对我们实际试用有没有帮助？

## Update Rule

When a new creator/source is added to `creator-seeds.md`, add a row here if its recommendation pattern is clear. If the pattern is not yet clear, write it as a note in `Candidate Seeds` first.
