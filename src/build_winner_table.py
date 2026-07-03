"""
==========================================================
Project : FEC Donor Analysis
Stage   : Winner Table Creation

Author  : Abinaya

Description
-----------
Creates the official winner lookup table from the
2022 Senate election results.
==========================================================
"""

from pathlib import Path
import pandas as pd
import re

# ======================================================
# Paths
# ======================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

INPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "senate_general_2022.csv"
)

OUTPUT_FOLDER = (
    PROJECT_ROOT
    / "outputs"
    / "winner_mapping"
)

OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

# ======================================================
# Name Standardization
# ======================================================

def standardize_name(name):

    if pd.isna(name):
        return ""

    name = str(name).upper()

    # Remove punctuation
    name = re.sub(r"[.,']", "", name)

    # Remove common suffixes
    remove_words = [
        "JR",
        "SR",
        "II",
        "III",
        "IV",
        "DR",
        "HON",
        "HONORABLE",
        "MR",
        "MRS",
        "MS",
        "SEN",
        "REP"
    ]

    words = []

    for word in name.split():

        if word not in remove_words:
            words.append(word)

    return " ".join(words)

# ======================================================
# Load
# ======================================================

print("="*70)
print("BUILDING WINNER TABLE")
print("="*70)

df = pd.read_csv(INPUT_FILE)

print("\nRows :", len(df))

# ======================================================
# Standardize Names
# ======================================================

df["candidate_standardized"] = df["name"].apply(standardize_name)

# ======================================================
# Winner Detection
# ======================================================

df["winner"] = 0

for state in df["state"].unique():

    idx = df[df["state"] == state]["votes"].idxmax()

    df.loc[idx, "winner"] = 1

# ======================================================
# Rank Candidates
# ======================================================

df["state_rank"] = (
    df.groupby("state")["votes"]
      .rank(method="dense", ascending=False)
      .astype(int)
)

# ======================================================
# Sort
# ======================================================

df = df.sort_values(
    ["state", "votes"],
    ascending=[True, False]
)

# ======================================================
# Save Winner Table
# ======================================================

winner_file = OUTPUT_FOLDER / "winner_mapping.csv"

df.to_csv(
    winner_file,
    index=False
)

# ======================================================
# Report
# ======================================================

report = []

report.append("="*70)
report.append("WINNER TABLE REPORT")
report.append("="*70)
report.append("")

report.append(f"Total Candidates : {len(df)}")
report.append(f"States           : {df['state'].nunique()}")
report.append(f"Winners          : {df['winner'].sum()}")
report.append("")

report.append("="*70)
report.append("STATE WINNERS")
report.append("="*70)

for state in sorted(df["state"].unique()):

    winner = df[
        (df["state"] == state) &
        (df["winner"] == 1)
    ].iloc[0]

    report.append(
        f"{state:<15} -> "
        f"{winner['name']} "
        f"({winner['share %']}%)"
    )

report_file = OUTPUT_FOLDER / "winner_table_report.txt"

with open(report_file, "w", encoding="utf-8") as f:
    f.write("\n".join(report))

print("\n")
print("="*70)
print("WINNER TABLE CREATED")
print("="*70)

print(f"\nSaved : {winner_file}")
print(f"Report: {report_file}")