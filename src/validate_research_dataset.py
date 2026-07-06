import duckdb

DB = r"outputs/database/fec_receipts.duckdb"

con = duckdb.connect(DB)

print("=" * 70)
print("RESEARCH DATASET VALIDATION")
print("=" * 70)

queries = {

"Rows":

"""
SELECT COUNT(*)
FROM research_receipts
""",

"Unique Candidates":

"""
SELECT COUNT(DISTINCT candidate)
FROM research_receipts
""",

"Winner Donations":

"""
SELECT COUNT(*)
FROM research_receipts
WHERE winner=1
""",

"Loser Donations":

"""
SELECT COUNT(*)
FROM research_receipts
WHERE winner=0
""",

"Missing Candidate":

"""
SELECT COUNT(*)
FROM research_receipts
WHERE candidate IS NULL
"""

}

for name, query in queries.items():

    value = con.execute(query).fetchone()[0]

    print(f"{name:<25} {value:,}")

print()

print("=" * 70)

print("TOP STATES")

print("=" * 70)

print(

con.execute("""

SELECT

state,

COUNT(*) donations

FROM research_receipts

GROUP BY state

ORDER BY donations DESC

LIMIT 10

""").fetchdf()

)

print()

print("=" * 70)

print("TOP CANDIDATES")

print("=" * 70)

print(

con.execute("""

SELECT

candidate,

COUNT(*) donations

FROM research_receipts

GROUP BY candidate

ORDER BY donations DESC

LIMIT 10

""").fetchdf()

)

con.close()