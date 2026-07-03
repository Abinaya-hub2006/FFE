"""
==========================================================
Project : FEC Donor Analysis
Stage   : Master Receipt Dataset Builder

Author  : Abinaya

Description
-----------
Combines every cleaned receipt dataset into one
master dataset for downstream analysis.
==========================================================
"""

from pathlib import Path
from datetime import datetime
import pandas as pd

# =====================================================
# Paths
# =====================================================

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
    "master_dataset"
)

OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

# =====================================================
# Load Files
# =====================================================

receipt_files = sorted(INPUT_FOLDER.glob("*.csv"))

print("=" * 70)
print("MASTER RECEIPT DATASET BUILDER")
print("=" * 70)

print(f"\nReceipt Files Found : {len(receipt_files)}")

master = []

total_rows = 0

for file in receipt_files:

    print(f"Loading : {file.name}")

    df = pd.read_csv(file, low_memory=False)

    # Candidate file name for traceability
    df.insert(
        0,
        "source_file",
        file.name
    )

    master.append(df)

    total_rows += len(df)

# =====================================================
# Merge
# =====================================================

master_df = pd.concat(
    master,
    ignore_index=True
)

# =====================================================
# Save
# =====================================================

output_file = (
    OUTPUT_FOLDER /
    "master_receipts.csv"
)

print("\nSaving Master Dataset...")

master_df.to_csv(
    output_file,
    index=False
)

# =====================================================
# Report
# =====================================================

report = []

report.append("=" * 70)
report.append("MASTER RECEIPT DATASET REPORT")
report.append("=" * 70)

report.append(f"Generated : {datetime.now()}")

report.append("")

report.append(f"Receipt Files Merged : {len(receipt_files)}")
report.append(f"Total Rows           : {len(master_df):,}")
report.append(f"Total Columns        : {master_df.shape[1]}")
report.append(f"Unique Source Files  : {master_df['source_file'].nunique()}")

report.append("")

report.append("Largest Source Files")

largest = (
    master_df
    .groupby("source_file")
    .size()
    .sort_values(ascending=False)
    .head(10)
)

for name, rows in largest.items():

    report.append(f"{name:<45} {rows:,}")

with open(
    OUTPUT_FOLDER /
    "master_dataset_report.txt",
    "w",
    encoding="utf-8"
) as f:

    f.write("\n".join(report))

print("\n")
print("=" * 70)
print("MASTER DATASET CREATED SUCCESSFULLY")
print("=" * 70)

print(f"Rows    : {len(master_df):,}")
print(f"Columns : {master_df.shape[1]}")
print(f"\nSaved to:\n{output_file}")