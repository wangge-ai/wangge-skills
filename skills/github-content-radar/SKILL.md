---
name: github-content-radar
description: Use when discovering, monitoring, deduplicating, scoring, or packaging GitHub repositories for practical trials, Chinese social-media trends, WeChat article material, shareability decisions, creator leads, or content topic pipelines.
---

# GitHub Content Radar

Use the GitHub connector for repository facts and the web or Kimi WebBridge for public social evidence. Use `github-repo-dissector` after a repository is selected for technical analysis.

## Workflow

1. Define the time window, audience, channel, and practical-use threshold.
2. Collect repository facts, growth signals, public mentions, creator sources, and trial evidence.
3. Deduplicate forks, mirrors, repeated posts, and the same project under multiple names.
4. Score practical value, explainability, novelty, proof strength, trial cost, and content fit.
5. Output a shortlist, rejection reasons, trial queue, shareability angle, and WeChat material card when requested.
6. Store working data under a task-local `github-radar/` directory or another workspace chosen by the user.

## Reference Routing

- For a Chinese social-platform scan, read `references/github-social-radar.md`, then use the `social-*` references it names for search, source memory, scoring, appearance history, trial outcomes, and output structure.
- For repository shareability or a lightweight public-facing explanation, read `references/github-repo-shareability.md`.
- For WeChat topic selection and material cards, read `references/github-wechat-curation.md` and the `wechat-*` references it names.

Read only the branch needed for the current request.
