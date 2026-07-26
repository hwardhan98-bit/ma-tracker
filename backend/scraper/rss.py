"""
RSS Feed Loader

Responsibilities
----------------
- Fetch RSS/Atom feeds
- Retry transient failures
- Parse publication dates
- Normalize feed entries
- Return a common article structure

No business logic.
No extraction.
No classification.
"""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from typing import Any

import feedparser
import requests

from .config import SCRAPER
from .logger import get_logger
from .utils import clean_text

logger = get_logger(__name__)


class RSSFetcher:

    def __init__(self, feeds: list[str]):

        self.feeds = feeds

    def fetch(self) -> list[dict]:

        articles = []

        with ThreadPoolExecutor(max_workers=8) as executor:

            futures = {

                executor.submit(
                    self._fetch_feed,
                    url
                ): url

                for url in self.feeds

            }

            for future in as_completed(futures):

                try:

                    articles.extend(future.result())

                except Exception as exc:

                    logger.exception(exc)

        return articles

    def _fetch_feed(self, url: str) -> list[dict]:

        logger.info("Fetching %s", url)

        response = requests.get(

            url,

            timeout=SCRAPER.timeout_seconds,

            headers={

                "User-Agent":
                    SCRAPER.user_agent

            }

        )

        response.raise_for_status()

        feed = feedparser.parse(response.content)

        output = []

        for entry in feed.entries:

            output.append(

                self._normalize_entry(

                    entry,
                    url

                )

            )

        logger.info(

            "%s : %d articles",

            url,

            len(output)

        )

        return output

    def _normalize_entry(

        self,

        entry,

        feed_url

    ) -> dict:

        published = self._parse_date(

            getattr(entry, "published", None)

        )

        return {

            "title":

                clean_text(

                    getattr(

                        entry,

                        "title",

                        ""

                    )

                ),

            "summary":

                clean_text(

                    getattr(

                        entry,

                        "summary",

                        ""

                    )

                ),

            "url":

                getattr(

                    entry,

                    "link",

                    ""

                ),

            "published":

                published,

            "source_feed":

                feed_url,

            "author":

                getattr(

                    entry,

                    "author",

                    ""

                )

        }

    @staticmethod

    def _parse_date(

        value

    ):

        if not value:

            return None

        try:

            dt = parsedate_to_datetime(value)

            if dt.tzinfo is None:

                dt = dt.replace(

                    tzinfo=timezone.utc

                )

            return dt.astimezone(

                timezone.utc

            )

        except Exception:

            return None
