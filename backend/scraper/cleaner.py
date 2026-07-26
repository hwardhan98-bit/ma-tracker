"""
Global M&A Intelligence Platform

cleaner.py

Production text normalization pipeline.

Responsibilities
----------------
* HTML removal
* HTML entity decoding
* Unicode normalization
* Boilerplate removal
* URL/email removal
* Markdown cleanup
* Quote normalization
* Dash normalization
* Whitespace normalization
* RSS text normalization

This module intentionally contains NO business logic.
It does not identify companies or classify deals.
"""

from __future__ import annotations

import html
import re
import unicodedata
from typing import Iterable

from .logger import get_logger

logger = get_logger(__name__)

try:
    from bs4 import BeautifulSoup
except ImportError:  # pragma: no cover
    BeautifulSoup = None


class TextCleaner:
    """
    Production text cleaning pipeline.

    Example
    -------
    cleaner = TextCleaner()

    clean_title = cleaner.clean(title)

    clean_summary = cleaner.clean(summary)
    """

    # ------------------------------------------------------------------
    # Compiled Regular Expressions
    # ------------------------------------------------------------------

    MULTISPACE_RE = re.compile(r"\s+")

    MULTILINE_RE = re.compile(r"\n+")

    TAB_RE = re.compile(r"\t+")

    HTML_TAG_RE = re.compile(r"<[^>]+>")

    URL_RE = re.compile(
        r"https?://\S+|www\.\S+",
        flags=re.IGNORECASE,
    )

    EMAIL_RE = re.compile(
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
    )

    HANDLE_RE = re.compile(
        r"(?<!\w)[@#][A-Za-z0-9_]+"
    )

    MULTI_DASH_RE = re.compile(r"[-]{2,}")

    MULTI_DOT_RE = re.compile(r"\.{2,}")

    MULTI_COMMA_RE = re.compile(r",{2,}")

    BRACKET_SPACE_RE = re.compile(r"\(\s+")

    SPACE_BRACKET_RE = re.compile(r"\s+\)")

    LEADING_PUNCT_RE = re.compile(r"^[,;:.\-]+")

    TRAILING_PUNCT_RE = re.compile(r"[,;:.\-]+$")

    # ------------------------------------------------------------------

    def __init__(
        self,
        remove_urls: bool = False,
        remove_emails: bool = True,
        remove_social_handles: bool = False,
    ) -> None:

        self.remove_urls = remove_urls
        self.remove_emails = remove_emails
        self.remove_social_handles = remove_social_handles

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def clean(self, text: str | None) -> str:
        """
        Cleans arbitrary text.

        Parameters
        ----------
        text:
            Raw HTML or plain text.

        Returns
        -------
        Clean normalized string.
        """

        if not text:
            return ""

        text = self.remove_html(text)

        text = self.decode_html_entities(text)

        text = self.normalize_unicode(text)

        text = self.normalize_whitespace(text)

        return text.strip()

    def clean_many(
        self,
        values: Iterable[str],
    ) -> list[str]:
        """
        Cleans multiple strings.
        """

        return [self.clean(v) for v in values]

    # ------------------------------------------------------------------
    # HTML
    # ------------------------------------------------------------------

    def remove_html(
        self,
        text: str,
    ) -> str:
        """
        Removes HTML tags.

        BeautifulSoup is preferred.

        Falls back to regex if unavailable.
        """

        if not text:

            return ""

        if BeautifulSoup is not None:

            try:

                soup = BeautifulSoup(
                    text,
                    "html.parser",
                )

                return soup.get_text(
                    separator=" ",
                    strip=True,
                )

            except Exception:

                logger.exception(
                    "BeautifulSoup parsing failed."
                )

        return self.HTML_TAG_RE.sub(
            " ",
            text,
        )

    # ------------------------------------------------------------------
    # HTML entities
    # ------------------------------------------------------------------

    @staticmethod
    def decode_html_entities(
        text: str,
    ) -> str:
        """
        Converts

            &amp;

        into

            &
        """

        return html.unescape(text)

    # ------------------------------------------------------------------
    # Unicode
    # ------------------------------------------------------------------

    @staticmethod
    def normalize_unicode(
        text: str,
    ) -> str:
        """
        Unicode normalization.

        Converts fancy unicode characters
        into canonical form.
        """

        text = unicodedata.normalize(
            "NFKC",
            text,
        )

        replacements = {

            "\u2018": "'",

            "\u2019": "'",

            "\u201c": '"',

            "\u201d": '"',

            "\u2013": "-",

            "\u2014": "-",

            "\u2212": "-",

            "\u00a0": " ",

            "\u200b": "",

            "\ufeff": "",
        }

        for old, new in replacements.items():

            text = text.replace(old, new)

        return text

    # ------------------------------------------------------------------
    # Whitespace
    # ------------------------------------------------------------------

    def normalize_whitespace(
        self,
        text: str,
    ) -> str:
        """
        Removes duplicate spaces,
        tabs and blank lines.
        """

        text = self.TAB_RE.sub(
            " ",
            text,
        )

        text = self.MULTILINE_RE.sub(
            " ",
            text,
        )

        text = self.MULTISPACE_RE.sub(
            " ",
            text,
        )

        return text.strip()
    # ------------------------------------------------------------------
    # Boilerplate Removal
    # ------------------------------------------------------------------

    BOILERPLATE_PATTERNS = (

        re.compile(r"click here to read more", re.I),

        re.compile(r"continue reading", re.I),

        re.compile(r"read the full article", re.I),

        re.compile(r"read more", re.I),

        re.compile(r"subscribe now", re.I),

        re.compile(r"all rights reserved", re.I),

        re.compile(r"copyright\s+\d{4}", re.I),

        re.compile(r"cookie policy", re.I),

        re.compile(r"privacy policy", re.I),

        re.compile(r"terms of use", re.I),

        re.compile(r"sign up for our newsletter", re.I),

        re.compile(r"follow us on twitter", re.I),

        re.compile(r"follow us on x", re.I),

        re.compile(r"follow us on linkedin", re.I),

        re.compile(r"share this article", re.I),

        re.compile(r"advertisement", re.I),

    )

    def remove_boilerplate(
        self,
        text: str,
    ) -> str:
        """
        Removes common footer/header boilerplate
        frequently found in RSS feeds.
        """

        for pattern in self.BOILERPLATE_PATTERNS:

            text = pattern.sub("", text)

        return text

    # ------------------------------------------------------------------
    # URLs
    # ------------------------------------------------------------------

    def remove_urls_from_text(
        self,
        text: str,
    ) -> str:

        if not self.remove_urls:

            return text

        return self.URL_RE.sub(" ", text)

    # ------------------------------------------------------------------
    # Emails
    # ------------------------------------------------------------------

    def remove_emails_from_text(
        self,
        text: str,
    ) -> str:

        if not self.remove_emails:

            return text

        return self.EMAIL_RE.sub(" ", text)

    # ------------------------------------------------------------------
    # Social Handles
    # ------------------------------------------------------------------

    def remove_social_handles_from_text(
        self,
        text: str,
    ) -> str:

        if not self.remove_social_handles:

            return text

        return self.HANDLE_RE.sub(" ", text)

    # ------------------------------------------------------------------
    # Markdown
    # ------------------------------------------------------------------

    @staticmethod
    def remove_markdown(
        text: str,
    ) -> str:
        """
        Removes lightweight markdown syntax.
        """

        replacements = (

            ("**", ""),

            ("__", ""),

            ("`", ""),

            ("###", ""),

            ("##", ""),

            ("#", ""),

            ("*", ""),

            ("---", " "),

        )

        for old, new in replacements:

            text = text.replace(old, new)

        return text

    # ------------------------------------------------------------------
    # Quotes
    # ------------------------------------------------------------------

    @staticmethod
    def normalize_quotes(
        text: str,
    ) -> str:

        return (

            text

            .replace("''", '"')

            .replace("``", '"')

            .replace("“", '"')

            .replace("”", '"')

            .replace("‘", "'")

            .replace("’", "'")

        )

    # ------------------------------------------------------------------
    # Dashes
    # ------------------------------------------------------------------

    def normalize_dashes(
        self,
        text: str,
    ) -> str:

        text = self.MULTI_DASH_RE.sub(

            "-",

            text,

        )

        return text

    # ------------------------------------------------------------------
    # Punctuation
    # ------------------------------------------------------------------

    def normalize_punctuation(
        self,
        text: str,
    ) -> str:

        text = self.MULTI_DOT_RE.sub(

            ".",

            text,

        )

        text = self.MULTI_COMMA_RE.sub(

            ",",

            text,

        )

        text = self.BRACKET_SPACE_RE.sub(

            "(",

            text,

        )

        text = self.SPACE_BRACKET_RE.sub(

            ")",

            text,

        )

        return text

    # ------------------------------------------------------------------
    # Leading / Trailing punctuation
    # ------------------------------------------------------------------

    def strip_punctuation(
        self,
        text: str,
    ) -> str:

        text = self.LEADING_PUNCT_RE.sub(

            "",

            text,

        )

        text = self.TRAILING_PUNCT_RE.sub(

            "",

            text,

        )

        return text

    # ------------------------------------------------------------------
    # RSS Cleaning
    # ------------------------------------------------------------------

    def clean_rss_summary(
        self,
        summary: str,
    ) -> str:
        """
        Cleans RSS descriptions while
        preserving sentence structure.
        """

        summary = self.remove_html(summary)

        summary = self.decode_html_entities(summary)

        summary = self.normalize_unicode(summary)

        summary = self.remove_boilerplate(summary)

        summary = self.remove_urls_from_text(summary)

        summary = self.remove_emails_from_text(summary)

        summary = self.remove_social_handles_from_text(summary)

        summary = self.remove_markdown(summary)

        summary = self.normalize_quotes(summary)

        summary = self.normalize_dashes(summary)

        summary = self.normalize_punctuation(summary)

        summary = self.normalize_whitespace(summary)

        summary = self.strip_punctuation(summary)

        return summary.strip()

    # ------------------------------------------------------------------
    # Title Cleaning
    # ------------------------------------------------------------------

    def clean_title(
        self,
        title: str,
    ) -> str:

        title = self.normalize_unicode(title)

        title = self.remove_markdown(title)

        title = self.normalize_quotes(title)

        title = self.normalize_dashes(title)

        title = self.normalize_punctuation(title)

        title = self.normalize_whitespace(title)

        return title.strip()
    # ------------------------------------------------------------------
    # Article Cleaning
    # ------------------------------------------------------------------

    def clean_article(
        self,
        title: str,
        summary: str,
    ) -> tuple[str, str]:
        """
        Cleans both title and summary.

        Returns
        -------
        (clean_title, clean_summary)
        """

        return (
            self.clean_title(title),
            self.clean_rss_summary(summary),
        )

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------

    @staticmethod
    def is_empty(
        text: str | None,
    ) -> bool:
        """
        Returns True if text is empty after trimming.
        """

        return not text or not text.strip()

    @staticmethod
    def has_minimum_length(
        text: str,
        minimum: int = 10,
    ) -> bool:
        """
        Checks whether cleaned text is useful.
        """

        return len(text.strip()) >= minimum

    # ------------------------------------------------------------------
    # Generic Pipeline
    # ------------------------------------------------------------------

    def pipeline(
        self,
        text: str,
    ) -> str:
        """
        Complete cleaning pipeline for arbitrary text.
        """

        if self.is_empty(text):
            return ""

        text = self.remove_html(text)
        text = self.decode_html_entities(text)
        text = self.normalize_unicode(text)
        text = self.remove_boilerplate(text)
        text = self.remove_urls_from_text(text)
        text = self.remove_emails_from_text(text)
        text = self.remove_social_handles_from_text(text)
        text = self.remove_markdown(text)
        text = self.normalize_quotes(text)
        text = self.normalize_dashes(text)
        text = self.normalize_punctuation(text)
        text = self.normalize_whitespace(text)
        text = self.strip_punctuation(text)

        return text.strip()

    # ------------------------------------------------------------------
    # Batch Processing
    # ------------------------------------------------------------------

    def clean_articles(
        self,
        articles,
    ):
        """
        Cleans an iterable of article-like objects.

        Supported object types:

        - dict
        - dataclass
        """

        cleaned = []

        for article in articles:

            try:

                if isinstance(article, dict):

                    title = article.get("title", "")
                    summary = article.get("summary", "")

                    title, summary = self.clean_article(
                        title,
                        summary,
                    )

                    article["title"] = title
                    article["summary"] = summary

                    cleaned.append(article)

                else:

                    article.title, article.summary = (
                        self.clean_article(
                            article.title,
                            article.summary,
                        )
                    )

                    cleaned.append(article)

            except Exception:

                logger.exception(
                    "Failed cleaning article."
                )

        return cleaned

    # ------------------------------------------------------------------
    # Logging Helper
    # ------------------------------------------------------------------

    def log_statistics(
        self,
        original: str,
        cleaned: str,
    ) -> None:
        """
        Logs reduction statistics.
        """

        logger.debug(
            "Cleaner reduced text from %d to %d characters.",
            len(original),
            len(cleaned),
        )


# ----------------------------------------------------------------------
# Module-level convenience instance
# ----------------------------------------------------------------------

default_cleaner = TextCleaner()


def clean(text: str) -> str:
    """
    Convenience function.

    Example
    -------
    from cleaner import clean

    text = clean(raw_text)
    """

    return default_cleaner.pipeline(text)


# ----------------------------------------------------------------------
# Self Test
# ----------------------------------------------------------------------

if __name__ == "__main__":

    SAMPLE_HTML = """
        <h2>Acme Inc. acquires Beta Ltd.</h2>

        <p>
            Read more at
            https://example.com/news?id=123
        </p>

        <p>
            Contact:
            deals@example.com
        </p>

        <p>
            Copyright 2026
        </p>
    """

    cleaner = TextCleaner(
        remove_urls=True,
        remove_emails=True,
    )

    result = cleaner.pipeline(SAMPLE_HTML)

    print(result)
