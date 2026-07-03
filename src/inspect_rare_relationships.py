"""
Stage 7.5 - Rare Relationship Inspector
"""

from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent

INPUT_FOLDER = (
    PROJECT_ROOT /
    "outputs" /
    "receipt_cleaning" /
    "cleaned_receipts"
)

OUTPUT_FOLDER = (
    PROJECT_ROOT /
    "outputs" /
    "rare_relationships"
)

OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

RARE = [
    "SA11B",
    "SA11C",
    "SA11D",
    "SA15",
    "SC/10"
]

all_rows = []

for file in sorted(INPUT_FOLDER.glob("*.csv")):

    print("Processing", file.name)

    df = pd.read_csv(file, low_memory=False)

    if "back_reference_schedule_name" not in df.columns:
        continue

    subset = df[
        df["back_reference_schedule_name"].isin(RARE)
    ].copy()

    if subset.empty:
        continue

    subset.insert(0, "Candidate File", file.name)

    cols = [
        "Candidate File",
        "transaction_id",
        "back_reference_transaction_id",
        "back_reference_schedule_name",
        "contributor_name",
        "committee_name",
        "contribution_receipt_amount",
        "memo_code",
        "memo_text"
    ]

    subset = subset[cols]

    all_rows.append(subset)

if all_rows:

    final = pd.concat(all_rows, ignore_index=True)

    final.to_csv(
        OUTPUT_FOLDER / "rare_relationships.csv",
        index=False
    )

    print("\nCompleted.")
    print("Rows:", len(final))

else:

    print("No rare relationships found.")