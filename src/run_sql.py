"""
Build a SQLite database from the cleaned CSVs and run every analysis query
in sql/, saving each result to outputs/<query name>.csv.

Run from the project root:  python src/run_sql.py
"""

import sqlite3
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
CLEAN = ROOT / "data" / "clean"
SQL = ROOT / "sql"
OUT = ROOT / "outputs"
DB = ROOT / "data" / "nhs_ae.db"


def build_database(con: sqlite3.Connection) -> None:
    con.executescript((SQL / "00_schema.sql").read_text())
    for table in ["dim_month", "fact_activity", "fact_performance", "fact_booked"]:
        df = pd.read_csv(CLEAN / f"{table}.csv")
        df.to_sql(table, con, if_exists="append", index=False)
    con.commit()


def main() -> None:
    OUT.mkdir(exist_ok=True)
    if DB.exists():
        DB.unlink()

    with sqlite3.connect(DB) as con:
        build_database(con)
        for path in sorted(SQL.glob("[0-9][0-9]_*.sql")):
            if path.name.startswith("00_"):
                continue
            result = pd.read_sql_query(path.read_text(), con)
            result.to_csv(OUT / f"{path.stem}.csv", index=False)
            print(f"\n=== {path.stem} ({len(result)} rows)")
            print(result.head(15).to_string(index=False))


if __name__ == "__main__":
    main()
