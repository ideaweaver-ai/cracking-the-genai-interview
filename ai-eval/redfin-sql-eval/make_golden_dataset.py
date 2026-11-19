"""
Builds golden_dataset.csv from the 20-question Redfin HARD-tier set.

Run:  python3 make_golden_dataset.py
Output: golden_dataset.csv
"""
import csv
import json
import sqlite3

from golden_dataset_generator import GOLDEN

DB = "redfin_2021_2024.db"
OUT = "golden_dataset.csv"

# Only #12 (top metro per year, ordered) is row-order-sensitive.
ORDER_SENSITIVE_IDS = {12}

conn = sqlite3.connect(DB)
cur = conn.cursor()

rows_out = []
for g in GOLDEN:
    cur.execute(g["sql"])
    cols = [d[0] for d in cur.description]
    data = cur.fetchall()
    rows_out.append(
        {
            "id": g["id"],
            "difficulty": g["diff"],
            "question": g["q"],
            "gold_sql": " ".join(g["sql"].split()),
            "gold_result_json": json.dumps(
                {"columns": cols, "rows": [list(r) for r in data]},
                ensure_ascii=False,
            ),
            "n_rows": len(data),
            "order_sensitive": str(g["id"] in ORDER_SENSITIVE_IDS).upper(),
        }
    )
conn.close()

with open(OUT, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(
        f,
        fieldnames=[
            "id",
            "difficulty",
            "question",
            "gold_sql",
            "gold_result_json",
            "n_rows",
            "order_sensitive",
        ],
    )
    w.writeheader()
    w.writerows(rows_out)

print(f"Wrote {OUT} with {len(rows_out)} rows")
