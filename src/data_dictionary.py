"""
==========================================================
Project : FEC Donor Analysis
Stage   : Data Dictionary
Author  : Abinaya

Description:
Creates a unified data dictionary from all FEC CSV files.
==========================================================
"""

from pathlib import Path
import pandas as pd

# --------------------------------------------------
# Paths
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_FOLDER = PROJECT_ROOT / "data" / "raw" / "data files"

OUTPUT_FOLDER = PROJECT_ROOT / "outputs" / "data_dictionary"
OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

csv_files = sorted(DATA_FOLDER.glob("*.csv"))

column_info = {}

print(f"\nScanning {len(csv_files)} CSV files...\n")

# --------------------------------------------------
# Read every CSV
# --------------------------------------------------

for file in csv_files:

    print(f"Reading : {file.name}")

    try:

        df = pd.read_csv(file, nrows=1000, low_memory=False)

        for col in df.columns:

            if col not in column_info:

                column_info[col] = {

                    "Files Found": 0,
                    "Example Data Type": str(df[col].dtype),
                    "Missing Values": 0

                }

            column_info[col]["Files Found"] += 1
            column_info[col]["Missing Values"] += int(df[col].isna().sum())

    except Exception as e:

        print(file.name, e)

# --------------------------------------------------
# Convert to dataframe
# --------------------------------------------------

rows = []

for col, info in column_info.items():

    rows.append({

        "Column Name": col,
        "Files Present": info["Files Found"],
        "Example Data Type": info["Example Data Type"],
        "Observed Missing Values": info["Missing Values"]

    })

dictionary_df = pd.DataFrame(rows)

dictionary_df = dictionary_df.sort_values(
    by="Files Present",
    ascending=False
)

dictionary_df.to_csv(
    OUTPUT_FOLDER/"data_dictionary.csv",
    index=False
)

with open(
    OUTPUT_FOLDER/"data_dictionary.txt",
    "w",
    encoding="utf-8"
) as f:

    f.write(dictionary_df.to_string(index=False))

print("\n")
print("="*60)
print("DATA DICTIONARY GENERATED")
print("="*60)
print(dictionary_df.head(20))