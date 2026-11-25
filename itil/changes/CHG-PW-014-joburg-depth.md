# CHG-PW-014 — Joburg depth: 2026–2031 council offices re-check

| Field | Value |
|---|---|
| Requested by / date (SAST) | Owner resumed all work, relayed by the orchestrator on 21 November 2026 at 07:54 SAST: leave PR #13 at `5b3c5e5c`, continue toward the next milestone on a new branch, keep it lean. After PR #13 was squash-merged into `main` as `7c741222` (21 Nov 2026 12:47 SAST; verified on GitHub 25 Nov 2026), the orchestrator asked for this change to be moved onto `main`. |
| Author / builder | author bot |
| Reviewers | two reviewers |
| Change authority | Owner (GO on the exact head to push or merge). Push and merge need the owner's GO naming the exact head. |
| Type | Standard — low (records a negative official-source check; no profile facts added) |
| Environment | DEV (docs and records). Publishes nothing: the publish gate and `PW_PUBLISH_ENABLED` are unchanged, and no push, merge or deploy is made here. |
| CIs affected | Records only (Joburg source notes, allowed-sources check log, ROADMAP wording). No profile, roster, collector, workflow or site-builder change. |
| Linked records | CHG-PW-013 (next milestone; [PR #13](https://github.com/GrokForum/politicianwatch-sa/pull/13) squash-merged as `7c741222`); `docs/ROADMAP.md` item 1 (Joburg depth — council offices) |
| Branch | `politicianwatch-sa` `dev/chg-pw-014-joburg-depth-main`, from `origin/main` `7c74122234106ce759ee4cefc0562b0fb4554895` (PR #13 squash). The earlier branch `dev/chg-pw-014-joburg-depth` at `7625e757374fc23dfdbea58e3ca45d18aa748c13` (cut from `5b3c5e5c`) is left as-is and is not the review branch. |
| Pre-change commit (rollback SHA) | `7c74122234106ce759ee4cefc0562b0fb4554895` (PR #13 squash on `main`) |

## What changes

1. **Council offices re-check (21 November 2026, SAST).** Whether the City of Johannesburg, or another source already in `data/sources.json` / `docs/allowed-sources.md`, had published the 2026–2031 executive mayor, speaker, chief whip and mayoral committee. The finding is that they have not. No office was guessed, and no position was added to any profile.
2. **Records.** This RFC, STATUS, the change log, `docs/sources-joburg-lge-2026.md`, the City pages note in `docs/allowed-sources.md`, and the council-offices bullet in `docs/ROADMAP.md` are updated with the date, the URLs checked, and the City's own statement that information on the new Council will be published once it has been formally constituted.

## What stays

PR #13, already squash-merged into `main` as `7c741222`. All 269 active CV profiles and the one held profile. The gazette roster. `data/sources.json`. The publish gate and `PW_PUBLISH_ENABLED`. Right-of-reply drafts (unsent). ElectionSePush (link-only, not fetched). SAFLII (by hand only). No contact with councillors. City pages were not re-fetched on 25 Nov 2026.

## Office check (21 November 2026, SAST)

Checked in the morning of 21 November 2026 (Africa/Johannesburg). Fetches were limited (about 16 official GETs, including a few repeat reads of the same homepage and media landing pages). No TLS or certificate errors were observed. News outlets were not fetched (budget; official sources already said the new Council had not been published). Municipal Money was not re-fetched (checked 20 Nov 2026 in CHG-PW-013; it was expected to lag the 4 Nov 2026 election, and the payload can carry contact fields).

| URL | HTTP | Result |
|---|---|---|
| `https://www.joburg.org.za/about_/Pages/Councillors.aspx` | 404 | Still unpublished (same path as 20 Nov 2026). |
| `https://www.joburg.org.za/about_/Pages/Executive-Mayor-and-Mayoral-Committee.aspx` | 404 | Still unpublished (same path as 20 Nov 2026). |
| `https://www.joburg.org.za/about_/Pages/Office-of-the-Speaker.aspx` | 404 | Still unpublished (same path as 20 Nov 2026). |
| `https://www.joburg.org.za/about_/Pages/default.aspx` | 404 | Still unpublished (same path as 20 Nov 2026). |
| `https://www.joburg.org.za/` (redirects to `https://joburg.org.za/Pages/homepage.aspx`) | 200 | City of Johannesburg homepage. Featured 2026 news items were operational (water restrictions, accessibility, Joburg Market, City Power, a trainee story). No mention of an executive mayor, speaker, chief whip or mayoral committee for 2026–2031. |
| `https://joburg.org.za/media_/` | 200 | Media landing. The only "executive mayor" wording found was historical (State of the City Address by former Executive Mayor Herman Mashaba). No 2026–2031 office announcement. |
| `https://www.joburg.org.za/media_/Pages/Media.aspx` | 404 | Not used. |
| `https://www.joburg.org.za/media_/Pages/Media/Media%20Statements/default.aspx` | 404 | Not used. |
| `https://www.joburg.org.za/media_/Pages/Media/Newsroom.aspx` | 404 | Not used. |
| `https://joburg.org.za/about_/government/Pages/Council/Council.aspx` | 200 | Title: Legislature. The page states, in substance: it reflects the previous Legislature of the City of Johannesburg, including the former Speaker of Council, Chief Whip, Councillors and Section 79 Committees; that Council term has concluded and those office-bearers are no longer in office; **information on the new Council will be published once it has been formally constituted.** Links to Speaker of Council and The Chief Whip subpages were not followed, because the parent page says those pages still describe the previous term. |
| `https://joburg.org.za/media_/Newsroom/Pages/default.aspx` | 200 | News articles home. No mention of executive mayor, speaker, chief whip, mayoral committee, first sitting or inauguration. |
| `https://joburg.org.za/media_/Newsroom/Pages/Newsroom.aspx` | 200 | Newsroom index, with a link to 2026 news stories. No mention of the 2026–2031 offices on this page. Individual 2026 article bodies were not fetched (homepage already listed the featured items, none of which were office announcements). |
| `https://joburg.org.za/media_/MediaStatements/Pages/default.aspx` | 200 | Media Statements index. Visible year folders ran from 2004 through 2018 only. No 2026 statements folder and no office-holder announcement on this page. |

**Finding:** the 2026–2031 executive mayor, speaker, chief whip and mayoral committee have not been published by the City. Offices stay Unknown. Not guessed.

## POPIA

- Public-role check only. No profile fact was added, so no new personal information was written into a CV.
- A "List of Councillors" link on the Council page pointed at a contact-details PDF. That file was **not fetched**.
- The 2024/25 Councillors Declaration of Interests PDF (previous term) was **not fetched**.
- Site footers on some City pages include general and emergency phone numbers. Those values were **not recorded** in this repository, this RFC, or the source notes.
- Nothing was written to `private/withheld-sources.json`. Nothing is Withheld (POPIA) in this change.

## Risks

Low. Docs and records only. The risk of treating a previous-term office-bearer as a 2026–2031 holder was avoided by not following the Speaker and Chief Whip subpages after the parent page labelled them as the previous legislature.

## Seen, not touched

- Filling remaining Unknown CV fields on gazette-only stubs (ROADMAP item 1). Scoped as "only if step 1 is quick, at most 5 stubs". Step 1 used the fetch budget on the official office check and found nothing to add, so stub research was not started.
- The 269 profile `unknown_fields` strings that still say the first sitting was "expected around 19 November 2026". Left as written at the time; the current official position is in this RFC and the source notes.
- Right-of-reply states (six items still pending; drafts stay unsent).
- The held profile.
- Municipal Money officials cube (not re-fetched; POPIA filter still required if it is used later).
- PR #13 is already on `main` as `7c741222`; no further #13 review-round work is in this change.
- `_site/` is not in `.gitignore`. A local build was used for `site check` and then deleted; it is not committed, and the gitignore was not changed here.


## Testing (evidence)

Recorded in the STATUS history row and the PR body draft: `uv run pytest -q` (151 passed) at the head on `dev/chg-pw-014-joburg-depth-main`; `uv run pwatch dq` pass (270 roster + 269 CV profiles, 1 on hold, 0 failures, 0 warnings, `as_of` 2026-11-25); `uv run pwatch render --check` pass; `uv run pwatch site build --out _site` + `pwatch site check _site` pass (269 profiles). The `_site` directory was deleted after the check and is not committed. Review kit output is saved outside the repo and pasted into the PR body draft outside the repo (box paths stripped). No workflow file is changed, so actionlint / zizmor are not re-run as a separate step.

## How to revert

Before any merge: leave the branch off origin, or delete it. After a later merge: `git revert <merge commit>`; `main` returns to the then-current parent (this change is stacked on `7c74122234106ce759ee4cefc0562b0fb4554895`).

## Result

SUCCEEDED in DEV (tests and records). No profile facts were added. The 2026–2031 council offices remain Unknown. Push and merge need the owner's GO naming the exact head.


## Review round (after critic PASS_WITH_CONCERNS on `da3d07eb`)

1. `itil/changes/CHG-PW-013-next-milestone.md` change-authority and Approval lines now end with a closure: squash-merged as `7c741222` on 21 Nov 2026 12:47 SAST (commit date of `7c741222`; `gh pr view 13 --json mergedAt` is empty). The dated follow-up history in that RFC is unchanged.
2. The 19 Nov 2026 CHG-PW-006 STATUS history row uses the role word "critic" in place of the agent name.

## Approval

Pending review and the owner's GO on the exact head before any push or merge.
