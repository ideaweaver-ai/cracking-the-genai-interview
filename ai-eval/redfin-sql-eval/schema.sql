-- Schema for Text-to-SQL generation prompt
-- Source DB: redfin_2021_2024.db
-- Data: Redfin Housing Market Tracker (monthly), 2021-2024
-- Cite: https://www.redfin.com/news/data-center/

CREATE TABLE "markets" (
  "region_id" INTEGER,
  "region_name" TEXT,
  "region_type" TEXT,              -- metro | state | country
  "metro_state" TEXT,              -- state code for metro rows (may be empty otherwise)
  "period_begin" TEXT,             -- YYYY-MM-DD (month start)
  "period_end" TEXT,               -- YYYY-MM-DD (month end)
  "median_sale_price" REAL,
  "median_new_listing_price" REAL,
  "homes_sold" REAL,
  "pending_sales" REAL,
  "new_listings" REAL,
  "inventory" REAL,                -- active listings
  "median_dom" REAL,               -- median days on market
  "months_of_supply" REAL,
  "avg_sale_to_list" REAL,
  "sold_above_list" REAL,
  "pct_price_drops" REAL,          -- share of active listings with a price drop
  "median_sale_ppsf" REAL,         -- median sale price per sq ft
  "median_sale_price_yoy" REAL,
  "homes_sold_yoy" REAL,
  "inventory_yoy" REAL,
  "months_of_supply_yoy" REAL,
  "median_dom_yoy" REAL
);
