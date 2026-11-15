"""Connector tests use a mock HTTP transport, never a live source."""

from datetime import datetime, timezone
from pathlib import Path

import httpx

from pwatch.connectors.iec_gazette import (
    GAZETTE_FILENAME,
    SOURCE_GAZETTE,
    SOURCE_IEC_RESULTS,
    ingest,
)
from pwatch.http import Fetcher, SourceBlocked
from pwatch.raw import RawStore, sha256_bytes
from pwatch.settings import GAZETTE_PDF_URL, IEC_JHB_SEAT_CALC_URL


def _store(tmp_path: Path) -> RawStore:
    now = lambda: datetime(2026, 11, 15, 16, 10, 0, tzinfo=timezone.utc)
    return RawStore(tmp_path / "raw", now=now)


def test_ingest_saves_bytes_sha256_and_manifest(tmp_path: Path):
    gazette = b"%PDF-synthetic-gazette%"
    seats = b"%PDF-synthetic-seats%"

    def handler(request: httpx.Request) -> httpx.Response:
        if str(request.url) == GAZETTE_PDF_URL:
            return httpx.Response(200, content=gazette)
        if str(request.url) == IEC_JHB_SEAT_CALC_URL:
            return httpx.Response(200, content=seats)
        return httpx.Response(404, text="missing")

    fetcher = Fetcher(transport=httpx.MockTransport(handler), retries=0, sleep=lambda _d: None)
    raw = _store(tmp_path)
    results = ingest(raw, fetcher, refresh=True)
    assert [r.status for r in results] == ["ok", "ok"]
    assert {r.source_id for r in results} == {SOURCE_GAZETTE, SOURCE_IEC_RESULTS}

    saved = raw.latest(SOURCE_GAZETTE, GAZETTE_FILENAME)
    assert saved is not None
    assert saved.sha256 == sha256_bytes(gazette)
    assert saved.url == GAZETTE_PDF_URL
    assert saved.bytes == len(gazette)
    dest = raw.path_of(saved)
    assert dest.read_bytes() == gazette
    sha_file = dest.with_name(dest.name + ".sha256")
    assert sha_file.read_text().startswith(saved.sha256)
    assert any(e.sha256 == saved.sha256 for e in raw.entries())


def test_source_blocked_is_not_retried(tmp_path: Path):
    calls = {"n": 0}

    def handler(request: httpx.Request) -> httpx.Response:
        calls["n"] += 1
        return httpx.Response(403, text="blocked")

    fetcher = Fetcher(transport=httpx.MockTransport(handler), retries=3, sleep=lambda _d: None)
    raw = _store(tmp_path)
    results = ingest(raw, fetcher, refresh=True)
    assert all(r.status == "blocked" for r in results)
    assert calls["n"] == 2  # one request per source, no retries on 403
