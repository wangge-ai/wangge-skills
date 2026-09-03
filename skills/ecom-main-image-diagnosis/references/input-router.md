# Input Router

## Evidence Labels

Use these labels in every formal report:

| Label | Meaning |
|---|---|
| Visible | Directly seen in an image, screenshot, page render, or table |
| Provided | Stated by the user or present in supplied files |
| Inferred | Reasonable judgment from visible material |
| Missing | Needed for a stronger answer but unavailable |
| Blocked | A link or page could not be accessed without login, verification, or unsupported interaction |

Do not blur these labels. If the product material, price, sales volume, CTR, or platform performance is not visible or provided, mark it as missing or inferred.

## Input Routes

### Main Image Only

Use for:

- first-screen clarity
- product recognizability
- click hook
- visual focus
- simple redesign directions

Avoid:

- platform ranking claims
- competitor position claims
- CTR/CVR diagnosis without data

### Search-Result Screenshot

Use for:

- shelf contrast
- visual crowding
- price and offer context when visible
- title-image mismatch
- competitor visual zones

Always note:

- screenshot platform
- visible competitor count
- whether the user's product is identifiable

### Product-Page Screenshot

Use for:

- main image plus title, price, SKU, trust badges, reviews, and visible modules
- consistency between title promise and image promise
- missing proof or unclear offer

Avoid reading backend metrics into the page.

### Image Set

Use for:

- 1-5 image sequence task planning
- repetition detection
- whether each image has a conversion job

Do not force every category into the same sequence. Assign jobs based on category, platform, and buyer risk.

### Competitor Images

Use for:

- visual crowding map
- click hook comparison
- category visual cliches
- open space for differentiation

Never ask the model to copy competitor composition, brand identifiers, packaging, models, slogans, or exact text.

### Product Link

Try public reading or rendering only. If blocked by login, verification, risk control, or empty shells, record the blocked state and ask for a screenshot, saved HTML, or product asset folder.

For Taobao/Tmall links, treat the link as an acquisition probe, not as guaranteed evidence. Common blocked outputs include login jump pages, `x5sec` / risk-control pages, `____tmd____` redirects, empty mobile shells, and mtop responses that point to verification pages. In those cases:

1. Label the link route as `Blocked`.
2. Do not write visual diagnosis or score the main image.
3. Ask for one of: product-page screenshot, search-result screenshot, uploaded main image, saved HTML from the user's visible browser, or explicit permission to inspect a user-controlled logged-in browser.
4. If only the URL is available, return a test note instead of a diagnosis report.

### Main Image + Detail Five-Image Set

Use for:

- combined main-image click diagnosis and detail-page first-five-image conversion diagnosis
- separating "click job" from "conversion support job"
- checking whether the detail page carries through the same result, mechanism, proof, offer, and scene promised by the main image
- producing designer execution notes for both first-screen main images and the first 5 detail-page images

Recommended input modes for public/share usage:

1. Auto acquisition: the user provides product links, and the workflow tries to collect public main images and detail images. If blocked by login, verification, risk control, or empty shells, mark the acquisition route as `Blocked`.
2. User-provided assets: the user provides 1-5 main images, 5 detail-page images/screenshots, product title, price band, platform, and any claim sources.

Always separate the report into:

- Main image: visibility, first-glance understanding, click promise, proof hint, offer hook.
- Detail first 5 images: result confirmation, mechanism explanation, proof/source, offer/SKU decision, scene/usage/persona support.

Do not treat the first 5 detail images as five more main images. Their job is to continue the buyer's decision after the click.
