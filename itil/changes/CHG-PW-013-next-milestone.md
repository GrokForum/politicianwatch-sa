# CHG-PW-013 — Next milestone: withheld-register checks, source pack, full CoJ gazette profiles

| Field | Value |
|---|---|
| Requested by / date (SAST) | Owner direction, 20 November 2026 at 20:21 SAST, relayed by the orchestrator: take the website to its next major milestone (fold in the source pack, clear the LATER items from the #11 reviews, expand coverage beyond the first 24 Joburg profiles, and work through the end-of-road plus 14-green-nights checklist). |
| Author / builder | author bot |
| Reviewers | two reviewers |
| Change authority | Owner (GO on the exact head to push or merge). This branch is local only until that GO. |
| Type | Normal — medium (gate fixes, source notes, and 245 new gazette-only CV profiles) |
| Environment | DEV + TEST profiles. Publishes nothing: the publish gate and `PW_PUBLISH_ENABLED` are unchanged by this change, and no push, merge or deploy is made here. |
| CIs affected | CI-009 Joburg CV profiles; DQ and site-check withheld-register gates; CI-010 draft-site builder (coverage of the new profiles); live-check (pre-publish nights); collectors (TLS error logging) |
| Linked records | CHG-PW-001 (roster); CHG-PW-007 (site profiles); CHG-PW-008 (nightly / live-check); CHG-PW-011 (Withheld (POPIA) and the private register); CHG-PW-010 (LATER and fresh-repo plan) |
| Branch | `politicianwatch-sa` `dev/chg-pw-013-next-milestone`, from `origin/main` |
| Pre-change commit (rollback SHA) | `df258cff054920d4dd749e4f0e6409287af25437` (`main` after the CHG-PW-011 squash merge) |

## What changes

1. **Site check and site build fail when a Withheld (POPIA) fact has no private-register entry.** The profiles are passed into the check. The missing-register guard keys off each profile's fact labels, not the words "Withheld (POPIA)" in built HTML (the privacy page always names the label, which would have failed a fresh repository that has no withheld facts and no `private/` directory). The contract is explicit: `WITHHELD_REGISTER_REQUIRED` (default True). A fresh public repository that does not carry `private/` must omit Withheld facts from the seed, or point `WITHHELD_SOURCES_PATH` at a sidecar store outside the public tree. Documented in `docs/FRESH-REPO-PLAN.md` and `docs/allowed-sources.md`.
2. **Title and URL leak matching is tightened**, with unit tests: `normalize_url` casefold and leading `www.` strip; needle casefold; `normalize_title` strips HTML tags (including titles split across tags), applies NFKC, folds non-ASCII hyphens, and matches on whitespace-normalised text (hyphens count as spaces). The site-side missing-register guard is tested with profiles, including the case where only the privacy page mentions the label.
3. **CHG-PW-011 RFC "Review round" item 3** is reworded to match what that head actually did (DQ checked per-fact entries; site check only failed on a missing or empty register when the built HTML mentioned the label).
4. **`pwatch live-check` treats a pre-publish state as not red.** When `PW_PUBLISH_ENABLED` is not true, and the live site has 0 profiles while tonight's build has N, the count (and the "lists profile pages" / freshness checks that would otherwise fail on an unpublished placeholder) are reported as `pre-publish` and the night can still be green. Once publishing is on, the check stays strict.
5. **Collectors log certificate and TLS errors** (source, URL, error) to a warning and to `data/raw/tls-errors.jsonl` (gitignored evidence), and surface them on the ingest result. They are never swallowed as a generic retry exhaustion with no TLS label.
6. **Source pack** (PoliticianWatch pack compiled 20 Nov 2026) is folded in as data, not instructions. Each source was checked on 20 Nov 2026 (streamed GET, this machine). Useful sources are recorded in `docs/allowed-sources.md` with tier and terms notes, and the machine-readable registry is **not** extended pending the owner's confirmation. National MPs (Parliament Register of Members' Interests and the PMG API) are a planned 2029 module in `docs/national-2029-module.md`, not code.
7. **Coverage expands from 24 active Joburg CV profiles to 269** (plus the one profile that stays on hold). The 245 new profiles are gazette-only stubs: name, party, seat type, ward or PR, and council, all Confirmed from Government Gazette 55741 (13 November 2026) with a dated source URL and page. Other CV fields are Unknown placeholders. No non-gazette sources, no adverse items, no right-of-reply drafts, and no invented facts. The existing 24 richer profiles and the held Mbatha profile are not rewritten. The committed roster was re-parsed from the local Gazette 55741 PDF on 20 Nov 2026 and matches 270/270.
8. **STATUS, the change log, LATER, the fresh-repo plan and the Joburg source notes** are updated. The 14-day checklist is ticked only where the work is actually in place; the green-night streak is not claimed.

## What stays

The 24 existing CV profiles (facts, sources, withheld entries, adverse items and unsent drafts); the held Mbatha profile; the publish gate and `PW_PUBLISH_ENABLED`; robots, noindex, the DRAFT banner and the privacy page; the unused rule-6 link-exception code; ElectionSePush is still link-only and is not fetched; SAFLII is still by hand only; no contact with councillors; right-of-reply drafts remain unsent.

## Gazette and source verification (20 Nov 2026, SAST)

- Local Gazette 55741 PDF SHA-256 `cd544faf2a703a81eb4466bbfcd3618f5ade03c7b456538116b385c266058798` still matches the committed manifest (7,845,217 bytes, 144 pages, Adobe Acrobat Paper Capture). `pdftotext -layout` of pages 43–47 parsed 270 Joburg rows that match the committed roster exactly (name, party, seat type, ward or PR rank, ward id, source page).
- The PMG mirror `https://static.pmg.org.za/55741_13-11_ElectoralComm_Final.pdf` returned HTTP 200 and is **byte-identical** to the Gazette Finder copy (same SHA-256 and length). The cited source URL on profiles remains the Gazette Finder URL already used since CHG-PW-001.
- IEC results home, LGE dashboard and `Downloads/ME-Results` returned HTTP 200. ElectionSePush was not fetched.
- Municipal Money `officials` facts cube returned HTTP 200, `total_fact_count` 2920. The payload includes official email and phone fields; those values were not stored, and no collector is added (the cube will lag the 4 Nov 2026 election; POPIA: only elected office-bearers' official council channels, never secretary/staff rows).
- Parliament Register of Members' Interests index and the June 2026 v2 PDF returned HTTP 200. Not ingested (planned 2029 module; the register can carry family and other personal details).
- PMG API root returned HTTP 200 with the documented v1 endpoints (including `/member/`). Not ingested (same module).
- DOJ Special Tribunal and Presidency SIU reports pages returned HTTP 200. Recorded as future primary sources for court matters; no new court facts added in this change.
- City of Johannesburg `joburg.org.za` councillor, Executive Mayor / Mayoral Committee, Office of the Speaker and `/about_/Pages/default.aspx` URLs returned HTTP 404. The homepage returned HTTP 200 (redirects to `/Pages/homepage.aspx`). Council offices for 2026–2031 remain Unknown; not guessed.

## Risks

Medium-low. The 245 new profiles contain only public-role facts already in the committed gazette roster. The withheld-register change is fail-closed and removes a false failure that would have bitten a fresh repo. Live-check is looser only while publishing is off; it stays strict once the gate is on. TLS errors are more visible, not less. New source domains are documented but not added to `data/sources.json` until the owner confirms them.

## Seen, not touched

- The unused rule-6 exception in `pwatch/dq.py` and related tests.
- Mechanical enforcement of the FRESH-REPO-PLAN do-not-carry list at seeding, and a decision on where the private register lives in a fresh public repository (still LATER).
- Tests that would catch a removed `check_pi_source_allowance` call in `check_profile` or a removed `check_withheld_entry_format` call in `dq.run` (still LATER). A test is added for `private/` appearing in built output.
- Filling 2026–2031 executive mayor, speaker, MMC and official contact fields (blocked by the joburg.org.za 404s and the lag on Municipal Money).
- The remaining held profile (still needs two identifying details from an allowed source).
- National and provincial 2029 profiles (docs only).
- Stale outcome wording in older STATUS history rows, except the CHG-PW-011 change-log outcome, which is updated to record the merge of PR #11.

## Testing (evidence)

Recorded in the STATUS history row and the PR body (local, not opened): `uv run pytest -q`; `pwatch dq`; `pwatch render --check`; `pwatch site build` + `pwatch site check`; actionlint / zizmor if a workflow file changed; review kit with `--pr-body-file`.

## How to revert

Before merge: delete the local branch (nothing has been pushed). After a future merge: `git revert <merge commit>`; `main` returns to `df258cff`. The 245 new profile files come out with the revert.

## Approval

Plain PASS from two reviewers on the same head, then the owner's GO naming that head before any push, and a further GO before merge. Outcome: pending (local branch only).
