"""
Global M&A Intelligence Platform

Data models used throughout the scraping pipeline.

Author: Global M&A Intelligence Platform
Python: 3.12+
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime
from typing import Any


@dataclass(slots=True)
class Article:
    """
    Normalized RSS article.

    Every RSS source is converted into this format before
    entering the processing pipeline.
    """

    title: str
    summary: str
    url: str
    source_feed: str

    published: datetime | None = None
    author: str | None = None

    def to_dict(self) -> dict[str, Any]:
        """Serialize to dictionary."""
        return asdict(self)


@dataclass(slots=True)
class DealCandidate:
    """
    Intermediate object representing an extracted deal.

    The object is progressively enriched by:

        Cleaner
            ↓
        Extractor
            ↓
        Classifier
            ↓
        Matcher
            ↓
        Database
    """

    # ---------- Source ----------
    source_url: str = ""
    source_name: str = ""
    source_feed: str = ""

    # ---------- Article ----------
    title: str = ""
    summary: str = ""
    published: datetime | None = None

    # ---------- Companies ----------
    acquirer: str | None = None
    target: str | None = None
    seller: str | None = None

    # ---------- Transaction ----------
    deal_type: str | None = None

    deal_value: float | None = None

    currency: str | None = None

    ownership_pct: float | None = None

    # ---------- Classification ----------
    industry: str | None = None

    country: str | None = None

    region: str | None = None

    tags: list[str] = field(default_factory=list)

    advisors: list[str] = field(default_factory=list)

    # ---------- Metadata ----------
    confidence: int = 0

    extraction_version: str = "1.0"

    matched: bool = False

    duplicate_of: str | None = None

    processing_time_ms: int | None = None

    def is_complete(self) -> bool:
        """
        Determines whether enough information exists
        to save the deal.
        """

        return bool(
            self.acquirer
            and self.target
            and self.deal_type
        )

    def add_tag(self, tag: str) -> None:
        """Adds tag if missing."""

        if tag and tag not in self.tags:
            self.tags.append(tag)

    def add_advisor(self, advisor: str) -> None:
        """Adds advisor if missing."""

        if advisor and advisor not in self.advisors:
            self.advisors.append(advisor)

    def increase_confidence(self, score: int) -> None:
        """
        Increase confidence while keeping it within
        the range [0,100].
        """

        self.confidence = max(
            0,
            min(
                100,
                self.confidence + score,
            ),
        )

    def to_dict(self) -> dict[str, Any]:
        """Serialize for database insertion."""
        return asdict(self)

    @classmethod
    def from_article(cls, article: Article) -> "DealCandidate":
        """
        Creates an empty DealCandidate from an article.
        """

        return cls(
            title=article.title,
            summary=article.summary,
            source_url=article.url,
            source_feed=article.source_feed,
            published=article.published,
        )
