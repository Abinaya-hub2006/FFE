"""
Stage 11.2a
Generate Donor Identity
"""

import duckdb
from pathlib import Path

# -------------------------------------------------------
# Paths
# -------------------------------------------------------

DB_PATH = "outputs/database/fec_receipts.duckdb"

OUTPUT_DIR = Path("outputs/features")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = OUTPUT_DIR / "donor_identity_sample.csv"

# -------------------------------------------------------
# Connect
# -------------------------------------------------------

con = duckdb.connect(DB_PATH)

print("=" * 60)
print("Stage 11.2a - Donor Identity")
print("=" * 60)

# -------------------------------------------------------
# Create Donor Key Preview
# -------------------------------------------------------

query = """
SELECT

candidate,

contributor_name,

contributor_city,

contributor_state,

contributor_zip,

UPPER(
COALESCE(TRIM(contributor_name),'')
|| '|'
|| COALESCE(TRIM(contributor_city),'')
|| '|'
|| COALESCE(TRIM(contributor_state),'')
|| '|'
|| COALESCE(TRIM(contributor_zip),'')
) AS donor_key

FROM research_receipts

LIMIT 1000;
"""

df = con.execute(query).fetchdf()

df.to_csv(OUTPUT_FILE, index=False)

print()

print("Rows Previewed :", len(df))

print("Unique donor keys :", df["donor_key"].nunique())

print()

print(df.head())

print()

print("Saved :", OUTPUT_FILE)

con.close()