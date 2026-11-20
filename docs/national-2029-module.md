# National and provincial 2029 module (plan only)

Status: **plan only** (CHG-PW-013). No collector, profile, schema change or site page for national MPs, NCOP delegates or MPLs is in this change. The Johannesburg 2026 local-government pilot remains the built coverage.

This note records sources that were reached on 20 November 2026 (SAST) so a later named change can use them, after the owner's confirmation of any new `data/sources.json` rows and a POPIA review of each fact.

## Why 2029, not now

National Assembly, NCOP and provincial legislature seats follow the national and provincial elections, next due in 2029. Building MP profiles now would mix a 2026 municipal gazette cohort with a still-sitting national Parliament elected earlier, and would need a separate identity and right-of-reply process. The sources below are useful when that module starts; they are not used on Joburg councillor profiles.

## Sources checked (20 November 2026)

| Source | What it offers | Check | Constraints |
|---|---|---|---|
| Parliament Register of Members' Interests, June 2026 v2 | Public disclosure of MPs' financial interests, directorships, shares and sponsorships | Index HTTP 200; PDF HTTP 200 (6,379,268 bytes, `%PDF-1.7`) | **POPIA:** publish only the office-bearer's own public section. Omit family or dependent details and private addresses. Consulted later, by a named change; not fetched into this repo now. |
| PMG API v1 (`https://api.pmg.org.za/`) | Machine-readable members, committees, attendance and parliamentary questions | Root HTTP 200; documented endpoints include `/member/`, `/minister/`, `/committee/`, `/committee-meeting/`, `/committee-question/`, `/committee-meeting-attendance/`. Documentation: https://github.com/OpenUpSA/pmg-cms-2/blob/master/API.md | Check rate limits and attribution before any collector. Do not use an undocumented `/v2/` path. |
| PMG members web list | Human-readable member directory | https://pmg.org.za/members/ HTTP 200 | Same terms as the API. |

IEC and Government Gazette remain the primary sources for who was elected. PMG and the Register would fill committees, attendance, questions and disclosed interests, each labelled and dated, with the two-detail identity rule before any fact is attached to a gazetted person.

## Out of scope here

City of Johannesburg councillor profiles, council offices for 2026–2031, and any contact with members. Right-of-reply drafts stay unsent unless the owner sends them.
