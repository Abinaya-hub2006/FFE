"""
==========================================================
Project : FEC Donor Analysis
Stage   : Candidate Mapping Investigation

Author  : Abinaya

Description
-----------
Investigates how candidates are represented in the
master DuckDB database.
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
    / "candidate_mapping"
)

OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

REPORT_FILE = OUTPUT_FOLDER / "candidate_mapping_report.txt"

# ======================================================
# Connect
# ======================================================

print("=" * 70)
print("CANDIDATE MAPPING INVESTIGATION")
print("=" * 70)

con = duckdb.connect(str(DB_FILE))

# ======================================================
# Basic Counts
# ======================================================

queries = {
    "Rows":
        "SELECT COUNT(*) FROM receipts",

    "Unique committee_id":
        """
        SELECT COUNT(DISTINCT committee_id)
        FROM receipts
        """,

    "Unique committee_name":
        """
        SELECT COUNT(DISTINCT committee_name)
        FROM receipts
        """,

    "Unique candidate_id":
        """
        SELECT COUNT(DISTINCT candidate_id)
        FROM receipts
        """,

    "Unique candidate_name":
        """
        SELECT COUNT(DISTINCT candidate_name)
        FROM receipts
        """
}

results = []

print()

for title, sql in queries.items():

    value = con.execute(sql).fetchone()[0]

    print(f"{title:<30} {value:,}")

    results.append((title, value))

# ======================================================
# Committee -> Candidate
# ======================================================

committee_candidate = con.execute("""

SELECT

committee_id,

committee_name,

COUNT(DISTINCT candidate_name) AS candidate_count

FROM receipts

GROUP BY
committee_id,
committee_name

ORDER BY candidate_count DESC,
committee_name

""").fetchdf()

committee_candidate.to_csv(

    OUTPUT_FOLDER /
    "committee_candidate_mapping.csv",

    index=False

)

# ======================================================
# Candidate -> Committee
# ======================================================

candidate_committee = con.execute("""

SELECT

candidate_name,

COUNT(DISTINCT committee_id) AS committee_count

FROM receipts

GROUP BY candidate_name

ORDER BY committee_count DESC,
candidate_name

""").fetchdf()

candidate_committee.to_csv(

    OUTPUT_FOLDER /
    "candidate_committee_mapping.csv",

    index=False

)

# ======================================================
# Sample Mapping
# ======================================================

sample = con.execute("""

SELECT DISTINCT

committee_id,

committee_name,

candidate_id,

candidate_name,

candidate_office,

candidate_office_state

FROM receipts

ORDER BY committee_name

LIMIT 200

""").fetchdf()

sample.to_csv(

    OUTPUT_FOLDER /
    "candidate_mapping_samples.csv",

    index=False

)

# ======================================================
# Report
# ======================================================

report = []

report.append("=" * 70)
report.append("CANDIDATE MAPPING REPORT")
report.append("=" * 70)
report.append(f"Generated : {datetime.now()}")
report.append("")

for k, v in results:
    report.append(f"{k:<30}{v:,}")

report.append("")
report.append("=" * 70)
report.append("COMMITTEES WITH MULTIPLE CANDIDATES")
report.append("=" * 70)

multi = committee_candidate[
    committee_candidate["candidate_count"] > 1
]

if len(multi) == 0:
    report.append("None")
else:
    for _, row in multi.iterrows():
        report.append(
            f"{row['committee_name']} ({row['committee_id']}) -> {row['candidate_count']} candidates"
        )

report.append("")
report.append("=" * 70)
report.append("CANDIDATES WITH MULTIPLE COMMITTEES")
report.append("=" * 70)

multi2 = candidate_committee[
    candidate_committee["committee_count"] > 1
]

if len(multi2) == 0:
    report.append("None")
else:
    for _, row in multi2.head(50).iterrows():
        report.append(
            f"{row['candidate_name']} -> {row['committee_count']} committees"
        )

with open(REPORT_FILE, "w", encoding="utf-8") as f:
    f.write("\n".join(report))

con.close()

print("\n")
print("=" * 70)
print("INVESTIGATION COMPLETED")
print("=" * 70)

print(f"\nReport saved to:\n{REPORT_FILE}")