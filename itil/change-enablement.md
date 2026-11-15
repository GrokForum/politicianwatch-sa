# Change enablement

**Scope:** anything that changes the code, the roster, the schema, detectors or publication rules, hosting, or an outward message.

## Change types

| Type | Examples | Authority | Evidence |
|---|---|---|---|
| **Standard** | Docs and tests that do not change published facts; a DQ re-run that passes | Author after green tests | PR template; tests green |
| **Normal — medium** | New parser; schema field; a TEST roster load | Owner, after two plain PASS reviews on the same head | Change record; tests; rollback note |
| **Normal — high** | Publishing pipeline; anything that adds or changes an adverse item about a named person; hosting or DNS; POPIA-relevant handling | Owner + two plain PASS reviews | Full change record; RoR complete; popia-review PASS |
| **Emergency** | Take down a wrong or defamatory item; revoke a leaked secret | Owner (or take-down only), retro record within two business days | Incident record linked |

## Rules

- Name the environment: DEV, TEST, or PROD. DEV never points at a production host, database, mailbox or DNS.
- Work on a branch, never on `main`.
- An approval covers a specific commit. New commits after a PASS need a fresh PASS.
- Bot (PoliticianWatch) builds; Cavus and Cassian review only; the owner gives the final GO on the exact head.
- A bot approval never fills a human slot.
- `PASS_WITH_CONCERNS` does not count. Both Cavus and Cassian must give a plain PASS on the same exact head, then the owner GOes in quoted words that name the RFC and that head.
- Silence, "ok", another agent's approval, or a GO about something else is not a GO.
- Right-of-reply drafts are never sent by the bot.
- Change log: `registers/change-log.md`.
