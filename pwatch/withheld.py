"""Private source references for facts labelled Withheld (POPIA) (CHG-PW-011).

A fact whose only source carries private personal details is not Unknown: it is
Withheld (POPIA). The public profile holds no value and no URL. The private file
stores only slug, fact key, URL, title and date, so a serious enquirer can be
referred to the source. The file is never rendered, never copied into a site
build, and must not be carried to a fresh public repository.
"""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from pwatch.schema import iter_adverse_items, iter_facts
from pwatch.settings import WITHHELD_LABEL, WITHHELD_SOURCES_PATH

REQUIRED_KEYS = ("slug", "fact", "source_url", "source_date", "title")


def load_withheld_sources(path: Path | None = None) -> list[dict[str, Any]]:
    """Load entries from the private file. Missing file yields an empty list."""
    p = path or WITHHELD_SOURCES_PATH
    if not p.is_file():
        return []
    raw = json.loads(p.read_text(encoding="utf-8"))
    if isinstance(raw, list):
        return [e for e in raw if isinstance(e, dict)]
    if isinstance(raw, dict) and isinstance(raw.get("entries"), list):
        return [e for e in raw["entries"] if isinstance(e, dict)]
    return []


def entries_for(slug: str, fact: str, entries: list[dict[str, Any]] | None = None) -> list[dict[str, Any]]:
    rows = entries if entries is not None else load_withheld_sources()
    return [e for e in rows if e.get("slug") == slug and e.get("fact") == fact]


def leak_needles(url: str) -> set[str]:
    """URL spellings to search for in public output (path required; bare hosts omitted)."""
    text = (url or "").strip()
    if not text:
        return set()
    variants = {text, text.rstrip("/")}
    grown: set[str] = set()
    for v in variants:
        grown.add(v)
        for prefix in ("https://", "http://"):
            if v.lower().startswith(prefix):
                rest = v[len(prefix) :]
                grown.add(rest)
                grown.add(rest.rstrip("/"))
                if rest.lower().startswith("www."):
                    grown.add(prefix + rest[4:])
                    grown.add(rest[4:])
                    grown.add((prefix + rest[4:]).rstrip("/"))
                    grown.add(rest[4:].rstrip("/"))
                else:
                    grown.add(prefix + "www." + rest)
                    grown.add("www." + rest)
                    grown.add((prefix + "www." + rest).rstrip("/"))
                    grown.add(("www." + rest).rstrip("/"))
    out = set()
    for v in grown:
        if not v:
            continue
        hostpath = v.split("://", 1)[-1]
        if "/" in hostpath and hostpath.split("/", 1)[1]:
            out.add(v)
    return out


def all_leak_needles(entries: list[dict[str, Any]] | None = None) -> set[str]:
    rows = entries if entries is not None else load_withheld_sources()
    needles: set[str] = set()
    for e in rows:
        needles |= leak_needles(str(e.get("source_url") or ""))
    return needles


def _has_public_url(fact: dict[str, Any]) -> bool:
    if str(fact.get("source_url") or "").strip():
        return True
    extra = fact.get("also_sourced") or []
    if isinstance(extra, list) and any(isinstance(s, dict) and s.get("source_url") for s in extra):
        return True
    return False


def check_withheld_facts(
    profile: dict[str, Any],
    locator: str,
    entries: list[dict[str, Any]] | None = None,
) -> list[str]:
    """A withheld fact needs a matching private entry, no public URL, and is not adverse."""
    if not isinstance(profile, dict):
        return []
    rows = entries if entries is not None else load_withheld_sources()
    slug = str(profile.get("slug") or "")
    failures: list[str] = []
    adverse = {k for k, _ in iter_adverse_items(profile)}
    for key, fact in iter_facts(profile):
        if not isinstance(fact, dict) or fact.get("label") != WITHHELD_LABEL:
            continue
        where = f"{locator}.{key}"
        if key in adverse:
            failures.append(f"{where}: {WITHHELD_LABEL} is not allowed on an adverse item")
        if fact.get("value") is not None:
            failures.append(f"{where}: {WITHHELD_LABEL} fact must have a null value")
        if _has_public_url(fact):
            failures.append(f"{where}: {WITHHELD_LABEL} fact must not carry a public source URL")
        if not slug or not entries_for(slug, key, rows):
            failures.append(f"{where}: {WITHHELD_LABEL} fact has no matching entry in the private withheld-sources file")
    if slug:
        withheld_keys = {k for k, f in iter_facts(profile) if isinstance(f, dict) and f.get("label") == WITHHELD_LABEL}
        for e in rows:
            if e.get("slug") != slug:
                continue
            fact_key = e.get("fact")
            if fact_key not in withheld_keys:
                failures.append(
                    f"{locator}: private withheld-sources entry for {slug!r} fact {fact_key!r} "
                    f"does not match a {WITHHELD_LABEL} fact"
                )
    return failures


def check_withheld_entry_format(entries: list[dict[str, Any]] | None = None) -> list[str]:
    """Format checks on the private file (URL, date, required keys). No personal-detail scan of titles."""
    rows = entries if entries is not None else load_withheld_sources()
    failures: list[str] = []
    for i, e in enumerate(rows):
        loc = f"withheld-sources[{i}]"
        for key in REQUIRED_KEYS:
            if not str(e.get(key) or "").strip():
                failures.append(f"{loc}: missing {key}")
        url = str(e.get("source_url") or "")
        parsed = urlparse(url)
        if url and (parsed.scheme not in ("http", "https") or not parsed.netloc or " " in url):
            failures.append(f"{loc}: source_url is not a valid http(s) URL")
        raw_date = str(e.get("source_date") or "")
        if raw_date:
            try:
                if len(raw_date) != 10:
                    raise ValueError
                date.fromisoformat(raw_date)
            except ValueError:
                failures.append(f"{loc}: source_date must be YYYY-MM-DD, got {raw_date!r}")
    return failures


def check_tree_for_withheld_urls(root: Path, entries: list[dict[str, Any]] | None = None) -> list[str]:
    """Fail if any withheld-source URL (or a close spelling) appears under root."""
    needles = all_leak_needles(entries)
    if not needles or not root.exists():
        return []
    # Longer needles first so a report is specific.
    ordered = sorted(needles, key=len, reverse=True)
    failures: list[str] = []
    files = [root] if root.is_file() else [p for p in root.rglob("*") if p.is_file() and ".git" not in p.parts]
    for path in files:
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            try:
                text = path.read_bytes().decode("utf-8", "replace")
            except OSError:
                continue
        for needle in ordered:
            if needle in text:
                rel = path.name if root.is_file() else str(path.relative_to(root))
                failures.append(f"{rel}: built output contains a withheld-source URL")
                break
    return failures
