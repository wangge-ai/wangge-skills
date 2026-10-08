# Page Architecture

Plan by buyer decision role. The sequences below are defaults, not fixed templates; substitute roles when the evidence cannot support a screen.

A standard page needs an explanation role and a product-evidence role; it does not automatically need an exploded structure image or synthetic macro. Use visible-part annotation and honest crops when one photo cannot support more.

## 1+5 Main-Image Sequence

| No. | Buyer decision | Default image job | Acceptable substitute |
|---:|---|---|---|
| 1 | What is it and why click? | Product-first hero with one primary purchase reason | Appearance-led hero |
| 2 | What changes for me? | Benefit or natural use scene | Scale or handling scene |
| 3 | Why does it work? | Visible mechanism or usage logic | Visible-feature callout |
| 4 | What proves it? | Detail evidence | Honest crop of a visible detail |
| 5 | Where does it fit? | One or several coherent scenes | Styling, pairing, storage, or placement |
| 6 | How do I choose? | SKU, included parts, summary, or trust cue | Single-SKU summary or care guidance |

Main images are normally square. Each image needs one headline, at most one short support line, and no more than three short labels.

## Six-Screen Detail Flow

| No. | Buyer decision | Default screen job |
|---:|---|---|
| 1 | Why stay on the page? | Restate the primary purchase reason with a new composition |
| 2 | When would I need it? | Pain-point or use-context scene without exaggerated failure drama |
| 3 | What is the visible solution? | Feature-to-benefit explanation or usage logic |
| 4 | Can I trust the product itself? | Visible detail, build, control, edge, closure, texture, or label |
| 5 | Does it fit my life? | Scene range, styling, placement, pairing, or handling |
| 6 | What should I remember or choose? | Overall summary, SKU choice, included parts, care, or next action |

Detail screens are normally portrait 3:4 and suitable for a 750px-wide domestic ecommerce slice.

## Dynamic Substitution Rules

- No structural evidence: replace structure with a visible-part annotation or use-logic screen.
- No credible detail evidence: use an honest crop, silhouette comparison, or handling screen; do not fabricate texture.
- No variants: do not invent colors or SKUs; use a single-product summary.
- No dimensions: omit exact measurements; use no scale claim unless the scene visibly provides one.
- No certification or test evidence: use no badge, laboratory scene, ranking, seal, or data chart.
- No target audience: use neutral hands, partial figures, or object-only scenes instead of assigning gender, age, profession, or condition.
- Category cues may suggest useful questions but never create facts. Use [category-routing.md](category-routing.md) for observable cues and category-specific traps.

## Distinctness Gate

Before writing prompts, check the page map:

1. Every screen has a unique `buyer_question` and `screen_job`.
2. The same hero framing appears no more than twice across the whole pack.
3. At least three composition families are used, such as hero, lifestyle, annotation, macro/crop, sequence, grid, or choice.
4. A repeated product pose must serve a different proof purpose, not merely carry new text.
5. The first three images progress from recognition to benefit to explanation; they must not be three versions of the same poster.

## Page-Map Record

Create one record per image:

```text
id:
channel: main | detail
buyer_question:
screen_job:
primary_message:
proof_used:
composition_family:
headline:
support_copy:
facts_used:
proposal_used:
risk_notes:
```
