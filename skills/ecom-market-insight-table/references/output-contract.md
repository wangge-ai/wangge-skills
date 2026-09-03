# Output Contract

## Quick Chat Read

Use when the user wants a short answer:

```text
样本口径：
当前判断：
最拥挤的地方：
相对值得看的方向：
最大缺口：

先做：
1.
2.
3.
```

## Market Insight Report

Use when saving a Markdown report:

```markdown
# <category> 市场洞察报告

> 数据来源：
> 样本数量：
> 关键字段：
> 证据说明：
> 生成时间：

## 1. 先说判断

## 2. 这份表能证明什么

## 3. 类目和场景分层

## 4. 标题词和需求语言

## 5. 价格带结构

## 6. 品牌 / 店铺格局

## 7. 卖点拥挤度

## 8. 机会和风险清单

| 方向 | 样本依据 | 风险 | 第一动作 |
|---|---|---|---|

## 9. 如果我们要做，先测什么

## 10. 还需要补的数据
```

Footer, if needed:

```text
本报告基于用户提供的样本表格生成，用于选品、定位和运营决策参考，不代表全平台市场份额、真实 GMV、搜索量、点击率、转化率、排名或收益承诺。涉及平台规则、资质、功效、广告法、知识产权和高风险类目时，需要人工复核。
```

## Market Insight Quality Bar

A market insight report must not stop at "the file can run". When the fields allow it, answer these eight operator questions:

1. Core conclusion: market type, confidence, competition pattern, opportunity direction, price suggestion, target buyer or scene.
2. Segment structure: subcategories or title-inferred demand clusters, with count, share, sales field, average sales, and interpretation.
3. Title root / keyword matrix: high-frequency words, whether they are baseline, crowded, proof-needed, or underused.
4. Price band analysis: row share, sales share, average sales, dominant terms, and what each band implies.
5. Seller and brand map: top shops, inferred brands when no brand field exists, concentration, and entry pressure.
6. Claim saturation: which claims are already crowded, which are basic category language, and which need more table evidence.
7. Buyer / scene judgment: who the sample appears to sell to, and whether that matches the user's target category.
8. First action: enter narrowly, wait and collect, avoid generic entry, reposition, or split the market.

If the input is not actually the target category, make that the headline finding and still analyze what the sample can prove. Do not hide the mismatch at the end.

For visual reports, use the same eight-part structure and make the first screen show:

- sample size
- report level
- strongest conclusion
- biggest limitation
- next action

## Data Sufficiency Check

Use this before a report when the user asks whether the file is enough:

```markdown
# 数据充分度检查

## 当前能出的报告

- 报告级别：
- 原因：

## 已有字段

| 分析模块 | 字段 | 是否支持 | 说明 |
|---|---|---|---|

## 现在能分析

-

## 现在不能分析

-

## 要升级报告，需要补

| 想要的分析 | 需要补的字段 |
|---|---|
```

## Boss Brief

Use when the user wants a concise decision note:

```markdown
# <category> 是否值得做：一页判断

## 结论
- 建议：进入 / 窄切进入 / 暂缓 / 不建议泛做
- 原因：
- 最大不确定性：

## 证据
- 样本：
- 价格：
- 标题词：
- 店铺/品牌：
- 卖点：

## 第一轮测试
- 产品/规格：
- 价格：
- 标题关键词：
- 主图承诺：
- 详情页证明：
- 验证指标：
```

## Action Plan

```text
Segment:
Buyer scene:
Price band:
Title words to keep:
Title words to avoid:
Claim to prove:
Main image direction:
Detail page proof:
First test:
Stop condition:
Data to collect next:
```

## Profile Script Output

When using `profile_market_table.py`, expect:

- `market_table_profile.md`: readable profile for the agent and user.
- `market_table_profile.json`: structured counts and warnings.

The script is a first pass. The final report should add human judgment and should remove irrelevant raw counts.
