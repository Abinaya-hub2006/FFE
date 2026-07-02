# Memo Analysis

## Objective

The objective of this stage is to identify memo-related transactions present in the cleaned receipt datasets.

Memo records often represent refunds, redesignations, reattributions or other accounting adjustments that affect the calculation of a donor's true contribution amount.

---

## Methodology

All cleaned receipt datasets were scanned for the following fields:

- memo_code
- memo_code_full
- memo_text

For each dataset, the analysis identified:

- Total receipt records
- Number of memo records
- Unique memo values
- Memo frequencies

---

## Output Files

outputs/memo_analysis/

- memo_summary.csv
- memo_details.csv
- memo_report.txt

---

## Purpose

Understanding memo transactions is essential before implementing:

- Refund detection
- True contribution recovery
- Donor aggregation

---

## Key Findings

The memo analysis revealed several important characteristics of the FEC receipt data:

- Memo records are extremely common across large campaigns.
- Most memo records are associated with **earmarked contributions**, rather than refunds.
- The two dominant memo texts are:
  - "NOTE: ABOVE CONTRIBUTION EARMARKED THROUGH THIS ORGANIZATION."
  - "* EARMARKED CONTRIBUTION: SEE BELOW"
- Many transactions appear in linked pairs, where one transaction ID has a corresponding ID ending in the suffix `E` (for example, `9998131` and `9998131E`).
- Refund- and redesignation-related memo texts exist but are comparatively rare.

### Research Implication

These findings suggest that memo records cannot be removed blindly. Instead, earmarked transactions must be analyzed to determine how related records should be linked before calculating each donor's true contribution amount.

## Status

✅ Completed