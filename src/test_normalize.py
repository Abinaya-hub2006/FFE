from utils.normalize import *

print("="*60)

examples = [

    "FRIENDS OF SCHUMER",

    "MARK KELLY FOR SENATE",

    "TEAM HERSCHEL, INC.",

    "BLAKE MASTERS FOR SENATE",

    "CT SENATE REPUBLICAN NOMINEE FUND - LEORA LEVY"

]

for e in examples:

    print(e)

    print(tokenize(e))

    print()