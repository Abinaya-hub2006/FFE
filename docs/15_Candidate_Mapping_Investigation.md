# Candidate Mapping Investigation

## Objective

The objective of this stage is to determine how recipient candidates are represented within the FEC receipt dataset.

Although the dataset contains `candidate_id` and `candidate_name` fields, preliminary validation showed that `candidate_id` is missing for the vast majority of records. Therefore, this stage investigates whether committees can be reliably mapped to candidates.

---

## Questions Investigated

- How many unique committees exist?
- How many unique candidate names exist?
- Does each committee correspond to one candidate?
- Does a candidate have multiple committees?
- Which field is most suitable as the recipient identifier?

---

## Outputs

outputs/candidate_mapping/

- candidate_mapping_report.txt
- committee_candidate_mapping.csv
- candidate_committee_mapping.csv
- candidate_mapping_samples.csv

---

## Purpose

The findings from this investigation will determine the correct join key for mapping election outcomes (winner/loser) to contribution records.

This decision is critical for answering the project's research question regarding whether donor characteristics predict support for winning candidates.

---

## Status

✅ Completed