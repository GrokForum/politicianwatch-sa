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
