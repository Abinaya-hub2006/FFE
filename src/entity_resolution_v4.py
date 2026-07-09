import os
import pandas as pd
from datetime import datetime

from utils.matcher import resolve_committee

print("=" * 70)
print("FEC ENTITY RESOLUTION V4")
print("=" * 70)

# -------------------------------------------------------
# Files
# -------------------------------------------------------

COMMITTEE_FILE = r"outputs/entity_resolution/unique_committees.csv"

ELECTION_FILE = r"data/reference/senate_general_2022.csv"
OUTPUT_DIR = r"outputs/entity_resolution"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# -------------------------------------------------------
# Load
# -------------------------------------------------------

committee_df = pd.read_csv(COMMITTEE_FILE)

election_df = pd.read_csv(ELECTION_FILE)

# -------------------------------------------------------
# Normalize election names
# -------------------------------------------------------

election_df["lookup_name"] = (
    election_df["name"]
    .str.upper()
    .str.replace(",", "", regex=False)
    .str.replace(".", "", regex=False)
    .str.strip()
)
# -------------------------------------------------------
# Compute Winner
# -------------------------------------------------------

election_df["winner"] = 0

winner_index = (
    election_df
    .groupby("state")["votes"]
    .idxmax()
)

election_df.loc[winner_index, "winner"] = 1

print()
print("Unique Committees :", len(committee_df))
print("Election Candidates :", len(election_df))

# -------------------------------------------------------
# Resolve
# -------------------------------------------------------

results = []

for _, row in committee_df.iterrows():

    committee_id = row["committee_id"]
    committee_name = row["committee_name"]

    candidate, method, status = resolve_committee(
        committee_name,
        election_df
    )

    state = ""
    winner = None

    if candidate != "":

        lookup_candidate = (
            candidate.upper()
            .replace(",", "")
            .replace(".", "")
            .strip()
        )

        match = election_df[
            election_df["lookup_name"] == lookup_candidate
        ]

        if not match.empty:

            state = match.iloc[0]["state"]
            winner = int(match.iloc[0]["winner"])

    results.append({

        "committee_id": committee_id,
        "committee_name": committee_name,
        "candidate": candidate,
        "state": state,
        "winner": winner,
        "method": method,
        "status": status

    })
# -------------------------------------------------------
# Save
# -------------------------------------------------------

result_df = pd.DataFrame(results)

resolved = result_df[
    result_df["status"] == "Matched"
]

review = result_df[
    result_df["status"] == "Review"
]

resolved.to_csv(

    os.path.join(
        OUTPUT_DIR,
        "committee_entity_resolution.csv"
    ),

    index=False

)

review.to_csv(

    os.path.join(
        OUTPUT_DIR,
        "manual_review.csv"
    ),

    index=False

)

# -------------------------------------------------------
# Report
# -------------------------------------------------------

with open(

    os.path.join(
        OUTPUT_DIR,
        "entity_resolution_report.txt"
    ),

    "w",

    encoding="utf-8"

) as f:

    f.write("=" * 70 + "\n")

    f.write("ENTITY RESOLUTION REPORT\n")

    f.write("=" * 70 + "\n\n")

    f.write(
        f"Generated : {datetime.now()}\n\n"
    )

    f.write(
        f"Committees : {len(result_df):,}\n"
    )

    f.write(
        f"Matched    : {len(resolved):,}\n"
    )

    f.write(
        f"Review     : {len(review):,}\n"
    )

print()

print("=" * 70)

print("Completed")

print("=" * 70)

print()

print()
print("Total rows in result_df:", len(result_df))
print()

print(result_df.head(10))