"""Nightly live check of the deployed draft site (CHG-PW-008).

Fetches the live site and checks that it responds and shows the expected draft content and labels:
robots.txt is exactly Disallow-all; the home, privacy and every page listed in the live
manifest pass the draft-page rules (noindex meta, DRAFT banner, privacy link, CSP, no scripts, PII
scan) and the claim rules (label, http(s) source link, date, "Right of reply" line); the privacy page
gives the role contact; an unknown path returns 404 with the DRAFT banner; the live manifest is a
draft, is fresh (48 h), and matches tonight's build (profile count, and build id after a publish).

The result is one JSON record per night (`record`), written to a file and appended to a JSONL log,
so a reviewer can read the streak. Green only if the build passed, the publish did not fail and
every live check passed.
"""

from __future__ import annotations

import json
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Callable

import httpx

from pwatch.settings import USER_AGENT
from pwatch.site import PRIVACY_EMAIL, ROBOTS_TXT, SAST, check_page
from pwatch.site_profiles import check_claims

FRESHNESS_HOURS = 48
MISSING_PATH = "/pw-live-check-missing-page/"


def _client(transport: httpx.BaseTransport | None = None) -> httpx.Client:
    return httpx.Client(
        headers={"User-Agent": USER_AGENT + " live-check"},
        timeout=30.0,
        follow_redirects=True,
        transport=transport,
    )


def _check(name: str, ok: bool, detail: str = "") -> dict[str, Any]:
    return {"name": name, "ok": bool(ok), "detail": detail}


def fetch_live_manifest(client: httpx.Client, base: str) -> dict[str, Any] | None:
    try:
        r = client.get(base + "/manifest.json", params={"nocache": str(time.time_ns())})
        return r.json() if r.status_code == 200 else None
    except (httpx.HTTPError, ValueError):
        return None


def wait_for_build(
    client: httpx.Client,
    base: str,
    build_id: str,
    *,
    timeout_s: int,
    interval_s: int = 30,
    sleep: Callable[[float], None] = time.sleep,
) -> bool:
    """After a publish, poll the live manifest until it shows `build_id` (Pages takes minutes)."""
    deadline = time.monotonic() + timeout_s
    while True:
        m = fetch_live_manifest(client, base)
        if m and m.get("build_id") == build_id:
            return True
        if time.monotonic() >= deadline:
            return False
        sleep(interval_s)


def run_checks(
    base: str,
    *,
    expected: dict[str, Any] | None,
    published: bool,
    publish_enabled: bool = False,  # aligned with CLI default "false"; omit for pre-publish, True stays strict
    now: datetime | None = None,
    client: httpx.Client | None = None,
    delay_s: float = 0.25,
) -> list[dict[str, Any]]:
    base = base.rstrip("/")
    now = now or datetime.now(timezone.utc)
    own = client is None
    client = client or _client()
    checks: list[dict[str, Any]] = []
    try:
        def get(path: str) -> httpx.Response | None:
            try:
                r = client.get(base + path)
            except httpx.HTTPError as e:
                checks.append(_check(f"GET {path}", False, f"{type(e).__name__}: {e}"))
                return None
            if delay_s:
                time.sleep(delay_s)
            return r

        r = get("/robots.txt")
        if r is not None:
            checks.append(_check("robots.txt is Disallow: /", r.status_code == 200 and r.text == ROBOTS_TXT, f"HTTP {r.status_code}"))

        manifest = fetch_live_manifest(client, base)
        checks.append(_check("manifest.json served", manifest is not None))
        pages = ["index.html", "privacy/index.html"]
        have_live_profiles = (manifest or {}).get("profiles")
        pre_publish_live = (not publish_enabled) and have_live_profiles in (0, None)
        if manifest:
            checks.append(_check("manifest status is draft", manifest.get("status") == "draft", str(manifest.get("status"))))
            gen = manifest.get("generated_at_sast")
            try:
                age = now - datetime.fromisoformat(gen)
                fresh = age <= timedelta(hours=FRESHNESS_HOURS)
                if pre_publish_live and not fresh:
                    checks.append(_check(
                        f"live build is fresh (<= {FRESHNESS_HOURS} h)",
                        True,
                        f"pre-publish: generated {gen}",
                    ))
                else:
                    checks.append(_check(f"live build is fresh (<= {FRESHNESS_HOURS} h)", fresh, f"generated {gen}"))
            except (TypeError, ValueError):
                if pre_publish_live:
                    checks.append(_check("live build is fresh", True, f"pre-publish: bad generated_at_sast {gen!r}"))
                else:
                    checks.append(_check("live build is fresh", False, f"bad generated_at_sast {gen!r}"))
            pages = [p for p in manifest.get("pages", []) if p != "404.html"] or pages
        if expected:
            want = expected.get("profiles")
            have = (manifest or {}).get("profiles")
            count_ok = manifest is not None and have == want
            # Pre-publish: publishing is off, live is still the empty/placeholder site
            # (0 profiles) while tonight's build has N. Do not turn the night red.
            # Once PW_PUBLISH_ENABLED is true, the check stays strict.
            pre_publish = (not publish_enabled) and (have in (0, None)) and bool(want)
            if pre_publish and not count_ok:
                checks.append(_check(
                    "live profile count matches tonight's build",
                    True,
                    f"pre-publish: live {have}, build {want}",
                ))
            else:
                checks.append(_check("live profile count matches tonight's build", count_ok, f"live {have}, build {want}"))
            if published:
                checks.append(_check("live build id is tonight's build", (manifest or {}).get("build_id") == expected.get("build_id"), f"live {(manifest or {}).get('build_id')}, build {expected.get('build_id')}"))
            if want and not pre_publish:
                checks.append(_check("live site lists profile pages", any(p.startswith("profiles/") for p in pages), f"{len(pages)} pages"))
            elif want and pre_publish:
                checks.append(_check("live site lists profile pages", True, f"pre-publish: {len(pages)} live pages, build {want} profiles"))

        page_fails: list[str] = []
        fetched = 0
        for rel in pages:
            path = "/" + rel.removesuffix("index.html")
            r = get(path)
            if r is None:
                continue
            fetched += 1
            if r.status_code != 200:
                page_fails.append(f"{path}: HTTP {r.status_code}")
                continue
            page_fails += check_page(path, r.text) + check_claims(path, r.text)
            if rel == "privacy/index.html" and f"mailto:{PRIVACY_EMAIL}" not in r.text:
                page_fails.append(f"{path}: role contact {PRIVACY_EMAIL} missing")
        checks.append(_check(f"{fetched} live pages pass draft and claim rules", not page_fails and fetched == len(pages), "; ".join(page_fails[:20])))

        r = get(MISSING_PATH)
        if r is not None:
            ok = r.status_code == 404 and not check_page("404", r.text)
            checks.append(_check("unknown path returns the DRAFT 404 page", ok, f"HTTP {r.status_code}"))
    finally:
        if own:
            client.close()
    return checks


def record(
    *,
    url: str,
    checks: list[dict[str, Any]],
    build_result: str,
    publish_result: str,
    publish_enabled: bool,
    expected: dict[str, Any] | None,
    dq: dict[str, Any] | None,
    run_url: str | None,
    now: datetime | None = None,
) -> dict[str, Any]:
    now = (now or datetime.now(timezone.utc)).astimezone(SAST)
    live_ok = bool(checks) and all(c["ok"] for c in checks)
    green = build_result == "success" and publish_result != "failure" and live_ok
    pre_publish = any(str(c.get("detail") or "").startswith("pre-publish") for c in checks)
    return {
        "night_sast": now.date().isoformat(),
        "checked_at_sast": now.isoformat(timespec="seconds"),
        "url": url,
        "result": "green" if green else "red",
        "pre_publish": pre_publish,
        "build": {
            "result": build_result,
            "build_id": (expected or {}).get("build_id"),
            "commit": (expected or {}).get("commit"),
            "profiles": (expected or {}).get("profiles"),
        },
        "dq": {k: (dq or {}).get(k) for k in ("status", "failure_count")} | {"warnings": len((dq or {}).get("warnings") or [])},
        "publish": {"enabled": publish_enabled, "result": publish_result},
        "live": {"ok": live_ok, "checks": checks},
        "run_url": run_url,
    }


def write_record(rec: dict[str, Any], out: Path | None, log: Path | None) -> None:
    if out:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(rec, indent=2) + "\n", encoding="utf-8")
    if log:
        log.parent.mkdir(parents=True, exist_ok=True)
        with log.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(rec, separators=(",", ":")) + "\n")
