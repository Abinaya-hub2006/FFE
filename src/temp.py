import duckdb

con = duckdb.connect("outputs/database/fec_receipts.duckdb")

cols = con.execute("""
DESCRIBE research_receipts
""").fetchdf()

keywords = [
    "memo",
    "earmark",
    "receipt",
    "transaction",
    "individual",
    "entity",
    "type"
]

for col in cols["column_name"]:
    if any(k in col.lower() for k in keywords):
        print(col)

con.close()