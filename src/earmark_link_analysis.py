"""
==========================================================
Project : FEC Donor Analysis
Stage   : Earmark Link Analysis

Author  : Abinaya

Description
-----------
Identifies whether transaction IDs ending with 'E'
have corresponding base transactions.

==========================================================
"""

from pathlib import Path
import pandas as pd

# =====================================================
# Paths
# =====================================================

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
    / "earmark_analysis"
)

OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

print("="*70)
print("Loading Dataset")
print("="*70)

df = pd.read_csv(INPUT_FILE, low_memory=False)

print(f"Rows : {len(df):,}")

# =====================================================
# Find E Transactions
# =====================================================

e_rows = df[
    df["transaction_id"]
    .astype(str)
    .str.endswith("E", na=False)
].copy()

print(f"E Transactions : {len(e_rows):,}")

results = []

transaction_lookup = {
    str(t): i
    for i, t in enumerate(df["transaction_id"].astype(str))
}

# =====================================================
# Match Base Transactions
# =====================================================

for _, row in e_rows.iterrows():

    e_id = str(row["transaction_id"])

    base_id = e_id[:-1]

    if base_id in transaction_lookup:

        base = df.iloc[transaction_lookup[base_id]]

        results.append({

            "Base Transaction": base_id,
            "E Transaction": e_id,

            "Same Contributor":
                base["contributor_name"] ==
                row["contributor_name"],

            "Same Amount":
                base["contribution_receipt_amount"] ==
                row["contribution_receipt_amount"],

            "Same Date":
                base["contribution_receipt_date"] ==
                row["contribution_receipt_date"],

            "Same Committee":
                base["committee_id"] ==
                row["committee_id"],

            "Base Memo":
                base["memo_text"],

            "E Memo":
                row["memo_text"]

        })

    else:

        results.append({

            "Base Transaction": base_id,

            "E Transaction": e_id,

            "Same Contributor": False,

            "Same Amount": False,

            "Same Date": False,

            "Same Committee": False,

            "Base Memo": "NOT FOUND",

            "E Memo": row["memo_text"]

        })

# =====================================================
# Save Results
# =====================================================

result_df = pd.DataFrame(results)

result_df.to_csv(

    OUTPUT_FOLDER / "earmark_links.csv",

    index=False

)

unmatched = result_df[
    result_df["Base Memo"] == "NOT FOUND"
]

unmatched.to_csv(

    OUTPUT_FOLDER / "unmatched_earmarks.csv",

    index=False

)

# =====================================================
# Summary
# =====================================================

summary = []

summary.append("="*70)
summary.append("EARMARK LINK ANALYSIS")
summary.append("="*70)

summary.append("")

summary.append(f"Total E Transactions : {len(result_df):,}")

summary.append(
    f"Matched Base Transactions : "
    f"{len(result_df)-len(unmatched):,}"
)

summary.append(
    f"Unmatched : {len(unmatched):,}"
)

summary.append("")

summary.append("Agreement")

summary.append(
    f"Same Contributor : "
    f"{result_df['Same Contributor'].mean()*100:.2f}%"
)

summary.append(
    f"Same Amount : "
    f"{result_df['Same Amount'].mean()*100:.2f}%"
)

summary.append(
    f"Same Date : "
    f"{result_df['Same Date'].mean()*100:.2f}%"
)

summary.append(
    f"Same Committee : "
    f"{result_df['Same Committee'].mean()*100:.2f}%"
)

with open(

    OUTPUT_FOLDER / "earmark_summary.txt",

    "w",

    encoding="utf-8"

) as f:

    f.write("\n".join(summary))

print("\n")
print("="*70)
print("Analysis Completed")
print("="*70)