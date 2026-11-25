# CHG-PW-016 — Add dpsa.gov.za as a tier-1 source

| Field | Value |
|---|---|
| Requested by / date (SAST) | Owner decision, 25 November 2026 at 16:37 SAST, quoted: "Yes, dpsa.gov.za is tier 1." Relayed after [PR #15](https://github.com/GrokForum/politicianwatch-sa/pull/15) was squash-merged into `main` as `75389ff`. |
| Author / builder | author bot |
| Reviewers | two reviewers |
| Change authority | Owner (GO on the exact head to push or merge). Push and merge need the owner's GO naming the exact head. |
| Type | Standard — low (source-registry addition; no profile facts or figures published) |
| Environment | DEV. The publish gate and `PW_PUBLISH_ENABLED` are unchanged. |
| CIs affected | CI source registry (`data/sources.json`); human-readable list `docs/allowed-sources.md`. No profile, roster, collector, workflow or site-builder change. |
| Linked records | CHG-PW-015 (pay-context RFC; [PR #15](https://github.com/GrokForum/politicianwatch-sa/pull/15) squash-merged as `75389ff`); CHG-PW-013 (earlier official-source additions) |
| Branch | `politicianwatch-sa` `dev/chg-pw-016-dpsa-tier1`, from `origin/main` `75389ffbd8229f865e6c6d2768a77a7e85b56dd2` |
| Pre-change commit (rollback SHA) | `75389ffbd8229f865e6c6d2768a77a7e85b56dd2` (PR #15 squash on `main`) |

## What changes

1. **`data/sources.json`.** Add `dpsa.gov.za` as tier 1, outlet "Department of Public Service and Administration (2022 Guide for Members of the Executive)", verified 2026-11-25. A domain matches itself and its subdomains, so `www.dpsa.gov.za` is covered.
2. **`docs/allowed-sources.md`.** Add the domain to the tier-1 table and a dated owner-approval section, including the Guide URL and the SHA-256 recorded when it was fetched for CHG-PW-015 on 25 November 2026 (SAST): HTTP 200, 32 pages, 829,996 bytes, SHA-256 `7ffd4ce3a56260d703e714378152a18b3d6b143e1b309ff1982eb4062653dae6`.
3. **`tests/test_sources.py`.** Assert that the Guide URL is classified as tier 1.
4. **Records.** This RFC, STATUS, and the change log.

This answers CHG-PW-015 open question 4 (source registry). The 015 RFC itself is not edited.

## What stays

[PR #15](https://github.com/GrokForum/politicianwatch-sa/pull/15), already squash-merged into `main` as `75389ff`. All profiles, the gazette roster, collectors, workflows, and the site builder. The publish gate. No package figures or executive entitlements are published. Other pack domains named in CHG-PW-015 (`gov.za`, `remcommission.gov.za`, `cogta.gov.za`, `statssa.gov.za`) are not added. The owner's separate decision of 25 November 2026 at 16:37 SAST, "First build: Joburg / Gazette 55749 only," is recorded on PR #15 and is not implemented in this change.

## POPIA

The 2022 Guide is an official public instrument. This change adds only the domain and a citation of the already-fetched file. It does not copy personal details, payment-account data, or entitlement figures into the site or the registry. Future use of the Guide should list entitlements as official provisions, not as a second personal cash total, and must not collect item-style personal fields.

## How to revert

Delete the branch, or leave a later PR unmerged. After a later merge: `git revert <merge commit>`; `main` returns to `75389ffbd8229f865e6c6d2768a77a7e85b56dd2`.

## Testing (evidence)

Recorded in the STATUS history row and the PR body draft (written outside the repo): `pytest`; `pwatch dq`; review kit on the committed head, including the agent-names-file variant.

## Approval

Push and merge need the owner's GO naming the exact head.
