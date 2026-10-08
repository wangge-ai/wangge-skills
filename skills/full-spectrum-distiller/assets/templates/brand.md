---
name: "{{BRAND_NAME}}"
website: "{{URL}}"  # ⚠️ Step 2.5 验证前的候选值
verified_website: "{{VERIFIED_URL}}"  # 🆕 v2.1: Step 2.5 验证后的最终值
mode: brand
step: 2
date: "{{DATE}}"
gaps: []  # 🆕 v2.1: 数据缺口动态登记数组
tags: [distiller, brand]
---

# {{BRAND_NAME}}

## 基本信息

| 字段 | 值 |
|---|---|
| 官网（候选） | {{URL}} |
| **官网（已验证）**🆕 | **{{VERIFIED_URL}}** （验证时间: {{VERIFICATION_DATE}} / 来源: {{VERIFICATION_SOURCES}}）|
| 创立时间 | {{YEAR}} |
| 创始人 | {{FOUNDER}}（背景：{{FOUNDER_BG}}） |
| 总部 | {{HQ}} |
| 团队规模 | {{TEAM_SIZE}}（来源：LinkedIn / 官网 / 推测） |
| 融资情况 | {{FUNDING}} |
| 估计规模 | {{REVENUE_OR_GMV}}（**数据截至 {{DATA_CUTOFF}}**，置信度: ★★★☆☆） |

## 产品线

- {{PRODUCT_1}}：{{ONE_LINER}}
- {{PRODUCT_2}}：{{ONE_LINER}}
- {{PRODUCT_3}}：{{ONE_LINER}}

## 价格区间

{{PRICE_RANGE}}（单 SKU 最低 / 最高 / 订阅折扣）

## 销售渠道

- DTC 官网
- Amazon（ASIN: **{{ASIN}}** 🆕）（如有）
- 线下零售（Target / Whole Foods / Sephora / 具体店名）
- TikTok Shop / Instagram Shop / 其他社交电商
- 国际市场（具体国家/地区）
- 分销商/代理商

## 核心卖点

1. {{USP_1}}
2. {{USP_2}}
3. {{USP_3}}

## 社媒账号

| 平台 | Handle | 粉丝 | 风格 |
|---|---|---|---|
| Instagram | @{{IG}} | {{N}} | ... |
| TikTok | @{{TT}} | {{N}} | ... |
| YouTube | {{YT_CHANNEL}} | {{N}} | ... |
| X/Twitter | @{{X}} | {{N}} | ... |
| Newsletter | {{NL}} | subs={{N}} | ... |

## 用户评价引用 🆕

> 从真实用户声音中提取的代表性评价。每条带来源链接。

### 正面评价 (Top 3-5)

1. > "{{QUOTE}}"
>
> —— [来源]（{{URL}}，填入真实来源后再生成链接） · ⭐⭐⭐⭐⭐ · {{DATE}}
> **提炼**: 这条好评说明了产品的哪个核心优势？

2. > "{{QUOTE}}"
>
> —— ...

### 负面评价 / 抱怨 (Top 3-5)

1. > "{{QUOTE}}"
>
> —— [来源]（{{URL}}，填入真实来源后再生成链接） · ⭐· {{DATE}}
> **提炼**: 这个抱怨指向什么未满足的需求/痛点？

2. > "{{QUOTE}}"
>
> —— ...

### 评价总结

- 用户最常夸的 3 点: ...
- 用户最常骂的 3 点: ...
- 购买决策关键因素排名: ...

## 优势 / 劣势

**优势**：
- ...
- ...

**劣势 / 风险**：
- ...
- ...

## 备注

- 数据缺口（gaps）: `{{GAPS_ARRAY}}`
- URL 验证状态: ✅ verified / ❌ failed / ⏳ pending
- 来源汇总: {{SOURCES}}

---
*由 distiller v2.1 Step 2 产出 · 含验证URL + ASIN + 用户评价 + gaps*
