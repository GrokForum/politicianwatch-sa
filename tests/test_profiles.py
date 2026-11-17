"""CHG-PW-002 rules for CV profiles, on synthetic fixtures only."""

from copy import deepcopy
from datetime import date

from pwatch.dq import check_profile, run
from pwatch.profiles import BLANK_REPLY, UNKNOWN_PLACEHOLDER, render_markdown, roster_index
from pwatch.schema import fact

AS_OF = date(2026, 11, 15)
NEWS = "https://example.test/news/2026-09-06-synthetic"


def _cv_profile(synthetic_profiles):
    p = deepcopy(synthetic_profiles[0])
    p["slug"] = "thabo-testward"
    p["known_as"] = fact("Thabo Test", "Reported", NEWS, "2026-09-06", "2026-11-15T20:00:00+02:00")
    p["cv"] = [
        {**fact("Former synthetic MMC", "Reported", NEWS, "2026-09-06", "2026-11-15T20:00:00+02:00"), "field": "position"}
    ]
    p["identity_match"] = {"matched_details": ["full name", "party and ward"], "note": None}
    return p


def test_cv_profile_passes(synthetic_profiles, repo_root):
    p = _cv_profile(synthetic_profiles)
    assert check_profile(p, drafts_root=repo_root, as_of=AS_OF, roster=roster_index(synthetic_profiles)) == []


def test_fact_without_retrieved_at_fails(synthetic_profiles, repo_root):
    p = _cv_profile(synthetic_profiles)
    p["cv"][0]["retrieved_at"] = None
    failures = check_profile(p, drafts_root=repo_root, as_of=AS_OF)
    assert any("retrieved_at" in f for f in failures)


def test_cv_item_without_label_or_bad_field_fails(synthetic_profiles, repo_root):
    p = _cv_profile(synthetic_profiles)
    p["cv"][0].pop("label")
    p["cv"].append({**fact("x", "Reported", NEWS, "2026-09-06", "2026-11-15T20:00:00+02:00"), "field": "hobby"})
    failures = check_profile(p, drafts_root=repo_root, as_of=AS_OF)
    assert any("label" in f for f in failures)
    assert any("field must be one of" in f for f in failures)


def test_linked_sources_need_two_identity_details(synthetic_profiles, repo_root):
    p = _cv_profile(synthetic_profiles)
    p["identity_match"] = {"matched_details": ["full name only"]}
    failures = check_profile(p, drafts_root=repo_root, as_of=AS_OF)
    assert any("identity_match" in f for f in failures)
    p.pop("identity_match")
    assert any("identity_match" in f for f in check_profile(p, drafts_root=repo_root, as_of=AS_OF))


def test_gazette_only_profile_needs_no_identity_match(synthetic_profiles, repo_root):
    assert "identity_match" not in synthetic_profiles[0]
    assert check_profile(synthetic_profiles[0], drafts_root=repo_root, as_of=AS_OF) == []


def test_profile_must_match_its_roster_row(synthetic_profiles, repo_root):
    roster = roster_index(synthetic_profiles)
    p = _cv_profile(synthetic_profiles)
    p["party"] = dict(p["party"], value="OTHER PARTY")
    assert any("party" in f and "roster" in f for f in check_profile(p, drafts_root=repo_root, as_of=AS_OF, roster=roster))
    p = _cv_profile(synthetic_profiles)
    p["name"] = dict(p["name"], value="NOT GAZETTED")
    result = run([p], drafts_root=repo_root, as_of=AS_OF, roster=roster)
    assert result["status"] == "fail"
    assert any("not in the gazetted roster" in f for f in result["failures"])


def test_pending_ror_may_leave_deadline_for_owner(synthetic_profiles, repo_root):
    p = deepcopy(synthetic_profiles[2])
    ror = p["scandals"][0]["right_of_reply"]
    ror["deadline"] = None
    assert check_profile(p, drafts_root=repo_root, as_of=AS_OF) == []
    ror.update(status="sent", sent_at="2026-11-16T08:00:00+02:00", recorded_by="owner")
    assert any("deadline is required" in f for f in check_profile(p, drafts_root=repo_root, as_of=AS_OF))


def test_draft_without_not_sent_marker_fails(synthetic_profiles, tmp_path):
    d = tmp_path / "drafts" / "right-of-reply"
    d.mkdir(parents=True)
    (d / "SYNTH-001.md").write_text("# a draft with no marker\n", encoding="utf-8")
    failures = check_profile(synthetic_profiles[2], drafts_root=tmp_path, as_of=AS_OF)
    assert any("DRAFT: NOT SENT" in f for f in failures)


def test_render_shows_pending_blank_reply_and_unknown_placeholders(synthetic_profiles):
    p = deepcopy(synthetic_profiles[2])
    p["unknown_fields"] = ["education"]
    md = render_markdown(p)
    assert "Right of reply: pending" in md
    assert BLANK_REPLY in md
    assert UNKNOWN_PLACEHOLDER in md
    assert "`Alleged`" in md


def test_marker_must_be_first_nonempty_line(synthetic_profiles, tmp_path):
    d = tmp_path / "drafts" / "right-of-reply"
    d.mkdir(parents=True)
    marker = "DRAFT: NOT SENT. The owner sends personally. The bot never sends."
    (d / "SYNTH-001.md").write_text(f"# Title first\n\n{marker}\n", encoding="utf-8")
    failures = check_profile(synthetic_profiles[2], drafts_root=tmp_path, as_of=AS_OF)
    assert any("first non-empty line" in f for f in failures)
    (d / "SYNTH-001.md").write_text(f"\n\n{marker}\n\n# Title\n", encoding="utf-8")
    assert check_profile(synthetic_profiles[2], drafts_root=tmp_path, as_of=AS_OF) == []


def test_also_sourced_entries_need_url_date_and_retrieved_at(synthetic_profiles, repo_root):
    p = _cv_profile(synthetic_profiles)
    p["cv"][0]["also_sourced"] = [{"source_url": NEWS, "source_date": "2026-09-06"}]
    failures = check_profile(p, drafts_root=repo_root, as_of=AS_OF)
    assert any("also_sourced[0]: missing retrieved_at" in f for f in failures)
    p["cv"][0]["also_sourced"][0]["retrieved_at"] = "2026-11-15T20:00:00+02:00"
    assert check_profile(p, drafts_root=repo_root, as_of=AS_OF) == []


def test_unknown_surname_placeholder_renders(synthetic_profiles):
    p = _cv_profile(synthetic_profiles)
    p["full_name_surname"] = fact(None, "Unknown")
    assert check_profile(p, drafts_root=None, as_of=AS_OF) == []
    assert f"**Surname in full legal name:** {UNKNOWN_PLACEHOLDER}" in render_markdown(p)


def test_adverse_item_cannot_outrank_its_identity_link(synthetic_profiles, repo_root):
    p = deepcopy(synthetic_profiles[2])
    item = p["scandals"][0]
    item["identity_link_label"] = "Reported"
    item["label"] = "Confirmed"
    failures = check_profile(p, drafts_root=repo_root, as_of=AS_OF)
    assert any("identity link to the gazetted person is Reported" in f for f in failures)
    item["label"] = "Reported"
    assert check_profile(p, drafts_root=repo_root, as_of=AS_OF) == []
    item["identity_link_label"] = "Probably"
    assert any("invalid identity_link_label" in f for f in check_profile(p, drafts_root=repo_root, as_of=AS_OF))


def test_reported_conviction_status_is_in_schema_and_renders(synthetic_profiles, repo_root):
    import json

    schema = json.loads((repo_root / "schemas" / "profile.schema.json").read_text(encoding="utf-8"))
    assert "reported_conviction" in json.dumps(schema)
    p = deepcopy(synthetic_profiles[2])
    p["scandals"][0]["matter_status"] = "reported_conviction"
    p["scandals"][0]["identity_link_label"] = "Reported"
    assert check_profile(p, drafts_root=repo_root, as_of=AS_OF) == []
    md = render_markdown(p)
    assert "`reported_conviction`" in md
    assert "Identity link to the gazetted person:** Reported" in md


def test_also_sourced_date_and_url_formats_are_checked(synthetic_profiles, repo_root):
    p = _cv_profile(synthetic_profiles)
    good = {"source_url": NEWS, "source_date": "2026-09-06", "retrieved_at": "2026-11-17T11:00:00+02:00"}
    p["cv"][0]["also_sourced"] = [dict(good)]
    assert check_profile(p, drafts_root=repo_root, as_of=AS_OF) == []
    bad = [
        ({"source_url": "example.test/no-scheme"}, "not a valid http(s) URL"),
        ({"source_url": "ftp://example.test/x"}, "not a valid http(s) URL"),
        ({"source_date": "6 Sep 2026"}, "source_date must be YYYY-MM-DD"),
        ({"source_date": "2026-02-30"}, "source_date must be YYYY-MM-DD"),
        ({"retrieved_at": "yesterday"}, "retrieved_at must be an ISO 8601 datetime"),
        ({"retrieved_at": "2026-11-17T11:00:00"}, "retrieved_at needs a UTC offset"),
    ]
    for change, message in bad:
        p["cv"][0]["also_sourced"] = [{**good, **change}]
        failures = check_profile(p, drafts_root=repo_root, as_of=AS_OF)
        assert any(message in f for f in failures), (change, failures)


def _write_profile(path, doc):
    import json

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(doc), encoding="utf-8")


def test_held_profiles_are_excluded_from_batch_dq_and_render(synthetic_profiles, tmp_path, capsys):
    """CHG-PW-003 fix 1: a profile in _hold/ or with status on_hold is not counted, rendered or checked."""
    from pwatch.cli import main
    from pwatch.profiles import load_held_profiles, load_profile_dir

    root = tmp_path / "profiles"
    active = _cv_profile(synthetic_profiles)
    _write_profile(root / "active.json", active)
    (root / "active.md").write_text(render_markdown(active), encoding="utf-8")
    held_dir = deepcopy(active)
    held_dir["slug"] = "held-in-dir"
    held_dir["identity_match"] = {"matched_details": ["surname only"], "note": None}  # would fail dq if checked
    _write_profile(root / "_hold" / "held-in-dir.json", held_dir)
    held_flag = deepcopy(held_dir)
    held_flag["slug"] = "held-flag"
    held_flag["status"] = "on_hold"
    _write_profile(root / "held-flag.json", held_flag)  # no .md: render --check must not ask for one

    assert [d["slug"] for _, d in load_profile_dir(root)] == ["thabo-testward"]
    assert sorted(d["slug"] for _, d in load_held_profiles(root)) == ["held-flag", "held-in-dir"]
    assert main(["render", "--check", "--profiles-dir", str(root)]) == 0
    capsys.readouterr()
    assert check_profile(held_dir, as_of=AS_OF) != []  # the held profile really would fail the gate
