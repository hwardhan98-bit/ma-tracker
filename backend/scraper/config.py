"""
Global M&A Intelligence Platform

Configuration Module

Loads environment variables and exposes immutable
application configuration.
"""

from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class SupabaseConfig:
    """
    Supabase configuration.
    """

    url: str
    key: str
    table: str = "ma_deals"


@dataclass(frozen=True)
class ScraperConfig:
    """
    Scraper configuration.
    """

    rss_days: int = 1

    github_action: bool = True

    timeout_seconds: int = 30

    max_retries: int = 3

    confidence_default: int = 50

    user_agent: str = (
        "GlobalMATerminal/1.0 "
        "(https://github.com)"
    )


SUPABASE = SupabaseConfig(
    url=os.getenv("SUPABASE_URL", ""),
    key=os.getenv("SUPABASE_KEY", "")
)

SCRAPER = ScraperConfig()
