# Master Receipt Dataset

## Objective

The objective of this stage is to consolidate all cleaned receipt datasets into a single master dataset.

This master dataset becomes the primary input for all subsequent preprocessing and analysis stages.

---

## Methodology

- Loaded all cleaned receipt CSV files.
- Added a `source_file` column to preserve the origin of each record.
- Combined all datasets into one DataFrame.
- Exported the merged dataset.

---

## Outputs

outputs/master_dataset/

- master_receipts.csv
- master_dataset_report.txt

---

## Benefits

Using a single master dataset simplifies:

- Relationship classification
- Donor identity resolution
- Contribution reconstruction
- Feature engineering
- Machine learning

It also ensures that all downstream analyses operate on a consistent and traceable dataset.

---

## Status

✅ Completed