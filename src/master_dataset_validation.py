"""
==========================================================
Project : FEC Donor Analysis
Stage   : Master Dataset Validation

Author  : Abinaya

Description
-----------
Validates the master receipt dataset before
starting preprocessing.
==========================================================
"""

from pathlib import Path
from datetime import datetime
import pandas as pd

# ======================================================
# Paths
# ======================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

INPUT_FILE = (
    PROJECT_ROOT
    / "outputs"
    / "master_dataset"
    / "master_receipts.csv"
)

OUTPUT_FOLDER = (
    PROJECT_ROOT
    / "outputs"
    / "master_dataset"
)

print("=" * 70)
print("MASTER DATASET VALIDATION")
print("=" * 70)

print("\nLoading dataset...")

df = pd.read_csv(INPUT_FILE, low_memory=False)

print("Loaded Successfully.\n")

# ======================================================
# Basic Statistics
# ======================================================

rows = len(df)
cols = df.shape[1]

summary = []

summary.append(("Total Rows", rows))
summary.append(("Total Columns", cols))

# ======================================================
# Unique Counts
# ======================================================

summary.append((
    "Unique Contributors",
    df["contributor_name"].nunique(dropna=True)
))

summary.append((
    "Unique Candidates",
    df["candidate_id"].nunique(dropna=True)
))

summary.append((
    "Unique Committees",
    df["committee_id"].nunique(dropna=True)
))

summary.append((
    "Unique Transactions",
    df["transaction_id"].nunique(dropna=True)
))

# ======================================================
# Missing Values
# ======================================================

important_columns = [

    "contributor_name",
    "candidate_id",
    "committee_id",
    "contribution_receipt_amount",
    "contribution_receipt_date",
    "memo_text"

]

for col in important_columns:

    missing = df[col].isna().sum()

    summary.append((

        f"Missing {col}",

        missing

    ))

# ======================================================
# Duplicate Transactions
# ======================================================

duplicates = df["transaction_id"].duplicated().sum()

summary.append((
    "Duplicate transaction_id",
    duplicates
))

# ======================================================
# Entity Types
# ======================================================

entity_counts = (
    df["entity_type_desc"]
    .fillna("NULL")
    .value_counts()
)

receipt_counts = (
    df["receipt_type_desc"]
    .fillna("NULL")
    .value_counts()
)

# ======================================================
# Save Summary CSV
# ======================================================

summary_df = pd.DataFrame(

    summary,

    columns=["Metric", "Value"]

)

summary_df.to_csv(

    OUTPUT_FOLDER /
    "validation_summary.csv",

    index=False

)

# ======================================================
# Report
# ======================================================

report = []

report.append("=" * 70)
report.append("MASTER DATASET VALIDATION REPORT")
report.append("=" * 70)

report.append(f"Generated : {datetime.now()}")

report.append("")

for metric, value in summary:

    report.append(f"{metric:<35} {value:,}")

report.append("")
report.append("=" * 70)
report.append("ENTITY TYPES")
report.append("=" * 70)

for k, v in entity_counts.items():

    report.append(f"{k:<40}{v:,}")

report.append("")
report.append("=" * 70)
report.append("RECEIPT TYPES")
report.append("=" * 70)

for k, v in receipt_counts.items():

    report.append(f"{k:<40}{v:,}")

with open(

    OUTPUT_FOLDER /
    "validation_report.txt",

    "w",

    encoding="utf-8"

) as f:

    f.write("\n".join(report))

print("=" * 70)
print("Validation Completed")
print("=" * 70)

print(summary_df)