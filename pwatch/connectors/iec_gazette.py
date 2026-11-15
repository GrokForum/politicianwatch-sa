"""IEC / Government Gazette connector skeleton.

Fetches primary-source files with provenance (raw bytes, sha256, manifest.jsonl).
Does not scrape ElectionSePush. Does not fetch SAFLII.

Callers may pass an existing Fetcher (tests inject a mock transport).
"""

from __future__ import annotations

from pathlib import Path

from pwatch.connectors.base import IngestResult
from pwatch.http import FetchError, Fetcher, SourceBlocked
from pwatch.raw import RawStore
from pwatch.settings import (
    GAZETTE_PDF_URL,
    IEC_JHB_SEAT_CALC_URL,
)

SOURCE_GAZETTE = "iec_gazette"
SOURCE_IEC_RESULTS = "iec_results"

GAZETTE_FILENAME = "government-gazette-55741-2026-11-13.pdf"
SEAT_CALC_FILENAME = "JHB-Seat-Calculation-Detail.pdf"


def ingest(
    raw: RawStore,
    fetcher: Fetcher | None = None,
    *,
    refresh: bool = False,
) -> list[IngestResult]:
    """Download the gazette PDF and the JHB seat-calculation PDF into the raw store."""
    own = fetcher is None
    fetcher = fetcher or Fetcher()
    try:
        return [
            _fetch_one(raw, fetcher, SOURCE_GAZETTE, GAZETTE_FILENAME, GAZETTE_PDF_URL, refresh),
            _fetch_one(raw, fetcher, SOURCE_IEC_RESULTS, SEAT_CALC_FILENAME, IEC_JHB_SEAT_CALC_URL, refresh),
        ]
    finally:
        if own:
            fetcher.close()


def _fetch_one(
    raw: RawStore,
    fetcher: Fetcher,
    source_id: str,
    name: str,
    url: str,
    refresh: bool,
) -> IngestResult:
    result = IngestResult(source_id=source_id)
    if not refresh:
        existing = raw.fresh_today(source_id, name)
        if existing:
            result.status = "unchanged"
            result.files.append(existing)
            result.notes.append("already fetched today; pass refresh=True to refetch")
            return result
    try:
        resp = fetcher.get(url)
        result.requests = fetcher.requests_made
        rf = raw.save(source_id, name, resp.content, url, resp.status_code)
        result.files.append(rf)
        result.status = rf.status
    except SourceBlocked as exc:
        result.status = "blocked"
        result.errors.append(str(exc))
        result.requests = fetcher.requests_made
    except FetchError as exc:
        result.status = "failed"
        result.errors.append(str(exc))
        result.requests = fetcher.requests_made
    return result


def extract_text(pdf_path: Path) -> str:
    """Extract text from a local PDF using pdfplumber (page breaks as form feeds)."""
    import pdfplumber

    pages: list[str] = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            pages.append(page.extract_text(layout=True) or "")
    return "\f".join(pages)
