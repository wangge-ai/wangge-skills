---
name: github-repo-dissector
description: Use when the user shares a GitHub repository URL or owner/repo and wants to understand, compare, evaluate, install, run, trial, or explain the repository, including purpose, architecture, setup, recent activity, growth signals, risks, and a readable technical report.
---

# GitHub Repository Dissector

Use the GitHub connector for repository facts, files, issues, releases, and activity. Clone or run code only when the user asks or technical verification requires it.

## Workflow

1. Confirm whether the user wants a quick scan, deep architecture analysis, install trial, comparison, or share-ready report.
2. Collect repository identity, purpose, license, release state, recent activity, architecture, setup path, and visible risks.
3. Distinguish repository claims from verified behavior. Do not equate stars with quality or current growth.
4. For a real trial, use an isolated temporary directory such as `github-trials/<owner-repo>` and record commands, outputs, failures, and cleanup needs.
5. For content selection and social packaging, hand the verified result to `github-content-radar`.
6. Produce a concise conclusion first, then evidence, architecture, setup, suitability, risks, and next action.

Use `scripts/github_repo_stats.py` only when connector data is insufficient or a deterministic trend calculation is requested. Resolve the current Python runtime instead of assuming `python` or `gh` is on PATH. Read `references/legacy-full-workflow.md` only for advanced legacy report details.
