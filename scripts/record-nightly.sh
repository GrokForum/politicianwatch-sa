#!/usr/bin/env bash
# CHG-PW-008: append one nightly record to nightly/log.jsonl on the "nightly-log" branch
# (an orphan branch of this private repo; never main) and keep the night's full record as
# nightly/<YYYY-MM-DD>-<run id>.json. Runs in GitHub Actions with the job's GITHUB_TOKEN.
set -euo pipefail
rec="$1"
test -s "$rec"
night=$(python3 -c 'import json,sys;print(json.load(open(sys.argv[1]))["night_sast"])' "$rec")
remote="${PW_LOG_REMOTE:-https://x-access-token:${GH_TOKEN:-}@github.com/${GITHUB_REPOSITORY:-}.git}"  # PW_LOG_REMOTE: tests only
dir=$(mktemp -d)
if git ls-remote --exit-code --heads "$remote" nightly-log >/dev/null 2>&1; then
  git clone --quiet --depth 1 --branch nightly-log "$remote" "$dir"
else
  git init --quiet -b nightly-log "$dir"
  git -C "$dir" remote add origin "$remote"
  printf '# Nightly records (CHG-PW-008)\n\nOne JSON line per night in `nightly/log.jsonl`; full records in `nightly/`. Written by the nightly workflow only.\n' > "$dir/README.md"
fi
mkdir -p "$dir/nightly"
python3 -c 'import json,sys;print(json.dumps(json.load(open(sys.argv[1])),separators=(",",":")))' "$rec" >> "$dir/nightly/log.jsonl"
cp "$rec" "$dir/nightly/${night}-${GITHUB_RUN_ID}.json"
cd "$dir"
git config user.name "PoliticianWatch publisher"
git config user.email "noreply@politicianwatch.grokforum.site"
git add -A
git commit --quiet -m "Nightly record ${night} (run ${GITHUB_RUN_ID})"
git push --quiet origin HEAD:nightly-log
