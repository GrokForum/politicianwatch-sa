"""Gazette parser tests use a synthetic excerpt only, never the live PDF."""

from pathlib import Path

from pwatch.parsers.gazette import parse_joburg_text

FIXTURE = Path(__file__).parent / "fixtures" / "gazette_joburg_excerpt.txt"


def test_parses_three_synthetic_joburg_rows_and_ignores_other_municipalities():
    rows = parse_joburg_text(FIXTURE.read_text(encoding="utf-8"))
    assert len(rows) == 3
    names = {r["name"] for r in rows}
    assert names == {"THABO TESTWARD", "KEVIN EXAMPLE", "NOMVULA FIXTURE"}
    assert all(r["council"] == "City of Johannesburg" for r in rows)
    assert all(r["party"] == "SYNTHETIC PARTY" for r in rows)


def test_source_page_comes_from_pdf_page_number():
    rows = parse_joburg_text(FIXTURE.read_text(encoding="utf-8"))
    by_name = {r["name"]: r for r in rows}
    assert by_name["THABO TESTWARD"]["source_page"] == 2
    assert by_name["KEVIN EXAMPLE"]["source_page"] == 2
    assert by_name["NOMVULA FIXTURE"]["source_page"] == 3


def test_ward_and_pr_fields():
    rows = {r["name"]: r for r in parse_joburg_text(FIXTURE.read_text(encoding="utf-8"))}
    w = rows["THABO TESTWARD"]
    assert w["seat_type"] == "ward"
    assert w["ward_number"] == 1
    assert w["ward_id"] == "79800001"
    assert w["pr_list_rank"] is None
    pr = rows["NOMVULA FIXTURE"]
    assert pr["seat_type"] == "PR"
    assert pr["ward_number"] is None
    assert pr["ward_id"] is None
    assert pr["pr_list_rank"] == 1
