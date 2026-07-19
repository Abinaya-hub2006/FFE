"""
Stage 11.1
Candidate Fundraising Feature Engineering
"""

import duckdb
import pandas as pd
from pathlib import Path

# ----------------------------------------------------
# Paths
# ----------------------------------------------------

DB_PATH = "outputs/database/fec_receipts.duckdb"

OUTPUT_DIR = Path("outputs/features")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = OUTPUT_DIR / "fundraising_features.csv"

# ----------------------------------------------------
# Connect
# ----------------------------------------------------

con = duckdb.connect(DB_PATH)

print("=" * 60)
print("Stage 11.1 - Fundraising Feature Engineering")
print("=" * 60)

# ----------------------------------------------------
# Aggregate Candidate Statistics
# ----------------------------------------------------

query = """
SELECT

candidate,

state,

winner,

SUM(contribution_receipt_amount)      AS total_amount,

COUNT(*)                              AS donation_count,

AVG(contribution_receipt_amount)      AS avg_donation,

MEDIAN(contribution_receipt_amount)   AS median_donation,

MIN(contribution_receipt_amount)      AS min_donation,

MAX(contribution_receipt_amount)      AS max_donation,

STDDEV_SAMP(contribution_receipt_amount) AS std_donation

FROM research_receipts

GROUP BY

candidate,
state,
winner

ORDER BY total_amount DESC;
"""

df = con.execute(query).fetchdf()

# ----------------------------------------------------
# Save
# ----------------------------------------------------

df.to_csv(OUTPUT_FILE, index=False)

# ----------------------------------------------------
# Summary
# ----------------------------------------------------

print()

print(f"Candidates           : {len(df)}")
print(f"Features             : {len(df.columns)}")
print(f"Output               : {OUTPUT_FILE}")

print()

print(df.head())

print()

print("Stage 11.1 completed successfully.")

con.close()