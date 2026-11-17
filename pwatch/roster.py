"""Load the committed Joburg roster CSV into profile objects with Unknown placeholders."""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Any

from pwatch.schema import fact, unknown_fact
from pwatch.settings import (
    COUNCIL_NAME,
    GAZETTE_DATE,
    GAZETTE_PDF_URL,
    ROSTER_DIR,
)


def empty_to_none(value: str | None) -> str | None:
    if value is None:
        return None
    value = value.strip()
    return value or None


def row_to_profile(row: dict[str, str], retrieved_at: str | None = None) -> dict[str, Any]:
    source_url = empty_to_none(row.get("source_url")) or GAZETTE_PDF_URL
    source_date = empty_to_none(row.get("source_date")) or GAZETTE_DATE
    retrieved = empty_to_none(row.get("retrieved_at")) or retrieved_at
    page_raw = empty_to_none(row.get("source_page"))
    page = int(page_raw) if page_raw else None
    seat_type = empty_to_none(row.get("seat_type"))
    ward_raw = empty_to_none(row.get("ward_number"))
    ward_number = int(ward_raw) if ward_raw else None

    def sourced(value: Any) -> dict[str, Any]:
        return fact(value, "Confirmed", source_url, source_date, retrieved, page)

    return {
        "name": sourced(empty_to_none(row.get("name"))),
        "party": sourced(empty_to_none(row.get("party"))),
        "seat_type": sourced(seat_type),
        "ward_number": sourced(ward_number),
        "council": sourced(empty_to_none(row.get("council")) or COUNCIL_NAME),
        "ward_id": empty_to_none(row.get("ward_id")),
        "pr_list_rank": int(row["pr_list_rank"]) if empty_to_none(row.get("pr_list_rank")) else None,
        "positions": unknown_fact(),
        "education": unknown_fact(),
        "career": unknown_fact(),
        "court_matters": [],
        "scandals": [],
    }


def load_csv(path: Path) -> list[dict[str, Any]]:
    with path.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        return [row_to_profile(row) for row in reader]


def default_roster_path() -> Path:
    return ROSTER_DIR / "joburg-2026.csv"


def load_joburg_roster(path: Path | None = None) -> list[dict[str, Any]]:
    return load_csv(path or default_roster_path())
