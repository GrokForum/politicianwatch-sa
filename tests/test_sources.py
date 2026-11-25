"""CHG-PW-004: source registry and tier rules, on synthetic fixtures (plus a registry sanity check)."""

import json
from copy import deepcopy
from datetime import date

from pwatch.dq import check_source_tiers, run
from pwatch.schema import fact
from pwatch.sources import REGISTRY_PATH, TIERS, load_registry, tier_of

REG = {"gazette.test": "1", "bignews.test": "2", "smallvoice.test": "3", "aggregator.test": "not_allowed", "esp.test": "link_only", "party.test": "party"}
GAZ = "https://gazette.test/55741.pdf"
T2 = "https://www.bignews.test/a"
T3 = "https://smallvoice.test/b"
T3B = "https://blog.smallvoice.test/c"  # subdomain matches its parent domain
RET = "2026-11-17"


def _profile(linked_urls, adverse_urls=None):
    p = {
        "name": fact("THABO TEST", "Confirmed", GAZ, "2026-11-13", RET),
        "cv": [{**fact("Former synthetic MMC", "Reported", u, "2026-09-06", RET), "field": "position"} for u in linked_urls],
        "court_matters": [],
        "scandals": [],
    }
    if adverse_urls is not None:
        item = fact("A synthetic allegation", "Alleged", adverse_urls[0], "2026-09-06", RET)
        item["also_sourced"] = [{"source_url": u, "source_date": "2026-09-06", "retrieved_at": RET} for u in adverse_urls[1:]]
        p["scandals"] = [item]
    return p


def test_tier_of_matches_domain_and_subdomains():
    assert tier_of(T2, REG) == "2"
    assert tier_of(T3B, REG) == "3"
    assert tier_of("https://notbignews.test/x", REG) is None  # suffix must be a whole label
    assert tier_of("https://unknown.example/x", REG) is None


def test_adverse_item_on_tier3_only_fails_and_passes_with_tier2_corroboration():
    only3 = _profile([T2], adverse_urls=[T3, T3B])
    fails = check_source_tiers(only3, "p", REG)
    assert any("adverse item relies only on tier-3 sources" in f for f in fails)
    corroborated = _profile([T2], adverse_urls=[T3, T2])
    assert check_source_tiers(corroborated, "p", REG) == []


def test_identity_link_on_tier3_only_fails():
    fails = check_source_tiers(_profile([T3]), "p", REG)
    assert any("identity link relies only on tier-3 sources" in f for f in fails)
    assert check_source_tiers(_profile([T3, T2]), "p", REG) == []
    assert check_source_tiers(_profile([]), "p", REG) == []  # gazette only: nothing linked


def test_not_allowed_and_link_only_domains_fail():
    fails = check_source_tiers(_profile([T2, "https://aggregator.test/c", "https://esp.test/w"]), "p", REG)
    assert any("not_allowed domain" in f for f in fails)
    assert any("link_only domain" in f for f in fails)


def test_unknown_domain_warns_but_does_not_fail(synthetic_profiles, repo_root):
    p = deepcopy(synthetic_profiles[0])
    p["cv"] = [{**fact("Synthetic role", "Reported", "https://unknown.example/x", "2026-09-06", RET), "field": "position"}]
    p["identity_match"] = {"matched_details": ["full name", "party and ward"], "note": None}
    result = run([p], drafts_root=repo_root, as_of=date(2026, 11, 15))
    assert any("not in data/sources.json: https://unknown.example/x" in w for w in result["warnings"])
    assert not any("unknown.example" in f for f in result["failures"])


def test_committed_registry_is_valid_and_covers_committed_profiles(repo_root):
    data = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    domains = [e["domain"] for e in data["sources"]]
    assert len(domains) == len(set(domains)), "duplicate domain in data/sources.json"
    assert all(str(e["tier"]) in TIERS and e.get("outlet") and e.get("verified") for e in data["sources"])
    reg = load_registry()
    assert tier_of("https://www.citizen.co.za/southern-courier/x", reg) == "2"
    assert tier_of("https://www.thecommonsense.co.za/x", reg) == "3"
    assert tier_of("https://thecapeindependent.com/x", reg) == "3"
    # Official sources added on the owner's decisions: five on 20 Nov 2026 (CHG-PW-013),
    # and dpsa.gov.za on 25 Nov 2026 (CHG-PW-016).
    for url, domain in (
        ("https://api.pmg.org.za/member/", "pmg.org.za"),
        ("https://static.pmg.org.za/55741_13-11_ElectoralComm_Final.pdf", "static.pmg.org.za"),
        ("https://municipaldata.treasury.gov.za/api/cubes/officials/facts", "municipaldata.treasury.gov.za"),
        ("https://www.parliament.gov.za/register-members-interests", "parliament.gov.za"),
        ("https://www.justice.gov.za/tribunal/index.html", "justice.gov.za"),
        ("https://www.thepresidency.gov.za/tso/siu-reports", "thepresidency.gov.za"),
        ("https://www.dpsa.gov.za/dpsa2g/documents/acts&regulations/Guide_for_members_of_the_executive/Guide%20for%20Members%20of%20the%20Executive%202022.pdf", "dpsa.gov.za"),
    ):
        assert tier_of(url, reg) == "1", domain
    # every source URL in the committed CV profiles is in the registry
    import re

    text = "".join(p.read_text(encoding="utf-8") for p in (repo_root / "data" / "profiles").rglob("*.json"))
    urls = set(re.findall(r'"source_url": "([^"]+)"', text))
    assert urls and all(tier_of(u, reg) is not None for u in urls), [u for u in urls if tier_of(u, reg) is None]


PARTY = "https://party.test/statement"
UNREG = "https://unregistered.example/x"


def test_adverse_tier3_with_party_statement_fails():
    fails = check_source_tiers(_profile([T2], adverse_urls=[T3, PARTY]), "p", REG)
    assert any("adverse item relies only on tier-3 sources" in f for f in fails)


def test_adverse_tier3_with_unregistered_domain_fails():
    fails = check_source_tiers(_profile([T2], adverse_urls=[UNREG, T3]), "p", REG)
    assert any("adverse item relies only on tier-3 sources" in f for f in fails)


def test_adverse_tier3_with_tier2_passes():
    assert check_source_tiers(_profile([T2], adverse_urls=[T3, PARTY, T2]), "p", REG) == []


def test_identity_tier3_with_party_statement_fails():
    fails = check_source_tiers(_profile([T3, PARTY]), "p", REG)
    assert any("identity link relies only on tier-3 sources" in f for f in fails)


def test_identity_tier3_with_unregistered_domain_fails():
    fails = check_source_tiers(_profile([UNREG, T3]), "p", REG)
    assert any("identity link relies only on tier-3 sources" in f for f in fails)


def test_identity_tier3_with_tier2_passes():
    assert check_source_tiers(_profile([T3, PARTY, T2]), "p", REG) == []


def test_party_and_unregistered_without_tier3_are_not_a_tier3_failure():
    fails = check_source_tiers(_profile([PARTY, UNREG], adverse_urls=[PARTY, UNREG]), "p", REG)
    assert not any("tier-3" in f for f in fails)
