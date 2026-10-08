---
name: webbridge-archive-publisher
description: Use when crawling, archiving, exporting, or packaging a URL, logged-in
  browser page, Feishu or Lark document or wiki, WeChat page, or browser-only source
  into traceable HTML, Markdown, screenshots, PDF, and a readable local archive using
  Kimi WebBridge or the connected browser.
license: MIT
---

# Web Archive Publisher

Archive browser-only sources without persisting credentials or session secrets.

## Workflow

1. Confirm the source URL, authorization state, scope, and desired artifacts.
2. Use Kimi WebBridge for the user's real logged-in browser session. Use the current Browser/Chrome surface when the user selects it or when Kimi is unavailable.
3. Capture source URL, title, collected time, visible content, attachments, and failure reasons.
4. Save raw evidence separately from cleaned Markdown and presentation HTML.
5. Generate screenshots or PDF when visual layout matters.
6. Build a folder reader with `scripts/build_archive_reader.py` only for the legacy page-JSON plus screenshot layout.
7. For rich Feishu archives, multi-batch deduplication, or a self-contained HTML likely to exceed 100 MB, return the verified per-document HTML/assets layout to `web-collection-orchestrator`; use its streaming bundle builder and cold first-open QA. Do not embed the whole archive in one JSON object or place the catalog script after the asset payload.
8. Store output under `./outputs/collection\web-archive\<date-task>`.

Never save passwords, cookies, tokens, authenticated request headers, or sensitive session URLs. Stop at CAPTCHA or access restrictions. The old PowerShell scripts are compatibility helpers only; prefer the installed Kimi WebBridge v1.11.6 workflow. Treat “works after refresh” as a failed first-open check until the directory renders on a cold open.
