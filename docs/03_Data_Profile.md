# Dataset Profiling

## Objective

The objective of this stage is to inspect every CSV file in the FEC dataset and understand its structure before beginning the data cleaning process.

---

## Methodology

A Python profiling script (`src/data_profile.py`) was executed to automatically analyze every CSV file.

For each dataset, the following information was collected:

- Number of rows
- Number of columns
- Total missing values
- Memory usage
- Column names
- Data types

The generated reports are stored under:

outputs/data_profile/

---

## Generated Files

- dataset_profile.csv
- dataset_profile.txt
- column_summary.csv

---

## Key Findings

### Total Files

- Total CSV Files : **164**

Although the project description mentions 158 files (79 receipt + 79 disbursement), the downloaded dataset contains **164 files** because several large receipt datasets are split into multiple parts (for example, Mark Kelly, Tim Scott, Catherine Cortez Masto).

---

### Dataset Size

The dataset size varies significantly.

Smallest receipt files contain only a few dozen records.

Largest receipt files contain more than **2 million donation records**.

Example:

| Candidate | Rows |
|-----------|------:|
| Raphael Warnock Receipt | 2,107,541 |
| Val Demings Receipt | 1,110,298 |
| John Fetterman Receipt | 757,268 |

---

### Columns

Most receipt files contain **78–79 columns**.

Most disbursement files contain **78 columns**.

This indicates that the FEC schema is highly standardized across candidates.

---

### Missing Values

A considerable number of missing values exist across multiple files.

Many columns such as employer, occupation and memo-related fields contain incomplete information.

This will require careful handling during the data-cleaning stage.

---

### Memory Usage

Large receipt datasets require several gigabytes of memory after loading into Pandas.

Examples:

- Raphael Warnock Receipt → ~5.7 GB
- Val Demings Receipt → ~2.9 GB
- John Fetterman Receipt → ~2.1 GB

Efficient processing strategies may be required for the largest files.

---

## Observations

- Every candidate has a disbursement file.
- Receipt files contain donation records.
- Several high-volume candidates have their receipt files split into multiple parts.
- Dataset schema appears consistent across almost all files.
- The dataset is suitable for building a unified preprocessing pipeline.

---

## Conclusion

The profiling stage confirms that the dataset has a consistent structure and can be processed using a common data-cleaning workflow. The next stage focuses on understanding each column in detail and creating a complete data dictionary before implementing the preprocessing pipeline.

---

## Status

✅ Completed