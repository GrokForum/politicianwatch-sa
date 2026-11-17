# Allowed sources

Status as of 17 November 2026 (SAST). Changes to this list need the owner's confirmation. The machine-readable registry is `data/sources.json` (domain → tier). `pwatch dq` enforces the tier rules below and warns about domains that are not in it.

Every domain below was checked on 17 Nov 2026: it was reached, or, where our fetcher was refused, confirmed through a search result or a reader fetch. Each was confirmed to be the named outlet. Anything that could not be verified is listed at the end and is **not** on the list.

## Tier 1: primary (can support Confirmed)
| Source | Domain |
|---|---|
| Independent Electoral Commission (IEC) | elections.org.za, results.elections.org.za |
| Government Gazette (e.g. Gazette 55741, via Gazette Finder's copy of the GPW issue) | gazettefinder.co.za, gpwonline.co.za |
| City of Johannesburg official statements and newsroom | joburg.org.za |
| Court judgments | supremecourtofappeal.org.za, lawlibrary.org.za. SAFLII (saflii.org) is consulted by hand only and never fetched automatically. |

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

## Tier 3: smaller and independent voices ("separate pen") — Reported only
Publications with a known public following and a wide-audience intent that are smaller, newer or editorially narrower than tier 2.

**Rules:** Reported only. A tier-3 source can **never** be the sole source for an adverse item or for an identity link. It always needs corroboration from tier 1 or tier 2. `pwatch dq` fails a profile where an adverse item, or the identity link, rests only on tier-3 sources. Opinion pieces in tier-3 outlets are not facts.

| Outlet | Domain / handle | What it is | Note |
|---|---|---|---|
| The Common Sense | thecommonsense.co.za; X @CommonSense_ZA | Independent SA news and analysis site with a daily "Morning Brief" newsletter; its writers include Dr Frans Cronje. X account created Aug 2025, about 8,100 followers on 17 Nov 2026 | **Owner to confirm** this is the "Common Sense" meant; see the identification note below |
| The Cape Independent | thecapeindependent.com (redirects to capeindependent.substack.com); older site capeindependent.com | Western Cape politics news and opinion site, launched Nov 2023, with an openly stated editorial stance (Cape independence, right of centre) | Founder/editor Robert Duigan, X **@uMarhobane** (about 17,400 followers on 17 Nov 2026; his X profile links thecapeindependent.com). capeindependent.com did not respond on 17 Nov 2026. The current Substack's recent posts are by another writer; who runs it now is unclear. **Owner to confirm** |
| Briefly News | briefly.co.za | High-traffic SA news site that mainly rewrites social-media posts and other outlets' reports | **Decision:** tier 3, not tier 2 and not excluded. It is aimed at a wide audience, so it is in the pen, but its stories are mostly second-hand. It can never carry a fact alone; cite the original report instead where possible. |
| Rand Desk | randdesk.co.za | Business, markets and politics news site that says it reports from primary sources and links to them | **Decision:** tier 3 for now. Its own about page says some stories go up without an editor when they rest on the official record or on three other publishers. **Owner to confirm** whether to move it to tier 2. |

**Adding a tier-3 voice:** each addition needs the owner's confirmation and must meet all of these:
1. A named editor or author who is accountable for the content.
2. A track record of at least about a year of regular publishing that can be checked (an archive of dated articles).
3. A wide-audience intent: published openly for the public, not a private newsletter or a personal social-media feed.
4. It is a publication. Posts on a person's own social-media account remain not allowed (see below), even when the person runs a tier-3 outlet.

## Party statements (Reported only)
Official party statements (e.g. DA: da.org.za, dagauteng.org.za; ActionSA: actionsa.org.za). A party statement is not an official City record, so it is never labelled Confirmed. The same applies when a statement is republished on Politicsweb.

## Link only, never scraped
ElectionSePush (esp.info/elections): link to it, but do not fetch or reuse its data (its terms forbid redistribution).

## Not allowed
Wikipedia and Wikidata, gossip sites, councillor aggregators (e.g. Counted.co.za, Mandate SA, Said in Council), personal social media and professional-network profiles.

## Checked and not added
| Name given | Finding |
|---|---|
| "Scrutinize" | scrutinize.co.za is a "Launching Soon" placeholder (17 Nov 2026), not a publication. "Scrutinize" is otherwise known as a 2009 HIV-prevention campaign. Not added. **Owner:** tell us if you meant a different outlet. |
| Ilanga (isiZulu weekly) | ilanga.co.za is a travel site; the newspaper's own domain was not found. Not added. |
| Joburg East Express (Caxton) | citizen.co.za/joburg-east-express/ returned 404. Not added by name (other Caxton titles at citizen.co.za are covered). |

## Common Sense: identification
The owner most likely means **The Common Sense** (thecommonsense.co.za, X @CommonSense_ZA): an SA news-and-analysis publication (its X account was created in August 2025) aimed at a general audience, with a daily Morning Brief. Its writers include Dr Frans Cronje, formerly of the Institute of Race Relations. No other SA publication called "Common Sense" was found. Possible confusion: the Cape Independent describes its readers as people "who value good old common sense", and "Common Sense" is also the name of a US newsletter (not SA). **Owner to confirm.**
