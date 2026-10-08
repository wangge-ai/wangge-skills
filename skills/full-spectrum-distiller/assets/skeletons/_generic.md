# 通用骨架 (Generic Skeleton)

> 当输入目标不匹配任何专用骨架时使用此通用骨架。

---

name: generic
category: 通用
keywords: []
aliases: ["默认"]

## 目录树

```
output/<slug>-OS/
├── _INDEX.md
├── _MAP.md
├── _CONNECTIONS.md          # 可选：如果行业有清晰的产业链/网络关系
├── _REFLECTION.md
├── Brands/
│   ├── _INDEX.md            # 汇总排序表
│   └── {brand}.md           # 使用 template-brand.md
├── Products/
│   ├── TREE.md              # 产品分类树状图
│   └── {category}.md        # 使用 template-product.md
├── Pain-Points/
│   └── PAIN_POINTS.md       # 痛点总文件（不分文件）
├── Keywords/
│   └── KEYWORDS.md          # 关键词总文件（按意图+平台分类）
├── Content-Sources/
│   ├── CREATORS.md
│   └── COMMUNITIES.md
├── Competitors/
│   ├── _SYNTHESIS.md        # 竞品综合对比
│   └── {brand-name}/
│       └── analysis.md      # 使用 template-competitor.md
├── Content/
│   ├── accounts/_INDEX.md   # 账号档案汇总
│   ├── taxonomy/_CONTENT_TAXONOMY.md
│   └── patterns/_REPEATING_PATTERNS.md
├── Knowledge-Cards/         # Standard+/Deep 推荐
│   └── {node}.md            # 使用 template-knowledge-card.md
├── Opportunities/
│   └── _INDEX.md            # Top 20 + 推荐 TOP 5
└── Sources/                 # Deep only
    ├── _INFO_SOURCES.md
    ├── _MONITORING.md
    ├── _WEEKLY_TEMPLATE.md
    └── _MAINTENANCE.md
```

## 字段定义

### 品牌（15 字段，见 SKILL.md Step 2.1）
### 产品（11 字段，见 SKILL.md Step 2.2）
### 痛点（五段式，见 SKILL.md Step 2.3）
### 关键词（五意图分类，见 SKILL.md Step 2.4）
### 竞品（六维拆解，见 SKILL.md Step 3.2）

## 搜索策略（通用起点）

| 数据需求 | 搜索关键词模板 | 推荐数据源 |
|---------|--------------|-----------|
| 品牌列表 | "{行业} top companies/brands 2025 2026" | Google/Baidu |
| 品牌详情 | "{brand} 官网 创始人 融资 营收" | Wikipedia/Crunchbase/企查查 |
| 产品分类 | "{行业} product categories 分类" | 行业报告/竞品网站 |
| 用户痛点 | "{行业} complaints problems 痛点 避坑" | Reddit/知乎/电商差评 |
| 关键词 | "{行业} SEO keywords 热搜词 小红书热词" | SEO工具/社媒平台 |
| 内容生态 | "{行业} KOL 博主 头部账号 推荐" | 各平台搜索/第三方数据 |
| 信息源 | "{行业} news blog newsletter RSS 行业媒体" | Feedly/Google News |

## 使用说明

1. 使用此骨架时在 `_INDEX.md` 中标注 `skeleton: generic`
2. 可根据 target 类型微调目录名（使其贴合行业语言）
3. 执行结束后将行业特征回填到 `../../references/skeleton-library.md`
