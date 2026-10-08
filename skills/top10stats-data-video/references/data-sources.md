# Data Sources

## Full Library

For hotspot-driven work, start with `official-data-source-library.csv`. It is a larger source catalog covering macro economy, trade, population, health, energy, climate, disasters, military, agriculture, technology, finance, China official statistics, tourism, transport, sports, air quality, ocean and space.

Use the smaller list below only as a fast starting point. The library is not a fixed whitelist; it is a seed list that must be checked against live web sources before production.

Excel-friendly versions are also available:

- `TOP10stats_数据源和路由表_Excel版.xlsx`
- `官方专业数据源库.xlsx`
- `热点到数据视频路由表.xlsx`

## Source Priority

1. Official national or intergovernmental sources.
2. Professional public datasets with clear methodology.
3. Third-party measurement sources, only when official usage data is unavailable.
4. Manual exports from visible charts, only when the original source and unit are retained.

Do not mix aggregate regions such as World, Europe or OECD with country rankings unless the video is explicitly about regions.

## Refresh Rule

Before using any source:

1. Open `home_url` or `api_or_download`.
2. Check whether the API, CSV, methodology page and update schedule still exist.
3. If the source is stale, unavailable or not fit for the current hotspot, search the web using `live_search_query`.
4. Add confirmed new sources back to `official-data-source-library.csv`, then refresh the Excel-safe files:

```powershell
python -X utf8 scripts\refresh_reference_tables.py --sync-skill
```

## Fast Sources For Ranking Videos

- StatCounter Global Stats: browser, search engine, social media, AI chatbot, mobile vendor and platform share. Good for monthly percentage ranking videos.
- World Bank DataBank/API: GDP, population, military expenditure, energy, health, education and country indicators. Good for long historical country rankings. Prefer indicator pages such as `NY.GDP.MKTP.CD`, `SP.POP.TOTL`, and `MS.MIL.XPND.CD`.
- Our World in Data Grapher: health, climate, energy, population and technology adoption. Good when CSV download is available. Filter `Code` to ISO3 country codes (`^[A-Z]{3}$`) when the video should be a country ranking, otherwise OWID regional aggregates such as World or Europe may enter the chart.
- National Bureau of Statistics of China: province and city indicators. Good for China regional rankings.
- CompaniesMarketCap: company market capitalization rankings. Check reuse limits before publishing.
- FAOSTAT: food and agriculture production rankings.
- SIPRI: military spending and arms transfer data.
- BP/Energy Institute Statistical Review: energy production and consumption.

## Source Checklist

Record these fields before rendering:

- Source name and URL.
- Download date.
- Time range.
- Unit, denominator, and whether values are percent, count, index, or amount.
- Whether the data is official, third-party measured, or estimated.
- Any filters, such as worldwide, mobile, desktop, all platforms, country, or region.

## StatCounter CSV Pattern

Many StatCounter pages expose CSV through `chart.php`:

```text
https://gs.statcounter.com/chart.php?<stat>-ww-monthly-<from>-<to>&statType_hidden=<stat>&region_hidden=ww&granularity=monthly&statDisplay=<display>&fromMonthYear=<from>&toMonthYear=<to>&csv=1
```

Examples of `stat`:

- `ai_chatbot`
- `search_engine`
- `social_media`

## World Bank API Pattern

Use a focused candidate-country pool instead of `country/all` when making Top10 videos:

```text
https://api.worldbank.org/v2/country/USA;CHN;JPN/indicator/NY.GDP.MKTP.CD?format=json&per_page=20000&date=1960:2025
```

This is faster and avoids mixing aggregate regions into the chart. Record the indicator code and the World Bank `lastupdated` date when available.

If the endpoint returns an empty column or a generic browser chart, use the visible page's "Download Data (.csv)" button manually and continue from the exported CSV.
