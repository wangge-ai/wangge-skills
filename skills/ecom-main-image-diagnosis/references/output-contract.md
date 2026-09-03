# Output Contract

## Quick Diagnosis

Use when the user wants a short answer in chat:

```text
Evidence scope:
Overall judgment:
Biggest click gap:
Best opportunity:

Fix now:
1.
2.

Test next:
1.
2.

Need from user:
```

## Formal Report

Use when saving or delivering a report:

```markdown
# 电商主图点击诊断报告

> 素材来源：
> 平台场景：
> 证据边界：
> 生成时间：

## 1. 一句话判断

## 2. 商品与流量场景

## 3. 点击缺口地图

## 4. 评分卡

## 5. 最小改图实验

## 6. 主图序列建议

## 7. 设计师执行清单

## 8. AI 生成 / 修图 Prompt

## 9. 测试与复盘建议

## 10. 边界与风险
```

Footer, if needed:

```text
输出内容用于主图优化和创意测试参考，不构成点击率、转化率、销量、排名或收益承诺。涉及商标、人物、品牌、包装、功效和平台规则时，需要人工复核。
```

## Designer Brief

```text
Objective:
Platform:
Image size:
Buyer:
Current problem:
Core click promise:
Keep:
Remove:
Make larger:
Make quieter:
Add:
Copy:
Layout:
Proof assets:
Variants:
Do not:
```

## A/B Test Plan

```text
Baseline:
Variant B:
Variant C:
One-variable rule:
Primary metric:
Secondary metric:
Minimum sample:
Decision rule:
Rollback condition:
```

## Same-Category Comparison

Use when the user tests two or more products in one category:

```markdown
## Same-Category Comparison

Evidence scope:

| Dimension | Product A | Product B | What to test |
|---|---|---|---|
| Shelf impact | | | |
| Click promise | | | |
| Proof / claim risk | | | |
| Offer clarity | | | |
| Title-image alignment | | | |
| Visual crowding | | | |

Best current use:
- Product A:
- Product B:

Next experiment:
- Product A:
- Product B:

Do not conclude:
```

## Main Image + Detail Five-Image Report

Use when the user wants one report that includes both main-image diagnosis and the first 5 detail-page images:

```markdown
# 电商主图与详情页五图诊断报告

> 素材来源：
> 平台场景：
> 证据边界：
> 生成时间：

## 1. 一句话判断

## 2. 主图和详情页分工

| 模块 | 任务 | 不该承担 |
|---|---|---|
| 主图 | 3 秒点击理由：结果、证明线索、成交钩子 | 完整机制、全部证明、所有套餐 |
| 详情页前 5 张 | 承接点击：结果确认、机制解释、证明来源、套餐选择、场景补充 | 重复做五张主图 |

## 3. 主图点击诊断

## 4. 详情页前 5 张承接诊断

| 序号 | 详情图任务 | 当前观察 | 重构建议 |
|---|---|---|---|
| 1 | 结果承接 | | |
| 2 | 机制解释 | | |
| 3 | 证明信任 | | |
| 4 | 套餐/价格 | | |
| 5 | 场景/人群/口味 | | |

## 5. 主图重构路线

## 6. 详情页五图重构路线

## 7. 设计执行清单

## 8. AI 修图提示词

## 9. A/B 测试与复盘

## 10. 边界与人工复核
```

For share packages, include two input modes:

- Auto acquisition: product links enter the workflow; public main/detail images are collected when possible.
- User-provided assets: the reader provides main images, detail images/screenshots, title, price band, platform, and claim sources.

## Case Summary For Public Sharing

Use this only for public articles or share packages:

```text
Before:
Problem:
Change:
After direction:
Why it matters:
Reusable lesson:
What this workflow will not claim:
```

Keep public writing result-first. Put commands, validation logs, source cleanup notes, and failed attempts in README or handoff docs.
