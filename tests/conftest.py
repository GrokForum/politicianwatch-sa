"""Synthetic fixtures only. Tests must not fetch live sources or read production hosts."""

from __future__ import annotations

from pathlib import Path

import pytest

from pwatch.ror import default_pending
from pwatch.schema import fact, unknown_fact

FIXTURES = Path(__file__).parent / "fixtures"
GAZETTE_URL = "https://example.test/gazette/55741.pdf"
RETRIEVED = "2026-11-15T16:00:00+00:00"
DRAFT_REL = "drafts/right-of-reply/SYNTH-001.md"


def sourced(value, page=10):
    return fact(value, "Confirmed", GAZETTE_URL, "2026-11-13", RETRIEVED, page)


@pytest.fixture
def fixtures_dir() -> Path:
    return FIXTURES


@pytest.fixture
def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


@pytest.fixture
def synthetic_profiles(repo_root: Path) -> list[dict]:
    """Two clean public-role profiles and one with a pending adverse item."""
    base = {
        "council": sourced("City of Johannesburg"),
        "positions": unknown_fact(),
        "education": unknown_fact(),
        "career": unknown_fact(),
        "court_matters": [],
        "scandals": [],
    }
    ward = {
        **base,
        "name": sourced("THABO TESTWARD"),
        "party": sourced("SYNTHETIC PARTY"),
        "seat_type": sourced("ward"),
        "ward_number": sourced(1),
        "ward_id": "79800001",
        "pr_list_rank": None,
    }
    pr = {
        **base,
        "name": sourced("NOMVULA FIXTURE"),
        "party": sourced("SYNTHETIC PARTY"),
        "seat_type": sourced("PR"),
        "ward_number": sourced(None),
        "pr_list_rank": 1,
    }
    adverse = {
        **base,
        "name": sourced("KEVIN EXAMPLE"),
        "party": sourced("SYNTHETIC PARTY"),
        "seat_type": sourced("ward"),
        "ward_number": sourced(2),
        "identity_match": {
            "matched_details": [
                "full name as gazetted (synthetic)",
                "party and ward number named in the synthetic report",
            ],
            "note": "synthetic fixture",
        },
        "scandals": [
            {
                **fact(
                    "A 2020 news report alleged a conflict of interest in a council tender.",
                    "Alleged",
                    "https://example.test/news/2020-01-15-synthetic",
                    "2020-01-15",
                    RETRIEVED,
                ),
                "right_of_reply": default_pending(DRAFT_REL, "2026-12-15"),
            }
        ],
    }
    return [ward, pr, adverse]
