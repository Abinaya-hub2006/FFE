# Data Dictionary

## Objective

The purpose of this stage is to identify every unique column available across all FEC datasets and determine its availability before beginning data preprocessing.

---

## Methodology

A Python script scanned all CSV files and extracted:

- Column Name
- Number of files containing the column
- Example Data Type
- Missing Values

---

## Output Files

outputs/data_dictionary/

- data_dictionary.csv
- data_dictionary.txt

---

## Observations

- Most columns are common across all receipt and disbursement files.
- The dataset follows a standardized schema.
- Some columns appear only in receipt files or only in disbursement files.
- Several columns contain a significant number of missing values and will require cleaning.

---

## Next Stage

The next stage focuses on understanding the business meaning of each important column such as donor name, transaction amount, memo indicator, election designation and refund-related fields.

---

## Status

✅ Completed