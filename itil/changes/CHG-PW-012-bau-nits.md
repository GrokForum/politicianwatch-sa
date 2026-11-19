# CHG-PW-012 — BAU nits after CHG-PW-009 merged

| Field | Value |
|---|---|
| Requested by / date (SAST) | Relayed by the orchestrator on 19 Nov 2026 (16:44 SAST), after CHG-PW-009 was squash-merged into `main` as `ce45d829` |
| Author / builder | author bot |
| Reviewers | two reviewers |
| Change authority | Owner (GO on the exact head) |
| Type | Standard — low (records wording and one test widening) |
| Environment | DEV. Nothing is published; the publish gate and `PW_PUBLISH_ENABLED` are unchanged (publishing stays off) |
| CIs affected | CI-012 nightly workflow (test only); records and the fresh-repo plan wording otherwise |
| Branch | `politicianwatch-sa` `dev/chg-pw-012-bau-nits`, from `origin/main` |
| Pre-change commit (rollback SHA) | `ce45d829dafcf5b86e2db142fea64335bb3dc611` (`main` after the CHG-PW-009 squash merge; tag `snapshot-2026-11-19-pre-pw-pr9` is the state before that merge) |

## What changes

1. **STATUS.md (CHG-PW-010 history row).** The 010 row now says "zizmor found 2 medium" (it previously said "1 medium finding on the unchanged publish checkout").
2. **`docs/FRESH-REPO-PLAN.md` (do-not-carry-over row for box paths).** The stale "this change, landing now" wording is replaced: seed from a `main` that includes CHG-PW-009, merged as `ce45d829`.
3. **`itil/changes/CHG-PW-009-bau.md` lines 6–7.** Role words only: Author / builder is "author bot"; Reviewers is "two reviewers".
4. **`tests/test_nightly_workflow.py`.** The publish-job no-upload test now fails for any step whose `uses` contains "upload", matched case-insensitively (not only `actions/upload-artifact`). A helper and a unit test pin that a step such as `Actions/Upload-Artifact@v4` is caught. Before commit, that string was inserted as a temporary publish step; `test_publish_job_does_not_upload_artifacts` failed on it; the workflow was then reverted and is unchanged in this change.

## What stays

Profiles, DQ rules, the site builder, the nightly workflow itself, the publish gate (green build, `main` only, `PW_PUBLISH_ENABLED == 'true'`, environment `site-publish`, deploy-key secret), the live check and the recorder script. No site-repo change, no DNS, no publish.

## Seen, not touched

- The live-check job still uploads a 90-day artifact with `actions/upload-artifact`; that job does not hold the deploy key. Only the publish job is guarded.
- PR bodies from earlier changes may still contain box paths in pasted kit output; this change does not rewrite them. New kit pastes strip those paths.
- The 010 row's other wording (pytest 107, and so on) is left as the record of that change.

## Testing (evidence)

See the STATUS history row for this change: pytest, `pwatch dq`, `pwatch render --check`, `pwatch site build` + `site check`, `actionlint`, and the review kit (output saved outside the repo and pasted into the PR body). The temporary `Actions/Upload-Artifact@v4` step made `test_publish_job_does_not_upload_artifacts` fail; after reverting `.github/workflows/nightly.yml` the test passed, and the workflow diff was empty.

## How to revert

Before merge: delete the branch. After merge: `git revert <merge commit>`; `main` returns to `ce45d829` (CHG-PW-009).

## Approval

Plain PASS from both reviewers on the same head, then the owner's GO to merge (or the standing BAU GO if the orchestrator applies it). Outcome: pending (not merged, not pushed).
