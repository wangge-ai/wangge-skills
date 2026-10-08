---
name: ecom-one-photo-page
description: Turn one clear ecommerce product photo plus a short description into
  an identity-locked product brief, an original 1+5 main-image plan, a detail-page
  flow, generation prompts, and optionally visually checked images. Use for low-input
  Chinese ecommerce page production; do not use for product-link collection, competitor
  crawling, review mining, or merely restyling an existing full page.
license: MIT
---

# Ecom One Photo Page

Create a useful first version from minimal input without pretending that one photo proves unseen structure or performance.

## Route the Request

- If the user asks for planning, copy, page structure, or prompts, use `plan` mode and do not generate images.
- If the user explicitly asks to generate, produce, render, or make the images, use `produce` mode after the plan is internally coherent.
- If the user provides an existing page for review, diagnose it only when the request is about the one-photo workflow; otherwise use the relevant ecommerce review skill.

Read the references needed for the selected work:

- For minimum intake, evidence states, selling-point choice, and low-input fallbacks, read [references/decision-engine.md](references/decision-engine.md).
- For the 1+5 main-image sequence and detail-page decision flow, read [references/page-architecture.md](references/page-architecture.md).
- For reference roles, SKU/count locking, consistency routing, and identity QA, read [references/product-consistency.md](references/product-consistency.md).
- For observable category cues and safe screen substitutions, read [references/category-routing.md](references/category-routing.md) when category-specific guidance would help.
- For claim classes and short Chinese copy, read [references/copy-and-claims.md](references/copy-and-claims.md) when writing page copy.
- For writing independent generation prompts, read [references/prompt-contract.md](references/prompt-contract.md).
- For actual image production, folder delivery, and visual QA, read [references/production-and-qa.md](references/production-and-qa.md).
- When the user asks where this method came from or the Skill is being revised, read [references/method-provenance.md](references/method-provenance.md).

## Minimum Input

One clear product photo is enough to start. A short product description is helpful but not mandatory when the category is obvious. Platform, audience, price band, style, and verified claims are optional.

Do not interrogate the user for optional fields. Ask only when:

1. the image does not identify the product;
2. multiple products or SKUs make the target ambiguous;
3. the requested result depends on an unseen structure or exact claim; or
4. the image is too poor to preserve product identity.

Otherwise create a version-one proposal immediately and label assumptions.

## Required Workflow

1. Inspect the anchor photo and build one `Product Identity Card`: target SKU, intended product count, visible shape, color blocking, proportions, parts, texture, labels, accessories, fragile details, and unseen boundaries.
2. Assign every supplied image one source role. Keep product identity authority separate from style, fact evidence, seller pages, and mixed-SKU material.
3. Separate `visible_facts`, `user_provided_facts`, `proposals`, and `missing_or_unverified`.
4. Run the product-consistency preflight and select a route: close-angle generation, original-pixel hybrid composition, or downgrade/request-more-views.
5. Choose one primary purchase reason by combining a visible difference, a buyer benefit, an evidence cue, and a plausible scene. Keep secondary points subordinate.
6. Plan the 1+5 main images and detail-page screens by buyer decision role, not by copying source layouts.
7. Compile one independent prompt per image. Every prompt must carry the same SKU/count lock and identity constraints but a different screen job and composition.
8. In `produce` mode, generate and inspect a hero plus one evidence screen before continuing the batch. Reject identity drift before assembling previews.

## Non-negotiable Invariants

- The product photo constrains what the product is; it does not constrain page composition or visual style.
- Product identity authority, creative authority, and factual authority are separate. A style reference never becomes a product reference.
- Lock the target SKU and intended visible product count before prompting. Do not let a reference layout silently duplicate, remove, or substitute products.
- One screen performs one buyer-decision job. Repeated hero poses with different text do not count as different screens.
- Never invent a back view, internal layer, exploded structure, texture, mechanism, accessory, specification, certification, performance level, or use result that the input does not support.
- Replace an unsupported structure or proof screen with a visible-feature, usage-logic, scale, care, or scene screen.
- Claims from the user may be used as `user_provided_facts`; claims merely visible in third-party marketing images remain unverified until the user confirms them.
- Existing seller or competitor pages may provide facts or category context, but their composition, slogans, brand assets, and visual system are not generation references.
- A prompt can request consistency but cannot prove it. Fine packaging text, logos, product count, and fragile geometry remain output-level QA items; use original-pixel composition when those details are business-critical.
- Do not require competitor collection, reviews, keywords, or a product link for the quick workflow.

## Default Delivery

Unless the user chooses another location, create the job under:

```text
./outputs/ecommerce\one-photo-page\<product>_<YYYY-MM-DD>\
```

Use `scripts/init_job.py` when a local anchor path is available. Deliver:

```text
input/
strategy/product-card.md
strategy/page-map.md
prompts/main/
prompts/detail/
renders/main/          # produce mode only
renders/detail/        # produce mode only
preview/               # produce mode only
qa/qa-report.md
job.json
```

For a standard full pack, create six main-image prompts and six detail-page prompts. Honor a shorter user-requested pack.

Run `scripts/validate_pack.py` `<job-directory>` before handoff. A valid folder structure does not replace visual QA for generated images.

## Completion Boundary

State whether the delivery is `plan only` or `produced and visually checked`. Do not describe prompts as completed images. Report any screen that was downgraded because one-photo evidence was insufficient.
