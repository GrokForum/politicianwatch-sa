# CHG-PW-015 — MP and councillor pay context (RFC draft only)

| Field | Value |
|---|---|
| Requested by / date (SAST) | Taken up on 25 November 2026 after the owner resumed all work, relayed by the orchestrator. The item comes from a source pack compiled 21 November 2026 (sources only, not a build GO). |
| Author / builder | author bot |
| Reviewers | two reviewers |
| Change authority | Owner (GO on the exact head to push or merge). Push and merge need the owner's GO naming the exact head. |
| Type | Standard — low (documentation only). A later implementation that publishes package figures next to named office-holders would be at least Normal-high. |
| Environment | DEV. No code, data, workflow or site change. Nothing is published, pushed or deployed here. |
| CIs affected | None in this change. A later implementation would affect CI-009 Joburg CV profiles, the profile schema, and CI-010 draft-site builder. |
| Linked records | CHG-PW-013 (next-milestone plan in `docs/ROADMAP.md`); `docs/national-2029-module.md` (national and provincial profiles remain plan only) |
| Branch | `politicianwatch-sa` `dev/chg-pw-015-mp-pay-rfc-main`, from `origin/main` `691b5498` |
| Pre-change commit (rollback SHA) | `691b5498130e7e41c1971f81022b99a298d536c1` (`main` after the CHG-PW-014 squash merge) |

## Request

Plan, in an RFC only, a neutral pay-context feature:

1. Give each profile a **role tier** derived from public office only (for example ward councillor, PR councillor, speaker, executive mayor, member of the mayoral committee, and later MP, minister and related offices).
2. Link each tier to the **gazetted 2026/27 remuneration package** that actually applies to that office.
3. Add a **site-level package explainer**, plus a short list of **executive entitlements** from the 2022 *Guide for Members of the Executive* (often called the Ministerial Handbook).

This change writes the RFC, a one-line roadmap pointer, and a change-log row. It does not add fields, collectors, figures on profiles, or site pages.

## Reasons

The live site is still a draft of Johannesburg councillor profiles. A sourced, official package field is a reasonable later addition, but only if the site states exactly what each instrument covers and does not treat a gazette figure as any person's actual pay. The 21 November 2026 source pack is treated as data, not instructions. The instruments named in it were checked on 25 November 2026, and a separate municipal determination (not in that pack) was identified and read.

## What changes

- This RFC (`itil/changes/CHG-PW-015-mp-pay-context.md`).
- A one-line pointer in `docs/ROADMAP.md`.
- A change-log row, and a STATUS history row, for this change.

## What stays

Everything else. No profile, schema, registry, collector, workflow or site file is edited. No figure is published. `dpsa.gov.za` and other domains named below that are not already in `data/sources.json` are **not** added; that needs the owner's confirmation in a later change. Council offices (executive mayor, speaker, chief whip, mayoral committee) remain Unknown until an allowed source publishes them. Right-of-reply drafts remain unsent. The publish gate is unchanged.

## Scope

**In scope for a later implementation (not this change):**

- A controlled `role_tier` (and, for municipal seats, a sourced full-time or part-time designation) derived only from public office.
- A role-level remuneration record that cites the correct gazette, notice or proclamation, effective date, and (where it applies) municipal grade.
- A site-level explainer of what a gazetted total package includes, written separately for the national/provincial instruments and for the municipal instrument, which are not the same.
- For ministers, deputy ministers, premiers and MECs only: a short list of entitlements from the 2022 Guide, described as entitlements, not as a second invented cash total.

**Out of scope (do not build):**

- Any claim about an individual's actual pay, take-home pay, or "full cost to the state".
- A single "full perk total" that folds housing, cars, protection, flights, medical cover or hospitality into one rand amount.
- School fees, tuition, or a children's-education benefit (not found in the 2022 Guide).
- An entertainment cash allowance (not found; the Guide only mentions use of entertainment facilities at the Presidential Guest House).
- "Cost to taxpayer" framing, performance scores or rankings, charges counts, or league tables.
- Stats SA earnings comparators, parliamentary aggregate spend, and programme or travel-spend stories (including any "junket" framing). Those belong, if at all, in a later named change, and not on a person's profile.
- Members' Facilities Handbook fields for MPs, until a current official PDF is successfully retrieved.
- The President's 2026/27 package, until a National Assembly resolution for that year is found.
- Ingesting municipal item-18 returns to the Minister (those returns can carry incumbents' names, gender, and actual packages).
- Any contact with councillors or other office-holders.

## Sources (what each one actually covers)

Verified by streamed GET on **25 November 2026 (SAST)**, from this machine. HTTP 200, no TLS error. PDFs were not committed. Gazette copies are the Gazette Finder GPW issues already allowed as tier 1. The 2022 Guide was fetched from `dpsa.gov.za`, which is **not** in `data/sources.json`; it is recorded here as a proposed source and is not added in this change.

### 1. Government Gazette 55765 — does *not* cover municipal councillors

- **Instrument:** Government Gazette **No. 55765**, 20 November 2026 (Vol. 737). Official GPW PDF via Gazette Finder: `https://www.gazettefinder.co.za/gazettes/government-gazette/2026/55765/government-gazette-55765-2026-11-20.pdf` (HTTP 200, 16 pages, 871,286 bytes, SHA-256 `115cae7b631bbf1b4f48307d205864b1e103a867fbdf2731d42c43026277ac94`).
- **Issuer:** The Presidency, by presidential proclamation under the Remuneration of Public Office Bearers Act, 1998 (Act 20 of 1998).
- **Contents (contents page, as printed):** only three proclamations.
  - **Proclamation 355** (s 4(1) of the Act): determination of **salaries and allowances** of the **Deputy President, Ministers and Deputy Ministers** for 2026/2027. This is a determination of the package, not an upper-limit notice. Schedule amounts from **1 April 2026**, headed "as adjusted by 3.5%": Deputy President R3,390,057; Minister R2,881,528; Deputy Minister R2,372,999.
  - **Proclamation 356** (s 6(1) of the Act): determination of the **upper limit** of salaries and allowances of **Premiers, Members of the Executive Councils, and Members of the Provincial Legislatures** for 2026/2027. These are **upper limits**, not automatically what each legislature pays. Schedule examples from 1 April 2026: Premier R2,712,085; MEC / provincial Speaker R2,372,999; Member of a Provincial Legislature R1,321,421.
  - **Proclamation 357** (s 3(1) of the Act): determination of **salaries and allowances** of **Members of the National Assembly and permanent delegates to the NCOP** for 2026/2027. This is a determination of the package, not an upper-limit notice. Schedule examples from 1 April 2026: Speaker of the National Assembly / Chairperson of the NCOP R3,390,057; ordinary Member of the National Assembly and permanent NCOP delegate **R1,365,315**; other parliamentary offices as printed in Schedule 1.
- **Package composition (all three proclamations, as printed):** the total remuneration package includes (1) a basic salary component equal to **60%** of the total package (the pensionable salary); (2) **R120,000** a year to which s 8(1)(d) of the Income Tax Act, 1962 applies, included in the basic salary component; (3) an employer's pension contribution equal to **22.5% of pensionable salary**; and (4) a flexible portion for the remainder.
- **Not in Gazette 55765:** municipal councillors; the President (whose salary is determined separately by a National Assembly resolution under s 2 of the Act); judges, magistrates, or traditional leaders.
- **Note, not resolved in this RFC:** each of Proclamations 355, 356 and 357 repeals "Proclamation No. 7005" in Government Gazette 53965 of 16 January 2026. The 21 November source pack recorded that Gazette 53965 used three notices (7004 executive, 7005 provincial, 7006 Parliament). This RFC did not re-read Gazette 53965. A later change should read that gazette before treating the repeal citation as the prior instrument for all three offices.
- **Note on the "3.5%" heading:** publish the printed rand amounts. Do not invent a recalculated "true 3.5%" figure. The source pack recorded that a straight 3.5% on the 2025/26 totals does not reproduce these 2026/27 printed amounts. This RFC did not re-read Gazette 53965 to repeat that arithmetic.

### 2. Government Gazette 55749 — municipal councillor upper limits

This is a **different gazette** from 55765. Johannesburg councillors fall under this instrument, not under 55765.

- **Instrument:** Government Gazette **No. 55749**, 17 November 2026 (Vol. 737), Department of Cooperative Governance and Traditional Affairs, Government Notice **8194**. Official GPW PDF via Gazette Finder: `https://www.gazettefinder.co.za/gazettes/government-gazette/2026/55749/government-gazette-55749-2026-11-17.pdf` (HTTP 200, 20 pages, 949,354 bytes, SHA-256 `cba454880d106682689e6f429e06aad01ff3acc18b9b66bce380ac5300d28545`).
- **Issuer:** the Minister of Cooperative Governance and Traditional Affairs, under ss **7(1), 8(5)(a) and 9(5)(a)** of the Act (signed 16 November 2026).
- **What it is:** the determination of the **upper limits** of the salaries, allowances and benefits of the different members of municipal councils. It is not a statement of what any named councillor is paid.
- **How actual pay is set (preamble, as printed):** the salary and allowances of a councillor are determined by that municipal council, by a majority resolution, in consultation with the provincial MEC for local government (meaning MEC concurrence before implementation), having regard to these upper limits, the municipal financial year, affordability, and Cabinet-approved austerity measures.
- **Effective date:** **1 July 2026** (item 20). This notice replaces Government Gazette 54179 of 20 February 2026 (GN 7159). The municipal year and the 1 April 2026 national/provincial date in Gazette 55765 are not the same.
- **Grading (items 2–4):** a council's grade (1 to 6) is the sum of points for **total municipal income** and points for **total population** (Statistician-General, 2022 Census). Total municipal income is taken from the 2025/26 audited statements (item 1, which defines that year), or from 2024/25 if those are not yet available (item 19(1)). Gazette 55749 **does not itself assign the City of Johannesburg a grade**. Grade must not be assumed from "metro" status, or from news reports that use Johannesburg as a Grade 6 example. Publish a grade on a Joburg profile only when the council's grading and MEC concurrence (or another allowed official source that names the municipality) have been read.
- **Full-time upper limits of the annual total remuneration package (item 5, as printed):**

  | Grade | Executive mayor or mayor | Speaker, deputy executive mayor or deputy mayor | MMC, executive committee member, whip, or chairperson of a subcouncil | Chairperson of an oversight committee |
  |---|---:|---:|---:|---:|
  | 6 | R1,716,041 | R1,385,901 | R1,305,503 | R1,267,207 |
  | 5 | R1,279,455 | R1,023,560 | R959,590 | R931,443 |
  | 4 | R1,092,295 | R873,842 | R819,596 | R795,196 |
  | 3 | R1,051,990 | R841,593 | R788,996 | R773,143 |
  | 2 | R985,032 | R788,027 | R745,808 | R723,933 |
  | 1 | R956,323 | R772,350 | R724,075 | R702,836 |

- **Part-time upper limits (item 8, as printed), including "other part-time members":**

  | Grade | Executive mayor or mayor | Speaker, deputy executive mayor or deputy mayor | MMC, executive committee, or whip | Chairperson of an oversight committee | Other part-time members |
  |---|---:|---:|---:|---:|---:|
  | 6 | R961,905 | R813,731 | R728,301 | R706,936 | R642,666 |
  | 5 | R713,769 | R571,016 | R535,328 | R519,620 | R404,202 |
  | 4 | R609,364 | R487,501 | R457,023 | R443,617 | R345,675 |
  | 3 | R586,874 | R469,459 | R440,163 | R427,242 | R332,905 |
  | 2 | R549,517 | R439,613 | R412,141 | R400,051 | R311,728 |
  | 1 | R533,505 | R426,802 | R400,131 | R387,585 | R302,279 |

- **Municipal package composition is not the 60% / R120,000 / 22.5% structure.** Item 1 defines the total remuneration package as the basic salary, the motor-vehicle allowance (item 9(1)), the housing allowance (item 9(2)), and the municipal contributions to a pension, provident or retirement annuity fund and to a medical aid scheme (item 13). A councillor may structure a vehicle or housing allowance *within* that package.
- **In addition to** that package, the notice sets separate upper limits, among others, for a cell-phone allowance (**not exceeding R3,600.00 a month**, item 11) and mobile data bundles (**not exceeding R317 a month**, item 12). Those two caps must not be silently added together and presented as a single gazetted allowance.
- **Tools of trade** (item 15) and **special risk cover** (item 14) sit outside the total remuneration package. They are listed as official provisions, not as a second personal cash total. Official accommodation and furniture for a full-time executive mayor or mayor apply "where it currently exists".
- **Full-time vs part-time:** a full-time councillor is one elected or appointed to an office designated full-time in terms of s 18(4) of the Municipal Structures Act, 1998. This RFC does not assume that a Joburg ward or PR seat is part-time or full-time.

### 3. Guide for Members of the Executive (2022)

- **Document:** *Guide for Members of the Executive*, approved by the President, effective **13 April 2022**. URL: `https://www.dpsa.gov.za/dpsa2g/documents/acts&regulations/Guide_for_members_of_the_executive/Guide%20for%20Members%20of%20the%20Executive%202022.pdf` (HTTP 200, 32 pages, 829,996 bytes, SHA-256 `7ffd4ce3a56260d703e714378152a18b3d6b143e1b309ff1982eb4062653dae6`).
- **Who it covers (as printed):** Ministers, Deputy Ministers, Premiers and Members of the Executive Council. It does **not** cover ordinary MPs, NCOP delegates, or municipal councillors.
- **Published entitlements (verified in this PDF; list as entitlements, not as a second rand total):**
  - One official residence per seat of office. One state-owned residence may be occupied free of charge (subject to a Public Works lease). A second state-owned residence is rented at a rate set by the Ministers responsible for Public Works and Finance; the member is personally responsible for the related tax implications. All procurement, upkeep and maintenance of a private residence designated as official stay with the member. Public Works pays water and electricity on official residences, not rates or taxes on private residences.
  - Official vehicles: purchase cap **R700,000** inclusive of VAT, security upgrades and maintenance plans, to be adjusted annually by the Minister responsible for Finance in consultation with the Ministers responsible for Police, Transport and State Security. Replace at 120,000 km or 5 years, whichever comes first. Whether that cap has been adjusted since 2022 was not traced in this RFC.
  - SAPS VIP drivers and protectors; the department provides and maintains official vehicles and cell phones for those SAPS personnel. Not costed per member in the Guide.
  - One Household Aide post per official residence, paid by the department (Ministers and Deputy Ministers eligible for two posts, Premiers and MECs one, if Public Works does not already provide the service). Extra domestic staff is at the member's expense.
  - National members and their spouses are jointly eligible for 20 single domestic economy-class tickets a year, at the department's expense; unused tickets lapse. Each dependent child is eligible for six single domestic economy-class tickets a year to reunite with their parents in either seat of office. Ticket *counts* are published; there is no official rand total per member.
  - International official travel is a departmental cost, with limits (including that dependent children who accompany official visits abroad do so at the member's own cost). Daily allowances refer to the DPSA Financial Manual, not a published annual cash amount in this Guide.
- **Not found in this Guide (full-text search of the 32-page PDF):** school, tuition, bursary, medical aid, or PARMED. The only "entertainment" provision found is use of entertainment facilities at the Presidential Guest House, not a cash allowance.
- **POPIA:** the Guide describes family travel and residence rules in general terms. The site may summarise those official rules. It must never name or describe a particular office-holder's family, home, or private contacts.

### 4. Source pack and instruments not re-fetched in this RFC

The 21 November 2026 source pack also cites Gazette 53965 (2025/26 presidential determination), Commission recommendations (Gazettes 53875 and 55446), Presidency media statements, a 3 March 2026 National Assembly resolution on the President's salary, Stats SA releases, a Joint Standing Committee readout of Parliament's 2025/26 annual report, and Parliament's Members' Facilities Handbook. Those URLs were not re-fetched in this session (a cap of about eight fetches was applied; three official PDFs were retrieved, all HTTP 200). They are not implementation sources for this RFC. The pack itself recorded that the live Members' Facilities Handbook PDF could not be retrieved on 21 November 2026.

## Data model sketch

All new fields are public-role facts, labelled and sourced, or explicit Unknown / Withheld (POPIA). None of this is implemented here.

```text
role_tier:
  value: enum derived from public office only
    municipal (pilot):
      ward_councillor | pr_councillor |
      chair_oversight | whip | mmc_or_exco |
      deputy_executive_mayor | speaker | executive_mayor
      (plus later district or organised-local-government sitting roles if sourced)
    national / provincial (later module):
      mp | permanent_ncop_delegate | whip | committee_chair | ...
      deputy_minister | minister | deputy_president | president |
      mpl | mec | premier | provincial_speaker | ...
  time_basis: full_time | part_time | not_applicable | unknown
  source: the public instrument that names the office (gazette roster, council
          notice, Hansard, Presidency list). Never inferred from pay.

remuneration_context:
  instrument_kind: determined_package | upper_limit
  instrument: { gazette, notice_or_proclamation, date, effective_from, act_section, url }
  municipal_grade: 1..6 | unknown     # required for municipal upper limits; must be sourced
  amount_zar_per_year: integer        # the printed gazette figure for that tier (and grade)
  label: Confirmed | Unknown | Withheld (POPIA)
  display_as: "gazetted total remuneration package for this office"
            | "gazetted upper limit of the total remuneration package for this office"
  not_stored: actual_pay, take_home, "full perk total", personal allowances claimed
```

Rules:

- `seat_type` (ward / PR) stays what it is: how the person was elected. `role_tier` is the office they hold. A ward councillor who is later confirmed as an MMC has both.
- Until Joburg council offices are published, the only honest municipal tiers are `ward_councillor` or `pr_councillor`, with office-holder tiers Unknown.
- Until grade and full-time or part-time designation are sourced, `amount_zar_per_year` stays Unknown. Do not pick a cell from the schedule by assumption.
- Cite Gazette **55749** for municipal councillors and Gazette **55765** for the national executive, MPs, NCOP delegates, and provincial upper limits. A later DQ rule should fail a cross-cite.
- The President's package, if ever shown, cites a National Assembly resolution, not Gazette 55765.
- Package composition belongs in a site-level explainer, not as a unique recalculation per person.
- Executive Guide entitlements attach only to tiers the Guide actually covers.

## UI wording drafts

Neutral and factual. Package figures are gazetted packages or upper limits for the **role**, not a claim about any individual's actual pay. Do not use "cost to taxpayer", "salary" as if it were cash only, "full cost to the state", rankings, or performance language.

**Site-level explainer (national / provincial offices under Gazette 55765):**

> Public office-bearers in the national executive, the National Assembly, the permanent delegates to the NCOP, and (as upper limits) the provincial legislatures, are paid a total remuneration package set in the Government Gazette. For 2026/27 the instrument is Government Gazette 55765, with amounts from 1 April 2026. The figure is a total package, not a cash salary alone. It includes a basic salary component equal to 60% of the package (the pensionable salary), an amount of R120,000 a year under section 8(1)(d) of the Income Tax Act, 1962, included in that basic component, an employer's pension contribution equal to 22.5% of pensionable salary, and a flexible portion for the remainder. Official housing, vehicles, protection, travel and other facilities, where they apply, are provided under separate official rules and are not included in that rand figure as a second published cash total. Gazette 55765 does not set the President's salary, and it does not set municipal councillor pay.

**Site-level explainer (municipal councillors under Gazette 55749):**

> Pay for municipal councillors is subject to upper limits set by the Minister of Cooperative Governance and Traditional Affairs in Government Gazette 55749, with effect from 1 July 2026. The figure shown for a role is the upper limit of the annual total remuneration package for that office in a council of a stated grade, not a statement of what any named councillor is paid. The council determines the actual package by a majority resolution, with the concurrence of the provincial MEC, within those limits and subject to affordability. The total package, as defined in that notice, includes a basic salary and may include a motor-vehicle allowance, a housing allowance, and municipal contributions to a pension or medical scheme. Some other allowances in the same notice, including a cell-phone allowance and a data-bundle allowance, may be paid in addition to that package, each within its own cap. A council's grade is calculated from official municipal income and census population figures; this site records a grade only when an allowed official source for that municipality has been read.

**On a profile, when the tier, instrument, and (if municipal) grade and time-basis are all sourced:**

> Gazetted upper limit of the total remuneration package for this office: R[amount] a year (Government Gazette 55749, from 1 July 2026, grade [N], [full-time | part-time]). This is the legal ceiling for the role. It is not a statement of what this councillor is paid.

**On a later MP or minister profile:**

> Gazetted total remuneration package for this office: R[amount] a year (Government Gazette 55765, from 1 April 2026). This is the official package for the office. It is not a statement of additional official facilities, and it is not a cash salary alone.

**When a field cannot yet be shown:**

> Remuneration for this office: Unknown. The applicable gazette has been identified, but this site does not yet have an allowed official source for [the council's grade / whether the seat is full-time or part-time / the office held].

**Executive entitlements (minister, deputy minister, premier, MEC only), as a list, not a sum:**

> Members of the executive are also covered by the Guide for Members of the Executive (effective 13 April 2022). That Guide provides for official residences, official vehicles within a published purchase cap, SAPS VIP protection, a household aide, and limited official and family travel, on the terms set out in the Guide. Those are entitlements and tools of trade, not a second published cash total, and they are not a description of any one person's household.

## POPIA review

**Verdict: PASS** for this documentation-only change. Nothing is published, and no personal information is added to the repo.

Checks:

- Public role only. The tier is derived from public office, not from private life or from pay.
- Gazette figures are official role-level amounts, not a person's banked pay, assets, or household finances.
- Do not collect or publish: home addresses, ID numbers, personal phones or emails, private family members, health information, vehicle ownership or travel logbooks (item 9 of Gazette 55749), property, asset or beneficiary details used for special risk cover (item 14), or the item-18 ministerial returns (names, gender, and actual packages).
- Family travel and residence rules in the 2022 Guide may be summarised as general official entitlements. Never attach them to a named relative.
- A fact whose only source carries personal details is Withheld (POPIA), with the source held in the private register, not Unknown.
- The Minister of Cooperative Governance and Traditional Affairs is named only as the public official who issued Notice 8194.
- Gazette 55765 and 55749 also contain unrelated Government Printing Works administrative material (including payment-account details). That material is out of scope and must not be copied into the site, this repo's public docs, or a PR body.
- Proposed new source domains are not added in this change.

## Risks

| Risk | Why it matters | Mitigation |
|---|---|---|
| Stale figures | Determinations are annual. A 2026/27 figure left in place after the next gazette would be wrong. | Store the gazette number, notice, and effective date with the amount. A later refresh change is required when a new determination is published. The site wording should name the instrument and the start date. |
| Municipal grade | Upper limits vary by grades 1–6. Publishing a Grade 6 cell for Johannesburg without a sourced grading is an invented fact. | Grade stays Unknown until an allowed official source for that council is read. News examples are not enough. |
| Full-time vs part-time | The two schedules differ substantially (for example a grade 6 "other part-time member" is R642,666; there is no "ordinary councillor" cell in the full-time table). | Time-basis stays Unknown until a s 18(4) designation or equivalent official source is read. |
| Actual pay versus the cap | Gazette 55749 is an upper limit. A council may resolve a lower package. Gazette 55765 Proc 356 is also an upper limit (provincial). Procs 355 and 357 are determinations of the package, still not a payslip. | UI must say "upper limit" or "gazetted package for this office", never "this person earns". |
| Wrong gazette for the role | Linking a Joburg councillor to Gazette 55765, or an MP to Gazette 55749, would be a false attribution. | Separate instruments in the data model and a later DQ cross-cite failure. |
| Collapsing two package definitions | The national/provincial 60% / R120,000 / 22.5% structure is not the municipal definition. | Two explainers, not one. |
| Allowances treated as in or out of the package | Municipal cell-phone and data caps are in addition to the total package. Vehicle and housing allowances are inside it. | Follow the notice item by item in the explainer. |
| Handbook entitlements treated as cash | The 2022 vehicle cap and ticket counts are not an annual personal total. The cap may also have been adjusted since 2022. | List entitlements; do not sum them. Record the Guide date. |
| Item-18 or special-risk data | Those provisions can expose personal property, family beneficiaries, gender, or actual pay. | Never ingest those returns. |
| Office still unpublished | Most current Joburg `positions` values are Unknown. Guessing mayor, speaker or MMC would be a false tier and a false package. | Office-holder tiers wait for an allowed source, as in the existing council-offices rule. |

## Test plan

**This change (docs only):** `pytest` on the branch; review kit against `origin/main`..`HEAD`. No schema, profile, or site change, so no new unit tests and no site build in this change.

**A later implementation change would need, at least:**

- Schema and DQ tests for `role_tier`, `instrument_kind`, municipal grade, and time-basis, including Unknown when any of those are missing.
- A DQ failure if a municipal councillor fact cites Gazette 55765, or if an MP, minister, deputy minister or Deputy President fact cites Gazette 55749, or if a President fact cites 55765.
- A DQ or site-check failure if copy on a profile presents the figure as the person's actual pay, as "salary" alone, or in "cost to taxpayer" language.
- Tests that printed gazette amounts are used as-is (no silent 3.5% recomputation).
- Site tests that the municipal and national explainers both appear as drafted, and that executive entitlements render only for tiers the 2022 Guide covers.
- A POPIA scan that fails if item-14 / item-18 personal fields, family names, or personal contact details appear in built pages or committed profiles.
- Mutation checks that those gates actually fail when broken.
- Existing `pytest`, `pwatch dq`, `pwatch render --check`, and `pwatch site build` / `site check` still green.

## Implementation plan (later named change only)

1. Owner answers the open questions, including source-registry additions.
2. Add the schema fields and explainers in a new RFC, with fixtures, not live figures, until grade, time-basis and offices are sourced.
3. For Joburg, attach `ward_councillor` / `pr_councillor` from the existing gazette roster; leave higher office tiers Unknown until the City (or another allowed source) publishes them.
4. Commit gazette PDFs only through the existing raw-manifest / fetch-source path, if the owner wants them as evidence; do not commit Government Printing Works administrative pages into public content.
5. No merge, publish or profile-figure release without a quoted owner GO on the exact implementation head.

## How to revert

Delete the branch, or leave a later PR unmerged. After merge: `git revert <merge commit>`; `main` returns to `691b5498130e7e41c1971f81022b99a298d536c1`.

## Seen, not touched

- Profile JSON, schema, `data/sources.json`, collectors, workflows, and the site builder.
- Filling 2026–2031 Joburg council offices (still blocked until an allowed source publishes them).
- The held profile in `_hold/`.
- National and provincial 2029 profiles (`docs/national-2029-module.md` remains plan only).
- Stale CHG-PW-013 "not merged" wording in older STATUS and change-log rows on `main` (historical rows, outside this change except where `docs/ROADMAP.md` was already being edited).
- Gazette 53965, Commission recommendations, the National Assembly resolution on the President's salary, Stats SA releases, and the Members' Facilities Handbook (not re-fetched in this session).

## Open questions for the owner

1. **Timing.** Should a later implementation wait until Johannesburg has published its executive mayor, speaker, chief whip and mayoral committee, or may ward and PR tiers be shown first, with higher offices left Unknown?
2. **Johannesburg grade.** May a grade (including Grade 6) be shown only after the City's own grading calculation and MEC concurrence, or another allowed official source that names the municipality, has been read? This RFC recommends waiting. Gazette 55749 does not itself grade Johannesburg.
3. **Full-time or part-time.** May the s 18(4) designation for Joburg seats be recorded only from an allowed official City or MEC source?
4. **Source registry.** May `dpsa.gov.za` be added as a tier-1 source for the 2022 Guide? The Guide was fetched for this RFC but is not in `data/sources.json`. Other pack domains (`gov.za`, `remcommission.gov.za`, `cogta.gov.za`, `statssa.gov.za`) can wait until a fact actually needs to cite them.
5. **First implementation scope.** Should the first build be Joburg councillor context from Gazette 55749 only, with Gazette 55765 and the 2022 Guide held for the later national and provincial module?
6. **Additional municipal allowances.** Should the site-level municipal explainer mention the cell-phone (R3,600 a month) and data (R317 a month) caps as amounts that may be paid in addition to the total package?
7. **Comparators and aggregates.** Confirm that Stats SA earnings comparisons, parliamentary spend totals, programme-travel stories, charges, and performance scores stay out of this work.
8. **The President.** Confirm that the 2026/27 presidential package stays Unknown until a National Assembly resolution for that year is found (Gazette 55765 does not cover it; the source pack found no such 2026/27 resolution as at 21 November 2026).
9. **MP facilities.** Confirm that Members' Facilities Handbook fields stay unbuilt until a current official PDF is retrieved.

## Testing (evidence)

Recorded in the STATUS history row and the PR body draft (written outside the repo): `pytest`; review kit on the committed head, including the agent-names-file variant.

## Approval

Push and merge need the owner's GO naming the exact head.
