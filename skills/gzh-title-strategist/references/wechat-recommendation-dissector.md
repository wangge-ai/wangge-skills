---
name: wechat-recommendation-dissector
description: Use when analyzing WeChat recommendation feeds, Kan Yi Kan screenshots, subscription recommendation cards, article cards, titles, covers, and visible recommendation signals.
---

# wechat-recommendation-dissector

Use this skill when analyzing 微信公众号“看一看”、订阅号推荐、推荐流截图、公众号卡片列表、标题/封面推荐原因， or when the user provides one or more long screenshots and asks why those articles might be recommended.

## Core stance

Do not claim to know the WeChat recommendation algorithm. Treat every conclusion as a visible-signal hypothesis based on the screenshot:

- What the card exposes: title, account, cover, layout, topic, image count, wording.
- What the recommendation system might be reacting to: interest graph, freshness, entity keywords, social proof, click behavior, local relevance, visual clarity, topical heat.
- What the creator can learn: title models, cover models, topic packaging, and what to test next.

Always separate two layers:

- **Personalization layer**: the screenshot is likely influenced by the user's past reading, follows, clicks, and topic interests.
- **Shared content layer**: beyond personalization, repeated cards often share visible traits: clear entity, concrete task, visible proof, low-friction promise, decision value, and boundary/risk framing.

The second layer is the one to transfer into公众号选题 and标题规范.

## Image handling

For recommendation screenshots:

- Height under 4000 px: usually analyze directly as one image.
- Height 4000-12000 px: can analyze, but prefer splitting into 2-4 segments if text is small or there are many cards.
- Height over 12000 px: ask for cropped segments or crop the local file before analysis.
- Prefer original PNG/JPG. Avoid compressed chat thumbnails because account names and small subtitles become unreadable.
- If the user sends many screenshots, process 3-5 medium screenshots per batch, or 1-2 very long screenshots per batch.

## Extraction Fields

For each visible card, extract:

- `序号`
- `可见标题`
- `账号/来源`
- `领域`
- `封面形态`
- `标题钩子`
- `封面信号`
- `可能被推荐的原因`
- `可学习点`
- `不建议照抄点`

## Topic Buckets

Classify cards into these buckets:

- AI工具/教程: tool names, prompts, coding, image/video generation, model updates.
- 产品/消费: phone, car, food, electronics, retail tips.
- 金融/开户/交易: bank accounts, credit cards, investing, trading.
- 本地/生活: city, housing, food, local services.
- 娱乐/影视: drama, celebrity, plot, visual emotion.
- 观点/情绪: contrarian claims, identity, social conflict, personal relationship.
- 资料/资源: templates, lists, datasets, downloads.

## Title Signals

Mark the title model:

- `实体词`: product/tool/company/model names such as Codex, GPT-Image-2, 小米, 奥迪.
- `结果承诺`: “就够了”, “全公开”, “一句话”, “从0开始”, “教你”.
- `强情绪`: “杀疯了”, “别错过”, “白费”, “压不住”.
- `数字锚点`: price, battery, count, percentage, version.
- `场景锚点`: “国内”, “手机线上”, “杭州下沙”, “盒马”.
- `反差/悬念`: “没想到”, “为什么没有”, “真实处境”.

## Cover Signals

Classify cover style:

- UI截图/后台截图: increases proof and tool credibility.
- 多图拼贴: raises information density and “值得点开看”的感觉.
- 产品实拍/商品图: makes object immediately clear.
- 人脸/影视画面: provides emotion and story.
- 本地场景/门店/街景: creates location trust.
- 大字封面: suitable for教程/观点 but must remain readable.
- 暗色技术封面: good for AI/coding, but easy to look similar if no strong entity word.

## Output Format

Create a report with:

1. 截图基础信息: file, date, size if known, visible card count.
2. 总体判断: this recommendation page's dominant buckets and visible logic.
3. 逐条卡片拆解 table.
4. 标题模型总结.
5. 封面模型总结.
6. 推荐假设, clearly marked as inference.
7. 对 目标公众号 的可迁移打法.
8. 下一批截图应该继续验证什么.

## Batch Mode

When the user provides a folder or multiple screenshots:

- Ignore files that already have a matching teardown report if the user says to skip previously analyzed images.
- Build one combined report unless the user explicitly asks for one report per image.
- For very long screenshots, do not mechanically list every card. Extract representative high-signal cards, then summarize repeated patterns.
- Track recurring entities across screenshots, especially repeated tool/model/company names.
- Add a cumulative frequency-style section:
  - repeated entities
  - repeated title hooks
  - repeated cover styles
  - repeated topic buckets
  - practical implications for the user's account

## Writing Rules

- Write in Chinese unless the user asks otherwise.
- Be concrete. Quote visible titles when readable.
- Do not overfit one screenshot. Say “这张图里能看到” instead of universal claims.
- Separate “能学” from “不建议学”.
- For the user's account, translate observations into practical rules: what to write, what cover to make, what title to test, what not to chase.
