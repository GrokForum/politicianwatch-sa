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



def test_tls_error_is_logged_and_not_swallowed(tmp_path, caplog):
    """A certificate failure is labelled TLS, written to evidence, and not retried."""
    import json
    import logging
    import ssl

    import httpx

    from pwatch.http import Fetcher, TlsError
    from pwatch.raw import RawStore

    def handler(request: httpx.Request) -> httpx.Response:
        err = ssl.SSLCertVerificationError("certificate verify failed: self-signed certificate")
        raise httpx.ConnectError("[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed") from err

    fetcher = Fetcher(transport=httpx.MockTransport(handler), retries=3, sleep=lambda _d: None, source="iec_gazette")
    raw = _store(tmp_path)
    with caplog.at_level(logging.WARNING, logger="pwatch.http"):
        results = ingest(raw, fetcher, refresh=True)
    assert results and all(r.status == "failed" for r in results)
    assert all(any("TLS error" in e for e in r.errors) for r in results)
    assert all(any("TLS error logged to evidence" in n for n in r.notes) for r in results)
    # One attempt per source, no retries on a certificate failure.
    assert fetcher.requests_made == 2
    assert fetcher.tls_errors and all("SSL" in e["error"] or "certificate" in e["error"].lower() for e in fetcher.tls_errors)
    evidence = raw.dir / "tls-errors.jsonl"
    assert evidence.is_file()
    lines = [json.loads(ln) for ln in evidence.read_text(encoding="utf-8").splitlines() if ln.strip()]
    assert lines and all(row["source_id"] and row["url"] and row["error"] for row in lines)
    assert any("TLS error" in rec.message for rec in caplog.records)
