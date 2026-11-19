"""DQ gate tests on synthetic profiles."""

from datetime import date
from copy import deepcopy

from pwatch.dq import EXIT_NOT_RELEASABLE, EXIT_OK, check_profile, exit_code, run
from pwatch.schema import fact


def test_clean_and_pending_adverse_profiles_pass(synthetic_profiles, repo_root):
    result = run(synthetic_profiles, drafts_root=repo_root, as_of=date(2026, 11, 15))
    assert result["status"] == "pass"
    assert result["failure_count"] == 0
    assert exit_code(result) == EXIT_OK


def test_missing_label_fails(synthetic_profiles, repo_root):
    profiles = deepcopy(synthetic_profiles)
    profiles[0]["education"] = {
        "value": "a degree",
        "source_url": "https://example.test/x",
        "source_date": "2020-01-01",
        "retrieved_at": "2026-11-15T16:00:00+00:00",
    }  # no label
    failures = check_profile(profiles[0], drafts_root=repo_root, as_of=date(2026, 11, 15))
    assert any("label" in f.lower() for f in failures)


def test_confirmed_fact_missing_source_fails(synthetic_profiles, repo_root):
    profiles = deepcopy(synthetic_profiles)
    profiles[0]["party"] = fact("SYNTHETIC PARTY", "Confirmed", None, "2026-11-13", "2026-11-15T16:00:00+00:00")
    failures = check_profile(profiles[0], drafts_root=repo_root, as_of=date(2026, 11, 15))
    assert any("source URL" in f for f in failures)
    result = run(profiles, drafts_root=repo_root, as_of=date(2026, 11, 15))
    assert result["status"] == "fail"
    assert exit_code(result) == EXIT_NOT_RELEASABLE


def test_unknown_placeholder_is_allowed_without_a_source(synthetic_profiles, repo_root):
    failures = check_profile(synthetic_profiles[0], drafts_root=repo_root, as_of=date(2026, 11, 15))
    assert failures == []
    assert synthetic_profiles[0]["education"]["label"] == "Unknown"
    assert synthetic_profiles[0]["education"]["value"] is None
    assert synthetic_profiles[0]["education"]["source_url"] is None


def test_set_aside_public_protector_finding_must_be_disputed() -> None:
    """CHG-PW-007 (Janus on PR #7): same label for every set-aside PP finding."""
    from pwatch.dq import check_set_aside_label

    item = {"category": "Public Protector finding (review)", "matter_status": "cleared", "label": "Reported"}
    assert check_set_aside_label(item, "x") and "Disputed" in check_set_aside_label(item, "x")[0]
    assert check_set_aside_label(dict(item, label="Disputed"), "x") == []
    assert check_set_aside_label(dict(item, matter_status="unknown"), "x") == []
    assert check_set_aside_label(dict(item, category="Criminal charge"), "x") == []


def test_committed_set_aside_pp_items_are_consistent() -> None:
    from pwatch.profiles import load_profile_dir
    from pwatch.schema import iter_adverse_items

    labels = {
        d["slug"]: it["label"]
        for _, d in load_profile_dir()
        for _, it in iter_adverse_items(d)
        if str(it.get("category", "")).startswith("Public Protector finding") and it.get("matter_status") == "cleared"
    }
    assert labels == {"herman-samtseu-philip-mashaba": "Disputed", "otta-helene-maree": "Disputed"}


# CHG-PW-011: rule 6 owner-approved exception for sources carrying private personal details.
PI_URL = "https://news.example.test/interview"


def _pi_profile():
    from pwatch.settings import PI_SOURCE_NOTE

    approved = {
        "value": "A degree",
        "label": "Reported",
        "source_url": PI_URL,
        "source_date": "2023-06-17",
        "retrieved_at": "2026-11-17",
        "note": PI_SOURCE_NOTE,
        "owner_approved_pi_source": "2026-11-19 16:27 SAST (CHG-PW-011)",
    }
    return {"education": dict(approved), "career": dict(approved, value="A job"), "cv": [], "court_matters": [], "scandals": []}


def test_pi_source_allowance_passes_when_approved_and_noted():
    from pwatch.dq import check_pi_source_allowance

    assert check_pi_source_allowance(_pi_profile(), "p") == []


def test_pi_source_note_without_approval_fails():
    from pwatch.dq import check_pi_source_allowance

    p = _pi_profile()
    for k in ("education", "career"):
        del p[k]["owner_approved_pi_source"]
    assert any("without owner_approved_pi_source" in f for f in check_pi_source_allowance(p, "p"))


def test_pi_source_approval_needs_exact_note_format_and_link():
    from pwatch.dq import check_pi_source_allowance

    p = _pi_profile()
    p["education"]["note"] = "contains personal details"
    p["career"]["owner_approved_pi_source"] = "yes"
    fails = check_pi_source_allowance(p, "p")
    assert any("needs the note" in f for f in fails) and any("must read" in f for f in fails)
    p = _pi_profile()
    p["education"].update(label="Unknown", value=None, source_url=None)
    assert any("http(s) source link" in f for f in check_pi_source_allowance(p, "p"))


def test_pi_source_reuse_without_approval_fails():
    from pwatch.dq import check_pi_source_allowance

    p = _pi_profile()
    p["cv"] = [{"value": "x", "label": "Reported", "source_url": PI_URL, "source_date": "2023-06-17", "retrieved_at": "2026-11-17"}]
    assert any("cv[0]: cites an owner-approved" in f for f in check_pi_source_allowance(p, "p"))


def test_pi_source_approval_not_allowed_on_adverse_items():
    from pwatch.dq import check_pi_source_allowance

    p = _pi_profile()
    p["court_matters"] = [dict(p["education"], value="a matter")]
    assert any("adverse item" in f for f in check_pi_source_allowance(p, "p"))


def test_magwentshu_restored_facts_carry_owner_approval(repo_root):
    import json

    from pwatch.settings import PI_SOURCE_NOTE

    d = json.loads((repo_root / "data/profiles/joburg-2026/lubabalo-cecil-magwentshu.json").read_text(encoding="utf-8"))
    facts = [d["education"], d["career"], d["cv"][0]]
    for f in facts:
        assert f["label"] == "Reported" and f["source_url"].startswith("https://www.citizen.co.za/")
        assert f["source_date"] == "2023-06-17" and f["note"] == PI_SOURCE_NOTE
        assert f["owner_approved_pi_source"] == "2026-11-19 16:27 SAST (CHG-PW-011)"
    assert len(d["identity_match"]["matched_details"]) >= 2
