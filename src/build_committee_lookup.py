import os
import pandas as pd

print("=" * 70)
print("BUILD COMMITTEE LOOKUP TABLE")
print("=" * 70)

ENTITY_FILE = r"outputs/entity_resolution/committee_entity_resolution.csv"

OUTPUT_DIR = r"outputs/lookup"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ----------------------------------------------------

df = pd.read_csv(ENTITY_FILE)

lookup = (
    df[
        [
            "committee_id",
            "committee_name",
            "candidate",
            "state",
            "winner",
            "method"
        ]
    ]
    .drop_duplicates()
    .sort_values("committee_id")
)

lookup.to_csv(

    os.path.join(
        OUTPUT_DIR,
        "committee_lookup.csv"
    ),

    index=False

)

print()

print("Unique Committees :", len(lookup))

print()

print("Saved to")

print(

    os.path.join(
        OUTPUT_DIR,
        "committee_lookup.csv"
    )

)

print()

print("=" * 70)

print("DONE")

print("=" * 70)