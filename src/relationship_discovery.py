"""
==========================================================
Project : FEC Donor Analysis
Stage   : Relationship Discovery (Version 2)

Author  : Abinaya

Description
-----------
Discovers every relationship type present in the cleaned
receipt datasets using official FEC linkage fields.
==========================================================
"""

from pathlib import Path
from datetime import datetime
import pandas as pd

# ======================================================
# Paths
# ======================================================

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
    "relationship_discovery"
)

OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

receipt_files = sorted(INPUT_FOLDER.glob("*.csv"))

print("=" * 70)
print("FEC RELATIONSHIP DISCOVERY")
print("=" * 70)

summary = []
details = []
samples = []

# ======================================================
# Process Files
# ======================================================

for file in receipt_files:

    print(f"Processing : {file.name}")

    df = pd.read_csv(file, low_memory=False)

    if "back_reference_schedule_name" not in df.columns:
        continue

    df["back_reference_schedule_name"] = (
        df["back_reference_schedule_name"]
        .fillna("NULL")
        .astype(str)
        .str.strip()
    )

    schedules = df["back_reference_schedule_name"].unique()

    for schedule in schedules:

        subset = df[
            df["back_reference_schedule_name"] == schedule
        ]

        summary.append({

            "File": file.name,
            "Schedule": schedule,
            "Rows": len(subset),
            "Unique Contributors":
                subset["contributor_name"].nunique(),

            "Unique Transactions":
                subset["transaction_id"].nunique(),

            "Unique Back References":
                subset["back_reference_transaction_id"].nunique()

        })

        memo_counts = (
            subset["memo_text"]
            .fillna("NULL")
            .astype(str)
            .value_counts()
        )

        for memo, count in memo_counts.items():

            details.append({

                "File": file.name,
                "Schedule": schedule,
                "Memo Text": memo,
                "Count": int(count)

            })

        sample = subset[[
            "transaction_id",
            "back_reference_transaction_id",
            "back_reference_schedule_name",
            "contributor_name",
            "committee_name",
            "contribution_receipt_amount",
            "memo_code",
            "memo_text"
        ]].head(10)

        sample.insert(0, "File", file.name)

        samples.append(sample)

# ======================================================
# Save Outputs
# ======================================================

summary_df = pd.DataFrame(summary)

details_df = pd.DataFrame(details)

samples_df = pd.concat(
    samples,
    ignore_index=True
)

summary_df.to_csv(

    OUTPUT_FOLDER /
    "schedule_summary.csv",

    index=False

)

details_df.to_csv(

    OUTPUT_FOLDER /
    "schedule_details.csv",

    index=False

)

samples_df.to_csv(

    OUTPUT_FOLDER /
    "schedule_samples.csv",

    index=False

)

# ======================================================
# Report
# ======================================================

report = []

report.append("=" * 70)
report.append("FEC RELATIONSHIP DISCOVERY")
report.append("=" * 70)
report.append(f"Generated : {datetime.now()}")
report.append("")

report.append(f"Receipt Files Analysed : {len(receipt_files)}")
report.append("")

report.append("Unique Schedule Types")
report.append("----------------------")

for schedule in sorted(summary_df["Schedule"].unique()):

    total_rows = summary_df[
        summary_df["Schedule"] == schedule
    ]["Rows"].sum()

    report.append(
        f"{schedule} : {total_rows:,} rows"
    )

report.append("")
report.append("Summary")

report.append(
    f"Total Schedule Types : "
    f"{summary_df['Schedule'].nunique()}"
)

report.append(
    f"Total Relationship Records : "
    f"{summary_df['Rows'].sum():,}"
)

with open(

    OUTPUT_FOLDER /
    "relationship_report.txt",

    "w",

    encoding="utf-8"

) as f:

    f.write("\n".join(report))

print("\n")
print("=" * 70)
print("Relationship Discovery Completed")
print("=" * 70)

print(f"Files Processed : {len(receipt_files)}")
print(f"Schedule Types  : {summary_df['Schedule'].nunique()}")