"""
Stage 11.4
Distribution Features
"""

import duckdb
from pathlib import Path

DB_PATH = "outputs/database/fec_receipts.duckdb"

OUTPUT_DIR = Path("outputs/features")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = OUTPUT_DIR / "distribution_features.csv"

con = duckdb.connect(DB_PATH)

print("=" * 60)
print("Stage 11.4 - Distribution Features")
print("=" * 60)

query = """
SELECT

candidate,

QUANTILE_CONT(contribution_receipt_amount, 0.25) AS donation_q1,

MEDIAN(contribution_receipt_amount) AS donation_median,

QUANTILE_CONT(contribution_receipt_amount, 0.75) AS donation_q3,

STDDEV_SAMP(contribution_receipt_amount) AS donation_std,

VAR_SAMP(contribution_receipt_amount) AS donation_variance,

AVG(contribution_receipt_amount) AS donation_mean

FROM research_receipts

GROUP BY candidate

ORDER BY donation_mean DESC;
"""

df = con.execute(query).fetchdf()

df["donation_iqr"] = df["donation_q3"] - df["donation_q1"]

df["donation_cv"] = (
    df["donation_std"] / df["donation_mean"]
)

df.drop(columns=["donation_mean"], inplace=True)

df.to_csv(OUTPUT_FILE, index=False)

print(df.head())

print()
print("Candidates :", len(df))
print("Saved :", OUTPUT_FILE)

con.close()