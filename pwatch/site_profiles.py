"""Profile pages for the draft site (CHG-PW-007).

Renders the active CV profiles (never `_hold/`) as static HTML. Every claim is an
`<li class="claim" data-fact=... data-label=...>` that shows its evidence label and, unless it is
Unknown or Withheld (POPIA), links to its source with a `<time datetime>` source date. Adverse items also show the
right-of-reply line ("Right of reply: pending" until the owner records otherwise) and a blank reply
field. `check_claims` re-parses built pages and fails any claim that lacks a label, a source link
or a date (except Unknown and Withheld (POPIA)); `check_coverage` fails if a profile, or any fact in it, is missing from the build, or if
a held profile was built.
"""

from __future__ import annotations

import re
from html import escape
from html.parser import HTMLParser
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from pwatch.ror import display
from pwatch.schema import iter_facts
from pwatch.settings import GAZETTE_DATE, GAZETTE_NUMBER, LABELS, PI_SOURCE_APPROVAL_FIELD, SOURCELESS_LABELS, WITHHELD_LABEL, WITHHELD_PUBLIC_TEXT

UNKNOWN_TEXT = "Unknown — not yet found in an allowed source"
BLANK_REPLY = "(blank — no reply recorded)"
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def profile_path(slug: str) -> str:
    return f"profiles/{slug}/index.html"


def _safe_url(url: Any) -> str | None:
    if not isinstance(url, str):
        return None
    u = urlparse(url)
    return url if u.scheme in ("http", "https") and u.netloc else None


def _source_html(f: dict[str, Any]) -> str:
    """Source link(s) with dates. Empty for Unknown facts."""
    if f.get("label") in SOURCELESS_LABELS:
        return ""
    parts = []
    url = _safe_url(f.get("source_url"))
    host = urlparse(url).netloc.removeprefix("www.") if url else "source missing"
    page = f", p.{escape(str(f['source_page']))}" if f.get("source_page") else ""
    date = f.get("source_date")
    date_html = f'<time datetime="{escape(str(date))}">{escape(str(date))}</time>' if date else "date missing"
    link = f'<a class="src-link" href="{escape(url)}" rel="noopener noreferrer">{escape(host)}</a>' if url else host
    ret = f.get("retrieved_at")
    ret_txt = ""
    if isinstance(ret, str) and ret:
        ret_txt = f"; retrieved {escape(ret[:10])}" + (", time not logged" if len(ret) == 10 else "")
    parts.append(f"{link}{page}, {date_html}{ret_txt}")
    for a in f.get("also_sourced") or []:
        aurl = _safe_url(a.get("source_url"))
        ahost = urlparse(aurl).netloc.removeprefix("www.") if aurl else "source missing"
        ad = a.get("source_date")
        ad_html = f'<time datetime="{escape(str(ad))}">{escape(str(ad))}</time>' if ad else "date missing"
        alink = f'<a class="src-link" href="{escape(aurl)}" rel="noopener noreferrer">{escape(ahost)}</a>' if aurl else ahost
        parts.append(f"also {alink}, {ad_html}")
    note = ""
    if f.get(PI_SOURCE_APPROVAL_FIELD) and f.get("note"):
        note = f' <span class="src-note">{escape(str(f["note"]))}</span>'
    return '<span class="src">Source: ' + "; ".join(parts) + "</span>" + note


def _label_class(label: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9]+", "-", label).strip("-")
    return f"label label-{escape(slug)}"


def _label_html(label: str) -> str:
    return f'<span class="{_label_class(label)}">{escape(label)}</span>'


def claim(fact_id: str, title: str, f: dict[str, Any], extra: str = "", css: str = "") -> str:
    label = str(f.get("label")) if isinstance(f, dict) else "Unknown"
    if label == WITHHELD_LABEL and isinstance(f, dict):
        body = f"<strong>{escape(title)}:</strong> {escape(WITHHELD_PUBLIC_TEXT)}"
    elif label == "Unknown" or not isinstance(f, dict):
        body = f"<strong>{escape(title)}:</strong> {UNKNOWN_TEXT}"
        label = "Unknown"
    elif f.get("value") is None:
        body = f"<strong>{escape(title)}:</strong> — (none)"
    else:
        body = f"<strong>{escape(title)}:</strong> {escape(str(f['value']))}"
    cls = "claim" + (f" {css}" if css else "")
    src = _source_html(f) if isinstance(f, dict) else ""
    return (
        f'<li class="{cls}" data-fact="{escape(fact_id)}" data-label="{escape(label)}">'
        f"{_label_html(label)}{body}<br>{src}{extra}</li>"
    )


def _seat_text(p: dict[str, Any]) -> str:
    seat = (p.get("seat_type") or {}).get("value")
    if seat == "ward":
        return f"Ward {(p.get('ward_number') or {}).get('value')}"
    rank = p.get("pr_list_rank")
    return f"PR list (rank {rank})" if rank is not None else "PR list"


def profile_body(p: dict[str, Any]) -> str:
    name = p["name"]["value"]
    seat_src = p["name"]
    out = [
        f"<h1>{escape(name)}</h1>",
        '<p class="note">Draft profile. Public role only. Every item shows an evidence label; every item except an Unknown or Withheld (POPIA) one links a dated source. '
        'To ask for a correction or to send a reply, see <a href="/privacy/#corrections">Privacy and corrections</a>.</p>',
        '<p><a href="/">All profiles</a></p>',
        f"<h2>Seat (Government Gazette {GAZETTE_NUMBER})</h2>",
        '<ul class="claims">',
        claim("name", "Name as gazetted", p["name"]),
    ]
    for key, title in (("known_as", "Known as"), ("given_names", "Given names"), ("full_name_surname", "Surname in full legal name")):
        if key in p:
            out.append(claim(key, title, p[key]))
    rank = p.get("pr_list_rank")
    rank_fact = dict(seat_src, value=rank if rank is not None else None)
    out += [
        claim("party", "Party", p["party"]),
        claim("seat_type", "Seat type", p["seat_type"]),
        claim("ward_number", "Ward", p["ward_number"]),
        claim("pr_list_rank", "PR list rank", rank_fact),
        claim("council", "Council", p["council"]),
        "</ul>",
        "<h2>Summary</h2>",
        '<ul class="claims">',
        claim("positions", "Positions", p["positions"]),
        claim("career", "Career", p["career"]),
        claim("education", "Education", p["education"]),
        "</ul>",
        "<h2>CV (public role)</h2>",
        '<ul class="claims">',
    ]
    cv = p.get("cv") or []
    if not cv:
        out.append(f'<li class="note">{UNKNOWN_TEXT}</li>')
    for i, item in enumerate(cv):
        period = f" ({item['period']})" if item.get("period") else ""
        out.append(claim(f"cv[{i}]", f"{str(item.get('field', 'item')).capitalize()}{period}", item))
    out.append("</ul>")
    for key, title in (("court_matters", "Court matters"), ("scandals", "Scandals and allegations")):
        out += [f"<h2>{title}</h2>", '<ul class="claims">']
        items = p.get(key) or []
        if not items:
            out.append('<li class="note">None recorded. (Absence here is not a finding.)</li>')
        for i, item in enumerate(items):
            shown = display(item.get("right_of_reply"))
            status = str((item.get("right_of_reply") or {}).get("status") or "pending")
            extra = (
                '<ul class="sub">'
                f"<li><strong>Status / outcome:</strong> {escape(str(item.get('outcome') or UNKNOWN_TEXT))}</li>"
                f"<li><strong>Identity link to the gazetted person:</strong> {escape(str(item.get('identity_link_label') or 'not recorded'))}</li>"
                f'<li class="ror" data-ror="{escape(status)}">{escape(shown["status_line"])}</li>'
                f"<li><strong>Reply:</strong> {escape(shown['reply_field']) or BLANK_REPLY}</li>"
                "</ul>"
            )
            out.append(claim(f"{key}[{i}]", "Item", item, extra=extra, css="adverse"))
        out.append("</ul>")
    unknown = p.get("unknown_fields") or []
    if unknown:
        out += ["<h2>Not yet known</h2>", '<ul class="claims">']
        out += [claim(f"unknown[{i}]", str(u), {"label": "Unknown", "value": None}) for i, u in enumerate(unknown)]
        out.append("</ul>")
    im = p.get("identity_match") or {}
    if im:
        out += [
            "<h2>Method note: how sources were linked to this person</h2>",
            '<p class="note">A source is linked to a gazetted person only when at least two details match. '
            "These notes explain the match; the sourced items above carry the evidence.</p>",
            '<ul class="note">',
        ]
        out += [f"<li>{escape(str(d))}</li>" for d in im.get("matched_details", [])]
        if im.get("note"):
            out.append(f"<li>Note: {escape(str(im['note']))}</li>")
        out.append("</ul>")
    return "\n".join(out)


def index_body(profiles: list[tuple[Path, dict[str, Any]]], site_name: str) -> str:
    rows = []
    for _, p in sorted(profiles, key=lambda t: t[1]["name"]["value"]):
        seat = p["name"]
        src = _safe_url(seat.get("source_url"))
        page = f", p.{escape(str(seat['source_page']))}" if seat.get("source_page") else ""
        rows.append(
            f'<tr class="claim" data-fact="index:{escape(p["slug"])}" data-label="{escape(str(seat.get("label")))}">'
            f'<td><a href="/profiles/{escape(p["slug"])}/">{escape(p["name"]["value"])}</a></td>'
            f"<td>{escape(str((p.get('party') or {}).get('value')))}</td>"
            f"<td>{escape(_seat_text(p))}</td>"
            f"<td>{_label_html(str(seat.get('label')))}"
            f'<a class="src-link" href="{escape(src or "")}" rel="noopener noreferrer">Gazette {GAZETTE_NUMBER}</a>{page}, '
            f'<time datetime="{escape(str(seat.get("source_date")))}">{escape(str(seat.get("source_date")))}</time></td></tr>'
        )
    return "\n".join(
        [
            f"<h1>{site_name}</h1>",
            "<p>Neutral, sourced public profiles of South Africa's elected representatives, starting with the "
            "City of Johannesburg councillors elected on 4 November 2026. Public role only.</p>",
            f"<p><strong>{len(profiles)} draft profiles.</strong> Seats are as published in Government Gazette "
            f"{GAZETTE_NUMBER} ({GAZETTE_DATE}). Council offices for the 2026–2031 term are shown as Unknown until "
            "they are published. Each profile item shows an evidence label (Confirmed, Reported, Alleged, Disputed or "
            "Unknown or Withheld (POPIA)); every item except an Unknown or Withheld (POPIA) one links to its source with a date.</p>",
            '<table><thead><tr><th scope="col">Name as gazetted</th><th scope="col">Party</th>'
            '<th scope="col">Seat</th><th scope="col">Seat source</th></tr></thead><tbody>',
            *rows,
            "</tbody></table>",
        ]
    )


def expected_fact_ids(p: dict[str, Any]) -> set[str]:
    ids = {loc for loc, _ in iter_facts(p)}
    ids.add("pr_list_rank")
    ids |= {f"unknown[{i}]" for i in range(len(p.get("unknown_fields") or []))}
    return ids


class _ClaimScan(HTMLParser):
    """Collect every element with class "claim": label, source links, dates, text, RoR line."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.claims: list[dict[str, Any]] = []
        self._stack: list[tuple[str, dict[str, Any] | None]] = []
        self._cur: list[dict[str, Any]] = []
        self._in_label = 0
        self._ror_depth: int | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        a = {k: (v or "") for k, v in attrs}
        if tag in ("br", "meta", "link", "img", "input", "hr"):
            return
        rec = None
        classes = a.get("class", "").split()
        if "claim" in classes:
            rec = {
                "fact": a.get("data-fact", ""),
                "label": a.get("data-label", ""),
                "adverse": "adverse" in classes,
                "badge": [],
                "links": [],
                "dates": [],
                "ror": [],
                "text": [],
            }
            self.claims.append(rec)
            self._cur.append(rec)
        self._stack.append((tag, rec))
        if self._cur:
            c = self._cur[-1]
            if tag == "span" and any(x.startswith("label") for x in classes):
                self._in_label = len(self._stack)
            if tag == "a" and "src-link" in classes:
                c["links"].append(a.get("href", ""))
            if tag == "time":
                c["dates"].append(a.get("datetime", ""))
            if "ror" in classes:
                c["ror"].append(a.get("data-ror", ""))
                self._ror_depth = len(self._stack)

    def handle_endtag(self, tag: str) -> None:
        while self._stack:
            t, rec = self._stack.pop()
            if self._in_label and len(self._stack) < self._in_label:
                self._in_label = 0
            if self._ror_depth and len(self._stack) < self._ror_depth:
                self._ror_depth = None
            if rec is not None and self._cur and self._cur[-1] is rec:
                self._cur.pop()
            if t == tag:
                break

    def handle_data(self, data: str) -> None:
        if not self._cur:
            return
        c = self._cur[-1]
        c["text"].append(data)
        if self._in_label:
            c["badge"].append(data.strip())
        if self._ror_depth:
            c.setdefault("ror_text", []).append(data)


def scan_claims(html: str) -> list[dict[str, Any]]:
    s = _ClaimScan()
    s.feed(html)
    s.close()
    return s.claims


def check_claims(rel: str, html: str) -> list[str]:
    """Every rendered claim shows a valid label; non-Unknown, non-withheld claims link a source with a date."""
    fails = []
    for c in scan_claims(html):
        where = f"{rel} [{c['fact'] or 'claim'}]"
        if c["label"] not in LABELS:
            fails.append(f"{where}: label {c['label']!r} is not one of {', '.join(LABELS)}")
            continue
        if c["label"] not in c["badge"]:
            fails.append(f"{where}: the {c['label']} label is not shown on the page")
        if c["label"] == "Unknown":
            continue
        if c["label"] == WITHHELD_LABEL:
            if any(_safe_url(h) for h in c["links"]):
                fails.append(f"{where}: {WITHHELD_LABEL} claim must not have a source link")
            text = "".join(c.get("text") or [])
            if WITHHELD_PUBLIC_TEXT not in text:
                fails.append(f"{where}: {WITHHELD_LABEL} claim does not show the withheld wording")
            continue
        if not any(_safe_url(h) for h in c["links"]):
            fails.append(f"{where}: claim has no http(s) source link")
        if not any(DATE_RE.match(d or "") for d in c["dates"]):
            fails.append(f"{where}: claim has no source date")
        if c["adverse"]:
            text = "".join(c.get("ror_text", [])).strip()
            status = (c["ror"] or [""])[0]
            if not text.startswith("Right of reply: "):
                fails.append(f"{where}: adverse item has no 'Right of reply' line")
            elif status == "pending" and text != "Right of reply: pending":
                fails.append(f"{where}: pending adverse item does not show 'Right of reply: pending'")
    return fails


def check_coverage(out: Path, profiles: list[tuple[Path, dict[str, Any]]], held: list[tuple[Path, dict[str, Any]]]) -> list[str]:
    """Every active profile and every fact in it is on the site; no held profile is."""
    fails = []
    built = {p.parent.name for p in (out / "profiles").glob("*/index.html")} if (out / "profiles").is_dir() else set()
    active = {d["slug"] for _, d in profiles}
    for slug in sorted(active - built):
        fails.append(f"profile {slug} has no page")
    for slug in sorted(built - active):
        fails.append(f"page profiles/{slug}/ has no active profile behind it")
    for _, d in held:
        slug = d.get("slug")
        if slug and (out / "profiles" / slug).exists():
            fails.append(f"held profile {slug} must not be on the site")
    for _, d in profiles:
        page = out / profile_path(d["slug"])
        if not page.is_file():
            continue
        rendered = {c["fact"] for c in scan_claims(page.read_text(encoding="utf-8"))}
        for missing in sorted(expected_fact_ids(d) - rendered):
            fails.append(f"profiles/{d['slug']}: fact {missing} is not rendered")
    index = out / "index.html"
    if index.is_file():
        listed = {c["fact"].removeprefix("index:") for c in scan_claims(index.read_text(encoding="utf-8"))}
        for slug in sorted(active - listed):
            fails.append(f"index.html does not list {slug}")
    return fails
