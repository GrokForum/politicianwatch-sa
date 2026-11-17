"""Parse the IEC elected-councillor list from Government Gazette 55741 text.

The official PDF is a scanned, OCR-processed A4 gazette. This parser operates on
extracted text (pdftotext or pdfplumber), not on live HTTP. Tests use synthetic
fixtures only.

Each returned row includes the gazette page number so a fact can be cited precisely.
"""

from __future__ import annotations

import re
from collections.abc import Iterable

# Columns observed in Gazette 55741 (13 Nov 2026):
# Province | Municipality | Party | Ward ID or PR(rank) | Surname | Full names | Seat type
JHB_LINE = re.compile(
    r"Gauteng\s+JHB - City of Johannesburg\s+(.+?)\s+"
    r"(PR\((\d+)\)|79800(\d{3}))\s+(.+?)\s+"
    r"(MC\s+Ward|MC\s+PR)\s*$"
)


class ParseError(ValueError):
    """A gazette line could not be parsed."""


def parse_joburg_pages(pages: Iterable[tuple[int, str]]) -> list[dict]:
    """Parse (page_number, page_text) pairs and return Joburg councillor rows.

    `page_number` is the PDF page number (1-based), stored as source_page.
    """
    rows: list[dict] = []
    errors: list[str] = []
    for page_number, page_text in pages:
        for ln in page_text.splitlines():
            if "JHB" not in ln or "Johannesburg" not in ln:
                continue
            m = JHB_LINE.search(ln)
            if not m:
                errors.append(f"page {page_number}: unparsed: {ln.strip()[:200]}")
                continue
            party, _seat_tok, pr_rank, ward_digits, names_block, seat_type_raw = m.groups()
            parts = re.split(r"\s{2,}", names_block.strip())
            if len(parts) != 2:
                errors.append(f"page {page_number}: name split failed: {names_block!r}")
                continue
            surname, given = parts
            seat_type = "ward" if "Ward" in seat_type_raw else "PR"
            rows.append(
                {
                    "name": f"{given} {surname}".strip(),
                    "surname": surname.strip(),
                    "given_names": given.strip(),
                    "party": re.sub(r"\s+", " ", party).strip(),
                    "seat_type": seat_type,
                    "ward_number": int(ward_digits) if ward_digits else None,
                    "ward_id": f"79800{ward_digits}" if ward_digits else None,
                    "pr_list_rank": int(pr_rank) if pr_rank else None,
                    "council": "City of Johannesburg",
                    "source_page": int(page_number),
                }
            )
    if errors:
        raise ParseError(f"{len(errors)} unparsed Joburg line(s): " + "; ".join(errors[:5]))
    return rows


def parse_joburg_text(text: str, *, form_feed: bool = True) -> list[dict]:
    """Parse a full pdftotext dump. Pages are split on form feed when present."""
    if form_feed and "\f" in text:
        pages = [(i, p) for i, p in enumerate(text.split("\f"), 1) if p.strip()]
    else:
        pages = [(1, text)]
    return parse_joburg_pages(pages)
