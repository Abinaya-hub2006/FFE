import os
import pandas as pd

INPUT = "outputs/entity_resolution/committee_entity_resolution.csv"
OUTPUT = "outputs/lookup/committee_lookup.csv"

df = pd.read_csv(INPUT)

# Prefer rows with a real state and winner value
df = df.sort_values(
    by=["winner", "state"],
    ascending=[False, True],
    na_position="last"
)

# Keep exactly one row per committee_id
lookup = df.drop_duplicates(
    subset=["committee_id"],
    keep="first"
)

os.makedirs("outputs/lookup", exist_ok=True)

lookup.to_csv(OUTPUT, index=False)

print("=" * 60)
print("Committee Lookup Rebuilt")
print("=" * 60)
print("Rows:", len(lookup))
print("Unique committee_id:", lookup["committee_id"].nunique())