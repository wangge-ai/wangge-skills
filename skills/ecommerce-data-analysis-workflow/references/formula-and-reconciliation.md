# Formula And Reconciliation

## Profit Formula

Do not hard-code this formula unless the user confirms it.

A common example is:

```text
profit = sales_amount
       - product_cost
       - promotion_cost
       - supplement_amount
       - platform_fee
       - tax
       - finance_cost
       - commission
       - freight
       + supplement_product_cost
```

Different companies may include or exclude different fields. Match the old workbook or the user's explicit rule first.

## Promotion Cost Rule

Promotion cost is often not perfectly aligned with sales rows.

If a date/store/operator has promotion cost but no sales or outbound rows, keep a promotion-only row when the business wants true operating profit. This row usually has:

- sales amount = 0
- quantity = 0
- profit = negative promotion cost

Do not remove real costs just because there was no sale.

## Effective Outbound Rule

If the workflow is rebuilding outbound detail, zero-quantity outbound rows usually should be filtered out.

This rule should not be applied to promotion-only, cost-only, or maintenance-derived rows unless the user confirms it.

## Reconciliation Tables

Always create these groups:

1. Missing in rebuilt data
   Exists in old result, absent in rebuilt result.

2. Added in rebuilt data
   Exists in rebuilt result, absent in old result.

3. Matched but different
   Same key exists on both sides, but metrics differ.

## Useful Reconciliation Keys

Choose keys based on the report goal:

- date
- platform
- channel
- store
- operator
- sku

For profit-source reconciliation, date + store + operator is often more useful than SKU because many old Excel pivots aggregate to that grain.
