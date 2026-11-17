# STATUS (as of 17 November 2026, SAST)

## Current

- Private repository `GrokForum/politicianwatch-sa`. No public site. No domain in use. No outward messages have been sent.
- `main` at `cfa7e22ff4fc7b12e2e891d1855e17ad261dcd84` (README + `.gitignore`) and branch `dev/chg-pw-001-scaffold` were pushed on the owner's GO, 15 November 2026 18:32 SAST.
- CHG-PW-001 (DEV scaffold + TEST Joburg roster) is open as draft PR #1 (https://github.com/GrokForum/politicianwatch-sa/pull/1). Nothing is merged. Awaiting a plain PASS from Cavus and from Cassian on the same exact head, then an owner GO before any merge or publish.
- Rollback SHA: `cfa7e22ff4fc7b12e2e891d1855e17ad261dcd84`.
- Pilot council: City of Johannesburg (270 seats, 135 wards). Executive mayor: Unknown (expected around 19 November 2026).
- Adverse items in the roster: none. Right-of-reply rules are in the schema and the DQ gate for later work.
- CHG-PW-002 (first 10 CV profiles, DEV/TEST) is on branch `dev/chg-pw-002-first-profiles` (PR #2, draft), branched from `ed801b1`. Not merged, not published. See the PR for the current head. 6 adverse items, all "Right of reply: pending"; 10 drafts in `drafts/right-of-reply/CHG-PW-002/`, none sent. Awaiting a plain PASS from Cavus and from Cassian on the same exact head, then an owner GO.
- CHG-PW-003 (batch 2, plus PR #2 review nits; DEV/TEST) is committed **locally** on `dev/chg-pw-003-batch-2`, stacked on the CHG-PW-002 branch. After Cassian's blind source check (fix 1): **14 active profiles (9 ward / 5 PR)**, 1 on hold (Mbatha, in `data/profiles/joburg-2026/_hold/`). No adverse items; 14 optional accuracy-check drafts in `drafts/right-of-reply/CHG-PW-003/` (+1 in `_hold/`), none sent. Not pushed, not merged, not published. Awaiting two plain PASS reviews on the same head and an owner GO.
- PROD: not created. Gate locked.

## History

| Date (SAST) | RFC | Env | Result | Rollback SHA |
|---|---|---|---|---|
| 2026-11-15 | CHG-PW-001 | DEV + TEST roster | Drafted locally; tests and POPIA check to be recorded on the branch head; not pushed | cfa7e22ff4fc7b12e2e891d1855e17ad261dcd84 |
| 2026-11-15 | CHG-PW-002 | DEV + TEST profiles | 10 CV profiles + 10 unsent drafts; pytest 29 passed; `pwatch dq` pass (270 + 10); popia-review PASS; first commit | ed801b102d286d4a6ee8bd781e72f4168f722288 |
| 2026-11-17 | CHG-PW-002 | DEV + TEST profiles | Review round 2 fixes (Cavus + Cassian PASS_WITH_CONCERNS on `c352484`): identity-link label on adverse items (Zille item now Reported), Kunene status `reported_conviction`, status wording; pytest 34 passed; `pwatch dq` pass; render check pass; popia-review PASS. Branch with PR #2 (draft); not merged | ed801b102d286d4a6ee8bd781e72f4168f722288 |
| 2026-11-17 | CHG-PW-003 | DEV + TEST profiles | Nits commit + 15 batch-2 profiles + 15 unsent optional drafts; pytest 35 passed; `pwatch dq` pass (270 + 25); render check pass; popia-review PASS; committed locally | 4a341fedb1c0287b1e7a748d9b2163198b69544e |
| 2026-11-17 | CHG-PW-003 | DEV + TEST profiles | Fix 1 (Cassian blind source check on `159542e`): Mbatha on hold (`_hold/`, excluded from dq/render; test added); first-year-in-council facts for Schay, Chame, Makhafola (Magwentshu re-verified); Steenkamp second detail checked, kept; pytest 36 passed; `pwatch dq` pass (270 + 24, 1 on hold); render check pass; popia-review PASS; committed locally | 159542e1e2bc94e767a1ea48e047733089019c6f |
