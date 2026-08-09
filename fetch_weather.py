#!/usr/bin/env python3
"""
每日天气数据抓取脚本
数据源: Open-Meteo (https://open-meteo.com/) —— 免费、无需 API Key
"""

import csv
import os
import sys
from datetime import datetime, timezone

import requests

# ============ 配置区：按需修改 ============
LOCATION_NAME = "Bukit Mertajam, Penang, MY"
LATITUDE = 5.3667
LONGITUDE = 100.4667
TIMEZONE = "Asia/Kuala_Lumpur"
OUTPUT_CSV = os.path.join(os.path.dirname(__file__), "data", "weather_history.csv")
# ==========================================

API_URL = "https://api.open-meteo.com/v1/forecast"


def fetch_weather():
    params = {
        "latitude": LATITUDE,
        "longitude": LONGITUDE,
        "current": [
            "temperature_2m",
            "relative_humidity_2m",
            "apparent_temperature",
            "precipitation",
            "weather_code",
            "wind_speed_10m",
        ],
        "daily": [
            "temperature_2m_max",
            "temperature_2m_min",
            "precipitation_sum",
            "weather_code",
        ],
        "timezone": TIMEZONE,
    }
    resp = requests.get(API_URL, params=params, timeout=20)
    resp.raise_for_status()
    return resp.json()


def append_to_csv(data):
    os.makedirs(os.path.dirname(OUTPUT_CSV), exist_ok=True)
    file_exists = os.path.isfile(OUTPUT_CSV)

    current = data.get("current", {})
    daily = data.get("daily", {})

    row = {
        "fetched_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "location": LOCATION_NAME,
        "latitude": LATITUDE,
        "longitude": LONGITUDE,
        "current_temperature_c": current.get("temperature_2m"),
        "apparent_temperature_c": current.get("apparent_temperature"),
        "relative_humidity_pct": current.get("relative_humidity_2m"),
        "precipitation_mm": current.get("precipitation"),
        "wind_speed_kmh": current.get("wind_speed_10m"),
        "weather_code": current.get("weather_code"),
        "today_temp_max_c": daily.get("temperature_2m_max", [None])[0],
        "today_temp_min_c": daily.get("temperature_2m_min", [None])[0],
        "today_precipitation_sum_mm": daily.get("precipitation_sum", [None])[0],
    }

    with open(OUTPUT_CSV, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=row.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)

    print(f"已写入一条记录到 {OUTPUT_CSV}")
    print(row)


def main():
    try:
        data = fetch_weather()
    except requests.RequestException as e:
        print(f"请求天气数据失败: {e}", file=sys.stderr)
        sys.exit(1)

    append_to_csv(data)


if __name__ == "__main__":
    main()
