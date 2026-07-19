import os
import duckdb
import pandas as pd

print("=" * 70)
print("STAGE 6.5 - TRANSACTION ID PATTERN ANALYSIS")
print("=" * 70)

DB = r"outputs/database/fec_receipts.duckdb"
OUTPUT = r"outputs/memo_analysis"

os.makedirs(OUTPUT, exist_ok=True)

con = duckdb.connect(DB)

# -------------------------------------------------------
# Load research receipts
# -------------------------------------------------------

df = con.execute("""

SELECT

    candidate,
    committee_id,
    committee_name,
    transaction_id,
    contribution_receipt_amount,
    contribution_receipt_date

FROM research_receipts

WHERE transaction_id IS NOT NULL

""").fetchdf()

print()
print("Transactions Loaded :", len(df))

# -------------------------------------------------------
# Identify E transactions
# -------------------------------------------------------

df["transaction_id"] = df["transaction_id"].astype(str)

df["is_e_transaction"] = (
    df["transaction_id"]
    .str.endswith("E")
)

# -------------------------------------------------------
# Base transaction id
# -------------------------------------------------------

df["base_transaction"] = df["transaction_id"]

df.loc[
    df["is_e_transaction"],
    "base_transaction"
] = (
    df.loc[
        df["is_e_transaction"],
        "transaction_id"
    ]
    .str[:-1]
)

# -------------------------------------------------------
# Candidate Summary
# -------------------------------------------------------

summary = []

for candidate, grp in df.groupby("candidate"):

    total = len(grp)

    e_rows = grp["is_e_transaction"].sum()

    example = grp["transaction_id"].iloc[0]

    summary.append({

        "candidate": candidate,
        "committee_id": grp.iloc[0]["committee_id"],
        "committee_name": grp.iloc[0]["committee_name"],
        "total_transactions": total,
        "e_transactions": int(e_rows),
        "uses_E_pattern": "Yes" if e_rows > 0 else "No",
        "sample_transaction_id": example

    })

summary = pd.DataFrame(summary)

summary = summary.sort_values(
    "e_transactions",
    ascending=False
)

summary.to_csv(

    os.path.join(
        OUTPUT,
        "candidate_transaction_patterns.csv"
    ),

    index=False

)

# -------------------------------------------------------
# Validate E links
# -------------------------------------------------------

lookup = set(df["transaction_id"])

e_df = df[df["is_e_transaction"]]

matched = 0

for tid in e_df["base_transaction"]:

    if tid in lookup:

        matched += 1

match_rate = matched / len(e_df) * 100 if len(e_df) else 0

# -------------------------------------------------------
# Report
# -------------------------------------------------------

with open(

    os.path.join(
        OUTPUT,
        "transaction_pattern_summary.txt"
    ),

    "w",

    encoding="utf-8"

) as f:

    f.write("=" * 70 + "\n")
    f.write("TRANSACTION ID PATTERN ANALYSIS\n")
    f.write("=" * 70 + "\n\n")

    f.write(f"Total Transactions : {len(df):,}\n")
    f.write(f"E Transactions     : {len(e_df):,}\n")
    f.write(f"Matched Base IDs   : {matched:,}\n")
    f.write(f"Match Rate         : {match_rate:.2f}%\n\n")

    f.write("Candidates using E pattern:\n")

    count = len(summary[summary["uses_E_pattern"] == "Yes"])

    f.write(f"{count} candidates\n")

print()
print("=" * 70)
print("Completed")
print("=" * 70)
print()

print(summary.head(20))