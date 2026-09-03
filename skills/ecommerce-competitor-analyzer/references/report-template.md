# Ecommerce Competitor Report Template

Use this structure for full competitor reports.

## Report Structure

```markdown
# <category> 竞品拆解报告

分析范围：<总样本/自然样本/广告样本>
数据来源：<public page/user table/screenshots/saved HTML/manifest>
样本说明：<what this sample can and cannot prove>

## 1. 先看结论

- <finding backed by evidence>
- <finding backed by evidence>
- <actionable suggestion>

## 2. 平台覆盖

| 平台 | 状态 | 有效样本 | 证据或受阻原因 |
|---|---|---:|---|

选择“全平台”时逐项列出所有目标平台；未尝试的平台不得省略。单平台或单一电商生态证据保持 `partial`。

多平台任务按平台独立执行。只要有平台可以继续，就不得只输出登录预检受阻报告：

- 种子链接所属平台可继续时必须读取种子商品，并用其类目、品牌、卖点和检索词作为后续证据。
- 可继续的平台已有样本、其他平台等待登录时，报告保留已完成平台的竞品池、价格带、卖点和限制，整体状态写 `partial`。
- 只有没有任何平台可以继续且至少一个平台明确出现登录或验证墙时，整体状态才写 `waiting_login`。
- 平台首页没有昵称或个人中心不能单独证明未登录；标签页或域名错位记录为线路错误，不写成登录失败。

## 3. 市场价格带

| 价格带 | 样本数 | 代表商品 | 常见卖点 |
|---|---:|---|---|

## 4. 竞品对比表

| 证据编号 | 页面位置 | 商品 | 平台 | 展示价格 | 价格口径 | 销量展示 | 广告边界 |
|---|---:|---|---|---:|---|---|---|

## 5. 买家关注点

- 好评集中：
- 差评集中：
- 购买顾虑：
- 未被满足的需求：

## 6. 我们怎么做

- 定价：
- 标题/搜索词：
- 主图：
- 详情页：
- 评价/问答：
- 产品改进：

## 7. 限制说明

本报告基于 <source>，不能代表全平台真实销量或全市场份额。
```

## Writing Rules

- 所有数量和价格统计只从确定性事实文件渲染，模型不得在报告正文中手工重算或覆盖。
- Say "样本显示" when the evidence is sample-based.
- Say "未提供" or leave blank when a field is missing.
- Bind sample claims to `sample_id` or a stable `ROW_###` evidence identifier.
- Separate ads from organic samples and state both denominators.
- Preserve price labels and sales display wording verbatim; do not upgrade them to checkout price or true sales.
- Do not write invented sales, review counts, traffic, conversion, market share, or sentiment percentages.
- Keep technical collection notes in README.
- 公开报告不得出现内部工具名称、调试过程或模型思索过程。
- For WeChat articles, open with the generated result and a plain pain point.
