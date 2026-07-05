import duckdb
import pandas as pd
import os

print("=" * 70)
print("EXTRACT UNIQUE COMMITTEES")
print("=" * 70)

DB = r"outputs/database/fec_receipts.duckdb"

OUTPUT_DIR = r"outputs/entity_resolution"
os.makedirs(OUTPUT_DIR, exist_ok=True)

con = duckdb.connect(DB)

query = """
SELECT DISTINCT
    committee_id,
    committee_name
FROM receipts
WHERE committee_id IS NOT NULL
ORDER BY committee_name;
"""

df = con.execute(query).fetchdf()

print()
print(f"Unique Committees : {len(df):,}")

output_file = os.path.join(
    OUTPUT_DIR,
    "unique_committees.csv"
)

df.to_csv(output_file, index=False)

print()
print("Saved to:")
print(output_file)

con.close()

print()
print("=" * 70)
print("DONE")
print("=" * 70)