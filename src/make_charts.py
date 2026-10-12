"""
Create the README charts in charts/ from the SQL outputs.

Run after src/run_sql.py:  python src/make_charts.py
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import FuncFormatter, PercentFormatter

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs"
CHARTS = ROOT / "charts"

SURFACE = "#fcfcfb"
INK = "#0b0b0b"
INK_2 = "#52514e"
GRID = "#e4e3df"
BLUE = "#2a78d6"     # series 1: all A&E / main series
ORANGE = "#eb6834"   # series 2: Type 1 major A&E
CAVEAT = "#f0efec"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 10,
    "axes.facecolor": SURFACE,
    "figure.facecolor": SURFACE,
    "axes.edgecolor": GRID,
    "axes.labelcolor": INK_2,
    "xtick.color": INK_2,
    "ytick.color": INK_2,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "axes.grid.axis": "y",
    "grid.color": GRID,
    "grid.linewidth": 0.8,
    "axes.axisbelow": True,
})


def title(ax, text, sub):
    ax.set_title(text, loc="left", fontsize=13, fontweight="bold", color=INK, pad=24)
    ax.text(0, 1.02, sub, transform=ax.transAxes, fontsize=9.5, color=INK_2)


def chart_four_hour():
    df = pd.read_csv(OUT / "03_monthly_trend_rolling.csv", parse_dates=["month_start"])
    df = df[df["pct_within_4h"].notna()]
    fig, ax = plt.subplots(figsize=(10, 5))

    crs = df[df["flag_crs_field_test"] == 1]["month_start"]
    ax.axvspan(crs.min(), crs.max(), color=CAVEAT, zorder=0)
    ax.text(crs.min() + (crs.max() - crs.min()) / 2, 99, "14 trusts missing\nfrom 4-hour data",
            ha="center", va="top", fontsize=8.5, color=INK_2)

    ax.plot(df["month_start"], df["pct_within_4h"], color=BLUE, lw=2, label="All A&E types")
    ax.plot(df["month_start"], df["pct_within_4h_type1"], color=ORANGE, lw=2,
            label="Major A&E (Type 1)")
    ax.axhline(95, color=INK_2, lw=1, ls="--")
    ax.text(pd.Timestamp("2016-06-01"), 95.8, "95% standard", fontsize=8.5, color=INK_2)

    last = df.iloc[-1]
    for col, colr in [("pct_within_4h", BLUE), ("pct_within_4h_type1", ORANGE)]:
        ax.annotate(f"{last[col]:.1f}%", (last["month_start"], last[col]),
                    xytext=(6, 0), textcoords="offset points", va="center",
                    fontsize=9, color=INK, fontweight="bold")
    ax.set_ylim(45, 100)
    ax.yaxis.set_major_formatter(PercentFormatter(decimals=0))
    ax.xaxis.set_major_locator(mdates.YearLocator(2))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    ax.legend(loc="lower left", frameon=False)
    title(ax, "Fewer patients are seen within 4 hours than a decade ago",
          f"Share of A&E patients admitted, transferred or discharged within 4 hours, England, "
          f"Nov 2010 to {last['month_label']}")
    fig.text(0.01, 0.01, "Source: NHS England Monthly A&E Time Series, Sep 2026", fontsize=8, color=INK_2)
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    fig.savefig(CHARTS / "four_hour_performance.png", dpi=150)
    plt.close(fig)


def chart_long_waits():
    df = pd.read_csv(OUT / "07_admissions_and_long_waits.csv")
    fig, ax = plt.subplots(figsize=(10, 4.8))
    bars = ax.bar(df["financial_year"], df["waits_over_12h_for_bed"], color=BLUE, width=0.7)
    for b, v in zip(bars, df["waits_over_12h_for_bed"]):
        if v >= 90000:
            ax.text(b.get_x() + b.get_width() / 2, v + 8000, f"{v/1000:,.0f}k",
                    ha="center", fontsize=8.5, color=INK)
    ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{x/1000:,.0f}k"))
    ax.tick_params(axis="x", rotation=45)
    title(ax, "Waits of 12+ hours for a hospital bed have soared since 2021",
          "Patients waiting more than 12 hours from the decision to admit to being admitted, "
          "England, by NHS financial year")
    fig.text(0.01, 0.01, "Source: NHS England Monthly A&E Time Series, Sep 2026", fontsize=8, color=INK_2)
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    fig.savefig(CHARTS / "twelve_hour_waits.png", dpi=150)
    plt.close(fig)


def chart_seasonality():
    df = pd.read_csv(OUT / "05_seasonality.csv")
    fig, ax = plt.subplots(figsize=(10, 4.5))
    worst = df["avg_pct_within_4h_type1"].idxmin()
    colors = [ORANGE if i == worst else BLUE for i in df.index]
    x = range(len(df))
    ax.plot(x, df["avg_pct_within_4h_type1"], color=GRID, lw=1.5, zorder=1)
    ax.scatter(x, df["avg_pct_within_4h_type1"], s=90, color=colors, zorder=2,
               edgecolors=SURFACE, linewidths=2)
    for i, v in zip(x, df["avg_pct_within_4h_type1"]):
        ax.text(i, v + 0.35, f"{v:.1f}%", ha="center", fontsize=8.5, color=INK)
    ax.set_xticks(list(x), df["month_name"])
    ax.set_ylim(53, 62)
    ax.yaxis.set_major_formatter(PercentFormatter(decimals=0))
    title(ax, "December is the hardest month for major A&E",
          "Average % within 4 hours in Type 1 departments by calendar month, "
          "2022-23 to 2025-26")
    fig.text(0.01, 0.01, "Source: NHS England Monthly A&E Time Series, Sep 2026", fontsize=8, color=INK_2)
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    fig.savefig(CHARTS / "seasonality.png", dpi=150)
    plt.close(fig)


def main():
    CHARTS.mkdir(exist_ok=True)
    chart_four_hour()
    chart_long_waits()
    chart_seasonality()
    print("Charts saved to", CHARTS)


if __name__ == "__main__":
    main()
