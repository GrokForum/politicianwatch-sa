# CHG-PW-019 — Watch network footer back-link

| Field | Value |
|---|---|
| Requested by / date (SAST) | Owner GO t812u on 28 November 2026, to add a footer back-link from every built page of this site to the Watch directory. Relayed by the orchestrator. That GO covers the DEV branch only. |
| Author / builder | author bot |
| Reviewers | two reviewers |
| Change authority | Owner (GO on the exact head to push or merge). Push and merge need a separate owner GO naming the exact head. |
| Type | Standard — low (footer chrome only; no profile facts, no indexing change) |
| Environment | DEV. The publish gate and `PW_PUBLISH_ENABLED` are unchanged. Nothing is deployed. Because nightly publish is already enabled, a later merge GO for this head must also cover the next nightly (or a same-day) publish to `politicianwatch-site`. |
| CIs affected | Site builder (`pwatch/site.py` `page()`), used by every built HTML page (home, privacy, 404, and profile pages). No workflow, CNAME, robots.txt or CSP change. |
| Linked records | Umbrella RFC-WATCH-BACKLINK (orchestrator draft, 28 November 2026). CHG-PW-017 is already on the base `origin/main`. PR #18 (CHG-PW-018) is awaiting merge and is not in this branch. |
| Branch | `politicianwatch-sa` `dev/chg-pw-019-watch-backlink`, from `origin/main` `a365913e6abc43e510135b97f1e18055ff8be8bf` |
| Pre-change commit (rollback SHA) | `a365913e6abc43e510135b97f1e18055ff8be8bf` (PR #17 squash on `main`; pre-merge tag `snapshot-2026-11-25-pre-pw-pr17` at `72d8f763311a7a1ace2b451860eeaebac5f93b3d`) |
| Numbering | Next free `CHG-PW` number after 018. `itil/changes` on `origin/main` has 001–017. 018 is taken by `dev/chg-pw-018-pdfminer-cve` (PR #18). No other `019` branch was present when this branch was created. |

## What changes

1. **`pwatch/site.py` `page()`.** After the existing footer paragraph (site name, Home, Privacy and corrections, optional build stamp), append one new paragraph:

   ```html
   <p><a href="https://watch.grokforum.site/">Part of the Watch network — watch.grokforum.site</a></p>
   ```

   Visible text is exactly that string, with a Unicode em dash (U+2014). The href is exactly `https://watch.grokforum.site/` (https, host only, trailing slash, no path, query or fragment). Plain `<a>`: no `target`, no `rel`, no tracking parameters. Existing footer wording is otherwise unchanged. Constants `WATCH_DIRECTORY_URL` and `WATCH_BACKLINK` hold the URL and the paragraph.

2. **`tests/test_site.py`.** `test_every_page_has_noindex_draft_banner_csp_and_privacy_link` now also requires that every built HTML page contains `href="https://watch.grokforum.site/"` and the exact footer paragraph. Existing noindex, DRAFT banner, CSP and privacy-link assertions stay.

3. **Records.** This RFC, STATUS, and the change log.

## What stays

noindex (`<meta name="robots" content="noindex, nofollow">`), `robots.txt` (`User-agent: *` / `Disallow: /`), the DRAFT banner, CSP, CNAME, DNS, Pages settings, workflows, the publish gate, profile data, collectors, and `politicianwatch-site`. No site output is committed.

## POPIA

Chrome only: a public link to the Watch directory. No personal details, new profile facts, or new sources are added.

## How to revert

On this branch, revert the implementation commit, or delete the branch and leave a later PR unmerged. After a later squash-merge: `git revert <squash commit>`; `main` returns to `a365913e6abc43e510135b97f1e18055ff8be8bf`.

## Testing (evidence)

Recorded in the STATUS history row and the PR body draft (written outside the repo):

- `uv run pytest -q`: 151 passed in 13.75s. The back-link assertions were added to an existing test, so the collected count is unchanged.
- `uv run pwatch dq`: pass (270 roster + 269 CV profiles, 1 on hold, 0 failures, 0 warnings, `as_of` 2026-11-28).
- `uv run pwatch render --check`: pass (exit 0).
- `uv run pwatch site build --out <temp> --commit <HEAD>` and `uv run pwatch site check <temp>`: pass. 272 HTML pages (home, privacy, 404, and 269 profiles); every page contained the exact href and the noindex meta; `robots.txt` was unchanged. The site output was not committed.
- `gitleaks detect --log-opts=--all --redact`, `actionlint` and `zizmor --offline` on `nightly.yml`: recorded in the PR body draft (workflow unchanged).
- Review kit on the committed head, including the agent-names-file variant.

## Seen, not touched

- STATUS and the change-log outcome for CHG-PW-017 still describe that RFC as awaiting a push GO, even though this branch is based on `origin/main` `a365913` (PR #17 squash of 25 Nov 2026 17:35:15 SAST). Those 017 records are left as they stand on `main`.
- PR #18 (CHG-PW-018, dependency pins) is awaiting merge. This branch does not include those pins. A rebase will be needed after it lands; this change does not wait for that merge.
- Indexing policy, robots, DRAFT banner copy, CSP, CNAME, DNS, Pages settings, workflows, and the publish gate.
- The `politicianwatch-site` repository (no publish as part of this change).
- The Watch directory itself (`GrokForum/watch-directory`).

## Approval

Owner GO t812u covers this DEV branch only. Push and merge need a separate owner GO naming the exact head.
