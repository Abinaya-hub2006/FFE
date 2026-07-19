import duckdb
import pandas as pd
from pathlib import Path

DB_PATH = "outputs/database/fec_receipts.duckdb"

OUTPUT_DIR = Path("outputs/features")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = OUTPUT_DIR / "individual_donor_features.csv"

con = duckdb.connect(DB_PATH)

print("="*60)
print("Stage 11.2 - Individual Donor Features")
print("="*60)

query = """
WITH donor_stats AS (

SELECT

candidate,

UPPER(TRIM(COALESCE(contributor_first_name,'')))
|| '|'
|| UPPER(TRIM(COALESCE(contributor_last_name,'')))
|| '|'
|| COALESCE(TRIM(contributor_zip),'') AS donor_key,

COUNT(*) AS donation_count,

SUM(contribution_receipt_amount) AS total_amount

FROM research_receipts

WHERE is_individual = TRUE

GROUP BY
candidate,
donor_key

)

SELECT

candidate,

COUNT(*) AS unique_individual_donors,

SUM(
CASE
WHEN donation_count > 1
THEN 1
ELSE 0
END
) AS repeat_individual_donors,

SUM(donation_count) AS total_individual_donations,

SUM(total_amount) AS total_individual_amount,

AVG(total_amount) AS avg_amount_per_donor,

MAX(donation_count) AS max_donations_single_donor,

MAX(total_amount) AS largest_single_donor

FROM donor_stats

GROUP BY candidate

ORDER BY total_individual_amount DESC;
"""

df = con.execute(query).fetchdf()

df.to_csv(OUTPUT_FILE,index=False)

print(df.head())

print()

print("Candidates :",len(df))

print("Saved :",OUTPUT_FILE)

con.close()