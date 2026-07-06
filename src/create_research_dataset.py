import duckdb
import pandas as pd
import os

print("=" * 70)
print("CREATE RESEARCH DATASET")
print("=" * 70)

DB = r"outputs/database/fec_receipts.duckdb"

LOOKUP = r"outputs/lookup/committee_lookup.csv"

con = duckdb.connect(DB)

print("\nLoading lookup table...")

lookup = pd.read_csv(LOOKUP)

con.register("lookup_df", lookup)

print("Creating lookup table...")

con.execute("""
DROP TABLE IF EXISTS committee_lookup
""")

con.execute("""
CREATE TABLE committee_lookup AS
SELECT *
FROM lookup_df
""")

print("Creating research_receipts table...")

con.execute("""
DROP TABLE IF EXISTS research_receipts
""")

con.execute("""
CREATE TABLE research_receipts AS

SELECT

    r.*,

    l.candidate,

    l.state,

    l.winner,

    l.method

FROM receipts r

LEFT JOIN committee_lookup l

ON r.committee_id = l.committee_id

""")

print()

rows = con.execute("""

SELECT COUNT(*)

FROM research_receipts

""").fetchone()[0]

cols = con.execute("""

SELECT COUNT(*)

FROM information_schema.columns

WHERE table_name='research_receipts'

""").fetchone()[0]

print("=" * 70)

print("RESEARCH DATASET CREATED")

print("=" * 70)

print()

print("Rows    :", f"{rows:,}")

print("Columns :", cols)

con.close()