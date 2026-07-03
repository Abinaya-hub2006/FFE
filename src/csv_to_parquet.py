"""
Stage 8A
Convert Master CSV to Parquet
"""

from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent

INPUT = (
    PROJECT_ROOT
    / "outputs"
    / "master_dataset"
    / "master_receipts.csv"
)

OUTPUT = (
    PROJECT_ROOT
    / "outputs"
    / "master_dataset"
    / "master_receipts.parquet"
)

CHUNK_SIZE = 200_000

print("="*60)
print("CSV → PARQUET")
print("="*60)

chunks = []

rows = 0

for chunk in pd.read_csv(INPUT, chunksize=CHUNK_SIZE, low_memory=False):

    rows += len(chunk)

    chunks.append(chunk)

    print(f"Loaded {rows:,} rows")

print("\nConcatenating...")

df = pd.concat(chunks, ignore_index=True)

print("Writing parquet...")

df.to_parquet(
    OUTPUT,
    index=False,
    engine="pyarrow"
)

print("Completed.")