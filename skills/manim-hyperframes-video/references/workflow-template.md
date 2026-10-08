# Manim + HyperFrames Technical Workflow Template

## Folder Structure

```text
project-name/
  DESIGN.md
  script.md
  storyboard.csv
  assets/
    ai/
    audio/
    manim/
    source/
  manim/
    scenes.py
  compositions/
  index.html
  renders/
  tools/
```

## Storyboard Columns

```csv
time,beat,voiceover,visual,tool,asset,notes
0-8s,hook,One sentence hook,big title + AI background,HyperFrames,assets/ai/hero.png,fast visual anchor
8-20s,scale,Turn abstract number into comparison,large number + tiled blocks,HyperFrames,,subtitle safe
20-35s,mechanism,Explain the key system behavior,transparent Manim diagram,Manim+HyperFrames,assets/manim/mechanism.webm,one concept only
35-50s,context,Show real-world environment,AI B-roll + callouts,HyperFrames,assets/ai/context.png,no copied logos
```

## Scene Type Map

| Scene Type | Best Tool | Notes |
| --- | --- | --- |
| Formula reveal | Manim | Highlight one term at a time |
| Data block split | Manim | File -> chunks -> replicas |
| System architecture | Manim or HTML/SVG | Use deterministic labels |
| Big-number comparison | HyperFrames | Huge type, tiles, cards |
| AI atmosphere | AI image + HyperFrames | No text/logos/watermarks |
| Subtitles and packaging | HyperFrames | Master timeline and audio |

## Manim Starter

```python
from manim import *


class DataBlocks(Scene):
    def construct(self):
        title = Text("不是一个大文件", font_size=42).to_edge(UP)
        source = RoundedRectangle(width=4.2, height=1.0, corner_radius=0.12)
        source.set_stroke(WHITE, 2)
        source_label = Text("原始视频文件", font_size=30).move_to(source)

        blocks = VGroup(*[
            RoundedRectangle(width=0.8, height=0.8, corner_radius=0.08)
            .set_fill(color, opacity=0.9)
            .set_stroke(WHITE, 1.5)
            for color in [BLUE, YELLOW, RED, GREEN]
        ]).arrange(RIGHT, buff=0.24)

        self.play(Write(title))
        self.play(FadeIn(source), Write(source_label))
        self.play(Transform(VGroup(source, source_label), blocks))
        self.wait(1)
```

## HyperFrames Pattern

```html
<video
  id="manim-atom"
  class="clip"
  data-start="20"
  data-duration="8"
  data-track-index="5"
  src="assets/manim/mechanism.webm"
  muted
  playsinline>
</video>

<div id="caption-2" class="clip caption" data-start="20" data-duration="8" data-track-index="8">
  系统不会把它当成一个巨大文件，而是拆成很多数据块。
</div>
```

## Technical Quality Checklist

- Does every Manim scene explain exactly one idea?
- Can the viewer understand the mechanism with sound muted?
- Are captions readable over AI/B-roll?
- Are generated images free of unwanted text, logos, or watermarks?
- Did Manim render before HyperFrames composition?
- Did HyperFrames `lint`, `validate`, and `inspect` run?
- Does `ffprobe` show both video and audio when audio is expected?
