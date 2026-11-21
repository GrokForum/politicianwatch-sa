"""CV-style profile documents (CHG-PW-002): load, roster cross-check, identity rule, markdown render.

Profiles live in data/profiles/joburg-2026/<slug>.json. Public role only. Every fact is labelled
and sourced. Unknown and Withheld (POPIA) fields stay null and render as visible placeholders (no source link). Adverse items render
"Right of reply: pending" with a blank reply field until the owner records otherwise.
"""

from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path
from typing import Any

from pwatch.ror import display
from pwatch.roster import row_to_profile
from pwatch.schema import iter_facts
from pwatch.settings import GAZETTE_PDF_URL, HOLD_DIRNAME, HOLD_STATUS, IDENTITY_MIN_DETAILS, PI_SOURCE_APPROVAL_FIELD, PROFILES_DIR, SOURCELESS_LABELS, WITHHELD_LABEL, WITHHELD_PUBLIC_TEXT

UNKNOWN_PLACEHOLDER = "Unknown — not yet sourced (placeholder)"
BLANK_REPLY = "_(blank — no reply recorded)_"

# Same placeholders as the CHG-PW-002/003 profiles, so the site wording stays uniform.
STUB_UNKNOWN_FIELDS = [
    "career",
    "education",
    "Council office or portfolio for the 2026–2031 term (executive mayor and mayoral committee not yet elected; first sitting expected around 19 November 2026 — not guessed)",
    "Official council contact channel (owner to confirm from the City's published councillor directory)",
]


def slug_from_gazetted_name(name: str) -> str:
    """Stable URL slug from a gazetted name: fold diacritics, drop apostrophes, hyphenate."""
    s = unicodedata.normalize("NFKD", name or "")
    s = "".join(c for c in s if not unicodedata.combining(c))
    for mark in ("'", "’", "‘", "`"):
        s = s.replace(mark, "")
    s = s.casefold()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


def stub_cv_profile(row: dict[str, Any], *, change: str = "CHG-PW-013") -> dict[str, Any]:
    """Build a gazette-only CV profile from a roster CSV row (Unknown placeholders, no adverse items)."""
    if isinstance((row.get("name") or None), dict):
        # Already a roster profile object.
        base = {k: v for k, v in row.items()}
        name = (base.get("name") or {}).get("value") or ""
    else:
        base = row_to_profile(row)
        name = (base.get("name") or {}).get("value") or row.get("name") or ""
    slug = slug_from_gazetted_name(str(name))
    if not slug:
        raise ValueError("cannot build a stub profile without a gazetted name")
    return {
        "slug": slug,
        "change": change,
        "name": base["name"],
        "party": base["party"],
        "seat_type": base["seat_type"],
        "ward_number": base["ward_number"],
        "council": base["council"],
        "ward_id": base.get("ward_id"),
        "pr_list_rank": base.get("pr_list_rank"),
        "positions": base.get("positions") or {"value": None, "label": "Unknown", "source_url": None, "source_date": None, "retrieved_at": None},
        "career": base.get("career") or {"value": None, "label": "Unknown", "source_url": None, "source_date": None, "retrieved_at": None},
        "education": base.get("education") or {"value": None, "label": "Unknown", "source_url": None, "source_date": None, "retrieved_at": None},
        "cv": [],
        "court_matters": list(base.get("court_matters") or []),
        "scandals": list(base.get("scandals") or []),
        "unknown_fields": list(STUB_UNKNOWN_FIELDS),
    }


def is_on_hold(profile: dict[str, Any]) -> bool:
    return isinstance(profile, dict) and profile.get("status") == HOLD_STATUS


def load_profile_dir(path: Path | None = None) -> list[tuple[Path, dict[str, Any]]]:
    """Active CV profiles only: top-level *.json, skipping any with status on_hold.

    Held profiles (in the _hold/ subdirectory, or marked on_hold) are not part of a batch,
    so dq does not count them and render does not write or check them.
    """
    root = path or PROFILES_DIR
    if not root.is_dir():
        return []
    out = []
    for p in sorted(root.glob("*.json")):
        doc = json.loads(p.read_text(encoding="utf-8"))
        if not is_on_hold(doc):
            out.append((p, doc))
    return out


def load_held_profiles(path: Path | None = None) -> list[tuple[Path, dict[str, Any]]]:
    """Profiles on hold: everything in <dir>/_hold/*.json plus any top-level file marked on_hold."""
    root = path or PROFILES_DIR
    if not root.is_dir():
        return []
    out = []
    for p in sorted(root.glob("*.json")):
        doc = json.loads(p.read_text(encoding="utf-8"))
        if is_on_hold(doc):
            out.append((p, doc))
    hold = root / HOLD_DIRNAME
    if hold.is_dir():
        for p in sorted(hold.glob("*.json")):
            out.append((p, json.loads(p.read_text(encoding="utf-8"))))
    return out


def roster_key(profile: dict[str, Any]) -> str | None:
    name = (profile.get("name") or {}).get("value")
    return str(name).strip().upper() if name else None


def roster_index(roster_profiles: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {k: p for p in roster_profiles if (k := roster_key(p))}


def check_against_roster(profile: dict[str, Any], index: dict[str, dict[str, Any]], locator: str) -> list[str]:
    """A profile must match one gazetted roster row on name, party, seat type, ward and PR rank."""
    key = roster_key(profile)
    row = index.get(key) if key else None
    if row is None:
        return [f"{locator}: name {key!r} is not in the gazetted roster"]
    failures = []
    for field in ("party", "seat_type", "ward_number", "council"):
        if (profile.get(field) or {}).get("value") != (row.get(field) or {}).get("value"):
            failures.append(f"{locator}.{field}: does not match the gazetted roster row")
    if profile.get("pr_list_rank") != row.get("pr_list_rank"):
        failures.append(f"{locator}.pr_list_rank: does not match the gazetted roster row")
    if profile.get("ward_id") != row.get("ward_id"):
        failures.append(f"{locator}.ward_id: does not match the gazetted roster row")
    return failures


def non_gazette_sources(profile: dict[str, Any]) -> set[str]:
    """Sources other than the seat source (the gazette URL that sources the name)."""
    seat_source = (profile.get("name") or {}).get("source_url") or GAZETTE_PDF_URL
    urls = set()
    for _, f in iter_facts(profile):
        if isinstance(f, dict) and f.get("label") != "Unknown" and f.get("source_url"):
            if f["source_url"] != seat_source:
                urls.add(f["source_url"])
    return urls


def check_identity(profile: dict[str, Any], locator: str) -> list[str]:
    """Linking any non-gazette source to a gazetted person needs at least two matching details."""
    if not non_gazette_sources(profile):
        return []
    im = profile.get("identity_match")
    details = im.get("matched_details") if isinstance(im, dict) else None
    if not isinstance(details, list) or len([d for d in details if str(d).strip()]) < IDENTITY_MIN_DETAILS:
        return [
            f"{locator}: non-gazette sources are linked but identity_match.matched_details has fewer than "
            f"{IDENTITY_MIN_DETAILS} details"
        ]
    return []


def _src(f: dict[str, Any]) -> str:
    if f.get("label") in SOURCELESS_LABELS:
        return ""
    page = f" p.{f['source_page']}" if f.get("source_page") else ""
    ret = f.get("retrieved_at")
    ret_txt = f"{ret}, time not logged" if isinstance(ret, str) and len(ret) == 10 else ret
    out = f" — [source]({f.get('source_url')}){page}, {f.get('source_date')} (retrieved {ret_txt})"
    for a in f.get("also_sourced") or []:
        out += f"; also [source]({a.get('source_url')}), {a.get('source_date')}"
    if f.get(PI_SOURCE_APPROVAL_FIELD) and f.get("note"):
        out += f" — {f['note']}"
    return out


def _fact_line(title: str, f: dict[str, Any]) -> str:
    if isinstance(f, dict) and f.get("label") == WITHHELD_LABEL:
        return f"- **{title}:** {WITHHELD_PUBLIC_TEXT} · `{WITHHELD_LABEL}`"
    if not isinstance(f, dict) or f.get("label") == "Unknown" or f.get("value") is None:
        if isinstance(f, dict) and f.get("label") != "Unknown" and f.get("value") is None:
            return f"- **{title}:** — (none) · `{f.get('label')}`{_src(f)}"
        return f"- **{title}:** {UNKNOWN_PLACEHOLDER} · `Unknown`"
    return f"- **{title}:** {f['value']} · `{f['label']}`{_src(f)}"


def render_markdown(profile: dict[str, Any]) -> str:
    name = profile["name"]["value"]
    lines = [
        f"<!-- Generated by `pwatch render` from {profile.get('slug', 'profile')}.json. Do not edit by hand. -->",
        f"# {name}",
        "",
        "DRAFT PROFILE — not published. Public role only. Every item carries an evidence label and a dated source.",
        "",
        "## Seat (Government Gazette 55741)",
        "",
        _fact_line("Name as gazetted", profile["name"]),
    ]
    if "known_as" in profile:
        lines.append(_fact_line("Known as", profile["known_as"]))
    if "given_names" in profile:
        lines.append(_fact_line("Given names", profile["given_names"]))
    if "full_name_surname" in profile:
        lines.append(_fact_line("Surname in full legal name", profile["full_name_surname"]))
    lines += [
        _fact_line("Party", profile["party"]),
        _fact_line("Seat type", profile["seat_type"]),
        _fact_line("Ward", profile["ward_number"]),
        f"- **PR list rank:** {profile.get('pr_list_rank') if profile.get('pr_list_rank') is not None else '—'}",
        _fact_line("Council", profile["council"]),
        "",
        "## Summary",
        "",
        _fact_line("Positions", profile["positions"]),
        _fact_line("Career", profile["career"]),
        _fact_line("Education", profile["education"]),
        "",
        "## CV (public role)",
        "",
    ]
    cv = profile.get("cv") or []
    if not cv:
        lines.append(f"- {UNKNOWN_PLACEHOLDER}")
    for item in cv:
        period = f" ({item['period']})" if item.get("period") else ""
        lines.append(_fact_line(f"{item.get('field', 'item').capitalize()}{period}", item))
    for key, title in (("court_matters", "Court matters"), ("scandals", "Scandals and allegations")):
        lines += ["", f"## {title}", ""]
        items = profile.get(key) or []
        if not items:
            lines.append("- None recorded in this change. (Absence here is not a finding.)")
        for item in items:
            shown = display(item.get("right_of_reply"))
            lines += [
                _fact_line("Item", item),
                f"  - **Status / outcome:** {item.get('outcome') or UNKNOWN_PLACEHOLDER} (matter_status: `{item.get('matter_status')}`)",
                f"  - **Identity link to the gazetted person:** {item.get('identity_link_label') or 'not recorded'}",
                f"  - **{shown['status_line']}**",
                f"  - **Reply:** {shown['reply_field'] or BLANK_REPLY}",
            ]
    unknown = profile.get("unknown_fields") or []
    if unknown:
        lines += ["", "## Not yet known (placeholders)", ""]
        lines += [f"- {u}: {UNKNOWN_PLACEHOLDER}" for u in unknown]
    im = profile.get("identity_match") or {}
    if im:
        lines += ["", "## Identity match (how sources were linked)", ""]
        lines += [f"- {d}" for d in im.get("matched_details", [])]
        if im.get("note"):
            lines.append(f"- Note: {im['note']}")
    lines.append("")
    return "\n".join(lines)
