# DTC E-Commerce 骨架（DTC独立站电商）

> 适用: DTC品牌、独立站电商、Shopify品牌、跨境电商、订阅制电商。

---

name: dtc-ecommerce
category: DTC / 独立站电商
keywords: [DTC, 独立站, 直销电商, Brand Commerce, Shopify, 订阅制, AOV, LTV, CAC, 跨境电商]
aliases: ["DTC", "独立站", "DTC电商", "Brand Commerce", "Direct-to-Consumer"]

## 目录树调整

```
output/<slug>-OS/
├── Brands/                      # 核心指标: AOV/LTV/CAC/复购率
│   ├── _INDEX.md                # 按 ARR 或估算营收排序
│   └── {brand}.md               # 含 DTC 特有字段
├── Products/
│   ├── TREE.md                  # 按 funnel 角色分类: 流量款/利润款/转化款/搭售款
│   └── {category}.md
├── Pain-Points/                 # DTC 特有痛点: 获客成本高/退货率/忠诚度
├── Keywords/                    # 高意向购买词占比高
├── Competitors/                 # ⭐ 核心产出: 全维度网站拆解
│   ├── _SYNTHESIS.md
│   └── {brand}/analysis.md      # 最详细的拆解（导航/Collection/Tag/Blog/SEO/弹窗/加购流/评测展示）
├── Content/                     # 重点: UGC激励 / 邮件营销 / 社媒引流 / 微影响者
├── Opportunities/               # 重点: 技术栈机会/物流优化/支付本地化/合规
└── Sources/
```

## 特有字段

### 品牌（DTC 核心指标组）
| 字段 | 说明 | 来源 |
|------|------|------|
| aov | Average Order Value 平均客单价 | OrderBrain / SimilarWeb+推测 / 行业基准 |
| ltv | Life Time Value 生命周期价值 | 估算 (LTV = AOV × Purchase Frequency × Lifespan) |
| cac | Customer Acquisition Cost 获客成本 | Social Blade ad spend估算 / 行业报告 |
| repeat_rate | 复购率 | 评测 / 订阅数据 / 行业基准 |
| checkout_platform | 建站工具 (Shopify Plus/Magento/Custom) | BuiltWith |
| fulfillment_mode | 履约方式 (自建仓/3PL/FBA/Dropship) | Shipping policy页 / Footer |
| email_list_size | 邮件列表规模 | Signup popup / Newsletter page |

### 竞品拆解（DTC 加深项）
| 分析维度 | 说明 |
|---------|------|
| landing_page_count | 专用落地页数量（产品线/受众/场景各一个？） |
| popups | 弹窗策略（exit-intent / welcome mat / spin-the-wheel / discount） |
| reviews_integration | 评价展示方式（Yotp/Judgeme/内置 / 无） |
| upsell_flow | 加购/交叉销售流程（cart page / post-purchase / bundle） |
| subscription_tier | 订阅档次和权益设计 |
| affiliate_program | 联盟营销计划（存在与否 / 佣金率 / 平台） |
| referral_program | 推荐奖励计划 |

## 搜索策略差异

| 需求 | 搜索关键词 |
|------|-----------|
| DTC品牌发现 | "DTC brands in {category}" / "{category} Shopify stores" / "best direct to consumer {category}" |
| 网站技术栈 | "builtwith {domain}" / "{domain} tech stack shopify apps" |
| 流量估算 | "{domain} similarweb traffic" / "{domain} monthly visitors" |
| 营收估算 | "{domain} revenue estimates" / "{company name} funding revenue" |
| 广告素材 | Facebook Ad Library {brand} / TikTok Creative Center {category} |
| 邮件营销 | 注册邮件列表 / 搜索 "{brand} newsletter signup offer" |

## 数据源优先级

| 数据类型 | 推荐源 |
|---------|-------|
| 流量/技术栈 | SimilarWeb / BuiltWhat / Wappalyzer |
| 营收/融资 | Owler / Crunchbase / PitchBook |
| 广告策略 | Meta Ad Library / TikTok Creative Center / Library |
| DTC新闻 | Retail Dive / Modern Retail / eCommerceNews / 2PM |
| 建站工具生态 | Shopify App Store / Shopify Plus case studies |
