"""
Stage 11.6
Receipt Composition Features
"""

import duckdb
from pathlib import Path

DB_PATH = "outputs/database/fec_receipts.duckdb"

OUTPUT_DIR = Path("outputs/features")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = OUTPUT_DIR / "receipt_composition_features.csv"

con = duckdb.connect(DB_PATH)

print("=" * 60)
print("Stage 11.6 - Receipt Composition Features")
print("=" * 60)

query = """
SELECT

candidate,

COUNT(*) AS total_receipts,

SUM(
CASE
WHEN is_individual = TRUE
THEN 1
ELSE 0
END
) AS individual_receipts,

SUM(
CASE
WHEN is_individual = FALSE
THEN 1
ELSE 0
END
) AS committee_receipts,

SUM(
CASE
WHEN memo_code IS NOT NULL
THEN 1
ELSE 0
END
) AS memo_receipts

FROM research_receipts

GROUP BY candidate

ORDER BY total_receipts DESC;
"""

df = con.execute(query).fetchdf()

df["individual_ratio"] = (
    df["individual_receipts"] / df["total_receipts"]
)

df["committee_ratio"] = (
    df["committee_receipts"] / df["total_receipts"]
)

df["memo_ratio"] = (
    df["memo_receipts"] / df["total_receipts"]
)

df.to_csv(OUTPUT_FILE, index=False)

print(df.head())

print()
print("Candidates :", len(df))
print("Saved :", OUTPUT_FILE)

con.close()