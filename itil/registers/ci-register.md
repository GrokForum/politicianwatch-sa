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
| CI-009 | Joburg CV profiles | data (TEST) | `data/profiles/joburg-2026/*.json` (+ generated `.md`); public role only; CHG-PW-002 |
| CI-010 | Draft-site builder | code | `pwatch/site.py`, `pwatch site build/check`; DRAFT banner, privacy page, robots/noindex/CSP checks; CHG-PW-006 |
| CI-011 | Public site repository | system (PROD host) | `GrokForum/politicianwatch-site`, GitHub Pages legacy build from `main` /, custom domain politicianwatch.grokforum.site; a merge to `main` deploys |
| CI-012 | Nightly workflow | control | `.github/workflows/nightly.yml`; build, gated publish (`PW_PUBLISH_ENABLED` + `PW_SITE_DEPLOY_KEY`), live check; CHG-PW-008 |
| CI-013 | Nightly records | evidence | branch `nightly-log` (`nightly/log.jsonl`, one line per night) + 90-day run artifacts; written by CI-012 only |
