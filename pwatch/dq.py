"""Data-quality gate. Exit 2 means the output is not releasable.

Checks:
- every fact has a label
- every fact that is not Unknown has a dated source URL
- every adverse item (court/criminal matter, scandal, allegation) has a right_of_reply
  object, a draft, and owner-recorded fields that match its status
- no_response is only allowed after the deadline
"""

from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Any

from pwatch.ror import check_right_of_reply
from pwatch.schema import iter_adverse_items, validate_profile_shape

EXIT_OK = 0
EXIT_NOT_RELEASABLE = 2


def check_profile(
    profile: dict[str, Any],
    *,
    drafts_root: Path | None = None,
    as_of: date | None = None,
    locator: str = "profile",
) -> list[str]:
    """Return DQ failure messages for one profile. Empty means pass."""
    as_of = as_of or date.today()
    failures = validate_profile_shape(profile, locator)
    name = None
    name_fact = profile.get("name") if isinstance(profile, dict) else None
    if isinstance(name_fact, dict):
        name = name_fact.get("value")
    loc = f"{locator}({name})" if name else locator
    # Re-tag shape failures with the name when we have it
    if name and locator == "profile":
        failures = [f.replace(locator, loc, 1) if f.startswith(locator) else f for f in failures]
    for item_loc, item in iter_adverse_items(profile if isinstance(profile, dict) else {}):
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
) -> dict[str, Any]:
    """Run the gate on a list of profiles. status is pass or fail."""
    as_of = as_of or date.today()
    all_failures: list[str] = []
    for i, profile in enumerate(profiles):
        all_failures.extend(
            check_profile(profile, drafts_root=drafts_root, as_of=as_of, locator=f"profile[{i}]")
        )
    status = "pass" if not all_failures else "fail"
    return {
        "status": status,
        "profiles": len(profiles),
        "failures": all_failures,
        "failure_count": len(all_failures),
        "as_of": as_of.isoformat(),
    }


def exit_code(result: dict[str, Any]) -> int:
    return EXIT_OK if result.get("status") == "pass" else EXIT_NOT_RELEASABLE
