# Next milestone (plan only)

Status: **plan only** (CHG-PW-013 follow-up, 20 November 2026). Nothing here is an RFC, a collector, a profile fact or a publish step. Each item below needs its own named change and, where the rules require it, the owner's GO.

The Johannesburg **pilot target is MET** (owner, 20 Nov 2026): 269 active CV profiles plus 1 on hold, of 270 gazetted seats. [PR #13](https://github.com/GrokForum/politicianwatch-sa/pull/13) was squash-merged into `main` as `7c741222` on 21 Nov 2026 12:47 SAST (verified 25 Nov 2026). The end-of-road checklist and the 14-green-nights streak are still open; see `docs/FRESH-REPO-PLAN.md`.

## 1. Joburg depth

- **Unknown CV fields.** Research positions, career and education for the 245 gazette-only stubs, and any remaining Unknowns on the original 24, from already-allowed sources only. Link a court or news item to a person only when at least two details match. A fact whose only source carries personal details is Withheld (POPIA), not Unknown.
- **Council offices.** Record the 2026–2031 executive mayor, speaker, chief whip and mayoral committee when the City (or another allowed source) publishes them. Re-checked 21 November 2026 (CHG-PW-014): the four City `/about_/Pages/...` directory URLs still returned HTTP 404. The Council legislature page (`/about_/government/Pages/Council/Council.aspx`, HTTP 200) states that information on the new Council will be published once it has been formally constituted. Do not guess. Municipal Money may lag the election and needs a POPIA filter (elected office-bearers' official channels only).
- **Right of reply.** Six adverse items on four of the original profiles still show "Right of reply: pending". Drafts stay drafts; the owner sends them and records the state (sent and date, reply received, or a decision not to send). No adverse item should go to a non-draft site without that record.
- **Held profile.** Return the one held profile to the batch only through a new change, once two identifying details exist in an allowed source.

## 2. The next councils

After Joburg depth is in hand, expand by gazette to the other metropolitan municipalities, starting with **Tshwane, Ekurhuleni, Cape Town and eThekwini**, then the remaining metros. Government Gazette 55741 already lists elected councillors for all municipalities; each council needs its own roster parse, page citations, identity checks and a named change. Do not invent rows, and do not scrape ElectionSePush. Official contact and office-holder fields wait for an allowed source, as with Joburg.

## 3. Fourteen green nights, end of road, and a fresh repository

The 14-day stability checklist in `docs/FRESH-REPO-PLAN.md` is still open. The streak starts from a green night on `main` after PR #13 merged (as `7c741222`) and the nightly has published the 269 profiles (the owner already turned publishing on for the earlier 24). A red night, a POPIA hit, or an unreviewed change on `main` restarts the count. The fresh public repository is seeded only when the owner judges the Joburg pilot at end of road and the 14 nights have been green, and only after a named change and a quoted GO. The do-not-carry list and the withheld-register sidecar decision remain as in that plan.

## 4. National and provincial 2029 module

Plan only, as in `docs/national-2029-module.md`. Parliament's Register of Members' Interests and the PMG API are now allowed tier-1 sources; they are not ingested until a later named change, and any fact still needs a POPIA review (no family, addresses or private contacts). IEC and the Government Gazette remain the primary record of who was elected.

## 5. Pay context (plan only)

Role tiers and gazetted remuneration packages ([CHG-PW-015](../itil/changes/CHG-PW-015-mp-pay-context.md), RFC only): municipal councillors from Government Gazette 55749 (upper limits, from 1 July 2026); the national executive, MPs and permanent NCOP delegates, and provincial upper limits, from Government Gazette 55765 (from 1 April 2026). Neutral package explainer; executive entitlements from the 2022 Guide for Members of the Executive. Figures are gazetted packages or upper limits for the role, not a claim about any person's actual pay. Implementation needs its own named change and the owner's GO.

## 6. National watch-list intake (plan only)

A documented batch intake path for national and provincial public-office holders, party-only posts and non-office-holder public figures, ahead of the 2029 module ([CHG-PW-017](../itil/changes/CHG-PW-017-national-watchlist-rfc.md), RFC only, Design B). Batch 1: national executive: 1. Batch 2: cited entries, described in the RFC by aggregate counts and coarse role buckets only; named entries and specific sources stay in a private, non-committed file. Teammate-bot briefings are unverified intake. Each item must be re-checked against a primary source or reputable reporting and labelled before use; no intake entry is published on a profile until that check is done and a right-of-reply draft exists. A later BEE elites page stays off until those gates are met. Implementation needs its own named change and the owner's GO.
