# Consumer Goods 骨架（消费品）

> 适用: 食品饮料、营养补剂、美妆个护、宠物、母婴、家居服饰、运动户外等实体消费品行业。

---

name: consumer-goods
category: B2C 实体消费品
keywords: [食品, 饮料, 补剂, 美妆, 个护, 宠物, 母婴, 家居, 服装, 运动, 户外, CPG, FMCG]
aliases: ["消费品", "CPG", "FMCG", "快消品", "耐用消费品"]

## 目录树（相比 generic 的调整）

```
output/<slug>-OS/
├── _INDEX.md
├── _MAP.md
├── _REFLECTION.md
├── Brands/                      # 强调三分法
│   ├── _INDEX.md                # 按 DTC品牌 / 传统转型 / 新锐 三组排序
│   └── {brand}.md               # 含特有字段: ingredient_sourcing, certification, clean_label_status
├── Products/
│   ├── TREE.md                  # 按使用场景分类 > 按成分分类
│   └── {category}.md
├── Pain-Points/                 # 强调四维度: 安全性/功效/价格敏感度/品牌信任
│   └── PAIN_POINTS.md
├── Keywords/                    # 三平台并重: 小红书种草词 + 抖音热搜 + Amazon搜索词 + 百度SEO词
│   └── KEYWORDS.md
├── Content-Sources/
│   ├── CREATORS.md
│   └── COMMUNITIES.md           # 强调: 小红书话题社区 / 抖音话题 / Reddit subreddit / 妈妈群/健身群
├── Competitors/                 # DTC站拆解 + 天猫/旗舰店分析
│   ├── _SYNTHESIS.md
│   └── {brand}/analysis.md      # 含: 天猫/京东旗舰店评分&评价分析
├── Content/                     # 三平台为主: 小红书 / 抖音 / YouTube
│   ├── accounts/_INDEX.md
│   ├── taxonomy/_CONTENT_TAXONOMY.md
│   └── patterns/_REPEATING_PATTERNS.md
├── Knowledge-Cards/
├── Opportunities/
└── Sources/                     # Deep only
    └── ...
```

## 特有字段

### 品牌（在标准 15 字段基础上增加）
| 字段 | 说明 | 来源建议 |
|------|------|---------|
| ingredient_sourcing | 原料来源（自有农场/认证供应商/普通采购） | 官网 sustainability 页 / 新闻 |
| certification | 认证（FDA/NMPA/USDA Organic/Non-GMO 等） | 官网 badge / 产品包装 |
| clean_label_status | 清洁标签状态（clean label / transitioning / conventional） | 成分表分析 |

### 产品（在标准字段基础上增加）
| 字段 | 说明 |
|------|------|
| price_per_unit | 单价（g/ml/份）用于跨品牌公平比较 |
| subscription_available | 是否有订阅制（定期购） |
| sku_count | 该类目下 SKU 数量（反映选择丰富度） |

### 痛点（强调四维度）
1. **安全性**: side effects(副作用) / contamination(污染) / fake products(假货)
2. **功效验证**: does it really work(真的有用吗) / how long to see results(多久见效)
3. **价格敏感度**: too expensive(太贵) / not worth it(不值) / cheaper alternatives(平替)
4. **品牌信任**: greenwashing(漂绿) / false claims(虚假宣传) / inconsistent quality(品质不稳定)

## 数据源优先级

| 数据类型 | 推荐源 | 说明 |
|---------|-------|------|
| 市场规模 | Euromonitor /尼尔森 NIQ | 权威消费品数据 |
| 产品趋势 | Amazon Best Sellers / 1688 / 天猫榜单 | 实时消费信号 |
| 内容趋势 | **小红书** > 抖音 > YouTube > Instagram | 中国市场小红书优先 |
| 用户声音 | 电商平台评论区 / 小红书评论 / 知乎 / Reddit | 一手用户反馈 |
| 监管动态 | FDA / NMPA / CFR / 国家药监局 | 合规风险 |
| 竞品动态 | 天猫/京东旗舰店监控 | 价格/促销/新品/评分变化 |
