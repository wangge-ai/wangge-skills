# 全域蒸馏器 (Full-Spectrum Distiller) v2.2

> **一句话**: 输入一个行业/品牌/网站/话题 → 自动输出一套完整的结构化深度认知体系（Obsidian 兼容 + HTML 总报告）。
> **v2.1 核心修复**: 解决"搜索能搜对但找网站总是找不对"的顽疾——新增 Google 高级搜索语法武器库 + URL 验证清洗流程。
> **v2.2 新增**: 收尾环节产出 `report.html` 单文件总报告，把分散 .md 聚合成可视化统一入口，浏览器直开可分享。

---

## 触发词

用户提到以下任意图景时触发：
- "帮我研究一下 XX 行业/领域/品牌/话题"
- "分析一下 XX 品牌/网站" / "拆解 XX"
- "我想了解 XX 领域" / "快速了解 XX"
- "蒸馏 XX" / "全域蒸馏 XX" / "Industry OS"
- "建立 XX 的认知体系" / "做一个 XX 的深度调研"

---

## 一、识别输入模式（必做的第一步）

按以下规则判定 `mode`，并在 `_INDEX.md` 顶部注明：

| 输入特征 | mode | 重点产出 |
|---|---|---|
| 含 `http://` `https://` 或裸域名（`.com/.io/.ai/.co/.cn`） | `website` | 第 4 步竞品拆解为主 |
| 单个公司 / 产品名（1-4 词，可识别为具体品牌） | `brand` | 第 4 步 + 该品牌内容矩阵 |
| 行业 / 市场 / 赛道短语（含"行业""市场"或宽领域词） | `industry` | 全跑 |
| 窄概念 / 技术词（如 GLP-1、MCP、向量数据库） | `topic` | 第 5、7 步 + 信息源 |

用户可以用 `--mode <industry/brand/website/topic>` 显式覆盖。

### 不同 mode 的步骤差异

| mode | Step 1 建骨架 | Step 2 填库 | Step 2.5 验证URL | Step 3 竞品拆解 | Step 5 内容生态 | Step 6 地图+机会 | Step 7 情报源 |
|---|---|---|---|---|---|---|---|
| `industry` | ✅ 完整骨架 | ✅ 全量数据库 | ✅ 全量验证 | ✅ Top 5-10 竞品 | ✅ 全平台采样 | ✅ 完整地图+机会 | 仅 Deep 档 |
| `brand` | ✅ 子集 | 该品牌产品+痛点 | ✅ 验证该品牌 | ✅ 深拆该品牌 | ✅ 该品牌矩阵 | ✅ 品牌为中心 | 仅 Deep 档 |
| `website` | 仅 Competitors/ | 跳过 | ✅ 验证该URL | ✅ 深拆该URL | 可选 | 仅站点机会 | 仅 Deep 档 |
| `topic` | ✅ 精简骨架 | 痛点 + 关键词 | ⏭️ | 跳过 | ✅ 相关内容 | ✅ 机会地图 | 仅 Deep 档 |

详见 `modes.md`。

---

## 二、识别深度档位

| 档位 | 触发关键词 / 参数 | 每维度抓取量 | 跑哪些步骤 |
|---|---|---|---|
| Quick | `--quick` / "快速过一下" / "简单看看" | Top 10-15 | 仅 Step 2 + 6 |
| **Standard（默认）** | 不指定 | **Top 20-30，每条字段填齐** | Step 1-6 全跑 |
| Deep | `--deep` / "深度研究" / "全套" | Top 50-100 | 全跑 + Step 7 情报系统 |

**质量铁律（⭐ 核心）**：宁可只列 20 个品牌但每条都有「官网/创始人/价格/渠道/卖点/社媒」，也不要列 100 个只有名字的空壳。抓不到实时数据时，老老实实标注 *数据截至 YYYY-Qq*，不要编造。

**URL 质量铁律（⭐⭐ v2.1 新增）**：宁可只验证 15 个正确官网并深拆，也不要拿 50 个错误/过期/代理页 URL 去空转。每个 URL 必须通过验证流程。

---

## 三、复用行业骨架（重要）

执行前必读 `skeleton-library.md`，按输入**关键词精确匹配**到对应骨架文件（`../assets/skeletons/*.md`）。如果命中已有骨架，直接套用其目录树、字段表、数据源建议。

匹配不到时落回 `../assets/skeletons/_generic.md`，并在执行结束后把新行业的特征写回 `skeleton-library.md` 末尾「已研究行业」清单，逐步沉淀复用资产。

---

## 四、流水线（v2.1：7 步）

每一步执行完，**必须**在该步主输出文件末尾追加一段「复盘 prompt」（模板见 `reflection-prompts.md`），让用户能复制出去再追问「这一步漏了什么」。

### 流程总览

```
┌──────────────────────────────────────────────────────────┐
│                   Industry Distiller v2.1                 │
│                                                          │
│  Input: target + mode (--mode) + depth (--deep)          │
│                                                          │
│  ┌─────────┐                                             │
│  │ Step 0  │  解析输入 & 初始化项目                        │
│  └────┬────┘                                             │
│       ▼                                                   │
│  ┌─────────┐                                             │
│  │ Step 1  │  建骨架 (scaffold)                           │
│  └────┬────┘                                             │
│       ▼                                                   │
│  ┌─────────────┐                                         │
│  │ Step 2      │  填数据库 (database)                      │
│  │ 品牌/产品    │                                         │
│  │ /痛点/关键词  │                                         │
│  └──────┬──────┘                                         │
│         ▼ ⭐ v2.1 核心                                    │
│  ┌──────────────────┐                                   │
│  │ Step 2.5         │  🔍 官网验证 & URL 清洗              │
│  │ Google 高级搜索   │  ← 解决"找不对网站"                 │
│  │ 多源交叉验证      │     的核心步骤                       │
│  └──────┬───────────┘                                   │
│         ▼                                                   │
│  ┌─────────┐   ┌─────────┐                                │
│  │ Step 3  │──▶│ Step 5  │                                │
│  │ 竞品拆解  │   │ 内容生态  │                               │
│  └─────────┘   └────┬────┘                                │
│                     │                                      │
│       ┌─────────────┼──────────┐                          │
│       ▼             ▼          ▼                          │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐                      │
│  │ Step 6  │ │ Step 7  │ │ Final   │                      │
│  │地图+机会  │ │情报系统  │ │ Report  │ → 🆕 v2.2: report.html│
│  └─────────┘ └────┬────┘ └─────────┘                      │
│                ↑                                        │
│        [仅 Deep]                                        │
└──────────────────────────────────────────────────────────┘
```

### 并发规则

| 可并行 | 必须串行 |
|---------|----------|
| Step 2 内部子任务可并行 | Step 1 → Step 2（依赖骨架） |
| **Step 2.5 内各品牌 URL 验证可并行** | **Step 2 → Step 2.5 ⚠️（依赖品牌列表 + 候选URL）** |
| Step 3 多个竞品的已验证URL抓取可并行 | **Step 2.5 → Step 3 ⚠️（依赖验证后的URL清单）** |
| Step 5 内容分类与模式挖掘可并行 | Step 3 → Step 5（依赖竞品清单） |
| Step 6 知识卡片生成可并行 | Step 5/6 → Step 7（汇总分析） |

单步执行：`--step <N>` 或自然语言「只跑第 X 步」。

详细执行说明 → `pipeline.md`

**Google 高级搜索语法武器库** → `google-search-tactics.md`（v2.1 新增，⭐⭐ 核心武器）

---

## Step 0：初始化项目

### 动作
1. 创建输出目录树（见第六节）
2. 生成 `_INDEX.md`（含输入元信息 + 进度追踪）
3. 根据输入类型确定 mode 和执行路径
4. 匹配行业骨架（第三节）

### _INDEX.md 模板

```markdown
---
title: {target} 行业操作系统
slug: {target-slug}
mode: {auto-detected}
depth: {quick/standard/deep}
created: {YYYY-MM-DD}
data_cutoff: {YYYY-MM-DD}
status: in-progress
url_verification: pending  # v2.1 新增
tags: [{industry}, distiller-os]
---

# {target} - OS

> **Mode**: {mode} | **Depth**: {depth} | **Created**: {date}

## 执行进度

| Step | 名称 | 状态 | 产出 | 备注 |
|------|------|------|------|------|
| 0 | 初始化 | ✅ | 本文件 | - |
| 1 | 建骨架 | ⏳ | - | - |
| 2 | 填数据库 | ⏳ | - | - |
| 2.5 | ⭐ URL验证 | ⏳ | verified-urls.json | v2.1 核心 |
| 3 | 竞品拆解 | ⏳ | - | - |
| 5 | 内容生态 | ⏳ | - | - |
| 6 | 地图+机会 | ⏳ | - | - |
| 7 | 情报系统 | ⏳ | Deep only | - |

## 导航
（同 v2.0）
```

---

## Step 1：建骨架（scaffold）

选骨架 → 在 `output/<slug>-OS/` 建目录 + 空 `.md` 文件 → 写 `_INDEX.md`。

根据 mode 决定建哪些子目录（参考第一节差异表）。每个目录放一个 `README.md` 说明该目录用途和字段定义。

**产出**: `output/<slug>-OS/` 完整目录树 + `_INDEX.md`

---

## Step 2：填数据库（database）

核心数据采集阶段。根据 mode 和 depth 决定采集范围。

### 2.1 品牌数据库

**工具策略**: 用 `WebSearch` + **Google 高级搜索语法**（见 `google-search-tactics.md`）搜索同行品牌。

> ⚠️ v2.1 关键变化：此步产出的 `official_website` 字段是**候选 URL**，不一定正确。正确性由 Step 2.5 保证。此步的目标是**尽可能多地收集候选品牌名和候选 URL**，不要在此步花时间验证。

**字段表**:

| 字段 | 必填 | 说明 | 数据来源建议 |
|------|------|------|-------------|
| brand_name | ✅ | 中文名 / 英文名 | 搜索结果 |
| official_website | ✅ | **候选**官网 URL（待 Step 2.5 验证） | 搜索结果（可能不准） |
| founded_year | ⚪ | 成立年份 | Wikipedia/Crunchbase |
| headquarters | ⚪ | 总部 | 官网关于页 |
| key_products | ✅ | 核心产品线（3-5个） | 官网产品页 |
| price_range | ⚪ | 价格区间 | 电商/官网 |
| estimated_revenue | ⚪ | 估算年营收（标注置信度） | 新闻/财报 |
| main_channels | ✅ | 主要销售渠道 | 官网/社媒 |
| core_selling_point | ✅ | 核心卖点（一句话） | 官网首页 |
| founder_background | ⚪ | 创始人背景 | 新闻/采访 |
| social_accounts | ⚪ | 社媒账号清单 | 官页 footer |
| positioning | ✅ | 定位（高端/大众/平价） | 价格+调性推断 |
| target_audience | ✅ | 目标人群 | 广告/文案推断 |
| unique_advantage | ⚪ | 独特优势 | 对比分析 |
| **user_reviews** | 🆕 | **用户评价引用 3-5 条**（带来源链接） | Reddit/Amazon/Trustpilot 评价 |
| **asin/amazon_id** | 🆕 | Amazon ASIN（如有） | Amazon 搜索 |
| **gaps** | 🆕 | 数据缺口数组 | 执行中动态登记 |

**输出**:
- 单文件: `Brands/{brand_name}.md`
- 汇总表: `Brands/_INDEX.md`（按营收降序）
- Quick: Top 10-15 / Standard: Top 20-30 / Deep: Top 50-100

### 2.2 产品数据库

按行业产品分类体系建立树状结构。（字段表同 v2.0，不变）

**输出**: `Products/TREE.md` + `Products/{category}.md`

### 2.3 用户痛点数据库 ⭐ 高价值

挖掘用户高频抱怨、未满足需求、FAQ。（结构同 v2.0，不变）

**输出**: `Pain-Points/PAIN_POINTS.md`

### 2.4 关键词数据库 🆕 拆分为独立文件

按搜索意图分成 **5 个独立 .md 文件**（比 v2.0 单文件更易检索）：

| 文件名 | 意图 | 特征 | 示例关键词 |
|--------|------|------|-----------|
| `Keywords/commercial.md` | Commercial | 有购买意向 | "best {product}", "buy ...", "{brand} 评测" |
| `Keywords/informational.md` | Informational | 信息查询 | "what is ...", "how to ...", "什么是..." |
| `Keywords/comparison.md` | Comparison | 对比选择 | "A vs B", "alternative to ...", "...和哪个好" |
| `Keywords/review.md` | Review | 评价参考 | "... review", "... 体验", "... 测评", "... 避坑" |
| `Keywords/buying-intent.md` | Buying Intent | 购买决策最后一步 | "X coupon code", "X discount", "X 便宜" |

每个文件含：
- Top 10-20 关键词 + 月搜索量(估算) + 难度 + CPC + 来源平台
- **用户语言原文短语**（来自真实评论/帖子，非搜索词——写文案时可直接用）
- 关联痛点和产品类型的双链

### 2.5 内容源 & 社区（可选，Standard+）

头部创作者、KOL、垂直媒体、重要社区/论坛的清单。（同 v2.0）

---

## Step 2.5：🔍 官网验证 & URL 清洗（v2.1 新增 · 核心步骤）

> **为什么需要这一步？**
>
> AI 生成的 URL 经常出错：拼写相似的域名、已倒闭的品牌、聚合页冒充官网、HTTP→HTTPS 未跳转、地区重定向到错误版本。
> 直接拿未验证的 URL 去 `WebFetch`，结果就是：404、拿到完全无关的页面、或浪费时间拆解一个假站点。
>
> **本步目标**：把 Step 2 产出的「候选 URL」清洗成「已验证 URL 清单」，供 Step 3 使用。

### 2.5.1 验证流程（对每个品牌的候选 URL）

```
候选 URL (来自 Step 2)
    │
    ▼
┌──────────────────────────────────────┐
│ Phase 1: 快速存活检查                  │
│ WebFetch 取前 500 字符                  │
│ → 能否访问？返回 200？                   │
│ → title 是否包含品牌名？                 │
│ → 是否是域名停放页/广告页/聚合页？        │
└──────────────┬───────────────────────┘
               │ 200 + title 匹配 ✅
               ▼
┌──────────────────────────────────────┐
│ Phase 2: 多源交叉验证（至少 2 个来源）    │
│                                       │
│ ① WebSearch "{brand} official site"   │
│ ② WebSearch "{brand} website"          │
│ ③ Wikipedia / Crunchbase / LinkedIn    │
│                                       │
│ → ≥2 个来源指向同一个 URL → ✅ 通过      │
│ → 来源冲突 → 取最权威的那个（官 > 维基 > 新闻) │
│ → 所有来源都没有 → ❌ 标记 unverified     │
└──────────────┬───────────────────────┘
               │ 验证通过
               ▼
┌──────────────────────────────────────┐
│ Phase 3: 内容抽样验证                   │
│ WebFetch 首页完整内容                   │
│ → 检查 hero 区域是否有品牌 logo/名称     │
│ → 检查导航栏是否合理（不是垃圾站）         │
│ → 检查 footer 有无 copyright + 年份      │
│ → 对比产品线是否和 Step 2 记录一致        │
└──────────────┬───────────────────────┘
               │ 全部通过
               ▼
        写入 verified-urls.json ✅
```

### 2.5.2 Google 高级搜索语法武器库 ⭐⭐

当普通搜索 `"top {industry} brands"` 返回的是文章而非官网列表时，使用以下语法精准定位**同行独立站**：

#### A. 找官网（最常用）

| 语法 | 作用 | 示例 |
|------|------|------|
| `site:.com "{keyword}" official` | 限 .com 域名 + 含 official | `site:.com "weight loss supplements" official` |
| `intitle:"shop" OR intitle:"store" "{industry}"` | 标题含 shop/store | `intitle:"shop" "DTC coffee brands"` |
| `inurl:/products "{keyword}"` | URL 含 /products（强电商信号） | `inurl:/products "skincare"` |
| `inurl:/shop "{keyword}"` | URL 含 /shop | `inurl:/shop "pet food"` |
| `"{keyword}" -amazon -walmart -target` | 排除大零售商 | `"clean beauty brands" -amazon -walmart` |
| `"{keyword}" -youtube -pinterest -instagram` | 排除社媒平台 | `"home organization" -youtube -pinterest` |

#### B. 从榜单文章反推品牌+官网

| 语法 | 作用 | 示例 |
|------|------|------|
| `"best {industry}" 2025 site:forbes.com OR site:entrepreneur.com` | 找权威榜单 | `"best DTC brands 2025" site:forbes.com` |
| `"top {industry}" list 2025` | 找各类 Top N 文章 | `"top supplement companies" list` |
| `"{industry}" market report filetype:pdf` | 找 PDF 行业报告（内有公司列表） | `"US pet food market" filetype:pdf` |

#### C. 找 Shopify / 独立站专用

| 语法 | 作用 | 示例 |
|------|------|------|
| `"{keyword}" myshopify.com` | 直接找 Shopify 店铺 | `"coffee subscription" myshopify.com` |
| `"powered by shopify" "{keyword}"` | 搜 Shopify 店铺 | `"powered by shopify" skincare` |
| `site:myshopify.com "{industry}"` | 限定在 Shopify 生态内 | `site:myshopify.com "protein bars"` |
| `"{keyword}" store powered by bigcommerce` | 找 BigCommerce 店 | （同理适配其他平台）|

#### D. 找特定页面类型

| 语法 | 作用 | 示例 |
|------|------|------|
| `site:{domain} inurl:/collections` | 找某站的 Collection 页 | `site:goli.com inurl:/collections` |
| `site:{domain} inurl:/blog` | 找某站的 Blog | `site:hellofresh.com inurl:/blog` |
| `site:{domain} inurl:/about` | 找某站的 About 页 | （用于验证公司真实性）|
| `"{brand}" careers OR jobs` | 找招聘页（验证是否真公司） | `"Goli Nutrition" careers` |
| `"{brand}" press OR media kit` | 找 press page（验证品牌正规性）| |

#### E. 中文行业补充语法

| 语法 | 作用 | 示例 |
|------|------|------|
| `site:.com.cn OR site:.cn "{行业}" 官方` | 找中国官网 | `site:.com.cn "美妆" 官方` |
| `"{行业}" 品牌 排行 2025` | 找中文排行榜 | `"功能性护肤品" 品牌 排行` |
| `"{行业}" 天猫旗舰店` | 找天猫店反推品牌 | `"益生菌" 天猫旗舰店` |
| `"{行业}" 小红书 品牌` | 找小红书上的品牌讨论 | （用于内容生态补充）|

### 2.5.3 Fallback 策略

当某个品牌的 URL 反复无法验证时：

| 尝试 | 方法 |
|------|------|
| Fallback 1 | 换搜索引擎/换关键词组合重新搜 |
| Fallback 2 | 去 LinkedIn 搜公司名 → 取其 website 字段 |
| Fallback 3 | 去 Wikipedia/Crunchbase/Yellow Pages 查 |
| Fallback 4 | 用 Wayback Machine (archive.org) 查历史快照确认曾经存在 |
| 最终兜底 | 标记 `unverified`，在 `_INDEX.md` gaps 数组登记，**不进入 Step 3 拆解** |

### 2.5.4 产出物

**`verified-urls.json`**（或用 Markdown 表格写入 `Competitors/_VERIFIED_URLS.md`）：

```markdown
# 已验证 URL 清单（Step 2.5 产出）

> 验证时间: {date} | 验证方法: multi-source-cross-check
> 总候选: N | 通过验证: M | 未通过: K | 待人工确认: L

| # | 品牌名 | 候选 URL | 验证后 URL | 验证状态 | 验证来源 | 备注 |
|---|--------|---------|-----------|---------|---------|------|
| 1 | Goli | goli.com (候选) | **https://goli.com** | ✅ verified | Google+Wikipedia+Crunchbase | 3源一致 |
| 2 | Ritual | ritual.com (候选) | **https://www.ritual.com** | ✅ verified | Google+LinkedIn | HTTP→HTTPS 重定向 |
| 3 | ??? Brand | xxx.com (候选) | — | ❌ failed | — | 404 / 域名停放 / 非官网 |
```

**同时**：回写到 `Brands/{brand}.md` 的 `official_website` 字段，把候选值替换为验证后的值。

---

## Step 3：竞品拆解（competitor）

> **核心思维**: 同行已经替你交了学费了。你只需要研究他们为什么赚钱。
> **v2.1 保证**: 进入本步的所有 URL 都已经过 Step 2.5 验证。

### 3.1 选择竞品池

从 **`verified-urls.json`** 中筛选（不再从品牌库盲选）：
- 直接竞品（同类产品/定位）— 3-4 个
- 间接竞品（替代方案）— 2-3 个
- 新兴挑战者（增速最快）— 1-2 个
- 跨区域对标 — 1-2 个（如有）

### 3.2 网站全维度拆解（12 维度，v2.1 从 8 维扩展）

**工具策略**: 用 `WebFetch` 抓取**已验证**的竞品 URL。

#### 3.2.1 导航栏拆解

| 导航项 | 子菜单 | 推断目的 | 利润角色 |
|--------|--------|---------|---------|
| ... | ... | ... | 流量产品/利润产品/转化产品/信任背书 |

**利润角色分类**: 流量产品 / 利润产品 / 转化产品 / 信任背书

#### 3.2.2 Collection / 分类结构分析

Collection = 成交路径。多竞品的 Collection 重合部分 = 已验证的高转化路径。

#### 3.2.3 Tag / 标签体系分析 ⭐ 高价值

Tag = 用户的搜索语言 = SEO 的理解方式 = 推荐系统的组织逻辑。

#### 3.2.4 SEO 结构分析

- Title 模板规律 / Meta Description / Schema 标记 / URL 结构 / 内链密度 / Sitemap 大小

#### 3.2.5 Blog 结构分析

- 文章总数 / 更新频率 / 主题分布（Top10/Best/HowTo/Vs/Review/Case Study 占比）

#### 3.2.6 Footer 结构 🆕

```
{{FOOTER_LINK_TREE}}
```
**信号**: Footer 链什么页面 = 品牌想被搜什么关键词命中。

#### 3.2.7 Landing Page 结构（抽 1-3 个）🆕

| 模块 | LP 中的位置 | 设计意图 |
|------|------------|---------|
| Hero | 第 1 屏 | 一句话价值主张 |
| 卖点 3 列 | 第 2 局 | 功能/利益排序 |
| 社会证明 | 第 3 屏 | 评价/Logo墙/数据 |
| CTA | 重复 N 次 | 行动召唤设计 |
| FAQ | 末屏 | 消除最后疑虑 |

#### 3.2.8 转化路径细节 🆕

- Email capture 方式：quiz / popup / 折扣码 / footer
- Loyalty / 积分体系：有/无 / 具体方案
- 订阅折扣：X% off / 首单优惠
- 凑单逻辑：满 N 包邮 / 送赠品 / 买 X 送 Y
- 弹窗策略：Privy / Justuno / 自建 / 无弹窗

#### 3.2.9 工具栈识别 🆕⭐

通过抓取页面源码 / view-source 推断技术栈：

| 类别 | 推断依据 | 常见选项 |
|------|---------|---------|
| 建站平台 | JS 变量 / meta generator / URL 结构 | Shopify / WooCommerce / BigCommerce / Headless / Custom |
| 评论系统 | class 名 / script src / iframe src | Yotpo / Judge.me / Loox / Stamped / Okendo / Reviews.io |
| 邮件营销 | script src / link href / cookie 名称 | Klaviyo / Mailchimp / Postscript / Sendlane / Omnisend |
| 订阅管理 | script src / checkout URL 参数 | Recharge / Bold / Skio / Loop |
| 分析追踪 | script src / noscript img | GA4 / Heap / Hotjar / Amplitude / Mixpanel |
| 弹窗/弹窗 | div id / script src / data 属性 | Privy / Justuno / OptinMonster / Wisepops / 上层自定义 |
| 客服工具 | widget script / iframe | Gorgias / Zendesk / Intercom / Crisp |
| 评价展示 | schema 标记 / class 名 | Yotpo / Judge.me / Loox / Stamped / Okendo |

> 💡 **为什么工具栈重要？** 工具栈反映了品牌的成熟度、预算量和技术选型倾向。一堆 DTC 品牌都用 Klaviyo+Yotpo+Recharge = 这套组合是该行业的"标准答案"。谁没用？为什么不用？（可能自研了、可能太早期、可能在测试替代品）= **差异化线索**。

#### 3.2.10 内容漏斗 & 社媒矩阵

- awareness → interest → consideration → conversion → retention 各阶段的典型内容
- 各平台的账号、粉丝量、内容策略、引流方式

#### 3.2.11 定价页分析（SaaS/B2B 适用）🆕

- 定价层级数 / 免费模式设计 / Enterprise 接洽方式 / 年付折扣 / 对比竞品定位

#### 3.2.12 移动端体验（快速检查）🆕

- 是否响应式 / 移动端导航差异 / AMP 使用 / PWA 支持

**输出**: `Competitors/{brand-name}/analysis.md`（使用 `../assets/templates/competitor.md` 模板，已包含上述全部维度）

### 3.3 竞品综合对比

将所有竞品整合为对比矩阵（维度从 8 个扩展到 12+）。

**关键产出**:
- **行业共识**（≥60% 竞品都在做）= 已验证的最佳实践
- **差异化机会**（≤20% 竞品在做但有效）= 蓝海空间
- **工具栈共识**（哪些工具组合出现频率最高）

**输出**: `Competitors/_SYNTHESIS.md`

---

## Step 5：内容生态（content）

> **核心思维**: 不要研究一个账号，要研究 100 个账号。一次爆可能是运气，十次爆一定是规律。

### 5.1 大规模账号采样

**工具策略**: 用 `WebSearch` + Google 高级语法搜索各平台创作者。

**采样范围**: Standard 50+ / Deep 100+ 账号。

**账号档案字段**（v2.1 增强）:

| 字段 | 说明 |
|------|------|
| account_name | 账号标识 |
| platform | 平台 |
| url | **真实链接（必填）** |
| followers | 粉丝数 |
| update_freq | 更新频率 |
| content_theme | 主要内容方向（1-2句话） |
| top_content_type | 最火内容类型 |
| monetization_mode | 变现模式 |
| engagement_rate | 互动率估算 |
| growth_trend | 增长趋势 |
| uniqueness_score | 稀缺度评分(1-10) |
| **content_mother_topics** | 🆕 母题（反复出现的选题方向，2-3个标签） |
| **team_size** | 🆕 个人/小工作室/公司 |

### 5.2 内容五分类法

对所有爆款内容逐一归类（分类定义同 v2.0 不变）。

### 5.3 重复爆款规律挖掘 ⭐ 核心

（分析方法同 v2.0，增加以下 🆕 维度）

**🆕 额外分析**:
- **沉默赢家**: 粉丝不多但每条都爆的小账号（通常比头部更值得抄）
- **死掉的爆款**: 6 个月前还爆但现在哑火的选题（不能复用）
- **跨平台迁移**: 某个选题在 A 平台爆了但 B 平台还没人做的

**输出**: `Content/patterns/_REPEATING_PATTERNS.md`

### 5.4 账号代表作档案 🆕

对 Top 20 账号，每家建立**可借鉴档案**：

```markdown
## {账号名} 可借鉴

### 钩子 / 标题套路
（他们常用的标题公式，可直接套用）

### 节奏 / 结构
（视频/文章的结构模式：怎么开头、怎么转折、怎么收尾）

### 视觉 / 包装
（封面风格、配色、字体、排版特点）

### 行动召唤 (CTA)
（他们怎么引导关注/购买/点击）

### 代表作 3 条（必须带真实链接）
1. **[标题](https://example.com/)** · {播放/阅读量} · {互动数据}
   - 类型: exposure/growth/save/conversion/personal
   - 为什么爆: {一句话分析}
   - 可借鉴点: {...}
```

**输出**: `Content/accounts/{handle}.md`

---

## Step 6：知识地图 + 机会（map + opportunity）

### 6.1 三级树状知识地图

（同 v2.0，不变）

**输出**: `_MAP.md`（**🆕 含 Mermaid mindmap 格式**）

```mermaid
mindmap
  root(({Industry}))
    一级领域A
      二级A1
        三级节点
        公司/产品
      二级A2
    一级领域B
      二级B1
```

### 6.2 网络视图

（同 v2.0，**🆕 强制 Mermaid flowchart LR**）

### 6.3 知识卡片

（同 v2.0，不变）

### 6.4 机会清单 🆕 拆分为 4 个独立文件

| 文件 | 聚焦 | 内容标准 |
|------|------|---------|
| `Opportunities/01-low-competition.md` | 🟢 低竞争蓝海 | 竞争弱 + 需求已验证 |
| `Opportunities/02-fast-growth.md` | 🟡 高增速赛道 | 增速快 + 时间窗口开放 |
| `Opportunities/03-content-gap.md` | ⚪ 内容空白 | 供给不足 + 有需求信号 |
| `Opportunities/04-aha-moments.md` | 💡 意外洞察 | 拆解过程中冒出来的反常识发现 |

每个文件含 3-8 条机会，每条用 `../assets/templates/template-opportunity.md` 格式。

**同时保留** `Opportunities/_INDEX.md` 作为总索引。

---

## Step 7：情报系统（sources）— 仅 Deep 档

（同 v2.0，不变）

---

## 五、不同深度的执行差异总结

| 步骤 | Quick (Top 10-15) | Standard (Top 20-30) | Deep (Top 50-100) |
|------|--------------------|---------------------|-------------------|
| Step 1 建骨架 | ✅ 精简 | ✅ 标准 | ✅ 完整 |
| Step 2 填库 | ✅ 品牌+痛点 | ✅ 全部子库 | ✅ 全部+详实+评价引用 |
| **Step 2.5 URL验证** | ⏭️ | ✅ **全量验证** | ✅ **全量+多轮fallback** |
| Step 3 竞品 | ⏭️ | ✅ 3-5个+8维 | ✅ 5-10个+**12维**+工具栈 |
| Step 5 内容 | ⏭️ | ✅ 50账号+分类 | ✅ 100账号+**可借鉴档案** |
| Step 6 地图 | ✅ 一级+二级 | ✅ 三级+Mermaid+卡片 | ✅ 全套+**4文件机会** |
| Step 7 情报 | ⏭️ | ⏭️ | ✅ 全套情报系统 |

---

## 六、输出结构（写入 `output/<slug>-OS/`）

每个 `.md` 文件 **必须带 frontmatter**。

### 目录树（v2.2 更新）

```
output/<slug>-OS/
├── _INDEX.md                    # 顶层导航 + 进度 + URL验证状态
├── _MAP.md                      # 知识地图（ASCII树 + Mermaid mindmap）
├── _CONNECTIONS.md              # 连接关系图（Mermaid flowchart LR）
├── _REFLECTION.md               # 复盘 prompts 汇总
├── report.html                  # 🆕 v2.2: HTML 总报告（自包含单文件，浏览器直开）
├── Brands/
│   ├── _INDEX.md                # 汇总排序表（含验证后URL）
│   └── {brand}.md              # 品牌卡（含 user_reviews + ASIN + gaps）
├── Products/
│   ├── TREE.md
│   └── {category}.md
├── Pain-Points/
│   └── PAIN_POINTS.md
├── Keywords/                    # 🆕 v2.1: 拆成5个独立文件
│   ├── commercial.md
│   ├── informational.md
│   ├── comparison.md
│   ├── review.md
│   ├── buying-intent.md
│   └── _INDEX.md              # 总索引
├── Content-Sources/
│   ├── CREATORS.md
│   └── COMMUNITIES.md
├── Competitors/
│   ├── _VERIFIED_URLS.md       # 🆕 v2.1: Step 2.5 产出
│   ├── _SYNTHESIS.md           # 横评（含工具栈共识）
│   └── {brand}/
│       └── analysis.md         # 🆕 12维拆解 + 工具栈
├── Content/
│   ├── accounts/
│   │   ├── _INDEX.md
│   │   └── {handle}.md        # 🆕 含代表作+可借鉴栏目
│   ├── taxonomy/
│   │   └── _CONTENT_TAXONOMY.md
│   └── patterns/
│       └── _REPEATING_PATTERNS.md  # 🆕 含沉默赢家+死掉的爆款
├── Knowledge-Cards/
│   └── {node}.md
├── Opportunities/              # 🆕 v2.1: 拆成4个文件
│   ├── _INDEX.md              # 总索引
│   ├── 01-low-competition.md
│   ├── 02-fast-growth.md
│   ├── 03-content-gap.md
│   └── 04-aha-moments.md
└── Sources/                    # Deep only
    ├── _INFO_SOURCES.md
    ├── _MONITORING.md
    ├── _WEEKLY_TEMPLATE.md
    └── _MAINTENANCE.md
```

---

## 七、产出的标准收尾

全部步骤执行完毕后：

1. **更新 `_INDEX.md`**：所有 step 状态改为 ✅，补充产物统计
2. **🆕 v2.2 生成 `report.html`**：把所有 .md 产物聚合成一份**自包含 HTML 单文件**（见下方「HTML 报告规范」）
3. **展示 `report.html`** 给用户（用 present_files 打开，浏览器内可滚动浏览）
4. **简述执行摘要**：mode/step/骨架/验证率(通过/总数)/抓到 vs 缺数据
5. **给出 3 条下一步建议**
6. **提醒用户**：复盘 prompt 在 `_REFLECTION.md`，HTML 报告内已含
7. **提示 Obsidian 导入**：.md 文件可直接拖进 vault；HTML 报告用于分享/演示

---

### HTML 报告规范（v2.2 新增）⭐

> **为什么需要 HTML 报告？** 用户看到 14 个分散 .md 文件时体验割裂；HTML 单文件提供统一可视化入口，可浏览器直开、可分享、可打印 PDF。

#### 文件位置
- 路径：`output/<slug>-OS/report.html`
- **单文件自包含**：CSS 内联、JS 内联（可用 CDN）、无外部资源依赖（除可选 CDN 字体/图表库）
- 用户双击即可在浏览器打开

#### 报告结构（7 大区块）

```
report.html
├── <head>
│   ├── meta + title（"{target} 蒸馏报告 · {date}"）
│   └── <style> 内联 CSS（响应式 + 打印友好）
├── <body>
│   ├── ① 封面 Hero
│   │   ├── 标题: {target}
│   │   ├── 副标题: {mode} mode · {depth} 深度 · {date}
│   │   ├── 4 个 KPI 卡片: 竞品数 / 验证率 / 机会数 / 文件数
│   │   └── 生成时间戳
│   ├── ② 侧边导航 (sticky sidebar)
│   │   └── 跳转锚点: 执行摘要 / 竞品格局 / 主对象深拆 / 横评矩阵 / 机会清单 / 复盘
│   ├── ③ 执行摘要
│   │   ├── mode/depth/路径说明
│   │   ├── 数据规模统计表
│   │   └── 3 条核心发现（高亮 callout）
│   ├── ④ 竞争格局
│   │   ├── 已验证 URL 表（从 _VERIFIED_URLS.md 提取）
│   │   ├── 竞品定位矩阵图（Chart.js 散点图：AI押注 × 主战场）
│   │   └── 护城河 vs 软肋对照
│   ├── ⑤ 主对象深拆（website/brand mode 必有）
│   │   ├── 一句话定位
│   │   ├── 12 维度拆解摘要（每个维度 3-5 行精炼，不全抄 .md）
│   │   └── "查看完整拆解" 链到 .md 文件（相对路径）
│   ├── ⑥ 横评矩阵
│   │   ├── 多竞品对比表（HTML table，sticky 第一列）
│   │   ├── 行业共识（≥60% 竞品都做）
│   │   └── 差异化机会（≤20% 竞品做但有效）
│   ├── ⑦ 机会清单
│   │   ├── 4 个分类 tab（蓝海/高增速/内容空白/aha）
│   │   └── 每条机会卡：标题 + 一句话 + 置信度 + 时间窗口
│   └── ⑧ 复盘 & 下一步
│       ├── 复盘 prompt（从 _REFLECTION.md 提取）
│       ├── 3 条下一步建议
│       └── 文件清单（所有 .md 文件相对路径链接）
```

#### 技术规范

| 项目 | 要求 |
|------|------|
| 框架 | 原生 HTML + CSS + JS，**不用 React/Vue**（保证单文件可双击运行）|
| 图表 | Chart.js via cdnjs（散点图/柱状图/雷达图）|
| 字体 | 系统字体栈（-apple-system / Segoe UI / sans-serif），不引外部字体 |
| 样式 | 内联 `<style>`，浅色主题，响应式（桌面 sidebar / 移动端折叠）|
| **布局** | **`.main` 区域 `max-width: 1400px; width: calc(100% - sidebar-width)`，内容区自适应撑满宽屏（不要用固定 980px 导致右侧大片空白）|
| 交互 | 侧边栏锚点跳转 + 机会 tab 切换 + 表格排序（可选）|
| 打印 | `@media print` 隐藏 sidebar，分页符在每大区块前 |
| 体量 | 推荐 50-200KB（含内联 CSS/JS），不要超过 500KB |

#### 质量要求

- **不是简单拼接 .md**：HTML 要做信息层级精炼，每个区块是"摘要 + 关键图表 + 链到详细 .md"
- **必须有图表**：至少 1 张散点图（竞品定位矩阵）+ 1 张柱状图（机会分布）
- **必须可分享**：单文件，发给别人双击即看，无需任何环境
- **必须可打印**：Ctrl+P 出来的 PDF 要排版干净

#### 渲染策略

- **数据来源**：直接读取 `output/<slug>-OS/` 下所有 .md 文件，提取关键内容
- **不重新做研究**：HTML 是产物的"可视化包装"，不是新一轮调研
- **链接到 .md**：用户想看完整细节时，从 HTML 跳到对应 .md（相对路径）

---

## 八、质量控制 Checkpoint

（同 v2.0 + 🆕 Step 2.5 专有检查项）

### Step 2.5 完成 🆕
- [ ] 每个候选 URL 都经过了至少 Phase 1 存活检查？
- [ ] 通过的 URL 都有 ≥2 个交叉验证来源？
- [ ] 未通过的 URL 都有 fallback 尝试记录？
- [ ] `verified-urls.json` / `_VERIFIED_URLS.md` 已写入？
- [ ] 回写到 Brands/*.md 的 official_website 字段？

### Step 3 完成（v2.1 增强）
- [ ] 导航栏解读出利润角色？
- [ ] Collection 揭示成交路径？
- [ ] Tag 体系反映用户搜索习惯？
- [ ] **🆕 Footer 结构已分析？**
- [ ] **🆕 Landing Page 结构已拆解？**
- [ ] **🆌 转化路径细节（邮件/积分/凑单/弹窗）已记录？**
- [ ] **🆌 工具栈已识别（≥7个类别）？**
- [ ] 跨竞品对比找出共识+差异化+工具栈共识？
- [ ] 已追加复盘 prompt？

### 收尾完成 🆕 v2.2
- [ ] `_INDEX.md` 所有 step 状态已更新？
- [ ] **🆕 `report.html` 已生成**（自包含单文件，浏览器可直开）？
- [ ] **🆕 HTML 含至少 1 张图表**（散点/柱状）？
- [ ] **🆕 HTML 侧边栏锚点可跳转**？
- [ ] **🆕 HTML 链接到 .md 文件用相对路径**？
- [ ] **🆕 HTML 打印友好**（Ctrl+P 排版干净）？
- [ ] **🆕 HTML 布局撑满宽屏**（`.main` max-width ≥ 1400px，右侧无大面积空白）？
- [ ] 执行摘要、3 条下一步建议已写？
- [ ] 复盘 prompt 已汇总到 `_REFLECTION.md`？

---

## 九、WorkBuddy 工具适配说明

（同 v2.0，不变）

---

## 版本记录

| 版本 | 日期 | 变更 |
|------|------|------|
| 1.0.0 | 2026-06-23 | 初始版本 |
| 2.0.0 | 2026-06-25 | 4模式/3档深度/骨架复用/复盘prompt/WorkBuddy适配 |
| **2.1.0** | **2026-06-25** | **⭐ 新增 Step 2.5 URL验证流程 / Google高级搜索语法武器库(30+条) / 竞品12维拆解(+工具栈识别+Footer+LP+转化路径) / 内容账号代表作+可借鉴档案 / Keywords拆5文件 / Opportunities拆4文件 / Mermaid地图 / 品牌卡加用户评价+ASIN+gaps / skeleton-library改关键词表匹配** |
| **2.2.0** | **2026-06-25** | **⭐ 新增 HTML 总报告产出环节（第七节+目录树+质量检查项）: report.html 单文件自包含 / 7 大区块结构 / Chart.js 图表 / 侧边栏锚点 / 打印友好 / 链回 .md 详细文件** |
