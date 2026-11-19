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
  link may not rest only on tier-3 sources (CHG-PW-005); unknown domains are warnings, not failures
- no retrieved_at anywhere in a profile (facts, also_sourced, adverse items) is later than the run time (CHG-PW-003 fix 2); a date-only value is future only if that date is after today's date in SAST (fix 3)
"""

from __future__ import annotations

import re
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

from pwatch.profiles import check_against_roster, check_identity, non_gazette_sources
from pwatch.ror import check_right_of_reply
from pwatch.schema import iter_adverse_items, iter_facts, retrieved_at_is_future, validate_profile_shape
from pwatch.settings import LABELS, PI_SOURCE_APPROVAL_FIELD, PI_SOURCE_NOTE
from pwatch.sources import FAIL_TIERS, source_urls, tier_of

EXIT_OK = 0
EXIT_NOT_RELEASABLE = 2


def check_retrieved_not_future(obj: Any, locator: str, now: datetime) -> list[str]:
    """Every retrieved_at, at any depth (facts, also_sourced, adverse items), must not be later than now.

    A date-only value (fetch time not logged) fails only if that date is after today's date in SAST.
    Malformed values are reported by the format checks, not here.
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


def _tier3_uncorroborated(urls: Any, registry: dict[str, str] | None = None) -> bool:
    """True if the URLs include at least one tier-3 source and no tier-1 or tier-2 source.

    Party statements, unregistered domains and any other tiers do not count as corroboration.
    """
    tiers = {tier_of(u, registry) for u in urls}
    return "3" in tiers and not tiers & {"1", "2"}


def check_source_tiers(profile: dict[str, Any], locator: str, registry: dict[str, str] | None = None) -> list[str]:
    """CHG-PW-004: source-tier rules (registry in data/sources.json).

    - A source on a link_only or not_allowed domain fails.
    - CHG-PW-005: an adverse item that cites at least one tier-3 URL and no tier-1 or tier-2 URL fails
      (source_url + also_sourced), whatever party, unregistered or other URLs sit alongside it.
    - CHG-PW-005: the same for the identity link (every source other than the gazetted seat source,
      including also_sourced): a tier-3 URL with no tier-1 or tier-2 URL fails.
    """
    failures: list[str] = []
    for url in sorted(set(source_urls(profile))):
        tier = tier_of(url, registry)
        if tier in FAIL_TIERS:
            failures.append(f"{locator}: source {url} is on a {tier} domain")
    for item_loc, item in iter_adverse_items(profile):
        urls = source_urls(item)
        if _tier3_uncorroborated(urls, registry):
            failures.append(
                f"{locator}.{item_loc}: adverse item relies only on tier-3 sources; corroborate from tier 1 or 2"
            )
    linked = set(non_gazette_sources(profile))
    seat_source = (profile.get("name") or {}).get("source_url")
    linked |= {u for u in source_urls(profile) if u != seat_source}
    if _tier3_uncorroborated(linked, registry):
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


SET_ASIDE_CATEGORY_PREFIX = "Public Protector finding"
SET_ASIDE_LABEL = "Disputed"


def check_set_aside_label(item: Any, locator: str) -> list[str]:
    """A Public Protector finding that a court set aside (matter_status `cleared`) is labelled Disputed.

    CHG-PW-007 (Janus on PR #7): Zille and Mashaba carried different labels for the same kind of
    item. The label describes the finding's standing (challenged and set aside), so it is the same
    for every profile. Disputed is never higher than any identity link, so this cannot break that rule.
    """
    if not isinstance(item, dict):
        return []
    if str(item.get("category") or "").startswith(SET_ASIDE_CATEGORY_PREFIX) and item.get("matter_status") == "cleared":
        if item.get("label") != SET_ASIDE_LABEL:
            return [f"{locator}: a Public Protector finding set aside by a court must be labelled {SET_ASIDE_LABEL}, not {item.get('label')}"]
    return []


PI_SOURCE_APPROVAL_RE = re.compile(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2} SAST \(CHG-PW-\d{3}\)$")


def check_pi_source_allowance(profile: dict[str, Any], locator: str) -> list[str]:
    """Rule 6 and its narrow owner-approved exception (CHG-PW-007, amended by CHG-PW-011).

    Default: a source that carries private personal details is not linked, and a fact found only
    there is Unknown. A fact may link such a source only when it carries
    `owner_approved_pi_source` ("YYYY-MM-DD HH:MM SAST (CHG-PW-NNN)", the owner's decision and the
    change that applied it) and the note exactly `PI_SOURCE_NOTE`. The note is never used without
    the approval, an approved fact is never Unknown, and every fact citing an approved URL in the
    same profile carries the approval too (no silent reuse). Adverse items may not use it.
    """
    failures: list[str] = []
    approved_urls: set[str] = set()
    facts = [(k, f) for k, f in iter_facts(profile) if isinstance(f, dict)]
    adverse = {k for k, _ in iter_adverse_items(profile)}
    for key, f in facts:
        approval = f.get(PI_SOURCE_APPROVAL_FIELD)
        where = f"{locator}.{key}"
        if approval is None:
            if f.get("note") == PI_SOURCE_NOTE:
                failures.append(f"{where}: the personal-details note is set without {PI_SOURCE_APPROVAL_FIELD}")
            continue
        if key in adverse:
            failures.append(f"{where}: {PI_SOURCE_APPROVAL_FIELD} is not allowed on an adverse item")
        if not isinstance(approval, str) or not PI_SOURCE_APPROVAL_RE.match(approval):
            failures.append(f"{where}: {PI_SOURCE_APPROVAL_FIELD} must read 'YYYY-MM-DD HH:MM SAST (CHG-PW-NNN)'")
        if f.get("label") == "Unknown" or not str(f.get("source_url") or "").startswith(("http://", "https://")):
            failures.append(f"{where}: {PI_SOURCE_APPROVAL_FIELD} needs a labelled fact with an http(s) source link")
        if f.get("note") != PI_SOURCE_NOTE:
            failures.append(f"{where}: {PI_SOURCE_APPROVAL_FIELD} needs the note {PI_SOURCE_NOTE!r}")
        if f.get("source_url"):
            approved_urls.add(f["source_url"])
    for key, f in facts:
        if f.get("source_url") in approved_urls and f.get(PI_SOURCE_APPROVAL_FIELD) is None and f.get("label") != "Unknown":
            failures.append(f"{locator}.{key}: cites an owner-approved personal-details source without {PI_SOURCE_APPROVAL_FIELD}")
    return failures


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
        failures.extend(check_pi_source_allowance(profile, loc))
        if roster is not None:
            failures.extend(check_against_roster(profile, roster, loc))
    for item_loc, item in iter_adverse_items(profile if isinstance(profile, dict) else {}):
        failures.extend(check_identity_link(item, f"{loc}.{item_loc}"))
        failures.extend(check_set_aside_label(item, f"{loc}.{item_loc}"))
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
