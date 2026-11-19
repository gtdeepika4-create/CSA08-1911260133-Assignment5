"""CSV validation, cleaning, normalisation and SQLite storage."""
from __future__ import annotations
import csv
import sqlite3
from datetime import date
from pathlib import Path

REQUIRED = {"station", "date", "hour", "pm25", "pm10", "no", "temperature", "temperature_unit"}

def to_float(value):
    if value is None or str(value).strip() == "" or str(value).strip().upper() == "NA":
        return None
    return float(value)

def fahrenheit_to_celsius(value):
    return (value - 32) * 5 / 9

def load_and_clean(csv_path):
    accepted, rejected = [], []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames:
            raise ValueError("Missing required CSV column(s)")
        missing = REQUIRED - set(reader.fieldnames)
        if missing:
            raise ValueError(f"Missing required CSV column(s): {sorted(missing)}")
        seen = set()
        for line_no, row in enumerate(reader, start=2):
            try:
                station = row["station"].strip().title()
                reading_date = date.fromisoformat(row["date"].strip()).isoformat()
                hour = int(row["hour"])
                if not 0 <= hour <= 23:
                    raise ValueError("invalid hour")
                pm25 = to_float(row["pm25"])
                if pm25 is None:
                    raise ValueError("missing PM2.5")
                if pm25 < 0 or pm25 > 999:
                    raise ValueError("PM2.5 outside demo range 0–999")
                key = (station, reading_date, hour)
                if key in seen:
                    raise ValueError("duplicate station/date/hour key")
                seen.add(key)
                temp = to_float(row["temperature"])
                unit = row["temperature_unit"].strip().upper()
                if temp is not None and unit == "F":
                    temp = fahrenheit_to_celsius(temp)
                elif unit not in {"C", "F"}:
                    raise ValueError("unknown temperature unit")
                accepted.append({
                    "station": station, "date": reading_date, "hour": hour,
                    "pm25": pm25, "pm10": to_float(row["pm10"]), "no": to_float(row["no"]),
                    "temperature_c": temp
                })
            except (ValueError, TypeError) as exc:
                rejected.append({"line": line_no, "reason": str(exc), "row": row})
    return accepted, rejected

def store_sqlite(rows, db_path):
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(db_path) as conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS readings (
            station TEXT NOT NULL, day TEXT NOT NULL, hour INTEGER NOT NULL,
            pm25 REAL, pm10 REAL, no REAL, temperature_c REAL,
            PRIMARY KEY(station, day, hour))""")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_station_day ON readings(station, day)")
        conn.executemany("""INSERT OR REPLACE INTO readings
            (station, day, hour, pm25, pm10, no, temperature_c)
            VALUES (?, ?, ?, ?, ?, ?, ?)""",
            [(r["station"], r["date"], r["hour"], r["pm25"], r["pm10"], r["no"], r["temperature_c"]) for r in rows])
        conn.commit()

def main():
    root = Path(__file__).resolve().parents[2]
    rows, rejected = load_and_clean(root / "data" / "air_quality_sample.csv")
    store_sqlite(rows, root / "output" / "air_quality.db")
    print(f"Accepted: {len(rows)}; rejected: {len(rejected)}")
    for item in rejected:
        print(f"Line {item['line']}: {item['reason']}")

if __name__ == "__main__":
    main()
