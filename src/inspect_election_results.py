"""
Inspect Election Results Dataset
"""

from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent

FILE = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "senate_general_2022.csv"
)

print("=" * 70)
print("LOADING DATASET")
print("=" * 70)

df = pd.read_csv(FILE)

print("\nShape")
print(df.shape)

print("\nColumns")
print(df.columns.tolist())

print("\nData Types")
print(df.dtypes)

print("\nFirst 20 Rows")
print(df.head(20))

print("\nMissing Values")
print(df.isnull().sum())

print("\nUnique Values Per Column")
print(df.nunique())

print("\nSample Values")
for col in df.columns:
    print(f"\n{col}")
    print(df[col].dropna().unique()[:10])