"""Gazette-only stub CV profiles (CHG-PW-013)."""

from __future__ import annotations

import csv
from pathlib import Path

from pwatch.dq import check_profile
from pwatch.profiles import (
    load_held_profiles,
    load_profile_dir,
    render_markdown,
    roster_index,
    slug_from_gazetted_name,
    stub_cv_profile,
)
from pwatch.roster import row_to_profile
from pwatch.settings import PROFILES_DIR, ROSTER_DIR


def test_slug_from_gazetted_name_folds_diacritics_and_apostrophes() -> None:
    assert slug_from_gazetted_name("DOMINIC GÜNTHER BAUER") == "dominic-gunther-bauer"
    assert slug_from_gazetted_name("ZONÉ HUGHES") == "zone-hughes"
    assert slug_from_gazetted_name("JONATHAN ANDRÉ PERRONET THOMPSON") == "jonathan-andre-perronet-thompson"
    assert slug_from_gazetted_name("CAROLINE DESIRÉ ANN LEWIN") == "caroline-desire-ann-lewin"
    assert slug_from_gazetted_name("RENÉ FIONA BENJAMIN") == "rene-fiona-benjamin"
    assert slug_from_gazetted_name("SIPH'ESIHLE SIBANDE") == "siphesihle-sibande"
    assert slug_from_gazetted_name("TSUNG-WEI LEE") == "tsung-wei-lee"
    assert slug_from_gazetted_name("NKOSEPHAYO GOD-SLOVE ZUNGU") == "nkosephayo-god-slove-zungu"


def test_existing_profile_slugs_match_the_helper() -> None:
    for path, doc in load_profile_dir(PROFILES_DIR) + load_held_profiles(PROFILES_DIR):
        assert path.stem == slug_from_gazetted_name(doc["name"]["value"])


def test_stub_from_synthetic_row_passes_dq_and_renders(repo_root) -> None:
    from datetime import date

    row = {
        "name": "THABO TESTWARD",
        "party": "SYNTHETIC PARTY",
        "seat_type": "ward",
        "ward_number": "1",
        "ward_id": "79800001",
        "pr_list_rank": "",
        "council": "City of Johannesburg",
        "source_url": "https://example.test/gazette.pdf",
        "source_date": "2026-11-13",
        "source_page": "2",
        "retrieved_at": "2026-11-15T16:10:03+00:00",
        "positions": "",
        "education": "",
        "career": "",
        "court_matters": "",
        "scandals": "",
    }
    profile = stub_cv_profile(row)
    assert profile["slug"] == "thabo-testward"
    assert profile["change"] == "CHG-PW-013"
    assert profile["name"]["value"] == "THABO TESTWARD"
    assert profile["name"]["label"] == "Confirmed"
    assert profile["name"]["source_page"] == 2
    assert profile["party"]["label"] == "Confirmed"
    assert profile["seat_type"]["value"] == "ward"
    assert profile["career"]["label"] == "Unknown"
    assert profile["education"]["label"] == "Unknown"
    assert profile["positions"]["label"] == "Unknown"
    assert profile["cv"] == []
    assert profile["court_matters"] == []
    assert profile["scandals"] == []
    roster = roster_index([row_to_profile(row)])
    assert check_profile(profile, drafts_root=repo_root, as_of=date(2026, 11, 20), roster=roster) == []
    md = render_markdown(profile)
    assert "THABO TESTWARD" in md
    assert "Confirmed" in md
    assert "Unknown — not yet sourced" in md
    assert "Right of reply" not in md


def test_roster_has_a_unique_profile_slug_for_every_gazetted_row() -> None:
    active = load_profile_dir(PROFILES_DIR)
    held = load_held_profiles(PROFILES_DIR)
    assert len(active) == 269 and len(held) == 1
    rows = list(csv.DictReader((ROSTER_DIR / "joburg-2026.csv").open(encoding="utf-8")))
    stubs = [stub_cv_profile(r) for r in rows]
    slugs = [s["slug"] for s in stubs]
    assert len(rows) == 270
    assert len(set(slugs)) == 270
    on_disk = {p.stem for p, _ in active} | {p.stem for p, _ in held}
    assert on_disk == set(slugs)
    new_on_disk = [d for _, d in active if d.get("change") == "CHG-PW-013"]
    assert len(new_on_disk) == 245
    assert all(d["name"]["label"] == "Confirmed" and d["council"]["value"] == "City of Johannesburg" for d in new_on_disk)
    assert all((_, d) and d.get("change") != "CHG-PW-013" for _, d in held)
