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
