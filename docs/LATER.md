# LATER: parked ideas

**These are not planned work.** Nothing here has an RFC, an owner GO or a date. An idea leaves this list only through a named change record (it-project), and the owner may drop any of them. One line each.

- A website aggregating all four watch sites (a private Build project, not part of this repo).
- A national and provincial 2029 elections module (National Assembly and provincial legislatures), including the Parliament Register of Members' Interests and the PMG API — see `docs/national-2029-module.md` (CHG-PW-013 recorded the sources; no collector was added).
- Rollout beyond the Johannesburg pilot to all municipal councils (Gazette 55741 covers all municipalities; only Joburg profiles are built).
- A hosting RFC for HSTS and an `X-Robots-Tag: noindex` header (GitHub Pages cannot set response headers; audit L1, CHG-PW-006/008).
- Hashed-script CSP instead of any `'unsafe-inline'` (audit M4 pattern; the PW site currently has no scripts).
- 2026–2031 executive mayor, speaker, chief whip and MMC roles once the council's first sitting is confirmed by an allowed source. Checked 20 Nov 2026 (CHG-PW-013): the City's councillor, mayor/MMC and speaker directory pages returned HTTP 404; Municipal Money still exposes an officials cube (it will lag the election, and contact fields need a POPIA filter). Not guessed.
- Resolve the one held profile in `_hold/` (needs two identifying details from an allowed source).
- IEC reuse-terms enquiry (drafted only after an owner GO; risk RSK-008).
- Official contact channels for right-of-reply drafts ("[official channel, owner to confirm]").
- Owner placement decisions for tier-3 outlets (Briefly News, Rand Desk) and Scrutinize once it publishes.
- Required reviewers on the `site-publish` environment if the GitHub plan or repo visibility allows it (CHG-PW-008).
- A scheduled source-refresh check (today the nightly rebuilds and re-checks; it does not re-fetch sources).
- An automated link-rot check that flags claim source links that stop resolving.
- A reviewer-facing view of the `nightly-log` streak (green nights in a row).
- A dq flag for PI-bearing sources (e.g. a per-source flag that warns when a source is marked as carrying private or special personal information).
- Where the private withheld-sources register lives in the fresh public repository setup (it must not be carried into the public tree; a sidecar or owner-held store is still to be decided). CHG-PW-013 documents the fail-closed contract: a seed that does not carry `private/` must omit Withheld facts, or point `WITHHELD_SOURCES_PATH` at a sidecar.
- Enforcing the FRESH-REPO-PLAN do-not-carry list mechanically at seeding, rather than by a manual delete step.
- Tests for currently uncaught gates: the `check_pi_source_allowance` call in `pwatch/dq.py` (`check_profile`), and the `check_withheld_entry_format` call in `pwatch/dq.py` (`run`). (CHG-PW-013 added a test for the site-check rejection of a `private/` directory in built output.)
- Owner confirmation to add the CHG-PW-013 recorded domains (pmg.org.za, static.pmg.org.za, municipaldata.treasury.gov.za, parliament.gov.za, justice.gov.za, thepresidency.gov.za, sanews.gov.za if used) to `data/sources.json`.
