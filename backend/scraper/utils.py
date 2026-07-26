"""
Shared utility functions.

No business logic belongs here.
"""

from __future__ import annotations

import hashlib
import re
from datetime import datetime, timezone
from urllib.parse import urlparse


def normalize_whitespace(text: str) -> str:
    """
    Collapse multiple whitespaces.

    Example:
        "A   B\nC" -> "A B C"
    """

    if not text:
        return ""

    return re.sub(r"\s+", " ", text).strip()


def clean_text(text: str) -> str:
    """
    Performs lightweight normalization.

    Does NOT perform NLP.
    """

    text = normalize_whitespace(text)

    text = text.replace("\u00a0", " ")

    return text.strip()


def generate_hash(value: str) -> str:
    """
    Stable SHA256 hash.
    """

    return hashlib.sha256(
        value.encode("utf-8")
    ).hexdigest()


def utc_now() -> datetime:
    """
    Current UTC timestamp.
    """

    return datetime.now(timezone.utc)


def extract_domain(url: str) -> str:
    """
    Returns domain only.

    Example:
        https://www.reuters.com/news
            ->
        reuters.com
    """

    domain = urlparse(url).netloc.lower()

    if domain.startswith("www."):

        domain = domain[4:]

    return domain


def safe_int(value):

    try:

        return int(value)

    except (TypeError, ValueError):

        return None


def safe_float(value):

    try:

        return float(value)

    except (TypeError, ValueError):

        return None


def unique(items):
    """
    Preserve insertion order while removing duplicates.
    """

    seen = set()

    output = []

    for item in items:

        if item not in seen:

            seen.add(item)

            output.append(item)

    return output
