# CHG-PW-007 — Draft profiles on the site, with a claim-level source check (Phase 0)

| Field | Value |
|---|---|
| Requested by / date (SAST) | Phase 0 hardening, relayed by Cavus on 19 Nov 2026. Audit `/workspace/cavus/phase0/phase0-audit-2026-11-19.md` (box): PoliticianWatch row 4 and finding B3 (a placeholder does not count; RFC §4 0b) |
| Author / builder | PoliticianWatch (Grok Bot) |
| Reviewers | Cavus; Janus |
| Change authority | Owner (GO on the exact head) |
| Type | Normal — high (publishes named people's profiles, including 6 adverse items, once deployed) |
| Environment | DEV (code, synthetic and real-data tests, local preview only). Nothing is published by this change. The first publish is CHG-PW-008's gated job, after the owner's GO. |
| CIs affected | CI-010 draft-site builder; CI-009 Joburg CV profiles (read only) |
| Linked records | CHG-PW-006 (site shell, DRAFT banner, privacy page; this branch is stacked on it); CHG-PW-008 (nightly build, live check, gated publish) |
| Branch | `politicianwatch-sa` `dev/chg-pw-007-profiles-site`, stacked on `dev/chg-pw-006-draft-privacy` at `8cf6c05`. No `politicianwatch-site` branch (see "Why no site-repo branch") |
| Pre-change commit (rollback SHA) | `8cf6c05c0aa63e4991d37a38f1f8e7d579ee6989` (CHG-PW-006 head); `main` `ba6fc8734d1961379776c76f9ca69f5fb4d0628f` |
| Head to approve | The tip of `dev/chg-pw-007-profiles-site`. Merge order: CHG-PW-006, then this change, then CHG-PW-008. |

## Request

Replace the "coming soon" placeholder with the real draft profiles rendered from `data/profiles/joburg-2026` (24 active, never `_hold/`). Every published claim shows its label and links to its source with a date; right-of-reply-pending items show "Right of reply: pending". Add a check that fails the build if any rendered claim lacks a source link.

## What changes

1. `pwatch/site_profiles.py` (new): the home page lists the 24 active profiles (name as gazetted, party, seat, and the seat source: Confirmed, Gazette 55741 link with page and date). One page per profile at `/profiles/<slug>/` with the same sections as the markdown render: seat, summary, CV, court matters, scandals and allegations, not yet known, and a method note on identity matching. Each claim is an `<li class="claim" data-fact data-label>` with a visible label badge; a non-Unknown claim shows `Source: <a class="src-link">host</a>, p.N, <time datetime>source date</time>; retrieved …`, plus every `also_sourced` link and date. Adverse items add status/outcome, the identity-link label, "Right of reply: <status>" (pending for all 6 today) and "Reply: (blank — no reply recorded)". Unknown fields show "Unknown — not yet found in an allowed source" with no link. The PR list rank is shown as a claim sourced to the gazette row (it is checked against the gazetted roster by `pwatch dq`). Only `http(s)` URLs become links.
2. `pwatch site check` gains the claim check on every page: each claim's label must be one of the five and be shown; each non-Unknown claim must have an `http(s)` source link and a `YYYY-MM-DD` source date; each adverse item must show a "Right of reply" line, and "Right of reply: pending" when its status is pending. With data (default; `--no-data` skips) it also checks coverage: every active profile has a page, every fact in it (`iter_facts`, PR rank, unknown fields) is rendered, and no held profile has a page. Exit 2 on any failure.
3. `pwatch site build` loads the active profiles by default (`load_profile_dir` skips `_hold/` and `on_hold`).
4. Tests: `tests/test_site_profiles.py` (15): synthetic build passes with coverage; every claim labelled and every non-Unknown claim sourced and dated; adverse item shows "Right of reply: pending" and a blank reply; every fact rendered; 7 broken-claim cases fail (link removed, date removed, badge removed, invalid label, RoR changed, RoR line removed, `javascript:` URL); coverage fails for a missing fact, a missing profile page and a held page; a fact with no source URL in the data fails the check; the real profiles build 24 pages, pass, never include the held profile, and show 6 "Right of reply: pending" items; CLI check exit codes.
5. README: the two `pwatch site` commands.

Built from the committed data on 19 Nov 2026: 27 HTML pages (home, privacy, 404, 24 profiles); 430 claims: Confirmed 181, Reported 95, Alleged 2, Disputed 1, Unknown 151; 6 adverse items, all "Right of reply: pending".

## What stays

Profile data, schema, DQ rules and markdown renders are unchanged. robots.txt `Disallow: /`, noindex meta, DRAFT banner and privacy page from CHG-PW-006. No publish, no site-repo change, no DNS or settings change.

## Why no site-repo branch

`GrokForum/politicianwatch-site` is a **public** repository. Pushing a branch with the built profiles would make the profiles (including 6 adverse items about 4 named councillors) public on GitHub before the owner's GO, and git history keeps them even after a revert. So the built profiles go to the site repo only through CHG-PW-008's publish job, which stays off until the owner flips it after his GO. Reviewers can read the build locally (`uv run pwatch site build --out _site`) or from the nightly job's private `site` artifact.

## Decisions for the owner before GO (not decided by the bot)

1. **Adverse items before right of reply is sent.** 6 adverse items (Zille 1, Gwamanda 2, Kunene 2, Mashaba 1) would be public with "Right of reply: pending", while their RoR drafts in `drafts/right-of-reply/` are unsent (the owner sends them personally). Publishing first and offering the reply later is the owner's call.
2. **Stale offices.** Positions such as "MMC for Transport (as described in September 2026)" are dated and labelled, but the 2026–2031 mayor and mayoral committee are expected around 19 Nov 2026. The profiles are not updated in this change.
3. **Permanence.** Once published, the site repo's public git history keeps every version. A take-down after publish needs a history rewrite of the public repo (an Emergency change).

## Risks

Medium to high on deploy (named people, adverse items); none until deploy. The claim check makes a missing link or date fail the build rather than ship.

## Testing (evidence)

At `ed73d48`: `uv run pytest -q` 83 passed (68 + 15); `uv run pwatch dq` exit 0; `uv run pwatch render --check` exit 0; `uv run pwatch site build --out <tmp>` + `uv run pwatch site check <tmp>` pass (24 profiles). popia-review on the built site: **PASS** — public-role facts of gazetted councillors only; the only e-mail is the role address; no phone, ID, home address, family or health data (the check's regex scan also passed on all 27 pages); no private persons.

## How to revert

Before merge: close the PR. After merge: `git revert -m 1 <merge commit>`. If the publish job has already published profiles: run CHG-PW-008's publish with the reverted builder (or revert the site repo's publish commit) — see that RFC.

## Approval

| Role | Name | Commit approved | Date | Result |
|---|---|---|---|---|
| Author | PoliticianWatch (Grok Bot) | | 2026-11-19 | Built |
| Reviewer | Cavus | | | |
| Reviewer | Janus | | | |
| Change authority | Owner | | | |
