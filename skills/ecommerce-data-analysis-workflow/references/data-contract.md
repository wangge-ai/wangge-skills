# Data Contract

Use this file to define the standard fields before writing transformation logic.

## Recommended Standard Detail Fields

Required:

- date
- platform
- channel
- store
- operator
- sku
- product_name
- quantity
- sales_amount
- product_cost
- promotion_cost
- profit

Often needed:

- supplement_amount
- supplement_units
- platform_fee
- tax
- finance_cost
- freight
- commission
- real_sales_amount
- profit_rate
- promotion_rate

## ID Rules

Treat these fields as text:

- SKU
- product ID
- order ID
- campaign ID
- shop ID

Do not let Excel or pandas convert long IDs into scientific notation. If a value ends with `.0` because of spreadsheet conversion, normalize it back to a plain text ID only when it is safe.

## Date Rules

Keep two forms:

- normalized date, such as `2026-07-01`
- source-compatible key, such as an Excel serial number when old formulas depend on it

## Source Types

Backend export:

- usually contains transaction, shipment, sales, promotion, or inventory details

Maintenance table:

- usually contains cost, ownership, fee, target, or mapping rules

Old result table:

- used to verify whether the rebuilt process matches the previous workflow
