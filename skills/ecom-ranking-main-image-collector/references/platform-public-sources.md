# Platform Public Source Playbook

Use this reference when choosing public sources for category main-image collection.

## Source Priority

1. Public official ranking pages visible without login.
2. Public category pages with visible ordering labels such as 销量、热卖、榜单、排行榜、人气.
3. Public search pages with sales/hot sorting parameters.
4. Reputable public third-party lists that link to products and show product images.
5. User-saved HTML from a page they can legally view, with no cookies or private account data included.

## Platform Notes

- `jd`: direct HTTP requests to search pages can trigger verification even when the same page is visible in a normal browser. If direct requests are blocked, use the semi-automatic visible-browser route: open the public search page, confirm the product grid, extract visible product cards, then feed saved HTML/card data to the collector. Label the result as search-derived unless the page says ranking.
- `taobao` / `tmall`: public search pages may block automated fetches or require verification. Do not bypass. Use public URLs, browser-visible saved HTML, or ask for exported HTML.
- `pdd`: public web pages may be limited. Use only pages visible without login or user-provided saved HTML.
- `douyin`: many commerce pages are app/session driven. Prefer public web pages or user-provided saved HTML; do not use logged-in app state.
- `mixed`: use only when the user wants platform comparison or when one platform cannot provide enough public samples.

## Search Phrases

For web discovery, combine the category with:

- `<类目> 销量排行榜 主图`
- `<类目> 热卖榜 商品`
- `<类目> 京东 销量 排行`
- `<类目> 天猫 热卖 榜单`
- `<类目> 商品榜单`

When using a search engine or browser, keep the source list short and visible in the final report. The collector script can then download and normalize images from the chosen public URLs.

## Blocked Source Handling

Record a blocked source when a response contains login walls, CAPTCHA, risk-control notices, empty script shells, or no product images. Do not retry with private cookies or anti-detection. Try another public source, reduce scope, or ask for saved HTML.

## Known Collection Pitfalls

- JD search direct `curl`/HTTP may return verification while Chrome can show the product grid. Treat this as a route failure, not a reason to bypass verification.
- Product cards may show lazy-load placeholders in `img.src`. Also inspect card links, embedded JSON, and query parameters such as `imgUrl`, `image`, `mainPic`, and `pic`.
- JD image URLs often contain tiny thumbnail prefixes such as `s80x80_` under `n7`; normalize them to larger product images before analysis. Avoid `shaidan` buyer-show thumbnails for main-image samples.
- JD public ranking/price pages can include shop logos, brand banners, certificates, ads, and other large non-product images. Always generate a contact sheet, manually mark keep/remove, and move abnormal images into evidence instead of using them for visual-rule analysis.
- Some contact sheets will contain one or two blank/abnormal samples on the first pass. Keep them in the test record, then remove or replace them before article evidence images.
- Browser scroll gestures can time out. Prefer page JavaScript scrolling and then re-extract visible cards.
- A single platform sample supports “platform + category front-rank image patterns”, not “whole-network explosive image rules”.
