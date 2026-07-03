# Winner Table Creation

## Objective

Create a clean election results table that assigns a winner for every state in the 2022 Senate election.

---

## Processing Steps

- Load election results
- Standardize candidate names
- Determine winner using highest vote count
- Rank candidates within each state
- Save reusable lookup table

---

## Outputs

outputs/winner_mapping/

- winner_mapping.csv
- winner_table_report.txt

---

## Columns Added

candidate_standardized

winner

state_rank

---

## Purpose

This table will later be linked to the FEC receipt data so every contribution can be associated with either a winning or losing Senate candidate.

---

Status

✅ Completed