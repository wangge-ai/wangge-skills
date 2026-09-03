# Report Router

Use this file when deciding what the uploaded table can safely support.

## Field Tiers

| Tier | Fields | Unlocks |
|---|---|---|
| A. identity | product title/name | title terms, buyer scenes, selling claims |
| B. price | price/current price | price bands, pricing pressure |
| C. demand | sales/monthly sales/payment count/receipt count/rank | demand-weighted price and segment judgment |
| D. seller | shop/seller, brand, shop type/platform | shop concentration, brand vs white-label pressure |
| E. taxonomy | category/subcategory, keyword/source platform | category split and sample scope |
| F. traceability | product URL, source, export date | audit trail and later manual review |
| G. time series | multiple exports or snapshot date | trend hints and price/rank movement |
| H. own product | user's cost, target price, specs, supply limits | entry plan and first test design |

## Report Types

| Available Data | Safe Report Type | Can Say | Cannot Say |
|---|---|---|---|
| title only | title language quick read | common words, claim crowding | price, demand, seller strength |
| title + price | supply and price-structure read | price bands, title language by price | demand-weighted opportunity |
| title + price + sales | preliminary market insight | demand signal by price/claim/category | true market size, search demand, conversion |
| title + price + sales + shop | seller/price/demand report | shop concentration, price bands, demand-weighted directions | brand pressure if brand missing |
| title + price + sales + shop + category | category market insight report | segment map, price ladder, first test direction | buyer reasons without review fields |
| above + brand/shop type/platform | full table market-entry report | brand vs white-label pressure, platform/sample scope | ROI or traffic judgment |
| multiple dated exports | trend snapshot | price movement and rank/sales signal movement | live monitoring unless automation exists |
| user's product data + competitor table | entry/action report | target segment, price, title, first test | guaranteed launch result |

## Missing-Field Template

```text
这份表现在可以出：<report type>。

能分析：
- <supported analysis>

不能分析：
- <unsupported analysis>

如果要升级成 <next report type>，建议补：
- <field 1>
- <field 2>
```

Core rule: data gives the report its depth. Missing fields should downgrade the report, not become invented conclusions.
