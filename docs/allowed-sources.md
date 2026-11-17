# Allowed sources

Status as of 17 November 2026 (SAST). Changes to this list need the owner's confirmation. The machine-readable registry is `data/sources.json` (domain → tier). `pwatch dq` fails a source on a link-only or not-allowed domain and warns about domains that are not in the registry.

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

## Party statements (Reported only)
Official party statements (e.g. DA: da.org.za, dagauteng.org.za; ActionSA: actionsa.org.za). A party statement is not an official City record, so it is never labelled Confirmed. The same applies when a statement is republished on Politicsweb.

## Link only, never scraped
ElectionSePush (esp.info/elections): link to it, but do not fetch or reuse its data (its terms forbid redistribution).

## Not allowed
Wikipedia and Wikidata, gossip sites, councillor aggregators (e.g. Counted.co.za, Mandate SA, Said in Council), personal social media and professional-network profiles.

## Smaller and independent outlets
Smaller and independent voices (a separate tier 3) are out of scope for CHG-PW-004 and are proposed in CHG-PW-005. Until that change is merged, they are not on the allowed list.

## Checked and not added
| Name given | Finding |
|---|---|
| "Scrutinize" | scrutinize.co.za is a "Launching Soon" placeholder (17 Nov 2026), not a publication. "Scrutinize" is otherwise known as a 2009 HIV-prevention campaign. Not added. **Owner to confirm:** tell us if you meant a different outlet. |
| Ilanga (isiZulu weekly) | ilanga.co.za is a travel site; the newspaper's own domain was not found. Not added. |
| Joburg East Express (Caxton) | citizen.co.za/joburg-east-express/ returned 404. Not added by name (other Caxton titles at citizen.co.za are covered). |
