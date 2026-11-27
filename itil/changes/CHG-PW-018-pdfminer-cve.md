# CHG-PW-018 — Raise pdfminer.six, pytest and duckdb pins

| Field | Value |
|---|---|
| Requested by / date (SAST) | Owner approved patching on 27 November 2026, for the pdfminer.six advisories CVE-2025-64512 and CVE-2025-70559. The same change also raises the pytest and duckdb pins listed in the 27 November 2026 security baseline. Relayed by the orchestrator. |
| Author / builder | author bot |
| Reviewers | two reviewers |
| Change authority | Owner (GO on the exact head to push or merge). Push and merge need the owner's GO naming the exact head. |
| Type | Standard — low (dependency pins only; no profile facts or site-output change) |
| Environment | DEV. The publish gate and `PW_PUBLISH_ENABLED` are unchanged. Nothing is deployed. |
| CIs affected | Python pins in `pyproject.toml` and `uv.lock`. Nightly already installs with `uv sync --frozen`, so the new lock is what CI will use. No workflow file is changed. |
| Linked records | Security baseline of 27 November 2026 (H-1 pdfminer.six; L-1 pytest; L-2 duckdb). CHG-PW-017 is already on the base `origin/main`. |
| Branch | `politicianwatch-sa` `dev/chg-pw-018-pdfminer-cve`, from `origin/main` `a365913e6abc43e510135b97f1e18055ff8be8bf` |
| Pre-change commit (rollback SHA) | `a365913e6abc43e510135b97f1e18055ff8be8bf` (PR #17 squash on `main`; pre-merge tag `snapshot-2026-11-25-pre-pw-pr17` at `72d8f763311a7a1ace2b451860eeaebac5f93b3d`) |
| Numbering | Next free `CHG-PW` number on `main` (`itil/changes` has 001–017). 015, 016 and 017 are already on `main`. No other `018` branch was present when this branch was created. Residual clash risk only if a parallel change also takes 018 before this is merged. |

## What changes

1. **`pyproject.toml` and `uv.lock`.** Exact pins:
   - `pdfplumber` `0.11.7` → `0.11.11`. That release requires `pdfminer.six==20260107`, which is later than `20251230` and closes CVE-2025-64512 (fixed in `20251107`) and CVE-2025-70559 (fixed in `20251230`). pdfplumber `0.11.9` was the first release to pin `pdfminer.six==20251230`; `0.11.11` is the current pdfplumber release and still pins `20260107`. An explicit pdfminer constraint was not needed.
   - `pytest` `8.4.2` → `9.2.0` (latest 9.x at the time of this change), which is past the CVE-2025-71176 fix in `9.0.3`.
   - `duckdb` `1.4.1` → `1.4.5`. DuckDB is a direct dependency and is used by `pwatch/warehouse.py` (in-memory roster load only; the encryption feature named in CVE-2025-64429 is not used). The first fixed release is `1.4.2`; `1.4.5` is the latest release on the 1.4 line. DuckDB `2.0.1` exists but is a major-version jump and is not required to close the advisory, so it is not taken.
2. **Records.** This RFC, STATUS, and the change log.

`uv.lock` version changes are only those four packages (pdfminer.six comes in via pdfplumber). The local `pwatch` metadata specifiers in the lock were updated to match. Pillow `13.0.0` and pypdfium2 `5.15.2` are unchanged. No packages were added or removed.

## What stays

Application code, profiles, the gazette roster, collectors, parsers, workflows, the site builder, and the publish gate. `UV_VERSION` in `nightly.yml` stays `0.13.8`. No new tests were added; existing warehouse and gazette tests were re-run, and the PDF extract path was smoke-tested outside the committed tree.

## POPIA

Pins and lockfile only. No personal details, new profile facts, or new sources are added.

## How to revert

On this branch, restore the previous `pyproject.toml` and `uv.lock`, or delete the branch and leave a later PR unmerged. After a later squash-merge: `git revert <squash commit>`; `main` returns to `a365913e6abc43e510135b97f1e18055ff8be8bf`.

## Testing (evidence)

Recorded in the STATUS history row and the PR body draft (written outside the repo):

- `uv run pytest -q`: 151 passed in 15.07s. Pytest 9.2.0 caused no test or config breakage (`tool.pytest.ini_options` is unchanged and still only sets `testpaths = ["tests"]`).
- `uv run pwatch dq`: pass (270 roster + 269 CV profiles, 1 on hold, 0 failures, 0 warnings, `as_of` 2026-11-27).
- `uv run pwatch render --check`: pass.
- `uv run pwatch site build --out <temp> --commit <HEAD>` and `uv run pwatch site check <temp>`: pass. The site output was not committed.
- DuckDB path: `tests/test_warehouse.py` passed; a one-off in-memory `load_profiles` smoke on duckdb `1.4.5` passed. No encrypted DuckDB files are used.
- PDF path: `pwatch.connectors.iec_gazette.extract_text` returned the expected text from a synthetic one-page PDF, and from Government Gazette 55741 (SHA-256 matches the committed hash; 144 pages). Confirmed installed versions: pdfplumber `0.11.11`, pdfminer.six `20260107`.
- `gitleaks detect --log-opts=--all --redact`: no leaks found (89 commits). `actionlint` and `zizmor --offline` on `nightly.yml`: no findings (workflow unchanged; run as the usual check).
- Review kit on the committed head, including the agent-names-file variant.

Nightly install path: `.github/workflows/nightly.yml` already runs `uv sync --frozen` in the build and live-check jobs, so CI will install the new lock.

## Seen, not touched

- STATUS and the change-log outcome for CHG-PW-017 still describe that RFC as awaiting a push GO, even though this branch is based on `origin/main` `a365913` (PR #17 squash of 25 Nov 2026 17:35:15 SAST). Those 017 records are left as they stand on `main`.
- DuckDB 2.0.1 is not pinned (see above).
- No change to `nightly.yml` or `UV_VERSION`.

## Approval

Push and merge need the owner's GO naming the exact head.
