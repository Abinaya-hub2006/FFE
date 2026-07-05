import re

# --------------------------------------------------
# Words that don't help identify a candidate
# --------------------------------------------------

STOPWORDS = {
    "FOR",
    "THE",
    "OF",
    "AND",
    "TO",
    "INC",
    "INC.",
    "COMMITTEE",
    "COMMITTEE,",
    "FRIENDS",
    "TEAM",
    "PEOPLE",
    "FUND",
    "VICTORY",
    "REPUBLICAN",
    "DEMOCRATIC",
    "NOMINEE",
    "SENATE",
    "CONGRESS",
    "US",
    "U.S.",
    "AMERICA",
    "AMERICAN",
    "PAC",
    "ACTION",
    "ELECTION",
    "2022",
    "2024",
    "2026",
    "CAMPAIGN",
    "COMMITTEE.",
    "INCORPORATED",
    "LIMITED"
}

# --------------------------------------------------
# Normalize text
# --------------------------------------------------

def normalize(text):

    if text is None:
        return ""

    text = str(text).upper()

    # remove punctuation
    text = re.sub(r"[^A-Z0-9 ]", " ", text)

    # remove multiple spaces
    text = re.sub(r"\s+", " ", text)

    return text.strip()


# --------------------------------------------------
# Tokenize
# --------------------------------------------------

def tokenize(text):

    text = normalize(text)

    tokens = []

    for token in text.split():

        if token not in STOPWORDS:

            tokens.append(token)

    return tokens


# --------------------------------------------------
# Unique surname
# --------------------------------------------------

def surname(candidate_name):

    """
    Election file format:

    Kelly, Mark
    Warnock, Raphael
    """

    if candidate_name is None:
        return ""

    candidate_name = str(candidate_name)

    if "," in candidate_name:

        return candidate_name.split(",")[0].strip().upper()

    return candidate_name.split()[-1].upper()


# --------------------------------------------------
# Initials removed
# --------------------------------------------------

def remove_initials(name):

    tokens = tokenize(name)

    clean = []

    for token in tokens:

        if len(token) == 1:
            continue

        clean.append(token)

    return clean