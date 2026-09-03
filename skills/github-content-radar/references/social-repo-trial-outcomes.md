# Repo Trial Outcomes

Last updated: 2026-06-05

This is our own feedback loop. It records what happened after a radar candidate was quick-dissected, installed, smoke-tested, adopted, rejected, or left in watchlist.

Do not write "usable", "stable", or "adopted" unless there was a real trial or explicit decision.

## Outcome Log

| Date | Repo | Source | Pain Category | Why Selected | Action | Result | Cost / Friction | Decision | Follow-up |
|---|---|---|---|---|---|---|---|---|---|
| 2026-06-03 | `op7418/guizang-social-card-skill` | 极客日志精选 | Content Delivery / Reusable Experience | 与 HTML 报告、封面、小红书卡片工作流高度相关 | 待短拆 | 未试 | 未确认 | Queue | 先做 quick HTML/README 拆解 |
| 2026-06-03 | `colbymchenry/codegraph` | IT咖啡馆 / GitTrend | Code Understanding | 已与 Codex 工作流相关，可能减少读仓库成本 | 已安装过，待系统化复盘 | 部分验证 | 需要 Codex 重启/索引目标仓库 | Queue | 复盘安装和实际查询收益 |
| 2026-06-03 | `Lum1104/Understand-Anything` | IT咖啡馆 / GitTrend | Code Understanding | 适合代码图谱可视化，对报告展示有价值 | 待对比 | 未试 | 未确认 | Queue | 与 CodeGraph 用同一仓库对比 |
| 2026-06-03 | `anthropics/financial-services` | OpenGithub / IT咖啡馆 | Reusable Experience / Business Workflow | 学习行业 Agent 模板拆法 | 待拆结构 | 未试 | 不需要跑完整金融场景 | Queue | 看插件、Skill、数据连接结构 |
| 2026-06-03 | `heygen-com/hyperframes` | IT咖啡馆 | Content Delivery | HTML 到视频，和报告/短视频交付有关 | 待试跑 | 未试 | 未确认 | Queue | 做 10 秒样片验证成本 |
| 2026-06-03 | `BerriAI/litellm` | HubLens | Model/API Operations | 多模型 API 网关可能对后续部署有用 | 待调研 | 未试 | 可能涉及服务部署和密钥管理 | Watch | 先看最小部署方式 |
| 2026-06-03 | `harry0703/MoneyPrinterTurbo` | OpenGithub | Content Delivery | 短视频生成，和内容自动化有关 | 待观察 | 未试 | 模型/素材/版权成本未知 | Watch | 先看安装成本和输出质量 |
| 2026-06-03 | `chopratejas/headroom` | GitTrend | Model/API Operations / Code Understanding | Agent 上下文压缩、工具输出压缩，可能减少长任务 token 成本 | 待短拆 | 未试 | 需要确认 MCP/代理接入方式与真实压缩质量 | Queue | 先做 quick HTML，再用一个长日志/README 做小样本测试 |
| 2026-06-03 | `anthropics/knowledge-work-plugins` | 逛逛GitHub/TrendingRepo/GitHub | Reusable Experience / Business Workflow | 官方知识工作插件库，适合研究“岗位经验如何封装成 plugin/skill” | 待结构拆解 | 未试 | Claude Cowork/Claude Code 插件生态要求需确认 | Queue | 优先看 data、marketing、customer-support、operations 插件结构 |
| 2026-06-03 | `mvanhorn/last30days-skill` | GeekWatcher/GitTrend | Reusable Experience / Research Workflow | 跨 Reddit、X、YouTube、HN、Polymarket 的近 30 天主题研究 skill，和我们的社媒雷达需求接近 | 待短拆 | 未试 | 数据源权限、登录、速率限制和引用可靠性未确认 | Queue | 对比我们自己的 github-social-radar，吸收可复用结构 |
| 2026-06-03 | `D4Vinci/Scrapling` | OpenGithub | Data Collection / Web Scraping | 自适应网页采集框架，和 Crawl4AI/电商采集场景可对比 | 待观察 | 未试 | 爬虫合规、风控、登录态和 JS 渲染成本需谨慎 | Watch | 后续可用公开页面做安全小样本对比 |
| 2026-06-03 | `hugohe3/ppt-master` | OpenGithub | Content Delivery | 文档转可编辑 PPTX，和报告/公众号素材转演示稿有关 | 待观察 | 未试 | 输出质量、模板兼容性和模型成本未确认 | Watch | 有演示需求时再做最小样本 |
| 2026-06-05 | `buluslan/gpt-image2-ecommerce` | Codex 生图素材池 | Ecommerce Image Workflow | 25 个电商场景模板，和主图、场景图、A+、社媒图高度相关 | 浅克隆 + README/SKILL/模板试读 + 截图 | 确认有 25 个 JSON 模板、Codex CLI 调用脚本和 Skill 工作流；未直接运行其脚本 | 需要 Codex CLI 登录；参考图一致性仍需真实产品图验证 | Quick Scanned | 下一步可用真实产品图跑主图、生活场景、A+ 三类小样本 |
| 2026-06-05 | `liangdabiao/ecom-details-image` | Codex 生图素材池 | Ecommerce Detail Page Workflow | 自带 PDP 详情页结构、样例图、prompt 文件，适合讲“整套详情页” | 浅克隆 + README/样例目录/详情页结构试读 + 截图 | 确认 README 写明 Prompt/Generate 双模式，并有 H1-H5、D1-D9 详情页结构和生成样例 | 出图依赖 OpenAI 兼容图片 API；默认示例模型需后续确认 | Quick Scanned | 先用 Prompt 模式拆一个产品详情页结构，再决定是否接 API 出图 |
| 2026-06-05 | `freestylefly/awesome-gpt-image-2` | Codex 生图素材池 | Prompt-as-Code / Image Style Library | 大型案例库 + Agent Skill，适合解决风格复用和提示词结构化 | 浅克隆 + README/Skill/docs/templates 试读 + 截图 | 确认包含 500 左右案例、商品与电商分类、工业模板、可安装 Skill | 仓库内容多，文章中不宜全讲；应只截取电商/风格库主线 | Quick Scanned | 后续筛 5-8 个电商相关案例做提示词参考表 |
| 2026-06-05 | `wuyoscar/GPT-Image2-Skill` | Codex 生图素材池 | Agentic Skill / CLI | 可作为 Codex 安装 Skill 的样板，补充非电商专用的 GPT Image 2 Skill 入口 | 浅克隆 + README.zh/SKILL 试读 | 确认支持 Codex 安装路径、CLI 和参考图库；更偏通用生图 | 需要 Python/uv/OPENAI_API_KEY，且不是电商专用 | Watch | 首篇文章可作为备选一笔带过，后续单独写 Skill 安装更合适 |

| 2026-06-06 | `wzj177/ecommerce-image-suite` | 国内电商 GitHub 初筛 | Ecommerce Image Workflow | 明确面向淘宝、京东、拼多多、抖音等国内平台，覆盖商品图分析、卖点提炼和套图生成 | README/metadata quick scan + HTML short report | 确认 README 写明 Python 脚本、SKILL.md、references、example 样例，以及白底主图、卖点图、材质图、场景图、详情图等输出类型；未本地跑模型 | 需要图像模型 API Key；真实出图质量、商品一致性和成本未验证 | Quick Scanned | 下一步用 1 个真实商品图跑白底主图、卖点图、场景图小样本 |
| 2026-06-06 | `Kumagt/price-monitor` | 国内电商 GitHub 初筛 | Ecommerce Monitoring / Price Tracking | 支持淘宝、京东、拼多多、抖音、快手等平台，贴近运营竞品价格监控痛点 | README/metadata quick scan + HTML short report | 确认 README 写明 v2.4.0、Web UI、REST API、价格历史、导入导出和多数据源 fallback；未接入真实数据源试跑 | 买手 API 邀请码与平台数据源需要验证；价格监控涉及频率、风控和合规边界 | Quick Scanned | 下一步用 3-5 个公开商品链接做低频监控实验 |
| 2026-06-06 | `xixihhhh/daihuo-jianshou` | 国内电商 GitHub 初筛 | Ecommerce Video Workflow | 面向抖音、快手、小红书带货短视频，适合内容电商出片流程验证 | README/metadata quick scan + HTML short report | 确认 README 写明 Next.js/React/TypeScript/SQLite/FFmpeg 架构、脚本生成、素材生成、视频合成和导出流程；未安装依赖或生成视频 | 需要多模型 API Key 和 LLM；视频质量、成本、导出稳定性需真实样本验证 | Quick Scanned | 下一步用 1 个商品生成 15-30 秒短视频，记录成本和出片质量 |

## Status Vocabulary

- `Queue`: 已进入近期行动队列。
- `Quick Scanned`: 已快速阅读 README/metadata，但未安装。
- `HTML Reported`: 已做短 HTML 报告。
- `Installed`: 已安装但未完整使用。
- `Smoke Tested`: 已跑最小示例。
- `Adopted`: 已进入我们的实际工作流。
- `Rejected`: 已明确不适合。
- `Watch`: 保留观察。

## Update Template

```markdown
| YYYY-MM-DD | `owner/repo` | source | pain category | why selected | action | result | cost/friction | decision | follow-up |
```

## Rules

- Update this file when a radar candidate is actually tried, rejected, or adopted.
- Keep facts separate from impressions.
- If a trial failed, record the blocker instead of hiding it.
- If a repo changes our future mining logic, mention it in follow-up and update `repo-mining-playbook.md` if needed.
