# FEC Donor Analysis - Project Progress Tracker

Author: Abinaya

Last Updated: 02-07-2026

---

# Overall Goal

Professor kudutha project objective:

> Recover clean donor data from messy FEC filings and identify donors whose contributions consistently back winning candidates.

Raw FEC data direct-a use panna mudiyadhu.

Reason:

- Duplicate reporting
- Memo transactions
- Earmarked contributions
- Joint fundraising
- Refunds
- Linked transactions

So namma first preprocessing pipeline build pannitu irukkom.

---

# Completed Stages

## Stage 1 - Project Setup ✅

Completed

Created project structure

- data/
- docs/
- outputs/
- src/
- notebooks/

GitHub initialized.

---

## Stage 2 - Data Audit ✅

Objective

Dataset structure understand pannadhu.

Completed

- Downloaded Dropbox dataset
- Checked folder structure
- Identified receipt/disbursement files

---

## Stage 3 - Dataset Profiling ✅

Objective

Every dataset profile generate pannadhu.

Completed

Generated

- row counts
- column counts
- missing values

---

## Stage 3.5 - Column Interpretation ✅

Objective

Important columns understand pannadhu.

Studied

- contributor_name
- committee_id
- transaction_id
- memo_code
- memo_text
- receipt_type
- election_type
- contribution_amount

---

## Stage 4 - Receipt Cleaning Pipeline ✅

Created reusable pipeline.

Features

- Auto detect receipt files
- Clean all receipt datasets
- Remove duplicates
- Trim text
- Standardize names
- Generate cleaning reports

Outputs

outputs/receipt_cleaning/

---

## Stage 5 - Schema Analysis ✅

Objective

Understand receipt schema.

Findings

- 85 receipt datasets
- ~12 Million contribution records
- Only 78 & 79 column schemas

Very consistent dataset.

---

## Stage 6 - Memo Analysis ✅

Objective

Understand memo transactions.

Major Findings

Most memo records are NOT refunds.

Largest memo texts:

- NOTE: ABOVE CONTRIBUTION EARMARKED THROUGH THIS ORGANIZATION
- * EARMARKED CONTRIBUTION: SEE BELOW

Conclusion

Memo mostly represents earmarked contributions.

---

## Stage 6.5 - Earmark Link Analysis ✅

Objective

Understand transaction IDs ending with E.

Findings

9998131

↓

9998131E

Every E transaction has matching base transaction.

Amount

100% same

Committee

100% same

Contributor

Different

Conclusion

E transactions represent linked reporting records.

---

## Stage 6.6 - Official Link Analysis ✅

Studied

- back_reference_transaction_id
- back_reference_schedule_name
- sub_id
- original_sub_id

Major Discovery

Official FEC linkage already exists.

Relationship is not inferred.

It is explicitly stored.

---

## Stage 7 - Relationship Discovery ✅

Analysed all 85 receipt files.

Relationship Types Found

NULL

SA11AI

SA11B

SA11C

SA11D

SA12

SA15

SC/10

Important Findings

NULL

↓

Normal contribution

SA11AI

↓

Earmarked contribution

↓

Linked transaction

SA12

↓

Joint fundraising relationship

Other schedules

↓

Need investigation

---

# Research Discoveries

Biggest discoveries till now

1.

Memo != Refund

Most memo entries are earmarked contributions.

---

2.

Transaction IDs ending with E are officially linked.

---

3.

back_reference_transaction_id is the official FEC linkage.

---

4.

Relationship types exist.

Every relationship type requires different preprocessing.

---

# Tomorrow Plan

## Stage 7.5

Relationship Type Investigation

Need to inspect

SA11B

SA11C

SA11D

SA15

SC/10

Need to answer

What does each schedule represent?

Business rule?

Need preprocessing?

---

## Stage 8

Business Rule Engine

Convert discoveries into preprocessing rules.

Example

NULL

↓

Keep

SA11AI

↓

Link paired transaction

SA12

↓

Joint fundraising handling

...

---

## Stage 9

Refund Detection

Identify

- refunds
- redesignations
- reattributions

---

## Stage 10

True Contribution Recovery

Recover actual donor contribution.

Remove duplicate reporting.

---

## Stage 11

Donor Resolution

Merge

JOHN A SMITH

John Smith

JOHN SMITH

↓

One donor

---

## Stage 12

Master Donor Table

Create one row per donor.

Features

- Total contribution
- Number of candidates
- States
- Occupation
- Employer
- Election types
- Winning candidates

---

## Stage 13

Feature Engineering

Prepare ML dataset.

---

## Stage 14

Winner Prediction

Answer professor's question.

Can donor features predict winners?

---

# Current Status

Infrastructure

100% Complete ✅

Research Discovery

~40% Complete

Business Rules

Pending

Machine Learning

Not Started

---

# Git Commands

After today's work

git status

git add .

git commit -m "Completed relationship discovery and FEC linkage analysis"

git push

---

# Tomorrow First Task

Run Stage 7.5

Inspect rare relationship types

SA11B

SA11C

SA11D

SA15

SC/10

Then derive business rules.

DO NOT start ML before completing preprocessing.