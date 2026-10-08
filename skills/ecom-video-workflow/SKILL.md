---
name: ecom-video-workflow
description: Use when analyzing local ecommerce videos, extracting shot and subtitle
  evidence, planning product videos, building marketing-video matrices, or producing
  evidence-constrained storyboards, voiceover, subtitles, and shooting priorities.
license: MIT
---

# Ecommerce Video Workflow

Route the task to analysis, single-video planning, or campaign-level planning.

1. For an existing local video, extract duration, shots, visible claims, subtitles, pacing, and risks. Read `references/ecom-video-evidence-analysis.md`.
2. For one deliverable, create storyboard, voiceover, subtitles, prop list, and acceptance checks. Read `references/ecom-video-planner.md`.
3. For a content matrix, map audience, pain point, benefit, proof, format, and shooting priority. Read `references/ecom-marketing-video-planner.md`.
4. Never invent product efficacy, certifications, sales, reviews, or performance uplift.
5. Store assets and outputs under `./outputs/ecommerce\video`.

Use FFmpeg/FFprobe only when available. If missing, report the dependency before attempting deterministic media extraction. Resolve the current Python runtime for bundled scripts.
