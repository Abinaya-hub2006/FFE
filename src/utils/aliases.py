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
COMMITTEE_ALIASES = {

    "TEAM HERSCHEL": "Walker, Herschel",
    "TEAM HERSCHEL INC": "Walker, Herschel",
    "TEAM HERSCHEL INC.": "Walker, Herschel",

    "FRIENDS OF SCHUMER": "Schumer, Chuck",

    "MAGGIE FOR NH": "Hassan, Maggie",

    "PEOPLE FOR PATTY MURRAY": "Murray, Patty",

    "CONNECTICUT SENATE REPUBLICAN NOMINEE FUND": "Levy, Leora",

    "KATRINA FOR SENATE": "Christiansen, Katrina",

    "OKLAHOMANS FOR MADISON": "Horn, Madison",

    "TAMMY FOR ILLINOIS": "Duckworth, Tammy",
    "KELLY FOR ALASKA": "Tshibaka, Kelly",
    "JOE PINION FOR US SENATE INC": "Pinion, Joseph",
}