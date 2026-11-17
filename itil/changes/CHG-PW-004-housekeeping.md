# CHG-PW-004: Allowed-source list and retrieved_at wording (housekeeping)

| Field | Value |
|---|---|
| Requested by / date (SAST) | Owner (project owner, by role), 17 November 2026 |
| Author / builder | PoliticianWatch (Grok Bot) |
| Type | Standard, low (commit 1: documentation and docstrings only). Commits 2–4: normal, low (tiered mainstream source list, source registry and DQ rules with tests, docstring fix, tier-3 scope removal; no profile data changes) |
| Environment | DEV |
| Branch | `dev/chg-pw-004-housekeeping`, stacked on CHG-PW-003 (`95426512`, draft PR #3) |
| Rollback | `git revert` this commit, or reset the branch to `95426512` |

## Request and reasons
1. On 17 Nov 2026 the owner confirmed that SA Jewish Report, Southern Courier and Sowetan join the allowed sources. They were first used in CHG-PW-003 fix 1 at reviewer Cassian's suggestion. The allowed list was scattered across the batch notes and RFCs; it is now a single file, `docs/allowed-sources.md`, which AGENTS.md rule 12 references.
2. Cavus review note on PR #3: the docstrings and the schema description said a date-only `retrieved_at` is "read as the end of that day". The code treats it as future only if that date is after today's date in SAST. The text now says that. No logic change.
3. Cavus review note: AGENTS.md rule 11 now says that `data/raw/manifest.jsonl` is committed and not gitignored, while fetched pages are.

4. **Tiered source list (owner, 17 Nov 2026):** "Ideally it covers all SA media, large audience anyway … Maroela Media? Common Sense? … Cape Independent is @uMarhobane on X … keep them in a separate pen." `docs/allowed-sources.md` is rewritten into tiers: tier 1 primary (unchanged); tier 2 mainstream SA news (national, broadcast, IOL titles, Afrikaans, regional dailies, Caxton locals, business/tech; about 45 outlets); tier 3, a "separate pen" for smaller, independent voices (The Common Sense, The Cape Independent, Briefly News, Rand Desk), Reported only, never the sole source for an adverse item or an identity link; plus criteria for adding tier-3 voices (named editor or author, track record, wide-audience intent, owner confirms each). Party statements, link-only and not-allowed sections kept. Every domain was checked on 17 Nov 2026; Scrutinize (placeholder site), Ilanga (domain not found) and Joburg East Express (404) were not added. Owner to confirm: The Common Sense identification, The Cape Independent's current operator, Rand Desk tier, Briefly News in tier 3.
5. **Source registry and DQ:** `data/sources.json` (domain → tier, 70 entries) and `pwatch/sources.py`. `pwatch dq` now fails a source on a `link_only` or `not_allowed` domain, an adverse item whose sources are all tier 3, and a profile whose identity link rests only on tier-3 sources. It **warns** (does not fail) on domains not in the registry and reports them under `warnings`. Tests: `tests/test_sources.py` (6 tests, synthetic registry, plus a check that every source URL in the committed profiles is registered). No profile data changed; the committed profiles produce 0 failures and 0 warnings.

6. **Docstring (Cassian/Cavus):** commit `7b7a0e5` removes a duplicated sentence in the `check_retrieved_not_future` docstring.
7. **Scope correction (owner, 17 Nov 2026, in chat):** "yes sorry my bad, original spec was mainstream, additional is new rfc". CHG-PW-004 covers **mainstream sources only** (tiers 1 and 2). A forward commit removes tier 3 from this change: the tier-3 section, its criteria and the Common Sense identification note in `docs/allowed-sources.md`; the 6 tier-3 entries in `data/sources.json` (now 64 entries); the tier-3 DQ rules (adverse item or identity link resting only on tier 3) and their 2 tests. Kept: tiers 1 and 2, the registry, the link-only and not-allowed checks and the unknown-domain warning. The smaller outlets (The Common Sense, The Cape Independent, Briefly News, Rand Desk) and their owner-to-confirm items move to CHG-PW-005. Items 4 and 5 above describe commit 2 as first built; this item supersedes their tier-3 parts.
8. **Owner to confirm (004):** "Scrutinize" (requested for tier 2) is still unverified: scrutinize.co.za is a placeholder. Owner to say which outlet was meant. BizNews (biznews.com) is in tier 2.

## Risk
Low. Commit 1 is documentation only. Commit 2 adds DQ rules that pass on the committed data; the risk is a future profile failing on a tier rule, which is the intent. Tests, `pwatch dq` and `pwatch render --check` must still pass. After commit 2: `uv run pytest -q` 46 passed; `uv run pwatch dq` pass (270 roster + 24 CV profiles, 1 on hold, 0 failures, 0 warnings); `uv run pwatch render --check` exit 0. After the scope correction: `uv run pytest -q` 44 passed; `uv run pwatch dq` pass, 0 warnings; `uv run pwatch render --check` exit 0. popia-review on the commit-2 diff: PASS (outlet names, domains and public X handles of publications or their public editor only; no personal information; the source-list note warns that Caxton local pages carry personal details and only public-role facts may be recorded).

## Merge order
PR #2, then PR #3, then this change.

## Approval
| Role | Name | Commit approved | Date | Result |
|---|---|---|---|---|
| Author / builder | PoliticianWatch (Grok Bot) | | 2026-11-17 | drafted |
| Reviewer | Cavus | | | pending PASS on the exact head |
| Reviewer | Cassian (Build, review only) | | | pending PASS on the exact head |
| Change authority | Owner | | | pending GO |
