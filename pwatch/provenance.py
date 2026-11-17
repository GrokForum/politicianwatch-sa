"""Fetch a profile source and log the real retrieval time (CHG-PW-003 fix 3).

Rule: a profile's retrieved_at comes from fetch provenance, never from a hand-typed time.
`fetch_source` downloads the page with the project Fetcher (no access-control workarounds), stores
the bytes in the raw layer (data/raw/profile-sources/<date>/<name>, kept out of git) and appends a
manifest row with the fetch time. It returns the retrieved_at to copy into the profile: the time of
this fetch (the manifest's checked_at_utc), converted to SAST with its offset.

When the fetch time was not logged, write the date only (YYYY-MM-DD), never an invented time.
"""

from __future__ import annotations

import hashlib
from datetime import datetime
from typing import Any
from urllib.parse import urlparse

from pwatch.http import Fetcher
from pwatch.raw import RawStore
from pwatch.schema import SAST
from pwatch.settings import PROFILE_SOURCES_ID


def source_name(url: str) -> str:
    """Stable file name for a URL: host + short hash (no query strings or personal data in the name)."""
    host = urlparse(url).netloc.replace(":", "_") or "source"
    return f"{host}-{hashlib.sha256(url.encode('utf-8')).hexdigest()[:16]}.html"


def retrieved_at_from_utc(iso_utc: str) -> str:
    """Manifest UTC time -> profile retrieved_at (SAST, seconds, with offset)."""
    return datetime.fromisoformat(iso_utc).astimezone(SAST).isoformat(timespec="seconds")


def fetch_source(url: str, *, raw: RawStore, fetcher: Fetcher, source_id: str = PROFILE_SOURCES_ID) -> dict[str, Any]:
    resp = fetcher.get(url)
    rf = raw.save(source_id, source_name(url), resp.content, url, resp.status_code)
    return {
        "source_url": url,
        "retrieved_at": retrieved_at_from_utc(rf.checked_at_utc),
        "raw_path": rf.path,
        "sha256": rf.sha256,
        "status": rf.status,
    }
