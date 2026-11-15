"""Right of reply (RoR) rules for adverse items.

The bot never sends a right-of-reply message. Drafts live in drafts/right-of-reply/
and are sent only by the owner, personally. Status changes only when the owner
records sending, a reply, or no_response after the deadline.
"""

from __future__ import annotations

from datetime import date, datetime
from pathlib import Path
from typing import Any

from pwatch.settings import DRAFT_MARKER, ROR_RECORDED_BY_OWNER, ROR_STATUSES

DISPLAY_PREFIX = "Right of reply: "


def default_pending(draft_path: str, deadline: str) -> dict[str, Any]:
    """Default RoR object for a new adverse item."""
    return {
        "status": "pending",
        "draft_path": draft_path,
        "deadline": deadline,
        "sent_at": None,
        "reply_text": None,
        "recorded_by": None,
    }


def display(ror: dict[str, Any] | None) -> dict[str, str]:
    """Visible profile wording: status line plus a reply field (blank until a reply exists)."""
    if not ror:
        return {"status_line": DISPLAY_PREFIX + "pending", "reply_field": ""}
    status = ror.get("status") or "pending"
    reply = ror.get("reply_text")
    return {
        "status_line": DISPLAY_PREFIX + str(status),
        "reply_field": "" if reply is None else str(reply),
    }


def first_nonempty_line(text: str) -> str:
    """The first line with content, stripped (used to check the NOT SENT marker opens the draft)."""
    for line in text.splitlines():
        if line.strip():
            return line.strip()
    return ""


def _parse_date(value: str | None) -> date | None:
    if not value:
        return None
    return date.fromisoformat(value[:10])


def check_right_of_reply(
    ror: Any,
    *,
    drafts_root: Path | None,
    as_of: date,
    locator: str,
) -> list[str]:
    """Return a list of DQ failure messages for one RoR object. Empty means pass."""
    failures: list[str] = []
    if not isinstance(ror, dict):
        return [f"{locator}: adverse item has no right_of_reply object"]
    status = ror.get("status")
    if status not in ROR_STATUSES:
        failures.append(f"{locator}: right_of_reply.status must be one of {ROR_STATUSES}, got {status!r}")
        return failures

    draft_path = ror.get("draft_path")
    if not draft_path or not str(draft_path).strip():
        failures.append(f"{locator}: adverse item has no draft (right_of_reply.draft_path is empty)")
    elif drafts_root is not None:
        path = Path(draft_path)
        if not path.is_absolute():
            path = drafts_root / path
        if not path.is_file():
            failures.append(f"{locator}: right_of_reply draft does not exist: {draft_path}")
        elif first_nonempty_line(path.read_text(encoding="utf-8")) != DRAFT_MARKER:
            failures.append(
                f"{locator}: right_of_reply draft must start with the marker {DRAFT_MARKER!r} "
                "(first non-empty line)"
            )

    deadline_invalid = False
    try:
        deadline = _parse_date(ror.get("deadline"))
    except ValueError:
        deadline = None
        deadline_invalid = True
        failures.append(f"{locator}: right_of_reply.deadline is not a date")
    # While pending and unsent, the owner sets the deadline on sending; a null deadline is allowed.
    if deadline is None and status != "pending" and not deadline_invalid:
        failures.append(f"{locator}: right_of_reply.deadline is required once status is {status!r}")

    sent_at = ror.get("sent_at")
    reply_text = ror.get("reply_text")
    recorded_by = ror.get("recorded_by")

    if status == "pending":
        if sent_at is not None:
            failures.append(f"{locator}: pending right_of_reply must have sent_at null")
        if reply_text is not None:
            failures.append(f"{locator}: pending right_of_reply must have a blank reply field (reply_text null)")
        return failures

    # Any status other than pending is recorded by the owner only.
    if recorded_by != ROR_RECORDED_BY_OWNER:
        failures.append(
            f"{locator}: right_of_reply.status {status!r} must be recorded_by="
            f"{ROR_RECORDED_BY_OWNER!r} (owner only); bot must not change this status"
        )

    if status == "sent":
        if not sent_at:
            failures.append(f"{locator}: status sent requires owner-recorded sent_at")
        if reply_text is not None:
            failures.append(f"{locator}: status sent must keep reply_text null until a reply is recorded")
    elif status == "replied":
        if not sent_at:
            failures.append(f"{locator}: status replied requires owner-recorded sent_at")
        if not reply_text:
            failures.append(f"{locator}: status replied requires owner-recorded reply_text")
    elif status == "no_response":
        if not sent_at:
            failures.append(f"{locator}: status no_response requires owner-recorded sent_at")
        if deadline is not None and as_of <= deadline:
            failures.append(
                f"{locator}: no_response is only allowed after the deadline "
                f"({deadline.isoformat()}; as_of={as_of.isoformat()})"
            )
        if reply_text is not None:
            failures.append(f"{locator}: status no_response must keep reply_text null")
    return failures
