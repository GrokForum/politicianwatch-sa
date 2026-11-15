# Configuration item register

| ID | Name | Type | Notes |
|---|---|---|---|
| CI-001 | Profile JSON Schema | contract | `schemas/profile.schema.json`; labels, provenance, right_of_reply on adverse items |
| CI-002 | Gazette 55741 | data source | Canonical councillor roster. See `config/sources.yaml` (`iec_gazette`) |
| CI-003 | IEC LGE 2026 JHB seat calculation | data source | Official party seat totals. See `config/sources.yaml` (`iec_results`) |
| CI-004 | DQ gate | control | `pwatch dq`; exit 2 = not releasable |
| CI-005 | Right-of-reply drafts | process artefact | `drafts/right-of-reply/`; never sent by the bot |
| CI-006 | Joburg LGE 2026 roster | data (TEST) | `data/roster/joburg-2026.csv`; public-role fields only |
| CI-007 | Private git repository | system | `GrokForum/politicianwatch-sa` |
| CI-008 | Bot box worktree | system | `/workspace/politicianwatch-sa` (DEV) |
