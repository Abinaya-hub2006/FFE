"""
Stage 11.3
Candidate Time Features
"""

import duckdb
from pathlib import Path

DB_PATH = "outputs/database/fec_receipts.duckdb"

OUTPUT_DIR = Path("outputs/features")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = OUTPUT_DIR / "time_features.csv"

con = duckdb.connect(DB_PATH)

print("=" * 60)
print("Stage 11.3 - Time Features")
print("=" * 60)
query = """
WITH filtered_receipts AS (

SELECT *
FROM research_receipts
WHERE contribution_receipt_date BETWEEN
      DATE '2021-01-01'
  AND DATE '2022-12-31'

),

campaign_dates AS (

SELECT

candidate,

MIN(contribution_receipt_date) AS first_donation,

MAX(contribution_receipt_date) AS last_donation

FROM filtered_receipts

GROUP BY candidate

),

donations AS (

SELECT
    r.*,
    c.first_donation,
    c.last_donation
FROM filtered_receipts r
JOIN campaign_dates c
ON r.candidate = c.candidate

)

SELECT

candidate,

MIN(first_donation) AS first_donation,

MAX(last_donation) AS last_donation,

DATEDIFF(
    'day',
    MIN(first_donation),
    MAX(last_donation)
) AS campaign_duration_days,

COUNT(
    DISTINCT DATE_TRUNC(
        'month',
        contribution_receipt_date
    )
) AS active_months,

SUM(
CASE
WHEN contribution_receipt_date
<= first_donation + INTERVAL 30 DAY
THEN contribution_receipt_amount
ELSE 0
END
) AS first30_amount,

SUM(
CASE
WHEN contribution_receipt_date
>= last_donation - INTERVAL 30 DAY
THEN contribution_receipt_amount
ELSE 0
END
) AS last30_amount,

SUM(contribution_receipt_amount) AS total_amount

FROM donations

GROUP BY candidate

ORDER BY total_amount DESC
"""

df = con.execute(query).fetchdf()

df["first30_ratio"] = df["first30_amount"] / df["total_amount"]
df["last30_ratio"] = df["last30_amount"] / df["total_amount"]

df.drop(columns=["total_amount"], inplace=True)

df.to_csv(OUTPUT_FILE, index=False)

print(df.head())

print()

print("Candidates :", len(df))

print("Saved :", OUTPUT_FILE)

con.close()