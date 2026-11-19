"""Small adversarial-input checks for CSV and parameterised SQL."""
import csv
import sqlite3
import tempfile
from pathlib import Path
from tasks.task1_data_cleaning.cleaning import load_and_clean

def run_checks():
    with tempfile.TemporaryDirectory() as tmp:
        p = Path(tmp) / "bad.csv"
        p.write_text("station,date,hour,pm25,pm10,no,temperature,temperature_unit\nAdyar,2026-10-01,27,20,30,2,25,C\n", encoding="utf-8")
        accepted, rejected = load_and_clean(p)
        assert not accepted and "invalid hour" in rejected[0]["reason"]

    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE readings(station TEXT, pm25 REAL)")
    conn.executemany("INSERT INTO readings VALUES (?,?)", [("Adyar", 48.0), ("Guindy", 95.0)])
    payload = "Adyar' OR '1'='1"
    safe = conn.execute("SELECT AVG(pm25) FROM readings WHERE station=?", (payload,)).fetchone()[0]
    assert safe is None
    print("Invalid-hour check: rejected")
    print("Parameterized SQL injection attempt:", safe)

if __name__ == "__main__":
    run_checks()
