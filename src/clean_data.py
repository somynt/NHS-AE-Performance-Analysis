"""
Clean the NHS England 'Monthly A&E Time Series' spreadsheet into tidy CSV
tables ready for SQL, Excel and Power BI.

Input : data/raw/Monthly-AE-Time-Series-September-2026.xls
Output: data/clean/dim_month.csv
        data/clean/fact_activity.csv
        data/clean/fact_performance.csv
        data/clean/fact_booked.csv

Run from the project root:  python src/clean_data.py
"""

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "Monthly-AE-Time-Series-September-2026.xls"
CLEAN = ROOT / "data" / "clean"

# Column positions in each sheet (column A is blank, B holds the period)
ACTIVITY_COLS = {
    1: "period",
    2: "att_type1",
    3: "att_type2",
    4: "att_type3",
    5: "att_total",
    6: "adm_via_type1",
    7: "adm_via_type2",
    8: "adm_via_type3_4",
    9: "adm_via_ae_total",
    10: "adm_other",
    11: "adm_total",
    12: "dta_over_4hrs",
    13: "dta_over_12hrs",
}
PERFORMANCE_COLS = {
    1: "period",
    2: "within4_type1",
    3: "within4_type2",
    4: "within4_type3",
    5: "within4_total",
    6: "over4_type1",
    7: "over4_type2",
    8: "over4_type3",
    9: "over4_total",
}
BOOKED_COLS = {
    1: "period",
    2: "booked_type1",
    3: "booked_type2",
    4: "booked_type3",
    5: "booked_total",
    9: "booked_within4_total",
    13: "booked_over4_total",
}


def read_block(sheet: str, header_row: int, columns: dict) -> pd.DataFrame:
    """Read the data block under the header row and keep the listed columns."""
    raw = pd.read_excel(RAW, sheet_name=sheet, header=None, skiprows=header_row + 1)
    df = raw[list(columns)].rename(columns=columns)
    # The reader converts Excel date cells to dates; drop any non-date rows
    df["period"] = pd.to_datetime(df["period"], errors="coerce")
    df = df[df["period"].notna()].copy()
    df["month_start"] = df["period"].dt.to_period("M").dt.to_timestamp()
    df = df.drop(columns="period")

    value_cols = [c for c in df.columns if c != "month_start"]
    df[value_cols] = df[value_cols].apply(pd.to_numeric, errors="coerce")
    # Figures before June 2015 were estimated from weekly data, so they are
    # fractional. Round to whole patients.
    df[value_cols] = df[value_cols].round().astype("Int64")
    return df[["month_start"] + value_cols]


def build_month_dimension(months: pd.Series) -> pd.DataFrame:
    """One row per month with calendar, NHS financial year and data-quality flags."""
    m = pd.DataFrame({"month_start": sorted(months.unique())})
    d = m["month_start"]
    m["month_key"] = d.dt.strftime("%Y%m").astype(int)
    m["year"] = d.dt.year
    m["month_num"] = d.dt.month
    m["month_name"] = d.dt.strftime("%b")
    m["month_label"] = d.dt.strftime("%b %Y")
    # NHS financial year runs April to March, e.g. "2025-26"
    fy_start = d.dt.year.where(d.dt.month >= 4, d.dt.year - 1)
    m["financial_year"] = fy_start.astype(str) + "-" + (fy_start + 1).astype(str).str[-2:]
    m["season"] = d.dt.month.map(
        {12: "Winter", 1: "Winter", 2: "Winter", 3: "Spring", 4: "Spring", 5: "Spring",
         6: "Summer", 7: "Summer", 8: "Summer", 9: "Autumn", 10: "Autumn", 11: "Autumn"}
    )

    # Data-quality flags taken from the notes sheet of the source file
    m["flag_estimated_from_weekly"] = ((d >= "2010-11-01") & (d <= "2015-05-01")).astype(int)
    m["flag_crs_field_test"] = ((d >= "2019-05-01") & (d <= "2023-05-01")).astype(int)
    m["flag_includes_booked"] = (d >= "2020-08-01").astype(int)
    m["flag_cyber_attack_type3"] = ((d >= "2022-08-01") & (d <= "2023-02-01")).astype(int)
    m["flag_covid_period"] = ((d >= "2020-03-01") & (d <= "2021-03-01")).astype(int)
    return m


def main() -> None:
    CLEAN.mkdir(parents=True, exist_ok=True)

    activity = read_block("Activity", 13, ACTIVITY_COLS)
    performance = read_block("Performance", 13, PERFORMANCE_COLS)
    booked = read_block("Booking", 12, BOOKED_COLS)

    month = build_month_dimension(activity["month_start"])
    key = month.set_index("month_start")["month_key"]

    for df in (activity, performance, booked):
        df.insert(0, "month_key", df["month_start"].map(key))

    # Basic checks: one row per month and totals that add up
    for name, df in [("activity", activity), ("performance", performance), ("booked", booked)]:
        assert df["month_key"].is_unique, f"duplicate months in {name}"
    gap = (activity[["att_type1", "att_type2", "att_type3"]].sum(axis=1) - activity["att_total"]).abs()
    assert gap.max() <= 3, "type attendances do not add up to the total"

    month.to_csv(CLEAN / "dim_month.csv", index=False, date_format="%Y-%m-%d")
    activity.drop(columns="month_start").to_csv(CLEAN / "fact_activity.csv", index=False)
    performance.drop(columns="month_start").to_csv(CLEAN / "fact_performance.csv", index=False)
    booked.drop(columns="month_start").to_csv(CLEAN / "fact_booked.csv", index=False)

    print(f"Months: {month['month_label'].iloc[0]} to {month['month_label'].iloc[-1]} ({len(month)})")
    print(f"Activity rows: {len(activity)}, performance rows: {len(performance)}, booked rows: {len(booked)}")


if __name__ == "__main__":
    main()
