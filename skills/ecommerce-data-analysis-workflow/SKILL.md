---
name: ecommerce-data-analysis-workflow
description: 从电商导出表和维护表重建明细、重算业务公式、对账并输出报告。
license: MIT
metadata:
  agent_created: true
  source_pack: '17'
---

# Ecommerce Data Analysis Workflow

This skill turns downloaded ecommerce operating files into a reconciled analysis report or dashboard. It starts after files have been downloaded (assume RPA or the user already downloaded them) and ends with a validated, shareable analysis workbench.

It is a *method*, not a fixed per-company template. Adapt the field names and profit formula to the user's actual business. The share package that this skill was adapted from contained no real store names, accounts, paths, or metrics — all names were already generalized.

## Operating Principles

1. Read source files only. Do not edit, move, overwrite, or delete the user's original Excel/CSV files.
2. Write all generated outputs into a separate output folder. In WorkBuddy, default to an `outputs/` subfolder of the current working directory.
3. Treat SKU, product ID, order ID, and campaign ID as text from the beginning. Prevent scientific-notation conversion.
4. Locate columns by header names, not by fixed column positions.
5. Preserve both machine-friendly dates (`2026-07-01`) and any source-compatible display/serial dates.
6. Rebuild detail data first, then reconcile, then visualize. Do not treat visualization as validation.
7. Split mismatches into three types: missing in rebuilt data, added in rebuilt data, and matched keys with metric differences.
8. Keep public-facing reports sanitized. Replace real brands, stores, people, local paths, and sensitive categories with generic names.

## Workflow

### 1. Inventory Inputs

List all files, sheets, row counts, date ranges, and likely report types.

Classify inputs into:
- Backend exports (transaction, shipment, sales, promotion, inventory details)
- Maintenance tables (cost, ownership, fee, target, mapping rules)
- Old result tables (used as the reconciliation baseline)

See `references/workflow.md` for the full seven-step overview and `references/usage-notes.md` for what the user should prepare and tell you up front.

### 2. Define Data Contract

Read `references/data-contract.md` when field design is unclear.

Ask or infer:
- Which fields identify date, SKU, store, operator, and platform.
- Which tables provide cost, promotion, supplement, fee, and ownership mappings.
- Which old table should be used as the reconciliation baseline.

### 3. Build Standard Detail

Normalize dates, text IDs, store names, operator names, and numeric metrics.

Filter only when the business rule is explicit. For outbound/shipment rows, zero-quantity rows usually should not enter the effective outbound detail. Promotion-only rows may still be needed later if a promotion cost exists without sales.

### 4. Recompute Metrics

Read `references/formula-and-reconciliation.md` before implementing formulas.

Never assume the profit formula. Rebuild it from the user's original workbook, old formulas, or explicit instruction. A common example (confirm before using):

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

### 5. Reconcile

Reconcile at multiple grains: detail, date, store/operator/date, channel/platform, and total KPI.

Output mismatch tables before making any visual charts. Always produce these three groups:
1. Missing in rebuilt data — exists in old result, absent in rebuilt result.
2. Added in rebuilt data — exists in rebuilt result, absent in old result.
3. Matched but different — same key on both sides, but metrics differ.

For profit-source reconciliation, `date + store + operator` is often more useful than SKU because many old Excel pivots aggregate to that grain.

### 6. Build Report or Dashboard

Only after reconciliation is explainable, generate:
- KPI overview
- daily trend
- store/operator ranking
- loss details
- promotion-cost risk
- added/missing source explanation
- searchable detail table

Keep tables separately expandable; avoid cramming many large tables into one row. See `references/sample-caliber.md` for a generic front-desk-profit example of fields and analysis dimensions.

### 7. Package Results

Provide:
- rebuilt standard detail
- reconciliation workbook or CSV
- reconciliation JSON or summary
- dashboard/report HTML
- short SOP explaining what to rerun next time

For a ready-to-send prompt the user can reuse, see `references/prompt-for-ai.md`.

## Validation Checklist

- SKU and IDs did not become scientific notation.
- Formula max difference is zero or explainably tiny.
- Added rows are separated from matched-row metric differences.
- Missing rows are listed with source/date/store/operator clues.
- Promotion-only or cost-only rows are handled by business rule.
- Public-facing outputs contain no real local paths, internal store names, personal names, account IDs, or sensitive categories.
