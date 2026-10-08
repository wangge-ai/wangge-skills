# Pipeline：7 步流水线详细执行说明（v2.1）

每一步独立可调。所有步骤都在执行完后**追加复盘 prompt**到对应输出文件末尾。

**v2.1 核心变更**: 新增 Step 2.5 (URL验证)、Step 3 从 8维扩展到 12维、Step 5 增加代表作+可借鉴档案。

---

## Step 0 · 初始化

**目标**: 1 分钟内建好项目骨架和元信息文件。

**操作**:
1. 用输入做 slug：英文化、小写、连字符。例 `美国减肥补充剂` → `us-weight-loss-supplements`
2. 读 `skeleton-library.md` → 按关键词匹配骨架
3. 命中 → 复制 `assets/skeletons/<matched>.md` 的目录树
4. 不命中 → 用 `assets/skeletons/_generic.md`
5. 在 `output/<slug>-OS/` 下创建全部子目录和顶层文件
6. `_INDEX.md` 用模板填充（含 `url_verification: pending` 字段）

**产出**: 空骨架 + `_INDEX.md`

---

## Step 1 · scaffold（建骨架）

**目标**: 建好完整目录树 + 空 `.md` 文件 + `_INDEX.md` 进度追踪。

（同 SKILL.md Step 1 描述，不赘述）

**产出**: 完整目录树 + `_INDEX.md`

---

## Step 2 · database（填库）

> ⚠️ **关键心态变化 (v2.1)**: 此步的目标是**广撒网收集候选品牌和候选 URL**，不要在此步花时间验证 URL 正确性。验证是 Step 2.5 的事。此步要的是"多"和"全"，不是"准"。

### Brands

**搜索策略（按顺序执行）**:

```
Round A — 广撒网拿品牌名单:
  WebSearch "top {industry} brands companies 2025 2026"
  WebSearch "{industry} market leaders biggest players"
  WebSearch "{industry} startups funding 2024 2025"

Round B — Google 高级语法精准找（见 google-search-tactics.md）:
  WebSearch 'site:.com "{industry}" official'
  WebSearch '"best {industry}" site:forbes.com OR site:entrepreneur.com'
  WebSearch '"{industry}" myshopify.com'
  WebSearch '{industry} "funding" OR "series A"'

Round C — 补漏:
  WebSearch 'site:producthunt.com "{keyword}"'
  WebSearch 'site:ycombinator.com "{industry}"'
  WebSearch '{known-brand} alternatives competitors'
```

**字段填写**: 使用 `assets/templates/brand.md` 模板。
- `official_website` 字段填**候选值**（可能不准）
- `gaps: []` 数组动态登记缺失数据
- `user_reviews` 字段从 Reddit/Amazon/Trustpilot 抓 3-5 条带来源引用
- `asin` 字段从 Amazon 搜索获取（如有）

### Products / Pain-Points / Keywords

（同 SKILL.md Step 2 描述。Keywords 拆为 5 个独立 .md 文件。详见 SKILL.md §2.4）

**产出**: Brands/*.md + Products/* + Pain-Points/* + Keywords/*.md (×5)

**复盘 prompt**: 追加到各子目录的汇总文件末尾。

---

## Step 2.5 · 🔍 URL 验证与清洗（v2.1 核心 · 新增）

> **这是解决"找不对网站"问题的核心步骤。**
>
> 输入: Step 2 产出的 N 个品牌的候选 URL 列表
> 输出: `Competitors/_VERIFIED_URLS.md` — 已验证 URL 清单 + 回写到 Brands/*.md

### 执行流程

#### Phase 1: 快速存活检查（对每个候选 URL）

```
对每个 candidate_url:
  ① WebFetch(candidate_url) 取前 500 字符
  ② 检查:
     - HTTP status 是否 200? （非 200 → 标记 failed → 跳到 Fallback）
     - 页面 title 是否包含品牌名? （不包含 → 可能是错域名）
     - 是否是域名停放页/广告页/聚合页? （是 → 标记 not-official）
     - 是否有大量无关内容? （是 → 可能被劫持）
  ③ 通过 → 进入 Phase 2
  ④ 不通过 → 尝试 Fallback 1（换搜索词重搜）→ 再回 Phase 1
```

#### Phase 2: 多源交叉验证（至少 2 个独立来源一致）

```
对 Phase 1 通过的每个 URL:
  ① WebSearch "{brand_name} official website"
     → 取第1个结果URL → 记录 source_A
  ② WebSearch "{brand_name} {industry} site"
     → 取第1个结果URL → 记录 source_B
  ③ 可选: WebSearch "{brand_name} linkedin.com/company"
     → LinkedIn 公司页 website 字段 → 记录 source_C
  ④ 可选: WebSearch "{brand_name} crunchbase"
     → Crunchbase homepage URL → 记录 source_D

  判定逻辑:
    ≥2 个源指向同一 URL → ✅ verified
    所有源指向不同 URL → 取最权威的那个（官 > LinkedIn > Wikipedia > 新闻 > 论坛）
    只有1个源或0个源 → ⚠️ unverified（标记但不丢弃，留人工确认）
```

#### Phase 3: 内容抽样验证（对 ✅ verified 的 URL）

```
WebFetch(verified_url) 取首页完整内容:
  ✓ Hero 区域是否有品牌 logo 或名称?
  ✓ 导航栏是否合理（不是垃圾站的无意义链接）？
  ✓ Footer 是否有 copyright + 年份 + 联系方式？
  ✓ 产品线是否和 Step 2 记录基本一致？（如果完全不符 → 可能是错品牌同名）
  全部通过 → 写入 verified-urls.json ✅
  任何一项异常 → 降级为 ⚠️ needs-review 并标注原因
```

### Fallback 策略（当 URL 反复无法验证时）

| 顺序 | 方法 | 成功率 |
|------|------|-------|
| Fallback 1 | 换搜索引擎 / 换关键词组合重新搜 | 中 |
| Fallback 2 | 去 LinkedIn 搜公司名 → 取 website 字段 | 高 |
| Fallback 3 | 去 Wikipedia / Crunchbase / Yellow Pages 查 | 高 |
| Fallback 4 | Wayback Machine (archive.org) 查历史快照 | 中（确认曾经存在）|
| 最终兜底 | 标记 `unverified`，登记 gaps，**不进入 Step 3** | — |

### 产出物

写入 `Competitors/_VERIFIED_URLS.md`：

```markdown
# 已验证 URL 清单

> 验证时间: {date} | 方法: multi-source-cross-check (v2.1)
> 总候选: N | ✅ verified: M | ❌ failed: K | ⚠️ needs-review: L

| # | 品牌 | 候选URL | 验证后URL | 状态 | 验证来源数 | 备注 |
|---|------|---------|-----------|------|----------|------|
| 1 | Goli | goli.com | https://goli.com | ✅ | 3 (Google+Wiki+Crunchbase) | |
| 2 | Ritual | ritual.com | https://www.ritual.com | ✅ | 2 (G+LinkedIn) | HTTP→HTTPS |
| 3 | FakeBrand | fake.io | — | ❌ | 0 | 404 / 域名停放 |
```

同时回写 `Brands/{brand}.md`：
- `verified_website` 字段 = 验证后的最终 URL
- 如果验证失败 → 在 `gaps: []` 追加 `"official_website": "unverified, candidate was X"`

### 复盘 prompt

追加到 `_VERIFIED_URLS.md` 末尾（使用 reflection-prompts.md 的 S25_URL_VERIFICATION 模板）

---

## Step 3 · competitor（竞品拆解）

> **v2.1 保证**: 进入本步的所有 URL 来自 Step 2.5 的 verified 列表。不再有"拿到一个错误 URL 然后白拆一场"的情况。

### 3.1 选品池

从 `_VERIFIED_URLS.md` 的 ✅ verified 列表中筛选：
- 直接竞品 3-4 / 间接竞品 2-3 / 新兴挑战者 1-2 / 跨区域对标 1-2

### 3.2 网站拆解（12 维度，使用 assets/templates/competitor.md 模板）

**对每个已验证竞品 URL**:

```
抓取计划:
  ① WebFetch(<root_url>)          → 第 0 步: 一句话定位 + 导航结构(维度1)
  ② WebFetch(<root_url>)          → Footer 结构(维度6)
  ③ 推断或尝试 <root>/collections  → Collection 结构(维度2)
  ④ 随机抽 3-5 个产品页           → Tag 体系(维度3)
  ⑤ 尝试 <root>/blog             → Blog 分析(维度5)
  ⑥ 尝试 <root>/pricing          → 定价页(维度11, SaaS适用)
  ⑦ 尝试 <root>/help 或 /faq      → 用户痛点补充
  ⑧ 抽 1-3 个 LP                 → Landing Page(维度7)
  ⑨ 从页面源码推断                → 工具栈(维度9) ⭐⭐
  ⑩ 社媒链接从 footer/nav 收集    → 社媒矩阵(维度10)
```

**12 个维度清单**（必须全部覆盖）:

| # | 维度 | 内容 | 模板位置 |
|---|------|------|---------|
| 1 | 导航结构 | 导航树 + 利润角色标注 | §1 |
| 2 | Collection | 分类/成交路径 | §2 |
| 3 | Product Tag | 标签频次 + 类型归类 | §3 |
| 4 | SEO | Title/Meta/Schema/URL/内链/Sitemap | §4 |
| 5 | Blog | 总量/频率/主题分布/角色判定 | §5 |
| 6 | **Footer** 🆕 | 链接树 + 信号解读 | §6 |
| 7 | **Landing Page** 🆕 | 模块拆解(Hero/卖点/社证/CTA/FAQ) | §7 |
| 8 | **转化路径** 🆕 | Email/Loyalty/订阅/凑单/弹窗 | §8 |
| 9 | **工具栈** 🆕⭐ | 8类技术工具识别 + 月花费估算 | §9 |
| 10 | 社媒矩阵 | 8平台账号 + 数据 + 策略 | §10 |
| 11 | 内容漏斗 | Awareness→Retention 映射 | §11 |
| 12 | **移动端** 🆕 | 响应式/导航变化/速度/PWA | §12 |

### 3.3 横评对比

写 `Competitors/_SYNTHESIS.md`：
- 12 维度对比矩阵
- 行业共识 (≥60%)
- 差异化机会 (≤20%)
- **🆌 工具栈共识**（哪些组合出现最多）

### 复盘 prompt

追加到 `_SYNTHESIS.md` 末尾（reflection-prompts.md 的 S3_COMPETITOR）

---

## Step 5 · content（内容生态）

### 5.1 账号采样

**搜索策略**:
- `WebSearch "best {topic} youtube channels 2025"`
- `WebSearch "top {topic} tiktok influencers"`
- `WebSearch "{topic} 小红书 博主"` (中文行业)
- `WebSearch "site:reddit.com r/{sub} top posters"` (Reddit KOL)

**产出**: `Content/accounts/_INDEX.md` + `{handle}.md`(每家一个, 用 content-account.md 模板)

### 5.2 内容五分类

（分类定义不变。产出: `Content/taxonomy/_CONTENT_TAXONOMY.md`）

### 5.3 重复爆款规律

**🆕 v2.1 额外分析维度**:
- **沉默赢家**: 低粉但高爆号（比头部更值得抄）
- **死掉的爆款**: 过去爆但现在哑火（不能复用）
- **跨平台迁移**: A 平台已爆、B 平台空白

**产出**: `Content/patterns/_REPEATING_PATTERNS.md`

### 5.4 🆌 代表作 + 可借鉴档案

Top 20 账号每家建立可借鉴档案（钩子/节奏/视觉/CTA/秘密武器），写在各自的 `Content/accounts/{handle}.md` 里（见 content-account.md 模板的「可借鉴档案」章节）。

### 复盘 prompt

追加到 `_REPEATING_PATTERNS.md` 末尾（reflection-prompts.md 的 S4_CONTENT）

---

## Step 6 · map + opportunity

### 6.1 知识地图
- ASCII 树 + **Mermaid mindmap**（双格式）
- 三级节点 + 质量检查

### 6.2 连接关系
- Mermaid flowchart LR（产业链/跨界/投资/人才）

### 6.3 知识卡片（Deep/Standard 可选）

### 6.4 🆌 机会清单拆分为 4 文件

| 文件 | 聚焦 |
|------|------|
| `Opportunities/01-low-competition.md` | 🟢 蓝海 |
| `Opportunities/02-fast-growth.md` | 🟡 成长赛道 |
| `Opportunities/03-content-gap.md` | ⚪ 内容空白 |
| `Opportunities/04-aha-moments.md` | 💡 意外洞察 |

每条机会用 `template-opportunity.md` 格式。

保留 `Opportunities/_INDEX.md` 作为总索引。

### 复盘 prompt

追加到 `_MAP.md` 末尾（reflection-prompts.md 的 S5_MAP）

---

## Step 7 · sources（仅 Deep）

（同 v2.0 不变。产出: Sources/ 下全套情报系统文件）

---
