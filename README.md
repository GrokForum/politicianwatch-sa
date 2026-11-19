# PoliticianWatch SA

A **neutral, sourced** public register of South African elected representatives. Every fact carries an evidence label (`Confirmed`, `Reported`, `Alleged`, `Disputed`, or `Unknown`) and, unless it is Unknown, a dated source URL. Missing values are explicit `null`s.

This repository is private. Nothing here is published until a named change is reviewed and the owner gives a GO.

**Pilot:** City of Johannesburg, 2026 local government elections — 270 seats, 135 wards. The executive mayor is **Unknown** (expected around 19 November 2026).

## Contents

| Path | What |
|---|---|
| `pwatch/` | Pipeline package: httpx fetcher, raw store, IEC/gazette connector, gazette parser, profile schema helpers, right-of-reply rules, DQ gate, DuckDB loader, CLI |
| `schemas/profile.schema.json` | Profile contract, including `right_of_reply` on adverse items |
| `data/roster/joburg-2026.csv` | TEST roster from Gazette 55741 (public office-holders, public-role fields only) |
| `data/raw/` | Provenance (`manifest.jsonl`, `.sha256`). Raw PDFs are gitignored |
| `data/profiles/joburg-2026/` | CV-style public-role profiles (CHG-PW-002), JSON plus generated markdown (`pwatch render`) |
| `drafts/right-of-reply/` | Unsent right-of-reply drafts. **The bot never sends these. The owner sends them personally.** |
| `docs/adr/` | Architecture decision records (ADR-0001: stack reuse from PublicFunds) |
| `docs/sources-joburg-lge-2026.md` | Gazette and IEC URLs, hashes, 270-row counts, ⚠ secondary-source discrepancies |
| `itil/` | Change enablement, CHG-PW-001, and the change, incident, CI and risk registers |
| `tests/` | pytest, synthetic fixtures only |
| `AGENTS.md`, `REVIEW.md`, `STATUS.md` | Agent rules, review checklist, change status |

## Running

```bash
uv sync                          # Python 3.13; pinned deps in uv.lock
uv run pytest -q                 # synthetic fixture tests
uv run pwatch dq                 # DQ gate on the Joburg roster and CV profiles (exit 2 = not releasable)
uv run pwatch render --check     # CV profile markdown renderings are current
uv run pwatch site build --out _site   # static draft site (24 active profiles, never _hold/); publishes nothing
uv run pwatch site check _site         # exit 2 if a page lacks noindex/DRAFT/privacy link, or a claim lacks a label, source link or date
uv run pwatch live-check --out r.json   # check the deployed site; one nightly record (exit 2 = red). Nightly: .github/workflows/nightly.yml (publish gated, see CHG-PW-008)
```

Exit code 2 means a data-quality check failed and the result is not releasable.

## Sources

Primary sources are the Electoral Commission and Government Gazette 55741 (13 November 2026). ElectionSePush may be linked; it must not be scraped. SAFLII must not be fetched automatically.

## Public role only

Profiles cover a person's public office. They must not include ID numbers, home addresses, personal phone numbers or emails, private family, or health information. A `popia-review` PASS is required before any publish.

## Right of reply

Every adverse item (a court or criminal matter, a scandal, or an allegation) carries a `right_of_reply` object. The default status is `pending`. The profile shows **Right of reply: pending** and a blank reply field until the owner records a send, a reply, or no response after the deadline. Drafts live in `drafts/right-of-reply/` and are never sent by the bot.

## Change process

DEV work happens on a branch. Cavus and Janus must each give a plain PASS on the **same exact head**. The owner then GOes that head before any merge, deploy, publish or outward message. Rollback is git. See `itil/change-enablement.md` and `itil/changes/CHG-PW-001-joburg-pilot-scaffold.md`.

## Status

See `STATUS.md`. CHG-PW-001 (PR #1) was merged into `main` as `3f3043a` on 17 Nov 2026 11:00 SAST.
