---
name: wechat-article-knowledge-pack
description: 把公众号文章链接或本地导出文件整理为原文档案、元数据和可追溯知识卡。
license: MIT
metadata:
  source_pack: '12'
---

# WeChat Article Knowledge Pack

Use this skill to help users organize WeChat Official Account articles into a local AI-readable knowledge base.

The skill is a router and organizer first. It does not default to crawling.

## Safety Boundary

Allowed:

- Personal study.
- Local backup.
- Internal knowledge base.
- Topic research.
- Summary, tagging, clustering, and method extraction.

Not allowed by default:

- Automatic login.
- Extracting cookies, credentials, or private tokens.
- Bypassing platform verification.
- Large-scale bulk collection.
- Public reposting or rewriting without attribution.
- Turning summaries into disguised copies of the original article.

If a user asks for risky behavior, redirect to compliant backup, summarization, or manual export workflows.

## Input Router

First identify the input type:

| Input | Route |
|---|---|
| Single `mp.weixin.qq.com/s/...` URL | Try normal request, then clean browser/mobile UA, then `wx2md-worker` or `ReadGZH`; use `feedgrab` as backup; if verification appears, switch to exported-file route |
| Collection / album URL | Recommend `wechatDownload` collection workflow |
| Public account name | Ask for a sample article link or exported files before suggesting batch export |
| Local folder with HTML/MD/PDF | Skip capture and organize/summarize files |
| Existing exported Markdown | Create knowledge cards, tags, and topic ideas |
| Need long-term updates | Suggest `we-mp-rss` as advanced RSS/API route |
| Need original layout preserved | Suggest `wechat-article-exporter` or HTML export |

## Link Readability Gate

For a single WeChat article URL, first determine whether the fetched/opened page contains the actual article.

It is readable only if it has at least:

- real article title,
- author or account information,
- multiple body paragraphs,
- no dominant verification prompt.

It is not readable if the content mainly contains:

- `环境异常`,
- `去验证`,
- `Weixin Official Accounts Platform`,
- CAPTCHA or verification instructions,
- empty body or only platform shell text.

If not readable, do not create a knowledge card. Report that the link route failed and switch to fallback input: exported Markdown/HTML/PDF, pasted article text, manual browser copy, or desktop tool export.

## Single Link Lightweight Attempts

Use this order:

1. Normal request.
2. Clean browser or mobile user agent.
3. `wx2md-worker` or `ReadGZH` service-side conversion.
4. `feedgrab` as a generic backup.
5. Exported file or pasted text.

Clean browser/mobile UA means simulating normal mobile reading conditions. It is not a bypass. Stop immediately if the page requires QR scan, CAPTCHA, login, or explicit verification.

## Tool Selection

Use this default mapping:

- `feedgrab`: single article, search, URL to Markdown, MCP-friendly route.
- `wx2md-worker`: single WeChat article URL to Markdown/HTML; good first try for direct link input.
- `ReadGZH`: AI-readable WeChat article service/API/MCP route; useful but may require API key or have rate limits.
- `wechatDownload`: desktop batch export, collection export, multiple local formats.
- `wechat-article-exporter`: layout-preserving HTML export, private deployment, API route.
- `we-mp-rss`: long-term RSS subscription and automated updates.

Never promise that a WeChat URL can always be fetched directly. Try service-side conversion first. If a verification page or rate limit appears, suggest another conversion route, desktop/manual export, or already-exported local files.

## Folder Template

Use this structure:

```text
公众号资料库/
  账号名/
    YYYY/
      YYYY-MM-DD_文章标题前20字/
        original.html
        article.md
        article.pdf
        assets/
        summary.md
        metadata.json
        notes.md
```

Clean file names by removing:

```text
? * : | " < > / \
```

## Summary Workflow

For each article, produce:

1. One-sentence summary.
2. Key points.
3. Reusable methods.
4. Quote/reference candidates.
5. Risks and boundaries.
6. Tags.
7. Topic ideas for future writing.

Use this output skeleton:

```markdown
# 文章知识卡

## 基本信息
- 账号：
- 标题：
- 日期：
- 原文链接：
- 导出文件：

## 一句话摘要

## 关键观点

## 可复用方法

## 可引用素材

## 风险和边界

## 标签

## 后续选题
```

## Recommended User-Facing Response

When starting a task, say:

```text
我先判断你的输入属于哪一种：单篇链接、合集、公众号名，还是本地已导出文件。然后我会推荐最轻的工具路线，并把结果整理成知识卡，不做默认批量采集。
```

## Failure Handling

- If direct URL fetch returns a verification page: record it and switch to manual/exported-file route.
- If Computer Use/browser can open the page but sees only a verification page: treat it as not readable. A normal browser is not the same as WeChat's internal browser or an already-authorized reading environment.
- If clean browser/mobile UA still shows scan, CAPTCHA, login, or verification: stop and switch to exported-file or pasted-text route.
- If local MCP is not running: tell the user to open the desktop tool and enable MCP.
- If a source build fails: suggest official web/Docker route instead of debugging deeply unless the user asks.
- If Docker pull fails: mark as network/environment issue and keep the repo as advanced route.
