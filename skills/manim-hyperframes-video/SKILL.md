---
name: manim-hyperframes-video
description: Use when a video needs precise technical explanation visuals with Manim
  and HyperFrames, such as formulas, data flows, storage/network/CPU/AI system diagrams,
  Chinese tech explainers, Bilibili-style science videos, or compositing Manim renders
  with subtitles, cards, transitions, and AI/B-roll.
license: MIT
---

# Manim + HyperFrames Technical Explainer

## Overview

Use this as the specialized layer for technical explainer videos. It is not a general video generator; use `video-producer-core` first for broad video planning, then use this skill when the video needs deterministic diagrams, formulas, system flows, or Manim + HyperFrames implementation.

## Division of Labor

| Layer | Responsibility |
| --- | --- |
| `video-producer-core` | Brief, script, storyboard, asset plan, audio plan, render verification |
| Manim | Formulas, data blocks, arrows, graphs, system mechanics, deterministic technical motion |
| HyperFrames | Master timeline, captions, title cards, callouts, AI/B-roll, transitions, audio tracks, final render |
| AI/B-roll | Atmosphere and context: data centers, chips, devices, hard drives, product shots |

## Workflow

1. **Start from a storyboard**
   - If none exists, use `video-producer-core` to create one.
   - Mark each beat as Manim, HyperFrames, AI/B-roll, screen recording, or mixed.

2. **Choose Manim beats**
   - Use Manim for exact logic: formulas, block splitting, replicas, routing, queues, latency, graphs, architecture.
   - Keep each Manim scene to one concept and usually 5-15 seconds.
   - Render transparent WebM when it will sit over HyperFrames backgrounds.

3. **Choose HyperFrames beats**
   - Use HyperFrames for pacing, subtitles, cards, scene transitions, title resets, sound effects, and final assembly.
   - Treat HyperFrames as the master timeline. Do not put the whole video in Manim unless it is purely mathematical.

4. **Generate or collect assets**
   - Use AI/B-roll for visual texture, not for precise labels or technical correctness.
   - Record all generated prompts in the project.
   - Avoid copyrighted clips, platform logos, and copied frames unless the user owns them.

5. **Build and verify**
   - Render Manim atoms first.
   - Compose in HyperFrames.
   - Run `lint`, `validate`, `inspect`, `ffprobe`, and representative frame checks.

## Windows Pitfalls

- Run Manim through the environment where it is installed. If Manim is in `.venv`, use `.venv\Scripts\manim.exe`.
- `MathTex` requires LaTeX/MiKTeX on PATH.
- PowerShell scripts containing Chinese should be saved as UTF-8 with BOM for Windows PowerShell 5.1.
- If HyperFrames bundled Chrome fails, set `HYPERFRAMES_BROWSER_PATH` to a local Chrome executable.
- If model-based TTS fails, use Windows SAPI as a temporary Chinese narration fallback through `video-producer-core`.

## Commands

```powershell
# Manim transparent atom
manim -ql -t --format=webm manim/scene.py SceneName -o scene_name

# HyperFrames checks
npx hyperframes lint
npx hyperframes validate
npx hyperframes inspect --samples 15

# HyperFrames draft render
$env:HYPERFRAMES_BROWSER_PATH='C:\Program Files\Google\Chrome\Application\chrome.exe'
npx hyperframes render --quality draft --output renders/draft.mp4

# Final file probe
ffprobe -v error -show_entries stream=index,codec_type,codec_name,width,height,avg_frame_rate,duration -show_entries format=duration,size -of json renders/draft.mp4
```

## Output Expectations

For a complete technical explainer job, produce:

- Script and storyboard from `video-producer-core`
- Manim source scenes
- Rendered Manim WebM assets
- HyperFrames composition
- AI/B-roll prompts and generated assets
- Audio sources and final MP4
- Verification notes and known limitations

## References

Read `references/workflow-template.md` for a technical storyboard template, folder structure, and Manim/HyperFrames scene patterns.
