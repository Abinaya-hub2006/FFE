"""
==========================================================
Project : FEC Donor Analysis
Stage   : DuckDB Validation

Author  : Abinaya

Description
-----------
Validates the DuckDB database and generates
a baseline report before preprocessing.
==========================================================
"""

from pathlib import Path
from datetime import datetime
import duckdb

# ======================================================
# Paths
# ======================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DB_FILE = (
    PROJECT_ROOT
    / "outputs"
    / "database"
    / "fec_receipts.duckdb"
)

OUTPUT_FOLDER = (
    PROJECT_ROOT
    / "outputs"
    / "database"
)

REPORT_FILE = OUTPUT_FOLDER / "duckdb_validation_report.txt"

# ======================================================
# Connect
# ======================================================

print("=" * 70)
print("DUCKDB VALIDATION")
print("=" * 70)

con = duckdb.connect(str(DB_FILE))

# ======================================================
# Basic Statistics
# ======================================================

queries = {
    "Total Rows":
        "SELECT COUNT(*) FROM receipts",

    "Total Columns":
        """
        SELECT COUNT(*)
        FROM information_schema.columns
        WHERE table_name='receipts'
        """,

    "Unique Contributors":
        """
        SELECT COUNT(DISTINCT contributor_name)
        FROM receipts
        """,

    "Unique Candidates":
        """
        SELECT COUNT(DISTINCT candidate_id)
        FROM receipts
        """,

    "Unique Committees":
        """
        SELECT COUNT(DISTINCT committee_id)
        FROM receipts
        """,

    "Unique Transactions":
        """
        SELECT COUNT(DISTINCT transaction_id)
        FROM receipts
        """,

    "Duplicate Transaction IDs":
        """
        SELECT COUNT(*) -
               COUNT(DISTINCT transaction_id)
        FROM receipts
        """
}

results = []

print()

for metric, sql in queries.items():

    value = con.execute(sql).fetchone()[0]

    print(f"{metric:<30} {value:,}")

    results.append((metric, value))

# ======================================================
# Entity Types
# ======================================================

entity = con.execute("""

SELECT
    entity_type_desc,
    COUNT(*) AS total

FROM receipts

GROUP BY entity_type_desc

ORDER BY total DESC

""").fetchall()

# ======================================================
# Receipt Types
# ======================================================

receipt = con.execute("""

SELECT
    receipt_type_desc,
    COUNT(*) AS total

FROM receipts

GROUP BY receipt_type_desc

ORDER BY total DESC

LIMIT 20

""").fetchall()

# ======================================================
# Relationship Types
# ======================================================

relationship = con.execute("""

SELECT
    back_reference_schedule_name,
    COUNT(*) AS total

FROM receipts

GROUP BY back_reference_schedule_name

ORDER BY total DESC

""").fetchall()

# ======================================================
# Missing Values
# ======================================================

missing_columns = [

    "contributor_name",
    "candidate_id",
    "committee_id",
    "transaction_id",
    "contribution_receipt_amount",
    "contribution_receipt_date"

]

missing_results = []

for col in missing_columns:

    sql = f"""

    SELECT COUNT(*)

    FROM receipts

    WHERE {col} IS NULL

    """

    value = con.execute(sql).fetchone()[0]

    missing_results.append((col, value))

# ======================================================
# Write Report
# ======================================================

report = []

report.append("=" * 70)
report.append("DUCKDB VALIDATION REPORT")
report.append("=" * 70)

report.append(f"Generated : {datetime.now()}")

report.append("")

report.append("DATABASE SUMMARY")

report.append("-" * 70)

for metric, value in results:

    report.append(f"{metric:<35}{value:,}")

report.append("")
report.append("=" * 70)
report.append("MISSING VALUES")
report.append("=" * 70)

for col, value in missing_results:

    report.append(f"{col:<35}{value:,}")

report.append("")
report.append("=" * 70)
report.append("ENTITY TYPES")
report.append("=" * 70)

for name, total in entity:

    report.append(f"{str(name):<40}{total:,}")

report.append("")
report.append("=" * 70)
report.append("TOP RECEIPT TYPES")
report.append("=" * 70)

for name, total in receipt:

    report.append(f"{str(name):<50}{total:,}")

report.append("")
report.append("=" * 70)
report.append("RELATIONSHIP TYPES")
report.append("=" * 70)

for name, total in relationship:

    report.append(f"{str(name):<20}{total:,}")

with open(REPORT_FILE, "w", encoding="utf-8") as f:

    f.write("\n".join(report))

con.close()

print("\n")
print("=" * 70)
print("VALIDATION COMPLETED")
print("=" * 70)

print(f"\nReport Saved To:\n{REPORT_FILE}")