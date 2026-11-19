# CHG-PW-011 — Magwentshu: drop The Citizen source; first year in council from the 2021 election gazette

| Field | Value |
|---|---|
| Requested by / date (SAST) | Owner decision, in the owner's own words, relayed by the orchestrator on 19 Nov 2026 at 18:15 SAST: "OK remove Citizen link. I've thought it through and through and they can make errors, we won't." (This supersedes the 16:27 SAST decision in the same change.) |
| Author / builder | author bot |
| Reviewers | two reviewers |
| Change authority | Owner (decision above; GO on the exact head to merge) |
| Type | Normal — medium (profile data; the rule-6 exception remains in code but unused) |
| Environment | DEV + TEST profiles. Publishes nothing: the publish gate and `PW_PUBLISH_ENABLED` are unchanged, and profiles stay unpublished |
| CIs affected | CI-009 Joburg CV profiles (one profile); DQ gate (exception unused); CI-010 draft-site builder |
| Linked records | CHG-PW-007 (rule 6); CHG-PW-003 (first year in council) |
| Branch | `politicianwatch-sa` `dev/chg-pw-011-magwentshu-source`, from `origin/main` |
| Pre-change commit (rollback SHA) | `c85db068b6933924cc0b571ed65e4192c661261a` (`main` after the CHG-PW-012 squash merge; tag `snapshot-2026-11-19-pre-pw-pr12` is the state before that merge) |

## What changes

1. **The Citizen interview is no longer linked.** The article at `citizen.co.za/news/lubabalo-magwentshu-mmc-interview` is removed from Magwentshu's education, career, first-year-in-council fact and identity-match citation. The `owner_approved_pi_source` field and the note "personal details not recorded here" are removed from this profile. The owner's reason, in the owner's words: the outside source can make errors, "we won't", and it is a source we do not want to link to because of personal details.
2. **Education and career are Unknown.** A further search (19 Nov 2026) for a tier-1 or tier-2 source that states those facts and does not carry private personal details found none that qualify. A City of Johannesburg MMC biography page (tier 1, confirmed to load) states public-role education and career facts but also carries private personal details, so it was not used. Other pages either are not on the allowed list, copy the same kind of personal details, or do not state the facts. Default rule 6 applies. The identity note says only "a source with personal details was not used".
3. **First year in council is Confirmed from a primary source.** Government Gazette 45447 (Electoral Commission, 9 November 2021), Notice 653, "Publication of the List of Elected Councillors" for the 2021 General Elections of Municipal Councils, page 50, lists MAGWENTSHU, LUBABALO CECIL, African Transformation Movement, PR(1), City of Johannesburg. Copy used: Gazette Finder, https://www.gazettefinder.co.za/gazettes/government-gazette/2021/45447/government-gazette-45447-2021-11-09.pdf (HTTP 200; SHA-256 `b00b9cabd8fbb1a3274855e265590cde14f646df203ecccaf2e0c070889e264e`; fetched 2026-11-19T18:19:22+02:00; logged in the raw manifest). The page lists province, municipality, party, list order, surname and full name only. Value: "First year in council: 2021. Elected as the African Transformation Movement's PR councillor for the City of Johannesburg in the 2021 local government elections".
4. **Identity match:** at least three details remain, with The Citizen removed: name, party ATM, and council role, from the City statement (2023-02-02), Sowetan (2022-09-14) and the 2021 elected-councillor list (GG 45447).
5. **Rule 6 exception mechanism kept, unused.** `check_pi_source_allowance`, the settings, the renderer for an approved-fact note, the allowed-sources exception text, and the synthetic tests stay in place. They currently have no uses in the data. The test that required approval on this profile was replaced by a test that the Citizen interview URL and the approval field are absent, education and career are Unknown, and first year in council cites GG 45447.
6. **Records aligned:** batch-2 doc, the unsent accuracy-check draft, CHG-PW-003 RFC row 2c, the CHG-PW-007 rule-6 amendment paragraph, change log, STATUS. `docs/LATER.md` keeps the parked idea for a dq flag on PI-bearing sources.

## What stays

All other profiles and their renders; Chame and Raphadu notes ("a source with personal details was not used"); the Sowetan committee-chair fact and the City and EWN MMC facts; the rule-6 default and the unused exception code; the publish gate; robots, noindex, DRAFT banner and privacy page; the LATER item for a dq flag on PI-bearing sources.

## Risks

Medium-low. The owner's stated concern is that an outside news source can make errors, and that this project should not link to a source that carries personal details. First year in council now rests on a primary Electoral Commission gazette, not on that news article. Education and career may stay Unknown until a qualifying public source is found.

## Seen, not touched

- The exception mechanism in `pwatch/dq.py`, `pwatch/settings.py`, `pwatch/site_profiles.py` and the synthetic tests in `tests/test_dq.py` and `tests/test_site_profiles.py`. Kept, unused.
- A City MMC biography page was checked (HTTP 200) and not used, because it carries private personal details.
- An IEC elected-councillor list was checked (HTTP 200) and not used, because it carries private personal details. The Gazette Finder copy of GG 45447, which does not, is the source cited.
- GG 45527 (22 November 2021, the amended elected-councillor list) also names the same person, party and seat; 45447 (the original 9 November list) is the source used.
- A Caxton local article was checked (HTTP 200) and does not state education, career or first year in council; it was not cited.
- Outlets not on the allowed list (including councillor aggregators) were not used.
- `docs/LATER.md` already has the parked dq-flag idea; not changed in this revision.

## Testing (evidence)

See the STATUS history row: pytest, `pwatch dq`, `pwatch render --check`, site build + check, `actionlint`, and the review kit (output saved outside the repo and pasted into the PR body).

## How to revert

Before merge: close the PR or delete the branch. After merge: `git revert <merge commit>`; `main` returns to `c85db068` (CHG-PW-012).

## Approval

Plain PASS from two reviewers on the same head, then the owner's GO to merge. Outcome: pending (in review as PR #11).
