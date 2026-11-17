# CHG-PW-002 — First CV-style profiles: 10 City of Johannesburg councillors

| Field | Value |
|---|---|
| Requested by / date (SAST) | Owner (project owner, by role), relayed by Cavus, 15 November 2026 |
| Author / builder | PoliticianWatch (Grok Bot) |
| Reviewers | Cavus; Cassian (review only) |
| Change authority | Owner (GO on the exact head) |
| Type | Normal — high (adds adverse items about named people; POPIA-relevant handling). Nothing is published by this change. |
| Environment | DEV (code, synthetic tests). TEST data (profiles and unsent drafts) on a branch (draft PR #2). Not PROD. |
| CIs affected | CI-001 schema; CI-004 DQ gate; CI-005 RoR drafts; new CI-009 CV profiles |
| Linked records | CHG-PW-001; `docs/profiles-joburg-2026-batch-1.md`; `docs/sources-joburg-lge-2026.md` |
| Branch | `dev/chg-pw-002-first-profiles` (off `dev/chg-pw-001-scaffold`); draft PR #2, opened 15 Nov 2026 20:28 SAST; base changed to `main` after PR #1 merged |
| Pre-change commit (rollback SHA) | `ed801b102d286d4a6ee8bd781e72f4168f722288` (head of `dev/chg-pw-001-scaffold`, draft PR #1) |
| Head to approve | The tip of `dev/chg-pw-002-first-profiles` after this commit. Reviewers must PASS that exact head. |

## Request

Build CV-style public-role profiles for a first batch of 10 City of Johannesburg councillors from the gazetted 2026 roster. Mix parties and seat types, prefer prominent councillors with public records. Public sources only. Label every fact, with `source_url`, `source_date` and `retrieved_at`. Every adverse item gets right of reply `pending` with a blank reply field and an unsent draft. Mayor stays Unknown; no 2026 MMC is guessed. The request was to commit locally only (no push, no PR, no contact); the branch was later pushed and raised as draft PR #2 on 15 Nov 2026 20:28 SAST.

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
- Not part of the build: push, PR, merge (each needs Cavus's request and the owner's GO; PR #2 was raised 15 Nov 2026), publish, domain, contact with any councillor, party, IEC or anyone else. No email.

## Sources and rules applied

Allowed list only: Gazette 55741; City of Johannesburg official statement; a party's official statement (DA); News24, Daily Maverick, Mail & Guardian, TimesLIVE / Sunday Times, EWN, IOL, The Citizen. SAFLII not fetched; the SCA judgment is cited only as named in The Citizen. ESP not fetched. Identity: at least two matching details per link; the uncertain cases are written up in the batch notes.

## Risks

- **Defamation (RSK-004).** Six adverse items. Each is attributed, labelled (as of review round 2: Reported ×3, Disputed ×1, Alleged ×2; every item's identity link is Reported), carries its outcome (two were set aside by courts, one cleared by an external review, one charge provisionally withdrawn), and has RoR `pending` with a blank reply. Not published. Four-eyes + owner GO required.
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
7. **Flag (not a block):** two items are criminal-behaviour information (Kunene conviction; Gwamanda charges). They are public, reported and relevant to public office; reviewers and the owner should confirm before any publish. (Round 1: the M&G link whose URL named a third party was removed.)

## Implementation plan

1. Branch `dev/chg-pw-002-first-profiles` from `ed801b1`.
2. Research (allowed sources), build the profiles and drafts, extend the schema and DQ gate with tests.
3. Run pytest, `pwatch dq`, `pwatch render --check`, a schema validation and popia-review.
4. Commit locally. **Stop.** No push or PR until Cavus asks and the owner GOes. (Pushed and raised as draft PR #2 on 15 Nov 2026 20:28 SAST.)
5. Cavus and Cassian each give a plain PASS on the same exact head; the owner GOes in quoted words naming this RFC and that head.

## How to revert

Rollback is git. While unmerged: close PR #2 and revert the branch's commits, or (with the owner's confirmation, as it needs a force-push) reset it to `ed801b102d286d4a6ee8bd781e72f4168f722288`. If it is ever merged, revert the merge commit. Removing a single profile means deleting its JSON, `.md` and draft and re-running `pwatch dq`.

## Approval

| Role | Name | Commit approved | Date | Result |
|---|---|---|---|---|
| Author / builder | PoliticianWatch (Grok Bot) | | 2026-11-15 | built locally 15 Nov 2026; draft PR #2 opened 15 Nov 2026 20:28 SAST; review-round-2 head `4a341fe` pushed |
| Reviewer | Cavus | `4a341fe` | 2026-11-17 | plain PASS |
| Reviewer | Cassian (review only) | | | no PASS recorded in this RFC as of 17 Nov 2026; see PR #2 |
| Change authority | Owner | | | no GO recorded in this RFC as of 17 Nov 2026; see PR #2 |

## Review round 1 (Cavus, PASS_WITH_CONCERNS on `5ab0b6e`) — fixes in one new commit

Every source below was fetched and read on 15 Nov 2026 (~20:20–20:35 SAST). Nothing was amended or force-pushed; nothing was pushed.

| # | Concern | Outcome |
|---|---|---|
| 1 | Zille PP outcome wording and citation | Done. Outcome now: "The SCA upheld the appeal and reviewed and set aside the Public Protector's findings and remedial action (Report No. 5 of 2018/19), 7 Feb 2022". Cited to [2022] ZASCA 16 on lawlibrary.org.za (order text verified, incl. "Report No. 5 of 2018/19") plus the SCA media summary on supremecourtofappeal.org.za; label Confirmed. The Citizen kept as a secondary source. SAFLII not used. |
| 2 | Kunene M&G link | Done. M&G link removed; item sourced to SABC (verified: "a law firm has cleared Kunene of any wrongdoing", re-sworn Friday 26 Sep 2025) and EWN. Outcome wording as requested. "African News Global" dropped; re-sourced to EWN ("his online news agency"). |
| 3 | Kenny→Kenneth inference | Done. SABC page carries the oath "I, Thapelo Kenneth Kunene, swear…"; recorded as Reported identity detail. |
| 4 | Zille Federal Council chair stale | Done. Now "former (2019–2026)": DA statement 12 Apr 2026 (Sarupen elected chair, verified; it does not name Zille), The Witness 13 Apr 2026 (Sarupen replaces Zille, who stepped down — verified), Britannica (2019–26, elected Oct 2019 — verified). Reported. |
| 5 | Zille given-name match | Done, with the owner's clarification: given names "Otta Helene" (Britannica, Reported) as the third identity detail; gazetted name kept as printed; "Maree" in the full name recorded as Unknown (`full_name_surname`, null). No family details. |
| 6 | Arnolds OCR claim | Done. "Spelled as gazetted; reported as Margaret (News24, EWN, SABC)" — all three verified. |
| 7 | Mashaba date / appeal | Done. "31 January 2023 (Pretoria)" verified via ActionSA's 31 Jan 2023 statement and TimesLIVE ("this week"); "no appeal found in allowed sources" after a search. Note: the exact date rests on a party statement (Reported). |
| 8 | Gwamanda "from 2012" | Done ("in 2012", Sunday Times wording). Withdrawal wording checked against The Citizen's NPA quote ("criminal proceedings will be re-instituted"). NPA primary statement not added (only a Facebook copy found). |
| 9 | DA press release labelled Confirmed | Done. Downgraded to Reported (Echeozonjoku ×2, Mabaso ×1). The City's 13 Dec 2021 statement was found only on a third-party host, so not cited. |
| 10 | NOT SENT check | Done. `ror.py` now tests the first non-empty line; new test `test_marker_must_be_first_nonempty_line`. |
| 11 | POPIA s26 note | Done in the batch notes: criminal-matter items are special personal information and must be re-verified on the day of any publish. |

Also added: `also_sourced` on facts (each entry DQ-checked for URL, date and retrieved_at; schema + test), optional `given_names` / `full_name_surname` facts (schema + render + test).

Evidence after the fixes: `uv run pytest -q` **32 passed**; `uv run pwatch dq` **pass** (270 + 10, 0 failures, exit 0); `pwatch render --check` exit 0; JSON Schema validation 0 errors; popia-review **PASS** (scan of added lines: no IDs, phones, emails, addresses; no private person named in text or URLs; the only "Molefe" in the repo is a gazetted councillor surname in the roster; no family details). Labels now: Confirmed 53, Reported 51, Unknown 21, Disputed 1, Alleged 2 (128).

## Review round 2 (Cavus + Cassian, PASS_WITH_CONCERNS on PR #2 head `c352484`) — one new commit

Local commit on `dev/chg-pw-002-first-profiles`; nothing amended, force-pushed or pushed.

| # | Concern | Outcome |
|---|---|---|
| a | STATUS.md said CHG-PW-002 was local only with no PR | Done. STATUS.md now says the change is on the branch with PR #2 (draft), not merged, "see the PR for the current head" (stays true after a push). Change-log row fixed the same way. A new STATUS history row records this round. |
| b | Zille court item claimed Confirmed although its link to OTTA HELENE MAREE is only Reported | Done. New `identity_link_label` on adverse items (schema + DQ: an item may not be labelled higher than its link; test added). Every adverse item has `identity_link_label: Reported`. The Zille item is now **Reported** (the SCA judgment is still cited as the source). Identity note explains it. |
| c | Kunene `convicted` (1997) rests on a Daily Maverick retelling | Done. No case citation was found in allowed sources (searched 17 Nov 2026: Daily Maverick, Sunday Times 2010, M&G 2011 all retell the conviction without a case number; SAFLII not fetched). `matter_status` is now `reported_conviction` (schema enum extended; test added); outcome reads "Reported: convicted (no judgment citation found)…"; label stays Reported. |

Evidence: `uv run pytest -q` **34 passed**; `uv run pwatch dq` pass (270 + 10, 0 failures); `pwatch render --check` exit 0; JSON Schema 0 errors; popia-review PASS (no IDs, phones, emails, addresses, family or private persons added). Labels: Confirmed 52, Reported 52, Unknown 21, Disputed 1, Alleged 2 (128).

## Post-implementation review

- Outcome: built and tested locally on 15 Nov 2026 (DEV build SUCCEEDED); raised as draft PR #2 on 15 Nov 2026 20:28 SAST; review rounds 1 and 2 fixed (head `4a341fe`); Cavus plain PASS on `4a341fe` (17 Nov 2026). Not published. Merge requires both reviewers' plain PASS on the same head and an owner GO; see PR #2 for current state.
- Follow-ups: refresh roles after the first council sitting (~19 Nov 2026); education and career research; official contact channels for the drafts (owner); later batches (e.g. Ennie Makhafola, Jack Sekwaila).

## Seen, not touched

- `docs/sources-joburg-lge-2026.md` still says "CVs: not built" (true for the roster; CV profiles live separately). Left as is to keep the change surgical.
- The DuckDB loader (`pwatch/warehouse.py`) does not load CV profiles. Out of scope.
- `ror.py` imports `datetime`, which is unused (pre-existing).
