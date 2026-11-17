# ADR-0001: Reuse the PublicFunds (Thusa) stack for PoliticianWatch SA
- Status: Accepted (DEV scaffold; subject to reviewer PASS and owner GO on CHG-PW-001)
- Date (SAST): 2026-11-15
- Deciders: proposed in DEV for the owner; reviewers Cavus and Cassian

## Context
PoliticianWatch SA is a neutral, sourced public register of South African elected representatives. The planning packet asked that the stack and repository structure be modelled on PublicFunds (`/workspace/publicfunds`, Python package `thusa`): Python 3.13 + uv, DuckDB, httpx connectors with raw/`.sha256`/`manifest.jsonl` provenance, pdfplumber, a data-quality gate, an ITIL folder, ADRs, `REVIEW.md` and `AGENTS.md`.

The owner has already chosen City of Johannesburg (270 seats, 135 wards) as the pilot, and a private repository `GrokForum/politicianwatch-sa`.

## Decision
- New package name `pwatch` (the PublicFunds package name `thusa` stays with that project).
- Python 3.13, `uv` with a lockfile, DuckDB for a later warehouse, httpx with the same fetch policy (no workarounds for 401/403/WAF), pdfplumber for gazette PDFs, pytest.
- Immutable raw layer: `data/raw/<source>/<date>/<file>` plus sidecar `.sha256` and an append-only `manifest.jsonl`. Raw PDFs stay out of git; provenance files may be committed.
- Every public-role fact carries a label (`Confirmed`, `Reported`, `Alleged`, `Disputed`, `Unknown`) and, unless it is Unknown, a dated source URL. Missing values are JSON `null`, never silently filled.
- A DQ gate fails the build (exit 2) if a fact is missing a label or a required source, or if an adverse item breaks the right-of-reply rules.
- ITIL change, incident, CI and risk registers; change records under `itil/changes/`; `STATUS.md` at the repo root.
- Environments: DEV (synthetic fixtures), TEST (full pilot roster, not public), PROD (a future static public site). This change stays in DEV and writes a TEST roster; it does not create PROD.

## Consequences
- (+) Agents who already know PublicFunds can review this repo with the same instincts (provenance, nulls, DQ exit 2, RFC discipline).
- (+) Provenance and a checksummed raw layer make the gazette parse auditable.
- (−) The first release still needs a review app, a public snapshot and hosting ADRs; those are follow-ups, not part of CHG-PW-001.
- Follow-up: confirm IEC reuse terms (draft enquiry only, unsent until an owner GO).

## Alternatives considered
- Starting from a different language or web framework: rejected, to stay close to PublicFunds and the owner's operating model.
- Reusing the `thusa` package name: rejected, to keep the two projects distinct.
