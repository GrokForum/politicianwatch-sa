"""Right-of-reply tests on synthetic adverse fixtures."""

from copy import deepcopy
from datetime import date

from pwatch.dq import check_profile, run
from pwatch.ror import display
from pwatch.schema import fact


AS_OF = date(2026, 11, 15)
DEADLINE = "2026-12-15"


def _adverse(profile):
    return profile["scandals"][0]


def test_pending_displays_status_and_blank_reply_field(synthetic_profiles):
    ror = _adverse(synthetic_profiles[2])["right_of_reply"]
    shown = display(ror)
    assert shown["status_line"] == "Right of reply: pending"
    assert shown["reply_field"] == ""


def test_adverse_item_without_right_of_reply_fails(synthetic_profiles, repo_root):
    profiles = deepcopy(synthetic_profiles)
    _adverse(profiles[2]).pop("right_of_reply")
    failures = check_profile(profiles[2], drafts_root=repo_root, as_of=AS_OF)
    assert any("no right_of_reply" in f for f in failures)


def test_adverse_item_without_a_draft_fails(synthetic_profiles, repo_root):
    profiles = deepcopy(synthetic_profiles)
    _adverse(profiles[2])["right_of_reply"]["draft_path"] = ""
    failures = check_profile(profiles[2], drafts_root=repo_root, as_of=AS_OF)
    assert any("no draft" in f for f in failures)


def test_missing_draft_file_fails(synthetic_profiles, repo_root):
    profiles = deepcopy(synthetic_profiles)
    _adverse(profiles[2])["right_of_reply"]["draft_path"] = "drafts/right-of-reply/DOES-NOT-EXIST.md"
    failures = check_profile(profiles[2], drafts_root=repo_root, as_of=AS_OF)
    assert any("does not exist" in f for f in failures)


def test_sent_without_sent_at_fails(synthetic_profiles, repo_root):
    profiles = deepcopy(synthetic_profiles)
    ror = _adverse(profiles[2])["right_of_reply"]
    ror["status"] = "sent"
    ror["sent_at"] = None
    ror["recorded_by"] = "owner"
    failures = check_profile(profiles[2], drafts_root=repo_root, as_of=AS_OF)
    assert any("sent_at" in f for f in failures)


def test_sent_recorded_by_owner_passes(synthetic_profiles, repo_root):
    profiles = deepcopy(synthetic_profiles)
    ror = _adverse(profiles[2])["right_of_reply"]
    ror["status"] = "sent"
    ror["sent_at"] = "2026-11-16T08:00:00+02:00"
    ror["recorded_by"] = "owner"
    ror["reply_text"] = None
    failures = check_profile(profiles[2], drafts_root=repo_root, as_of=date(2026, 11, 16))
    assert failures == []
    assert display(ror)["status_line"] == "Right of reply: sent"
    assert display(ror)["reply_field"] == ""


def test_replied_requires_reply_text(synthetic_profiles, repo_root):
    profiles = deepcopy(synthetic_profiles)
    ror = _adverse(profiles[2])["right_of_reply"]
    ror["status"] = "replied"
    ror["sent_at"] = "2026-11-16T08:00:00+02:00"
    ror["recorded_by"] = "owner"
    ror["reply_text"] = None
    failures = check_profile(profiles[2], drafts_root=repo_root, as_of=date(2026, 11, 20))
    assert any("reply_text" in f for f in failures)
    ror["reply_text"] = "I deny the allegation."
    failures = check_profile(profiles[2], drafts_root=repo_root, as_of=date(2026, 11, 20))
    assert failures == []
    assert display(ror)["reply_field"] == "I deny the allegation."


def test_no_response_before_deadline_fails(synthetic_profiles, repo_root):
    profiles = deepcopy(synthetic_profiles)
    ror = _adverse(profiles[2])["right_of_reply"]
    ror["status"] = "no_response"
    ror["sent_at"] = "2026-11-16T08:00:00+02:00"
    ror["recorded_by"] = "owner"
    ror["reply_text"] = None
    failures = check_profile(profiles[2], drafts_root=repo_root, as_of=date(2026, 12, 15))
    assert any("only allowed after the deadline" in f for f in failures)
    result = run(profiles, drafts_root=repo_root, as_of=date(2026, 12, 15))
    assert result["status"] == "fail"


def test_no_response_after_deadline_passes(synthetic_profiles, repo_root):
    profiles = deepcopy(synthetic_profiles)
    ror = _adverse(profiles[2])["right_of_reply"]
    ror["status"] = "no_response"
    ror["sent_at"] = "2026-11-16T08:00:00+02:00"
    ror["recorded_by"] = "owner"
    ror["reply_text"] = None
    failures = check_profile(profiles[2], drafts_root=repo_root, as_of=date(2026, 12, 16))
    assert failures == []


def test_bot_cannot_record_status_change(synthetic_profiles, repo_root):
    profiles = deepcopy(synthetic_profiles)
    ror = _adverse(profiles[2])["right_of_reply"]
    ror["status"] = "sent"
    ror["sent_at"] = "2026-11-16T08:00:00+02:00"
    ror["recorded_by"] = "bot"
    failures = check_profile(profiles[2], drafts_root=repo_root, as_of=date(2026, 11, 16))
    assert any("owner only" in f for f in failures)
