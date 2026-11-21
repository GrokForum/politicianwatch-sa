# Allowed sources

Status as of 20 November 2026 (SAST). The machine-readable registry was extended on 20 November 2026 after the owner's decision: "Yes, add the five official sources." Changes to this list need the owner's confirmation. The machine-readable registry is `data/sources.json` (domain → tier). `pwatch dq` fails a source on a link-only or not-allowed domain, fails an adverse item or identity link that rests only on tier-3 sources, and warns about domains that are not in the registry.

Every domain below was checked on 17 Nov 2026: it was reached, or, where our fetcher was refused, confirmed through a search result or a reader fetch. Each was confirmed to be the named outlet. Anything that could not be verified is listed at the end and is **not** on the list.

## Tier 1: primary (can support Confirmed)
| Source | Domain |
|---|---|
| Independent Electoral Commission (IEC) | elections.org.za, results.elections.org.za |
| Government Gazette (e.g. Gazette 55741, via Gazette Finder's copy of the GPW issue) | gazettefinder.co.za, gpwonline.co.za |
| City of Johannesburg official statements and newsroom | joburg.org.za |
| Court judgments | supremecourtofappeal.org.za, lawlibrary.org.za. SAFLII (saflii.org) is consulted by hand only and never fetched automatically. |
| Parliamentary Monitoring Group (owner, 20 Nov 2026) | pmg.org.za, static.pmg.org.za. Official parliamentary records and a byte-identical mirror of Government Gazette 55741. Check rate and attribution terms before any collector. A PMG republication of a party statement is still labelled as a party statement, not as a PMG primary record. |
| National Treasury Municipal Money data API (owner, 20 Nov 2026) | municipaldata.treasury.gov.za. Official local-government office-holders. The cube will lag the 4 Nov 2026 election until Treasury refreshes. **POPIA:** the payload includes email and phone fields; publish only elected office-bearers' official council channels and drop secretary/staff rows. |
| Parliament of South Africa (owner, 20 Nov 2026) | parliament.gov.za, including the Register of Members' Interests. Planned 2029 module. **POPIA:** publish only the office-bearer's own public disclosure; omit family or dependent details and private addresses. |
| Department of Justice (owner, 20 Nov 2026) | justice.gov.za, including the Special Tribunal. Official court and inquiry records for `Court matters`, with the two-detail identity rule and right of reply. |
| The Presidency (owner, 20 Nov 2026) | thepresidency.gov.za, including SIU reports. Official inquiry records; same rules as the Special Tribunal. |

## Tier 2: mainstream SA news (Reported)
Outlets aimed at a wide audience, with an editor and a public complaints route. Each can support a Reported fact on its own. An adverse item still follows the right-of-reply rules.

**National news, print and online**
| Outlet | Domain |
|---|---|
| News24 | news24.com |
| City Press (closed 10 May 2026; archive only) | news24.com/citypress |
| Daily Maverick | dailymaverick.co.za |
| Mail & Guardian | mg.co.za |
| TimesLIVE | timeslive.co.za |
| Sunday Times | sundaytimes.timeslive.co.za |
| Sowetan | sowetan.co.za |
| Business Day / BusinessLIVE | businessday.co.za (businesslive.co.za redirects there) |
| Financial Mail | fm.co.za |
| The Citizen | citizen.co.za |
| Daily Sun | snl24.com (dailysun.co.za redirects there) |
| Sunday World | sundayworld.co.za |
| The South African | thesouthafrican.com |
| Newsday | newsday.co.za |
| GroundUp | groundup.org.za |
| amaBhungane Centre for Investigative Journalism | amabhungane.org |
| SA Jewish Report (owner, 17 Nov 2026) | sajr.co.za |
| Politicsweb | politicsweb.co.za. It also republishes **party statements**: label those as party statements (Reported, see below), not as Politicsweb reporting. |

**Business, finance and technology**
| Outlet | Domain |
|---|---|
| Moneyweb | moneyweb.co.za |
| BizNews | biznews.com |
| BusinessTech | businesstech.co.za |
| MyBroadband | mybroadband.co.za |
| Daily Investor | dailyinvestor.com |

**Broadcast**
| Outlet | Domain |
|---|---|
| SABC News | sabcnews.com (incl. elections.sabcnews.com) |
| eNCA | enca.com |
| Newzroom Afrika | newzroomafrika.tv |
| EWN (Eyewitness News; Primedia's news service, also heard on 702 and 94.7) | ewn.co.za |
| Radio 702 and 94.7 (Primedia) | 702.co.za and 947.co.za, both now redirect to primediaplus.com |
| Jacaranda FM news | jacarandafm.com |

**IOL (Independent Media) and its titles**
| Outlet | Domain |
|---|---|
| IOL | iol.co.za |
| The Star | thestar.co.za (also iol.co.za/the-star) |
| Pretoria News | pretorianews.co.za |
| Cape Times | capetimes.co.za |
| Cape Argus | capeargus.co.za |
| Daily News (Durban) | dailynews.co.za |
| The Mercury | themercury.co.za |
| Isolezwe (isiZulu) | isolezwe.co.za |

**Afrikaans**
| Outlet | Domain |
|---|---|
| Netwerk24 (Beeld, Rapport, Volksblad, Die Burger) | netwerk24.com (rapport.co.za and beeld.com redirect there) |
| Maroela Media | maroelamedia.co.za |

**Regional dailies**
| Outlet | Domain |
|---|---|
| The Witness (Pietermaritzburg) | witness.co.za |
| Daily Dispatch (East London) | dailydispatch.co.za (dispatchlive.co.za redirects there) |
| The Herald (Gqeberha) | theherald.co.za (heraldlive.co.za redirects there) |

**Community: Caxton local newspapers (hosted on citizen.co.za)**
Southern Courier (owner, 17 Nov 2026), Sandton Chronicle, Randburg Sun, Northcliff Melville Times, Rosebank Killarney Gazette, Roodepoort Record, Fourways Review, Alberton Record, Lowvelder, all at `citizen.co.za/<title>/`. Other Caxton local titles at citizen.co.za are tier 2 as well. Their pages often print personal details (ages, suburbs, phone numbers); record only public-role facts from them.

**Reference work (Reported)**
Encyclopaedia Britannica (britannica.com). Not SA media; used once, for Zille's given names, on the owner's instruction.

## Tier 3: smaller and independent voices ("separate pen") — Reported only (CHG-PW-005)
Publications with a known public following and a wide-audience intent that are smaller, newer or editorially narrower than tier 2.

**Rules:** Reported only. A tier-3 source can **never** be the sole source for an adverse item or for an identity link. It always needs corroboration from tier 1 or tier 2. `pwatch dq` fails an adverse item, or an identity link, that cites at least one tier-3 URL and no tier-1 or tier-2 URL, whatever party-statement, unregistered or other URLs sit alongside it. Opinion pieces in tier-3 outlets are not facts.

| Outlet | Domain / handle | What it is | Note |
|---|---|---|---|
| The Common Sense | thecommonsense.co.za; X @CommonSense_ZA | Independent SA news and analysis site with a daily "Morning Brief" newsletter; its writers include Dr Frans Cronje. X account created Aug 2025, about 8,100 followers on 17 Nov 2026 | **Owner-confirmed** (17 Nov 2026) as the "Common Sense" meant |
| The Cape Independent | thecapeindependent.com (redirects to capeindependent.substack.com); older site capeindependent.com | Western Cape politics news and opinion site, launched Nov 2023, with an openly stated editorial stance (Cape independence, right of centre) | Founder/editor Robert Duigan, X **@uMarhobane** (about 17,400 followers on 17 Nov 2026; his X profile links thecapeindependent.com). capeindependent.com did not respond on 17 Nov 2026. The current Substack's recent posts are by another writer; who runs it now is unclear. **Owner to confirm** who runs it now. |
| Briefly News | briefly.co.za | High-traffic SA news site that mainly rewrites social-media posts and other outlets' reports | **Proposed:** tier 3, not tier 2 and not excluded (**owner to confirm** the placement). It is aimed at a wide audience, so it is in the pen, but its stories are mostly second-hand. It can never carry a fact alone; cite the original report instead where possible. |
| Rand Desk | randdesk.co.za | Business, markets and politics news site that says it reports from primary sources and links to them | **Proposed:** tier 3 for now. Its own about page says some stories go up without an editor when they rest on the official record or on three other publishers. **Owner to confirm** whether to move it to tier 2. |

**Adding a tier-3 voice:** each addition needs the owner's confirmation and must meet all of these:
1. A named editor or author who is accountable for the content.
2. A track record of at least about a year of regular publishing that can be checked (an archive of dated articles).
3. A wide-audience intent: published openly for the public, not a private newsletter or a personal social-media feed.
4. It is a publication. Posts on a person's own social-media account remain not allowed (see below), even when the person runs a tier-3 outlet.

## Party statements (Reported only)
Official party statements (e.g. DA: da.org.za, dagauteng.org.za; ActionSA: actionsa.org.za). A party statement is not an official City record, so it is never labelled Confirmed. The same applies when a statement is republished on Politicsweb.

## Link only, never scraped
ElectionSePush (esp.info/elections): link to it, but do not fetch or reuse its data (its terms forbid redistribution).

## Sources that carry private personal details (rule 6, CHG-PW-007; amended by CHG-PW-011)

Default (owner rule, 19 Nov 2026 18:25 SAST): if the only source for a fact also carries private personal details (home address, family, ID number, health, personal phone or email), the source is **not linked** and the fact is **Withheld (POPIA)**, not Unknown. Unknown means no source was found. The public profile shows the withheld wording, holds no fact value, and links nothing. A private file (`private/withheld-sources.json`) keeps only the URL, title, date and fact key so a serious enquirer can be referred to the source. That file is never rendered, never copied into a site build, and is not carried to a fresh public repository. `pwatch dq` fails a withheld fact that has no matching private entry, that carries a public URL, or that is an adverse item. `pwatch site build` and `pwatch site check` fail if a withheld-source URL or title appears in the built output, and (when the profiles are passed in) if a Withheld fact has no matching private-register entry. That missing-register guard keys off the profiles' fact labels, not the wording on the privacy page, so a fresh repository with no Withheld facts does not need a register. See `docs/FRESH-REPO-PLAN.md`.

Exception, only with the owner's approval for named facts: the source may be linked if (1) no private detail from it is reproduced anywhere in the repo or on the site, (2) each such fact carries the note "personal details not recorded here", and (3) each such fact records the approval as `owner_approved_pi_source: "YYYY-MM-DD HH:MM SAST (CHG-PW-NNN)"`. `pwatch dq` fails a fact that has the note without the approval, the approval without the note or a source link, the approval on an adverse item, or a fact citing an approved source without the approval. The approval is recorded in the change's RFC (date and time only, no personal information). The exception is implemented and tested and currently has no uses.

## Not allowed
Wikipedia and Wikidata, gossip sites, councillor aggregators (e.g. Counted.co.za, Mandate SA, Said in Council), personal social media and professional-network profiles.

## Checked and not added
| Name given | Finding |
|---|---|
| "Scrutinize" | scrutinize.co.za is a "Launching Soon" placeholder (17 Nov 2026), not a publication. "Scrutinize" is otherwise known as a 2009 HIV-prevention campaign. **Deferred: not yet publishing (owner, 17 Nov 2026).** Left off until it publishes. |
| Ilanga (isiZulu weekly) | ilanga.co.za is a travel site; the newspaper's own domain was not found. Not added. |
| Joburg East Express (Caxton) | citizen.co.za/joburg-east-express/ returned 404. Not added by name (other Caxton titles at citizen.co.za are covered). |

## The Common Sense: identification
The owner confirmed on 17 Nov 2026 that "Common Sense" means **The Common Sense** (thecommonsense.co.za, X @CommonSense_ZA): an SA news-and-analysis publication (its X account was created in August 2025) aimed at a general audience, with a daily Morning Brief.

## Added to the registry 20 November 2026 (CHG-PW-013) — owner approved

The owner decided, on 20 November 2026: "Yes, add the five official sources." The five are PMG (`pmg.org.za` and `static.pmg.org.za`), National Treasury municipal data (`municipaldata.treasury.gov.za`), Parliament (`parliament.gov.za`), Justice (`justice.gov.za`) and the Presidency (`thepresidency.gov.za`). They are in `data/sources.json` as tier 1, verified 2026-11-20. They were listed in a PoliticianWatch source pack compiled on 20 November 2026 and were checked with a streamed GET on 20 November 2026 (SAST) from this project's fetcher identity. No new collector uses them in this change, and no profile fact was sourced from them here. The 245 new profiles cite only the already-allowed Gazette Finder copy of Government Gazette 55741. Terms and POPIA notes are in the tier-1 table above and in the check log below.

| Source | URL checked | HTTP | Tier | Terms / notes |
|---|---|---|---|---|
| Government Gazette 55741 (PMG mirror) | https://static.pmg.org.za/55741_13-11_ElectoralComm_Final.pdf | 200, `application/pdf`, 7,845,217 bytes | 1 (same gazette already cited via Gazette Finder) | Byte-identical to the Gazette Finder copy already used (SHA-256 `cd544faf2a703a81eb4466bbfcd3618f5ade03c7b456538116b385c266058798`). Official IEC / Government Gazette public notice, mirrored by PMG. Profile `source_url` values are unchanged (Gazette Finder). |
| Municipal Money `officials` cube (National Treasury / OpenUp) | https://municipaldata.treasury.gov.za/api/cubes/officials/facts | 200, JSON, `total_fact_count` 2920 | 1 (official local-government office-holders) | Machine-readable official contacts and roles (Mayor / Executive Mayor, Deputy, Speaker, and other rows). **Will lag** the 4 Nov 2026 election until Treasury refreshes. **POPIA:** the payload includes email and phone fields; publish only elected office-bearers' official council channels and drop secretary/staff rows. No collector was added; contact values were not stored. |
| Parliament Register of Members' Interests (June 2026 v2) | Index https://www.parliament.gov.za/register-members-interests (200); PDF https://www.parliament.gov.za/storage/app/media/Register%20of%20Members%20Interests/Register_of_members_interests_june_2026_v2.pdf (200, PDF, 6,379,268 bytes) | 200 | 1 (public disclosure register) for a future national module | Planned 2029 module only (`docs/national-2029-module.md`). **POPIA:** publish only the office-bearer's own public disclosure; omit family/dependent details and private addresses. Not ingested. |
| PMG API (Parliamentary Monitoring Group) | https://api.pmg.org.za/ (200, JSON; v1 endpoints including `/member/`, `/committee/`, `/committee-meeting-attendance/`, `/committee-question/`). Web: https://pmg.org.za/members/ (200). Documentation: https://github.com/OpenUpSA/pmg-cms-2/blob/master/API.md | 200 | 1 (owner, 20 Nov 2026; official parliamentary records) | Planned 2029 module. Public parliamentary data; check rate and attribution terms before any collector. Not ingested. `/v2/` is not used (reported 404 in the pack; not re-probed beyond the v1 root). |
| IEC LGE results and by-elections downloads | https://results.elections.org.za/home/ (200); `/dashboards/lge` (200); `/home/Downloads/ME-Results` (200) | 200 | 1 (already listed: results.elections.org.za) | Already an allowed primary source. Useful later for vote shares and by-election replacements. Not scraped beyond this reachability check. |
| DOJ Special Tribunal | https://www.justice.gov.za/tribunal/index.html | 200 | 1 (official court/inquiry records) | Future primary source for `Court matters`, with the two-detail identity rule and right of reply. No new court facts in this change. |
| Presidency SIU reports | https://www.thepresidency.gov.za/tso/siu-reports | 200 | 1 (official inquiry records) | Same use as the Special Tribunal, same rules. No new court facts in this change. |

### City of Johannesburg pages checked and not usable (20 Nov 2026)

The City remains an allowed tier-1 source (`joburg.org.za`). These directory URLs returned **HTTP 404** on 20 Nov 2026, so they were not used to fill council offices or official contacts: `/about_/Pages/Councillors.aspx`, `/about_/Pages/Executive-Mayor-and-Mayoral-Committee.aspx`, `/about_/Pages/Office-of-the-Speaker.aspx`, `/about_/Pages/default.aspx`. The homepage returned HTTP 200 (redirects to `/Pages/homepage.aspx`). Offices stay Unknown until an allowed source confirms them.

### City of Johannesburg offices re-check (21 Nov 2026)

The same four `/about_/Pages/...` directory URLs still returned **HTTP 404**. The homepage again returned HTTP 200 (redirects to `/Pages/homepage.aspx`) with no 2026–2031 office announcement. A current Council legislature page, `https://joburg.org.za/about_/government/Pages/Council/Council.aspx`, returned HTTP 200 and states that it reflects the previous Legislature (former Speaker, Chief Whip, Councillors and Section 79 Committees), that that term has concluded, and that information on the new Council will be published once it has been formally constituted. Newsroom and media-statements indexes (`/media_/Newsroom/Pages/default.aspx`, `/media_/Newsroom/Pages/Newsroom.aspx`, `/media_/MediaStatements/Pages/default.aspx`) returned HTTP 200 and did not publish the 2026–2031 executive mayor, speaker, chief whip or mayoral committee. A councillors contact-details PDF and a previous-term declaration-of-interests PDF were linked from the Council page and were not fetched (POPIA). Offices stay Unknown until an allowed source confirms them. The URL list is in `itil/changes/CHG-PW-014-joburg-depth.md`.

