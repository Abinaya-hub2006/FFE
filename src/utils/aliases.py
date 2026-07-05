"""
Alias Dictionary

Maps committee words to official election candidate names.

Used before token matching.
"""

# -------------------------------------------------------
# Nickname -> Official First Name
# -------------------------------------------------------

FIRST_NAME_ALIASES = {

    "CHUCK": "CHARLES",
    "DICK": "RICHARD",
    "PATTY": "PATRICIA",
    "TED": "THEODORE",
    "JD": "J D",
    "JOE": "JOSEPH",
    "MIKE": "MICHAEL",
    "TAMMY": "TAMMY",
    "CHRIS": "CHRISTOPHER",
    "MARKWAYNE": "MARKWAYNE",
    "RAND": "RAND",
    "RON": "RON",
    "TIM": "TIM",
    "KATIE": "KATIE",
    "JOHN": "JOHN",
    "JERRY": "JERRY",
    "RAPHAEL": "RAPHAEL",
    "HERSCHEL": "HERSCHEL",
    "MARCO": "MARCO",
    "MAGGIE": "MAGGIE",
    "MANDELA": "MANDELA",
    "LEORA": "LEORA",
    "VAL": "VAL",
    "MEHMET": "MEHMET",
    "CHERI": "CHERI",
    "BLAKE": "BLAKE",
    "ADAM": "ADAM",
    "KELLY": "KELLY",
    "ALEX": "ALEX",
    "LISA": "LISA",
    "KENDRA": "KENDRA",
    "LUKE": "LUKE",
    "JAMES": "JAMES",
    "PETER": "PETER",
    "WILL": "WILL",
    "TRUDY": "TRUDY",
    "BRIAN": "BRIAN",
    "DON": "DON",
    "ERIC": "ERIC",
    "EVAN": "EVAN",
    "MARK": "MARK",
    "TODD": "TODD"
}

# -------------------------------------------------------
# Committee aliases
# -------------------------------------------------------
COMMITTEE_ALIASES = {

    # Existing aliases...
    "TEAM HERSCHEL": "WALKER, HERSCHEL",
    "FRIENDS OF SCHUMER": "SCHUMER, CHARLES",
    "MAGGIE FOR NH": "HASSAN, MAGGIE",
    "PEOPLE FOR PATTY MURRAY": "MURRAY, PATRICIA",

    # ----------------------------
    # Add these new aliases
    # ----------------------------

    "TEAM HERSCHEL INC": "WALKER, HERSCHEL",
    "TEAM HERSCHEL INC.": "WALKER, HERSCHEL",

    "CONNECTICUT SENATE REPUBLICAN NOMINEE FUND":
        "LEVY, LEORA",

    "KATRINA FOR SENATE":
        "CHRISTIANSEN, KATRINA",

    "OKLAHOMANS FOR MADISON":
        "HORN, MADISON",

    "TAMMY FOR ILLINOIS":
        "DUCKWORTH, TAMMY",
}