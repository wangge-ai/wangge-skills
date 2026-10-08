# Product Consistency

Use this reference whenever prompts or images are produced from a product photo.

## 1. Separate Authorities

- `identity_anchor`: the only image allowed to define the target SKU, product pixels, color blocking, parts, label, logo, and included accessories.
- `fact_evidence`: supports a visible or user-confirmed fact but does not define page composition.
- `style_reference`: may guide composition, camera logic, background, lighting, material mood, and text-safe regions only when the user requests it.
- `exclude_from_generation`: seller pages, competitor creatives, screenshots, reviews, mixed-SKU images, or low-quality material that could contaminate identity.

Never let one reference silently carry both product-identity and style authority. A style reference contributes no authority over product, brand, packaging, SKU, count, claims, slogans, or readable text.

## 2. Product Identity and Inventory Lock

Freeze these before prompt compilation:

```text
identity_anchor:
target_sku:
target_instance_count:
locked_visible_attributes:
fragile_identity_details:
included_accessories:
unseen_or_unreadable:
```

The intended product count is a composition decision. Do not infer a bundle, duplicate a product to match a layout, or remove an included item without explicit support.

## 3. Preflight

Block production when any condition is unresolved:

- target product, SKU, bundle, or instance count is ambiguous;
- the anchor mixes variants or contains a reference product that cannot be separated;
- a requested angle exposes unseen construction or requires an invented back, interior, mechanism, texture, or accessory;
- style instructions conflict with locked color, proportions, parts, packaging, label, or count;
- the anchor is too small, blurred, occluded, or cropped to preserve a business-critical feature;
- a fact or claim has no visible or user-provided authority.

Warnings that require output-level QA:

- fine packaging text and small logos;
- exact product count, overlap, or repeated instances in a generative composition;
- thin geometry, transparent edges, spokes, straps, hinges, handles, or other fragile parts;
- Chinese text rendered inside the generated image.

## 4. Select a Consistency Route

### G — Close-angle generation

Use when product identity is visually simple, the requested view stays close to the anchor, and small text is not business-critical. Include the identity anchor in every call and keep target count explicit.

### H — Original-pixel hybrid

Use when exact packaging, label, logo, color boundaries, geometry, or product count matters. Generate the background or scene plate without a substitute product, preserve a product-safe placement, then composite an approved cutout of the original product. Add Chinese copy as a separate deterministic layer when possible.

If the anchor has a rectangular background and cannot be cleanly isolated, do not pretend route H is available. Request a cleaner white-background or transparent image, or downgrade the layout.

### D — Downgrade or request more views

Use when the requested result depends on unseen construction or a materially different angle. Replace the screen with a visible-part callout, crop, silhouette, handling scene, placement scene, care screen, or other supported decision role. Ask for more photos only when that missing view materially changes the result.

## 5. Output Identity QA

Compare each result directly with the identity anchor.

- `critical`: wrong SKU/count, reference product residue, changed silhouette or key part, missing/invented accessory, identity-changing logo or label corruption. Reject.
- `major`: unstable proportions, hardware/texture change, unsupported new angle, malformed thin geometry, rectangular replacement trace, or obvious cutout mismatch. Reject or change route.
- `minor`: scene styling, shadow softness, prop position, or other non-identity polish. Correct only when useful.

Inspect the hero and one evidence screen before producing the rest. A prompt, model status, file download, or correct dimensions do not prove product consistency. Keep every result `pending-qc` until visual inspection is complete.
