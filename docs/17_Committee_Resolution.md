# Committee Resolution

## Objective

Resolve each campaign committee to its corresponding Senate candidate using rule-based text normalization.

---

## Method

- Extract unique committees from DuckDB
- Normalize committee names
- Normalize candidate names from the election results
- Perform deterministic substring matching
- Separate matched, unmatched, and ambiguous cases

---

## Outputs

outputs/committee_resolution/

- committee_resolution.csv
- unresolved_committees.csv
- multiple_matches.csv
- committee_resolution_report.txt

---

## Purpose

The committee resolution table will be used to assign the correct Senate candidate—and later the winner/loser label—to every contribution record.

---

Status

✅ Completed