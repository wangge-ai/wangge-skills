---
name: wechat-cover-maker
description: Create WeChat Official Account article cover images from a user-provided
  title/text and visual prompt. Use when the user asks for 公众号封面、微信公众号首图、article cover、WeChat
  cover, or wants exact Chinese text placed into a generated cover image while they
  provide the image content prompt.
license: MIT
---

# WeChat Cover Maker

## Core Rule

Generate the cover background from the user's visual prompt without title text, then add the user's exact title/text locally with `scripts/render_cover_text.py`. Do not rely on an image model to render important Chinese text.

Default cover format: WeChat Official Account article cover, `900x383`, ratio about `2.35:1`.

Default batch count: `3` final cover images. Use 3 images for future cover-generation requests unless the user explicitly overrides this preference.

Default output root: `./outputs/05_公众号与内容项目\06_封面与设计\公众号封面项目`. The built-in image generation tool may still create its raw cache under `$CODEX_HOME\generated_images`; copy selected backgrounds and all final reusable covers into this cover project folder before finishing. Do not create new `wechat-cover-*` folders directly under `D:\codex`.

Use clear subfolders for every batch:

- `final-with-title\`: final covers with the exact rendered title text. These are the user-facing deliverables.
- `backgrounds\`: generated no-text backgrounds kept for reuse.
- `prompts\`: prompt and run notes for the batch.
- `preview-all-with-title.jpg`: contact sheet made from final covers only.

## Workflow

1. Extract two inputs from the user:
   - `title`: the exact text to place on the cover.
   - `visual_prompt`: the requested image content, style, mood, and objects.
2. If either input is ambiguous, infer conservatively from the request. Ask only when the title or visual prompt cannot be identified.
3. Use the built-in `image_gen` tool to generate one or more background images:
   - Generate 3 backgrounds by default.
   - Prompt for a clean `2.35:1` WeChat cover background.
   - Include the visual content the user requested.
   - Explicitly say: no text, no letters, no watermark, leave title-safe negative space.
   - Prefer leaving text space on the left unless the user asks otherwise.
4. Copy selected generated backgrounds into `./outputs/05_公众号与内容项目\06_封面与设计\公众号封面项目\<descriptive-folder>\backgrounds`.
5. Run `scripts/render_cover_text.py` to create the final cover with exact text.
   - Save final covers into `./outputs/05_公众号与内容项目\06_封面与设计\公众号封面项目\<descriptive-folder>\final-with-title`.
   - Save the prompt/run record into `prompts\prompt-and-qc.md`.
   - Name final files clearly, such as `final-01-with-title.jpg`.
   - Preserve the right-side visual subject. For left-position titles, keep the text block around `--block-ratio 0.5` or lower, and rerender if the panel overlaps important icons, product visuals, faces, app cards, or other focal elements.
   - Make the title feel integrated with the image, not pasted on. Use the default soft panel style, subtle shadow/stroke, and low-opacity backing. Use the stronger `--panel-style card` only when the title is otherwise unreadable.
6. Inspect the final image when possible. Check that the title is readable on mobile-size thumbnails and not clipped.
7. Produce 3 final covers by default, not just raw backgrounds.

## Background Prompt Pattern

Use this pattern and adapt it to the user's visual prompt:

```text
Create a WeChat Official Account article cover background, 2.35:1 horizontal composition, suitable for 900x383.
Visual prompt: <user visual prompt>.
Leave a clean title-safe area on the <left/center/right> with enough negative space for large Chinese headline text.
No text, no letters, no numbers, no logos, no watermark.
Professional editorial cover design, strong focal point, high contrast, clean composition.
```

When the user asks for a GitHub repository icon or another recognizable symbol, include it in the background prompt as a visual icon element, but still tell the model not to render article-title text.

## Text Rendering

Use the script:

```powershell
python scripts/render_cover_text.py `
  --background <background.png> `
  --title "<exact title>" `
  --out <final-cover.png>
```

Useful options:

```powershell
--position left|center|right
--theme auto|light|dark
--accent "#22c55e"
--kicker "AI 电商实战"
--no-panel
--size 900x383
--block-ratio 0.5
--panel-style soft|card
```

Defaults are tuned for WeChat covers:

- `--position left`
- `--theme auto`
- `--size 900x383`
- `--block-ratio 0.5`
- `--panel-style soft`
- A soft low-opacity backing is used behind text for readability. Avoid hard card-like blocks unless needed for contrast.

## Output Guidance

- For preview-only requests, show the final generated covers inline.
- For reusable/project-bound covers, save final covers, copied backgrounds, and contact sheets under the default cover folder, then report paths.
- In the final response, point first to `final-with-title`, because those are the images with text. Mention that `backgrounds` are intentionally text-free.
- Keep generated backgrounds and final covers non-destructive. Do not overwrite unless the user asks.
- If the user asks for exact text changes after seeing a cover, reuse the same background and rerun only the text-rendering script.
## Local HTML Cover Fallback

If image generation produces unrelated subjects, wrong text, random English, anatomy diagrams, animals, fake logos, distorted UI, or anything unrelated to the requested article theme, stop using that generated image for the cover.

For covers with important Chinese title text, a local HTML/CSS cover is an acceptable and often safer fallback:

1. Create `cover-html/cover-01.html`, `cover-02.html`, `cover-03.html`.
2. Set canvas to `900x383`.
3. Render the exact Chinese title directly in HTML.
4. Use short labels from the article as chips/cards.
5. Export with Playwright screenshot into `final-with-title/`.
6. Save notes in `prompts/prompt-and-qc.md`.

The generated background can be abandoned if it is off-topic. Do not try to rescue a wrong image by adding correct text on top.

For GitHub/ecommerce cover images, prefer concrete local visual metaphors:

- repo cards
- dashboard tiles
- code window
- product grid hints
- shopping cart or order flow hints
- short repo labels

Do not include author bars, public-account metadata, or backend article title areas in the cover.
