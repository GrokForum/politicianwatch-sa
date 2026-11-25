# CHG-PW-017 — National watch-list intake (RFC draft only, Design B)

| Field | Value |
|---|---|
| Requested by / date (SAST) | Owner GO, 25 November 2026, for a national watch-list intake RFC, starting with a national executive subject. Relayed by the orchestrator. Later the same day the owner recorded the three decisions below (ref t706s3008). This change covers drafting the RFC only. |
| Author / builder | author bot |
| Reviewers | two reviewers |
| Change authority | Owner (GO on the exact head to push or merge). Push and merge need the owner's GO naming the exact head. |
| Type | Standard — low (documentation only). A later implementation that stores intake, publishes national watch-list items, or adds national profiles would be at least Normal-high. |
| Environment | DEV. No code, data, workflow or site change. Nothing is published, pushed or deployed here. |
| CIs affected | None in this change. A later implementation would affect intake storage, the profile schema, CI-010 draft-site builder, and the national and provincial 2029 module plan. |
| Linked records | [CHG-PW-015](CHG-PW-015-mp-pay-context.md) (pay context, including ministers' pay); `docs/national-2029-module.md`; `docs/ROADMAP.md` |
| Branch | `politicianwatch-sa` `dev/chg-pw-017-national-watchlist-rfc-b`, from `origin/main` `72d8f76` |
| Pre-change commit (rollback SHA) | `72d8f763311a7a1ace2b451860eeaebac5f93b3d` (`main` after the CHG-PW-016 squash merge) |

## Owner decisions (25 November 2026, ref t706s3008)

These are decisions, not open questions.

1. **Design B.** Named intake entries stay in a private, non-committed file. The committed RFC carries only the schema, counts, hold reasons, process rules, and (at most) generic source types. It does not name people, unique offices, departments or ministries, specific party posts, companies, or dated sources tied to entries.
2. **BEE elites page stays off** until each entry has passed the primary-source check and the right-of-reply gate. The page is specified below, disabled by default. It is not built in this change.
3. **Scope.** Non-office-holder public figures, and party-only posts, are in scope, subject to the same checks as office-holders (two-detail match, no paywalled sole citation, Reported (unconfirmed) until a primary-source check, right of reply pending, public-role or business facts only, no private particulars).

## Request

Plan, in an RFC only, a **national watch-list intake** area that receives **batches** of cited entries:

1. Say where intake lives (Design B: names off the public tree).
2. Define an entry schema and how an item moves from intake to a labelled profile fact.
3. Set the scope, including the decisions above.
4. Record two example batches by id, with aggregate counts, coarse role buckets, and hold reasons, not names or unique offices.

This change writes the RFC, a roadmap pointer, and a change-log and STATUS row. It does not add intake files, profile data, collectors, or site pages. It does not label any committed item as a profile fact.

## Public-repository note

**`politicianwatch-sa` is a public GitHub repository.** Design B is the chosen design: this RFC does not bind a name to a claim. Working intake, including named entries, is held outside the repository and must not be committed, copied into a pull request, or rendered from a committed file. A later change must not add the private file to this tree.

## Reasons

The live site is still a draft of Johannesburg councillor profiles. National and provincial profiles remain plan only (`docs/national-2029-module.md`). The owner has asked for a watch-list intake, starting with a national executive subject, and for a batch process that can take further cited entries. Teammate-bot briefings and research notes are received as data, not as sources. Because this repository is public, named unconfirmed claims stay off the committed tree until the gates below are met.

## What changes

- This RFC (`itil/changes/CHG-PW-017-national-watchlist-rfc.md`).
- A one-line pointer in `docs/ROADMAP.md`.
- A change-log row, and a STATUS history row, for this change. The Current section records PR #16 as squash-merged into `main` as `72d8f76`.

## What stays

Everything else. No profile, schema, registry, collector, workflow or site file is edited. No intake note is committed. No fact is added to a profile. No BEE elites page is built or enabled. No new source domains are added to `data/sources.json`. Right-of-reply drafts remain unsent. The publish gate is unchanged. The 2029 module remains plan only. CHG-PW-015 stays as merged documentation; this change does not implement pay-context figures. CHG-PW-016 is already merged (`dpsa.gov.za` is tier 1) and is not edited here.

## Scope

**In scope for a later implementation (not this change):**

- A defined intake area that accepts batches of cited entries for national and provincial public-office holders, party-only posts, and non-office-holder public figures, starting with Batch 1 (national executive: 1).
- The entry schema below, and a written path from unverified intake to a labelled, sourced profile fact, in a later named change, after review and any required owner GO.
- A later BEE elites (or equivalent) page, **disabled by default**, enabled only under a future named change, and only for entries that have passed the primary-source check and right-of-reply gate.

**Out of scope (do not build in this change, and do not do later without a named change):**

- Committing the private intake file, or any profile JSON, for these subjects.
- Publishing any intake entry on a profile, or turning the BEE elites page on.
- Contact with any subject.
- Sending right-of-reply letters (drafts only; the owner sends them).
- Submitting a parliamentary question (a draft for the owner to send would need its own GO).
- Scraping ElectionSePush, or fetching SAFLII automatically (looked up by hand only).
- Home addresses, ID numbers, dates of birth, personal phones or emails, private family members, or health information.
- Treating a teammate-bot briefing, or a commentator's opinion piece, as a primary source.
- Attaching aggregate or statistical claims that name nobody to any person.
- Expanding a family or group mention into named individuals.

## Intake rules

These rules bind any later implementation.

1. **Intake arrives in batches.** A batch has an id, a date received, an attribution, and one or more entries.
2. **Teammate-bot briefings and research notes are unverified intake.** They are not a source. Each discrete claim is re-checked independently before use.
3. **Re-check against a primary source or reputable reporting.** Preferred primary sources: Parliament and PMG, the Government Gazette, official departmental sites (`gov.za`, including a department's own site once allowed), the IEC, the courts (SAFLII by hand only), company regulatory notices (for example JSE SENS) where a business fact is in issue, and other already-allowed tier-1 sources such as The Presidency. Reputable reporting means an already-allowed tier-2 outlet, used at the Reported label, never as the sole support for an identity link or for a Confirmed fact.
4. **Label before use, but labelling is not publication.** An intake entry must carry exactly one of: Confirmed, Reported, Alleged, Disputed, or Unknown before it may be used on a profile. Active Batch 2 entries in the private file are labelled **Reported (unconfirmed, pending a primary-source check)**. That is an intake label only. **Withheld (POPIA)** remains the existing privacy status: a fact whose only source carries personal details is Withheld (POPIA), with the source held in `private/withheld-sources.json`, and with no value and no link on the public profile. It is not a sixth ordinary fact label.
5. **No intake entry is published on a profile until both of the following are true:** (a) a primary-source check has been done and the label is set; and (b) a right-of-reply draft exists, and the profile shows "Right of reply: pending" or the reply itself. Drafts only; the owner sends them and records the state.
6. **Public sources only.** Do not use non-public documents, leaked files, or private correspondence. Drop a Sunday Times PREMIUM or other paywalled citation. If the claim then has no remaining source, hold the entry.
7. **In committed text, refer to subjects only by a coarse role bucket or an entry id** (for example "national executive"), never by a unique office, department, ministry, party post or company. Named entries stay in the private file. Do not add family, household, dates of birth, or other private individuals named in coverage. Public-role and business facts only.
8. **Two-detail match.** Link a court or news item to a person only when at least two identifying details in that item match (for example a name and a public office, a party post, or a distinct public business identifier such as a company). One matching name is not enough. If an entry fails the rule, hold it.
9. **Office-holders, party-only posts, and non-office-holder public figures are in scope**, per the 25 November 2026 decision. If a person is a private individual without a public role, or a relative named only through family status, do not name them in committed text; hold that entry.
10. **Co-accused are described as charged, not convicted.** Case status stays Unknown until a primary court or official record is checked. A charge mentioned only in a dropped PREMIUM source is not used.
11. **No contact with the subject.** Right-of-reply drafts stay drafts. The owner sends them and records the state.
12. **Design B.** Committed documents describe batches by id, coarse role buckets, counts and hold reasons. They do not name the people in the batches, and they do not use a unique office or a dated source to point at one person. Prof William Gumede may be named only as the published author of cited source work, without dating or tying a piece to an entry.

## Entry schema (proposal)

A later implementation would store one record per discrete claim, not one record per person. Proposed fields:

| Field | Purpose |
|---|---|
| `batch_id` | Batch identifier (for example `1`, `2`). |
| `batch_attribution` | Why the entry is in the batch (briefing; named in a cited piece; "named by other authors, not by the Batch 2 commentator"). |
| `subject_id` | A role-based slug, not a personal identifier. Examples: `za-national-executive`; `za-office-holder`; `public-figure-business`. |
| `subject_kind` | `office_holder`, `party_post`, or `public_figure_non_office`. On a later page, the last two sit in a clearly marked section, separate from elected or appointed office-holders. |
| `public_offices` | Current or former public offices or party posts, from an allowed or cited public source. For a non-office-holder public figure, a short public-role or business description instead. |
| `claim` | A short restatement of one discrete claim. |
| `label` | Confirmed, Reported, Alleged, Disputed, or Unknown. Withheld (POPIA) is recorded as the privacy status where it applies. |
| `source_url` and `source_date` | The cited public URL and its date, held in the private file when a path would identify a person. Paywalled or PREMIUM citations are not stored as the supporting source. |
| `primary_source_check` | `planned`, `done` (with date, SAST, and result), or `pending`. |
| `right_of_reply` | `not_started`, `draft`, `pending` (the profile must show "Right of reply: pending"), `received`, or `owner_declined_to_send`. |
| `state` | `active` or `hold`. |
| `hold_reason` | Required when `state` is `hold`. Coded reasons used in this RFC: `hold-owner-ruling` (low-profile official, or ambiguous group or family-status entries); `hold-premium-source-dropped-no-remaining-cite`; `hold-two-detail-match-failed`. Held entries in committed text are described by count and reason only. |

## Where intake lives

Working intake, including every named entry, is held **outside this repository**. It is not committed here.

`private/` in this repo is tracked on the public GitHub tree. It is not rendered on the site (`private/README.md`), but a file committed there is still public on GitHub. Design B therefore keeps named intake off the tree entirely (untracked, a gitignored sidecar, or an off-repo store). Commit only labelled, reviewed profile facts, plus Withheld (POPIA) register rows in the existing private register when that status applies.

## How an item moves from intake to a profile

1. **Receive a batch.** Record the attribution, the date received, and each discrete claim with its cited URLs, in the private file. New entries start as unverified intake, or with an intake label such as Reported (unconfirmed) when that is the rule for the batch, and with `primary_source_check` planned or pending.
2. **Filter.** Apply the scope, two-detail, paywall, and private-person rules. Entries that fail are held, by reason, with no name in public committed text.
3. **Re-check.** Fetch or read an allowed primary or reputable source. Record the check date (SAST), HTTP status, any TLS error, and what the source actually says. A reachable URL is not, by itself, a completed check or a final label.
4. **Identify.** Apply the two-detail match before attaching the claim to a person. If the match fails, hold the entry.
5. **Set the label** after the check: Confirmed, Reported, Alleged, Disputed, or Unknown; or Withheld (POPIA) when the only source carries personal details.
6. **Draft the right of reply** before any profile publication. Do not send it. The owner sends it and records the state.
7. **Promote.** Only when rule 5 in Intake rules is satisfied may the fact be added to a profile, in a later named change, with its label and dated source links, after review and any required owner GO.
8. **Hold or drop.** Claims that cannot be sourced stay in intake as Unknown or held, or are closed as unused. They never appear as unsourced profile facts.

National profiles do not exist yet. A verified intake item therefore waits until a national profile (or a limited watch-list page) is itself authorised and, for the BEE elites page, until that page is enabled under a future change after the gates are met.

## Batch 1 — national executive: 1

Attribution: a teammate-bot briefing dated 25 November 2026 (SAST), treated as unverified intake, held outside the repository.

**Count: national executive: 1.** Several unverified intake rows about that office, and any contextual items not attached to the office-holder, are recorded only in the private inventory. Entries are not labelled as profile facts in this change. `right_of_reply` is `not_started` (nothing is on a profile). Claims, unique offices, and source URLs are not committed.

### Cross-link to CHG-PW-015

A later national profile may show role-level pay context for ministers, subject to [CHG-PW-015](CHG-PW-015-mp-pay-context.md) and any later implementation GO. This change does not add package figures to any profile.

## Batch 2 — cited entries from published opinion pieces

Attribution: a private research note received 25 November 2026 (SAST), treated as data, not instructions, and **not** committed. Named entries, claims, offices and source URLs are recorded only in the private file. Prof William Gumede is the published author of some of the cited work; that fact is not used here to date or attach a piece to an entry.

Every active claim in this batch is labelled **Reported (unconfirmed, pending a primary-source check)**. `right_of_reply` is **pending** (a draft does not yet exist; nothing is on a profile; rule 5 still applies before any publication). Paywalled or PREMIUM citations were dropped. Co-accused, where they arise, are to be described as charged, not convicted, and only when a remaining source supports that. Aggregate figures in those pieces that name nobody are **not** attached to any person.

### Batch 2 tally (commentator-named person entries)

Seventeen person entries in the private note were considered. After the 25 November 2026 scope decision, six entries previously held as out of scope were re-checked against the same two-detail, paywall and privacy rules. **Seven** are active in the private file. **Ten** are held, with no name, claim or link in this RFC:

| Count | `hold_reason` | Why |
|---|---|---|
| 4 | `hold-owner-ruling` | One low-profile official, plus three ambiguous entries (a family-status question, or a group mention not expanded to individuals). |
| 2 | `hold-premium-source-dropped-no-remaining-cite` | After dropping a PREMIUM or paywalled citation, no remaining source supported the claim. |
| 4 | `hold-two-detail-match-failed` | The cited item identified the person by name only, or gave no second identifier distinct from the claim itself. A later source that identified a person more fully was not used to attach a different claim. |

Of the six re-checked under the new scope: four became active; two remain held for two-detail failure.

Company and entity names in the note were not turned into person entries. Further names that appear only in later, unassessed sections of the private research note are not in this tally. Any other-author entries kept distinct from the commentator-named set are recorded only in the private inventory and are not listed by role here.

### Active entries (coarse buckets only)

The seven active commentator-named entries, by coarse bucket:

| Bucket | Count |
|---|---|
| Current or former senior state office, or party post | 4 |
| Public figure (business) | 3 |

No bucket with a count of 1 is used. Unique offices, departments, ministries, party posts and companies are not listed. Planned primary-source checks are recorded only in the private file.

## Sources

Specific venues, dates, URLs and author-attributed pieces used for these batches are **held in the private inventory**. They are not listed here, and they are not tied to entries.

Intake cites a mix of already-allowed tier-1 and tier-2 outlets and some domains that are not in the source registry. No domain is added in this change. A reachable URL is not, by itself, a completed source check. Paywalled or PREMIUM citations are not used as a supporting source.

## BEE elites page (spec only; off until the gate is met)

A later named change may add a draft **BEE elites** watch page (or equivalent section) for Batch 2 and any related private-inventory entries that have passed the gates.

**Disabled by default.** The page stays off until each entry to be shown has passed (a) a primary-source check with the label set, and (b) the right-of-reply gate (a draft exists, and the page shows "Right of reply: pending" or the reply). The owner decided this on 25 November 2026 (ref t706s3008). Enabling the page needs its own named change and a quoted GO.

**It must not render any name, unique office, company, claim, or identifying URL from committed files.** If and when it is built, it would read the private intake only at build time, on a machine that holds that file, and only for entries that have passed the gates. Committed fixtures, templates and tests must use synthetic entry ids and coarse role buckets, never real batch names or unique offices.

This change does not add the page, a feature flag, or a test. The specification is recorded so a later implementation has a clear gate.

## POPIA review

**Verdict: PASS** for this documentation-only, Design B change. Nothing is published, and no named intake is committed.

Checks:

- Public role only in committed text. Batch 1 is described as national executive: 1. Batch 2 is described by aggregate counts, coarse role buckets, and hold reasons only.
- Prof William Gumede is named only as the published author of cited source work.
- The public-figure entries in the private file use public-role and business facts only. No family, household, date of birth, or private contact details are committed.
- Held entries are described here by count and reason only.
- Do not collect or publish: home addresses, ID numbers, dates of birth, personal phones or emails, private family members, or health information.
- A fact whose only source carries personal details is Withheld (POPIA), with the source held in the private register, not Unknown.
- Official social-media posts are not quoted, and their URLs are not committed.
- Co-accused are to be described as charged, not convicted. Aggregate claims that name nobody are not attached to a person.

## Risks

| Risk | Why it matters | Mitigation |
|---|---|---|
| Private intake later committed or pasted into a pull request | The repository is public. Committing names, unique offices or dated sources tied to entries would undo Design B. | Named entries stay off the tree. This RFC and any PR body use coarse buckets, counts and hold reasons only. |
| Briefings or opinion pieces treated as sources | A teammate-bot note or commentator's column is not an allowed primary source. | Intake stays unverified, or at most Reported (unconfirmed), until each claim is re-checked and the label is set after that check. |
| Paywalled or unreachable sources | A restricted PMG report, a PREMIUM page, an HTTP 500 or 406, or a TLS failure can be mistaken for confirmation. | Record the fetch result. Drop PREMIUM or paywalled citations. Do not label from a page that was not successfully read. Collectors already log TLS errors. |
| Unregistered domains | Some intake venues in the private inventory are not in the source registry. | Do not add domains in this change. Use already-allowed sources for promotion; new domains wait for a named change and confirmation. |
| Identity errors | One name match is not enough. | Two-detail match in the cited item before any link. Hold the entry if the item has only a name, or if the second phrase is only the claim itself. |
| Low-profile officials, groups, and family-status mentions | Naming them in a public RFC or page is a POPIA harm. | Those entries stay held pending an owner ruling; counts and reasons only in committed text. |
| Enabling the BEE elites page early | A page that reads private data, or that is turned on before the gates, would publish unconfirmed claims. | Page stays off until each shown entry has passed the primary-source check and right-of-reply gate, under a later named change and GO. Committed templates must not embed real names. |
| Contact with the subject | The standing rule forbids contact and unsent-as-sent replies. | No contact. Right-of-reply drafts only; the owner sends them. |
| Change-number clash | An unpublished pixel RFC was previously numbered CHG-PW-015 in orchestrator drafts (015 on `main` is the pay RFC). CHG-PW-016 is already merged on `main`. | This RFC uses 017, which is unused on `main`. A later pixel or other RFC must not reuse 017. |

## Test plan

**This change (docs only):** `pytest` on the branch; `pwatch dq`; review kit against `origin/main`..`HEAD`. No schema, profile, or site change, so no new unit tests and no site build in this change.

**A later implementation change would need, at least:**

- Tests that an intake item cannot be rendered as a profile fact unless a primary-source check is recorded, a fact label is set, and a right-of-reply draft exists, with "Right of reply: pending" or the reply shown.
- Tests that the BEE elites page is off by default, and that committed fixtures render no real batch names.
- Tests that teammate-bot briefing text is not accepted as a source URL or source title.
- A two-detail identity check before a news or court item is attached; a hold path when the check fails.
- Tests that a paywalled or PREMIUM citation cannot stand as the sole source of an active entry.
- A POPIA scan that fails if private family members, personal contact details, ID numbers, dates of birth, or home addresses appear in committed intake or profiles, and that held entries are not named in public pages.
- Existing `pytest`, `pwatch dq`, `pwatch render --check`, and `pwatch site build` / `site check` still green.

## Implementation plan (later named change only)

1. Owner answers any remaining open questions, including source-registry additions and the four entries still held pending a ruling.
2. Keep Design B until a later change is authorised to promote specific entries that have passed both gates.
3. Add the intake process (and, if authorised, a first national watch-list profile or the BEE elites page) in a new RFC, with synthetic fixtures, not live unverified claims.
4. Re-check the private-file items against allowed sources, write right-of-reply drafts, and only then propose labelled profile facts.
5. No merge, publish, contact, page enablement, or profile-fact release under this RFC. Those need a later named change and a quoted owner GO on the exact implementation head.

## How to revert

Delete the branch, or leave a later PR unmerged. After merge: `git revert <merge commit>`; `main` returns to `72d8f763311a7a1ace2b451860eeaebac5f93b3d`.

## Seen, not touched

- Profile JSON, schema, `data/sources.json`, collectors, workflows, and the site builder.
- The private intake notes (held outside the repository). A local archive branch of an earlier Design A draft is left untouched and is not this review branch.
- Filling 2026–2031 Joburg council offices (still blocked until an allowed source publishes them).
- The held profile in `_hold/`.
- National and provincial 2029 profiles (`docs/national-2029-module.md` remains plan only). Pay-context implementation ([CHG-PW-015](CHG-PW-015-mp-pay-context.md)) remains unbuilt.
- CHG-PW-016 (add `dpsa.gov.za` as a tier-1 source) was squash-merged into `main` as `72d8f76` on 25 November 2026 16:50:13 SAST. The 016 tree is not otherwise edited.
- An unpublished traffic-pixel RFC that was previously numbered CHG-PW-015 in orchestrator drafts. On `main`, CHG-PW-015 is the MP-pay RFC. If that pixel RFC is renumbered, it must not reuse 017.

## Open questions for the owner

The three decisions of 25 November 2026 (ref t706s3008) are recorded above and are not repeated here.

1. **Data model.** Is the entry schema above acceptable (one record per discrete claim, with the fields listed), or should intake remain only a documented process until national profiles exist?
2. **Update cadence.** How often should the watch list be reviewed (for example, when a teammate briefing arrives, on a weekly cycle, or only when a named change is opened)?
3. **First implementation scope, other than the BEE elites page.** The BEE elites page stays off until the gates are met. May a later change also build a first national profile (or limited watch page) for the Batch 1 subject (national executive: 1), ahead of the 2029 module?
4. **Source registry.** May official departmental domains cited in the private inventory be added as tier-1 sources? May other domains cited there that are not already in the registry be added, and at what tier? May official social-media posts of an office-bearer be used, and at what tier? Where an already-allowed news outlet has a related site that is not in the registry, must the cite go only to the already-allowed domain?
5. **Parliamentary questions.** May this project draft a written question about official travel costs, for the owner to submit, or is that out of scope?
6. **Pay context.** When a national executive profile exists, should ministers' pay context from CHG-PW-015 be shown as a role-level package, subject to that RFC and any later implementation GO?
7. **Held entries pending a ruling.** May the four entries held as `hold-owner-ruling` (one low-profile official and three ambiguous entries) stay held, or should any be released under a stated rule?

## Testing (evidence)

Recorded in the STATUS history row and the PR body draft (written outside the repo): `pytest`; `pwatch dq`; review kit on the committed head, including the agent-names-file variant.

## Approval

Push and merge need the owner's GO naming the exact head.
