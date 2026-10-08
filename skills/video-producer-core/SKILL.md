---
name: video-producer-core
description: Use when planning, creating, replicating, or extending videos of any
  style or platform, including scripts, storyboards, visual direction, voiceover/TTS,
  sound effects, AI/B-roll asset plans, subtitles, render checks, and final MP4 production.
license: MIT
---

# Video Producer Core

## Overview

Use this as the general video production backbone. It handles the production brief, script, storyboard, asset plan, audio plan, build plan, and verification, while specialized skills handle domain-specific visuals such as Manim technical diagrams or platform-specific styles.

## Route the Request

Use this skill first for broad video requests. Then add specialized skills only when needed:

| Need | Add |
| --- | --- |
| Technical diagrams, formulas, data flows, system architecture | `manim-hyperframes-video` |
| HyperFrames HTML composition, subtitles, transitions, render | `hyperframes:hyperframes` and `hyperframes:hyperframes-cli` |
| Raster images, B-roll plates, cover images | `imagegen` |
| Website capture into video | `hyperframes:website-to-hyperframes` |
| Remotion/React video composition | `remotion:remotion-best-practices` |

## Minimum Inputs

If the user gives little context, proceed with sensible defaults and state assumptions. The minimum useful brief is:

- Topic or product
- Target duration
- Audience
- Style reference or mood
- Voiceover choice: no voice, temporary TTS, user-provided audio, or final TTS
- Output: script only, storyboard, project files, or final MP4

For stronger results, also ask for required talking points, forbidden claims, brand rules, aspect ratio, target platform, and reference links/files.

## Workflow

1. **Frame the video**
   - Write a one-sentence thesis.
   - Pick the format: explainer, tutorial, product demo, course, ad, social clip, recap, or documentary.
   - Choose aspect ratio and duration before writing the timeline.

2. **Write script and storyboard**
   - Split into beats of 5-20 seconds.
   - Keep one main visual idea per beat.
   - Use `references/production-template.md` for the brief, folder structure, and storyboard columns.

3. **Plan visuals**
   - Classify each beat as footage, screen recording, AI image/B-roll, motion graphic, chart, diagram, or title card.
   - Use original or user-owned assets. Do not depend on copyrighted source clips unless the user explicitly owns or licenses them.
   - Record prompts for generated assets in the project.

4. **Plan audio**
   - Generate temporary TTS when the user has not provided narration.
   - Keep narration, ambience, transition hits, and effects as separate source files before final render.
   - On Windows, check SAPI voices as a fallback if model-based TTS fails.

5. **Build**
   - Put source assets, generated assets, audio, captions, and renders in separate folders.
   - Build a short draft first for timing and style.
   - Expand to the full target duration after the draft checks out.

6. **Verify**
   - Confirm the final file has video and audio streams with `ffprobe`.
   - For HyperFrames, run `npx hyperframes lint`, `validate`, and `inspect`.
   - Extract representative frames and inspect title, dense middle scenes, subtitle scenes, and ending.

## Environment Preflight

For production work, run the bundled script when available:

```powershell
powershell -ExecutionPolicy Bypass -File "scripts/check_video_environment.ps1"
```

It checks common dependencies such as FFmpeg, Node, Chrome, Python, Manim, MiKTeX, and Windows TTS voices.

## Deliverables

A complete video job should leave behind:

- `script.md` or `script_full.md`
- `storyboard.csv`
- `assets/ai/` with prompts recorded
- `assets/audio/` with source audio
- composition source files
- `renders/*.mp4`
- verification notes: duration, resolution, fps, audio stream, and warnings

## Common Mistakes

- Starting composition before the script and storyboard are clear.
- Treating a style reference as permission to copy assets.
- Putting the whole video into one tool when different beats need different tools.
- Forgetting audio verification and delivering a silent MP4.
- Trusting render success without checking representative frames.
