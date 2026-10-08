---
name: ai-topic-planner
description: Use when discovering, verifying, screening, or planning Chinese AI hot
  topics from AIHot, NewsNow, social feeds, websites, or user-provided links for WeChat,
  Xiaohongshu, video, or internal content planning.
license: MIT
---

# AI Topic Planner

Turn current AI signals into evidence-backed topic briefs. Use Kimi WebBridge, the connected browser, or web search according to the user's requested surface and login needs.

## Workflow

1. Confirm audience, channel, time window, and desired topic count.
2. Collect candidate events with source URL, event date, publish date, and visible evidence.
3. Deduplicate the same event across feeds.
4. Score practical value, novelty, evidence strength, account fit, and production cost.
5. Reject rumors, recycled announcements, and topics without a usable primary source.
6. Produce a short list with angle, proof, risk, recommended format, and next action.

Default working root: `./outputs/content\ai-topics`. Do not store credentials or browser session data.

Read `references/aihot-source.md` for AIHot-specific retrieval and `references/topic-planning.md` for the legacy planning rubric only when needed.
