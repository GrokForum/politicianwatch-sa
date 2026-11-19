# LATER: parked ideas

**These are not planned work.** Nothing here has an RFC, an owner GO or a date. An idea leaves this list only through a named change record (it-project), and the owner may drop any of them. One line each.

- A website aggregating all four watch sites (a private Build project, not part of this repo).
- A national and provincial 2029 elections module (National Assembly and provincial legislatures).
- Rollout beyond the Johannesburg pilot to all municipal councils.
- A hosting RFC for HSTS and an `X-Robots-Tag: noindex` header (GitHub Pages cannot set response headers; audit L1, CHG-PW-006/008).
- Hashed-script CSP instead of any `'unsafe-inline'` (audit M4 pattern; the PW site currently has no scripts).
- 2026–2031 executive mayor, speaker, chief whip and MMC roles once the council's first sitting is confirmed by an allowed source.
- CV profiles for the remaining Joburg councillors (24 active of 270 today), batch by batch.
- Resolve the one held profile in `_hold/` (needs two identifying details from an allowed source).
- IEC reuse-terms enquiry (drafted only after an owner GO; risk RSK-008).
- Official contact channels for right-of-reply drafts ("[official channel, owner to confirm]").
- Owner placement decisions for tier-3 outlets (Briefly News, Rand Desk) and Scrutinize once it publishes.
- Required reviewers on the `site-publish` environment if the GitHub plan or repo visibility allows it (CHG-PW-008).
- A scheduled source-refresh check (today the nightly rebuilds and re-checks; it does not re-fetch sources).
- An automated link-rot check that flags claim source links that stop resolving.
- A reviewer-facing view of the `nightly-log` streak (green nights in a row).
- A dq flag for PI-bearing sources (e.g. a per-source flag that warns when a source is marked as carrying private or special personal information).
- Where the private withheld-sources register lives in the fresh public repository setup (it must not be carried into the public tree; a sidecar or owner-held store is still to be decided).
- Enforcing the FRESH-REPO-PLAN do-not-carry list mechanically at seeding, rather than by a manual delete step.
- Tests for currently uncaught gates: the `check_pi_source_allowance` call in `pwatch/dq.py` (`check_profile`), the `check_withheld_entry_format` call in `pwatch/dq.py` (`run`), and the site-check rejection of a `private/` directory in built output.
