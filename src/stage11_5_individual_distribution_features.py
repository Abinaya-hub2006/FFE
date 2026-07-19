"""
Stage 11.5
Individual Donation Distribution Features
"""

import duckdb
from pathlib import Path

DB_PATH = "outputs/database/fec_receipts.duckdb"

OUTPUT_DIR = Path("outputs/features")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = OUTPUT_DIR / "individual_distribution_features.csv"

con = duckdb.connect(DB_PATH)

print("=" * 60)
print("Stage 11.5 - Individual Distribution Features")
print("=" * 60)

query = """
SELECT

candidate,

QUANTILE_CONT(contribution_receipt_amount, 0.25) AS individual_q1,

MEDIAN(contribution_receipt_amount) AS individual_median,

QUANTILE_CONT(contribution_receipt_amount, 0.75) AS individual_q3,

STDDEV_SAMP(contribution_receipt_amount) AS individual_std,

VAR_SAMP(contribution_receipt_amount) AS individual_variance,

AVG(contribution_receipt_amount) AS individual_mean

FROM research_receipts

WHERE is_individual = TRUE

GROUP BY candidate

ORDER BY individual_mean DESC;
"""

df = con.execute(query).fetchdf()

df["individual_iqr"] = (
    df["individual_q3"] - df["individual_q1"]
)

df["individual_cv"] = (
    df["individual_std"] / df["individual_mean"]
)

df.drop(columns=["individual_mean"], inplace=True)

df.to_csv(OUTPUT_FILE, index=False)

print(df.head())

print()
print("Candidates :", len(df))
print("Saved :", OUTPUT_FILE)

con.close()