# AGENTS.md — context for AI agents working on PoliticianWatch SA

**What this is:** a neutral, sourced public register of South African elected representatives. Design and source policy: `README.md`, `docs/sources-joburg-lge-2026.md`, `schemas/profile.schema.json`. Stack: ADR-0001.

**Stack:** Python 3.13 (uv + lockfile), DuckDB, httpx, pdfplumber, pytest. Package `pwatch`. Modelled on PublicFunds (`thusa`), not a copy of that package.

**Non-negotiables**

1. Neutral, factual tone. No opinion adjectives such as "corrupt" or "incompetent". Every claim is attributed.
2. Every fact has a label: `Confirmed`, `Reported`, `Alleged`, `Disputed`, or `Unknown`. A non-Unknown fact has a dated source URL. Missing is `null`, never silently filled.
3. Public role only. Never collect or store ID numbers, home addresses, personal phones or emails, private family, or health information. Official office contacts only.
4. Primary sources are the IEC and Government Gazette 55741 (and later official records). **Do not scrape ElectionSePush.** Link only. **Do not fetch SAFLII automatically.**
5. Right of reply: every adverse item (court or criminal matter, scandal, allegation) has a `right_of_reply` object and a draft in `drafts/right-of-reply/`. Default status is `pending`. The profile shows "Right of reply: pending" with a blank reply field. **The bot never sends a draft. The owner sends them personally.** Status changes only when the owner records `sent_at`, a reply, or `no_response` after the deadline. `recorded_by` on those statuses is `owner`.
6. The DQ gate (`pwatch dq`) fails (exit 2) if a fact is missing a label or a required source, or if an adverse item has no right_of_reply, has no draft, or is in `sent` / `replied` / `no_response` without the matching owner-recorded fields.
7. Drafts only until a quoted owner GO: do not push to `main`, merge, publish, deploy, change a domain, or contact anyone (including the IEC, councillors, ElectionSePush, or the MDB) unless the owner has named that action and that head.
8. Change process: name the RFC, work on a branch, record the pre-change SHA, make only the change the RFC names. Two reviewers (Cavus and Cassian) must each give a plain PASS on the same exact head. `PASS_WITH_CONCERNS` does not count. The owner GOes last.
9. Before adding a dependency, confirm the package exists on PyPI, is the intended one, and is actively maintained. Update the lockfile.
10. No secrets in code, the repo, logs or chat. Parameterised SQL only, when SQL is used.
11. `retrieved_at` comes from fetch provenance, never from memory. Fetch sources with `uv run pwatch fetch-source <url>`, which stores the page in the raw layer, logs the real fetch time in `data/raw/manifest.jsonl` and prints the `retrieved_at` to copy. A fetched file's own timestamp also counts. **Never type a `retrieved_at` time by hand.** If the time was not logged, write the date only (`YYYY-MM-DD`), which is read as "time not logged". `pwatch dq` fails any value later than the run time (a date-only value fails only if that date is after today's date in SAST). Fetched pages under `data/raw/` are gitignored, but `data/raw/manifest.jsonl` is committed and is not gitignored: it is the provenance record.
12. Use only sources on the allowed list in `docs/allowed-sources.md` (tiers 1 and 2; registry `data/sources.json`). A source not on it needs the owner's confirmation before it is cited. `pwatch dq` fails link-only and not-allowed domains and warns about domains that are not in the registry.

**How to verify your work (show the output, don't claim it):** `uv run pytest -q` · `uv run pwatch dq` (exit 0). Docs-only changes need a link check. Run a `popia-review` before a PR or publish.

**Goals:** an honest, sourced register; explicit unknowns; a Joburg pilot that can be checked against 270 official seats. **Non-goals:** verdicts of guilt, leaked data, scraping licence-restricted sites, contacting subjects from the bot.
