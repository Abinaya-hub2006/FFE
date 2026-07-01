"""
==========================================================
Project : FEC Donor Analysis
Stage   : Receipt Cleaning Pipeline (Production Version)

Author  : Abinaya

Description
-----------
1. Automatically detects every receipt file
2. Cleans each receipt dataset
3. Saves cleaned CSV
4. Creates cleaning report
5. Generates master summary
==========================================================
"""

from pathlib import Path
from datetime import datetime
import pandas as pd

# ======================================================
# Paths
# ======================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_FOLDER = PROJECT_ROOT / "data" / "raw" / "data files"

OUTPUT_FOLDER = PROJECT_ROOT / "outputs" / "receipt_cleaning"

CLEAN_FOLDER = OUTPUT_FOLDER / "cleaned_receipts"
REPORT_FOLDER = OUTPUT_FOLDER / "cleaning_reports"

CLEAN_FOLDER.mkdir(parents=True, exist_ok=True)
REPORT_FOLDER.mkdir(parents=True, exist_ok=True)

# ======================================================
# Detect Receipt Files
# ======================================================

receipt_files = sorted(DATA_FOLDER.glob("*receipt*.csv"))

print("=" * 70)
print(f"Receipt Files Found : {len(receipt_files)}")
print("=" * 70)

summary = []

# ======================================================
# Process Every Receipt File
# ======================================================

for file in receipt_files:

    print(f"\nCleaning -> {file.name}")

    df = pd.read_csv(file, low_memory=False)

    original_rows = len(df)

    # ------------------------------------------
    # Standardize Column Names
    # ------------------------------------------

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
    )

    # ------------------------------------------
    # Remove Duplicate Rows
    # ------------------------------------------

    duplicate_rows = df.duplicated().sum()

    df = df.drop_duplicates()

    # ------------------------------------------
    # Trim Spaces
    # ------------------------------------------

    object_columns = df.select_dtypes(
        include=["object", "string"]
    ).columns

    for col in object_columns:

        df[col] = (
            df[col]
            .fillna("")
            .astype(str)
            .str.strip()
        )

    # ------------------------------------------
    # Standardize Important Text
    # ------------------------------------------

    important_columns = [

        "contributor_name",
        "contributor_city",
        "contributor_state",
        "contributor_employer",
        "contributor_occupation"

    ]

    for col in important_columns:

        if col in df.columns:

            df[col] = df[col].str.upper()

    # ------------------------------------------
    # Missing Values
    # ------------------------------------------

    total_missing = int(df.isna().sum().sum())

    # ------------------------------------------
    # Save Cleaned CSV
    # ------------------------------------------

    output_name = file.stem.replace(" ", "_") + "_cleaned.csv"

    df.to_csv(

        CLEAN_FOLDER / output_name,

        index=False

    )

    # ------------------------------------------
    # Individual Report
    # ------------------------------------------

    report = []

    report.append("=" * 60)
    report.append(file.name)
    report.append("=" * 60)

    report.append(f"Generated : {datetime.now()}")
    report.append("")

    report.append(f"Original Rows : {original_rows}")
    report.append(f"Final Rows    : {len(df)}")
    report.append(f"Duplicates Removed : {duplicate_rows}")
    report.append(f"Total Missing Values : {total_missing}")

    report_path = REPORT_FOLDER / (

        file.stem.replace(" ", "_") + "_report.txt"

    )

    with open(

        report_path,

        "w",

        encoding="utf-8"

    ) as f:

        f.write("\n".join(report))

    # ------------------------------------------
    # Master Summary
    # ------------------------------------------

    summary.append({

        "File": file.name,

        "Original Rows": original_rows,

        "Final Rows": len(df),

        "Duplicates Removed": duplicate_rows,

        "Missing Values": total_missing

    })

# ======================================================
# Save Master Summary
# ======================================================

summary_df = pd.DataFrame(summary)

summary_df.to_csv(

    OUTPUT_FOLDER / "receipt_cleaning_summary.csv",

    index=False

)

print("\n")
print("=" * 70)
print("Receipt Cleaning Completed Successfully")
print("=" * 70)
print(f"Receipt Files Processed : {len(receipt_files)}")
print(f"Cleaned Files Folder    : {CLEAN_FOLDER}")
print(f"Reports Folder          : {REPORT_FOLDER}")