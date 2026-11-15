# CHG-PW-002 — First CV-style profiles: 10 City of Johannesburg councillors

| Field | Value |
|---|---|
| Requested by / date (SAST) | Owner (project owner, by role), relayed by Cavus, 15 November 2026 |
| Author / builder | PoliticianWatch (Grok Bot) |
| Reviewers | Cavus; Cassian (review only) |
| Change authority | Owner (GO on the exact head) |
| Type | Normal — high (adds adverse items about named people; POPIA-relevant handling). Nothing is published by this change. |
| Environment | DEV (code, synthetic tests). TEST data (profiles and unsent drafts) on a local branch. Not PROD. |
| CIs affected | CI-001 schema; CI-004 DQ gate; CI-005 RoR drafts; new CI-009 CV profiles |
| Linked records | CHG-PW-001; `docs/profiles-joburg-2026-batch-1.md`; `docs/sources-joburg-lge-2026.md` |
| Branch | `dev/chg-pw-002-first-profiles` (off `dev/chg-pw-001-scaffold`) |
| Pre-change commit (rollback SHA) | `ed801b102d286d4a6ee8bd781e72f4168f722288` (head of `dev/chg-pw-001-scaffold`, draft PR #1) |
| Head to approve | The tip of `dev/chg-pw-002-first-profiles` after this commit. Reviewers must PASS that exact head. |

## Request

Build CV-style public-role profiles for a first batch of 10 City of Johannesburg councillors from the gazetted 2026 roster. Mix parties and seat types, prefer prominent councillors with public records. Public sources only. Label every fact, with `source_url`, `source_date` and `retrieved_at`. Every adverse item gets right of reply `pending` with a blank reply field and an unsent draft. Mayor stays Unknown; no 2026 MMC is guessed. Commit locally only: no push, no PR, no contact.

## What changes

- `data/profiles/joburg-2026/<slug>.json` — 10 profiles, plus a generated markdown rendering `<slug>.md` for each.
- `drafts/right-of-reply/CHG-PW-002/<slug>.md` — 10 drafts: 4 right-of-reply drafts (6 adverse items) and 6 clearly marked *optional factual-accuracy checks*. Every draft starts with "DRAFT: NOT SENT. The owner sends personally. The bot never sends."
- `drafts/right-of-reply/TEMPLATE.md` and `SYNTH-001.md` — the NOT SENT marker added; the deadline reads "[owner sets on sending]".
- `schemas/profile.schema.json` — optional `slug`, `change`, `known_as`, `cv[]` (labelled facts with `field` position/career/candidacy/education), `identity_match`, `unknown_fields`; adverse items may carry `outcome` and `category`; `right_of_reply.deadline` may be null while pending, plus `deadline_rule`.
- DQ gate (`pwatch/schema.py`, `pwatch/ror.py`, `pwatch/dq.py`, new `pwatch/profiles.py`): (a) every non-Unknown fact needs `retrieved_at`; (b) `cv[]` and `known_as` facts are label/source checked; (c) a profile linking any non-seat source needs ≥ 2 identity details; (d) a CV profile must match its gazetted roster row (name, party, seat type, ward, ward id, PR rank, council); (e) every RoR draft must carry the NOT SENT marker; (f) a null deadline is allowed only while pending.
- CLI: `pwatch dq` now gates the roster **and** the CV profiles; new `pwatch render [--check]`.
- Tests: `tests/test_profiles.py` (9 tests, synthetic only); `tests/conftest.py` synthetic adverse fixture gains an `identity_match`.
- Docs and records: `docs/profiles-joburg-2026-batch-1.md`, this RFC, `STATUS.md`, `itil/registers/change-log.md`, CI and risk registers, `README.md` contents.

## What stays

- The 270-row roster, its counts (270 / 135 / 135) and the gazette/IEC provenance are unchanged.
- Executive mayor stays Unknown in `data/roster/joburg-2026-council.json`.
- No dependency added (`jsonschema` was used ad hoc via `uv run --with` for a one-off validation, not added to the project).
- No push, no PR, no merge, no publish, no domain, no contact with any councillor, party, IEC or anyone else. No email.

## Sources and rules applied

Allowed list only: Gazette 55741; City of Johannesburg official statement; a party's official statement (DA); News24, Daily Maverick, Mail & Guardian, TimesLIVE / Sunday Times, EWN, IOL, The Citizen. SAFLII not fetched; the SCA judgment is cited only as named in The Citizen. ESP not fetched. Identity: at least two matching details per link; the uncertain cases are written up in the batch notes.

## Risks

- **Defamation (RSK-004).** Six adverse items. Each is attributed, labelled (Disputed ×2, Alleged ×2, Reported ×2), carries its outcome (two were set aside by courts, one cleared by an external review, one charge provisionally withdrawn), and has RoR `pending` with a blank reply. Not published. Four-eyes + owner GO required.
- **Identity error (new RSK-009).** Gazette legal names differ from public names for Zille (Otta Helene Maree), Kunene and Arnolds. Mitigation: ≥ 2-detail rule enforced by DQ; reasoning recorded per profile; reviewers asked to confirm.
- **POPIA special personal information (criminal behaviour, s26).** The Kunene conviction and the Gwamanda charges are criminal-behaviour information about public office-holders, drawn from reputable reporting and relevant to public office. Flagged for reviewer judgement before any publish.
- **Stale facts.** Roles change at the first sitting (~19 Nov 2026). Profiles mark 2026–2031 roles Unknown.

## Testing (evidence, not claims)

- [x] `uv run pytest -q`: **29 passed** (20 existing + 9 new), synthetic fixtures only, no network.
- [x] `uv run pwatch dq`: **pass**, 270 roster profiles + 10 CV profiles, 0 failures, exit 0 (as of 2026-11-15).
- [x] `uv run pwatch render --check`: exit 0 (renderings current).
- [x] JSON Schema: all 10 profiles validate against `schemas/profile.schema.json` (Draft 2020-12, jsonschema 4.25.1 run ad hoc): 0 errors.
- [x] popia-review of the diff: **PASS** (see below).

## POPIA review (popia-review skill) — verdict PASS

1. **Scan** of every added line in the diff for SA ID numbers, passport numbers, phone numbers, emails, street addresses, account numbers and private social accounts: **0 hits**. No personal contact details; each draft uses "[official channel, owner to confirm]".
2. **Identity linking:** no anonymous or pseudonymous account is unmasked. Links are between a gazetted public office-holder and reporting about that office-holder, each with ≥ 2 matching details.
3. **Necessity:** public-role facts only (offices, candidacies, party roles, public court/regulatory matters with outcomes). Removed or not collected: family members (including names that appear in encyclopaedia entries), birth dates and places, personal contacts on aggregator sites, a spouse reference in one source, the names of a private co-accused and of a private third party.
4. **Public figures:** all ten are elected councillors; content is kept to the public role and public record.
5. **Companies:** iThemba Lama Afrika and a law firm are named only as they appear in reputable reporting, as attributed reports, not as findings.
6. **Storage:** private repo, local branch only. The builder script lives in the bot's scratch space, outside the repo.
7. **Flag (not a block):** two items are criminal-behaviour information (Kunene conviction; Gwamanda charges). They are public, reported and relevant to public office; reviewers and the owner should confirm before any publish. The Kunene item's M&G URL slug contains a third party's name (required for the citation).

## Implementation plan

1. Branch `dev/chg-pw-002-first-profiles` from `ed801b1`.
2. Research (allowed sources), build the profiles and drafts, extend the schema and DQ gate with tests.
3. Run pytest, `pwatch dq`, `pwatch render --check`, a schema validation and popia-review.
4. Commit locally. **Stop.** No push or PR until Cavus asks and the owner GOes.
5. Cavus and Cassian each give a plain PASS on the same exact head; the owner GOes in quoted words naming this RFC and that head.

## How to revert

Rollback is git. The branch is local and unmerged: delete it, or reset it to `ed801b102d286d4a6ee8bd781e72f4168f722288`. If it is ever merged, revert the merge commit. Removing a single profile means deleting its JSON, `.md` and draft and re-running `pwatch dq`.

## Approval

| Role | Name | Commit approved | Date | Result |
|---|---|---|---|---|
| Author / builder | PoliticianWatch (Grok Bot) | | 2026-11-15 | built locally; not pushed |
| Reviewer | Cavus | | | pending PASS on the exact head |
| Reviewer | Cassian (review only) | | | pending PASS on the exact head |
| Change authority | Owner | | | pending GO |

## Post-implementation review

- Outcome: built and tested locally; not pushed, not reviewed, not merged, not published. Result: SUCCEEDED (DEV build); awaiting review.
- Follow-ups: refresh roles after the first council sitting (~19 Nov 2026); education and career research; official contact channels for the drafts (owner); later batches (e.g. Ennie Makhafola, Jack Sekwaila).

## Seen, not touched

- `docs/sources-joburg-lge-2026.md` still says "CVs: not built" (true for the roster; CV profiles live separately). Left as is to keep the change surgical.
- The DuckDB loader (`pwatch/warehouse.py`) does not load CV profiles. Out of scope.
- `ror.py` imports `datetime`, which is unused (pre-existing).
