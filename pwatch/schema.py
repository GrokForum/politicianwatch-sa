"""Profile fact helpers and structural checks (the JSON Schema is the contract)."""

from __future__ import annotations

from datetime import date, datetime, timedelta, timezone
from typing import Any
from urllib.parse import urlparse

from pwatch.settings import ADVERSE_FIELDS, CV_FIELDS, LABELS, OPTIONAL_FACT_FIELDS, SAST_OFFSET_HOURS, SEAT_TYPES

SAST = timezone(timedelta(hours=SAST_OFFSET_HOURS), "SAST")


def parse_retrieved_at(raw: Any) -> tuple[datetime | date | None, str | None]:
    """Parse a retrieved_at value (CHG-PW-003 fix 3).

    Two forms are allowed:
    - an ISO 8601 datetime with a UTC offset: the logged fetch time (returns a datetime);
    - a date only, YYYY-MM-DD: the fetch time was not logged, only the day (SAST) is known (returns a date).
    Returns (value, None) or (None, error message).
    """
    text = str(raw)
    if len(text) == 10:
        try:
            return date.fromisoformat(text), None
        except ValueError:
            return None, f"retrieved_at must be YYYY-MM-DD or an ISO 8601 datetime with a UTC offset, got {text!r}"
    try:
        ts = datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError:
        return None, f"retrieved_at must be YYYY-MM-DD or an ISO 8601 datetime with a UTC offset, got {text!r}"
    if ts.tzinfo is None:
        return None, f"retrieved_at needs a UTC offset, got {text!r}"
    return ts, None


def retrieved_at_is_future(raw: Any, now: datetime) -> bool:
    """True if retrieved_at is later than now. A date-only value counts as the end of that day (SAST),
    so it is future only if the date is after today's date in SAST."""
    value, err = parse_retrieved_at(raw)
    if err or value is None:
        return False
    if isinstance(value, datetime):
        return value > now
    return value > now.astimezone(SAST).date()

SCALAR_FACT_FIELDS = ("name", "party", "seat_type", "ward_number", "council", "positions", "education", "career")


def fact(
    value: Any,
    label: str,
    source_url: str | None = None,
    source_date: str | None = None,
    retrieved_at: str | None = None,
    source_page: int | None = None,
) -> dict[str, Any]:
    out: dict[str, Any] = {
        "value": value,
        "label": label,
        "source_url": source_url,
        "source_date": source_date,
        "retrieved_at": retrieved_at,
    }
    if source_page is not None:
        out["source_page"] = source_page
    return out


def unknown_fact() -> dict[str, Any]:
    return fact(None, "Unknown")


def is_fact(obj: Any) -> bool:
    return isinstance(obj, dict) and "label" in obj and "value" in obj


def _source_format_failures(src: dict[str, Any], locator: str) -> list[str]:
    """Format checks for an extra source: http(s) URL with a host, ISO date, ISO datetime with offset."""
    failures: list[str] = []
    url = urlparse(str(src.get("source_url")))
    if url.scheme not in ("http", "https") or not url.netloc or " " in str(src.get("source_url")):
        failures.append(f"{locator}: source_url is not a valid http(s) URL")
    raw_date = str(src.get("source_date"))
    try:
        if len(raw_date) != 10:
            raise ValueError
        date.fromisoformat(raw_date)
    except ValueError:
        failures.append(f"{locator}: source_date must be YYYY-MM-DD, got {raw_date!r}")
    _, err = parse_retrieved_at(src.get("retrieved_at"))
    if err:
        failures.append(f"{locator}: {err}")
    return failures


def fact_failures(obj: Any, locator: str) -> list[str]:
    """Fail if a fact is missing a label, or (when not Unknown) missing a source."""
    if not is_fact(obj):
        return [f"{locator}: not a fact object (needs value, label, source_url, source_date, retrieved_at)"]
    failures: list[str] = []
    label = obj.get("label")
    if label not in LABELS:
        failures.append(f"{locator}: missing or invalid label {label!r}")
        return failures
    if label == "Unknown":
        if obj.get("value") is not None:
            failures.append(f"{locator}: Unknown fact must have a null value")
        return failures
    if not obj.get("source_url"):
        failures.append(f"{locator}: fact labelled {label} is missing a source URL")
    if not obj.get("source_date"):
        failures.append(f"{locator}: fact labelled {label} is missing a source date")
    if not obj.get("retrieved_at"):
        failures.append(f"{locator}: fact labelled {label} is missing retrieved_at")
    else:
        _, err = parse_retrieved_at(obj.get("retrieved_at"))
        if err:
            failures.append(f"{locator}: {err}")
    extra = obj.get("also_sourced")
    if extra is not None:
        if not isinstance(extra, list):
            failures.append(f"{locator}.also_sourced: must be a list")
        else:
            for i, src in enumerate(extra):
                missing = False
                for key in ("source_url", "source_date", "retrieved_at"):
                    if not isinstance(src, dict) or not src.get(key):
                        failures.append(f"{locator}.also_sourced[{i}]: missing {key}")
                        missing = True
                if not missing:
                    failures.extend(_source_format_failures(src, f"{locator}.also_sourced[{i}]"))
    return failures


def iter_facts(profile: dict[str, Any]) -> list[tuple[str, dict[str, Any]]]:
    """Walk every fact in a profile, including items in adverse lists."""
    found: list[tuple[str, dict[str, Any]]] = []
    for key in SCALAR_FACT_FIELDS:
        if key in profile:
            found.append((key, profile[key]))
    for key in OPTIONAL_FACT_FIELDS:
        if key in profile:
            found.append((key, profile[key]))
    for i, item in enumerate(profile.get("cv") or []):
        found.append((f"cv[{i}]", item))
    for key in ADVERSE_FIELDS:
        items = profile.get(key) or []
        if isinstance(items, list):
            for i, item in enumerate(items):
                found.append((f"{key}[{i}]", item))
    return found


def iter_adverse_items(profile: dict[str, Any]) -> list[tuple[str, dict[str, Any]]]:
    found: list[tuple[str, dict[str, Any]]] = []
    for key in ADVERSE_FIELDS:
        items = profile.get(key) or []
        if isinstance(items, list):
            for i, item in enumerate(items):
                found.append((f"{key}[{i}]", item))
    return found


def validate_profile_shape(profile: dict[str, Any], locator: str = "profile") -> list[str]:
    failures: list[str] = []
    if not isinstance(profile, dict):
        return [f"{locator}: profile must be an object"]
    for key in SCALAR_FACT_FIELDS:
        if key not in profile:
            failures.append(f"{locator}: missing field {key}")
        else:
            failures.extend(fact_failures(profile[key], f"{locator}.{key}"))
    seat = profile.get("seat_type")
    if is_fact(seat) and seat.get("label") != "Unknown":
        if seat.get("value") not in SEAT_TYPES:
            failures.append(f"{locator}.seat_type: value must be one of {SEAT_TYPES}")
    for key in OPTIONAL_FACT_FIELDS:
        if key in profile:
            failures.extend(fact_failures(profile[key], f"{locator}.{key}"))
    cv = profile.get("cv")
    if cv is not None:
        if not isinstance(cv, list):
            failures.append(f"{locator}.cv: must be a list")
        else:
            for i, item in enumerate(cv):
                failures.extend(fact_failures(item, f"{locator}.cv[{i}]"))
                if isinstance(item, dict) and item.get("field") not in CV_FIELDS:
                    failures.append(f"{locator}.cv[{i}]: field must be one of {CV_FIELDS}")
    for key in ADVERSE_FIELDS:
        if key not in profile:
            failures.append(f"{locator}: missing field {key}")
            continue
        items = profile[key]
        if not isinstance(items, list):
            failures.append(f"{locator}.{key}: must be a list (empty if none recorded)")
            continue
        for i, item in enumerate(items):
            failures.extend(fact_failures(item, f"{locator}.{key}[{i}]"))
    return failures
