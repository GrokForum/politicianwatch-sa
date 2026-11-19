# CHG-PW-010 — Parked-ideas list and fresh public repository plan (documentation only)

| Field | Value |
|---|---|
| Requested by / date (SAST) | Relayed by the orchestrator on 19 Nov 2026 (16:16 SAST) |
| Author / builder | PoliticianWatch (Grok Bot) |
| Reviewers | reviewer (two reviewers) |
| Change authority | Owner (GO on the exact head) |
| Type | Standard — low (documentation only) |
| Environment | DEV. No code, data, workflow or site change; nothing is created, pushed or published |
| Branch | `politicianwatch-sa` `dev/chg-pw-010-later-and-fresh-repo`, from `origin/main`, separate from CHG-PW-009 |
| Pre-change commit (rollback SHA) | `a0698d20022b8d1be2861c2a041978203b13a2b3` |

## What changes

- `docs/LATER.md` (new): parked ideas, one line each, with a header saying they are not planned work.
- `docs/FRESH-REPO-PLAN.md` (new): (1) the end-of-road definition for the Joburg pilot and a 14-day stability checklist; (2) what must not carry over to a fresh public repository, from an inspection of the tree and refs; (3) a seeding procedure (clean `git archive` export of the approved `main`, exclusion list, PI scan plus dq and tests, one root commit under the neutral publisher identity, branch protection, merge only on human approval). It records that the owner says the old repositories will be deleted.
- Change log row and STATUS line for this change.

## What stays

Everything else. The plan's steps that create a repository, push, set protection or delete repositories each need their own change record and the owner's GO.

## Seen, not touched

- No check confirms that claim source links still resolve; the 14-day checklist relies on it, so it is listed in LATER.md and marked as manual in the plan.
- `tests/test_dq.py` and `tests/test_live_check.py` use real profile slugs as fixtures (listed in the plan for replacement before seeding).

## Testing

Docs only. pytest, `pwatch dq`, `pwatch render --check`, site build and check were run to confirm no drift; the review kit was run on the committed head (output saved outside the repo).

## How to revert

Delete the branch, or `git revert` after merge.

## Approval

Plain PASS from both reviewers on the same head, then the owner's GO. Outcome: **merged** — PR #10 squash-merged into `main` as `33b3fb32` (pre-merge tag `snapshot-2026-11-19-pre-pw-pr10`).
