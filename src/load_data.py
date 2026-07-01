"""
==========================================================
Project : FEC Donor Analysis
Stage   : Data Audit
Author  : Abinaya

Description:
    1. Detect all CSV files
    2. Separate Receipt & Disbursement files
    3. Print dataset summary
    4. Save audit report automatically
==========================================================
"""

from pathlib import Path
from datetime import datetime


# ==========================================================
# Project Paths
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_FOLDER = PROJECT_ROOT / "data" / "raw" / "data files"

OUTPUT_FOLDER = PROJECT_ROOT / "outputs" / "data_audit"

OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

REPORT_FILE = OUTPUT_FOLDER / "data_audit_report.txt"


# ==========================================================
# Load CSV Files
# ==========================================================

csv_files = list(DATA_FOLDER.glob("*.csv"))

receipt_files = []
disbursement_files = []

for file in csv_files:

    name = file.name.lower()

    if "receipt" in name:
        receipt_files.append(file)

    elif "disbursement" in name:
        disbursement_files.append(file)


# ==========================================================
# Create Report
# ==========================================================

report = []

report.append("=" * 70)
report.append("FEC DATA AUDIT REPORT")
report.append("=" * 70)

report.append(f"Generated On : {datetime.now()}")
report.append("")

report.append(f"Total CSV Files       : {len(csv_files)}")
report.append(f"Receipt Files         : {len(receipt_files)}")
report.append(f"Disbursement Files    : {len(disbursement_files)}")

report.append("")
report.append("=" * 70)
report.append("FIRST 10 RECEIPT FILES")
report.append("=" * 70)

for file in receipt_files[:10]:
    report.append(file.name)

report.append("")
report.append("=" * 70)
report.append("FIRST 10 DISBURSEMENT FILES")
report.append("=" * 70)

for file in disbursement_files[:10]:
    report.append(file.name)


# ==========================================================
# Print Report
# ==========================================================

for line in report:
    print(line)


# ==========================================================
# Save Report
# ==========================================================

with open(REPORT_FILE, "w", encoding="utf-8") as f:

    for line in report:
        f.write(line + "\n")

print("\n")
print("=" * 70)
print("Audit Report Saved Successfully")
print(REPORT_FILE)
print("=" * 70)