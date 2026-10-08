---
brand: "{{BRAND}}"
url: "{{URL}}"
scraped_at: "{{DATE}}"
step: 3
tags: [distiller, competitor]
---

# 竞品拆解 · {{BRAND}}

## 0. 一句话定位

{{POSITIONING}}

## 1. 导航结构

```
{{NAV_TREE}}
```

**老板大脑解读**：
- 第一屏 / 第一个 Tab 放的是【利润 / 流量 / 新品】
- 排序背后的意图：...

**利润角色标注**：
| 导航项 | 推断角色 |
|--------|---------|
| ... | 流量产品 / 利润产品 / 转化产品 / 信任背书 |

## 2. Collection 结构

```
{{COLLECTIONS}}
```

**典型成交路径**：Best Sellers / New Arrival / Under $X / Gift / Bundle / Sale

**多竞品重合分析**: （哪些 Collection 在 ≥2 个竞品中出现？= 已验证高转化路径）

## 3. Product Tag 结构

抽样 N 个产品页拿到的标签：

| 标签 | 频次 | 类型（材质/场景/人群/季节/价格/功效） |
|---|---|---|
| ... | ... | ... |

**推断**：
- Google 怎么理解这类产品
- 站内推荐怎么组织
- 用户搜索语言习惯

## 4. SEO 结构

| 维度 | 内容 |
|---|---|
| Title 模板 | {{TITLE_PATTERN}} |
| Meta Description | {{META_PATTERN}} |
| URL 结构 | /collections/.../products/... |
| Schema 标记 | Product / Review / FAQ / Breadcrumb / Organization |
| 内部链接密度 | 高/中/低 |
| Sitemap 大小 | {{N}} URL |
| Canonical 使用 | 有/无（是否规范） |

## 5. Blog 结构

- 文章总数：{{N}}
- 更新频率：{{FREQ}}/周
- 最后更新：{{DATE}}
- 主题分布：

| 主题类型 | 数量 | 占比 | 代表文章 |
|---------|------|------|---------|
| "Top N / Best ..." | | | [{{TITLE}}]（{{URL}}，填入真实来源后再生成链接） |
| "How To / Guide" | | | |
| "VS / Comparison" | | | |
| "Review / 测评" | | | |
| Case Study | | | |
| Company News | | | |

**结论**：博客是 **流量入口** / **教育转化** / **信任建立** / **SEO 主力**？

## 6. Footer 结构 🆕

```
{{FOOTER_LINK_TREE}}
```

**信号解读**：
- Footer 链了什么 = 品牌想被什么关键词搜到
- 是否有站点地图链接？（SEO 规范性信号）
- 是否有 social 链接？哪些平台？
- 版权信息和法律链接是否齐全？（正规度信号）

## 7. Landing Page 结构 🆕

抽 {{N}} 个 Landing Page 分析：

| 模块 | 在 LP 的位置 | 设计意图 | 具体内容 |
|------|------------|---------|---------|
| Hero | 第 1 屏 | 一句话价值主张 | {{HERO_TEXT}} |
| 卖点排列 | 第 2 屏 | 功能→利益翻译 | {{POINTS_LIST}} |
| 社会证明 | 第 3 屏 | 消除疑虑 | {{PROOF_ELEMENTS}} (评价/Logo墙/数据) |
| CTA 按钮 | 重复出现 | 行动召唤 | {{CTA_TEXT}} + 出现次数 |
| FAQ / Objections | 末屏 | 打消最后顾虑 | {{FAQ_COUNT}} 条 |
| 附加模块 | — | 差异化元素 | （如计算器/quiz/对比表/AR展示）|

**LP 分析结论**：该品牌的核心转化心理是什么？

## 8. 转化路径细节 🆕

### Email Capture
- 方式: quiz / popup / footer / checkout / 侧边栏
- 弹窗工具: Privy / Justuno / OptinMonster / 自建 / 无
- 诱饵: X% off / free guide / quiz result / giveaway
- 出现时机: 首次访问 / 离开意图 / 滚动到位置 / 时间延迟

### Loyalty & 积分
- 有/无: ✅ / ❌
- 方案名称: （如 Goli Rewards / Ritual Points）
- 积分规则: （消费X元=1分 / 1分=$X / 等级制）
- 会员权益: （免邮 / 早期访问 / 专属产品）

### 订阅模式
- 有/无: ✅ / ❌
- 折扣: 首 X% off / 固定金额 off
- 频率: 每 X 周 / 每月 / 自定义
- 工具: Recharge / Bold / Skio / Loop / 自建

### 凑单逻辑
- 满 ¥/$ X 包邮: 是/否，门槛多少
- 买 X 送 Y: 具体方案
- Bundle 折扣: 套装 vs 单买省多少
- 限时促销: countdown / flash sale / evergreen

### 弹窗策略
- 工具识别: （见下方第 9 节工具栈）
- 弹窗数量: 首页共几个弹窗层
- 弹出时机: immediate / exit-intent / scroll / time-delay
- 关闭难度: 容易关闭 / 需要填邮箱才能关 / 多次出现

## 9. 工具栈识别 🆕⭐

通过页面源码 / script src / meta 标记 / class 名推断：

| 类别 | 识别结果 | 置信度 |
|------|---------|-------|
| **建站平台** | Shopify / WooCommerce / BigCommerce / Headless / Custom / 其他 | 高/中/低 |
| **评论系统** | Yotpo / Judge.me / Loox / Stamped / Okendo / Reviews.io / 自建 / 无 | |
| **邮件营销** | Klaviyo / Mailchimp / Postscript / Sendlane / Omnisend / 其他 | |
| **订阅管理** | Recharge / Bold / Skio / Loop / Ordergroove / 自建 / 无 | |
| **分析追踪** | GA4 / Heap / Hotjar / Amplitude / Mixpanel / Segment / 其他 | |
| **弹窗工具** | Privy / Justuno / OptinMonster / Wisepops / 上层自建 / 无 | |
| **客服工具** | Gorgias / Zendesk / Intercom / Crisp / 其他 | |
| **CDN / 加速** | Cloudflare / Fastly / Shopify CDN / 无 | |
| **其他关键工具** | （如 referral program / affiliate platform / SMS marketing）| |

**工具栈洞察**：
- 该品牌的**月技术栈花费估算**: $X-$Y/月（基于工具公开定价）
- 与行业标准对比: （超前/持平/落后）
- 可复制的组合: ...
- 差异化选择: （选了不常见的工具 → 为什么？）

## 10. 社媒矩阵

| 平台 | 账号 | 粉丝 | 内容风格 | 更新频率 | 互动率 | 引流方式 |
|------|------|------|---------|---------|-------|---------|
| Instagram | @{{IG}} | {{N}} | | | | profile link / bio link / stories link |
| TikTok | @{{TT}} | {{N}} | | | | bio link / comments / video caption |
| YouTube | {{YT}} | {{N}} | | | | description / cards / end screen |
| X/Twitter | @{{X}} | {{N}} | | | | bio link / pinned tweet |
| Newsletter | {{NL}} | subs={{N}} | | | freq={{F}} | signup CTA everywhere |
| Facebook | @{{FB}} | {{N}} | | | | group + page |
| Pinterest | @{{PT}} | {{N}} | | | | pin links to blog/product |
| LinkedIn | (B2B适用) | {{N}} | | | | company page posts |

## 11. 内容漏斗映射

| 漏斗阶段 | 对应内容类型 | 该品牌的具体表现 |
|---------|------------|----------------|
| Awareness（曝光） | Blog top-of-funnel / 社媒 viral content | |
| Interest（种草） | Instagram feed / Pinterest pins / TikTok trends | |
| Consideration（对比）| Comparison pages / Review features / Specs | |
| Conversion（行动）| LP / Product page / Sale popup | |
| Retention（复购）| Email flow / Loyalty program / Unboxing | |

## 12. 移动端快速检查 🆕

- 响应式: ✅ 完美 / ⚠️ 基本可用 / ❌ 问题明显
- 导航变化: （移动端导航是否不同？hamburger menu?）
- 页面速度感: 快 / 中 / 慢（主观感受）
- AMP / PWA: 有 / 无
- 移动端特有元素: （app download banner / click-to-call 等）

---

*由 distiller v2.1 Step 3 产出 · 12 维拆解*
