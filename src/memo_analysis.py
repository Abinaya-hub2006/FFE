"""
==========================================================
Project : FEC Donor Analysis
Stage   : Memo Analysis

Author  : Abinaya

Description
-----------
Analyzes memo fields across all cleaned receipt datasets.
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
    PROJECT_ROOT
    / "outputs"
    / "receipt_cleaning"
    / "cleaned_receipts"
)

OUTPUT_FOLDER = (
    PROJECT_ROOT
    / "outputs"
    / "memo_analysis"
)

OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

receipt_files = sorted(INPUT_FOLDER.glob("*.csv"))

summary = []
details = []

print("=" * 70)
print("MEMO ANALYSIS")
print("=" * 70)

for file in receipt_files:

    print(f"Processing : {file.name}")

    df = pd.read_csv(file, low_memory=False)

    memo_cols = [
        "memo_code",
        "memo_code_full",
        "memo_text"
    ]

    available = [c for c in memo_cols if c in df.columns]

    if not available:

        continue

    memo_rows = df[
        df[available]
        .notna()
        .any(axis=1)
    ]

    summary.append({

        "File": file.name,
        "Total Rows": len(df),
        "Memo Rows": len(memo_rows)

    })

    for col in available:

        value_counts = (
            memo_rows[col]
            .fillna("NULL")
            .astype(str)
            .str.strip()
            .value_counts()
        )

        for value, count in value_counts.items():

            details.append({

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
    OUTPUT_FOLDER / "memo_summary.csv",
    index=False
)

details_df = pd.DataFrame(details)
details_df.to_csv(
    OUTPUT_FOLDER / "memo_details.csv",
    index=False
)

# =====================================================
# Report
# =====================================================

report = []

report.append("=" * 70)
report.append("MEMO ANALYSIS REPORT")
report.append("=" * 70)
report.append(f"Generated : {datetime.now()}")
report.append("")

report.append(f"Receipt Files Analysed : {len(receipt_files)}")
report.append("")

report.append("Files containing memo rows:")
report.append("")

memo_files = summary_df[
    summary_df["Memo Rows"] > 0
]

for _, row in memo_files.iterrows():

    report.append(
        f"{row['File']} -> {row['Memo Rows']} memo rows"
    )

with open(
    OUTPUT_FOLDER / "memo_report.txt",
    "w",
    encoding="utf-8"
) as f:

    f.write("\n".join(report))

print("\n")
print("=" * 70)
print("Memo Analysis Completed")
print("=" * 70)