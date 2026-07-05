import pandas as pd

from utils.matcher import resolve_committee

election = pd.DataFrame({

    "name":[

        "Kelly, Mark",

        "Rubio, Marco",

        "Warnock, Raphael",

        "Walker, Herschel",

        "Padilla, Alex",

        "Hassan, Maggie",

        "Schumer, Charles",

        "Murray, Patricia"

    ]

})

examples = [

    "MARK KELLY FOR SENATE",

    "TEAM HERSCHEL",

    "WARNOCK FOR GEORGIA",

    "PEOPLE FOR PATTY MURRAY",

    "ALEX PADILLA FOR SENATE",

    "FRIENDS OF SCHUMER",

    "MAGGIE FOR NH"

]

print("="*70)

for committee in examples:

    candidate, method, status = resolve_committee(

        committee,

        election

    )

    print()

    print("Committee :", committee)

    print("Candidate :", candidate)

    print("Method    :", method)

    print("Status    :", status)