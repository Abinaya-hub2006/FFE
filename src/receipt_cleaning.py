"""
==========================================================
Project : FEC Donor Analysis
Stage   : Receipt Cleaning (Version 1)
Author  : Abinaya

Description:
Basic cleaning pipeline for one receipt file.
==========================================================
"""

from pathlib import Path
from datetime import datetime
import pandas as pd

# ---------------------------------------------------------
# Paths
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

INPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "data files"
    / "Brian Bengs receipt.csv"
)

OUTPUT_FOLDER = PROJECT_ROOT / "outputs" / "receipt_cleaning"
OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = OUTPUT_FOLDER / "Brian_Bengs_receipt_cleaned.csv"
REPORT_FILE = OUTPUT_FOLDER / "receipt_cleaning_report.txt"

# ---------------------------------------------------------
# Load Data
# ---------------------------------------------------------

print("\nLoading receipt file...")

df = pd.read_csv(INPUT_FILE, low_memory=False)

original_rows = len(df)

# ---------------------------------------------------------
# Standardize Column Names
# ---------------------------------------------------------

df.columns = (
    df.columns
      .str.strip()
      .str.lower()
)

# ---------------------------------------------------------
# Remove Exact Duplicate Rows
# ---------------------------------------------------------

duplicate_rows = df.duplicated().sum()

df = df.drop_duplicates()

# ---------------------------------------------------------
# Trim Spaces
# ---------------------------------------------------------

object_columns = df.select_dtypes(include="object").columns

for col in object_columns:
    df[col] = df[col].astype(str).str.strip()

# ---------------------------------------------------------
# Standardize Uppercase
# ---------------------------------------------------------

important_columns = [
    "contributor_name",
    "contributor_city",
    "contributor_state",
    "contributor_employer",
    "contributor_occupation"
]

for col in important_columns:

    if col in df.columns:

        df[col] = (
            df[col]
            .fillna("")
            .str.upper()
        )

# ---------------------------------------------------------
# Missing Value Summary
# ---------------------------------------------------------

missing_values = df.isna().sum()

# ---------------------------------------------------------
# Save Cleaned Data
# ---------------------------------------------------------

df.to_csv(
    OUTPUT_FILE,
    index=False
)

# ---------------------------------------------------------
# Cleaning Report
# ---------------------------------------------------------

report = []

report.append("=" * 60)
report.append("RECEIPT CLEANING REPORT")
report.append("=" * 60)
report.append(f"Generated : {datetime.now()}")
report.append("")
report.append(f"Original Rows : {original_rows}")
report.append(f"Final Rows    : {len(df)}")
report.append(f"Duplicates Removed : {duplicate_rows}")
report.append("")
report.append("Top Missing Value Columns")
report.append("-" * 40)

for col, value in missing_values.sort_values(
    ascending=False
).head(15).items():

    report.append(f"{col:<35}{value}")

with open(
    REPORT_FILE,
    "w",
    encoding="utf-8"
) as f:

    for line in report:

        f.write(line + "\n")

print("\nCleaning completed successfully.")
print(f"\nCleaned File : {OUTPUT_FILE}")
print(f"Report       : {REPORT_FILE}")