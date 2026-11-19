# CHG-PW-011 — Magwentshu: restore The Citizen source on the owner's decision; rule 6 owner-approved exception

| Field | Value |
|---|---|
| Requested by / date (SAST) | Owner decision, in the owner's own words, relayed by the orchestrator on 19 Nov 2026 at 16:27 SAST: "Keep The Citizen link with the 'personal details not recorded here' note." |
| Author / builder | author bot |
| Reviewers | two reviewers |
| Change authority | Owner (decision above; GO on the exact head to merge) |
| Type | Normal — medium (profile data, a DQ rule and the renderers) |
| Environment | DEV + TEST profiles. Publishes nothing: the publish gate and `PW_PUBLISH_ENABLED` are unchanged, and profiles stay unpublished |
| CIs affected | CI-009 Joburg CV profiles (one profile); DQ gate; CI-010 draft-site builder (note rendering) |
| Linked records | CHG-PW-007 (rule 6, set the three facts to Unknown); CHG-PW-003 (first sourced the facts) |
| Branch | `politicianwatch-sa` `dev/chg-pw-011-magwentshu-source`, from `origin/main` |
| Pre-change commit (rollback SHA) | `c85db068b6933924cc0b571ed65e4192c661261a` (`main` after the CHG-PW-012 squash merge; tag `snapshot-2026-11-19-pre-pw-pr12` is the state before that merge) |

## What changes

1. **Profile `lubabalo-cecil-magwentshu`:** three facts restored exactly as they were before CHG-PW-007 set them to Unknown (taken from git history at `ffa062c`): `education`, `career` and `cv[0]` ("First year in council: 2021. Became a councillor in November 2021", field position, period 2021-11). Each is **Reported**, source The Citizen (`citizen.co.za`, tier 2), source date 2023-06-17, retrieved 2026-11-17 (date only, as logged then). Each carries the owner's exact note, `note: "personal details not recorded here"`, and `owner_approved_pi_source: "2026-11-19 16:27 SAST (CHG-PW-011)"`. They leave `unknown_fields`. No private detail from the article is copied (values are the same public-role text as before). The article was not fetched or saved in this change; the URL and the public-role wording are taken from git history (`ffa062c`).
2. **Identity match (at least two details):** the three matched details (name, party ATM, council role) now cite The Citizen as well as the City statement (2023-02-02) and Sowetan (2022-09-14), as before CHG-PW-007. The identity note says the interview is linked on the owner's decision of 19 Nov 2026, 16:27 SAST, and uses the same note: personal details not recorded here.
3. **Rule 6 amended** (CHG-PW-007 RFC item 6, `docs/allowed-sources.md`): the default is unchanged (a source carrying private personal details is not linked; the fact is Unknown). A source **may** be linked when the owner approves it for named facts, provided no private detail is reproduced and the note is present.
4. **DQ (`pwatch dq`):** new `check_pi_source_allowance`. It fails: the note without the approval; the approval without the exact note, without an http(s) link, on an Unknown fact or in the wrong format (`YYYY-MM-DD HH:MM SAST (CHG-PW-NNN)`); the approval on an adverse item; and any fact in the same profile citing an approved URL without its own approval. Rule 6 was not enforced mechanically before; this enforces only the exception. Tests in `tests/test_dq.py`.
5. **Renderers:** for an approved fact only, the note is shown next to the source on the site (`<span class="src-note">`) and in the markdown render. Other fact notes are still not rendered (no change to other profiles). Test in `tests/test_site_profiles.py`.
6. **Records aligned:** batch-2 doc, the unsent accuracy-check draft (education, career and first-year lines restored), CHG-PW-003 RFC row 2c, change log, STATUS (009 merged as `ce45d829`, 010 merged as `33b3fb32`; 011 in review as PR #11).

## What stays

All other profiles and their renders; Chame and Raphadu notes ("a source with personal details was not used"); the Sowetan committee-chair fact; the publish gate; robots, noindex, DRAFT banner and privacy page.

## Risks

Medium-low. The note tells readers that the linked article carries personal details, which earlier reviews asked to avoid; it is the owner's explicit choice. The article itself is unchanged by us; if it is later edited to add more private details, the link still points to it (the 14-day link check in the fresh-repo plan would surface changes only to availability, not content). The linked article also carries, recorded here by category only and with no detail from the article: special personal information (religious belief, POPIA s26); information about children, including a minor (POPIA s34); date of birth; and family details.

## Seen, not touched

- Per-fact `note` fields on other profiles (e.g. `known_as`) are not rendered; unchanged.
- CHG-PW-009 (merged as `ce45d829`) and CHG-PW-010 (merged as `33b3fb32`) are on main; this branch merges `origin/main` at `c85db068` (CHG-PW-012).

## Testing (evidence)

See the STATUS history row: pytest, `pwatch dq`, `pwatch render --check`, site build + check, `actionlint`, the review kit (output saved outside the repo and pasted into the PR body), and a PI scan of the diff.

## How to revert

Before merge: close the PR or delete the branch. After merge: `git revert <merge commit>`; `main` returns to `c85db068` (CHG-PW-012), the three facts go back to Unknown and the exception is removed.

## Approval

Plain PASS from two reviewers on the same head, then the owner's GO to merge. Outcome: pending (in review as PR #11).
