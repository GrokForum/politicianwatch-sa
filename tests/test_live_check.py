"""CHG-PW-008: live check against a served build (httpx MockTransport; no network)."""

from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

import httpx
import pytest

from pwatch.live_check import _client, record, run_checks, wait_for_build, write_record
from pwatch.profiles import load_profile_dir
from pwatch.settings import PROFILES_DIR
from pwatch.site import build_site

NOW = datetime(2026, 11, 19, 1, 30, tzinfo=timezone.utc)
BASE = "https://pw.example.test"


def serve(root: Path, *, override: dict[str, tuple[int, str]] | None = None) -> httpx.MockTransport:
    def handler(req: httpx.Request) -> httpx.Response:
        path = req.url.path
        if override and path in override:
            code, body = override[path]
            return httpx.Response(code, text=body)
        f = root / path.lstrip("/")
        if path.endswith("/"):
            f = f / "index.html"
        if f.is_file():
            return httpx.Response(200, content=f.read_bytes())
        return httpx.Response(404, content=(root / "404.html").read_bytes())

    return httpx.MockTransport(handler)


@pytest.fixture(scope="module")
def site(tmp_path_factory) -> tuple[Path, dict]:
    out = tmp_path_factory.mktemp("live") / "_site"
    m = build_site(out, profiles=load_profile_dir(PROFILES_DIR), now=NOW)
    return out, m


def check(root: Path, expected: dict, *, published=True, now=NOW + timedelta(minutes=5), override=None):
    with _client(serve(root, override=override)) as c:
        return run_checks(BASE, expected=expected, published=published, now=now, client=c, delay_s=0)


def test_good_live_site_is_all_green(site) -> None:
    root, m = site
    checks = check(root, m)
    assert checks and all(c["ok"] for c in checks), [c for c in checks if not c["ok"]]
    pages = next(c for c in checks if "live pages pass" in c["name"])
    assert pages["name"].startswith("26 live pages")  # home + privacy + 24 profiles


def test_placeholder_site_is_red(tmp_path: Path, site) -> None:
    _, m = site
    ph = tmp_path / "ph"
    build_site(ph, now=NOW)
    failed = {c["name"] for c in check(ph, m, published=False) if not c["ok"]}
    assert "live profile count matches tonight's build" in failed


@pytest.mark.parametrize(
    "path, body, broken",
    [
        ("/robots.txt", "User-agent: *\nAllow: /\n", "robots.txt is Disallow: /"),
        ("/privacy/", "<html><title>x</title></html>", "pass draft and claim rules"),
    ],
)
def test_broken_live_file_is_red(site, path: str, body: str, broken: str) -> None:
    root, m = site
    failed = [c["name"] for c in check(root, m, override={path: (200, body)}) if not c["ok"]]
    assert any(broken in f for f in failed), failed


def test_profile_page_without_noindex_or_source_is_red(site) -> None:
    root, m = site
    slug = "thapelo-kenneth-kunene"
    html = (root / "profiles" / slug / "index.html").read_text(encoding="utf-8")
    bad = html.replace('<meta name="robots" content="noindex, nofollow">', "").replace('class="src-link"', 'class="x"')
    checks = check(root, m, override={f"/profiles/{slug}/": (200, bad)})
    detail = next(c for c in checks if "live pages pass" in c["name"])
    assert not detail["ok"] and "noindex" in detail["detail"] and "source link" in detail["detail"]


def test_stale_or_wrong_build_is_red(site) -> None:
    root, m = site
    failed = {c["name"] for c in check(root, m, now=NOW + timedelta(hours=49)) if not c["ok"]}
    assert any("fresh" in f for f in failed)
    failed = {c["name"] for c in check(root, dict(m, build_id="B20990101T000000Z")) if not c["ok"]}
    assert "live build id is tonight's build" in failed
    # Without a publish tonight the build id is not compared.
    assert all(c["ok"] for c in check(root, dict(m, build_id="B20990101T000000Z"), published=False))


def test_missing_page_must_be_draft_404(site) -> None:
    root, m = site
    failed = {c["name"] for c in check(root, m, override={"/pw-live-check-missing-page/": (503, "")}) if not c["ok"]}
    assert "unknown path returns the DRAFT 404 page" in failed


def test_wait_for_build_polls_until_live(site) -> None:
    root, m = site
    calls = {"n": 0}

    def handler(req: httpx.Request) -> httpx.Response:
        calls["n"] += 1
        bid = m["build_id"] if calls["n"] >= 3 else "Bold"
        return httpx.Response(200, json={"build_id": bid})

    with _client(httpx.MockTransport(handler)) as c:
        assert wait_for_build(c, BASE, m["build_id"], timeout_s=60, interval_s=0, sleep=lambda s: None)
    assert calls["n"] == 3


def test_record_verdict_and_log(tmp_path: Path, site) -> None:
    root, m = site
    ok = [{"name": "x", "ok": True, "detail": ""}]
    args = dict(url=BASE, expected=m, dq={"status": "pass", "failure_count": 0, "warnings": []}, run_url=None, now=NOW, publish_enabled=True)
    green = record(checks=ok, build_result="success", publish_result="success", **args)
    assert green["result"] == "green" and green["night_sast"] == "2026-11-19" and green["dq"]["status"] == "pass"
    assert record(checks=ok, build_result="failure", publish_result="skipped", **args)["result"] == "red"
    assert record(checks=ok, build_result="success", publish_result="failure", **args)["result"] == "red"
    assert record(checks=[{"name": "x", "ok": False, "detail": ""}], build_result="success", publish_result="skipped", **args)["result"] == "red"
    assert record(checks=[], build_result="success", publish_result="skipped", **args)["result"] == "red"
    log = tmp_path / "nightly" / "log.jsonl"
    write_record(green, tmp_path / "nightly" / "2026-11-19.json", log)
    write_record(green, None, log)
    lines = log.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 2 and json.loads(lines[0])["result"] == "green"
