"""
==========================================================
Project : FEC Donor Analysis
Stage   : Dataset Profiling
Author  : Abinaya

Description:
    Generates profile for every CSV file.
==========================================================
"""

from pathlib import Path
from datetime import datetime
import pandas as pd

# ==========================================================
# Paths
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_FOLDER = PROJECT_ROOT / "data" / "raw" / "data files"

OUTPUT_FOLDER = PROJECT_ROOT / "outputs" / "data_profile"
OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

profile_rows = []
column_rows = []

csv_files = sorted(DATA_FOLDER.glob("*.csv"))

print(f"\nFound {len(csv_files)} CSV files.\n")

for file in csv_files:

    print(f"Profiling -> {file.name}")

    try:

        df = pd.read_csv(file, low_memory=False)

        profile_rows.append({

            "File Name": file.name,
            "Rows": len(df),
            "Columns": len(df.columns),
            "Missing Values": int(df.isna().sum().sum()),
            "Memory (MB)": round(df.memory_usage(deep=True).sum()/1024/1024,2)

        })

        for col in df.columns:

            column_rows.append({

                "File": file.name,
                "Column": col,
                "Data Type": str(df[col].dtype),
                "Missing": int(df[col].isna().sum())

            })

    except Exception as e:

        profile_rows.append({

            "File Name": file.name,
            "Rows": "ERROR",
            "Columns": "ERROR",
            "Missing Values": str(e),
            "Memory (MB)": "-"

        })

# ==========================================================
# Save CSV Reports
# ==========================================================

profile_df = pd.DataFrame(profile_rows)
column_df = pd.DataFrame(column_rows)

profile_df.to_csv(
    OUTPUT_FOLDER/"dataset_profile.csv",
    index=False
)

column_df.to_csv(
    OUTPUT_FOLDER/"column_summary.csv",
    index=False
)

# ==========================================================
# Save TXT Report
# ==========================================================

report = []

report.append("="*70)
report.append("DATASET PROFILE REPORT")
report.append("="*70)

report.append(f"Generated : {datetime.now()}")

report.append("")
report.append(f"Total Files : {len(csv_files)}")
report.append("")

report.append(profile_df.to_string(index=False))

with open(
    OUTPUT_FOLDER/"dataset_profile.txt",
    "w",
    encoding="utf-8"
) as f:

    for line in report:
        f.write(line+"\n")

print("\n")
print("="*70)
print("Dataset Profiling Completed")
print("="*70)
print(f"Reports saved in : {OUTPUT_FOLDER}")