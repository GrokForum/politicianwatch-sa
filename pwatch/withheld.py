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
from html import unescape
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urlparse

from pwatch.schema import iter_adverse_items, iter_facts
from pwatch.settings import WITHHELD_LABEL, WITHHELD_SOURCES_PATH

REQUIRED_KEYS = ("slug", "fact", "source_url", "source_date", "title")


def register_path(path: Path | None = None) -> Path:
    return path or WITHHELD_SOURCES_PATH


def load_withheld_sources(path: Path | None = None) -> list[dict[str, Any]]:
    """Load entries from the private file. Missing file or a non-list payload yields an empty list."""
    p = register_path(path)
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


def _decode_text(text: str) -> str:
    """html.unescape, then urllib.parse.unquote until the value is stable."""
    s = unescape(text or "")
    while True:
        nxt = unquote(s)
        if nxt == s:
            return nxt
        s = nxt


def normalize_url(text: str) -> str:
    """Casefold, decode, then strip scheme, a leading www. and a trailing slash."""
    s = _decode_text(text).casefold().strip()
    for prefix in ("https://", "http://"):
        if s.startswith(prefix):
            s = s[len(prefix) :]
            break
    if s.startswith("www."):
        s = s[4:]
    return s.rstrip("/")


def normalize_title(text: str) -> str:
    """Casefold, unescape, and collapse whitespace."""
    return " ".join(unescape(text or "").casefold().split())


def _has_public_url(fact: dict[str, Any]) -> bool:
    if str(fact.get("source_url") or "").strip():
        return True
    extra = fact.get("also_sourced") or []
    if isinstance(extra, list) and any(isinstance(s, dict) and s.get("source_url") for s in extra):
        return True
    return False


def _profile_has_withheld(profile: dict[str, Any]) -> bool:
    return any(isinstance(f, dict) and f.get("label") == WITHHELD_LABEL for _, f in iter_facts(profile))


def check_withheld_facts(
    profile: dict[str, Any],
    locator: str,
    entries: list[dict[str, Any]] | None = None,
    *,
    path: Path | None = None,
) -> list[str]:
    """A withheld fact needs a matching private entry, no public URL, and is not adverse.

    If any fact is Withheld (POPIA) and the register file is missing or empty, that is a failure.
    """
    if not isinstance(profile, dict):
        return []
    reg = register_path(path)
    loaded_from_disk = entries is None
    rows = entries if entries is not None else load_withheld_sources(reg)
    slug = str(profile.get("slug") or "")
    failures: list[str] = []
    if _profile_has_withheld(profile) and loaded_from_disk:
        if not reg.is_file():
            failures.append(
                f"{locator}: {WITHHELD_LABEL} fact(s) present but the private withheld-sources file is missing"
            )
        elif not rows:
            failures.append(
                f"{locator}: {WITHHELD_LABEL} fact(s) present but the private withheld-sources file is empty"
            )
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


def _read_text(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        try:
            return path.read_bytes().decode("utf-8", "replace")
        except OSError:
            return None


def _iter_tree_files(root: Path) -> list[Path]:
    if root.is_file():
        return [root]
    return [p for p in root.rglob("*") if p.is_file() and ".git" not in p.parts]


def check_tree_for_withheld_urls(root: Path, entries: list[dict[str, Any]] | None = None, *, path: Path | None = None) -> list[str]:
    """Fail if a withheld-source URL or title appears under root, after normalisation.

    Also fails when built output has a Withheld (POPIA) fact and the register is missing or empty.
    URLs are matched after casefold, repeated unquote, html.unescape, and stripping the scheme,
    a leading www. and a trailing slash. Titles are matched after casefold, unescape and
    collapsed whitespace.
    """
    if not root.exists():
        return []
    reg = register_path(path)
    loaded_from_disk = entries is None
    rows = entries if entries is not None else load_withheld_sources(reg)
    files = _iter_tree_files(root)
    failures: list[str] = []

    mentions_withheld = False
    for fp in files:
        text = _read_text(fp)
        if text is None:
            continue
        if WITHHELD_LABEL in text:
            mentions_withheld = True
            break
    if mentions_withheld and loaded_from_disk:
        if not reg.is_file():
            failures.append(
                "built output has a Withheld (POPIA) fact but the private withheld-sources file is missing"
            )
        elif not rows:
            failures.append(
                "built output has a Withheld (POPIA) fact but the private withheld-sources file is empty"
            )

    url_needles = sorted({normalize_url(str(e.get("source_url") or "")) for e in rows} - {""}, key=len, reverse=True)
    title_needles = sorted({normalize_title(str(e.get("title") or "")) for e in rows} - {""}, key=len, reverse=True)
    for fp in files:
        text = _read_text(fp)
        if text is None:
            continue
        rel = fp.name if root.is_file() else str(fp.relative_to(root))
        url_haystack = _decode_text(text).casefold()
        for needle in url_needles:
            if needle in url_haystack:
                failures.append(f"{rel}: built output contains a withheld-source URL")
                break
        title_haystack = normalize_title(text)
        for needle in title_needles:
            if needle in title_haystack:
                failures.append(f"{rel}: built output contains a withheld-source title")
                break
    return failures
