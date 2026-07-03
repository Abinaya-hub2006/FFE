import pandas as pd

from relationship_rules import RULES


class RelationshipEngine:

    def __init__(self):
        self.rules = RULES

    def classify(self, row):

        schedule = str(row.get("schedule_type", "")).upper()

        memo = str(
            row.get("memo_text", "")
        ).lower()

        for rule in self.rules:

            if schedule in rule["schedule"]:

                return rule["name"]

            for keyword in rule["keywords"]:

                if keyword in memo:

                    return rule["name"]

        return "Unknown"

    def process(self, df):

        df["relationship_type"] = df.apply(
            self.classify,
            axis=1
        )

        return df