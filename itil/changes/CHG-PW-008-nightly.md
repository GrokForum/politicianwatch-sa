# CHG-PW-008 — Nightly build, gated publish and live check (Phase 0)

| Field | Value |
|---|---|
| Requested by / date (SAST) | Phase 0 hardening, relayed by Cavus on 19 Nov 2026. Audit `/workspace/cavus/phase0/phase0-audit-2026-11-19.md` (box): PoliticianWatch row 5 and finding B2 (no nightly; streak 0); evidence pattern from H4 (one record per night) |
| Author / builder | PoliticianWatch (Grok Bot) |
| Reviewers | Cavus; Janus |
| Change authority | Owner (GO on the exact head; a **separate** GO to turn publishing on) |
| Type | Normal — high (publishing pipeline) |
| Environment | DEV (code, tests, `actionlint`). Merging adds a scheduled workflow to the private repo that builds, checks and records but **does not publish** (gate below). Turning publish on is the PROD step. |
| CIs affected | CI-012 nightly workflow (new); CI-013 `nightly-log` branch (new); CI-010 draft-site builder; CI-011 public site repo (written only by the publish job, when enabled) |
| Linked records | CHG-PW-006, CHG-PW-007 (this branch is stacked on CHG-PW-007); PublicFunds nightly (box routine ~03:20 SAST, check_live) as the model |
| Branch | `politicianwatch-sa` `dev/chg-pw-008-nightly`, stacked on `dev/chg-pw-007-profiles-site` at `678d370` |
| Pre-change commit (rollback SHA) | `678d3709a56e8cd92274d8fdf0e3f9a2279a08ba` (CHG-PW-007 head); `main` `ba6fc8734d1961379776c76f9ca69f5fb4d0628f` |
| Head to approve | The tip of `dev/chg-pw-008-nightly`. Merge order: CHG-PW-006, CHG-PW-007, then this change. |

## Request

A nightly build-and-publish job with a live check that verifies the deployed site responds and shows the expected draft content and labels, and saves its result each night where a reviewer can read it. Publishing stays gated until the owner's GO.

## Why GitHub Actions in the private repo

The site repo has no workflow (Pages "legacy" build from `main`). The build needs the private profile data, so the job runs in `politicianwatch-sa` (Actions enabled; default token read-only). PublicFunds uses a box routine instead; a routine would need the box up at 03:30 and a new routine record, and Actions keeps the evidence next to the code.

## What changes

1. `.github/workflows/nightly.yml` — triggers: `schedule` `30 1 * * *` (03:30 SAST) and `workflow_dispatch` (no inputs). Shell `bash -eo pipefail`. Actions pinned to commit SHAs (checkout v4.4.0, setup-python v5.6.0, upload-artifact v4.6.2, download-artifact v4.3.0; same pins as MediaWatch where shared).
   - **build:** `uv sync --frozen`; `pytest`; `pwatch dq` (exit 2 fails); `pwatch render --check`; `pwatch site build --out _site --commit $GITHUB_SHA`; `pwatch site check _site` (noindex, DRAFT, privacy, every claim labelled with a dated source link, coverage). Artifacts: `site` (7 days, private) and `build-evidence` (dq/site JSON, 90 days).
   - **publish (gated):** copies `_site` over `GrokForum/politicianwatch-site` `main` (keeps `CNAME` and `README.md`), commits "Nightly publish <build id> from politicianwatch-sa@<sha>" and pushes. Pages then deploys.
   - **live-check (always):** after a publish, waits up to 15 min for the live manifest to show tonight's build id, then runs `pwatch live-check`; writes `nightly/result.json`, adds a run summary, uploads artifact `nightly-<run id>` (90 days) and appends the record to `nightly/log.jsonl` (plus `nightly/<date>-<run id>.json`) on the orphan branch **`nightly-log`** of this private repo, never `main`. The job's last step fails the run if the night is red. Only this job has `contents: write`, for that branch.
2. `pwatch/live_check.py` + `pwatch live-check`: read-only GETs (0.25 s apart) of the live site. Checks: robots.txt exactly `Disallow: /`; `manifest.json` served, `status` draft, fresh (≤ 48 h); profile count equals tonight's build; after a publish, build id equals tonight's; profile pages listed; home, privacy and every page in the live manifest return 200 and pass the draft-page rules (noindex meta, DRAFT banner, privacy link, CSP, no script, PII scan) and the claim rules (label, `http(s)` source link, date, "Right of reply" line); privacy page gives `privacy@grokforum.site`; an unknown path returns 404 with the DRAFT page. **Green** only if the build succeeded, the publish did not fail and every live check passed. The record holds night (SAST), check time, build id, commit, profiles, DQ status/failures/warnings, publish flag and result, every check with detail, and the run link.
3. `scripts/record-nightly.sh`: the append to `nightly-log` (creates the orphan branch on first run; a failed lookup can only cause a rejected push, never an overwrite).
4. Tests (16): `tests/test_live_check.py` (9; a built site served through `httpx.MockTransport`, no network): good site all green with 26 pages checked; placeholder site red; broken robots and privacy red; a profile page without noindex or a source link red; stale (49 h) or wrong build id red (build id not compared when nothing was published); missing page must be the DRAFT 404; wait-for-build polling; verdict rules and JSONL append. `tests/test_nightly_workflow.py` (7): triggers are cron + manual only with no inputs; publish `if` needs the flag, `main` and a green build with no `||`; deploy-key step fails closed; only `publish` pushes to `main`; default permissions read-only and only `live-check` writes; build runs tests, dq, render, site build and check; live check always runs and records with 90-day retention; every action pinned to a 40-char SHA; the recorder appends two nights to a local bare repo's `nightly-log` branch and creates no other branch.

## How publishing is gated (exact)

The `publish` job runs only if **all** hold: (a) `needs.build.result == 'success'` (tests, dq, render check, site build and site check all passed tonight); (b) `github.ref == 'refs/heads/main'` (and a scheduled or manual workflow only exists once this file is on `main`, i.e. after the owner's merge GO); (c) repository variable **`PW_PUBLISH_ENABLED` is exactly `'true'`** — not set today. Then (d) the first step fails the job unless the repository secret **`PW_SITE_DEPLOY_KEY`** exists — not set today; the site repo has no deploy keys (checked 19 Nov 2026, read-only). A failed publish makes the night red.

**To turn publishing on (after the owner's quoted GO naming CHG-PW-008 and PROD):** add a write deploy key to `GrokForum/politicianwatch-site` and its private half as secret `PW_SITE_DEPLOY_KEY` in `politicianwatch-sa`; set variable `PW_PUBLISH_ENABLED=true`; optionally run the workflow once by hand. **To turn it off:** delete the variable (or set it to anything but `true`); the next night publishes nothing. Repo settings changes are owner actions.

Until then each night is expected to be **red**: the live site is the placeholder (no manifest, no profiles). That is correct for the Phase 0 streak, which starts at the first green night after publishing is on.

## What stays

No change to profile data, DQ rules, the builder output or the site repo. robots `Disallow: /`, noindex, DRAFT banner and privacy page unchanged. No DNS, Pages or certificate change.

## Not addressed here (recorded)

- HSTS (L1) and an `X-Robots-Tag` header: GitHub Pages cannot set headers (see CHG-PW-006).
- GitHub environment protection (required reviewer on the publish job): not used, because environments on private repositories need a paid plan; the variable + secret gate replaces it. It can be added if the plan allows.
- The nightly does not refresh source data (profiles are curated by hand and reviewed per change); "nightly" here means rebuild, re-check and re-verify the live site.

## Risks

Medium. After the flag is on, any merged change to profiles reaches the public site the same night; the gate is the merge GO plus the build checks. GitHub Actions minutes on a private repo (about 3–5 min a night). The publish rewrites the site repo's `main` from the build (no force-push; `CNAME`/README kept).

## Testing (evidence)

At `5f72395`: `uv run pytest -q` 99 passed (83 + 16); `uv run pwatch dq` exit 0; `uv run pwatch render --check` exit 0; `actionlint` 1.7.7 on the workflow: no findings (shellcheck not installed on the box, so embedded scripts were not shell-linted). `uv run pwatch live-check` against the real site on 19 Nov 2026 (read-only GETs): **red**, as expected — robots PASS; no manifest; home lacks DRAFT banner, CSP and privacy link; `/privacy/` 404; unknown path gives GitHub's plain 404. The workflow itself has not run (it can only run from `main`). popia-review: PASS (no personal data in code or records; the record holds check names, URLs of the site's own pages and counts).

## How to revert

Turn publishing off (delete `PW_PUBLISH_ENABLED`). Before merge: close the PR. After merge: `git revert -m 1 <merge commit>` removes the workflow (no more nightly runs). The `nightly-log` branch can stay as evidence. To undo a publish: revert the publish commit on the site repo (Pages redeploys) — content stays in public history (see CHG-PW-007).

## Approval

| Role | Name | Commit approved | Date | Result |
|---|---|---|---|---|
| Author | PoliticianWatch (Grok Bot) | | 2026-11-19 | Built |
| Reviewer | Cavus | | | |
| Reviewer | Janus | | | |
| Change authority | Owner (merge) | | | |
| Change authority | Owner (publish flag on, PROD) | | | |
