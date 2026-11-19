# CHG-PW-011 — Magwentshu sources and Withheld (POPIA) status

| Field | Value |
|---|---|
| Requested by / date (SAST) | Owner rule, in the owner's own words, relayed by the orchestrator on 19 Nov 2026 at 18:25 SAST: "For future, it's not unknown it's not released due to a higher priority, POPIA. If a serious person questions us for knowing, we could refer the source. However this is not about nitpicking, it's about aggregating this data erring on ethically if necessary." This follows, and does not undo, the 18:15 SAST decision: "OK remove Citizen link. I've thought it through and through and they can make errors, we won't." (Both supersede the 16:27 SAST decision in the same change.) |
| Author / builder | author bot |
| Reviewers | two reviewers |
| Change authority | Owner (decision above; GO on the exact head to merge) |
| Type | Normal — medium (profile data and a new public status; the rule-6 link exception remains in code but unused) |
| Environment | DEV + TEST profiles. Publishes nothing: the publish gate and `PW_PUBLISH_ENABLED` are unchanged, and profiles stay unpublished |
| CIs affected | CI-009 Joburg CV profiles; DQ gate (Withheld (POPIA) check; exception unused); CI-010 draft-site builder (render and leak check) |
| Linked records | CHG-PW-007 (rule 6); CHG-PW-003 (first year in council) |
| Branch | `politicianwatch-sa` `dev/chg-pw-011-magwentshu-source`, from `origin/main` |
| Pre-change commit (rollback SHA) | `c85db068b6933924cc0b571ed65e4192c661261a` (`main` after the CHG-PW-012 squash merge; tag `snapshot-2026-11-19-pre-pw-pr12` is the state before that merge) |

## What changes

1. **New public status: Withheld (POPIA).** It is not Unknown. Schema design: a new label value `Withheld (POPIA)` in `LABELS` and the profile JSON Schema, rather than `Unknown` plus a flag, so the rendered text says withheld and Unknown stays reserved for "no source found". A withheld fact has a null value and no public URL. The site and markdown render show: "Withheld (POPIA): a source exists but carries personal details, so it is not published here." There is no link and no hint about which outlet it is.
2. **Private source references, so a serious enquirer can be referred to the source.** URL, title, date and fact key only (plus slug so the entry can be matched) are stored in `private/withheld-sources.json`. No fact values and no personal details are copied. The `private/` directory is never rendered, never copied into a site build, and is on the FRESH-REPO-PLAN "do not carry over" list. `pwatch site build` and `pwatch site check` fail if any withheld-source URL or title appears in the built output (matched after normalisation).
3. **The Citizen interview is not linked on the public profile.** Education and career values stay out of the public profile. The 2021 election fact is Confirmed from Government Gazette 45447 (Electoral Commission, 9 November 2021, p. 50; Gazette Finder copy, HTTP 200; SHA-256 `b00b9cabd8fbb1a3274855e265590cde14f646df203ecccaf2e0c070889e264e`; fetched 2026-11-19T18:19:22+02:00). Value, worded only as far as the gazette shows: "Elected ATM PR councillor (City of Johannesburg), 2021 local government elections". It does not claim a first year in council beyond that.
4. **Magwentshu education and career are Withheld (POPIA).** Private entries (titles and dates only): The Citizen interview, 2023-06-17, and the City of Johannesburg MMC for Community Development page, date recorded as 2026-11-19 (the date the page was checked, HTTP 200; the page has no usable publication date). Each fact has both entries.
5. **Identity match** still has at least three details, with The Citizen not cited: name, party ATM, and council role, from the City statement (2023-02-02), Sowetan (2022-09-14) and the 2021 elected-councillor list (GG 45447).
6. **DQ:** a withheld fact needs a matching private-source entry, carries no public URL, and is not an adverse item. The gate also fails when any fact is Withheld (POPIA) and the register is missing or empty. Tests cover the passing case, a missing or empty register, a missing entry, a public URL, a non-null value, and an adverse item. The owner-approved link exception (`check_pi_source_allowance`) stays in place and still has no uses.
7. **Docs:** rule 6 in `docs/allowed-sources.md` and the CHG-PW-007 RFC now state the default as Withheld (POPIA), and Unknown as no source found. Batch-2, the unsent accuracy-check draft, CHG-PW-003 row 2c, change log, STATUS, README, AGENTS and REVIEW are aligned. `docs/LATER.md` keeps the parked idea for a dq flag on PI-bearing sources, and records further parked items from the review round (where the private register lives in a fresh public-repo setup, mechanical enforcement of the do-not-carry list at seeding, and tests for currently uncaught gates).

## Conversions of the old "a source with personal details was not used" Unknown notes

- **Converted, with private-source entries:** Magwentshu `education` and `career` (URLs recorded in history for The Citizen interview; the City MMC page was checked in this change and is recorded too).
- **Not converted (label stays Unknown; no private entry):** no other profile had an Unknown fact with that note. Chame and Raphadu still have the phrase on the *identity-match* note only; their education and career remain Unknown because no source was found, and no PI-source URL is recorded in history for those two facts.

## What stays

All other profiles and their renders; Chame and Raphadu identity notes; the Sowetan committee-chair fact and the City and EWN MMC facts; the unused owner-approved link-exception code; the publish gate; robots, noindex, DRAFT banner and privacy page (the privacy page now lists the new status); the LATER item for a dq flag on PI-bearing sources.

## Risks

Medium-low. The public site does not link to, or repeat values from, a source that carries personal details. The private file exists only in this private repository, is excluded from the site build by a leak check, and is listed as not to be carried into a fresh public repository. The 2021 election fact rests on a primary Electoral Commission gazette and is worded only as far as that gazette shows.

## Seen, not touched

- The exception mechanism in `pwatch/dq.py`, `pwatch/settings.py`, `pwatch/site_profiles.py` and the synthetic tests in `tests/test_dq.py` and `tests/test_site_profiles.py`. Kept, unused.
- An IEC elected-councillor list was checked (HTTP 200) and not used, because it carries private personal details. The Gazette Finder copy of GG 45447, which does not, is the source cited for the 2021 election fact.
- GG 45527 (22 November 2021, the amended elected-councillor list) also names the same person, party and seat; 45447 (the original 9 November list) is the source used.
- Outlets not on the allowed list (including councillor aggregators) were not used.
- The `pwatch/provenance.py` helper still names fetched profile-sources with a `.html` suffix; only the GG 45447 manifest row was renamed to `.pdf`. Left as a later tidy.


## Review round (19 Nov 2026, after head `1f80de37`)

One reviewer passed that head; the other passed with concerns. This revision, to reach a plain PASS:

1. Leak matching in `pwatch/withheld.py` normalises both the built output and the register values before comparing: casefold, `urllib.parse.unquote` (repeated until stable), `html.unescape`, then strip the scheme (`http`/`https`), a leading `www.` and any trailing slash. Each register title is also matched after casefold, unescape and collapsed whitespace. Tests cover an upper-case URL, `%2F` encoding, `&#47;` HTML entities, and a title leak (each fails `pwatch site check`); clean output still passes.
2. Magwentshu's GG 45447 fact is reworded to "Elected ATM PR councillor (City of Johannesburg), 2021 local government elections" (Confirmed; same source, date and page). It no longer claims "first year in council" beyond what the gazette shows. The `field` remains `position`.
3. DQ and site check fail when any fact is Withheld (POPIA) and the register is missing, empty, or has no entry for that slug and fact. Tests cover a missing file and an empty register.
4. The raw-manifest row for the GG 45447 fetch is renamed from `.html` to `.pdf` (the file is a PDF). The on-disk copy was renamed to match; it stays gitignored.
5. Parked in `docs/LATER.md` only (not implemented): where the private register lives in the fresh public-repo setup; mechanical enforcement of the do-not-carry list at seeding; tests for currently uncaught gates (`check_pi_source_allowance` in `check_profile`, `check_withheld_entry_format` in `run`, and the `private/`-in-built-output check).

## Testing (evidence)

See the STATUS history row: pytest, `pwatch dq`, `pwatch render --check`, site build + check, `actionlint`, and the review kit (output saved outside the repo and pasted into the PR body).

## How to revert

Before merge: close the PR or delete the branch. After merge: `git revert <merge commit>`; `main` returns to `c85db068` (CHG-PW-012).

## Approval

Plain PASS from two reviewers on the same head, then the owner's GO to merge. Outcome: pending (in review as PR #11).
