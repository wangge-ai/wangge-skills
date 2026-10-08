---
name: ecom-page-planner
description: Use when planning ecommerce product-link positioning, visible selling-point
  analysis, main-image marketing positioning, 1+5 main-image sequences, or detail-page
  structure from product facts, competitor images, keywords, reviews, Q&A, and market
  evidence.
license: MIT
---

# Ecommerce Page Planner

Plan the complete page strategy without blurring evidence and creative proposals.

## Route the request

- Visible competitor expression: read `references/ecom-main-image-selling-point-analysis.md`.
- Buyer, pain point, benefit, and proof priority: read `references/ecom-main-image-marketing-positioning.md`.
- Main-image sequence: read `references/ecom-main-image-series-planner.md`.
- Detail-page screen plan: read `references/ecom-detail-page-planner.md`.
- Multiple listing/link division: read `references/ecom-category-link-positioning-matrix.md` and `references/category-output-contract.md`.

## Shared workflow

1. Build an evidence pack from product facts, market data, visible competitor material, keyword data, and user feedback.
2. Label every claim as fact, visible observation, inference, proposal, or missing evidence.
3. Select only the requested planning layer; do not generate every artifact by default.
4. Write executable page tasks with copy limits, proof assets, layout intent, and acceptance criteria.
5. Keep all business data and outputs under `./outputs/ecommerce\page-planning` unless the user chooses another output directory.

Use `scripts/validate_output.py` for category-link matrices. `scripts/build_planning_artifact.py` is a shared lightweight scaffold. Resolve the available Python runtime instead of assuming `python` is on PATH.
