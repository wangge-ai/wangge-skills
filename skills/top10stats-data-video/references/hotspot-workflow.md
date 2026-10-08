# Hotspot To Data Video Workflow

## 1. Hotspot Collector

Collect candidate topics from hot lists, search trends, social feeds, news, platform rankings or manual user input. Save each item as:

```csv
captured_at,platform,title,url,summary,heat_score,language
```

Do not treat a hot title as a data topic yet. It is only a lead.

## 2. Topic Router

Run [hotspot_video_router.py](../scripts/hotspot_video_router.py) on each hot title. The router reads:

- `hotspot-to-video-routing.csv`
- `official-data-source-library.csv`

It returns topic type, recommended video format, expected data shape, preferred sources, backup sources and quality gate.

If the router returns `needs_live_source_search: true`, stop routing and search the web. Do not force the hotspot into the nearest local category. The local route table is a convenience layer, not a closed taxonomy.

## 3. Data Acquisition

Use the highest-priority source that has a reachable API, CSV download or manual export path. Keep:

- source name and URL
- download time
- metric definition
- unit and denominator
- filters and geography
- any missing coverage

If the data source is third-party measured, state that clearly in the video footer or report.

When live search finds a new useful source, update:

- `official-data-source-library.csv`
- `hotspot-to-video-routing.csv`, if this is a repeatable topic type
- the `last_reviewed`, `refresh_cadence`, `live_search_query` and `refresh_rule` columns

Then run:

```powershell
python -X utf8 scripts\refresh_reference_tables.py --sync-skill
```

## 4. Data QA

Before rendering:

- confirm the table has enough time range or enough current entities
- remove region aggregates from country rankings unless intentional
- normalize units
- check latest year/month coverage
- keep at least 12 entities for country ranking videos when the screen can support it

## 5. Video Form Selector

Use `video-form-library.md` before choosing a template.

- Long historical rankings: GDP, population, military spending, emissions, electricity.
- Snapshot Top榜: earthquakes, city air quality, rankings, market cap.
- Comparison: two countries, two products, two platforms.
- Structure chart: energy mix, age structure, trade mix.
- Map heatmap: climate, disasters, air quality.
- Indicator card: central bank, CPI, jobs, finance.
- Timeline event榜: disasters, wars, sports, launches.

## 6. Render And Verify

Render MP4, cover, storyboard and clean CSV. Then verify:

- video and audio streams exist
- title, date, bars, labels and footer do not overlap
- Top12 rows are readable on a mid-video frame
- manifest records duration, source and output paths

## 7. Handoff

Every finished run should include:

- final videos
- clean data
- source links and source type
- route decision
- chosen video form
- known limitations
- next recommended adapter or template to build
