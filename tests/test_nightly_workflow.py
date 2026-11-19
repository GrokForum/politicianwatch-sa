"""CHG-PW-008: the nightly workflow's publish gate and evidence steps, and the log recorder."""

from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
WF = ROOT / ".github" / "workflows" / "nightly.yml"


def wf() -> dict:
    doc = yaml.safe_load(WF.read_text(encoding="utf-8"))
    doc["on"] = doc.pop(True, doc.get("on"))  # YAML 1.1 reads the key `on` as True
    return doc


def test_triggers_are_nightly_cron_and_manual_only() -> None:
    on = wf()["on"]
    assert set(on) == {"schedule", "workflow_dispatch"}
    assert on["schedule"] == [{"cron": "30 1 * * *"}]
    assert on["workflow_dispatch"] in (None, {})  # no inputs that could force a publish


def test_publish_is_gated_on_flag_main_and_green_build() -> None:
    jobs = wf()["jobs"]
    cond = jobs["publish"]["if"]
    assert "vars.PW_PUBLISH_ENABLED == 'true'" in cond
    assert "github.ref == 'refs/heads/main'" in cond
    assert "needs.build.result == 'success'" in cond
    assert " || " not in cond
    steps = jobs["publish"]["steps"]
    assert "PW_SITE_DEPLOY_KEY is not set" in steps[0]["run"] and "exit 1" in steps[0]["run"]
    push_jobs = [n for n, j in jobs.items() if any("push origin HEAD:main" in (s.get("run") or "") for s in j["steps"])]
    assert push_jobs == ["publish"]


def test_default_permissions_read_only_and_only_live_check_writes() -> None:
    doc = wf()
    assert doc["permissions"] == {"contents": "read"}
    writers = {n for n, j in doc["jobs"].items() if j.get("permissions")}
    assert writers == {"live-check"} and doc["jobs"]["live-check"]["permissions"] == {"contents": "write"}


def test_build_runs_tests_dq_render_site_build_and_check() -> None:
    runs = " ".join(s.get("run") or "" for s in wf()["jobs"]["build"]["steps"])
    for cmd in ("pytest", "pwatch dq", "pwatch render --check", "pwatch site build", "pwatch site check"):
        assert cmd in runs


def test_live_check_always_runs_and_records() -> None:
    job = wf()["jobs"]["live-check"]
    assert job["if"] == "${{ always() }}" and job["needs"] == ["build", "publish"]
    runs = " ".join(s.get("run") or "" for s in job["steps"])
    assert "pwatch live-check" in runs and "record-nightly.sh" in runs
    uploads = [s for s in job["steps"] if str(s.get("uses", "")).startswith("actions/upload-artifact@")]
    assert uploads and uploads[0]["with"]["retention-days"] == 90


def test_actions_are_pinned_to_commit_shas() -> None:
    for job in wf()["jobs"].values():
        for s in job["steps"]:
            if "uses" in s:
                ref = s["uses"].split("@", 1)[1]
                assert len(ref) == 40 and all(c in "0123456789abcdef" for c in ref), s["uses"]


def test_record_script_appends_to_nightly_log_branch(tmp_path: Path) -> None:
    remote = tmp_path / "remote.git"
    subprocess.run(["git", "init", "--quiet", "--bare", str(remote)], check=True)
    rec = tmp_path / "result.json"
    rec.write_text(json.dumps({"night_sast": "2026-11-19", "result": "red"}), encoding="utf-8")
    env = dict(os.environ, PW_LOG_REMOTE=str(remote), GITHUB_RUN_ID="111", GIT_CONFIG_GLOBAL="/dev/null")
    for run_id in ("111", "222"):
        env["GITHUB_RUN_ID"] = run_id
        subprocess.run(["bash", str(ROOT / "scripts" / "record-nightly.sh"), str(rec)], check=True, env=env, capture_output=True)
    log = subprocess.run(["git", "--git-dir", str(remote), "show", "nightly-log:nightly/log.jsonl"], check=True, capture_output=True, text=True).stdout
    assert [json.loads(x)["result"] for x in log.splitlines()] == ["red", "red"]
    files = subprocess.run(["git", "--git-dir", str(remote), "ls-tree", "-r", "--name-only", "nightly-log"], check=True, capture_output=True, text=True).stdout.split()
    assert "nightly/2026-11-19-111.json" in files and "nightly/2026-11-19-222.json" in files
    branches = subprocess.run(["git", "--git-dir", str(remote), "branch", "--list"], check=True, capture_output=True, text=True).stdout.split()
    assert branches == ["nightly-log"]
