---
name: ecom-main-image-diagnosis
description: Use when diagnosing or improving Chinese ecommerce main images, search-result cards, product-page screenshots, ad creatives, competitor image sets, designer briefs, AI image prompts, CTR problems, click hooks, visual hierarchy, platform fit, or main-image A/B test plans for Taobao, Tmall, JD, Pinduoduo, Douyin, Xiaohongshu, 1688, or similar marketplaces.
---

# Ecom Main Image Diagnosis

## Core Stance

Diagnose the user's buying decision at the image-card level, not whether the image is "nice". The useful question is:

```text
Will the right buyer notice it, understand it, trust it, and have a sharper reason to click than nearby alternatives?
```

This is a clean-room local skill. Do not include external author names, toolbox names, contact details, private version labels, generated-by footers, or source authorization text in reports, examples, README files, or share packages.

## First Triage

Classify the input before diagnosing:

| Input | Use It For | Caveat |
|---|---|---|
| Single main image | Quick click diagnosis and minimal edit plan | Mark product facts as inferred |
| Search-result screenshot | Shelf contrast, price-band pressure, visual crowding | Compare only visible competitors |
| Product-page screenshot | Main image plus title, price, SKU, trust signals | Do not infer backend data |
| 1-5 image set | Image sequence task planning | Judge each image's job, not decoration |
| Competitor images | Differentiation map and visual crowding | Do not copy competitor assets or text |
| Product link | Public field and image acquisition | If blocked, ask for screenshot or saved page |
| CTR/CVR/exposure data | Test design and priority setting | Do not promise future uplift |

If visual material is unavailable, ask for an image, screenshot, or rendered page before making visual claims.

## Diagnosis Workflow

1. State the evidence scope: what was visible, what was inferred, and what is missing.
2. Identify the platform scene: search shelf, recommendation feed, product page, ad placement, Xiaohongshu cover, or mixed use.
3. Build a compact strategy card: product, buyer, price band, decision pressure, strongest click promise, strongest proof.
4. Run the click-gap map:
   - Recognition gap: can buyers tell what it is in one glance?
   - Benefit gap: is the buyer outcome concrete?
   - Trust gap: does it reduce risk before click?
   - Difference gap: does it avoid looking like the rest of the shelf?
   - Focus gap: does the product beat background, labels, and props?
   - Platform gap: does the style match where it will be shown?
5. Produce a minimum viable change plan:
   - Fix now: 1-3 edits that remove the biggest click blockers.
   - Test next: 2-3 variants with one clear hypothesis each.
   - Rebuild later: deeper reshoot, copy, proof, or sequence changes.
6. Offer optional outputs only when useful: designer brief, AI image prompt, 1-5 image sequence, A/B test plan, or share-ready case summary.

## Output Rules

- Be concrete enough for a designer or operator to act: placement, scale, crop, copy length, color role, proof asset, and safe area.
- Separate facts, visual observations, inferences, and suggestions.
- Prefer "test this hypothesis" over "this will improve CTR".
- For formal reports, use neutral metadata only: material source, platform scene, generated time, assumptions, and limits.
- For public articles or share packages, lead with the result and usage value. Keep commands, validation logs, blocked attempts, and regeneration notes in README or handoff docs.
- Never reuse source-branded report headers, examples, names, or footers from external skill packages.

## Reference Routing

- For input routing and evidence labels, read `references/input-router.md`.
- For the click-gap framework and scoring, read `references/diagnosis-framework.md`.
- For platform-specific notes, read `references/platform-playbook-cn.md`.
- For report, quick diagnosis, designer brief, prompt, and test formats, read `references/output-contract.md`.
- For AI prompt and designer handoff details, read `references/prompt-and-brief.md`.
- For public sharing, article packaging, and source-neutral release checks, read `references/share-guidance.md`.

Read only the references needed for the user's requested output.
