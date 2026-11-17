"""Source registry (CHG-PW-004): which tier a source URL belongs to.

The registry is data/sources.json (domain -> tier); the human-readable list is docs/allowed-sources.md.
A domain matches itself and its subdomains ("www." is ignored).

DQ rules built on it (see pwatch.dq):
- a source on a not_allowed or link_only domain fails;
- a domain not in the registry is a warning, not a failure.
"""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from pwatch.settings import DATA_DIR

REGISTRY_PATH = DATA_DIR / "sources.json"
TIERS = ("1", "2", "party", "link_only", "not_allowed")
FAIL_TIERS = ("link_only", "not_allowed")


@lru_cache(maxsize=4)
def load_registry(path: Path = REGISTRY_PATH) -> dict[str, str]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    out: dict[str, str] = {}
    for entry in data["sources"]:
        tier = str(entry["tier"])
        if tier not in TIERS:
            raise ValueError(f"{path}: unknown tier {tier!r} for {entry.get('domain')}")
        out[entry["domain"].lower().removeprefix("www.")] = tier
    return out


def host_of(url: str) -> str:
    host = (urlparse(str(url)).hostname or "").lower()
    return host.removeprefix("www.")


def tier_of(url: str, registry: dict[str, str] | None = None) -> str | None:
    """Tier for a URL, or None if its domain is not in the registry. The longest matching domain wins."""
    reg = load_registry() if registry is None else registry
    host = host_of(url)
    best: tuple[int, str] | None = None
    for domain, tier in reg.items():
        if host == domain or host.endswith("." + domain):
            if best is None or len(domain) > best[0]:
                best = (len(domain), tier)
    return best[1] if best else None


def source_urls(obj: Any) -> list[str]:
    """Every source_url at any depth (facts, also_sourced, adverse items)."""
    out: list[str] = []
    if isinstance(obj, dict):
        for key, val in obj.items():
            if key == "source_url" and isinstance(val, str) and val:
                out.append(val)
            else:
                out.extend(source_urls(val))
    elif isinstance(obj, list):
        for val in obj:
            out.extend(source_urls(val))
    return out
