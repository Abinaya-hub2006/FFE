import os
import re
import duckdb
import pandas as pd

print("=" * 70)
print("GENERALIZED TRANSACTION SUFFIX ANALYSIS")
print("=" * 70)

DB = r"outputs/database/fec_receipts.duckdb"
OUTPUT = r"outputs/memo_analysis"

os.makedirs(OUTPUT, exist_ok=True)

con = duckdb.connect(DB)

df = con.execute("""

SELECT
    candidate,
    committee_id,
    committee_name,
    transaction_id

FROM research_receipts

WHERE transaction_id IS NOT NULL

""").fetchdf()

df["transaction_id"] = df["transaction_id"].astype(str).str.strip()

# -------------------------------------------------------
# Detect numeric IDs with ONE trailing letter
# -------------------------------------------------------

pattern = re.compile(r"^(\d+)([A-Z])$")

df["has_suffix"] = False
df["base_transaction"] = None
df["suffix"] = None

for idx, tid in df["transaction_id"].items():

    m = pattern.match(tid)

    if m:

        df.at[idx, "has_suffix"] = True
        df.at[idx, "base_transaction"] = m.group(1)
        df.at[idx, "suffix"] = m.group(2)

# -------------------------------------------------------
# Lookup table
# -------------------------------------------------------

lookup = set(df["transaction_id"])

# -------------------------------------------------------
# Candidate Summary
# -------------------------------------------------------

rows = []

for candidate, grp in df.groupby("candidate"):

    suffix_rows = grp[grp["has_suffix"]]

    matched = 0

    for base in suffix_rows["base_transaction"]:

        if base in lookup:
            matched += 1

    suffix_counts = (
        suffix_rows["suffix"]
        .value_counts()
        .to_dict()
    )

    rows.append({

        "candidate": candidate,

        "committee_id": grp.iloc[0]["committee_id"],

        "committee_name": grp.iloc[0]["committee_name"],

        "transactions": len(grp),

        "suffix_transactions": len(suffix_rows),

        "matched_base": matched,

        "match_rate":

            round(
                matched / len(suffix_rows) * 100,
                2
            )

            if len(suffix_rows)

            else None,

        "suffixes": str(suffix_counts),

        "sample_id": grp.iloc[0]["transaction_id"]

    })

summary = pd.DataFrame(rows)

summary = summary.sort_values(
    "suffix_transactions",
    ascending=False
)

summary.to_csv(

    os.path.join(
        OUTPUT,
        "candidate_suffix_analysis.csv"
    ),

    index=False

)

# -------------------------------------------------------
# Overall suffix counts
# -------------------------------------------------------

overall = (

    df[df["has_suffix"]]["suffix"]

    .value_counts()

    .rename_axis("suffix")

    .reset_index(name="count")

)

overall.to_csv(

    os.path.join(
        OUTPUT,
        "overall_suffix_counts.csv"
    ),

    index=False

)

# -------------------------------------------------------
# Report
# -------------------------------------------------------

with open(

    os.path.join(
        OUTPUT,
        "suffix_analysis_report.txt"
    ),

    "w",

    encoding="utf-8"

) as f:

    f.write("=" * 70 + "\n")
    f.write("GENERALIZED SUFFIX ANALYSIS\n")
    f.write("=" * 70 + "\n\n")

    f.write(f"Transactions : {len(df):,}\n\n")

    f.write("Suffix Counts\n\n")

    for _, row in overall.iterrows():

        f.write(
            f"{row['suffix']} : {row['count']:,}\n"
        )

    f.write("\n")

    total_candidates = len(summary)

    suffix_candidates = (
        summary["suffix_transactions"] > 0
    ).sum()

    f.write(
        f"Candidates using suffix IDs : "
        f"{suffix_candidates}/{total_candidates}\n"
    )

print()
print("=" * 70)
print("Completed")
print("=" * 70)
print()

print(summary.head(20))