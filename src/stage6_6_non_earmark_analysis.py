import os
import duckdb
import pandas as pd

print("=" * 70)
print("STAGE 6.6 - NON-EARMARK MEMO ANALYSIS")
print("=" * 70)

DB = r"outputs/database/fec_receipts.duckdb"
OUTPUT = r"outputs/memo_analysis"

os.makedirs(OUTPUT, exist_ok=True)

con = duckdb.connect(DB)

# -------------------------------------------------------
# Load memo transactions
# -------------------------------------------------------

df = con.execute("""

SELECT
    transaction_id,
    memo_code,
    memo_text

FROM receipts

WHERE memo_code IS NOT NULL
   OR memo_text IS NOT NULL

""").fetchdf()

print()
print("Total Memo Rows :", len(df))

# -------------------------------------------------------
# Normalize memo text
# -------------------------------------------------------

df["memo_text"] = (
    df["memo_text"]
    .fillna("")
    .str.upper()
    .str.strip()
)

# -------------------------------------------------------
# Identify earmark transactions
# -------------------------------------------------------

earmark_keywords = [
    "EARMARK",
    "EARMARKED",
    "SEE BELOW"
]

pattern = "|".join(earmark_keywords)

df["is_earmark"] = df["memo_text"].str.contains(
    pattern,
    regex=True,
    na=False
)

# -------------------------------------------------------
# Remaining memo rows
# -------------------------------------------------------

remaining = df[~df["is_earmark"]].copy()

print("Non-earmark Memo Rows :", len(remaining))

# -------------------------------------------------------
# Top remaining memo texts
# -------------------------------------------------------

summary = (
    remaining["memo_text"]
    .value_counts(dropna=False)
    .reset_index()
)

summary.columns = ["memo_text", "count"]

summary.to_csv(
    os.path.join(
        OUTPUT,
        "non_earmark_memo_texts.csv"
    ),
    index=False
)

# -------------------------------------------------------
# Report
# -------------------------------------------------------

with open(
    os.path.join(
        OUTPUT,
        "non_earmark_summary.txt"
    ),
    "w",
    encoding="utf-8"
) as f:

    f.write("=" * 70 + "\n")
    f.write("NON-EARMARK MEMO ANALYSIS\n")
    f.write("=" * 70 + "\n\n")

    f.write(f"Total Memo Rows      : {len(df):,}\n")
    f.write(f"Earmark Rows         : {df['is_earmark'].sum():,}\n")
    f.write(f"Non-Earmark Rows     : {len(remaining):,}\n")
    f.write(
        f"Percentage Remaining : {len(remaining)/len(df)*100:.2f}%\n"
    )

print()
print("=" * 70)
print("TOP NON-EARMARK MEMO TEXTS")
print("=" * 70)
print(summary.head(20))