import os
import re
import duckdb
import pandas as pd

print("=" * 70)
print("TRANSACTION ID FORMAT ANALYSIS")
print("=" * 70)

DB = r"outputs/database/fec_receipts.duckdb"
OUTPUT = r"outputs/memo_analysis"

os.makedirs(OUTPUT, exist_ok=True)

con = duckdb.connect(DB)

# -------------------------------------------------------
# Load data
# -------------------------------------------------------

df = con.execute("""

SELECT
    candidate,
    committee_id,
    committee_name,
    transaction_id

FROM research_receipts

WHERE transaction_id IS NOT NULL

""").fetchdf()

print()
print("Transactions Loaded :", len(df))

df["transaction_id"] = df["transaction_id"].astype(str).str.strip()

# -------------------------------------------------------
# Classify transaction ID
# -------------------------------------------------------

def classify_transaction_id(tid):

    tid = str(tid)

    if re.fullmatch(r"\d+", tid):
        return "Digits Only"

    if re.fullmatch(r"\d+E", tid):
        return "Digits + E"

    if re.fullmatch(r"\d+\.\d+", tid):
        return "Decimal"

    if re.search(r"[A-Za-z]", tid):
        return "Letters"

    return "Other"

df["pattern"] = df["transaction_id"].apply(classify_transaction_id)

# -------------------------------------------------------
# Candidate-wise summary
# -------------------------------------------------------

records = []

for candidate, grp in df.groupby("candidate"):

    counts = grp["pattern"].value_counts()

    records.append({

        "candidate": candidate,

        "committee_id": grp.iloc[0]["committee_id"],

        "committee_name": grp.iloc[0]["committee_name"],

        "total_transactions": len(grp),

        "digits_only": counts.get("Digits Only", 0),

        "digits_plus_E": counts.get("Digits + E", 0),

        "decimal": counts.get("Decimal", 0),

        "letters": counts.get("Letters", 0),

        "other": counts.get("Other", 0),

        "sample_transaction_id": grp.iloc[0]["transaction_id"]

    })

summary = pd.DataFrame(records)

summary = summary.sort_values(
    "candidate"
)

summary.to_csv(

    os.path.join(
        OUTPUT,
        "candidate_transaction_formats.csv"
    ),

    index=False

)

# -------------------------------------------------------
# Overall Summary
# -------------------------------------------------------

overall = df["pattern"].value_counts()

overall.to_csv(

    os.path.join(
        OUTPUT,
        "overall_transaction_patterns.csv"
    )

)

# -------------------------------------------------------
# Text Report
# -------------------------------------------------------

with open(

    os.path.join(
        OUTPUT,
        "transaction_format_report.txt"
    ),

    "w",

    encoding="utf-8"

) as f:

    f.write("=" * 70 + "\n")
    f.write("TRANSACTION ID FORMAT REPORT\n")
    f.write("=" * 70 + "\n\n")

    f.write(f"Total Transactions : {len(df):,}\n\n")

    f.write("Overall Pattern Counts\n\n")

    for pattern, count in overall.items():

        f.write(f"{pattern:20s} : {count:,}\n")

    f.write("\n")

    candidates_using_E = (
        summary["digits_plus_E"] > 0
    ).sum()

    f.write(
        f"Candidates using E pattern : {candidates_using_E}\n"
    )

    candidates_decimal = (
        summary["decimal"] > 0
    ).sum()

    f.write(
        f"Candidates using Decimal IDs : {candidates_decimal}\n"
    )

    candidates_letters = (
        summary["letters"] > 0
    ).sum()

    f.write(
        f"Candidates using Letter IDs : {candidates_letters}\n"
    )

print()
print("=" * 70)
print("Completed")
print("=" * 70)
print()

print(summary.head(20))