"""Data-quality gate. Exit 2 means the output is not releasable.

Checks:
- every fact has a label
- every fact that is not Unknown has a dated source URL
- every adverse item (court/criminal matter, scandal, allegation) has a right_of_reply
  object, a draft, and owner-recorded fields that match its status
- no_response is only allowed after the deadline
- every right-of-reply draft starts with the DRAFT: NOT SENT marker (CHG-PW-002)
- every non-Unknown fact has retrieved_at (CHG-PW-002)
- a profile that links non-gazette sources records at least two matching identity details (CHG-PW-002)
- a CV profile matches its gazetted roster row (CHG-PW-002, when a roster index is given)
- source tiers (CHG-PW-004, data/sources.json): no link_only/not_allowed domains; an adverse item or an identity
  link may not rest only on tier-3 sources; unknown domains are warnings, not failures
- no retrieved_at anywhere in a profile (facts, also_sourced, adverse items) is later than the run time (CHG-PW-003 fix 2); a date-only value is future only if that date is after today's date in SAST (fix 3)
"""

from __future__ import annotations

from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

from pwatch.profiles import check_against_roster, check_identity, non_gazette_sources
from pwatch.ror import check_right_of_reply
from pwatch.schema import iter_adverse_items, retrieved_at_is_future, validate_profile_shape
from pwatch.settings import LABELS
from pwatch.sources import FAIL_TIERS, source_urls, tier_of

EXIT_OK = 0
EXIT_NOT_RELEASABLE = 2


def check_retrieved_not_future(obj: Any, locator: str, now: datetime) -> list[str]:
    """Every retrieved_at, at any depth (facts, also_sourced, adverse items), must not be later than now.

    A date-only value (fetch time not logged) is future only if that date is after today's date in SAST: it fails only if the
    date is after the run date. Malformed values are reported by the format checks, not here.
    """
    failures: list[str] = []
    if isinstance(obj, dict):
        for key, val in obj.items():
            here = f"{locator}.{key}"
            if key == "retrieved_at" and isinstance(val, str):
                if retrieved_at_is_future(val, now):
                    failures.append(
                        f"{here}: retrieved_at {val} is later than the run time {now.isoformat(timespec='seconds')}"
                    )
            else:
                failures.extend(check_retrieved_not_future(val, here, now))
    elif isinstance(obj, list):
        for i, val in enumerate(obj):
            failures.extend(check_retrieved_not_future(val, f"{locator}[{i}]", now))
    return failures


def check_source_tiers(profile: dict[str, Any], locator: str, registry: dict[str, str] | None = None) -> list[str]:
    """CHG-PW-004: source-tier rules (registry in data/sources.json).

    - A source on a link_only or not_allowed domain fails.
    - An adverse item whose sources (source_url + also_sourced) are all tier 3 fails.
    - A profile whose identity link rests only on tier-3 sources fails (the non-gazette sources,
      including also_sourced, are all tier 3).
    """
    failures: list[str] = []
    for url in sorted(set(source_urls(profile))):
        tier = tier_of(url, registry)
        if tier in FAIL_TIERS:
            failures.append(f"{locator}: source {url} is on a {tier} domain")
    for item_loc, item in iter_adverse_items(profile):
        urls = source_urls(item)
        if urls and all(tier_of(u, registry) == "3" for u in urls):
            failures.append(
                f"{locator}.{item_loc}: adverse item relies only on tier-3 sources; corroborate from tier 1 or 2"
            )
    linked = set(non_gazette_sources(profile))
    seat_source = (profile.get("name") or {}).get("source_url")
    linked |= {u for u in source_urls(profile) if u != seat_source}
    if linked and all(tier_of(u, registry) == "3" for u in linked):
        failures.append(f"{locator}: identity link relies only on tier-3 sources; corroborate from tier 1 or 2")
    return failures


def source_warnings(profile: dict[str, Any], locator: str, registry: dict[str, str] | None = None) -> list[str]:
    """Warnings (not failures): source domains that are not in the registry."""
    out = []
    for url in sorted(set(source_urls(profile))):
        if tier_of(url, registry) is None:
            out.append(f"{locator}: source domain not in data/sources.json: {url}")
    return out


def check_identity_link(item: Any, locator: str) -> list[str]:
    """An adverse item cannot be more certain than its link to the gazetted person."""
    if not isinstance(item, dict) or "identity_link_label" not in item:
        return []
    link = item.get("identity_link_label")
    if link not in LABELS:
        return [f"{locator}: invalid identity_link_label {link!r}"]
    if link != "Confirmed" and item.get("label") == "Confirmed":
        return [
            f"{locator}: item labelled Confirmed but its identity link to the gazetted person is {link}; "
            "label the item no higher than the link"
        ]
    return []


def check_profile(
    profile: dict[str, Any],
    *,
    drafts_root: Path | None = None,
    as_of: date | None = None,
    locator: str = "profile",
    roster: dict[str, Any] | None = None,
    now: datetime | None = None,
) -> list[str]:
    """Return DQ failure messages for one profile. Empty means pass."""
    as_of = as_of or date.today()
    now = now or datetime.now(timezone.utc)
    failures = validate_profile_shape(profile, locator)
    name = None
    name_fact = profile.get("name") if isinstance(profile, dict) else None
    if isinstance(name_fact, dict):
        name = name_fact.get("value")
    loc = f"{locator}({name})" if name else locator
    # Re-tag shape failures with the name when we have it
    if name and locator == "profile":
        failures = [f.replace(locator, loc, 1) if f.startswith(locator) else f for f in failures]
    if isinstance(profile, dict):
        failures.extend(check_retrieved_not_future(profile, loc, now))
        failures.extend(check_identity(profile, loc))
        failures.extend(check_source_tiers(profile, loc))
        if roster is not None:
            failures.extend(check_against_roster(profile, roster, loc))
    for item_loc, item in iter_adverse_items(profile if isinstance(profile, dict) else {}):
        failures.extend(check_identity_link(item, f"{loc}.{item_loc}"))
        failures.extend(
            check_right_of_reply(
                item.get("right_of_reply") if isinstance(item, dict) else None,
                drafts_root=drafts_root,
                as_of=as_of,
                locator=f"{loc}.{item_loc}",
            )
        )
    return failures


def run(
    profiles: list[dict[str, Any]],
    *,
    drafts_root: Path | None = None,
    as_of: date | None = None,
    roster: dict[str, Any] | None = None,
    locator_prefix: str = "profile",
    now: datetime | None = None,
) -> dict[str, Any]:
    """Run the gate on a list of profiles. status is pass or fail."""
    as_of = as_of or date.today()
    now = now or datetime.now(timezone.utc)
    all_failures: list[str] = []
    all_warnings: list[str] = []
    for i, profile in enumerate(profiles):
        if isinstance(profile, dict):
            all_warnings.extend(source_warnings(profile, f"{locator_prefix}[{i}]"))
        all_failures.extend(
            check_profile(
                profile,
                drafts_root=drafts_root,
                as_of=as_of,
                locator=f"{locator_prefix}[{i}]",
                roster=roster,
                now=now,
            )
        )
    status = "pass" if not all_failures else "fail"
    return {
        "status": status,
        "profiles": len(profiles),
        "failures": all_failures,
        "failure_count": len(all_failures),
        "warnings": all_warnings,
        "as_of": as_of.isoformat(),
    }


def exit_code(result: dict[str, Any]) -> int:
    return EXIT_OK if result.get("status") == "pass" else EXIT_NOT_RELEASABLE
