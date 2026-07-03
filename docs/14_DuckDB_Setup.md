# DuckDB Database Setup

## Objective

The cleaned receipt datasets were imported into a local DuckDB database.

DuckDB was chosen because the master dataset contains over 10 million records, making full in-memory pandas processing inefficient.

---

## Database

outputs/database/fec_receipts.duckdb

---

## Table

receipts

---

## Benefits

- Fast analytical queries
- SQL support
- Low memory usage
- Works directly with large datasets
- Easy integration with Python

---

## Status

✅ Completed