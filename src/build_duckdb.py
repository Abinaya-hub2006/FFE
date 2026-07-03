"""
==========================================================
Project : FEC Donor Analysis
Stage   : Build DuckDB Database

Author  : Abinaya

Description
-----------
Loads all cleaned receipt CSV files into a DuckDB database.
==========================================================
"""

from pathlib import Path
import duckdb

# ---------------------------------------------------
# Paths
# ---------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

CSV_FOLDER = (
    PROJECT_ROOT
    / "outputs"
    / "receipt_cleaning"
    / "cleaned_receipts"
)

DATABASE_FOLDER = (
    PROJECT_ROOT
    / "outputs"
    / "database"
)

DATABASE_FOLDER.mkdir(parents=True, exist_ok=True)

DATABASE_FILE = DATABASE_FOLDER / "fec_receipts.duckdb"

print("=" * 70)
print("BUILDING FEC DUCKDB DATABASE")
print("=" * 70)

print("\nConnecting...")

con = duckdb.connect(str(DATABASE_FILE))

print("Creating table...")

con.execute(f"""
CREATE OR REPLACE TABLE receipts AS

SELECT *

FROM read_csv_auto(
'{CSV_FOLDER.as_posix()}/*.csv',
union_by_name = true,
ignore_errors = true
)
""")

print("Counting rows...")

rows = con.execute("""
SELECT COUNT(*)
FROM receipts
""").fetchone()[0]

cols = con.execute("""
SELECT COUNT(*)

FROM information_schema.columns

WHERE table_name='receipts'
""").fetchone()[0]

print("\n")
print("=" * 70)
print("DATABASE CREATED SUCCESSFULLY")
print("=" * 70)

print(f"Rows    : {rows:,}")
print(f"Columns : {cols}")

con.close()