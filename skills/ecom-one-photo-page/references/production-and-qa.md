# Production and QA

Use this reference only when the user asks for actual images or when generated outputs must be reviewed.

Read [product-consistency.md](product-consistency.md) before production.

## Production Gate

Do not generate images until `product-card.md` and `page-map.md` are coherent. Planning permission does not imply permission to generate a large image batch.

When production is requested:

1. freeze the Product Identity Card, target SKU, intended count, source roles, and consistency route;
2. include the local identity anchor in every route-G generation call;
3. for route H, generate a scene plate and composite the approved original product pixels afterward;
4. generate the hero first and inspect product identity and count;
5. generate one evidence/detail image and inspect fragile features;
6. continue the remaining batch only after both pilot checks pass;
7. use the smallest set of references needed to lock the target SKU;
8. never use mixed-SKU, seller, or competitor images as product identity references.

If the generator cannot preserve a requested unseen angle, downgrade that screen instead of repeatedly hallucinating it.

## Retry Boundary

Retry an image at most twice for the same failure. On repeated failure:

- simplify the composition;
- return closer to the anchor angle;
- remove unsupported detail or text;
- generate a clean plate; or
- switch from route G to route H when an acceptable original-pixel cutout is available; or
- deliver the prompt with a documented limitation.

Do not burn repeated generations trying to force structure that one photo cannot prove.

## Visual QA

Reject an image when any critical issue appears:

- target SKU or intended product count changes;
- product silhouette, color blocking, proportions, parts, label, or logo drift;
- invented mechanism, texture, accessory, parameter, certification, or performance result;
- mixed SKU identity;
- copied seller/competitor page composition or brand assets;
- unreadable or incorrect Chinese that changes the claim;
- duplicate or malformed product geometry.

Use three severity levels:

- `critical`: wrong SKU/count, reference product residue, silhouette or key-part change, missing or invented accessory, logo/label corruption that changes identity. Reject.
- `major`: material-looking texture drift, hardware change, unstable proportions, unsupported angle, or visible cutout/rectangular replacement artifact. Reject or switch route.
- `minor`: scene styling, shadow softness, prop placement, or other non-identity polish. Correct only when it improves the page job.

Provider or model technical success is never an identity pass. Record `pending-qc` until the rendered pixels are inspected.

Check the complete pack for:

- unique screen jobs and visibly distinct compositions;
- consistent product identity, palette, light direction, and type system;
- no more than two uses of the same hero framing;
- text hierarchy that remains readable at marketplace size;
- correct aspect ratio and complete file naming;
- a clear progression from recognition to benefit, explanation, evidence, scene, and choice.

## Output Structure

```text
<job>/
  input/
    anchor.<ext>
  strategy/
    product-card.md
    page-map.md
  prompts/
    main/01-hero.md ... 06-summary.md
    detail/01-value.md ... 06-summary.md
  renders/
    main/
    detail/
  preview/
    main-contact-sheet.jpg
    detail-long-preview.jpg
  qa/
    qa-report.md
    validation.json
  job.json
```

For `plan` mode, `renders/` and `preview/` may remain absent. State that the pack contains prompts rather than images.

## QA Report Minimum

Record:

```text
mode:
anchor_used:
primary_purchase_reason:
generated_count:
accepted_count:
rejected_or_downgraded:
identity_status:
inventory_status:
consistency_route:
claim_status:
distinctness_status:
text_status:
remaining_limitations:
```
