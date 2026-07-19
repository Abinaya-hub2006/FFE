"""
Stage 11.7
Merge Candidate Feature Tables
"""

from pathlib import Path
import pandas as pd

FEATURE_DIR = Path("outputs/features")

files = [
    "fundraising_features.csv",
    "individual_donor_features.csv",
    "time_features.csv",
    "distribution_features.csv",
    "individual_distribution_features.csv",
    "receipt_composition_features.csv"
]

print("=" * 60)
print("Stage 11.7 - Merge Candidate Features")
print("=" * 60)

merged = None

for file in files:
    path = FEATURE_DIR / file
    df = pd.read_csv(path)

    print(f"{file:45} {df.shape}")

    if merged is None:
        merged = df
    else:
        merged = merged.merge(df, on="candidate", how="inner")

print("\nFinal Dataset Shape:", merged.shape)

# ---------- Validation ----------

duplicates = merged["candidate"].duplicated().sum()
missing = merged.isnull().sum().sum()

print("Duplicate candidates :", duplicates)
print("Missing values       :", missing)

# ---------- Save ----------

output = FEATURE_DIR / "candidate_features.csv"
merged.to_csv(output, index=False)

print("\nSaved :", output)

print("\nPreview")
print(merged.head())