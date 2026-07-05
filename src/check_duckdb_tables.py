import duckdb

DB = r"outputs/database/fec_receipts.duckdb"

con = duckdb.connect(DB)

print("=" * 60)
print("TABLES")
print("=" * 60)

print(con.execute("SHOW TABLES").fetchdf())

con.close()