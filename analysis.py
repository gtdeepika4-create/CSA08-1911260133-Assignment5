"""Daily summaries, SQL examples, charts and simple timing comparisons."""
from pathlib import Path
import sqlite3
import time
import pandas as pd
import matplotlib.pyplot as plt

def daily_summary(rows):
    df = pd.DataFrame(rows)
    if df.empty:
        return df
    return (df.groupby(["station", "date"])["pm25"]
              .agg(minimum="min", maximum="max", mean="mean", valid_count="count")
              .reset_index())

def make_charts(df, output_dir):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    if df.empty:
        return
    # Synthetic sample visualisations
    daily = df.groupby(["date", "station"], as_index=False)["pm25"].mean()
    for station, part in daily.groupby("station"):
        plt.plot(part["date"], part["pm25"], marker="o", label=station)
    plt.title("Daily PM2.5 Trend by Station")
    plt.xlabel("Date"); plt.ylabel("Mean PM2.5"); plt.xticks(rotation=35); plt.legend()
    plt.tight_layout(); plt.savefig(output_dir / "figure1_daily_trend.png"); plt.close()

    means = df.groupby("station")["pm25"].mean()
    means.plot(kind="bar", title="Mean PM2.5 by Station", ylabel="Mean PM2.5")
    plt.tight_layout(); plt.savefig(output_dir / "figure2_station_means.png"); plt.close()

    plt.scatter(df["temperature_c"], df["pm25"], alpha=.7)
    plt.title("Temperature vs PM2.5"); plt.xlabel("Temperature (°C)"); plt.ylabel("PM2.5")
    plt.tight_layout(); plt.savefig(output_dir / "figure3_temperature_scatter.png"); plt.close()

    df.boxplot(column="pm25", by="hour")
    plt.title("PM2.5 Distribution by Hour"); plt.suptitle("")
    plt.xlabel("Hour"); plt.ylabel("PM2.5")
    plt.tight_layout(); plt.savefig(output_dir / "figure4_hourly_boxplot.png"); plt.close()

def main():
    root = Path(__file__).resolve().parents[2]
    csv_path = root / "data" / "air_quality_sample.csv"
    df = pd.read_csv(csv_path)
    df["pm25"] = pd.to_numeric(df["pm25"], errors="coerce")
    df = df[df["pm25"].between(0, 999)].dropna(subset=["pm25"]).copy()
    df["temperature_c"] = pd.to_numeric(df["temperature"], errors="coerce")
    mask = df["temperature_unit"].str.upper().eq("F")
    df.loc[mask, "temperature_c"] = (df.loc[mask, "temperature_c"] - 32) * 5 / 9
    print(daily_summary(df.rename(columns={"date":"date"}).to_dict("records")))
    make_charts(df, root / "output" / "charts")

if __name__ == "__main__":
    main()
