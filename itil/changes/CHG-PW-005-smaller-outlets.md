# CHG-PW-005 — Smaller and independent outlets (tier 3, "separate pen")

| Field | Value |
|---|---|
| Requested by / date (SAST) | Owner, 17 November 2026, in chat ("yes sorry my bad, original spec was mainstream, additional is new rfc") |
| Author / builder | PoliticianWatch (Grok Bot) |
| Reviewers | Cavus; Cassian |
| Change authority | Owner (GO on the exact head) |
| Type | Normal — low (source policy, registry entries, one DQ rule with tests; no profile data changes) |
| Environment | DEV (docs, code, synthetic tests). Not PROD. |
| CIs affected | CI-004 DQ gate; source policy (`docs/allowed-sources.md`, `data/sources.json`) |
| Linked records | CHG-PW-004 (mainstream tiers 1 and 2, registry) |
| Branch | `dev/chg-pw-005-smaller-outlets`, made locally on 17 Nov 2026 from the CHG-PW-004 head `d4b01cec7754ad553d580dc9677b44e8e88b0c3d`. Merge order: CHG-PW-004, then this change. |
| Pre-change commit (rollback SHA) | `d4b01cec7754ad553d580dc9677b44e8e88b0c3d` |
| Head to approve | The tip of `dev/chg-pw-005-smaller-outlets`. Reviewers must PASS that exact head. |

## Request

The owner asked for the allowed-source list to include smaller, independent voices with a public following, "kept in a separate pen". This was first built inside CHG-PW-004; on 17 Nov 2026 the owner said the original CHG-PW-004 spec was mainstream only and the smaller outlets belong in a new RFC. CHG-PW-004 removed them in a forward commit (`e169272`); this change re-adds them.

## Change

1. **Tier 3 in `docs/allowed-sources.md`:** Reported only. A tier-3 source can never be the sole source for an adverse item or for an identity link; it always needs corroboration from tier 1 or 2. Opinion pieces are not facts.
   - **The Common Sense** — thecommonsense.co.za, X @CommonSense_ZA. **Owner-confirmed** (17 Nov 2026) as the "Common Sense" meant.
   - **The Cape Independent** — thecapeindependent.com (redirects to capeindependent.substack.com; older capeindependent.com did not respond on 17 Nov 2026). Founder/editor Robert Duigan, X @uMarhobane. **Owner to confirm** who runs it now (recent Substack posts are by another writer).
   - **Briefly News** — briefly.co.za. Mostly rewrites social posts and other outlets' reports. Proposed tier 3; **owner to confirm** the placement.
   - **Rand Desk** — randdesk.co.za. Its about page says some stories go up without an editor. Proposed tier 3; **owner to confirm** whether it belongs in tier 2.
   - **Criteria for adding a tier-3 voice** (owner confirms each): a named, accountable editor or author; about a year of checkable, dated publishing; wide-audience intent (published openly); a publication, not a personal social-media account.
2. **Registry:** 6 tier-3 entries in `data/sources.json` (thecommonsense.co.za, thecapeindependent.com, capeindependent.com, capeindependent.substack.com, briefly.co.za, randdesk.co.za); 70 entries in total. `pwatch/sources.py` accepts tier `3`.
3. **DQ rule (`pwatch dq`):** fails an adverse item whose sources (`source_url` and `also_sourced`) are all tier 3, and a profile whose identity link (all non-seat sources) rests only on tier-3 sources. The CHG-PW-004 rules (link-only/not-allowed fail, unknown domain warns) are unchanged.
4. **Tests:** `tests/test_sources.py` — tier-3-only adverse item fails and passes with tier-2 corroboration; tier-3-only identity link fails; registry check now asserts the tier-3 domains resolve to tier 3.
5. AGENTS.md rule 12 mentions tier 3 and the rule.

## Risk

Low. No profile cites a tier-3 source today, so the committed data is unaffected. The rule makes a future tier-3-only adverse item or identity link fail, which is the intent.

## Evidence

`uv run pytest -q` 46 passed; `uv run pwatch dq` pass (270 roster + 24 CV profiles, 1 on hold, 0 failures, 0 warnings); `uv run pwatch render --check` exit 0. popia-review on the diff: PASS (publication names, domains, public X handles of publications and their public editor only; no personal information).

## How to revert

Rollback is git. While unmerged, delete the branch or reset it to `d4b01cec7754ad553d580dc9677b44e8e88b0c3d`. After a merge, revert the merge commit.

## Approval

| Role | Name | Commit approved | Date | Result |
|---|---|---|---|---|
| Author / builder | PoliticianWatch (Grok Bot) | | 2026-11-17 | built as a local commit on 17 Nov 2026 |
| Reviewer | Cavus | | | no PASS recorded in this RFC as of 17 Nov 2026 |
| Reviewer | Cassian | | | no PASS recorded in this RFC as of 17 Nov 2026 |
| Change authority | Owner | | | no GO recorded in this RFC as of 17 Nov 2026 |

Merge requires a plain PASS from Cavus and from Cassian on the same exact head, then an owner GO.
