"""
Build a SQLite DB from Redfin's public Housing Market Tracker (monthly).

Source (cite Redfin):
  https://www.redfin.com/news/data-center/housing-market/
  https://redfin-public-data.s3.us-west-2.amazonaws.com/redfin_html_public_dashboards/housing_market_tracker/housing_market_tracker_monthly.csv.gz

Expects:
  data/housing_market_tracker_monthly.csv

Produces:
  redfin_2021_2024.db  with table: markets
"""

import csv
import sqlite3
from pathlib import Path

CSV_PATH = Path("data/housing_market_tracker_monthly.csv")
DB_PATH = "redfin_2021_2024.db"
YEARS = {"2021", "2022", "2023", "2024"}

COLUMN_MAP = {
    "REGION_ID": "region_id",
    "REGION_NAME": "region_name",
    "REGION_TYPE": "region_type",
    "METRO_STATE": "metro_state",
    "PERIOD_BEGIN": "period_begin",
    "PERIOD_END": "period_end",
    "MEDIAN_SALE_PRICE": "median_sale_price",
    "MEDIAN_NEW_LISTING_PRICE": "median_new_listing_price",
    "HOMES_SOLD": "homes_sold",
    "PENDING_SALES_LISTING_UPDATES": "pending_sales",
    "NEW_LISTINGS": "new_listings",
    "ACTIVE_LISTINGS": "inventory",
    "MEDIAN_DAYS_ON_MARKET": "median_dom",
    "MONTHS_OF_SUPPLY": "months_of_supply",
    "AVG_SALE_TO_LIST": "avg_sale_to_list",
    "SOLD_ABOVE_ORIGINAL_LIST": "sold_above_list",
    "PERCENT_ACTIVE_WITH_PRICE_DROPS": "pct_price_drops",
    "MEDIAN_SALE_PPSF": "median_sale_ppsf",
    "MEDIAN_SALE_PRICE_YOY": "median_sale_price_yoy",
    "HOMES_SOLD_YOY": "homes_sold_yoy",
    "ACTIVE_LISTINGS_YOY": "inventory_yoy",
    "MONTHS_OF_SUPPLY_YOY": "months_of_supply_yoy",
    "MEDIAN_DAYS_ON_MARKET_YOY": "median_dom_yoy",
}

OUT_COLS = list(COLUMN_MAP.values())
INT_COLS = {"region_id"}
FLOAT_COLS = {
    c
    for c in OUT_COLS
    if c
    not in {
        "region_id",
        "region_name",
        "region_type",
        "metro_state",
        "period_begin",
        "period_end",
    }
}


def _to_float(v):
    if v is None or str(v).strip() == "":
        return None
    try:
        return round(float(v), 6)
    except ValueError:
        return None


def _to_int(v):
    if v is None or str(v).strip() == "":
        return None
    try:
        return int(float(v))
    except ValueError:
        return None


def main():
    rows_out = []
    with CSV_PATH.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row.get("CONSTRUCTION_CATEGORY") != "All":
                continue
            if row.get("REGION_TYPE") not in {"Metro", "State", "Country"}:
                continue
            begin = row.get("PERIOD_BEGIN") or ""
            if len(begin) < 4 or begin[:4] not in YEARS:
                continue

            out = {}
            for src, dst in COLUMN_MAP.items():
                val = row.get(src, "")
                if dst in INT_COLS:
                    out[dst] = _to_int(val)
                elif dst in FLOAT_COLS:
                    out[dst] = _to_float(val)
                elif dst == "region_type":
                    out[dst] = (val or "").lower()
                elif dst in {"period_begin", "period_end"}:
                    out[dst] = (val or "")[:10]
                else:
                    out[dst] = val
            rows_out.append(out)

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS markets")
    cur.execute(
        """
        CREATE TABLE markets (
            region_id INTEGER,
            region_name TEXT,
            region_type TEXT,
            metro_state TEXT,
            period_begin TEXT,
            period_end TEXT,
            median_sale_price REAL,
            median_new_listing_price REAL,
            homes_sold REAL,
            pending_sales REAL,
            new_listings REAL,
            inventory REAL,
            median_dom REAL,
            months_of_supply REAL,
            avg_sale_to_list REAL,
            sold_above_list REAL,
            pct_price_drops REAL,
            median_sale_ppsf REAL,
            median_sale_price_yoy REAL,
            homes_sold_yoy REAL,
            inventory_yoy REAL,
            months_of_supply_yoy REAL,
            median_dom_yoy REAL
        )
        """
    )
    cur.executemany(
        f"INSERT INTO markets ({', '.join(OUT_COLS)}) VALUES ({', '.join('?' for _ in OUT_COLS)})",
        [tuple(r[c] for c in OUT_COLS) for r in rows_out],
    )
    cur.execute("CREATE INDEX IF NOT EXISTS idx_markets_region ON markets(region_type, region_name)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_markets_period ON markets(period_begin)")
    conn.commit()

    print("--- Verification ---")
    print("rows:", cur.execute("SELECT COUNT(*) FROM markets").fetchone()[0])
    print(
        "by type:",
        cur.execute(
            "SELECT region_type, COUNT(*) FROM markets GROUP BY region_type ORDER BY 1"
        ).fetchall(),
    )
    print(
        "date range:",
        cur.execute("SELECT MIN(period_begin), MAX(period_begin) FROM markets").fetchone(),
    )
    print(
        "metros:",
        cur.execute(
            "SELECT COUNT(DISTINCT region_name) FROM markets WHERE region_type='metro'"
        ).fetchone()[0],
    )
    conn.close()
    print(f"\nDone. Wrote {DB_PATH}")


if __name__ == "__main__":
    main()
