# City of Johannesburg LGE 2026 — source notes

**Environment:** TEST roster, built in DEV on 15 November 2026 (SAST). Not published.
**Retrieved:** 15 November 2026, 18:10 SAST (16:10 UTC).
**CVs:** not built. Education, career, positions, court matters and scandals are empty / Unknown placeholders.
**Executive mayor:** Unknown. The council elects an executive mayor at its first sitting, expected around 19 November 2026. No mayor had been elected as of 15 November 2026.

## Primary sources used

### 1. Government Gazette 55741 (canonical names)

| Field | Value |
|---|---|
| Title | Publication of the List of Elected Councillors |
| Authority | Electoral Commission, Notice 8183 of 2026 |
| Gazette | No. 55741, Friday 13 November 2026, Vol. 737, 144 pages |
| PDF used | https://www.gazettefinder.co.za/gazettes/government-gazette/2026/55741/government-gazette-55741-2026-11-13.pdf |
| Landing page | https://www.gazettefinder.co.za/gazettes/government-gazette/2026/55741/ |
| SHA-256 | `cd544faf2a703a81eb4466bbfcd3618f5ade03c7b456538116b385c266058798` |
| Joburg pages | 43–47 (PDF page numbers) |

Gazette Finder published the same SHA-256 for a copy it reports having fetched from the Government Printing Works on 13 November 2026. A stable `gov.za` or `gpwonline.co.za` direct URL for gazette 55741 was not found on 15 November 2026. The gazette itself states that it is also available free online at www.gpwonline.co.za. The IEC announced the gazetting on 13 November 2026: [IEC news](https://www.elections.org.za/pw/News-And-Media/News-List/News/IECNews/5726), also reported by [SAnews](https://www.sanews.gov.za/south-africa/iec-gazettes-names-councillors-elected-2026-local-government-polls).

The national gazette excludes Siyancuma Local Municipality (Northern Cape) pending a revote on 18 November 2026. That exclusion is outside the Joburg pilot.

### 2. IEC seat calculation detail — JHB (cross-check)

| Field | Value |
|---|---|
| Report | Seat Calculation Detail, 2026 Local Government Elections |
| Municipality | JHB — City of Johannesburg |
| Event id | 1887 |
| URL | https://results.elections.org.za/home/LGEPublicReports/1887/Seat%20Calculation%20Detail/GP/JHB.pdf |
| Results home | https://results.elections.org.za/home/ |
| Printed | 13 November 2026, 15:55:11 SAST |
| SHA-256 | `6cc25c2d0814b9dfa88e1066129df2c65b34cf0dc9ba36d497f18c4d21347aac` |
| Totals | 270 seats; 135 ward; 135 PR; 0 independents; majority 136 |

No public IEC councillor-name CSV or Excel file with a stable direct URL was found on 15 November 2026. Paths under `LGEPublicReports/1887/Seat Allocation/` returned HTTP 404. The IEC results home page offers an interactive downloader for PDF, Excel and CSV reports; "Seat allocation: Party, seat type, candidate name, and candidate ID" is described under municipal **by-election** reports, not retrieved here. The page [List of current ward councillors](https://www.elections.org.za/pw/StatsData/List-Of-Current-Ward-Councillors) is an interactive search form, not a bulk file, and was not used (it should not be used to search by ID number). A drafted enquiry to the IEC for a councillor CSV and reuse terms would need an owner GO and has not been sent.

ElectionSePush (https://esp.info/elections) was **not fetched or scraped**. It is a link-only reference.

## Roster counts versus 270

The gazette parse of the Johannesburg section produced **270 rows**: 135 ward seats (wards 1–135, official IDs `79800001`–`79800135`, no gaps and no duplicates) and 135 PR seats. PR list ranks are complete and sequential for every party that won PR seats. There are no duplicate names in the Joburg section.

These counts match the IEC seat-calculation PDF exactly (270 / 135 / 135). There is **no discrepancy between the two primary sources**.

### Party seats (gazette = IEC)

| Party | Total | Ward | PR |
|---|---:|---:|---:|
| DEMOCRATIC ALLIANCE | 91 | 51 | 40 |
| AFRICAN NATIONAL CONGRESS | 64 | 64 | 0 |
| ACTIONSA | 42 | 9 | 33 |
| ECONOMIC FREEDOM FIGHTERS | 17 | 2 | 15 |
| UMKHONTO WESIZWE PARTY | 15 | 1 | 14 |
| INKATHA FREEDOM PARTY | 7 | 4 | 3 |
| PATRIOTIC ALLIANCE | 5 | 2 | 3 |
| RISE MZANSI | 5 | 0 | 5 |
| VRYHEIDSFRONT PLUS \| FREEDOM FRONT PLUS | 5 | 0 | 5 |
| AFRICAN TRANSFORMATION MOVEMENT | 3 | 0 | 3 |
| AL JAMA-AH | 3 | 2 | 1 |
| AFRICAN CHRISTIAN DEMOCRATIC PARTY | 2 | 0 | 2 |
| AFRIKA MAYIBUYE MOVEMENT | 2 | 0 | 2 |
| SOUTH AFRICAN COMMUNIST PARTY | 2 | 0 | 2 |
| AFRICAN HEART CONGRESS | 1 | 0 | 1 |
| AFRICAN INDEPENDENT CONGRESS | 1 | 0 | 1 |
| AFRICAN PEOPLE'S CONVENTION | 1 | 0 | 1 |
| BUILD ONE SOUTH AFRICA | 1 | 0 | 1 |
| ECONOMIC LIBERATORS FORUM SOUTH AFRICA | 1 | 0 | 1 |
| PAN AFRICANIST CONGRESS OF AZANIA | 1 | 0 | 1 |
| PEOPLE'S MOVEMENT FOR CHANGE | 1 | 0 | 1 |
| **Total** | **270** | **135** | **135** |

The ANC is the excessive-seat party in the IEC calculation (64 ward seats, 0 PR). Independents: 0.

## ⚠ Discrepancies (secondary sources only)

Secondary tallies published around 10–15 November 2026 disagree with the official IEC and gazette figures on two parties:

| Party | Official (IEC PDF + Gazette 55741) | ACCORD / MzansiData (secondary) |
|---|---:|---:|
| African National Congress | **64** (64 ward, 0 PR) | 63 |
| ActionSA | **42** (9 ward, 33 PR) | 43 |

The planning packet noted that ElectionSePush already showed ANC 64/0 and ActionSA 9/33, which matches the official files. This project does not scrape ESP and does not publish secondary tallies. The committed roster follows the gazette, cross-checked against the IEC PDF.

Democratic Alliance 91, EFF 17 and MK 15 agree across the official files and those secondary write-ups.

## Parse method and residual risk

The gazette PDF was produced with Adobe Acrobat Paper Capture (OCR). Text was extracted with `pdftotext -layout`. All 270 Johannesburg lines matched a single pattern (municipality, party, ward ID or `PR(rank)`, surname, full names, `MC Ward` / `MC PR`). Five names contain diacritics (GÜNTHER, ZONÉ, ANDRÉ, DESIRÉ, RENÉ), which were preserved. Residual OCR risk remains on individual spellings; the page number on each row is the way back to the source image. No curriculum vitae was built from this parse.
