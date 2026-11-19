# Fresh public repository plan (PoliticianWatch SA)

Status: **plan only**. Nothing here creates a repository, pushes, publishes or changes settings. Each step that does needs its own named change record and the owner's quoted GO. The owner has said the old repositories (`GrokForum/politicianwatch-sa` and `GrokForum/politicianwatch-site`) will be deleted once the fresh repository exists. Until then they remain the record.

## 1. End of road for the Johannesburg pilot

### Remaining scope we would call done

1. **Profiles.** Every active CV profile passes `pwatch dq` with zero failures. Each fact is labelled and dated, with an allowed source or Unknown, and has public-role information only. The owner decides the pilot's target number (24 of 270 today) and records it. Held profiles stay held or return only through a change record.
2. **Council offices.** The 2026–2031 executive mayor, speaker and mayoral committee are recorded from an allowed source, or kept Unknown with a dated note.
3. **Right of reply.** For every adverse item (6 items on 4 profiles today, all "Right of reply: pending"), the owner has recorded the state: sent and date, reply received, or a decision not to send. No adverse item goes public without that record.
4. **Site.** The DRAFT banner, privacy and corrections page (privacy@grokforum.site), 404, noindex meta and robots `Disallow: /` are all present. `pwatch site check` passes. Publishing has been turned on only after the owner's GO (CHG-PW-008 gate).
5. **Operations.** The nightly runs on `main`, records to `nightly-log`, and the live check verifies the deployed build.
6. **Records.** Every change on `main` has an RFC, a change-log row and a STATUS line, with a reviewer PASS and an owner GO.
7. **Stability.** The 14-day checklist below passes.

### 14-day stability checklist (every night for 14 consecutive nights, Africa/Johannesburg)

- [ ] The nightly workflow is green every night, and there is one `nightly-log` record per night (no gaps).
- [ ] Live checks are green: pages 200, the deployed `build_id` matches the build, DRAFT banner, noindex, robots and the privacy page are present.
- [ ] Zero POPIA / personal-information scan hits on the built site and the tree (ID numbers, personal phones and emails, home addresses, accounts, private family or health details, names-file terms).
- [ ] `pwatch dq`: zero failures; `pwatch render --check` passes; `pwatch site check` passes.
- [ ] Every claim's source link resolves (HTTP 2xx/3xx), or is flagged and recorded with a dated note and a follow-up. This needs a link check that does not exist yet (see LATER.md); until then it is a manual check, recorded weekly.
- [ ] Every page carries the DRAFT banner and the noindex meta; robots `Disallow: /` is unchanged.
- [ ] No unreviewed change on `main`: every merge has a reviewer PASS on the exact head and an owner GO; no direct pushes.
- [ ] The state of each right-of-reply item is recorded by the owner (not inferred by a bot).
- [ ] Every unexplained incident is resolved or has its own incident record; no open high or medium risk without an owner decision.
- [ ] The secret-scan and workflow scan (gitleaks, actionlint, zizmor) are clean on `main`.

The streak restarts at zero after any red night, any POPIA hit, or any unreviewed change on `main`.

## 2. What must NOT carry over to a fresh public repository

Inspected on the tree at `main` `a0698d20` and the repo's refs (19 Nov 2026):

| Item | Where today | Why it stays out |
|---|---|---|
| All old git history, branches and PR refs | every commit before the fresh root; `dev/chg-pw-001`…`008` branches | Older commits carry machine-local paths, earlier commit identities (including a personal address in merge-commit metadata), and superseded wording about sources with personal details |
| Snapshot and other tags | `snapshot-2026-11-17-pre-pw-pr1`…`pr5`, `snapshot-2026-11-19-pre-pw-pr6`…`pr8` | They point at old history |
| `nightly-log` branch | private repo (created by the first nightly run) | Run records from the old repo; a fresh streak starts in the new repo |
| Held profiles and their drafts | `data/profiles/joburg-2026/_hold/`, `drafts/right-of-reply/CHG-PW-003/_hold/` | Not published, identity unresolved |
| Right-of-reply drafts (unsent correspondence) | `drafts/right-of-reply/CHG-PW-002/`, `CHG-PW-003/` | Unsent letters to named people; internal until the owner sends them. `TEMPLATE.md`, `README.md` and the synthetic `SYNTH-001.md` may carry over |
| Research notes that describe sources seen and not used | `docs/profiles-joburg-2026-batch-1.md` and `-batch-2.md` ("seen, not used" tables and notes, including descriptions of pages with private details) | They point readers to where private details can be found. Carry over only a rewritten, neutral batch summary, if anything |
| Old RFCs, STATUS history, change log and registers | `itil/changes/CHG-PW-001`…`009`, `STATUS.md`, `itil/registers/*` | Internal process records with reviewer and agent names, superseded source notes and old SHAs. The fresh repo starts its own ITIL records with one seeding RFC that references the old records by name only |
| Fetched source copies and raw binaries | `data/raw/profile-sources/`, `data/raw/**/*.pdf` (already git-ignored) | They can carry personal information. Only the provenance manifest and `.sha256` files are committed |
| Names files and local scan lists | `.popia-names.local` (git-ignored; not present on this machine) and any reviewer names file | They list terms to search for; they must never be in a repo |
| Tests that use real people's slugs as fixtures | `tests/test_dq.py` (two profiles' Disputed labels) and `tests/test_live_check.py` (one profile) | Replace with synthetic fixtures before seeding, so tests do not name real people outside the published data |
| Workflow secret and variable references, and environment setup | `.github/workflows/nightly.yml` (`secrets.PW_SITE_DEPLOY_KEY`, `vars.PW_PUBLISH_ENABLED`, environment `site-publish`) | The names may carry over, but no values, deploy keys or environments. Each is recreated by the owner after a GO. The fresh repo starts with publishing off |
| Box or machine paths | removed from the tree by CHG-PW-009 (the CHG-PW-006 RFC, the CI register (CI-008) and ADR-0001); they remain in old history | Seed from a `main` that includes CHG-PW-009 (merged as `ce45d829`); keep the history out; re-grep before seeding |

May carry over after the checks in section 3: the `pwatch` package, schemas, tests (with synthetic fixtures), `scripts/`, the workflow (gate off), the site assets, `data/roster/` (gazette public record), active profiles and their renders, `data/sources.json`, `docs/allowed-sources.md`, `docs/sources-joburg-lge-2026.md`, ADRs (with reviewer names neutralised), `README.md`, `AGENTS.md`, `REVIEW.md`, `pyproject.toml` and `uv.lock`.

## 3. Seeding procedure (each step needs a named change and the owner's GO where marked)

1. **Pick the approved source.** The exact `main` commit that both reviewers passed and the owner approved. Record its full SHA in the seeding RFC.
2. **Export a clean tree, with no history:** `git archive --format=tar <approved-sha> | tar -x -C /path/to/seed`.
3. **Apply the exclusion list** in section 2 (delete paths; swap real-person test fixtures for synthetic ones; replace the ITIL folder with a fresh seeding RFC and empty registers). Commit the exclusion list itself as a file in the seed (paths only, no personal data).
4. **Scan and test in the seed directory:**
   - PI scan: the review kit with `--scan-tree`, a names file kept outside the tree, and `--site-dir` on a fresh build. gitleaks on the directory. A grep for machine paths, ID-number, phone and email patterns. Expect zero hits apart from role and noreply addresses.
   - `uv run pytest -q`, `uv run pwatch dq` (zero failures), `uv run pwatch render --check`, `uv run pwatch site build` + `site check`, `actionlint`, `zizmor`.
   - A second reviewer repeats the scan on the same directory and confirms the result.
5. **Owner GO: create the fresh repository** (empty, no template, no README). Visibility as the owner decides.
6. **One root commit** in the seed, `git init`, under the neutral identity "PoliticianWatch publisher" <noreply@politicianwatch.grokforum.site>, with a neutral message naming the seeding RFC and the approved source SHA. No old history, no tags, one branch `main`.
7. **Owner GO: push the root commit** (one push, `main` only).
8. **Branch protection on `main`** (owner; precondition: public repo or paid plan, needed for environment required reviewers and branch protection): require a pull request, at least one approving review from a human, no force-push, no deletion. Merge only on a human approval; bots may open PRs but never merge.
9. **Re-create operations** (owner, separate GO): the `site-publish` environment, the deploy key secret and the `PW_PUBLISH_ENABLED` variable (left off until a publish GO). The nightly then starts a fresh 14-day streak.
10. **Retire the old repositories** (owner): after the fresh repo is verified, the owner deletes the old repos as stated. Before that, take an owner-held offline archive if the owner wants one. That is the owner's choice, and it is not stored in the new repo.
