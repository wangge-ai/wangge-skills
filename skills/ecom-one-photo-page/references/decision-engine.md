# One-Photo Decision Engine

Use this reference whenever the input is one product photo or one photo plus a short description.

## 1. Build the Input Card

Record only what is available:

```text
anchor_image:
product_name:
user_description:
target_sku: optional
target_instance_count: optional
platform: optional
audience: optional
price_band: optional
style_direction: optional
verified_claims: optional
```

Infer an obvious product name instead of asking. Treat omitted platform as `domestic ecommerce general`, omitted audience as `not specified`, and omitted style as a proposal derived from product appearance. These defaults are creative settings, not product facts.

When one clearly isolated product is visible and the user has not requested a group composition, propose `target_instance_count: 1`. Mark it as a planning decision, not a fact about the seller's inventory. If multiple products, variants, boxes, bundles, or accessories make the target ambiguous, stop and ask which SKU and count the page should sell.

## 2. Separate Evidence States

Create four lists before planning:

- `visible_facts`: directly visible in the anchor image.
- `user_provided_facts`: explicitly stated by the user, including true selling points or specifications.
- `proposals`: audience, benefit wording, scene, mood, or positioning proposed by Codex.
- `missing_or_unverified`: unseen angles, internal structure, exact materials, dimensions, performance, certification, inventory, price, and other unsupported claims.

Do not let `proposals` leak into factual labels or diagrams. A proposal may guide scene and tone when it does not assert an unknown product property.

## 3. Create the Product Identity Card

Record the minimum identity and inventory that must remain stable across every image:

- target SKU or the narrowest honest visible description;
- intended visible product count;
- silhouette and overall proportions;
- primary and secondary colors;
- visible parts and their relationships;
- texture or finish only when visible;
- buttons, handles, closures, edges, seams, hardware, labels, and logos;
- included accessories that are clearly present;
- fragile identity details most likely to drift, such as a ring handle, hinge, cap, printed label, buckle, panel edge, button cluster, or color boundary;
- unseen sides, hidden construction, and text that cannot be read reliably;
- features that must not be added or transformed.

The identity card never contains page layout, background, typography, slogan, or competitor style. Those belong to creative composition. A camera angle may be recorded only as an anchor limitation, not as a mandatory page layout.

## 4. Select the Primary Purchase Reason

Generate up to five candidates from visible differences and user-provided facts. Score each candidate from 0 to 3 on:

| Dimension | Question |
|---|---|
| Difference | Is it visually distinguishable from a generic category item? |
| Benefit | Can a buyer understand the practical or emotional value? |
| Evidence | Can the image or user statement support it? |
| Scene | Can it be shown in a believable use context? |
| Claim risk | Does it require proof that is missing? Subtract this score. |

Use the highest defensible candidate as the primary purchase reason. A useful expression is:

```text
visible difference + buyer benefit + visible or provided proof cue
```

Example pattern:

```text
环扣手柄 + 随包挂放更顺手 + 白底图中可见环扣结构
```

Do not choose a generic style adjective when a functional visible difference exists. Do not force a functional promise when only appearance is visible; appearance-led positioning is valid.

## 5. Low-Input Fallbacks

When only one view exists:

- Use the same verified silhouette in new backgrounds and plausible scenes.
- Create detail focus by cropping or magnifying visible regions, not by hallucinating a macro texture.
- Use callouts on visible parts instead of exploded views.
- Use relative scale only when a familiar hand or prop can be introduced without implying an exact size.
- Replace unseen back or internal screens with scene, styling, storage, care, pairing, or visible-feature screens.
- Keep claims soft and observable: `轮廓清楚`, `环扣可挂`, `细节看得见`.

## 6. Source Roles and Anti-Copy Rule

Classify every supplied image as one of:

- `product_anchor`: identity reference;
- `fact_evidence`: supports a visible or stated fact;
- `style_reference`: used only when the user explicitly asks for that visual direction;
- `exclude_from_generation`: seller page, competitor creative, review image, screenshot, or mixed-SKU material that should not guide composition.

Never use a seller or competitor detail page as both product anchor and composition reference. If a screenshot contains the product, extract or select the cleanest product region and write a new composition from the page architecture.

After assigning roles, run the preflight in [product-consistency.md](product-consistency.md). Do not compile prompts while SKU, instance count, reference authority, or consistency route remains ambiguous.
