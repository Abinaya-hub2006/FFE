from utils.normalize import tokenize, surname, normalize
from utils.aliases import COMMITTEE_ALIASES

# --------------------------------------------------------
# Alias Match
# --------------------------------------------------------

def alias_match(committee_name):

    committee = normalize(committee_name)

    for alias, candidate in COMMITTEE_ALIASES.items():

        alias_norm = normalize(alias)

        # Exact match
        if alias_norm == committee:
            return candidate, "Alias Match"

        # Alias is contained in committee name
        if alias_norm in committee:
            return candidate, "Alias Match"

        # Committee name is contained in alias
        if committee in alias_norm:
            return candidate, "Alias Match"

    return None, None


# --------------------------------------------------------
# Token Match
# --------------------------------------------------------

def token_match(committee_name, election_df):

    committee_tokens = set(tokenize(committee_name))

    best_candidate = None
    best_score = 0

    for _, row in election_df.iterrows():

        candidate = row["name"]

        candidate_tokens = set(tokenize(candidate))

        common = committee_tokens.intersection(candidate_tokens)

        score = len(common)

        if score > best_score:

            best_score = score
            best_candidate = candidate

    if best_score >= 2:

        return best_candidate, "Token Match"

    return None, None


# --------------------------------------------------------
# Unique Surname Match
# --------------------------------------------------------

def surname_match(committee_name, election_df):

    committee_tokens = set(tokenize(committee_name))

    matches = []

    for _, row in election_df.iterrows():

        last = surname(row["name"])

        if last in committee_tokens:

            matches.append(row["name"])

    if len(matches) == 1:

        return matches[0], "Surname Match"

    return None, None


# --------------------------------------------------------
# Master Resolver
# --------------------------------------------------------

def resolve_committee(committee_name, election_df):

    # Alias
    candidate, method = alias_match(committee_name)

    if candidate is not None:

        return candidate, method, "Matched"

    # Token
    candidate, method = token_match(
        committee_name,
        election_df
    )

    if candidate is not None:

        return candidate, method, "Matched"

    # Surname
    candidate, method = surname_match(
        committee_name,
        election_df
    )

    if candidate is not None:

        return candidate, method, "Matched"

    return "", "", "Review"