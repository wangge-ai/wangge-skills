# SaaS B2B 骨架（企业服务软件）

> 适用: SaaS软件、B2B企业服务、云软件、开发工具、协作工具、低代码平台等。

---

name: saas-b2b
category: B2B 软件 / SaaS
keywords: [SaaS, ERP, CRM, HRIS, 项目管理, 协作工具, 低代码, API, PLG, 企业软件, ToB]
aliases: ["SaaS", "企业软件", "B2B SaaS", "Cloud Software", "ToB软件"]

## 目录树调整

```
output/<slug>-OS/
├── Brands/                      # 强调: ARR/增长率/融资阶段/目标客户规模/部署模式
│   └── {brand}.md               # 含 SaaS 特有字段
├── Products/
│   ├── TREE.md                  # 按功能模块分 / 按部署模式分 (SaaS-PaaS-IaaS)
│   └── {category}.md
├── Pain-Points/                 # 强调: 采购决策链长/集成难/安全合规/ROI证明
├── Keywords/                    # G2/Gartner/Capterra评测词 + IT决策者搜索词
├── Competitors/                 # 定价页分析为核心 + G2对比 + 文案策略
│   └── {brand}/analysis.md      # 含: pricing_page / free_trial / enterprise_features / security_certs / API_docs
├── Content/                     # LinkedIn > Newsletter > 白皮书 > Webinar > 行业会议 > Podcast
├── Knowledge-Cards/             # 技术概念卡片深度加强
├── Opportunities/
└── Sources/
```

## 特有字段

### 品牌（SaaS 核心）
| 字段 | 说明 | 来源 |
|------|------|------|
| arr | Annual Recurring Revenue 年度经常性收入 | Forbes Cloud 100 / 融资新闻 / 估算 |
| growth_rate_yoy | YoY 同比增长率 | Press release / 行业报告 |
| funding_stage | 融资阶段 (Seed/A/B/C/D/IPO/Public) | Crunchbase / PitchBook |
| pricing_model | freemium / usage-based / per-seat / per-feature / tiered / enterprise | Pricing page |
| icp | Ideal Customer Profile 理想客户画像 (team size / industry / geo / role) | Landing page / Case studies |
| deployment | cloud / on-premise / hybrid | Product docs / Enterprise page |
| founding_date | 公司成立日期 | About page / LinkedIn |

### 痛点（B2B 决策链特有）
| 维度 | 典型痛点 |
|------|---------|
| 采购决策 | cycle too long(周期太长) / too many stakeholders(决策者太多) / procurement bureaucracy(采购流程官僚) |
| 集成 | integration pain(集成痛苦) / data silos(数据孤岛) / API limits(API限制) / vendor lock-in(厂商锁定) |
| 安全合规 | SOC2 / GDPR / data residency / audit requirements |
| ROI证明 | hard to measure ROI(难以衡量ROI) / no clear baseline(无基线) / long time to value(价值兑现慢) |
| 采用阻力 | user resistance(用户抗拒) / training burden(培训负担) | feature bloat(功能臃肿) |

### 竞品拆解加深
| 分析项 | 说明 |
|--------|------|
| pricing_page_structure | 定价页结构（tier名称/锚定/年度折扣/enterprise联系销售） |
| free_trial_design | 免费试用设计（时长/功能限制/信用卡要求/转化流程） |
| enterprise_features | 企业版特性（SSO/SLA/专属客服/自定义/合规认证） |
| security_certifications | SOC2 Type II / GDPR / ISO27001 / HIPAA 等 |
| api_documentation_quality | API文档质量（完整度/示例/SDK/版本管理） |
| developer_experience | DX评分（CLI/SDK/library质量/响应时间/TTFB） |
| PLG signals | Product-Led Growth 信号（free tier质量/self-serve/viral loops） |

## 搜索策略差异

| 需求 | 搜索关键词 |
|------|-----------|
| SaaS品牌发现 | "top {category} software 2025" / "best {category} tools for {team_size}" |
| G2评测数据 | "G2 {category} grid report" / "{product} G2 review rating" |
| 融资/ARR | "{company} funding round" / "{company} ARR revenue" / "Cloud 100 {year}" |
| 对比内容 | "{productA} vs {productB}" / "{productA} alternative" / "switch from {productA} to" |
| IT决策者内容 | "{category} for enterprise" / "{category} RFP template" / "{category} TCO comparison" |
| 开发者信号 | GitHub stars {repo} / "{product} API documentation" / Hacker News {product} |

## 数据源优先级

| 数据类型 | 推荐源 |
|---------|-------|
| 评测对比 | **G2** > Capterra > Gartner > TrustRadius > Oyster |
| 融资/估值 | **Crunchbase** > PitchBook > TechCrunch > Forbes |
| 新产品 | **ProductHunt** > Hacker News > Betalist |
| 决策者内容 | **LinkedIn** (thought leadership) > Newsletter (Stratechery/Ben Evans/etc.) |
| 开发者趋势 | **GitHub** trending/trending devs > StackOverflow survey > HN |
| 行业报告 | Gartner Magic Quadrant > Forrester Wave > IDC > McKinsey tech |
