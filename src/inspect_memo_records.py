from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent

FILE = (
    PROJECT_ROOT
    / "outputs"
    / "receipt_cleaning"
    / "cleaned_receipts"
    / "Raphael_Warnock_receipt_cleaned.csv"
)

df = pd.read_csv(FILE, low_memory=False)

# Keep only rows with actual memo information
memo = df[
    (
        df["memo_code"].fillna("").astype(str).str.strip() != ""
    ) |
    (
        df["memo_text"].fillna("").astype(str).str.strip() != ""
    )
]

print("="*70)
print("TOTAL MEMO ROWS")
print("="*70)
print(len(memo))

print("\n")

print("="*70)
print("UNIQUE MEMO CODES")
print("="*70)
print(memo["memo_code"].value_counts(dropna=False))

print("\n")

print("="*70)
print("TOP MEMO TEXTS")
print("="*70)
print(memo["memo_text"].value_counts(dropna=False).head(20))

print("\n")

cols = [

    "transaction_id",

    "back_reference_transaction_id",

    "contributor_name",

    "contribution_receipt_amount",

    "memo_code",

    "memo_text"

]

print("="*70)
print("SAMPLE MEMO RECORDS")
print("="*70)

print(memo[cols].head(30))