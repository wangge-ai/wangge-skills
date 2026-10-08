import argparse
import json
import sys
import time
import urllib.request
from datetime import date
from io import BytesIO
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from make_rank_videos import WORK_DATA, OUTPUTS, ensure_dirs, render_video, ffprobe_video


UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"


PRO_TOPICS = {
    "world_gdp": {
        "index": "04",
        "title": "世界GDP排行 1960-2025",
        "subtitle": "全球经济牌桌洗牌，谁在追赶第一梯队",
        "hook": "几十年过去，全球经济中心发生了什么变化？",
        "source_page": "https://data.worldbank.org/indicator/NY.GDP.MKTP.CD",
        "source_label": "World Bank - GDP (current US$), indicator NY.GDP.MKTP.CD",
        "indicator": "NY.GDP.MKTP.CD",
        "countries": "USA;CHN;JPN;DEU;IND;GBR;FRA;ITA;BRA;CAN;RUS;KOR;AUS;ESP;MEX;IDN;NLD;SAU;TUR;CHE;POL;SWE;BEL;ARG;THA;IRL;AUT;NOR;ARE;SGP",
        "from": 1960,
        "to": 2025,
        "top_n": 12,
        "duration": 90,
        "value_divisor": 1_000_000_000_000,
        "value_suffix": " 万亿美元",
        "value_precision": 2,
    },
    "world_population": {
        "index": "05",
        "title": "世界人口排行 1960-2025",
        "subtitle": "人口大国的排名，正在悄悄重排",
        "hook": "印度、中国、美国之后，谁在加速上桌？",
        "source_page": "https://data.worldbank.org/indicator/SP.POP.TOTL",
        "source_label": "World Bank - Population, total, indicator SP.POP.TOTL",
        "indicator": "SP.POP.TOTL",
        "countries": "IND;CHN;USA;IDN;PAK;NGA;BRA;BGD;RUS;MEX;ETH;JPN;PHL;EGY;VNM;COD;TUR;IRN;DEU;THA;GBR;FRA;ITA;TZA;ZAF;MMR;KEN;KOR;COL;ESP",
        "from": 1960,
        "to": 2025,
        "top_n": 12,
        "duration": 90,
        "value_divisor": 100_000_000,
        "value_suffix": " 亿人",
        "value_precision": 2,
    },
    "military_spending": {
        "index": "06",
        "title": "全球军费开支排行 1960-2024",
        "subtitle": "SIPRI口径下，军费格局如何变化",
        "hook": "谁在持续加码，谁又退出了第一梯队？",
        "source_page": "https://data.worldbank.org/indicator/MS.MIL.XPND.CD",
        "source_label": "World Bank / SIPRI - Military expenditure (current USD)",
        "indicator": "MS.MIL.XPND.CD",
        "countries": "USA;CHN;RUS;IND;SAU;GBR;DEU;FRA;JPN;KOR;UKR;ISR;ITA;AUS;CAN;BRA;POL;TUR;ESP;NLD;IRN;PAK;IDN;SWE;NOR;GRC;ARE;QAT;EGY;SGP",
        "from": 1960,
        "to": 2024,
        "top_n": 12,
        "duration": 90,
        "value_divisor": 1_000_000_000,
        "value_suffix": " 十亿美元",
        "value_precision": 1,
    },
    "co2_emissions": {
        "index": "07",
        "title": "全球CO2排放排行 1949-2024",
        "subtitle": "工业化、能源结构和发展阶段，都写在这条曲线上",
        "hook": "全球排放第一梯队，几十年里换过哪些位置？",
        "source_page": "https://ourworldindata.org/grapher/annual-co2-emissions-per-country",
        "source_label": "Our World in Data / Global Carbon Budget - Annual CO2 emissions",
        "top_n": 12,
        "from": 1949,
        "to": 2024,
        "duration": 90,
        "value_divisor": 1_000_000_000,
        "value_suffix": " 十亿吨",
        "value_precision": 2,
    },
    "electricity_generation": {
        "index": "08",
        "title": "全球发电量排行 2000-2024",
        "subtitle": "电力需求背后，是工业、人口和数字化的竞赛",
        "hook": "谁的电力增长最猛？答案很直观。",
        "source_page": "https://ourworldindata.org/grapher/electricity-generation",
        "source_label": "Our World in Data / Ember - Total electricity generation",
        "top_n": 12,
        "from": 2000,
        "to": 2024,
        "duration": 80,
        "value_divisor": 1,
        "value_suffix": " TWh",
        "value_precision": 0,
    },
}


def fetch_bytes(url: str, tries: int = 4) -> bytes:
    last_error = None
    for attempt in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=80) as response:
                return response.read()
        except Exception as exc:
            last_error = exc
            time.sleep(1.5 * (attempt + 1))
    raise RuntimeError(f"Failed to fetch {url}: {last_error}")


def world_bank_indicator(topic_key: str, topic: dict) -> pd.DataFrame:
    rows = []
    url = (
        f"https://api.worldbank.org/v2/country/{topic['countries']}/indicator/{topic['indicator']}"
        f"?format=json&per_page=20000&date={topic['from']}:{topic['to']}"
    )
    data = json.loads(fetch_bytes(url).decode("utf-8"))
    if not isinstance(data, list) or len(data) < 2:
        raise RuntimeError(f"Unexpected World Bank response for {topic_key}: {data}")
    rows.extend(data[1])

    records = []
    for row in rows:
        value = row.get("value")
        if value is not None:
            records.append({"Date": int(row["date"]), "Entity": row["country"]["value"], "Value": float(value)})
    return records_to_wide(topic_key, topic, pd.DataFrame(records))


def owid_csv(topic_key: str, topic: dict, url: str, value_col: str) -> pd.DataFrame:
    raw = fetch_bytes(url)
    df = pd.read_csv(BytesIO(raw))
    df = df[df["Code"].notna()].copy()
    df = df[df["Code"].astype(str).str.match(r"^[A-Z]{3}$")].copy()
    df = df.rename(columns={"Year": "Date", "Entity": "Entity", value_col: "Value"})
    df = df[["Date", "Entity", "Value"]]
    df["Value"] = pd.to_numeric(df["Value"], errors="coerce")
    df = df.dropna(subset=["Value"])
    return records_to_wide(topic_key, topic, df)


def records_to_wide(topic_key: str, topic: dict, records: pd.DataFrame) -> pd.DataFrame:
    if "from" in topic:
        records = records[records["Date"] >= int(topic["from"])].copy()
    if "to" in topic:
        records = records[records["Date"] <= int(topic["to"])].copy()
    latest_year = int(records["Date"].max())
    latest = records[records["Date"] == latest_year].sort_values("Value", ascending=False).head(topic["top_n"] + 2)
    entities = latest["Entity"].tolist()

    # Keep a few historically important countries if they exist, without overcrowding the chart.
    for important in ["United States", "China", "India", "Japan", "Germany", "Russian Federation", "Russia"]:
        if important in set(records["Entity"]) and important not in entities:
            entities.append(important)

    records = records[records["Entity"].isin(entities)].copy()
    wide = records.pivot_table(index="Date", columns="Entity", values="Value", aggfunc="last").sort_index()
    wide = wide.interpolate(limit_direction="both").fillna(0)
    wide = wide.loc[(wide.sum(axis=1) > 0)]
    wide = wide.reset_index()
    wide["Date"] = pd.to_datetime(wide["Date"].astype(str), format="%Y")
    out = WORK_DATA / f"{topic['index']}_{topic_key}_clean.csv"
    wide.to_csv(out, index=False, encoding="utf-8")
    return wide


def main() -> int:
    parser = argparse.ArgumentParser(description="Fetch professional datasets and render TOP10stats-style ranking videos.")
    parser.add_argument(
        "--topics",
        nargs="*",
        default=list(PRO_TOPICS.keys()),
        choices=sorted(PRO_TOPICS.keys()),
        help="Topic keys to render. Defaults to all professional topics.",
    )
    parser.add_argument("--manifest-name", default="professional_video_manifest.json", help="Manifest filename under outputs/.")
    args = parser.parse_args()

    ensure_dirs()
    selected = list(dict.fromkeys(args.topics))

    fetchers = {
        "world_gdp": lambda: world_bank_indicator("world_gdp", PRO_TOPICS["world_gdp"]),
        "world_population": lambda: world_bank_indicator("world_population", PRO_TOPICS["world_population"]),
        "military_spending": lambda: world_bank_indicator("military_spending", PRO_TOPICS["military_spending"]),
        "co2_emissions": lambda: owid_csv(
            "co2_emissions",
            PRO_TOPICS["co2_emissions"],
            "https://ourworldindata.org/grapher/annual-co2-emissions-per-country.csv",
            "Annual CO₂ emissions",
        ),
        "electricity_generation": lambda: owid_csv(
            "electricity_generation",
            PRO_TOPICS["electricity_generation"],
            "https://ourworldindata.org/grapher/electricity-generation.csv",
            "Total electricity",
        ),
    }
    datasets = {key: fetchers[key]() for key in selected}

    manifest = {
        "generated_at": date.today().isoformat(),
        "workflow": "professional source fetch -> clean country time series -> dynamic ranking video",
        "selected_topics": selected,
        "topics": [],
    }
    for key, df in datasets.items():
        topic = PRO_TOPICS[key]
        item = render_video(key, topic, df, fps=12)
        item["clean_csv"] = str(WORK_DATA / f"{topic['index']}_{key}_clean.csv")
        item["probe"] = ffprobe_video(item["video"])
        item["professional_source"] = topic["source_page"]
        item["source_label"] = topic["source_label"]
        manifest["topics"].append(item)

    path = OUTPUTS / args.manifest_name
    path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(manifest, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
