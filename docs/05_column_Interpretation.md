# Column Interpretation

## Category 1 - Donor Information
Purpose:
Used for donor identification and matching.

Important Columns:
- contributor_name
- contributor_first_name
- contributor_last_name
- contributor_city
- contributor_state
- contributor_zip
- contributor_employer
- contributor_occupation

---

## Category 2 - Transaction Information
Purpose:
Used for calculating true donation amounts.

Important Columns:
- contribution_receipt_amount
- contribution_receipt_date
- transaction_id
- contributor_aggregate_ytd

---

## Category 3 - Election Information
Purpose:
Used to distinguish primary/general election contributions.

Important Columns:
- election_type
- election_type_full
- fec_election_year

---

## Category 4 - Memo Information
Purpose:
Used to reconstruct refunds, redesignations and reallocations.

Important Columns:
- memo_code
- memo_code_full
- memo_text