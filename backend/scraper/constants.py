"""
Knowledge Base Loader

Loads all static datasets used by the scraper.
"""

from __future__ import annotations

import json
from pathlib import Path


DATA_DIR = (
    Path(__file__)
    .resolve()
    .parent.parent
    / "data"
)


def load_json(filename: str):

    with open(
        DATA_DIR / filename,
        encoding="utf-8"
    ) as file:

        return json.load(file)


INDUSTRIES = load_json("industries.json")

DEAL_TYPES = load_json("deal_types.json")

REGIONS = load_json("regions.json")

COUNTRIES = load_json("countries.json")

TAGS = load_json("tags.json")

COMPANY_PATTERNS = load_json(
    "company_patterns.json"
)

with open(
    DATA_DIR / "stopwords.txt",
    encoding="utf-8"
) as file:

    STOPWORDS = {

        line.strip().lower()

        for line in file

        if line.strip()

    }
