---
name: top10stats-data-video
description: Create TOP10stats-style data videos from hot topics, official/professional
  datasets, or local CSV/XLSX files. Use when the user asks to 拆解 or 制作 B站/TOP10stats/数据可视化/动态排行/热点数据视频,
  including hotspot routing, data sourcing, cleaning, storyboard, cover, MP4 rendering,
  and verification.
license: MIT
---

# TOP10stats Data Video

## Core Rule

复刻流程，不搬运素材。学习 TOP10stats 的选题、数据结构、节奏、标题和图表方法，但使用公开数据、自有素材和本地脚本生成画面。

## Workflow

1. **热点入口**
   - 先把热点写成一句话，例如“AI搜索大战：谁能撼动 Google”。
   - 用路由脚本把热点映射到题材、数据源、视频形态和质检要求：
     ```powershell
     python -X utf8 scripts\hotspot_video_router.py --hotspot "AI搜索大战：谁能撼动Google"
     ```
   - 路由表在 `references/hotspot-to-video-routing.csv`，官方/专业数据源库在 `references/official-data-source-library.csv`。
   - 如果输出 `needs_live_source_search: true`，不要硬套现有分类；必须联网搜索官方或专业数据源，再回写新来源。

2. **判断是否值得做**
   - 优先选择“有热度 + 有可复查数据 + 能形成排名、趋势、结构变化或对比”的题材。
   - 不强行做年度动态排行。先读 `references/video-form-library.md`，选择长周期动态排行、热点快照 Top榜、双对象对比、结构变化图、地图热力图、指标卡或时间轴事件榜。
   - 题材如果只有传闻、截图、单一口径或无法复查来源，先不要进入制作。

3. **拿数据**
   - `official-data-source-library.csv` 是种子库，不是写死清单。每次制作前都要按 `refresh_cadence`、`live_search_query` 和 `refresh_rule` 快速校验。
   - 优先使用官方或专业来源：World Bank、IMF、UN、OECD、WHO、IEA、EIA、Ember、NASA、NOAA、国家统计局、海关总署、央行等。
   - 热点不在库里、来源过期、接口失效、口径不匹配或只有二手截图时，必须联网搜索补源。
   - 如果网页有 CSV/API，先自动抓；失败时手工导出 CSV，再继续。
   - 保留来源链接、下载日期、口径、单位和时间范围。
   - 读取 `references/data-sources.md` 查看快速数据源说明；读取 `references/official-data-source-library.csv` 或 `references/TOP10stats_数据源和路由表_Excel版.xlsx` 查看更完整的数据网站库。

4. **整理数据**
   - 标准长表：`date,entity,value,unit,source_url`。
   - 标准宽表：第一列 `Date`，后面每列是一个实体，值为百分比、数量或指数。
   - 清理同名实体、缺失值、异常单位；不要混用不同口径的数据。
   - 国家排行默认至少准备 12 个对象；长周期视频优先拉到 20 年以上，能拉到 1960 或 2000 以前更好。

5. **制作视频**
   - StatCounter 月度份额类题材使用：
     ```powershell
     python -X utf8 scripts\make_rank_videos.py --topics ai_chatbots search_engines social_media --fps 12
     ```
   - World Bank / Our World in Data 等专业国家数据使用：
     ```powershell
     python -X utf8 scripts\make_professional_data_videos.py
     ```
   - 专业数据脚本会抓取 World Bank GDP、人口、SIPRI/World Bank 军费、OWID/Global Carbon Budget CO2、OWID/Ember 发电量，并过滤 OWID 的全球/地区汇总，只保留国家排行。
   - 当前模板支持 Top12 动态排行，专业数据默认 80-90 秒；如要做快照榜、结构图、地图或指标卡，先按 `references/video-form-library.md` 确认形态，再扩展模板。

6. **验片**
   - 用 ffprobe 确认 MP4 同时有 video 和 audio 流。
   - 抽查标题卡、中段排行、结尾定格；检查中文、长英文名、数值和页脚不重叠。
   - 对 Top12 视频必须抽中段帧，确认 12 行都可读。
   - 检查封面、分镜 CSV、清洗后的数据表和 manifest 都已生成。

## TOP10stats Style Notes

读取 `references/style-teardown.md` 了解拆解要点。简化版规律：

- 视频多为 1-4 分钟，核心是“时间推进 + 排名变化”。
- 标题喜欢把数据主题和情绪钩子放在一起，如“谁能霸榜”“谁在追赶”“格局洗牌”。
- 画面不复杂，但信息密度高：大标题、大日期、动态条形图、来源或话题标签。
- 重点不是讲很多话，而是让观众看见“追赶、逆袭、掉队、霸榜”。

## Deliverables

一次完整任务至少产出：

- `*.mp4`：最终视频。
- `*_cover.png`：封面图。
- `*_storyboard.csv`：分镜表。
- `*_clean.csv`：清洗后的数据。
- `video_production_manifest.json`：时长、分辨率、音视频流、来源页。
- `professional_video_manifest.json`：专业数据源视频的来源、口径和验片信息。
- 热点路由结果：说明热点、数据源、视频形态和质检要求。
- 流程报告：说明选题、数据、制作步骤、限制和下一步优化。

## Quality Bar

- 不使用未授权视频片段、音乐或图标。
- 来源必须能让后来者复查，且要区分官方、国际机构、专业整理和第三方测量。
- 专业数据源不能写死；本地库只是起点，实际制作前要联网校验，缺源时要搜索、记录、回写。
- 画面优先清楚，不追求炫技。
- 热点驱动，但不能牺牲数据口径；不把第三方份额说成官方用户数。
- 自动化优先，但保留手工导出、Flourish/录屏路线作为备选。
