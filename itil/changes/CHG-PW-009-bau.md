# CHG-PW-009 — BAU housekeeping: path scrub, test name, nightly record and checkout hardening

| Field | Value |
|---|---|
| Requested by / date (SAST) | Relayed by the orchestrator on 19 Nov 2026 (16:16 SAST), after CHG-PW-008 was squash-merged |
| Author / builder | PoliticianWatch (Grok Bot) |
| Reviewers | reviewer (two reviewers) |
| Change authority | Owner (GO on the exact head) |
| Type | Standard — low (records wording, one test rename, two workflow hardening lines) |
| Environment | DEV. Nothing is published; the publish gate and `PW_PUBLISH_ENABLED` are unchanged (publishing stays off) |
| CIs affected | CI-012 nightly workflow; CI-008 working copy (register wording); records only otherwise |
| Branch | `politicianwatch-sa` `dev/chg-pw-009-bau`, from `origin/main` |
| Pre-change commit (rollback SHA) | `a0698d20022b8d1be2861c2a041978203b13a2b3` (`main` after the CHG-PW-008 squash merge; tag `snapshot-2026-11-19-pre-pw-pr8` is the state before that merge) |

## What changes

1. **Path scrub (records only).** Machine-local paths replaced with neutral wording in `itil/changes/CHG-PW-006-draft-privacy.md` (request row: "Phase 0 audit (19 Nov 2026)"), `itil/registers/ci-register.md` (CI-008: "DEV clone of `GrokForum/politicianwatch-sa` on the bot's machine") and `docs/adr/0001-stack-reuse-from-publicfunds.md` ("the PublicFunds repository"). A whole-tree grep (hidden files included) for `/workspace`, `/home/…`, `/cursor/stores`, `/tmp/` and `~/` now finds nothing. Older commits still contain such paths (history is not rewritten here; see the fresh-repo plan, CHG-PW-010).
2. **Test rename.** `test_default_permissions_read_only_and_only_live_check_writes` → `test_default_permissions_read_only_and_only_record_job_writes` (it asserts the default `contents: read` and that `record` is the only job with permissions, `contents: write`).
3. **`record` job only on `main`.** `if: ${{ always() && github.ref == 'refs/heads/main' }}`. Scheduled runs are on the default branch, so nightly records continue; a `workflow_dispatch` run from another branch no longer writes to `nightly-log`. Tests: `test_record_job_skips_runs_not_on_main`, and `test_record_job_is_the_only_nightly_log_writer` updated to the new condition.
4. **Build checkout drops the token.** `persist-credentials: false` on the `build` job's `actions/checkout` only. The `publish` job's checkout of the site repo is **unchanged**: it must keep the persisted deploy key because its later `git push origin HEAD:main` uses it. Test: `test_build_checkout_does_not_persist_but_publish_checkout_does` (with that reason as a comment). `zizmor` flags that checkout (`artipacked`, medium, low confidence); it is suppressed on that one line with an inline `zizmor: ignore[artipacked]` and a comment: the key is needed for the push, and the publish job uploads no artifacts.

## What stays

Profiles, DQ rules, the site builder, the publish gate (green build, `main` only, `PW_PUBLISH_ENABLED == 'true'`, environment `site-publish`, deploy-key secret), the live check and the recorder script. No site-repo change, no DNS, no publish.

## Seen, not touched

- `docs/adr/0001-stack-reuse-from-publicfunds.md` still lists the then-reviewers by name (accurate when the ADR was decided, 15 Nov 2026).
- Old commits on `main` and on the merged branches contain machine-local paths and the earlier commit identities; only a fresh repository removes them (CHG-PW-010 plan).

## Testing (evidence)

See the STATUS history row for this change: pytest, `pwatch dq`, `pwatch render --check`, `pwatch site build` + `site check`, `actionlint`, `zizmor`, and the review kit (output saved outside the repo and pasted into the PR body).

## How to revert

Before merge: close the PR / delete the branch. After merge: `git revert <merge commit>`; `main` returns to `33b3fb32` (CHG-PW-010).

## Approval

Plain PASS from both reviewers on the same head, then the owner's GO. Outcome: in review (PR #9; not merged).
