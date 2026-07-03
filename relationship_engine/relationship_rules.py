import re

RULES = [

    {
        "name": "Candidate Loan",
        "schedule": ["SC/10"],
        "keywords": []
    },

    {
        "name": "Joint Fundraising",
        "schedule": ["SA12"],
        "keywords": [
            "victory fund",
            "joint fundraising"
        ]
    },

    {
        "name": "Earmarked Contribution",
        "schedule": [
            "SA11AI",
            "SA11B"
        ],
        "keywords": [
            "earmarked",
            "through conduit",
            "winred",
            "actblue"
        ]
    },

    {
        "name": "Attribution",
        "schedule": [
            "SA15"
        ],
        "keywords": [
            "partnership attribution",
            "permissible funds",
            "living trust",
            "trust"
        ]
    },

    {
        "name": "Redesignation",
        "schedule": [
            "SA11C",
            "SA15"
        ],
        "keywords": [
            "redesignation",
            "from primary",
            "to general",
            "from runoff",
            "to runoff",
            "see redesignation"
        ]
    },

    {
        "name": "Refund",
        "schedule": [
            "SA17",
            "SB28A"
        ],
        "keywords": [
            "refund",
            "refunded"
        ]
    },

    {
        "name": "Expenditure",
        "schedule": [
            "SB23",
            "SB29"
        ],
        "keywords": []
    },

    {
        "name": "Normal Contribution",
        "schedule": [
            "SA11A"
        ],
        "keywords": []
    }

]