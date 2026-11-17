# CHG-PW-004: Allowed-source list and retrieved_at wording (housekeeping)

| Field | Value |
|---|---|
| Requested by / date (SAST) | Owner (project owner, by role), 17 November 2026 |
| Author / builder | PoliticianWatch (Grok Bot) |
| Type | Standard, low (documentation and docstrings only; no data or logic changes) |
| Environment | DEV |
| Branch | `dev/chg-pw-004-housekeeping`, stacked on CHG-PW-003 (`95426512`, draft PR #3) |
| Rollback | `git revert` this commit, or reset the branch to `95426512` |

## Request and reasons
1. On 17 Nov 2026 the owner confirmed that SA Jewish Report, Southern Courier and Sowetan join the allowed sources. They were first used in CHG-PW-003 fix 1 at reviewer Cassian's suggestion. The allowed list was scattered across the batch notes and RFCs; it is now a single file, `docs/allowed-sources.md`, which AGENTS.md rule 12 references.
2. Cavus review note on PR #3: the docstrings and the schema description said a date-only `retrieved_at` is "read as the end of that day". The code treats it as future only if that date is after today's date in SAST. The text now says that. No logic change.
3. Cavus review note: AGENTS.md rule 11 now says that `data/raw/manifest.jsonl` is committed and not gitignored, while fetched pages are.

## Risk
Low. Documentation only. Tests, `pwatch dq` and `pwatch render --check` must still pass.

## Merge order
PR #2, then PR #3, then this change.

## Approval
| Role | Name | Commit approved | Date | Result |
|---|---|---|---|---|
| Author / builder | PoliticianWatch (Grok Bot) | | 2026-11-17 | drafted |
| Reviewer | Cavus | | | pending PASS on the exact head |
| Reviewer | Cassian (Build, review only) | | | pending PASS on the exact head |
| Change authority | Owner | | | pending GO |
