# HARD-TIER golden dataset (20 questions) for Redfin Housing Market Tracker text-to-SQL eval.
# Mirrors the IPL hard/brutal style: ratios, thresholds, YoY, rankings, multi-row answers.
#
# Path A convention: "which metro" questions include name + value in gold; the
# evaluator can tolerate name-only OR name+value.
#
# Internal gradient:
#   hard    (1-2 traps) : #1-8
#   brutal  (3+ traps)  : #9-20
#
# Trap vocabulary:
#   - months_of_supply / sale-to-list / price-drop share (ratios)
#   - HAVING / threshold filters (min homes_sold)
#   - latest-period subquery
#   - YoY comparisons
#   - region_type filters (metro vs state vs country)
#   - window functions / one-row-per-group
#   - NULL-safe numeric filters

GOLDEN = [
    # ================= HARD (1-2 traps) =================
    dict(
        id=1,
        diff="hard",
        q="What is the average median sale price across all metro areas in December 2024? Give a single number.",
        sql="""SELECT AVG(median_sale_price) AS avg_median_sale_price
               FROM markets
               WHERE region_type = 'metro' AND period_begin = '2024-12-01'""",
    ),
    dict(
        id=2,
        diff="hard",
        q="Which metro had the highest median sale price in December 2024? Give the metro and the price.",
        sql="""SELECT region_name AS metro, median_sale_price
               FROM markets
               WHERE region_type = 'metro' AND period_begin = '2024-12-01'
               ORDER BY median_sale_price DESC LIMIT 1""",
    ),
    dict(
        id=3,
        diff="hard",
        q="How many metros had at least 2000 homes sold in December 2024?",
        sql="""SELECT COUNT(*) AS n_metros
               FROM markets
               WHERE region_type = 'metro'
                 AND period_begin = '2024-12-01'
                 AND homes_sold >= 2000""",
    ),
    dict(
        id=4,
        diff="hard",
        q="Which metro had the most homes sold in December 2024? Give the metro and the homes sold.",
        sql="""SELECT region_name AS metro, homes_sold
               FROM markets
               WHERE region_type = 'metro' AND period_begin = '2024-12-01'
               ORDER BY homes_sold DESC LIMIT 1""",
    ),
    dict(
        id=5,
        diff="hard",
        q="What was the national median sale price in December 2024? Give a single number.",
        sql="""SELECT median_sale_price
               FROM markets
               WHERE region_type = 'country'
                 AND region_name = 'National'
                 AND period_begin = '2024-12-01'""",
    ),
    dict(
        id=6,
        diff="hard",
        q="Which state had the lowest median days on market in December 2024? Ignore states with missing days-on-market. Give the state and the days.",
        sql="""SELECT region_name AS state, median_dom
               FROM markets
               WHERE region_type = 'state'
                 AND period_begin = '2024-12-01'
                 AND median_dom IS NOT NULL
               ORDER BY median_dom ASC LIMIT 1""",
    ),
    dict(
        id=7,
        diff="hard",
        q="How many total homes were sold across all metros in 2024?",
        sql="""SELECT SUM(homes_sold) AS total_homes_sold
               FROM markets
               WHERE region_type = 'metro'
                 AND period_begin >= '2024-01-01'
                 AND period_begin <= '2024-12-01'""",
    ),
    dict(
        id=8,
        diff="hard",
        q="Which metro had the shortest median days on market in December 2024 among metros with at least 1000 homes sold? Give the metro and the days.",
        sql="""SELECT region_name AS metro, median_dom
               FROM markets
               WHERE region_type = 'metro'
                 AND period_begin = '2024-12-01'
                 AND homes_sold >= 1000
               ORDER BY median_dom ASC LIMIT 1""",
    ),
    # ================= BRUTAL (3+ traps) =================
    dict(
        id=9,
        diff="brutal",
        q="Which metro has the lowest months of supply among metros with at least 500 homes sold in the latest month in this database? Months of supply is the months_of_supply column. Give the metro and the months of supply.",
        sql="""SELECT region_name AS metro, months_of_supply
               FROM markets
               WHERE region_type = 'metro'
                 AND period_begin = (SELECT MAX(period_begin) FROM markets)
                 AND homes_sold >= 500
               ORDER BY months_of_supply ASC LIMIT 1""",
    ),
    dict(
        id=10,
        diff="brutal",
        q="Which metro had the highest average sale-to-list ratio in December 2024 among metros with at least 500 homes sold? Give the metro and the ratio.",
        sql="""SELECT region_name AS metro, avg_sale_to_list
               FROM markets
               WHERE region_type = 'metro'
                 AND period_begin = '2024-12-01'
                 AND homes_sold >= 500
               ORDER BY avg_sale_to_list DESC LIMIT 1""",
    ),
    dict(
        id=11,
        diff="brutal",
        q="Which metro had the largest year-over-year decline in median sale price in December 2023 among metros with at least 500 homes sold? Give the metro and the YoY change.",
        sql="""SELECT region_name AS metro, median_sale_price_yoy
               FROM markets
               WHERE region_type = 'metro'
                 AND period_begin = '2023-12-01'
                 AND homes_sold >= 500
                 AND median_sale_price_yoy IS NOT NULL
               ORDER BY median_sale_price_yoy ASC LIMIT 1""",
    ),
    dict(
        id=12,
        diff="brutal",
        q="For each year from 2021 to 2024, which metro had the highest median sale price in December of that year? Give year, metro, and price, one row per year, ordered by year.",
        sql="""SELECT year, metro, median_sale_price FROM (
                 SELECT CAST(substr(period_begin, 1, 4) AS INTEGER) AS year,
                        region_name AS metro,
                        median_sale_price,
                        RANK() OVER (
                          PARTITION BY substr(period_begin, 1, 4)
                          ORDER BY median_sale_price DESC
                        ) AS rk
                 FROM markets
                 WHERE region_type = 'metro'
                   AND substr(period_begin, 6, 2) = '12'
               ) t
               WHERE rk = 1
               ORDER BY year""",
    ),
    dict(
        id=13,
        diff="brutal",
        q="Which metro had the highest share of active listings with a price drop in December 2024 among metros with at least 5000 active listings (inventory)? Give the metro and the share.",
        sql="""SELECT region_name AS metro, pct_price_drops
               FROM markets
               WHERE region_type = 'metro'
                 AND period_begin = '2024-12-01'
                 AND inventory >= 5000
               ORDER BY pct_price_drops DESC LIMIT 1""",
    ),
    dict(
        id=14,
        diff="brutal",
        q="Among metros in December 2024 with at least 500 homes sold, which had the biggest gap between median new listing price and median sale price (listing minus sale)? Give the metro and the gap.",
        sql="""SELECT region_name AS metro,
                      (median_new_listing_price - median_sale_price) AS list_sale_gap
               FROM markets
               WHERE region_type = 'metro'
                 AND period_begin = '2024-12-01'
                 AND homes_sold >= 500
                 AND median_new_listing_price IS NOT NULL
                 AND median_sale_price IS NOT NULL
               ORDER BY list_sale_gap DESC LIMIT 1""",
    ),
    dict(
        id=15,
        diff="brutal",
        q="What percentage of metros in December 2024 had months of supply greater than 4? Give a single percentage of all metros.",
        sql="""SELECT 100.0 * SUM(CASE WHEN months_of_supply > 4 THEN 1 ELSE 0 END) / COUNT(*) AS pct
               FROM markets
               WHERE region_type = 'metro' AND period_begin = '2024-12-01'""",
    ),
    dict(
        id=16,
        diff="brutal",
        q="Which metro had the largest year-over-year increase in inventory in December 2023 among metros that also saw a year-over-year decline in median sale price? Give the metro and the inventory YoY change.",
        sql="""SELECT region_name AS metro, inventory_yoy
               FROM markets
               WHERE region_type = 'metro'
                 AND period_begin = '2023-12-01'
                 AND inventory_yoy IS NOT NULL
                 AND median_sale_price_yoy < 0
               ORDER BY inventory_yoy DESC LIMIT 1""",
    ),
    dict(
        id=17,
        diff="brutal",
        q="Compute months of supply yourself as inventory divided by homes_sold for December 2024 metros with at least 500 homes sold. Which metro has the lowest computed months of supply? Give the metro and the value.",
        sql="""SELECT region_name AS metro,
                      1.0 * inventory / homes_sold AS computed_months_of_supply
               FROM markets
               WHERE region_type = 'metro'
                 AND period_begin = '2024-12-01'
                 AND homes_sold >= 500
               ORDER BY computed_months_of_supply ASC LIMIT 1""",
    ),
    dict(
        id=18,
        diff="brutal",
        q="Which state had the highest tightness proxy in December 2024: pending sales divided by inventory, among states with at least 5000 inventory? Ignore rows with missing pending_sales or inventory. Give the state and the ratio.",
        sql="""SELECT region_name AS state,
                      1.0 * pending_sales / inventory AS pending_to_inventory
               FROM markets
               WHERE region_type = 'state'
                 AND period_begin = '2024-12-01'
                 AND inventory >= 5000
                 AND pending_sales IS NOT NULL
                 AND inventory IS NOT NULL
               ORDER BY pending_to_inventory DESC LIMIT 1""",
    ),
    dict(
        id=19,
        diff="brutal",
        q="Across 2024, which metro had the highest average median sale price (average of its monthly median_sale_price values) among metros present in all 12 months? Give the metro and the average price.",
        sql="""SELECT region_name AS metro, AVG(median_sale_price) AS avg_price
               FROM markets
               WHERE region_type = 'metro'
                 AND period_begin >= '2024-01-01'
                 AND period_begin <= '2024-12-01'
               GROUP BY region_name
               HAVING COUNT(*) = 12
               ORDER BY avg_price DESC LIMIT 1""",
    ),
    dict(
        id=20,
        diff="brutal",
        q="What is the average first-half-2024 national median sale price (January through June 2024 for the National country row)? Give a single number.",
        sql="""SELECT AVG(median_sale_price) AS avg_h1_national_price
               FROM markets
               WHERE region_type = 'country'
                 AND region_name = 'National'
                 AND period_begin >= '2024-01-01'
                 AND period_begin <= '2024-06-01'""",
    ),
]

if __name__ == "__main__":
    import sqlite3
    from collections import Counter

    DB = "redfin_2021_2024.db"
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    print(f"Validating {len(GOLDEN)} HARD golden queries against {DB}\n")
    ok = 0
    for g in GOLDEN:
        try:
            rows = cur.execute(g["sql"]).fetchall()
            preview = rows[0] if rows else "(empty)"
            print(f"[{g['diff']:6}] #{g['id']:2}  OK  rows={len(rows):<3} sample={str(preview)[:70]}")
            ok += 1
        except Exception as e:
            print(f"[{g['diff']:6}] #{g['id']:2}  FAIL  {e}")
    print(f"\n{ok}/{len(GOLDEN)} passed")
    print("spread:", dict(Counter(g["diff"] for g in GOLDEN)))
    conn.close()
