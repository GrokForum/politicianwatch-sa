# CHG-PW-006 — DRAFT label, privacy page and noindex test for the draft site (Phase 0)

| Field | Value |
|---|---|
| Requested by / date (SAST) | Phase 0 hardening, relayed by Cavus on 19 Nov 2026 (owner rule t371u: all four test sites must be rock-solid). Audit: `/workspace/cavus/phase0/phase0-audit-2026-11-19.md` (box), PoliticianWatch rows 2, 3, 7 and findings H2, M4, L2, L4 |
| Author / builder | PoliticianWatch (Grok Bot) |
| Reviewers | Cavus; Janus |
| Change authority | Owner (GO on the exact heads of both branches) |
| Type | Normal — high (public site content and POPIA wording on a hosted site) |
| Environment | DEV (code, synthetic tests, local preview). Merging the site branch **is** the PROD deploy (GitHub Pages "legacy" build from `main` /), so it needs the owner's GO. |
| CIs affected | CI-010 draft-site builder (new); CI-011 public site repo (new to the register) |
| Linked records | PublicFunds CHG-2026-067 (DRAFT banner, privacy page, role mailbox pattern); CHG-PW-007 (profiles on the site, stacked on this); CHG-PW-008 (nightly build, live check, gated publish, stacked on CHG-PW-007) |
| Branches | `politicianwatch-sa`: `dev/chg-pw-006-draft-privacy` from `main` `ba6fc8734d1961379776c76f9ca69f5fb4d0628f`. `politicianwatch-site`: `dev/chg-pw-006-draft-privacy` from `main` `8f00b8662365ab5e3ed34d3474575cf270638ee8` |
| Pre-change commits (rollback) | `politicianwatch-sa` `ba6fc8734d1961379776c76f9ca69f5fb4d0628f`; `politicianwatch-site` `8f00b8662365ab5e3ed34d3474575cf270638ee8` |
| Head to approve | The tips of both branches. Reviewers must PASS those exact heads. |

## Request

Phase 0 audit (19 Nov 2026): the live PoliticianWatch site is a "coming soon" page with no DRAFT label (row 2, H2), no privacy page or contact (row 3, H2), no CSP meta (M4) and a favicon 404 (L2). Cavus asked for a visible DRAFT label on every page and a privacy page with `privacy@grokforum.site` as the role contact, on the PublicFunds CHG-2026-067 pattern, keeping robots `Disallow: /` and `noindex` everywhere, with a test.

## What changes

`politicianwatch-sa` (builder, private):

1. `pwatch/site.py` + `pwatch/site_assets/` (CSS, SVG favicon): `build_site` writes a static site with no scripts. Every page has the robots `noindex, nofollow` meta, a meta CSP (`default-src 'none'; style-src 'self'; img-src 'self'; base-uri 'none'; form-action 'none'`), `referrer no-referrer`, a title starting `DRAFT ·`, a visible DRAFT banner linking to `/privacy/`, and a footer with the build id. It writes `robots.txt` (`User-agent: *` / `Disallow: /`), `404.html` (DRAFT, fixes Pages' default error page), `privacy/index.html`, `favicon.svg`, `assets/site.css`, `_config.yml` (keeps the repo README off the Jekyll site) and `manifest.json` (build id, SAST build time, source commit, page list, sha256 per file). The home page in this change is the labelled placeholder; CHG-PW-007 replaces it with the profiles.
2. Privacy page, modelled on CHG-2026-067 with PoliticianWatch wording: what the site is; **public role only**; sources and the five evidence labels; what it never shows (home addresses, ID numbers, personal phones and e-mails, private family members, health); allegations only from courts or established reporting, two-detail identity rule, "Right of reply: pending"; purpose and basis (marked **[legal wording unverified]**, as on PF); no cookies, analytics, trackers, forms or scripts; how to ask for a correction, reply or removal at `privacy@grokforum.site` (and not to send ID numbers, phones or addresses); retention (public version history); responsible party GrokForum; rights of access, correction and objection; Information Regulator link.
3. `pwatch site build --out DIR [--commit SHA]` and `pwatch site check DIR` (exit 2 on any failure). The check fails closed on: robots.txt not exact; a sitemap; no privacy page or no role contact on it; any page without the noindex meta, the CSP meta, the DRAFT banner, the `/privacy/` link or a `DRAFT` title; any `<script>`; any external resource; any e-mail other than the role address; text shaped like an SA phone number or a 13-digit ID; unexpected file types.
4. `tests/test_site.py` (15 tests): built site passes; robots exact and no sitemap; every page has noindex, DRAFT banner, CSP, privacy link, DRAFT title and no script; privacy wording and role contact; manifest and Jekyll config; the check fails for each of 8 broken-page cases and for a changed robots.txt or a sitemap; CLI build/check exit codes.
5. Housekeeping (Cavus, 19 Nov 2026): the CHG-PW-002 and CHG-PW-003 change-log rows say "reviewer" instead of naming agents. Reviewer roster in `itil/change-enablement.md`, the change-request template, AGENTS.md rule 8, README and the PR template: Cavus and Janus (Cassian reviewed CHG-PW-001 to 005 and is no longer involved). This roster change was relayed by Cavus, not stated by the owner in this chat; the owner's GO on this RFC confirms it.

`politicianwatch-site` (public): the output of `pwatch site build` at `politicianwatch-sa` `00b7510` (the coming-soon page with the DRAFT banner, privacy page, 404, favicon, CSS, `_config.yml`, `manifest.json`); `robots.txt` and `CNAME` unchanged; three README lines saying the pages are generated and giving the role contact.

## What stays

robots.txt `Disallow: /`; noindex on every page; custom domain and Pages settings; no profile content on the public site (that is CHG-PW-007, and only after the owner's GO). No DNS, settings, HSTS or certificate change.

## Not possible on this host (recorded, not hidden)

- **noindex response header (`X-Robots-Tag`) and HSTS (L1):** GitHub Pages does not let a repository set response headers. The controls are robots.txt plus the per-page meta, and a test enforces both. Adding headers needs a different host or a CDN in front, which is a hosting/DNS change for a separate RFC and an owner GO.
- **CSP `frame-ancestors`:** ignored in a meta CSP, so not set.

## Risks

Low to medium. The privacy wording is a public statement: the lawful-basis line is marked "[legal wording unverified]" like PF's. `privacy@grokforum.site` is the role mailbox already used by PublicFunds (audit: MX present); someone must read it. A merge of the site branch deploys within minutes.

## Testing (evidence)

At `politicianwatch-sa` `00b7510`: `uv run pytest -q` 68 passed (53 before + 15 new); `uv run pwatch dq` exit 0; `uv run pwatch render --check` exit 0; `uv run pwatch site check` on the site branch working tree: pass. popia-review on both diffs: **PASS** — the only address is the role mailbox `privacy@grokforum.site`; no names of private people, no IDs, phones, addresses or keys.

## How to revert

Before merge: close the PRs. After merge: `git revert -m 1 <merge commit>` on each repo (site first; Pages redeploys the placeholder at `8f00b86`'s content). Tags to set by whoever merges: `snapshot-2026-11-19-pre-pw-chg006` on each repo's pre-merge `main`.

## Approval

| Role | Name | Commit approved | Date | Result |
|---|---|---|---|---|
| Author | PoliticianWatch (Grok Bot) | | 2026-11-19 | Built |
| Reviewer | Cavus | | | |
| Reviewer | Janus | | | |
| Change authority | Owner | | | |
