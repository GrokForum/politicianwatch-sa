# CHG-PW-003 — CV profiles batch 2: City of Johannesburg councillors (14 active + 1 on hold) (+ PR #2 review nits)

| Field | Value |
|---|---|
| Requested by / date (SAST) | Owner (project owner, by role), relayed by Cavus, 17 November 2026 |
| Author / builder | PoliticianWatch (Grok Bot) |
| Reviewers | Cavus; Cassian |
| Change authority | Owner (GO on the exact head) |
| Type | Normal — medium (named people, public role only; no adverse items in this batch). Nothing is published by this change. |
| Environment | DEV (code, synthetic tests). TEST data (profiles and unsent drafts) on a local branch. Not PROD. |
| CIs affected | CI-001 schema/DQ checks (`also_sourced` formats); CI-005 RoR drafts; CI-009 CV profiles |
| Linked records | CHG-PW-002 (PR #2); `docs/profiles-joburg-2026-batch-2.md`; `docs/profiles-joburg-2026-batch-1.md` |
| Branch | `dev/chg-pw-003-batch-2`, stacked on `dev/chg-pw-002-first-profiles` |
| Pre-change commit (rollback SHA) | `4a341fedb1c0287b1e7a748d9b2163198b69544e` (local head of the PR #2 branch after review round 2; not yet pushed) |
| Head to approve | The tip of `dev/chg-pw-003-batch-2`. Reviewers must PASS that exact head. |

## Request

Next batch of 15 Johannesburg councillor profiles from the 2026 roster, excluding the 10 in CHG-PW-002; weighted to ward seats (≥ 8), spread across parties roughly by seats; prefer councillors with a public record. Same standards as CHG-PW-002, enforced by DQ. Plus, as a separate commit, Cavus's nits from the PR #2 review. Commit locally only: no push, no PR, no contact.

## Pre-check (17 Nov 2026, ~10:59 SAST)

`git fetch` and `gh pr list`: PR #2 "CHG-PW-002: first 10 Joburg councillor profiles" is **open, draft**, head `dev/chg-pw-002-first-profiles` at `c352484`, base `dev/chg-pw-001-scaffold`, created 15 Nov 2026 20:28 SAST; no reviews or comments recorded on GitHub. PR #1 is open, draft. `origin/main` is `cfa7e22`. The PR #2 branch is frozen at `c352484` on the remote; the review-round-2 fix `4a341fe` exists only locally (not pushed by this change).

## Commits in this change

1. **Nits commit** (`CHG-PW-003: PR #2 review nits (Cavus)`):
   - Mashaba outcome: duplicate "(Pretoria)" removed.
   - Gwamanda outcome: the repeated closing-bracket sentence removed (the NPA wording stays once: provisionally withdrew; proceedings would be re-instituted).
   - Zille Britannica fact: `source_date` 2026-11-13 confirmed as the page's own dateline ("Nov. 13, 2026"), re-checked on the live page on 17 Nov 2026; noted on the fact.
   - `pwatch dq`: every `also_sourced` entry is now format-checked — `source_url` must be an http(s) URL with a host, `source_date` a real `YYYY-MM-DD` date, `retrieved_at` an ISO 8601 datetime with a UTC offset. New test `test_also_sourced_date_and_url_formats_are_checked`.
2. **Batch commit** (`CHG-PW-003: batch 2 — 15 Joburg CV profiles`, `159542e`): 15 profiles + rendered `.md`, 15 optional accuracy-check drafts, batch notes, this RFC, STATUS and change log.
3. **Fix commit** (`CHG-PW-003: fix 1 — Cassian blind source check on 159542e`): see "Review round 1" below. Mbatha on hold (14 active profiles), first-year-in-council facts for Schay, Chame, Makhafola (and Magwentshu re-verified), Steenkamp second-detail check, hold handling in the loader with a test.

## What changes

- `data/profiles/joburg-2026/<slug>.json` and `.md` for 15 new slugs (see batch notes).
- `drafts/right-of-reply/CHG-PW-003/<slug>.md` — 15 optional factual-accuracy checks (no adverse items in this batch). Marker on the first line; channel "[official channel, owner to confirm]"; deadline "[owner sets on sending]".
- Nits commit: 3 existing CHG-PW-002 profiles (+ 2 drafts), `pwatch/schema.py`, `tests/test_profiles.py`.
- Docs/records: `docs/profiles-joburg-2026-batch-2.md`, this RFC, `STATUS.md`, `itil/registers/change-log.md`.

## What stays

- Roster (270 / 135 / 135), mayor Unknown, schema shape, the 10 CHG-PW-002 profiles except the three nits.
- No dependency added. No push, PR, merge, publish or contact.

## Sources and rules applied

- Allowed sources only: Gazette 55741; City of Johannesburg statements/newsroom; News24, TimesLIVE, IOL, EWN, The Citizen, SABC; party statements (DA Gauteng, ActionSA) labelled Reported. Fix 1 adds three sources named by reviewer Cassian, each labelled Reported: SA Jewish Report, Southern Courier (Caxton local newspaper, published on citizen.co.za) and Sowetan. **Owner to confirm** these join the allowed list. SAFLII not fetched; esp.info not scraped (an ESP link appeared in a search result and was not opened).
- Every fact has a label, `source_url`, `source_date`, `retrieved_at`. Identity ≥ 2 details for every non-gazette source; uncertain links listed as "not linked" in the batch notes.
- Public role only. No private persons or co-accused named. No 2026–2031 office guessed.

## Risks

- **Misidentification (RSK-009).** Mitigated by ≥ 2 details; short-form names (Gert, Jakes, Adolph) not used as matches; Atterbury, Marema and Mpolobosho left out.
- **Stale roles.** Several roles are "as at" 2026 dates; re-verify after the first sitting.
- **POPIA.** A City PDF with councillors' home addresses and phones was seen and deliberately not cited; DOB/family details in cited sources not recorded.

## Testing evidence (on the batch-commit head)

- `uv run pytest -q`: **35 passed**.
- `uv run pwatch dq`: **pass** — 270 roster rows + 25 CV profiles, 0 failures (exit 0).
- `uv run pwatch render --check`: exit 0.
- JSON Schema (ad hoc, `uv run --with jsonschema==4.25.1`): 0 errors across 25 profiles.
- Labels (batch 2): Confirmed 86, Reported 41, Unknown 29 (156). Adverse items: 0.
- popia-review on the diff: **PASS** (see below).

## POPIA review (popia-review skill)

- Scan of added lines: no SA ID numbers, phone numbers, email addresses, home addresses, account numbers or credentials.
- Identity linking: only public office-holders, by public role; no pseudonymous accounts unmasked.
- Necessity: DOB, family, religious role and personal descriptions in sources were not recorded; the City's chairpersons PDF (home addresses, phones) is not cited.
- Private persons: none named. Third parties named are public office-holders in their public role (mayors, caucus leaders).
- Verdict: **PASS**.

## Review round 1 — Cassian blind source check on `159542e` (17 Nov 2026)

One fix commit on `dev/chg-pw-003-batch-2`, local only (no push, no amend). Every source below was fetched and read on 17 Nov 2026 (~11:45 SAST, `retrieved_at` 2026-11-17T11:45:00+02:00); the publication date is the article's own dateline / `datePublished`.

| # | Finding | Outcome |
|---|---|---|
| 1 | MTHEMBENI SELBY MBATHA (MK, ward 61): Gazette 55741 has two councillors surnamed MBATHA (the other is PHUMLANI MOSES MBATHA, DA, ward 92) and the profile did not show which was matched | **On hold.** Profile moved to `data/profiles/joburg-2026/_hold/` (JSON carries `"status": "on_hold"` and `hold_reason`; `.md` carries a hold notice), its draft to `drafts/right-of-reply/CHG-PW-003/_hold/`, each folder with a README. Reason recorded: two identifying details from an allowed source are needed before linking; none was found. Roster row unchanged. `load_profile_dir` now skips `_hold/` (already non-recursive) **and** any file marked `on_hold`; new `load_held_profiles`; `pwatch dq` reports `cv_profiles_on_hold`; render neither writes nor checks held files. New test `test_held_profiles_are_excluded_from_batch_dq_and_render`. |
| 2a | Schay — first year in council (SA Jewish Report) | **Added**, Reported: "First year in council: 2021. Newly elected as the DA's ward 72 councillor in the 1 November 2021 local government elections". Source: https://www.sajr.co.za/the-winners-and-losers-in-the-elections/ (2021-11-04). Identity: name 'Daniel Schay' + DA + ward 72 (three details). The article's professional qualification is not added (out of scope; career stays Unknown). |
| 2b | Chame — ward 57 by-election, 2 Jul 2014 (Southern Courier) | **Added**, Reported: "First year in council: 2014. Won the City of Johannesburg ward 57 by-election for the DA on Wednesday 2 July 2014 (66.09% of the vote, as reported)". Source: https://www.citizen.co.za/southern-courier/news-headlines/2014/07/11/new-da-ward-57-councillor-faeeza-chame/ (2014-07-11). Identity: name + DA + ward 57 (three details; boundaries redrawn since 2014). The article's age, suburb, family, personal phone and email are **not** recorded. Continuous service 2014–2026 is listed as Unknown. |
| 2c | Magwentshu — councillor since Nov 2021 (The Citizen) | **Verified; already in the profile.** Wording aligned to "First year in council: 2021. Became a councillor in November 2021", Reported. Source: https://www.citizen.co.za/news/lubabalo-magwentshu-mmc-interview/ (2023-06-17). Identity: name + ATM + Community Development MMC (three details). |
| 2d | Makhafola — sworn in 3 Feb 2023 (Sowetan) | **Added**, Reported: "First year in council: 2023. Sworn in as a City of Johannesburg councillor (EFF) on Friday 3 February 2023". Source: https://www.sowetan.co.za/news/south-africa/2023-02-03-kunene-makhafola-sworn-in-as-councillors/ (2023-02-03; "on Friday" = 3 Feb 2023). Identity: name 'Ennie Makhafola' + EFF + City of Johannesburg councillor (three details). |
| 3 | DEVON STEENKAMP: Gazette has two councillors surnamed STEENKAMP | **Kept; check passes.** The DA statement (https://dagauteng.org.za/2024/07/johannesburg-region-caucus-elections-official-statement, 2024-07-23) gives the given name Devon and the party (DA, Johannesburg region caucus). Both match DEVON STEENKAMP (DA, ward 98); neither matches RAYMONT ISMAEL STEENKAMP (PA, ward 29). It gives no ward; "Region C" is a DA caucus region and is **not** used as a match (no allowed source maps ward 98 to it). Identity note updated to say so. No facts dropped. |

Counts after fix 1 (14 active batch-2 profiles): Confirmed 81, Reported 44, Unknown 26 — 151 facts; adverse items 0. All 24 active profiles (batch 1 + batch 2): Confirmed 133, Reported 96, Unknown 47, Alleged 2, Disputed 1 — 279; adverse items 6 (unchanged).

Tests after fix 1: `uv run pytest -q` 36 passed; `uv run pwatch dq` pass (270 roster + 24 CV profiles, 1 on hold, 0 failures); `uv run pwatch render --check` exit 0. popia-review on the fix diff: PASS (see below).

**POPIA (fix 1):** Scan of added lines: no ID numbers, phone numbers, email addresses, home addresses or accounts. The Southern Courier article contains a personal phone number, email, age, suburb and family details, and the Citizen interview contains a date of birth, family and religious details; none is recorded. No private persons named (the 2014 by-election opponent is not named). The held Mbatha profile links nothing to anyone. Verdict: **PASS**.

**Seen, not touched (fix 1):** The Citizen (2023-06-17) says Gwamanda "recently appointed" Magwentshu as MMC, while the City statement (2023-02-02) records his appointment by Mayor Amad; probably a reappointment after the May 2023 mayoral change, but not checked and not recorded.

## Rollback

`git checkout dev/chg-pw-002-first-profiles` (or `git branch -D dev/chg-pw-003-batch-2`); pre-change SHA `4a341fedb1c0287b1e7a748d9b2163198b69544e`. Fix 1 alone: `git reset --hard 159542e1e2bc94e767a1ea48e047733089019c6f` on the local branch (owner confirmation needed first). Nothing is pushed, so rollback is local only.

## Seen, not touched

- `pwatch/ror.py` imports `datetime` unused (pre-existing).
- STATUS history row for CHG-PW-001 still says "not pushed" for 15 Nov (historical wording; left as is).

## Result

Built and checked locally; review round 1 (Cassian) fixed in fix 1. **Awaiting** a plain PASS from Cavus and from Cassian on the same head, then an owner GO. Not SUCCEEDED until then.
