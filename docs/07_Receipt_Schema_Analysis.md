# Receipt Schema Analysis

## Objective

The objective of this stage was to validate the consistency of the cleaned FEC receipt datasets before proceeding to donor matching, memo analysis, feature engineering, and predictive modeling.

This analysis verifies whether all cleaned receipt files follow a consistent schema and identifies any structural differences across candidate datasets.

---

## Methodology

A schema analysis script (`src/receipt_schema_analysis.py`) was executed on all cleaned receipt datasets.

The script performed the following tasks:

- Loaded every cleaned receipt CSV file.
- Counted the total number of rows.
- Counted the total number of columns.
- Compared schema consistency across datasets.
- Generated a schema summary report.

The generated outputs are stored in:

```text
outputs/schema_analysis/
```

Generated files:

- `schema_summary.csv`
- `categorical_values.csv`
- `schema_report.txt`

---

## Dataset Overview

The cleaned receipt datasets contain campaign contribution records collected from multiple U.S. Senate candidates.

### Overall Statistics

| Metric | Value |
|---------|-------|
| Total Receipt Files | **82** |
| Total Contribution Records | **≈ 11.98 Million** |
| Schema Variants | **2** |
| Minimum Columns | **78** |
| Maximum Columns | **79** |

The complete receipt dataset contains approximately **12 million contribution records**, making it suitable for large-scale donor analysis.

---

## Schema Consistency

The schema analysis revealed that every cleaned dataset follows one of only two schema structures:

- **78 Columns**
- **79 Columns**

No unexpected schema variations were observed.

This indicates that the preprocessing pipeline successfully standardized the receipt datasets while preserving important campaign finance information.

---

## Largest Receipt Datasets

The following candidates contain the largest number of contribution records.

| Candidate | Records |
|-----------|--------:|
| Raphael Warnock | 2,107,541 |
| Mark Kelly (Part 0–3 Combined) | 1,255,245 |
| Val Demings | 1,110,298 |
| John Fetterman | 757,268 |
| Catherine Cortez Masto (Part 1–2 Combined) | 620,806 |
| Tim Ryan | 541,729 |

These campaigns represent a significant proportion of the total dataset and may dominate aggregate statistics if appropriate normalization is not performed.

---

## Smallest Receipt Datasets

Several candidates reported relatively few contribution records.

| Candidate | Records |
|-----------|--------:|
| Chase Oliver | 11 |
| Jeremy Kauffman | 35 |
| William Redpath | 41 |
| Marc Victor | 52 |
| Rick Becker | 61 |

Although these datasets are comparatively small, they are retained to preserve the completeness of the campaign finance records.

---

## Key Findings

The schema analysis produced the following observations:

- All receipt datasets were successfully processed.
- Approximately **12 million contribution records** are available for downstream analysis.
- Only **two schema versions** (78 and 79 columns) exist across all receipt datasets.
- No unexpected structural inconsistencies were identified.
- The preprocessing pipeline successfully standardized the receipt datasets.

---

## Importance of this Stage

Schema validation is an essential step before implementing:

- Memo transaction analysis
- Refund detection
- Donor identity resolution
- Feature engineering
- Predictive modeling

Ensuring a consistent schema reduces the likelihood of downstream processing errors and simplifies the implementation of a unified donor analysis pipeline.

---

## Conclusion

The schema summary confirms that the cleaned receipt datasets are structurally consistent and suitable for subsequent stages of the research project.

The preprocessing pipeline has successfully standardized approximately **12 million campaign contribution records** across **82 receipt datasets**, providing a reliable foundation for donor matching, feature extraction, and winner prediction.

---

## Status

✅ Completed