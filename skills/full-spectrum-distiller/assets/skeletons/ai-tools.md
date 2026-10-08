# AI Tools / AIGC 骨架（AI 工具与生成式 AI）

>适用: AI工具、大模型应用、AIGC、AI Native、GenAI、LLM应用、Agent、RAG等技术导向领域。

---

name: ai-tools
category: AI / 深度科技
keywords: [AI, LLM, GPT, Claude, AIGC, 文生图, Copilot, Agent, RAG, 向量数据库, MCP, AI Coding, 大模型]
aliases: ["AI工具", "AIGC", "大模型应用", "AI Native", "GenAI"]

## 目录树调整

```
output/<slug>-OS/
├── Brands/                      # 强调: 技术壁垒/模型依赖/商业化阶段/开源vs闭源
│   └── {brand}.md               # 含 AI 特有字段: underlying_model, context_window, per-unit-pricing
├── Products/
│   ├── TREE.md                  # 按技术路线分 (LLM/Image/Audio/Video/Multimodal) + 按应用场景分
│   └── {category}.md
├── Pain-Points/                 # AI 特有: 幻觉/成本/延迟/隐私/合规/模型更新破坏性
├── Keywords/                    # 英文技术词主导 / GitHub star / HN讨论 / arXiv Paper
├── Competitors/                 # 技术文档/API质量/Developer DX/Pricing-per-token/Rate-limit 为核心
│   └── {brand}/analysis.md      # 含: model_card / benchmark_comparison / playground_quality
├── Content/                     # Twitter/X > GitHub > HN > YouTube Tech > arXiv > Papers
├── Knowledge-Cards/             # ⚠️ 必须做最深: 技术概念需4-5级深度
├── Opportunities/               # 强调: Infrastructure layer机会 / Vertical application / Edge AI
└── Sources/
```

## 特有字段

### 品牌（AI 核心）
| 字段 | 说明 |
|------|------|
| underlying_model | 底层模型 (GPT-4o / Claude 3.5 / Llama 3 / 自训练 / Mix) |
| context_window | 上下文窗口大小 (K tokens) |
| pricing_per_unit | 每单位价格 ($/1M tokens input-output / per image / per video min) |
| rate_limits | 速率限制 (RPM / TPM / daily caps) |
| api_quality_score | API 质量 (1-10: 文档完整性/错误信息/延迟/一致性) |
| open_source | 是/否 (license type if yes) |
| modality | text / image / audio / video / multimodal / code / agent |
| training_data_origin | 公开数据 / 自有数据 / 合成数据 / licensed / unknown |

### 痛点（AI 特有）
| 维度 | 痛点 |
|------|------|
| 准确性 | hallucination(幻觉) / factual errors(事实错误) / inconsistency(不一致性) |
| 成本 | cost at scale(规模化成本) / token waste(token浪费) / unexpected bills(意外账单) |
| 性能 | latency(p99延迟高) / throughput限制 / cold start |
| 隐私合规 | data privacy(数据隐私) / GDPR compliance / data used for training(数据被用于训练) |
| 模型风险 | model obsolescence(模型快速迭代导致过时) / vendor dependency(供应商依赖) / breaking changes(破坏性更新) |
| 采用门槛 | prompt engineering skill(提示工程技能) / integration complexity(集成复杂度) | evaluation difficulty(评估困难) |

### 竞品拆解加深
| 分析项 | 说明 |
|--------|------|
| model_card | 模型规格卡（参数量/训练数据/基准测试分数） |
| benchmark_comparison | 在标准基准上的表现对比（MMLU/HumanEval/MATH etc.） |
| playground_quality | Playground/体验环境的质量（易用性/示例丰富度/免费额度） |
| docs_quality | 技术文档质量（API参考/快速入门/SDK/example/错误码） |
| ecosystem | 生态系统（plugin数/integration数/community size/partner network） |
| research_output | 研究产出（论文发表频率/arXiv preprints/blog技术深度） |

## 搜索策略差异

| 需求 | 搜索关键词 |
|------|-----------|
| AI产品发现 | "best AI tools for {use_case} 2025 2026" / "{task} AI tool" |
| 技术评估 | "{model} benchmark comparison" / "{model} vs {model} benchmark" |
| 开发者视角 | GitHub stars {repo} / "{tool} API documentation" / "{tool} SDK" |
| 学术前沿 | arXiv {topic} / "{technique} paper 2025 2026" / HN discussion {topic} |
| 商业动态 | OpenAI/Anthropic/Google blog / YC AI companies / AI funding news |
| 价格对比 | "{tool} pricing vs {tool}" / "AI API cost comparison per 1M tokens" |

## 数据源优先级

| 数据类型 | 推荐源 |
|---------|-------|
| 模型基准 | **Artificial Analysis** (速度/价格/质量) / Hugging Face Leaderboards / LM Evaluation Harness |
| 论文研究 | **arXiv** (cs.CL/cs.AI/cs.LG) / Semantic Scholar / Google Scholar / Papers with Code |
| 开发者讨论 | **Hacker News** (Show HN / technical discussions) / r/LocalLLaMA / Discord communities |
| 产品发布 | **ProductHunt** (AI category) / BetaList / Hacker News Launches |
| 公司动向 | **官方Blog** (OpenAI/Anthropic/Google DeepMind/Meta AI) / The Information / TechCrunch |
| 创业公司 | **YC Directory** (AI batch companies) / AngelList / Crunchbase AI tags |
| 开源项目 | **GitHub** (trending/star history/release cadence) / Hugging Face Models |
