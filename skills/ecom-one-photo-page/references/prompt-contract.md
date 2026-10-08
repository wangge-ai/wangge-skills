# Prompt Contract

Write one independent prompt file per image. The prompt must work without relying on another prompt's context.

## Required Sections

Use these exact section labels so the pack can be validated:

```text
PRODUCT_LOCK
CONSISTENCY_ROUTE
SCREEN_JOB
BENEFIT_AND_PROOF
COMPOSITION
ALLOWED_COPY
EVIDENCE_LIMITS
NEGATIVE_CONSTRAINTS
OUTPUT_SPEC
```

## Section Rules

### PRODUCT_LOCK

Use these explicit fields:

```text
identity_anchor:
target_sku:
target_instance_count:
locked_visible_attributes:
fragile_identity_details:
unseen_or_unreadable:
```

Describe only stable product identity: silhouette, color blocking, proportions, visible parts, texture, labels, and included accessories. State that the anchor controls product identity only; its background, crop, typography, and layout must not be copied. If a style reference exists, say explicitly that it has no authority over SKU, product count, packaging, logo, label, or product color.

### CONSISTENCY_ROUTE

Choose one route defined in [product-consistency.md](product-consistency.md):

- `G close-angle generation` for low-fragility images near the visible angle;
- `H original-pixel hybrid` when the product, packaging, label, logo, or exact count must remain strict;
- `D downgrade-or-more-views` when the requested image exposes unseen construction or cannot preserve identity honestly.

For route H, the generation prompt creates the scene plate and product-safe placement; the original product pixels are composited afterward. Do not ask the model to invent a substitute product.

### SCREEN_JOB

State the buyer question and the single job of this image. Do not list multiple conversion tasks.

### BENEFIT_AND_PROOF

Write the primary message and the visible or user-provided evidence supporting it. Label a creative scene as a proposal when it is not a product fact.

### COMPOSITION

Specify camera angle, product scale, placement, scene, lighting, palette, text-safe area, and the composition family. Create an original layout. Do not mention the position of elements in seller or competitor images.

If a user-approved style reference is present, list only the transferable composition properties. Explicitly exclude its product, brand, logo, packaging, claims, slogans, and readable text.

### ALLOWED_COPY

Limit Chinese text:

- headline: ideally 4-10 Chinese characters;
- support copy: ideally no more than 18 Chinese characters;
- labels: no more than three, each ideally 2-6 characters.

Ask for large readable Chinese. If reliable Chinese rendering is not available, generate a clean plate with reserved text-safe areas and provide the overlay copy separately.

### EVIDENCE_LIMITS

List facts that may appear and missing claims that must not appear. Include screen-specific limitations, such as no internal structure or exact size.

### NEGATIVE_CONSTRAINTS

Block product drift and common generation errors: recoloring, redesigning, changing proportions, adding or removing parts, changing SKU, changing the intended count, duplicating the product, retaining a reference product, rewriting packaging text, inventing packaging or logos, copying seller composition, adding watermarks, and creating unsupported claims.

### OUTPUT_SPEC

Specify channel, aspect ratio, intended pixel width, style, and whether the result needs text or a clean plate.

## Product Lock vs. Creative Direction

The most important sentence in each prompt is conceptually:

```text
Use the anchor image only to preserve the product; create a new composition from the screen job below.
```

Do not describe the anchor background as part of the product. Do not preserve existing promotional labels, decorative props, page layout, or typography unless the user explicitly identifies them as brand assets.

## One-Photo Limit

When a prompt asks for a new angle, keep it close enough to the visible view to preserve identity. If the requested shot would reveal unseen construction, replace it with a crop, annotation, silhouette, scene, or handling composition.
