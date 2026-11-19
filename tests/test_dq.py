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
