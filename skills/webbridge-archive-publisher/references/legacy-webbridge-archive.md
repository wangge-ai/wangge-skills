---
name: webbridge-archive-publisher
description: Use when the user gives a URL, website, Feishu/Lark document/wiki link, logged-in page, or browser-only page and asks Codex to crawl, archive, export, package, or turn it into a high-quality readable/shareable HTML, Markdown, screenshots, or knowledge-base bundle using Kimi WebBridge.
---

# WebBridge Archive Publisher

把一个真实浏览器可访问的页面或站点，归档成“能读、能分享、能追溯”的资料包。

This skill sits on top of Kimi WebBridge. Use the real browser for content that needs the user's current login session, client-side rendering, lazy-loaded images, Feishu/Lark docs, dashboards, or pages that ordinary HTTP fetch cannot read correctly.

## When To Use

Use this skill when the user says things like:

- 给你一个链接，帮我爬下来
- 把这个网站/飞书文档整理成 HTML
- 导出成可以分享的单文件
- 本地图片别人看不到，帮我内嵌进去
- 这个页面要保留原貌、截图、正文、JSON
- 用 Kimi WebBridge 操作浏览器抓取
- 登录态页面、飞书知识库、飞书文档、网页资料归档

Do not use this skill for ordinary public pages where a simple HTTP request already provides clean article HTML, unless the user explicitly wants browser screenshots or original visual layout.

## Output Standard

Default output root should be outside C drive when possible:

`./outputs/webbridge-archive-{yyyyMMdd-HHmmss}`

Each archive should contain:

- `reader.html`: local readable HTML with left navigation, original long-image view, copyable text, search, screenshot backup.
- `{title}-可分享单文件.html`: a single HTML with images embedded as data URIs for sharing.
- `readable/clean-markdown/`: one clean UTF-8 Markdown file per page.
- `readable/{title}合集.md`: combined Markdown.
- `pages/*.json`: structured source data, used for regeneration/import.
- `pages/*.md`: per-page Markdown beside the JSON.
- `screenshots/`: viewport screenshot backups when screenshots are requested.
- `stitched-hq/`: PNG long images stitched from screenshots.
- `manifest.json`: discovered page list.
- `crawl-results.json`: extraction result and failures.
- `screenshot-results.json`: screenshot result and failures when screenshots are requested.
- `README.md`, `README_使用说明.md`, `VERIFICATION.md`: human-facing index, usage, and validation record.

## Workflow

1. Clarify only if necessary:
   - If the user gives one URL, proceed.
   - If scope is ambiguous on a large site, pick a conservative default: current page plus clearly visible child pages. Say the boundary.
   - If the page requires manual login/captcha/permission, ask the user to open/login manually, then continue with `find_tab active:true` or navigate after login.
2. Use Kimi WebBridge with one stable session name for the whole task.
   - On Windows, every WebBridge command must be sent through a UTF-8 JSON temp file and `curl.exe --data-binary @file`.
   - Never pipe non-ASCII JSON directly through PowerShell.
3. Discover pages:
   - For Feishu/Lark wiki: collect sidebar tree nodes with wiki tokens.
   - For a single document/article: archive the current page only.
   - For ordinary sites: do not spider the whole domain unless the user explicitly asks.
4. Extract structured text:
   - Scroll the document container from top to bottom.
   - Collect readable lines after lazy content loads.
   - Save UTF-8 Markdown and JSON.
5. Capture visual evidence:
   - Use viewport screenshots for pages where original layout matters.
   - For Feishu/Lark docs, crop fixed sidebar/topbar when stitching long images.
   - Prefer PNG for stitched long images; avoid second-generation JPG compression.
6. Build readable outputs:
   - Generate `reader.html`.
   - Generate shareable single-file HTML if the user needs to send it to others.
   - Explain that single-file HTML can be large and slower to open.
7. Verify before claiming completion:
   - Count pages, JSON, Markdown, screenshot files, stitched PNG files.
   - Check shareable HTML has data URI images and no local image path references.
   - Check generated files are not empty.
   - Record validation in `VERIFICATION.md`.

## Script Usage

The helper scripts live under this skill's `scripts/` directory.

### One-step archive with browser extraction

```powershell
& "../scripts/webbridge_archive.ps1" `
  -Url "https://example.com/page" `
  -OutDir "./outputs/webbridge-archive-demo" `
  -Mode auto `
  -BuildReader `
  -MakeShareable
```

Common options:

- `-Mode auto`: detect Feishu wiki vs single page.
- `-Mode single`: archive only the supplied URL/current page.
- `-Mode feishu-wiki`: collect Feishu/Lark wiki children from the sidebar.
- `-MaxPages 3`: limit pages for testing.
- `-NoScreenshots`: only extract text/JSON/Markdown.
- `-JpegQuality 82`: viewport screenshot quality.
- `-CommandTimeoutSec 60`: timeout per WebBridge command.
- `-MaxScreenshotFailures 2`: stop screenshot loop after repeated screenshot failures, preserving partial screenshots.
- `-ScreenshotRetries 1`: retry each screenshot before marking it failed.
- `-ScreenshotDelayMs 700`: wait after scrolling before taking a screenshot.
- `-ResumeScreenshots`: reuse existing non-empty screenshot files when rerunning the same output directory.
- `-BuildReader`: call the Python reader builder after crawling.
- `-MakeShareable`: embed images into a single HTML.

### Build or rebuild reader from existing archive

```powershell
python "../scripts/build_archive_reader.py" `
  "./outputs/webbridge-archive-demo" `
  --title "资料归档" `
  --shareable `
  --zip
```

Use this when screenshots/JSON already exist and only the reading layer needs to be rebuilt.

On Windows, if a Chinese title is passed from PowerShell to Python and becomes mojibake, write the title to a UTF-8 file and use:

```powershell
python "../scripts/build_archive_reader.py" `
  "./outputs/webbridge-archive-demo" `
  --title-file "$env:TEMP\archive-title.txt" `
  --shareable `
  --zip
```

The PowerShell crawler already uses `--title-file` internally when `-BuildReader` is enabled.

### L6 anti-bot safe routing audit

Use this before attempting protected, suspicious, or unstable pages. It does not bypass access controls. It only classifies the page and records which route is appropriate.

```powershell
& "../scripts/l6_antibot_router.ps1" `
  -Url "https://example.com/protected-page" `
  -OutDir "./outputs/l6-audit-demo"
```

The result file is `l6-antibot-router-result.json` and includes:

- direct HTTP probe status and challenge markers.
- real-browser probe status and page risk markers.
- available local tooling such as `browseact`, `playwright`, `node`, and `python`.
- recommended route: `L1-direct`, `L2-browser-dom-or-L4-login-session`, `L6-manual-review-safe-mode`, or `manual-open-or-fix-webbridge`.

Safety boundary: do not solve captchas, steal credentials, bypass access controls, or rotate proxies by default. When a challenge page appears, preserve evidence and ask for manual takeover or explicit authorization.

## Quality Rules

- Preserve source URL and extraction timestamp in every JSON/Markdown record.
- JSON is the structured source of truth; Markdown and HTML are generated reading layers.
- Treat PDF export as optional only. If generated PDF is blank/tiny, mark it invalid instead of presenting it as a success.
- Do not claim "complete" until a fresh verification command confirms counts and path references.
- For external sharing, prefer a ZIP containing the single-file HTML if the HTML is too large for the platform.
- Do not expose private tokens, cookies, request headers, or unrelated local paths in public-facing README files.
- Screenshot capture must be timeout-protected and resumable. If one page fails after some screenshots, preserve partial screenshots, record `status: partial`, and still build the text reader. When rerunning with `-ResumeScreenshots`, reuse existing non-empty screenshots instead of starting from zero.
- L6 is a routing and safety layer unless an explicitly authorized external component is installed. It detects challenge pages and available tools; it does not perform captcha solving, credential extraction, or access-control bypass.

## Known Limits

- Single-file HTML grows by roughly 1.33x of embedded image bytes.
- Very tall images look blurry if a viewer fits the entire image to screen; the reader should display long images at original width or above with horizontal scroll.
- Some pages virtualize content aggressively; when text extraction misses content, screenshots become the reliable visual backup.
- Captchas and pages that require trusted user input need manual help from the user.
