import duckdb
import pandas as pd

DB = "outputs/database/fec_receipts.duckdb"

con = duckdb.connect(DB)

print("=" * 70)
print("INVESTIGATE MISSING STATES")
print("=" * 70)

query = """
SELECT
    committee_id,
    committee_name,
    candidate,
    winner,
    COUNT(*) AS donations
FROM research_receipts
WHERE state IS NULL
GROUP BY
    committee_id,
    committee_name,
    candidate,
    winner
ORDER BY donations DESC
"""

df = con.execute(query).fetchdf()

print(df)

df.to_csv(
    "outputs/entity_resolution/missing_state_committees.csv",
    index=False
)

print()
print("Saved:")
print("outputs/entity_resolution/missing_state_committees.csv")