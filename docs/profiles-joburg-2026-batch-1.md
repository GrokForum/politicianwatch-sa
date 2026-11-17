# City of Johannesburg — CV profiles, batch 1 (CHG-PW-002)

**Environment:** DEV / TEST data on branch `dev/chg-pw-002-first-profiles`. Not published. Nothing sent to anyone.
**Researched:** 15 November 2026, about 20:05–20:20 SAST. `retrieved_at` on news facts is the date only, `2026-11-15` (time not logged; changed in CHG-PW-003 from a hand-typed `2026-11-15T20:15:00+02:00`); gazette facts keep the CHG-PW-001 roster retrieval time.
**Executive mayor:** Unknown. The council elects the mayor and the mayoral committee at its first sitting, expected around 19 November 2026. No 2026–2031 mayoral or MMC role is guessed in any profile.

## The ten profiles

| # | Gazetted name (known as) | Party | Seat | Gazette p. | Adverse items | RoR draft |
|---|---|---|---|---:|---:|---|
| 1 | OTTA HELENE MAREE (Helen Zille) | DA | PR rank 1 | 46 | 1 | right of reply |
| 2 | BELINDA CYNTHIA ECHEOZONJOKU | DA | Ward 74 (79800074) | 45 | 0 | optional accuracy check |
| 3 | HERMAN SAMTSEU PHILIP MASHABA | ActionSA | PR rank 1 | 43 | 1 | right of reply |
| 4 | NOMOYA DAPHNEY MNISI | ANC | Ward 129 (79800129) | 45 | 0 | optional accuracy check |
| 5 | TLALENG PETRONELLA MOFOKENG (Dr Tlaleng Mofokeng) | EFF | PR rank 1 | 46 | 0 | optional accuracy check |
| 6 | BONGANI MICHAEL BALOYI | MK Party | PR rank 1 | 47 | 0 | optional accuracy check |
| 7 | THAPELO KENNETH KUNENE (Kenny Kunene) | Patriotic Alliance | PR rank 1 | 47 | 2 | right of reply |
| 8 | KABELO GWAMANDA | Al Jama-ah | PR rank 1 | 45 | 2 | right of reply |
| 9 | MLUNGISI PROVIDENCE MABASO | IFP | PR rank 1 | 47 | 0 | optional accuracy check |
| 10 | MARGERET SHERON ARNOLDS (Margaret Arnolds) | AIC | PR rank 1 | 44 | 0 | optional accuracy check |

Files: `data/profiles/joburg-2026/<slug>.json` (+ generated `<slug>.md`), drafts in `drafts/right-of-reply/CHG-PW-002/<slug>.md`.

**Why only two ward seats.** The ANC won 63 wards and no PR seats, so every ANC councillor holds a ward (News24, 8 November 2026). Most other prominent figures entered on PR lists. The batch has one ANC ward councillor (former MMC) and one DA ward councillor (former MMC, former caucus leader).

## Labelling policy used

| Label | Used for |
|---|---|
| Confirmed | Government Gazette 55741; a City of Johannesburg official media statement. A court judgment is a primary record, but an adverse item is labelled no higher than its **identity link** to the gazetted person (`identity_link_label`, enforced by DQ since review round 2) |
| Reported | Reputable news on the allowed list (News24, Daily Maverick, M&G, TimesLIVE/Sunday Times, EWN, IOL, The Citizen, SABC); **party press statements** (DA, ActionSA) — a party statement is not an official City record (fix round 1) |
| Alleged | An allegation or charge not decided by a court (Gwamanda ×2) |
| Disputed | An official adverse finding that the person challenged and a court set aside, where only news reporting was available (Mashaba) |
| Unknown | Not found in an allowed source; value `null`, shown as a visible placeholder |

Fact counts across the 10 profiles (seat facts, summary fields, known-as / given-names / surname, CV entries and adverse items), after review round 2: **Confirmed 52, Reported 52, Unknown 21, Disputed 1, Alleged 2 — 128 facts.** Of the Confirmed facts, 50 are gazette seat facts (5 per profile) and 2 come from the City of Johannesburg's February 2023 statement (Mnisi). The Zille SCA item is Reported because its link to the gazetted OTTA HELENE MAREE is Reported.

**Sources outside the default list, used at reviewer request or as party records:** Encyclopaedia Britannica (Zille's given names and Federal Council dates), The Witness (Media24; Sarupen replacing Zille), DA and ActionSA party statements. All are labelled Reported.

## Adverse items (6, all "Right of reply: pending", reply field blank)

| Profile | Type | Label | matter_status | Outcome as reported |
|---|---|---|---|---|
| Maree (Zille) | Public Protector finding on 2017 tweets (Report No. 5 of 2018/19) | Reported (SCA judgment cited; identity link Reported) | cleared | SCA upheld the appeal and reviewed and set aside the findings and remedial action, 7 Feb 2022 |
| Mashaba | Public Protector findings on his mayoral term | Disputed | cleared | High Court, Pretoria, set findings aside on 31 Jan 2023; no appeal found in allowed sources |
| Kunene | Historical fraud conviction (1997, per DM) | Reported | reported_conviction | Reported: convicted (no judgment citation found in allowed sources; SAFLII not searched) |
| Kunene | 2025 PA suspension after presence at an arrest | Reported (SABC, EWN) | cleared | An external law firm cleared him of wrongdoing; reinstated and sworn in 26 Sep 2025 |
| Gwamanda | FSCA / funeral-scheme allegations (scheme in 2012; reported 2023) | Alleged | unknown | FSCA investigation confirmed; final outcome not found |
| Gwamanda | Fraud charges (2024) | Alleged | withdrawn | Provisionally withdrawn 25 Feb 2025; NPA said it would re-institute once investigations were finalised |

Third parties are not named unless they are public office-holders (e.g. a former mayor). The person arrested in the Kunene item and the co-accused in the Gwamanda case are not named in any profile, draft or URL. Fix round 1 removed the M&G link whose URL named a private person; the Kunene item now cites SABC and EWN.

### POPIA: special personal information — re-verify on the day of any publish

The criminal-matter items — **Kunene's 1997 fraud conviction** and **Gwamanda's 2024 fraud charges (provisionally withdrawn) and the related FSCA allegations** — are information about criminal behaviour, which is *special personal information* under POPIA s26. They are kept because they are public, reported and relevant to public office, but each must be **re-verified against its sources on the day of any publish** (status, outcome, any reinstated charge, appeal or expungement), and must pass four-eyes review and an owner GO first.

## Identity matching

Every profile has `identity_match.matched_details` with at least two details (the DQ gate enforces ≥ 2 whenever a non-gazette source is linked). Points for reviewers:

- **OTTA HELENE MAREE → Helen Zille.** The gazetted name is kept exactly as printed. The link rests on **party (DA) + DA PR rank 1 + council** (News24, 8 Nov 2026: DA PR list "topped by Helen Zille") plus a third detail: the **given names "Otta Helene"** (Britannica, Reported). Per the owner's instruction, **"Maree" as part of her full name is recorded as Unknown** (`full_name_surname`, value null): no allowed source confirms it. No family details are recorded.
- **THAPELO KENNETH KUNENE → Kenny Kunene.** SABC News (26 Sep 2025) quotes his oath: "I, Thapelo Kenneth Kunene, swear…" (Reported). This replaces the earlier Kenny→Kenneth inference. Plus party (PA PR rank 1) and council role (Transport MMC).
- **MARGERET SHERON ARNOLDS → Margaret Arnolds.** Spelled as gazetted; reported as Margaret (News24 2023-11-20, EWN 2025-09-26, SABC 2025-09-26 — all three verified). Linked on party (AIC PR rank 1) + council speaker role.
- **NOMOYA DAPHNEY MNISI.** Exact full name + council role (City statement). The City statement does not name her party; party is from the gazette only.

## Not linked, insufficient match, or deliberately left out

| Item | Why it was left out |
|---|---|
| Wikipedia / Wikidata / Briefly / Ghanamma pages giving Helen Zille's legal name and family details | Not on the allowed source list; the family details are private and out of scope |
| A 2026 social-media claim (reported by a non-allowed site) that Zille appeared on the candidate list under a variant spelling, and a residency query | Not from an allowed source; not linked |
| Counted.co.za, Mandate SA, Said in Council councillor pages | Aggregators, not on the allowed list. Counted.co.za shows a councillor's personal mobile and personal email — deliberately not used or copied |
| Mlungisi Mabaso — 2022 reports about a Lufhereng housing report and Fleurhof allocations (IOL / The Star, Polity) | The search summaries attribute claims to unnamed sources and do not clearly state an allegation against him personally; not opened in full this session. Left out pending a full read (insufficient basis to link an allegation to the person) |
| Herman Mashaba — 2025 News24 / City Press report on a dispute with Paul O'Sullivan; 2025 Citizen report on parliamentary questions about the City's forensic unit | Not read in full; not clearly an allegation against him with a status. Left out |
| Kunene — details of the third party at whose home he was found | Third party not named; not needed for the public-role record |
| Kunene — M&G 23 Sep 2025 (law-firm report details) and the "African News Global" naming | Removed in fix round 1: its URL names a private person. The job entry is re-sourced to EWN ("his online news agency") |
| Gwamanda — NPA statement as a primary source | The only copy found was an NPA Facebook post; not added. The Citizen quotes the NPA statement. An EWN follow-up was read but not added because its text names the co-accused |
| Echeozonjoku, Mabaso — City of Johannesburg's 13 Dec 2021 mayoral committee statement | Found only as a PDF hosted by a third-party association, not on joburg.org.za; not used. The DA statement is kept, labelled Reported |
| Mashaba — Sunday World (31 Jan 2023) | Not on the allowed list; the date is sourced to ActionSA's 31 Jan 2023 statement ("today the High Court in Pretoria…") and TimesLIVE ("this week") |
| Gwamanda — co-accused's name | Private individual; not needed |
| Dada Morero, Loyiso Masuku, Frank Chikane | Not in the gazetted Joburg roster (ANC PR list unused — overhang). Out of scope |
| Ennie Makhafola (EFF PR 14) and Jack Sekwaila (ANC ward 64), both 2023 MMCs | Candidates for a later batch; not researched here |

## Gaps

- **Education is Unknown for all 10.** No allowed source stating a qualification was opened. Dr Mofokeng's medical degree is not inferred from "medical doctor".
- **Career is Unknown for 8 of 10** (sourced for Mofokeng and, via CV entries, for Kunene).
- **2026–2031 council roles** (mayor, speaker, MMCs, whips, caucus leaders): Unknown until the first sitting, around 19 November 2026.
- **Official contact channels** are not filled in. Each draft says "[official channel, owner to confirm]".
- Mnisi's MMC end date and Echeozonjoku's current caucus role are Unknown.
- Gwamanda: final FSCA outcome and whether charges were re-instituted: Unknown as of 15 Nov 2026.
- The SCA judgment is cited from LawLibrary and the SCA's own media summary (both fetched and read). SAFLII was not fetched.
- ESP was not used or fetched.
