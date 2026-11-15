# CHG-PW-001 — Scaffold PoliticianWatch SA and the Johannesburg LGE 2026 roster

| Field | Value |
|---|---|
| Requested by / date (SAST) | Cavus (Grok Bot), 15 November 2026 |
| Type | Normal — medium (new repo scaffold and a TEST roster of public office-holders; no PROD, no publish, no outward message) |
| Environment | DEV (code, synthetic tests). TEST roster committed from a public gazette. Not PROD. |
| CIs affected | New repo `GrokForum/politicianwatch-sa`; CI-001 schema; CI-002 gazette source; CI-003 IEC results source; CI-004 DQ gate; CI-005 right-of-reply drafts |
| Linked records | ADR-0001; docs/sources-joburg-lge-2026.md |
| Branch | `dev/chg-pw-001-scaffold` |
| Pre-change commit (rollback SHA) | `cfa7e22ff4fc7b12e2e891d1855e17ad261dcd84` (initial `main`: README + .gitignore only) |
| Head to approve | the tip of `dev/chg-pw-001-scaffold` after this change is committed; reviewers must PASS that exact head |

## Request

Create the PoliticianWatch SA repository scaffold, modelled on PublicFunds (package `thusa`), and load a City of Johannesburg councillor roster for LGE 2026 from Government Gazette 55741, cross-checked against the IEC seat-calculation PDF. Include the profile JSON schema, an IEC/gazette connector with provenance, a DQ gate, right-of-reply rules and an unsent draft template, ITIL registers, ADR-0001, and pytest coverage on synthetic fixtures.

This is a draft change only. It does not merge to `main`, does not publish a site, does not change a domain, and does not contact the IEC, councillors, ElectionSePush, the Municipal Demarcation Board, or anyone else.

## Reasons

- The owner has chosen **City of Johannesburg** (270 seats, 135 wards) as the pilot, and the private repository `GrokForum/politicianwatch-sa` already exists and was empty.
- Gazette 55741 (13 November 2026) is the canonical public list of declared councillors. Councillors are public office-holders named in that gazette, so the roster is committed (public-role fields only).
- A reusable stack (Python 3.13 + uv, DuckDB, httpx, raw checksums, pdfplumber, DQ exit 2, ITIL, ADRs) lets later profile research proceed under the same rules as PublicFunds.
- Right-of-reply rules need to be in the schema and the gate **before** any adverse item is researched, so a later CV pass cannot publish a court matter or allegation without a draft and an owner-recorded status.

## What changes

- Repository scaffold: `README.md`, `AGENTS.md`, `REVIEW.md`, `STATUS.md`, `pyproject.toml`, package `pwatch`, tests, `schemas/profile.schema.json`, `config/sources.yaml`.
- ADR-0001 (stack reuse) and ITIL registers (change, incident, CI, risk) plus this change record.
- IEC/gazette connector skeleton with `data/raw/` provenance. Raw PDFs stay gitignored; `manifest.jsonl` and `.sha256` sidecars are committed.
- TEST roster `data/roster/joburg-2026.csv` (270 rows: name, party, seat type, ward number, gazette URL, source page) plus Unknown/empty placeholders for education, career, positions, court matters and scandals. Executive mayor recorded as Unknown in `data/roster/joburg-2026-council.json`.
- Right-of-reply: schema object, DQ rules, `drafts/right-of-reply/TEMPLATE.md`, and a standing rule that the bot never sends a draft. The owner sends personally. Status stays `pending` until the owner records `sent_at`, a reply, or `no_response` after the deadline.

## What stays

- `main` is not updated by this change (beyond the already-local initial commit, which must not be pushed until the owner GOes that step).
- No public site, no domain, no hosting, no review app, no CV research, no contact with third parties.
- ElectionSePush is link-only. SAFLII is not fetched automatically.

## Risks

- **OCR error on a gazetted name or party** (the PDF is a scanned capture). Mitigated by page-level citations, a full 270-row count, ward 1–135 completeness, and an exact match to official IEC party seat totals. Residual spelling risk remains; it is recorded in the source notes.
- **Secondary sources disagree** on ANC (64 official vs 63) and ActionSA (42 official vs 43). Mitigated by using only the gazette and the IEC PDF. Documented as ⚠ in `docs/sources-joburg-lge-2026.md`.
- **POPIA / over-collection.** The roster contains public-role names only. No ID numbers, home addresses, personal phones or emails, family or health information. Candidate-ID reports were not downloaded.
- **Defamation.** No adverse items are in the roster. RoR rules are in place before any such item is added. Four-eyes (Cavus and Cassian) plus an owner GO are required before a negative item is published, in a later change.
- **Licence / reuse terms** for IEC files are not yet confirmed. The files used are official public records. A drafted enquiry is out of scope until the owner GOes sending it.
- **Blast radius:** private repo and local box only. Nothing is public.

## Right of reply (this change)

- Every adverse item (court or criminal matter, scandal, allegation) must carry a `right_of_reply` object: `status` (pending / sent / replied / no_response), `draft_path`, `deadline`, `sent_at` (null until the owner records a send), `reply_text` (null; a blank field on the profile), `recorded_by` (owner only).
- Default status is `pending`. A profile must show "Right of reply: pending" with a blank reply field.
- The DQ gate fails if an adverse item has no `right_of_reply`, has no draft, or is in status `sent` / `replied` / `no_response` without the matching owner-recorded fields. `no_response` is only allowed after the deadline.
- Drafts live in `drafts/right-of-reply/` and are **never sent by the bot**. The owner sends them personally.

## Testing (evidence, not claims)

- [x] `uv run pytest -q`: **20 passed** in 0.17s (parser, mock-HTTP connector and provenance, DQ label/source rules, RoR rules, DuckDB load). Synthetic fixtures only.
- [x] `uv run pwatch dq` on the committed Joburg roster: **pass**, 270 profiles, 0 failures, exit 0 (15 November 2026). Gazette parse: 270 rows, 135 unique wards 1–135, 135 PR, party totals identical to the IEC seat-calculation PDF. Notes in `docs/sources-joburg-lge-2026.md`.
- [x] POPIA scan of the git-visible tree and of the Joburg gazette lines: no ID numbers, personal phones, personal emails, or home addresses. Hits were documentation prohibitions only ("never include personal phone…"). Verdict: **PASS**. Public office-holder names and official ward identifiers (`79800nnn`) are public-role data from the gazette.

## Implementation plan

1. Local initial commit on `main` (README + `.gitignore` only), recorded as the rollback SHA above. Not pushed until the owner GOes it.
2. Work on `dev/chg-pw-001-scaffold`. Commit the scaffold, schema, tests, provenance, roster and this record.
3. Run pytest and the POPIA check.
4. Stop. Reviewers Cavus and Cassian each give a plain PASS on the **same exact head**. `PASS_WITH_CONCERNS` does not count.
5. Owner GO (quoted words, naming this RFC and the exact head) before any push, draft PR, merge, publish or outward message.

## How to revert

Rollback is git. If this branch has not been merged, delete the local branch or reset it to `cfa7e22ff4fc7b12e2e891d1855e17ad261dcd84`. If a later merge to `main` is authorised, revert that merge commit. Raw PDFs in `data/raw/` are gitignored and can be deleted without affecting git history. The committed roster is a data file: reverting the merge removes it from `main`.

## Approval

Reviewers must give a plain PASS on the same exact head. The owner then GOes (or not) that head and this RFC.

| Role | Name | Commit approved | Date | Result |
|---|---|---|---|---|
| Author | Cavus (Grok Bot) | | 2026-11-15 | drafted |
| Reviewer | Cavus | | | pending PASS on the exact head |
| Reviewer | Cassian (Build, review only) | | | pending PASS on the exact head |
| Change authority | Owner | | | pending GO |

## Post-implementation review

- Outcome: pending reviews and owner GO. Not merged. Not published.
- Follow-ups: IEC CSV / reuse-terms enquiry (draft only, unsent); mayor and mayoral committee after the first sitting; CV research under a later RFC; public site ADRs.

## Seen, not touched

- Domain and hosting decisions, the PublicFunds review-app port, People's Assembly / PMG / MDB ingestion, SAFLII lookups, any contact with councillors, ElectionSePush embedding, and all non-Joburg councils.
