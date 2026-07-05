"""
==========================================================
Committee Entity Resolution Engine
Stage 10.5 v2
==========================================================
"""

from pathlib import Path
import pandas as pd
import duckdb
import re

# ==========================================================
# PATHS
# ==========================================================

ROOT = Path(__file__).resolve().parent.parent

DB = ROOT / "outputs/database/fec_receipts.duckdb"

WINNER = ROOT / "outputs/winner_mapping/winner_mapping.csv"

OUT = ROOT / "outputs/committee_resolution"

OUT.mkdir(parents=True, exist_ok=True)

# ==========================================================
# LOAD
# ==========================================================

print("="*70)
print("COMMITTEE ENTITY RESOLUTION")
print("="*70)

winner = pd.read_csv(WINNER)

con = duckdb.connect(DB)

committee = con.execute("""

SELECT DISTINCT

committee_id,
committee_name

FROM receipts

ORDER BY committee_name

""").fetchdf()

con.close()

# ==========================================================
# ALIAS DICTIONARY
# ==========================================================

ALIASES = {

    "DOCTOR OZ":"MEHMET OZ",

    "TEAM HERSCHEL":"HERSCHEL WALKER",

    "PEOPLE PATTY":"PATTY MURRAY",

    "MAGGIE":"MAGGIE HASSAN",

    "BENNET":"MICHAEL BENNET",

    "JD":"JD VANCE",

    "ALEX PADILLA":"ALEX PADILLA",

    "VAL DEMINGS":"VAL DEMINGS",

    "TIM RYAN":"TIM RYAN",

    "MARK KELLY":"MARK KELLY",

    "WARNOCK":"RAPHAEL WARNOCK",

    "RUBIO":"MARCO RUBIO",

    "BOOZMAN":"JOHN BOOZMAN",

    "FETTERMAN":"JOHN FETTERMAN",

    "SMILEY":"TIFFANY SMILEY",

    "LAXALT":"ADAM LAXALT",

    "MASTERS":"BLAKE MASTERS",

    "ODEA":"JOE ODEA",

    "MURKOWSKI":"LISA MURKOWSKI",

    "PERKINS":"JO RAE PERKINS",

    "MCMULLIN":"EVAN MCMULLIN",

    "BRITT":"KATIE BRITT",

    "BEASLEY":"CHERI BEASLEY",

    "BOOKER":"CHARLES BOOKER",

    "BENGS":"BRIAN BENGS",

    "PADILLA":"ALEX PADILLA",

    "CRAPO":"MIKE CRAPO",

    "LEE":"MIKE LEE",

    "MORAN":"JERRY MORAN",

    "SCHMITT":"ERIC SCHMITT",

    "WYDEN":"RON WYDEN",

    "SCHATZ":"BRIAN SCHATZ",

    "HOEVEN":"JOHN HOEVEN",

    "GRASSLEY":"CHUCK GRASSLEY",

    "THUNE":"JOHN THUNE"

}

REMOVE = {

"FOR","THE","INC","COMMITTEE","TEAM",

"FRIENDS","PEOPLE","US","USA",

"U","S","SENATE","CONGRESS",

"FUND","2022","REPUBLICAN",

"NOMINEE","DEMOCRATIC","CAMPAIGN",

"LIMITED"

}

# ==========================================================
# FUNCTIONS
# ==========================================================

def normalize(text):

    if pd.isna(text):

        return ""

    text = text.upper()

    text = re.sub(r"[^A-Z0-9 ]"," ",text)

    words=[]

    for w in text.split():

        if w not in REMOVE:

            words.append(w)

    return " ".join(words)


def token_set(text):

    return set(normalize(text).split())


winner["tokens"]=winner["candidate_standardized"].apply(token_set)

results=[]

# ==========================================================
# MATCH
# ==========================================================

for _,com in committee.iterrows():

    cname=com.committee_name

    ckey=normalize(cname)

    # ----------------------------
    # Alias Expansion
    # ----------------------------

    for k,v in ALIASES.items():

        if k in ckey:

            ckey=v

            break

    ctokens=set(ckey.split())

    best=None

    best_score=0

    for _,cand in winner.iterrows():

        wtokens=cand.tokens

        score=len(ctokens & wtokens)

        if score>best_score:

            best_score=score

            best=cand

    if best is None:

        status="Unmatched"

    elif best_score>=2:

        status="Matched"

    elif best_score==1:

        status="Review"

    else:

        status="Unmatched"

    if best is not None:

        results.append({

            "committee_id":com.committee_id,

            "committee_name":cname,

            "candidate":best["name"],

            "state":best["state"],

            "winner":best["winner"],

            "score":best_score,

            "status":status

        })

    else:

        results.append({

            "committee_id":com.committee_id,

            "committee_name":cname,

            "candidate":"",

            "state":"",

            "winner":"",

            "score":0,

            "status":"Unmatched"

        })

# ==========================================================
# SAVE
# ==========================================================

df=pd.DataFrame(results)

df.to_csv(

OUT/"committee_entity_resolution.csv",

index=False

)

df[df.status=="Review"].to_csv(

OUT/"manual_review.csv",

index=False

)

df[df.status=="Unmatched"].to_csv(

OUT/"unmatched.csv",

index=False

)

report=[]

report.append("="*70)

report.append("ENTITY RESOLUTION REPORT")

report.append("="*70)

report.append("")

report.append(f"Committees : {len(df)}")

report.append(f"Matched    : {(df.status=='Matched').sum()}")

report.append(f"Review     : {(df.status=='Review').sum()}")

report.append(f"Unmatched  : {(df.status=='Unmatched').sum()}")

with open(

OUT/"entity_resolution_report.txt",

"w",

encoding="utf8"

) as f:

    f.write("\n".join(report))

print()

print(df.status.value_counts())

print()

print("Done.")