import pandas as pd

from relationship_engine import RelationshipEngine

df = pd.read_csv("all_transactions.csv")

engine = RelationshipEngine()

df = engine.process(df)

df.to_csv(
    "transactions_relationships.csv",
    index=False
)

print(df["relationship_type"].value_counts())