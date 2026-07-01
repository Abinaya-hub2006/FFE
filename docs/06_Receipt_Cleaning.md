## Pipeline Improvements (Version 2)

The initial receipt cleaning script was refactored into a reusable pipeline.

### Improvements

- Automatic detection of every receipt file
- Support for split receipt datasets (e.g., Mark Kelly Part0–Part3)
- Individual cleaning report for every file
- Automatic generation of cleaned CSV files
- Master cleaning summary for the entire dataset

### Output

outputs/receipt_cleaning/

- cleaned_receipts/
- cleaning_reports/
- receipt_cleaning_summary.csv