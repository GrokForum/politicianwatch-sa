"""Withheld-register leak matching and the site-side missing-register guard (CHG-PW-013)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from pwatch.settings import WITHHELD_LABEL, WITHHELD_PUBLIC_TEXT
from pwatch.withheld import (
    check_tree_for_withheld_urls,
    check_withheld_register_for_profiles,
    normalize_title,
    normalize_url,
)


def test_normalize_url_casefold_and_www_strip() -> None:
    assert normalize_url("HTTPS://WWW.Example.COM/Path/") == "example.com/path"
    assert normalize_url("http://www.example.com/path") == "example.com/path"
    assert normalize_url("https://example.com/path") == "example.com/path"
    assert normalize_url("WWW.EXAMPLE.COM/Path") == "example.com/path"


def test_normalize_url_needle_casefold_matches_haystack() -> None:
    needle = normalize_url("https://News.Example.TEST/Held/Private")
    haystack = "See HTTPS://NEWS.EXAMPLE.TEST/HELD/PRIVATE for the interview."
    # Haystack side of the leak check: decode + casefold, as in check_tree_for_withheld_urls.
    from pwatch.withheld import _decode_text

    assert needle in _decode_text(haystack).casefold()


def test_normalize_title_strips_tags_including_split_titles() -> None:
    assert normalize_title("Exam<b>ple inter</b>view") == "example interview"
    assert normalize_title("Example<br>interview") == "example interview"
    assert normalize_title("Example</p><p>interview") == "example interview"


def test_normalize_title_nfkc_and_non_ascii_hyphens() -> None:
    # Fullwidth characters collapse under NFKC; en/em dashes fold to spaces.
    assert normalize_title("Ｅｘａｍｐｌｅ ｉｎｔｅｒｖｉｅｗ") == "example interview"
    assert normalize_title("Example–interview") == "example interview"  # en dash
    assert normalize_title("Example—interview") == "example interview"  # em dash
    assert normalize_title("Example‐interview") == "example interview"  # hyphen
    assert normalize_title("Example interview") == normalize_title("Example-interview")


def test_normalize_title_casefold_and_whitespace() -> None:
    assert normalize_title("  Example\n\tINTERVIEW  ") == "example interview"
    assert normalize_title("Example  interview") == "example interview"


def _profile(slug: str, *, withheld: bool = True) -> dict:
    fact = {
        "value": None,
        "label": WITHHELD_LABEL if withheld else "Unknown",
        "source_url": None,
        "source_date": None,
        "retrieved_at": None,
    }
    return {
        "slug": slug,
        "name": {"value": "SYNTH PERSON", "label": "Confirmed", "source_url": "https://example.test/g.pdf", "source_date": "2026-11-13", "retrieved_at": "2026-11-15"},
        "education": fact,
        "court_matters": [],
        "scandals": [],
    }


def _write_register(path: Path, slug: str = "synth-person", fact: str = "education") -> Path:
    path.write_text(
        json.dumps(
            [
                {
                    "slug": slug,
                    "fact": fact,
                    "source_url": "https://news.example.test/held/private",
                    "source_date": "2023-06-17",
                    "title": "Example interview",
                }
            ]
        ),
        encoding="utf-8",
    )
    return path


def test_register_guard_fails_when_withheld_fact_has_no_entry(tmp_path: Path) -> None:
    missing = tmp_path / "no-such.json"
    fails = check_withheld_register_for_profiles([_profile("synth-person")], path=missing)
    assert fails
    assert any("missing" in f or "no matching entry" in f for f in fails)


def test_register_guard_fails_when_entry_is_for_a_different_fact(tmp_path: Path) -> None:
    reg = _write_register(tmp_path / "withheld-sources.json", fact="career")
    fails = check_withheld_register_for_profiles([_profile("synth-person")], path=reg)
    assert any("no matching entry" in f for f in fails)


def test_register_guard_passes_when_entry_matches(tmp_path: Path) -> None:
    reg = _write_register(tmp_path / "withheld-sources.json")
    assert check_withheld_register_for_profiles([_profile("synth-person")], path=reg) == []


def test_register_guard_ignores_privacy_page_wording_without_withheld_facts(tmp_path: Path) -> None:
    """A page that only names the label (as the privacy page does) must not require a register."""
    missing = tmp_path / "no-such.json"
    page = tmp_path / "site" / "privacy" / "index.html"
    page.parent.mkdir(parents=True)
    page.write_text(
        f"<p>Labels include {WITHHELD_LABEL}. {WITHHELD_PUBLIC_TEXT}</p>",
        encoding="utf-8",
    )
    profiles = [_profile("synth-person", withheld=False)]
    assert check_withheld_register_for_profiles(profiles, path=missing) == []
    # The leak check also stays quiet when there is no register to leak from.
    assert check_tree_for_withheld_urls(page.parent.parent, path=missing) == []


def test_register_guard_can_be_disabled(tmp_path: Path) -> None:
    missing = tmp_path / "no-such.json"
    assert check_withheld_register_for_profiles([_profile("synth-person")], path=missing, require_register=False) == []


def test_title_leak_catches_tag_split_and_en_dash(tmp_path: Path) -> None:
    site = tmp_path / "site"
    site.mkdir()
    (site / "index.html").write_text("<p>See the Exam<b>ple inter</b>view — full text.</p>", encoding="utf-8")
    entries = [{"source_url": "https://news.example.test/x", "title": "Example interview"}]
    fails = check_tree_for_withheld_urls(site, entries)
    assert any("withheld-source title" in f for f in fails)
