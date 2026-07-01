"""
==========================================================
Project : FEC Donor Analysis
Stage   : Receipt Schema Analysis

Author  : Abinaya

Description
-----------
Analyzes cleaned receipt datasets and discovers
all categorical values used in important columns.
==========================================================
"""

from pathlib import Path
import pandas as pd
from datetime import datetime

# =====================================================
# Paths
# =====================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

INPUT_FOLDER = (
    PROJECT_ROOT
    / "outputs"
    / "receipt_cleaning"
    / "cleaned_receipts"
)

OUTPUT_FOLDER = (
    PROJECT_ROOT
    / "outputs"
    / "schema_analysis"
)

OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

# =====================================================
# Columns to Analyze
# =====================================================

TARGET_COLUMNS = [

    "entity_type",
    "entity_type_desc",

    "receipt_type",
    "receipt_type_desc",
    "receipt_type_full",

    "memo_code",
    "memo_code_full",

    "election_type",
    "election_type_full",

    "amendment_indicator",
    "amendment_indicator_desc",

    "is_individual"

]

# =====================================================
# Read Files
# =====================================================

receipt_files = sorted(INPUT_FOLDER.glob("*.csv"))

print("=" * 70)
print(f"Receipt Files : {len(receipt_files)}")
print("=" * 70)

summary = []
categorical = []

# =====================================================
# Process Every File
# =====================================================

for file in receipt_files:

    print(f"Analyzing -> {file.name}")

    df = pd.read_csv(file, low_memory=False)

    summary.append({

        "File": file.name,
        "Rows": len(df),
        "Columns": len(df.columns)

    })

    for col in TARGET_COLUMNS:

        if col in df.columns:

            values = (
                df[col]
                .fillna("NULL")
                .astype(str)
                .str.strip()
                .unique()
            )

            values = sorted(values)

            for value in values:

                count = (
                    df[col]
                    .fillna("NULL")
                    .astype(str)
                    .str.strip()
                    .eq(value)
                    .sum()
                )

                categorical.append({

                    "File": file.name,
                    "Column": col,
                    "Value": value,
                    "Count": int(count)

                })

# =====================================================
# Save CSV
# =====================================================

summary_df = pd.DataFrame(summary)
summary_df.to_csv(
    OUTPUT_FOLDER / "schema_summary.csv",
    index=False
)

categorical_df = pd.DataFrame(categorical)
categorical_df.to_csv(
    OUTPUT_FOLDER / "categorical_values.csv",
    index=False
)

# =====================================================
# Report
# =====================================================

report = []

report.append("=" * 70)
report.append("RECEIPT SCHEMA ANALYSIS")
report.append("=" * 70)
report.append(f"Generated : {datetime.now()}")
report.append("")
report.append(f"Receipt Files Analysed : {len(receipt_files)}")
report.append("")

for column in TARGET_COLUMNS:

    report.append("-" * 60)
    report.append(column.upper())

    if column in categorical_df["Column"].values:

        vals = categorical_df[
            categorical_df["Column"] == column
        ]["Value"].unique()

        for v in sorted(vals):
            report.append(f"   {v}")

    report.append("")

with open(
    OUTPUT_FOLDER / "schema_report.txt",
    "w",
    encoding="utf-8"
) as f:

    f.write("\n".join(report))

print("\n")
print("=" * 70)
print("Schema Analysis Completed")
print("=" * 70)
print(f"Output Folder : {OUTPUT_FOLDER}")