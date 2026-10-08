# Google 高级搜索语法武器库

> **用途**: 当普通搜索 `"top XX brands"` 返回的是**文章而非官网列表**时，用以下语法精准定位同行独立站。
> **核心原则**: 不要搜"关于XX的文章"，要搜"XX的官网本身"。
>
> **使用时机**: Step 2（收集品牌候选）+ Step 2.5（验证URL）+ Step 3（补充竞品）

---

## 一、找独立站 / 官网（最常用 · 用在 Step 2）

### 1.1 基础精准定位

| # | 语法 | 作用 | 搜索示例 |
|---|------|------|---------|
| 1 | `site:.com "{keyword}"` | 限 .com 域名（排除 .org/.net/.edu 等非商业站点）| `site:.com "weight loss supplements"` |
| 2 | `site:.com "{keyword}" official` | 含 "official" 关键词（命中官方页面概率高）| `site:.com "DTC coffee" official` |
| 3 | `intitle:"shop" OR intitle:"store" "{industry}"` | 标题含 shop 或 store（电商站强信号）| `intitle:"shop" "clean beauty"` |
| 4 | `inurl:/products "{keyword}"` | URL 路径含 `/products`（Shopify 等电商平台标准结构）| `inurl:/products "skincare brand"` |
| 5 | `inurl:/shop "{keyword}"` | URL 含 `/shop` | `inurl:/shop "pet food"` |
| 6 | `inurl:/collections "{keyword}"` | URL 含 `/collections`（Shopify Collection 页）| `inurl:/collections "home organization"` |
| 7 | `intitle:"welcome to" OR intitle:"home" "{brand-like}"` | 品牌首页常见标题 | `intitle:"welcome to" "nutrition brand"` |

### 1.2 排除噪音

| # | 语法 | 排除什么 | 示例 |
|---|------|---------|------|
| 8 | `"{keyword}" -amazon -walmart -target -ebay` | 排除大零售商 | `"protein powder brands" -amazon -walmart -target` |
| 9 | `"{keyword}" -youtube -pinterest -instagram -tiktok` | 排除社媒平台 | `"home decor" -youtube -pinterest -instagram` |
| 10 | `"{keyword}" -indeed -glassdoor -linkedin` | 排除招聘网站 | `"SaaS company" -indeed -glassdoor` |
| 11 | `"{keyword}" -wikipedia -encyclopedia` | 排除百科 | `"AI tools" -wikipedia -encyclopedia` |
| 12 | `"{keyword}" -filetype:pdf -filetype:ppt` | 排除文档 | （保留只看网页结果）|

### 1.3 找特定电商平台

| # | 语法 | 目标 | 示例 |
|---|------|------|------|
| 13 | `"{keyword}" myshopify.com` | Shopify 店铺 | `"coffee subscription" myshopify.com` |
| 14 | `site:myshopify.com "{industry}"` | 限定 Shopify 生态 | `site:myshopify.com "skincare"` |
| 15 | `"powered by shopify" "{keyword}"` | 页面含 Shopify 标记 | `"powered by shopify" "vitamins"` |
| 16 | `"{keyword}" "powered by bigcommerce"` | BigCommerce 店 | `"fashion" "powered by bigcommerce"` |
| 17 | `"{keyword}" "powered by woocommerce"` | WooCommerce 店 | `"organic food" "powered by woocommerce"` |
| 18 | `site:squarespace.com "{keyword}"` | Squarespace 站 | `site:squarespace.com "photographer"` |

### 1.4 从榜单/文章反推品牌+URL

> 有时候最快的方式不是直接搜品牌，而是先找到"Top N 品牌"的**榜单文章**，从中提取品牌名→再逐个验证。

| # | 语法 | 目标 | 示例 |
|---|------|------|------|
| 19 | `"best {industry}" 2025 site:forbes.com` | Forbes 榜单 | `"best DTC brands 2025" site:forbes.com` |
| 20 | `"top {industry} companies" 2025` | 各类 Top N 文章 | `"top supplement companies" 2025` |
| 21 | `{industry} market report filetype:pdf` | PDF 行业报告（内有公司列表+官网）| `US pet food market report filetype:pdf` |
| 22 | `"{industry}" "funding" OR "series A" OR "raised"` | 融资新闻（含公司名+官网）| `"AI writing" funding series A` |
| 23 | `"founders of" "{industry}"` | 创始人采访/介绍（含公司链接）| `"founders of" "DTC skincare"` |
| 24 | `site:techcrunch.com "{industry}"` | TechCrunch 报道（有 startup 链接）| `site:techcrunch.com "AI agent"` |
| 25 | `site:producthunt.com "{keyword}"` | ProductHunt（产品页常带官网链接）| `site:producthunt.com "note taking app"` |
| 26 | `site:ycombinator.com "{industry}"` | YC 公司目录（有 website 字段）| `site:ycombinator.com "developer tool"` |

---

## 二、验证 URL / 确认公司真实性（用在 Step 2.5）

### 2.1 验证这个域名是否真的是该品牌的官网

| # | 语法 | 目标 | 示例 |
|---|------|------|------|
| 27 | `site:{domain} about` | 找 About 页面（确认公司信息）| `site:goli.com about` |
| 28 | `site:{domain} careers OR jobs` | 找招聘页（真公司才有招聘）| `site:ritual.com careers` |
| 29 | `site:{domain} press OR media kit` | 找 Press Page（正规品牌特征）| `site:hellofresh.com press` |
| 30 | `"{brand}" linkedin.com/company` | LinkedIn 公司页（有 verified website）| `"Goli Nutrition" linkedin.com/company` |
| 31 | `"{brand}" crunchbase.com` | Crunchbase 公司档案（有 homepage URL）| `"Notion" crunchbase.com` |
| 32 | `"{brand}" wikipedia.org` | Wikipedia（大品牌才有条目）| `"OpenAI" wikipedia.org` |

### 2.2 找站内特定页面类型

| # | 语法 | 目标 | 示例 |
|---|------|------|------|
| 33 | `site:{domain} inurl:/products` | 产品列表（用于分析 SKU 结构）| `site:goli.com inurl:/products` |
| 34 | `site:{domain} inurl:/collections` | Collection/分类列表 | `site:goli.com inurl:/collections` |
| 35 | `site:{domain} inurl:/blog` | 博客列表（内容分析入口）| `site:hellofresh.com inurl:/blog` |
| 36 | `site:{domain} inurl:/pricing` | 定价页（SaaS 必拆）| `site:notion.so inurl:/pricing` |
| 37 | `site:{domain} inurl:/help OR inurl:/faq` | FAQ/帮助页（用户痛点金矿）| `site:slack.com inurl:/help` |
| 38 | `site:{domain} inurl:/testimonials` | 客户评价页 | `site:hubspot.com inurl:/testimonials` |

---

## 三、中文行业专用语法

| # | 语法 | 目标 | 示例 |
|---|------|------|------|
| 39 | `site:.com.cn OR site:.cn "{行业}" 官方` | 中国官网 | `site:.com.cn "美妆" official` |
| 40 | `"{行业}" 品牌 排行 2025` | 中文排行榜 | `"功能性护肤品" 品牌 排行 2025` |
| 41 | `"{行业}" 天猫旗舰店` | 天猫店 → 反推品牌 | `"益生菌" 天猫旗舰店` |
| 42 | `"{行业}" 小红书 品牌 OR 博主` | 小红书品牌讨论 | `"精酿啤酒" 小红书 品牌` |
| 43 | `"{行业}" 微信 公众号 头部` | 公众号头部账号 | `"知识付费" 微信 公众号 头部` |
| 44 | `"{行业}" 抖音 带货 OR 直播` | 抖音带货主播 | `"零食" 抖音 带货` |

---

## 四、组合搜索策略模板

### 场景 A：全新陌生行业，一个品牌都不知道

```
Round 1 — 广撒网（拿品牌名单）:
  WebSearch "top {industry} companies brands 2025"
  WebSearch "{industry} market leaders"

Round 2 — 精准找官网（本武器库 1-8 条语法）:
  WebSearch 'site:.com "{industry}" official'
  WebSearch '"best {industry}" 2025 site:forbes.com OR site:entrepreneur.com'

Round 3 — 补漏（从融资/榜单/YC/PH 反推）:
  WebSearch '{industry} "funding" OR "series A"'
  WebSearch 'site:producthunt.com "{keyword}"'
  WebSearch 'site:ycombinator.com "{industry}"'
```

### 场景 B：已知几个头部品牌，要找长尾/新兴品牌

```
Round 1 — 以已知品牌为锚点找同类:
  WebSearch 'similar to {known-brand} OR "{known-brand} alternative"'
  WebSearch '"like {known-brand}" but {differentiator}'
  WebSearch '{known-brand} competitors'

Round 2 — 在 Shopify 生态内扫:
  WebSearch '"{industry}" myshopify.com'
  WebSearch 'site:myshopify.com "{keyword}"'

Round 3 — 内容营销角度反推:
  WebSearch '"we switched from {known-brand} to"'   ← 用户真实转移信号
  WebSearch '{known-brand} vs'                       ← 对比文里会提竞品
```

### 场景 C：已知品牌名但找不到正确官网

```
Step 1 — 多源交叉:
  WebSearch '{brand-name} official website'
  WebSearch '{brand-name} linkedin.com/company'
  WebSearch '{brand-name} crunchbase'

Step 2 — 排除干扰:
  WebSearch '"{brand-name}" -amazon -youtube -pinterest'

Step 3 — 如果还是不对 → Fallback:
  → Wikipedia
  → Wayback Machine (archive.org)
  → 标记 unverified，跳过该品牌
```

---

## 五、常见错误 & 纠正

| 错误现象 | 原因 | 纠正语法 |
|---------|------|---------|
| 结果全是 Amazon/eBay 产品页 | 没排除大平台 | 加 `-amazon -ebay -walmart` |
| 结果全是 YouTube 视频 | 没排除视频平台 | 加 `-youtube -vimeo -dailymotion` |
| 结果全是 Pinterest 图片 | 没排除图片站 | 加 `-pinterest -imgur -unsplash` |
| 结果全是招聘广告 | 搜索词触发了 job 类结果 | 加 `-indeed -glassdoor -jobs` |
| 结果太少（<5条）| 语法太严格 | 去掉部分限制符（如去掉 `site:` 改为宽松搜索）|
| 结果太多但不相关 | 语法太宽泛 | 加 `intitle:` / `inurl:` 缩窄 |
| 找到的是代理商/分销商而非品牌官网 | 品牌词太通用 | 加 `"official"` 或 `"headquarters"` 或换品牌全称 |
| 域名拼写相似但不是同一家 | AI 生成近似域名 | **必须做 Phase 2 多源交叉验证** |
