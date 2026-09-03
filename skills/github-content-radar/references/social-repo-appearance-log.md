# Repo Appearance Log

Last updated: 2026-06-05

This is the cross-run dedup and repeated-appearance ledger for GitHub Social Radar.

Counts here are **lower-bound observations from our own scans**, not global social popularity. Use them to decide what deserves observation or trial, but never treat appearance frequency as proof that a repo is stable, safe, or production-ready.

## Counting Rules

- `Mentions`: source records or historical radar mentions we recorded.
- `Platforms`: distinct public surfaces, such as B站, 抖音, 公众号/文章源, GitHub trend source, HN/GitHub trend source.
- `Sources`: distinct creators/accounts/sources. The same creator cross-posting one episode to B站 and 抖音 counts as 2 platforms but usually 1 source.
- `Scan Dates`: dates when our radar saw the repo.
- `Signal`: new / repeated / cross-platform / multi-source / warming / watch / risk.

## Appearance Ledger

| Repo | First Seen | Last Seen | Mentions | Platforms | Sources | Scan Dates | Signal | Current Status | Notes |
|---|---|---|---:|---:|---:|---|---|---|---|
| `colbymchenry/codegraph` | 2026-06-03 | 2026-06-05 | 5+ | 4+ | 4+ | 2026-06-03, 2026-06-05 | cross-platform / multi-source / warming | Installed earlier, needs systematic review | B站/抖音 115, OpenGithub/GitTrend trend lane, our prior CodeGraph install experiment. Strong recurring signal for code understanding. |
| `tinyhumansai/openhuman` | 2026-06-03 | 2026-06-05 | 3+ | 3+ | 2+ | 2026-06-03, 2026-06-05 | cross-platform / repeated | Watch | B站/抖音 115 and earlier repo dissection interest. Needs privacy, local/managed service, and install-friction review before trial. |
| `HKUDS/CLI-Anything` | 2026-06-05 | 2026-06-05 | 2+ | 2 | 1 | 2026-06-05 | cross-platform | Queue | B站/抖音 115. Interesting because it turns software into Agent-callable CLI surfaces. |
| `CloakHQ/CloakBrowser` | 2026-06-05 | 2026-06-05 | 2+ | 2 | 1 | 2026-06-05 | cross-platform / risk | Risk watch | B站/抖音 115. Browser automation and anti-bot boundary require cautious, legal-only analysis. |
| `Robbyant/lingbot-map` | 2026-06-05 | 2026-06-05 | 2+ | 2 | 1 | 2026-06-05 | cross-platform | Watch | B站/抖音 115. Strong visual/media signal, but lower fit to our immediate Codex/ecommerce workflow. |
| `anthropics/financial-services` | 2026-06-03 | 2026-06-05 | 2+ | 2+ | 2+ | 2026-06-03, 2026-06-05 | repeated / business-workflow | Queue | 抖音 114 and prior radar queue. Useful for translating industry plugins into ecommerce/operations templates. |
| `anthropics/knowledge-work-plugins` | 2026-06-03 | 2026-06-05 | 3+ | 3+ | 3+ | 2026-06-03, 2026-06-05 | multi-source / repeated | Queue | Chinese article sources plus trend/GitHub evidence. Important for skill/plugin-as-business-process pattern. |
| `AIDC-AI/Pixelle-Video` | 2026-05-27 | 2026-06-05 | 2+ | 2+ | 2+ | 2026-05-27, 2026-06-05 | repeated | Quick-scanned earlier, watch | Prior repo test plus 抖音 113. Content delivery relevance; output quality and model cost need real test. |
| `EvoLinkAI/awesome-gpt-image-2-prompts` | 2026-05-25 | 2026-06-05 | 2+ | 2 | 1 | 2026-05-25, 2026-06-05 | cross-platform / repeated | Prior related analysis | B站/抖音 112. Prompt-library/content-asset direction already influenced our GitHub repo report work. |
| `playcanvas/supersplat` | 2026-06-05 | 2026-06-05 | 1+ | 1 | 1 | 2026-06-05 | new | Watch | 抖音 114. Useful for 3D/media trend observation, not immediate trial. |

## Update Template

```markdown
| `owner/repo` | YYYY-MM-DD | YYYY-MM-DD | N+ | P | S | dates | signal | status | evidence/notes |
```

## Use In Reports

For every radar output, classify each repo as:

- `新发现`: first recorded appearance.
- `重复出现`: seen before in this ledger.
- `跨平台重复出现`: 2+ platforms.
- `多账号重复出现`: 2+ distinct creators/accounts/sources.
- `持续出现`: 2+ scan dates.
- `已短拆/已试跑/观察池/风险`: status from trial outcomes and this ledger.

Repeated appearance should move a repo into observation or short-dissect consideration, but it should not override pain clarity, trial friction, or safety boundaries.

## 2026-06-05 Strict 15-Day Scan Addendum

Window: 2026-05-21 to 2026-06-05. Counts below are lower-bound observations from this scan only and should be merged into the ledger rows during later cleanup.

| Repo | 15-Day Evidence | Repeated Signal | Suggested Status | Notes |
|---|---|---|---|---|
| `colbymchenry/codegraph` | Bilibili/Douyin GitHub Weekly Hot 115 on 2026-05-23; OpenGithub 2026-05-31 weekly rank; Allhot 2026-06-05 GitHub week list | cross-platform / multi-source / sustained | Priority review | Repeated across social video, weekly growth ranking, and our own prior install experiment. |
| `Lum1104/Understand-Anything` | ITCafe GitHub Weekly Hot 116 candidate; OpenGithub 2026-05-31 weekly #1; Allhot 2026-06-05 GitHub week list | multi-source / warming | Queue | Strong knowledge-graph/code-visualization signal; compare with CodeGraph before recommending. |
| `tinyhumansai/openhuman` | Bilibili/Douyin GitHub Weekly Hot 115 on 2026-05-23; OpenGithub 2026-05-31 weekly rank | cross-platform / multi-source | Watch | Practical value depends on privacy, install path, and local/managed mode. |
| `CloakHQ/CloakBrowser` | Bilibili/Douyin GitHub Weekly Hot 115 on 2026-05-23; OpenGithub 2026-05-31 weekly rank; Allhot 2026-06-05 month list | cross-platform / trend-source repeat / risk | Risk watch | Browser stealth/anti-bot boundary: observe and explain risks; do not recommend misuse. |
| `HKUDS/CLI-Anything` | Bilibili/Douyin GitHub Weekly Hot 115 on 2026-05-23 | cross-platform same-source | Queue | Converts existing software into Agent-callable CLI surfaces. |
| `Robbyant/lingbot-map` | Bilibili/Douyin GitHub Weekly Hot 115 on 2026-05-23 | cross-platform same-source | Watch | Visual/media research signal, lower immediate fit to our Codex/ecommerce workflow. |
| `EverMind-AI/EverOS` | ITCafe GitHub Weekly Hot 116 candidate in Douyin/search snippets | new / date-pending | Watch | Agent memory OS direction; exact source date still needs original-link verification. |
| `esengine/DeepSeek-Reasonix` | ITCafe GitHub Weekly Hot 116 candidate; Douyin Daily AI Review on 2026-05-27; Bilibili Programer Xiaoliu on 2026-05-28 search result | cross-platform / multi-source | Queue | Repeated pain: lower-cost DeepSeek coding agent / terminal agent. |
| `heygen-com/hyperframes` | ITCafe GitHub Weekly Hot 116 candidate; prior radar queue | repeated / date-pending | Queue | HTML-to-video fits report/video delivery workflow; needs small sample test. |
| `Imbad0202/academic-research-skills` | ITCafe GitHub Weekly Hot 116 candidate; OpenGithub 2026-05-31 weekly rank; Allhot 2026-06-05 month list | multi-source / repeated | Watch/Queue | Skill package as reusable research workflow; not yet tested. |
| `hardikpandya/stop-slop` | Allhot 2026-06-05 GitHub week list; our prior deep report with taste-skill | sustained in our work / trend-source repeat | Already analyzed, observe | Useful as AI writing-quality guardrail; appearance is not proof of effectiveness. |
| `Leonxlnx/taste-skill` | Allhot 2026-06-05 GitHub week list; our prior deep report with stop-slop | sustained in our work / trend-source repeat | Already analyzed, observe | Skill-as-front-end-review workflow; needs real before/after task evidence. |
| `chopratejas/headroom` | Allhot 2026-06-05 GitHub day/week/month lists; prior radar queue | repeated / warming | Queue | Context compression/tool-output compression aligns with long Codex tasks. |
| `mvanhorn/last30days-skill` | Allhot 2026-06-05 GitHub day list; prior radar queue | repeated in our watchlist | Queue | Similar to our social radar idea; compare methodology before adopting. |
| `anthropics/financial-services` | Allhot 2026-06-05 GitHub month list; prior radar queue | repeated | Queue | Business-workflow plugin template; useful as reference, not a direct ecommerce tool. |

## 2026-06-21 Recent 15-Day AI Scan Addendum

Window: 2026-06-06 to 2026-06-21. Sources used: GitHub public Search API, Trendshift monthly trending page, OpenGithubs 2026-06-09~2026-06-14 weekly rank, OSSInsight Trending AI page. Counts remain lower-bound observations from this radar, not global popularity.

| Repo | 15-Day Evidence | Repeated Signal | Suggested Status | Notes |
|---|---|---|---|---|
| `DietrichGebert/ponytail` | Created 2026-06-12; GitHub API showed 43.5k stars on 2026-06-21; Trendshift monthly ranked it as new 2026 AI agent / AI coding assistant. | new / trend-source repeat | Queue | Coding-agent behavior guardrail; very high new-repo momentum. |
| `XiaomiMiMo/MiMo-Code` | Created 2026-06-10; GitHub API showed 10.1k stars; OpenGithub weekly rank listed it #15 for 2026-06-09~14. | new / multi-source | Queue | Agent/model co-evolution direction; worth short dissection. |
| `omnigent-ai/omnigent` | Created 2026-06-11; GitHub API showed 4.2k stars. | new | Queue | Meta-harness orchestrating Claude Code, Codex, Cursor and custom agents. |
| `BuilderIO/skills` | Created 2026-06-10; GitHub API showed 2.2k stars. | new | Queue | Coding-agent skills library; directly relevant to local Skills workflows. |
| `vercel/eve` | Created 2026-06-16; GitHub API showed 1.9k stars. | new | Watch/Queue | Framework for building agents; verify docs and trial friction before article use. |
| `JimLiu/baoyu-design` | Created 2026-06-07; GitHub API showed 1.7k stars. | new | Queue | Claude Design as local Agent Skill; relevant to article visuals and UI mockups. |
| `plannotator/effective-html` | Created 2026-06-09; GitHub API showed 1.1k stars. | new | Queue | Agent skill for HTML plans/diagrams; relevant to WeChat HTML/report workflow. |
| `amElnagdy/guard-skills` | Created 2026-06-06; GitHub API showed 852 stars. | new | Watch/Queue | Quality gates for AI-generated code/tests/docs; fits verification workflows. |
| `orange2ai/renwei-writing` | Created 2026-06-12; GitHub API showed 833 stars. | new | Queue | Human-taste writing skill; relevant to user's anti-AI-writing rules. |
| `duckbugio/flock` | Created 2026-06-08; GitHub API showed 749 stars. | new | Watch | Autonomous AI dev-team bot; needs safety and install-friction review. |
| `TestSprite/testsprite-cli` | Created 2026-06-11; GitHub API showed 634 stars. | new | Watch/Queue | AI-powered automated testing CLI; relevant if trial cost is low. |
| `chopratejas/headroom` | Existing repo, OpenGithub weekly #2 with 10,310 weekly star gain; Trendshift monthly also high. | repeated / trend-source repeat | Priority review | Token compression for tool outputs/RAG/logs; already in prior radar watchlist. |
| `addyosmani/agent-skills` | OpenGithub weekly #3 with 10,173 weekly star gain; Trendshift monthly high. | repeated / trend-source repeat | Priority review | Production-grade engineering skills for AI coding agents; strong fit. |
| `Panniantong/Agent-Reach` | OpenGithub weekly #8 with 5,077 weekly star gain; Trendshift monthly high. | repeated / trend-source repeat | Watch/Queue | Gives agents web/social search reach; verify compliance and API-free claims. |
| `Lum1104/Understand-Anything` | OpenGithub weekly #9 with 4,987 weekly star gain; GitHub API showed 64.7k stars. | repeated / trend-source repeat | Priority compare | Code/knowledge graph direction; compare against CodeGraph. |

## 2026-06-21 Social-First 15-Day Scan Addendum

Window: 2026-06-06 to 2026-06-21. Discovery route was corrected to social/web first: Bilibili, Douyin, WeChat-style public articles, Zhihu/CSDN/SMZDM mirrors. GitHub was used only for low-cost repo fact verification after social discovery. Counts remain lower-bound observations from this radar, not global popularity.

| Repo | Social Evidence | Repeated Signal | Suggested Status | Notes |
|---|---|---|---|---|
| `nexu-io/open-design` | ITCafe Douyin/Bilibili GitHub Weekly Hot 117, 2026-06-06/06-09; Chinese articles and Zhihu design-skill discussions. | cross-platform same-source / article repeat | Priority review | Open-source Claude Design alternative; strong fit for our WeChat HTML, cover, and visual workflow. |
| `chopratejas/headroom` | ITCafe GitHub Weekly Hot 117; Bilibili search result for 117; prior trend-source appearances. | cross-platform same-source / sustained in radar | Priority review | Compresses tool outputs/logs/RAG chunks before LLM context; directly useful for long Codex sessions. |
| `Leonxlnx/taste-skill` | ITCafe GitHub Weekly Hot 117; Bilibili 热带猫AI资讯 2026-06-08 daily hot-project video; prior radar/visual-writing use. | multi-source / sustained | Already analyzed, keep in queue | Useful for AI visual taste and anti-generic output guardrails; needs before/after evidence when sharing. |
| `rohitg00/ai-engineering-from-scratch` | ITCafe GitHub Weekly Hot 117; independent Chinese/English explainer search results around 2026-06-06. | cross-platform/article repeat | Watch/learning queue | Learning resource, not immediate workflow tool. |
| `pewdiepie-archdaemon/odysseus` | ITCafe GitHub Weekly Hot 118 on 2026-06-13; GitCode 2026-06-09 article; SMZDM/WeChat-style article 2026-06-17. | multi-source / article repeat | Priority review | Self-hosted AI workspace; useful for local/private AI-workbench angle, but install friction and security need real trial. |
| `santifer/career-ops` | ITCafe GitHub Weekly Hot 118 on 2026-06-13. | cross-platform same-source | Watch | AI job-search system built on Claude Code; useful pattern, lower fit to current ecommerce/content workflow. |
| `refactoringhq/tolaria` | ITCafe GitHub Weekly Hot 118; Bilibili/YouTube/Twitter-style social search hits; CSDN article around 2026-06-11. | social/article repeat | Watch | Markdown knowledge base desktop app; relevant if we build local knowledge-base workflow. |
| `addyosmani/agent-skills` | ITCafe GitHub Weekly Hot 119 on 2026-06-20/21; YouTube cross-post; prior trend-source repeat. | cross-platform same-source / trend-source repeat | Priority review | Production-grade engineering skills for AI coding agents; highly relevant to local Skills workflow. |
| `NVIDIA/cosmos` | ITCafe GitHub Weekly Hot 119. | cross-platform same-source | Watch | Physical AI/world-model platform; important but less immediately actionable for our Codex/content/ecommerce work. |
| `apple/container` | ITCafe GitHub Weekly Hot 119. | cross-platform same-source | Non-AI infra watch | Strong open-source signal, but not an AI repo; do not prioritize unless scanning general dev tooling. |
| `chatwoot/chatwoot` | ITCafe GitHub Weekly Hot 119. | cross-platform same-source | Ecommerce/customer-service watch | Not AI-first, but relevant to open-source客服/CRM workflows. |
| `iptv-org/iptv` | ITCafe GitHub Weekly Hot 119. | cross-platform same-source | Skip for AI radar | Popular repo but outside AI/tooling focus. |
| `mvanhorn/last30days-skill` | Bilibili 热带猫AI资讯 2026-06-08 "GitHub今日7大爆款"; prior radar queue. | multi-source / sustained | Queue | Skill that researches across Reddit/X/YouTube/HN/web; close to this radar's own methodology. |
| `hermes-agent` (unresolved owner/repo) | Bilibili 热带猫AI资讯 2026-06-08 "GitHub今日7大爆款". | social-only | Resolve later | Mentioned as "会成长的Agent"; repo owner not verified in this scan, so do not present as confirmed. |

## 2026-08-05 AI Data Analysis Repository Scan Addendum

Scope: GitHub public Search/REST API plus official README, documentation, benchmark and product pages. These are discovery observations, not installation or production-readiness claims.

| Repo | Evidence | Repeated Signal | Suggested Status | Notes |
|---|---|---|---|---|
| `ruc-datalab/DeepAnalyze` | GitHub API and README verified 2026-08-05; end-to-end data science pipeline, training data, demo, report output and evaluation path. | new / GitHub + official demo | Priority review | Strong reference for a flagship case because it shows input, executable workflow, rendered report, benchmark and contribution format. |
| `Canner/WrenAI` | GitHub API and README verified 2026-08-05; governed text-to-SQL, semantic/context layer, sample dataset and eval primitives. | new / GitHub + docs | Priority compare | Useful for business-metric grounding, dry-plan validation, structured errors and trusted chart/SQL outputs. |
| `microsoft/data-formulator` | GitHub API and README verified 2026-08-05; online demo, CSV/XLSX/database inputs, agent exploration, charts and editable reports. | new / GitHub + demo | Priority review | High fit for file-to-analysis-to-visual-report cases; MIT license recorded by GitHub API. |
| `ucbepic/DataAgentBench` | GitHub repository and official leaderboard verified 2026-08-05; 12 datasets, 54 queries, 9 domains, 4 DBMSes, validators and trace requirements. | new / GitHub + benchmark site | Priority benchmark | Best current evidence for making cases difficult, reproducible and objectively scored. |
| `HKUSTDial/awesome-data-agents` | GitHub API and README verified 2026-08-05; current taxonomy, research list and benchmark index. | new / GitHub + survey | Discovery utility | Use as the landscape map; it is not itself an executable case library. |
| `fafa-ai-data-lab/ai-data-analyst-agent` | GitHub API and README verified 2026-08-05; metrics-first methodology, independent validation, correction-to-rule and provenance footer templates. | new / GitHub only | Methodology compare | Small project but structurally close to the AI++ repository; useful for evidence design, not popularity proof. |
| `data-goblin/power-bi-agentic-development` | GitHub API and README verified 2026-08-05; Power BI/Fabric skills, agents, hooks, validation and report-building workflows. | new / GitHub + project site | Priority domain reference | Strong example of turning one analytics ecosystem into reusable skills and executable checks; GPL-3.0. |
