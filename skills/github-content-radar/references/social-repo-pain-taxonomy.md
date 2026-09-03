# Repo Pain Taxonomy

Last updated: 2026-06-03

Classify repositories by the real pain they solve. Do not classify only by language/framework. If a repo cannot map to a real pain, downgrade it to watchlist.

## Pain Categories

| 痛点分类 | 真实痛点 | 典型仓库形态 | 代表仓库 | 我们的判断重点 |
|---|---|---|---|---|
| Code Understanding | AI 或人看不懂复杂代码关系 | 代码知识图谱、代码地图、repo QA、调用关系索引 | `colbymchenry/codegraph`, `Lum1104/Understand-Anything` | 是否能减少我们读仓库/写报告/改代码的时间 |
| Agent Tool Interface | Agent 不会稳定操作软件或工具 | CLI 化、MCP、GUI Agent、浏览器/桌面自动化 | `HKUDS/CLI-Anything`, `Mininglamp-AI/Mano-P` | 是否能把原本手点/手配的工具变成 Agent 可调用动作 |
| Reusable Experience | 提示词、流程和经验不可复用 | Skill、Prompt 模板库、Agent 模板、任务包 | `academic-research-skills`, `financial-services`, `guizang-social-card-skill` | 是否能沉淀成我们自己的 Skill 或 SOP |
| Content Delivery | AI 只能输出文本，不能直接交付成品 | HTML-to-video、短视频生成、卡片/封面生成、PPT 自动化 | `heygen-com/hyperframes`, `MoneyPrinterTurbo` | 是否能进入公众号、短视频、报告、封面图工作流 |
| Model/API Operations | 多模型、API、成本、网关和观测混乱 | LLM gateway、API router、model ops、eval/monitor | `BerriAI/litellm` | 是否能降低我们多模型调用和密钥管理复杂度 |
| Learning Path | 学习路线太散，不知道从哪开始 | 教程仓库、路线图、awesome list、案例库 | `ai-engineering-from-scratch`, `awesome-architecture` | 是否能作为内部学习资料或训练新流程 |
| Ecommerce/Business Workflow | 行业业务流程难 AI 化 | 行业 Agent、业务模板、客服/电商/金融/运营自动化 | `anthropics/financial-services` | 是否能迁移到电商运营、客服、内容、数据分析流程 |
| Visual/Media Model | 图像、语音、视频、3D 等生成或理解能力提升 | 模型项目、TTS、3DGS、视觉编辑器 | `OpenBMB/VoxCPM`, `playcanvas/supersplat`, `lingbot-map` | 是否能低成本试用，是否需要 GPU/模型权重 |
| Security/Risk Boundary | 工具能力强但可能触及合规边界 | 自动化浏览器、安全工具、代理、反检测 | `CloakHQ/CloakBrowser` | 只做合法用途和风险观察，不做规避教程 |

## Classification Questions

For each repo, answer:

1. 谁会觉得这个问题很烦？
2. 它帮人少做哪一步？
3. 它是直接工具，还是模板/经验/模型/资料？
4. 我们能不能低成本试？
5. 它能进入哪个内部场景：Codex、GitHub 拆解、电商、内容生产、数据分析、培训、工具部署？

## Downgrade Rules

Downgrade to watchlist when:

- The pain is vague or only a technical slogan.
- There is no README/demo/quickstart.
- It is very hot but irrelevant to our workflows.
- It requires heavy GPU/cloud/API cost before any value is visible.
- It has compliance or misuse risk and the safe use case is unclear.
