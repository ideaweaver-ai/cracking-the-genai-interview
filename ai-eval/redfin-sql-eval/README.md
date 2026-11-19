# Redfin Text-to-SQL Golden Dataset

Student-facing housing analogue of `llm-sql-eval` (IPL cricket), using **public Redfin Housing Market Tracker** data.

> Cite Redfin: https://www.redfin.com/news/data-center/  
> Do **not** scrape redfin.com listings.

## What’s included

| File | Purpose |
|------|---------|
| `data/housing_market_tracker_monthly.csv` | Raw Redfin monthly download |
| `db.py` | Builds `redfin_2021_2024.db` |
| `schema.sql` | Schema text for the LLM prompt |
| `golden_dataset_generator.py` | 20 hard/brutal questions + gold SQL |
| `make_golden_dataset.py` | Runs gold SQL → `golden_dataset.csv` |
| `golden_dataset.csv` | Same columns as the IPL golden set |
| `prompt_example.txt` | Final SYSTEM/USER prompt example |

## CSV columns (same as IPL)

`id, difficulty, question, gold_sql, gold_result_json, n_rows, order_sensitive`

## Rebuild

```bash
# if needed, re-download:
curl -L -A "Mozilla/5.0" -o data/housing_market_tracker_monthly.csv.gz \
  "https://redfin-public-data.s3.us-west-2.amazonaws.com/redfin_html_public_dashboards/housing_market_tracker/housing_market_tracker_monthly.csv.gz"
gunzip -f data/housing_market_tracker_monthly.csv.gz

python3 db.py
python3 golden_dataset_generator.py   # validates gold SQL
python3 make_golden_dataset.py        # writes golden_dataset.csv
```

## Notes for students

- `region_type` is `metro`, `state`, or `country`
- Counts like `homes_sold` can be fractional (Redfin methodology)
- Some state rows have NULLs — gold SQL often filters `IS NOT NULL`
- Only question `#12` is `order_sensitive=TRUE`
