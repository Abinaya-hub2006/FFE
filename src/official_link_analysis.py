"""
==========================================================
Project : FEC Donor Analysis
Stage   : Official Link Analysis

Author  : Abinaya

Description
-----------
Investigates official FEC linkage fields such as
back_reference_transaction_id and original_sub_id.
==========================================================
"""

from pathlib import Path
import pandas as pd

# ---------------------------------------------------------
# Paths
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

INPUT_FILE = (
    PROJECT_ROOT
    / "outputs"
    / "receipt_cleaning"
    / "cleaned_receipts"
    / "Raphael_Warnock_receipt_cleaned.csv"
)

OUTPUT_FOLDER = (
    PROJECT_ROOT
    / "outputs"
    / "official_link_analysis"
)

OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

print("=" * 70)
print("Loading Dataset")
print("=" * 70)

df = pd.read_csv(INPUT_FILE, low_memory=False)

# ---------------------------------------------------------
# Columns to investigate
# ---------------------------------------------------------

columns = [
    "transaction_id",
    "back_reference_transaction_id",
    "back_reference_schedule_name",
    "sub_id",
    "original_sub_id"
]

available = [c for c in columns if c in df.columns]

print("\nColumns Found")
print("---------------------------")

for c in available:
    print(c)

summary = []

for c in available:

    summary.append({

        "Column": c,
        "Missing Values": int(df[c].isna().sum()),
        "Unique Values": df[c].nunique(dropna=True)

    })

summary_df = pd.DataFrame(summary)

summary_df.to_csv(

    OUTPUT_FOLDER / "back_reference_analysis.csv",

    index=False

)

# ---------------------------------------------------------
# Linked Samples
# ---------------------------------------------------------

sample = df[
    df["back_reference_transaction_id"].notna()
].copy()

sample = sample[[
    "transaction_id",
    "back_reference_transaction_id",
    "back_reference_schedule_name",
    "contributor_name",
    "contribution_receipt_amount",
    "memo_text"
]].head(100)

sample.to_csv(

    OUTPUT_FOLDER / "linked_transaction_samples.csv",

    index=False

)

# ---------------------------------------------------------
# Summary Report
# ---------------------------------------------------------

report = []

report.append("=" * 70)
report.append("OFFICIAL LINK ANALYSIS")
report.append("=" * 70)

report.append("")

report.append(f"Rows : {len(df):,}")

report.append("")

report.append(summary_df.to_string(index=False))

with open(

    OUTPUT_FOLDER / "official_link_summary.txt",

    "w",

    encoding="utf-8"

) as f:

    f.write("\n".join(report))

print("\nAnalysis Completed.")