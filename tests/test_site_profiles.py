"""CHG-PW-007: draft profiles on the site; every claim labelled, sourced and dated; RoR pending shown."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import pytest

from pwatch.cli import main
from pwatch.profiles import load_held_profiles, load_profile_dir
from pwatch.settings import LABELS, PROFILES_DIR
from pwatch.site import build_site, check_site
from pwatch.site_profiles import check_claims, expected_fact_ids, scan_claims

NOW = datetime(2026, 11, 19, 1, 30, tzinfo=timezone.utc)


def _with_slugs(profiles: list[dict]) -> list[tuple[Path, dict]]:
    out = []
    for p in profiles:
        slug = p["name"]["value"].lower().replace(" ", "-")
        out.append((Path(f"{slug}.json"), {**p, "slug": slug, "unknown_fields": ["Council office for the 2026–2031 term"]}))
    return out


@pytest.fixture
def synth(synthetic_profiles: list[dict]) -> list[tuple[Path, dict]]:
    return _with_slugs(synthetic_profiles)


@pytest.fixture
def held(synthetic_profiles: list[dict]) -> list[tuple[Path, dict]]:
    p = dict(synthetic_profiles[0], status="on_hold")
    p["name"] = dict(p["name"], value="HELD PERSON")
    return [(Path("_hold/held-person.json"), dict(p, slug="held-person"))]


@pytest.fixture
def built(tmp_path: Path, synth) -> Path:
    out = tmp_path / "_site"
    build_site(out, profiles=synth, now=NOW)
    return out


def test_synthetic_site_passes_with_coverage(built: Path, synth, held) -> None:
    assert check_site(built, profiles=synth, held=held) == []
    assert sorted(p.parent.name for p in (built / "profiles").glob("*/index.html")) == sorted(d["slug"] for _, d in synth)


def test_every_claim_shows_label_and_non_unknown_claims_link_a_dated_source(built: Path) -> None:
    claims = [c for p in built.rglob("*.html") for c in scan_claims(p.read_text(encoding="utf-8"))]
    assert claims
    for c in claims:
        assert c["label"] in LABELS and c["label"] in c["badge"]
        if c["label"] != "Unknown":
            assert any(h.startswith(("http://", "https://")) for h in c["links"]), c
            assert any(len(d) == 10 for d in c["dates"]), c


def test_adverse_item_shows_right_of_reply_pending_and_blank_reply(built: Path) -> None:
    html = (built / "profiles" / "kevin-example" / "index.html").read_text(encoding="utf-8")
    adverse = [c for c in scan_claims(html) if c["adverse"]]
    assert len(adverse) == 1 and adverse[0]["label"] == "Alleged"
    assert "".join(adverse[0]["ror_text"]) == "Right of reply: pending"
    assert "(blank — no reply recorded)" in html


def test_every_fact_is_rendered(built: Path, synth) -> None:
    for _, d in synth:
        html = (built / "profiles" / d["slug"] / "index.html").read_text(encoding="utf-8")
        assert {c["fact"] for c in scan_claims(html)} >= expected_fact_ids(d)


BROKEN = [
    (lambda h: h.replace('class="src-link"', 'class="x"'), "no http(s) source link"),
    (lambda h: h.replace("<time ", "<span "), "no source date"),
    (lambda h: h.replace('class="label label-Confirmed">Confirmed', 'class="label label-Confirmed">'), "label is not shown"),
    (lambda h: h.replace('data-label="Confirmed"', 'data-label="Probable"', 1), "is not one of"),
    (lambda h: h.replace(">Right of reply: pending<", ">Right of reply: sent<"), "Right of reply: pending"),
    (lambda h: h.replace('class="ror"', 'class="x"'), "no 'Right of reply' line"),
    (lambda h: h.replace('href="https://example.test/news', 'href="javascript:alert(1)//', 1), "no http(s) source link"),
]


@pytest.mark.parametrize("mutate, expected", BROKEN)
def test_claim_check_fails_closed(built: Path, mutate, expected: str) -> None:
    html = (built / "profiles" / "kevin-example" / "index.html").read_text(encoding="utf-8")
    fails = check_claims("kevin", mutate(html))
    assert any(expected in f for f in fails), fails


def test_coverage_fails_for_missing_fact_missing_profile_and_held_page(built: Path, synth, held) -> None:
    page = built / "profiles" / "kevin-example" / "index.html"
    page.write_text(page.read_text(encoding="utf-8").replace('data-fact="scandals[0]"', 'data-fact="gone"'), encoding="utf-8")
    (built / "profiles" / "thabo-testward" / "index.html").unlink()
    (built / "profiles" / "held-person").mkdir()
    (built / "profiles" / "held-person" / "index.html").write_text("x", encoding="utf-8")
    fails = check_site(built, profiles=synth, held=held)
    assert any("fact scandals[0] is not rendered" in f for f in fails)
    assert any("thabo-testward has no page" in f for f in fails)
    assert any("held profile held-person" in f for f in fails)


def test_source_missing_in_data_fails_the_build_check(tmp_path: Path, synth) -> None:
    broken = [(p, dict(d)) for p, d in synth]
    broken[0][1]["party"] = dict(broken[0][1]["party"], source_url=None)
    out = tmp_path / "s"
    build_site(out, profiles=broken, now=NOW)
    assert any("[party]: claim has no http(s) source link" in f for f in check_site(out, profiles=broken))


def test_real_profiles_build_pages_and_pass(tmp_path: Path) -> None:
    active = load_profile_dir(PROFILES_DIR)
    held_real = load_held_profiles(PROFILES_DIR)
    assert len(active) == 269 and held_real
    out = tmp_path / "s"
    m = build_site(out, profiles=active, now=NOW)
    assert m["profiles"] == 269
    assert check_site(out, profiles=active, held=held_real) == []
    assert len(list((out / "profiles").glob("*/index.html"))) == 269
    for _, d in held_real:
        assert not (out / "profiles" / d["slug"]).exists()
        assert d["name"]["value"] not in (out / "index.html").read_text(encoding="utf-8")
    pending = sum(
        "".join(c.get("ror_text", [])) == "Right of reply: pending"
        for p in (out / "profiles").glob("*/index.html")
        for c in scan_claims(p.read_text(encoding="utf-8"))
        if c["adverse"]
    )
    assert pending == 6


def test_cli_site_check_uses_committed_profiles(tmp_path: Path) -> None:
    out = tmp_path / "s"
    assert main(["site", "build", "--out", str(out)]) == 0
    assert main(["site", "check", str(out)]) == 0
    next((out / "profiles").glob("*/index.html")).unlink()
    assert main(["site", "check", str(out)]) == 2
    assert main(["site", "check", "--no-data", str(out)]) == 0


def test_home_and_profile_wording_exclude_unknown_items(built: Path) -> None:
    """Janus on PR #6, applied to the CHG-PW-007 pages: Unknown items carry no source link."""
    home = (built / "index.html").read_text(encoding="utf-8")
    assert "every item except an Unknown or Withheld (POPIA) one links to its source with a date" in home
    prof = (built / "profiles" / "kevin-example" / "index.html").read_text(encoding="utf-8")
    assert "every item except an Unknown or Withheld (POPIA) one links a dated source" in prof
    assert "Every item shows an evidence label and a dated source" not in prof


def test_owner_approved_pi_source_note_is_rendered_next_to_the_source():
    # CHG-PW-011: the note shows with the link; ordinary fact notes are not rendered.
    from pwatch.settings import PI_SOURCE_NOTE
    from pwatch.site_profiles import claim

    base = {"value": "A degree", "label": "Reported", "source_url": "https://news.example.test/i", "source_date": "2023-06-17", "retrieved_at": "2026-11-17"}
    html = claim("education", "Education", dict(base, note=PI_SOURCE_NOTE, owner_approved_pi_source="2026-11-19 16:27 SAST (CHG-PW-011)"))
    assert f'<span class="src-note">{PI_SOURCE_NOTE}</span>' in html
    assert "src-note" not in claim("education", "Education", dict(base, note="some other note"))


def test_withheld_fact_renders_without_a_source_link():
    from pwatch.settings import WITHHELD_LABEL, WITHHELD_PUBLIC_TEXT
    from pwatch.site_profiles import check_claims, claim

    fact = {"value": None, "label": WITHHELD_LABEL, "source_url": None, "source_date": None, "retrieved_at": None}
    html = claim("education", "Education", fact)
    assert WITHHELD_LABEL in html
    assert WITHHELD_PUBLIC_TEXT in html
    assert "Unknown — not yet found" not in html
    assert "src-link" not in html
    assert check_claims("edu", f"<ul>{html}</ul>") == []


def _write_withheld_register(tmp_path: Path, monkeypatch, *, url: str = "https://news.example.test/held/private", title: str = "Example interview") -> None:
    import json

    from pwatch import withheld as withheld_mod

    private = tmp_path / "withheld-sources.json"
    private.write_text(
        json.dumps(
            {
                "entries": [
                    {
                        "slug": "anyone",
                        "fact": "education",
                        "source_url": url,
                        "source_date": "2023-06-17",
                        "title": title,
                    }
                ]
            }
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr(withheld_mod, "WITHHELD_SOURCES_PATH", private)


def test_site_check_passes_on_clean_output_when_a_register_exists(tmp_path: Path, built: Path, synth, monkeypatch) -> None:
    _write_withheld_register(tmp_path, monkeypatch)
    assert check_site(built, profiles=synth) == []


@pytest.mark.parametrize(
    "planted, expected",
    [
        ("HTTPS://NEWS.EXAMPLE.TEST/HELD/PRIVATE", "withheld-source URL"),
        ("https://news.example.test/held%2Fprivate", "withheld-source URL"),
        ("https://news.example.test/held&#47;private", "withheld-source URL"),
        ("Standalone. Example interview.", "withheld-source title"),
    ],
)
def test_site_check_fails_on_normalised_url_or_title_leak(tmp_path: Path, built: Path, monkeypatch, planted: str, expected: str) -> None:
    _write_withheld_register(tmp_path, monkeypatch)
    page = built / "profiles" / "kevin-example" / "index.html"
    page.write_text(page.read_text(encoding="utf-8") + f"<p>{planted}</p>", encoding="utf-8")
    fails = check_site(built)
    assert any(expected in f for f in fails), fails



def test_site_check_fails_if_private_dir_is_in_output(tmp_path: Path, built: Path, synth, monkeypatch) -> None:
    _write_withheld_register(tmp_path, monkeypatch)
    private = built / "private"
    private.mkdir()
    (private / "secret.json").write_text("{}", encoding="utf-8")
    fails = check_site(built, profiles=synth)
    assert any("private/" in f for f in fails)


def test_site_check_fails_when_a_withheld_fact_has_no_register_entry(tmp_path: Path, monkeypatch) -> None:
    """Passing the profiles in, not the privacy-page wording, is what requires a register entry."""
    import json
    from datetime import datetime, timezone

    from pwatch import withheld as withheld_mod
    from pwatch.schema import fact, unknown_fact
    from pwatch.site import build_site

    now = datetime(2026, 11, 19, 1, 0, tzinfo=timezone.utc)
    monkeypatch.setattr(withheld_mod, "WITHHELD_SOURCES_PATH", tmp_path / "no-such-register.json")
    person = {
        "slug": "synth-withheld",
        "name": fact("SYNTH WITHHELD", "Confirmed", "https://example.test/g.pdf", "2026-11-13", "2026-11-15", 43),
        "party": fact("SYNTHETIC PARTY", "Confirmed", "https://example.test/g.pdf", "2026-11-13", "2026-11-15", 43),
        "seat_type": fact("ward", "Confirmed", "https://example.test/g.pdf", "2026-11-13", "2026-11-15", 43),
        "ward_number": fact(1, "Confirmed", "https://example.test/g.pdf", "2026-11-13", "2026-11-15", 43),
        "council": fact("City of Johannesburg", "Confirmed", "https://example.test/g.pdf", "2026-11-13", "2026-11-15", 43),
        "ward_id": "79800001",
        "pr_list_rank": None,
        "positions": unknown_fact(),
        "career": unknown_fact(),
        "education": {"value": None, "label": "Withheld (POPIA)", "source_url": None, "source_date": None, "retrieved_at": None},
        "cv": [],
        "court_matters": [],
        "scandals": [],
    }
    profiles = [(tmp_path / "synth-withheld.json", person)]
    out = tmp_path / "site"
    build_site(out, profiles=profiles, now=now)
    fails = check_site(out, profiles=profiles)
    assert any("missing" in f or "no matching entry" in f for f in fails), fails


def test_site_check_does_not_require_a_register_when_no_fact_is_withheld(tmp_path: Path, built: Path, synth, monkeypatch) -> None:
    from pwatch import withheld as withheld_mod

    monkeypatch.setattr(withheld_mod, "WITHHELD_SOURCES_PATH", tmp_path / "no-such-register.json")
    # The built synthetic site names the label on the privacy page, but no fact is withheld.
    assert check_site(built, profiles=synth) == []



def test_cli_site_build_fails_when_the_withheld_register_is_missing(tmp_path: Path, monkeypatch) -> None:
    """cmd_site_build must surface leak_fails (exit 2). Removing that handling fails this test."""
    import json
    from datetime import datetime, timezone

    from pwatch import withheld as withheld_mod
    from pwatch.cli import main
    from pwatch.schema import fact, unknown_fact

    monkeypatch.setattr(withheld_mod, "WITHHELD_SOURCES_PATH", tmp_path / "no-such-register.json")
    profiles_dir = tmp_path / "profiles"
    profiles_dir.mkdir()
    person = {
        "slug": "synth-withheld",
        "name": fact("SYNTH WITHHELD", "Confirmed", "https://example.test/g.pdf", "2026-11-13", "2026-11-15", 43),
        "party": fact("SYNTHETIC PARTY", "Confirmed", "https://example.test/g.pdf", "2026-11-13", "2026-11-15", 43),
        "seat_type": fact("ward", "Confirmed", "https://example.test/g.pdf", "2026-11-13", "2026-11-15", 43),
        "ward_number": fact(1, "Confirmed", "https://example.test/g.pdf", "2026-11-13", "2026-11-15", 43),
        "council": fact("City of Johannesburg", "Confirmed", "https://example.test/g.pdf", "2026-11-13", "2026-11-15", 43),
        "ward_id": "79800001",
        "pr_list_rank": None,
        "positions": unknown_fact(),
        "career": unknown_fact(),
        "education": {"value": None, "label": "Withheld (POPIA)", "source_url": None, "source_date": None, "retrieved_at": None},
        "cv": [],
        "court_matters": [],
        "scandals": [],
    }
    (profiles_dir / "synth-withheld.json").write_text(json.dumps(person), encoding="utf-8")
    out = tmp_path / "site"
    code = main(["site", "build", "--out", str(out), "--profiles-dir", str(profiles_dir)])
    assert code == 2
