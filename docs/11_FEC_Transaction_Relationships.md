# FEC Transaction Relationship Discovery

## Objective

The objective of this stage is to investigate how transactions are related within the Federal Election Commission (FEC) receipt datasets.

Unlike previous stages that focused on cleaning and profiling, this stage examines the official relationship fields provided by the FEC to understand how contribution records are linked.

---

## Fields Investigated

- transaction_id
- back_reference_transaction_id
- back_reference_schedule_name
- memo_code
- memo_text

---

## Methodology

Every cleaned receipt dataset was analyzed to identify the relationship patterns used by the FEC.

For each unique schedule type, the following information was collected:

- Number of records
- Number of unique contributors
- Number of unique transactions
- Number of linked transactions
- Most frequent memo descriptions
- Representative sample records

---

## Output Files

outputs/relationship_discovery/

- relationship_report.txt
- schedule_summary.csv
- schedule_details.csv
- schedule_samples.csv

---

## Purpose

The objective of this stage is to reverse engineer the FEC transaction reporting system.

Understanding these relationships is essential before implementing:

- Earmark handling
- Refund detection
- Joint fundraising analysis
- True contribution recovery
- Donor resolution

The discovered relationship patterns will later be converted into preprocessing rules for reconstructing each donor's actual contribution history.

---

## Key Findings

The relationship discovery stage identified **eight distinct transaction relationship types** across all 85 cleaned receipt datasets.

| Relationship Type | Records |
|-------------------|--------:|
| NULL | 5,307,312 |
| SA11AI | 5,213,699 |
| SA12 | 140,351 |
| SA11C | 920 |
| SA15 | 421 |
| SA11D | 38 |
| SC/10 | 13 |
| SA11B | 3 |

### Observations

- Nearly half of the records are standard contribution records with no relationship (`NULL`).
- `SA11AI` is the dominant non-null relationship type and corresponds to earmarked contributions requiring linked transaction handling.
- `SA12` represents a distinct relationship pattern involving linked committee transactions and requires separate processing.
- The remaining schedule types are rare and will be investigated individually before defining preprocessing rules.

### Research Implication

The FEC receipt dataset contains multiple transaction relationship types, each representing different reporting mechanisms. Correctly interpreting these relationships is essential for reconstructing each donor's true contribution history and avoiding duplicate or misattributed donations.

## Status

✅ Completed