"""Command-line entry point."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path

from pwatch import __version__
from pwatch.dq import exit_code, run
from pwatch.profiles import load_held_profiles, load_profile_dir, render_markdown, roster_index
from pwatch.roster import load_csv, load_joburg_roster
from pwatch.settings import PROFILES_DIR, REPO_ROOT


def _load_profiles(path: Path | None) -> list[dict]:
    if path is None:
        return load_joburg_roster()
    if path.suffix.lower() == ".json":
        data = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(data, dict) and "profiles" in data:
            return data["profiles"]
        if isinstance(data, list):
            return data
        raise SystemExit(f"unrecognised JSON profile document: {path}")
    return load_csv(path)


def cmd_dq(args: argparse.Namespace) -> int:
    path = Path(args.profiles) if args.profiles else None
    profiles = _load_profiles(path)
    as_of = date.fromisoformat(args.as_of) if args.as_of else date.today()
    drafts_root = Path(args.drafts_root) if args.drafts_root else REPO_ROOT
    result = run(profiles, drafts_root=drafts_root, as_of=as_of)
    if path is None:
        # Default run: the gazetted roster plus the CV profiles, each cross-checked to its roster row.
        cv_dir = Path(args.profiles_dir) if args.profiles_dir else PROFILES_DIR
        docs = load_profile_dir(cv_dir)
        cv_result = run(
            [d for _, d in docs],
            drafts_root=drafts_root,
            as_of=as_of,
            roster=roster_index(profiles),
            locator_prefix="cv_profile",
        )
        result = {
            "status": "pass" if result["status"] == "pass" and cv_result["status"] == "pass" else "fail",
            "profiles": result["profiles"],
            "cv_profiles": cv_result["profiles"],
            "cv_profiles_on_hold": len(load_held_profiles(cv_dir)),
            "failures": result["failures"] + cv_result["failures"],
            "failure_count": result["failure_count"] + cv_result["failure_count"],
            "warnings": result.get("warnings", []) + cv_result.get("warnings", []),
            "as_of": result["as_of"],
        }
    print(json.dumps(result, indent=2))
    return exit_code(result)


def cmd_render(args: argparse.Namespace) -> int:
    cv_dir = Path(args.profiles_dir) if args.profiles_dir else PROFILES_DIR
    stale = []
    for p, doc in load_profile_dir(cv_dir):
        md = render_markdown(doc)
        out = p.with_suffix(".md")
        if args.check:
            if not out.is_file() or out.read_text(encoding="utf-8") != md:
                stale.append(str(out))
        else:
            out.write_text(md, encoding="utf-8")
            print(out)
    if stale:
        print("stale renders: " + ", ".join(stale))
        return 2
    return 0


def cmd_fetch_source(args: argparse.Namespace) -> int:
    from pwatch.http import Fetcher
    from pwatch.provenance import fetch_source
    from pwatch.raw import RawStore
    from pwatch.settings import RAW_DIR

    fetcher = Fetcher()
    try:
        out = [fetch_source(u, raw=RawStore(RAW_DIR, resume=False), fetcher=fetcher) for u in args.urls]
    finally:
        fetcher.close()
    print(json.dumps(out, indent=2))
    return 0


def cmd_site_build(args: argparse.Namespace) -> int:
    from pwatch.site import build_site

    out = Path(args.out)
    profiles = _site_profiles(args)
    manifest = build_site(out, profiles=profiles, commit=args.commit)
    from pwatch.withheld import check_tree_for_withheld_urls, check_withheld_register_for_profiles

    leak_fails = check_withheld_register_for_profiles(profiles)
    leak_fails += check_tree_for_withheld_urls(out)
    if (out / "private").exists():
        leak_fails.append("site output must not contain the private/ directory")
    if leak_fails:
        print(json.dumps({"status": "fail", "failures": leak_fails}, indent=2))
        return 2
    print(json.dumps({k: v for k, v in manifest.items() if k != "files"}, indent=2))
    return 0


def _site_profiles(args: argparse.Namespace) -> list:
    """Active CV profiles for the site (CHG-PW-007). Held profiles (`_hold/`) are never loaded."""
    return load_profile_dir(Path(args.profiles_dir) if args.profiles_dir else PROFILES_DIR)


def cmd_site_check(args: argparse.Namespace) -> int:
    from pwatch.site import check_site

    if args.no_data:
        fails = check_site(Path(args.dir))
    else:
        cv_dir = Path(args.profiles_dir) if args.profiles_dir else PROFILES_DIR
        fails = check_site(Path(args.dir), profiles=load_profile_dir(cv_dir), held=load_held_profiles(cv_dir))
    print(json.dumps({"status": "fail" if fails else "pass", "failures": fails}, indent=2))
    return 2 if fails else 0


def cmd_live_check(args: argparse.Namespace) -> int:
    from pwatch.live_check import _client, record, run_checks, wait_for_build, write_record

    expected = json.loads(Path(args.expect_manifest).read_text(encoding="utf-8")) if args.expect_manifest and Path(args.expect_manifest).is_file() else None
    dq = json.loads(Path(args.dq).read_text(encoding="utf-8")) if args.dq and Path(args.dq).is_file() else None
    published = args.publish_result == "success"
    base = args.url.rstrip("/")
    with _client() as client:
        if published and expected and args.wait_seconds:
            wait_for_build(client, base, expected["build_id"], timeout_s=args.wait_seconds)
        checks = run_checks(
            base,
            expected=expected,
            published=published,
            publish_enabled=args.publish_enabled == "true",
            client=client,
        )
    rec = record(
        url=base,
        checks=checks,
        build_result=args.build_result,
        publish_result=args.publish_result,
        publish_enabled=args.publish_enabled == "true",
        expected=expected,
        dq=dq,
        run_url=args.run_url,
    )
    write_record(rec, Path(args.out) if args.out else None, Path(args.log) if args.log else None)
    print(json.dumps(rec, indent=2))
    return 0 if rec["result"] == "green" else 2


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="pwatch", description="PoliticianWatch SA pipeline")
    p.add_argument("--version", action="version", version=__version__)
    sub = p.add_subparsers(dest="command", required=True)
    dq = sub.add_parser("dq", help="run the data-quality gate (exit 2 = not releasable)")
    dq.add_argument("--profiles", help="CSV or JSON profiles (default: committed Joburg roster)")
    dq.add_argument("--drafts-root", help="repo root used to resolve right-of-reply draft paths")
    dq.add_argument("--as-of", help="YYYY-MM-DD, for no_response deadline checks (default: today)")
    dq.add_argument("--profiles-dir", help="CV profile JSON directory (default: data/profiles/joburg-2026)")
    dq.set_defaults(func=cmd_dq)
    rd = sub.add_parser("render", help="write markdown renderings next to CV profile JSON files")
    rd.add_argument("--profiles-dir", help="CV profile JSON directory (default: data/profiles/joburg-2026)")
    rd.add_argument("--check", action="store_true", help="exit 2 if any rendering is missing or stale")
    rd.set_defaults(func=cmd_render)
    fs = sub.add_parser("fetch-source", help="fetch profile source pages, log them in the raw manifest, print retrieved_at")
    fs.add_argument("urls", nargs="+", help="source URL(s) to fetch")
    fs.set_defaults(func=cmd_fetch_source)
    st = sub.add_parser("site", help="static draft site: build into a directory, or check a built directory")
    st_sub = st.add_subparsers(dest="site_command", required=True)
    sb = st_sub.add_parser("build", help="write the static draft site into --out (publishes nothing)")
    sb.add_argument("--out", required=True, help="output directory, e.g. _site")
    sb.add_argument("--commit", help="source commit SHA to record in manifest.json")
    sb.add_argument("--profiles-dir", help="CV profile JSON directory (default: data/profiles/joburg-2026)")
    sb.set_defaults(func=cmd_site_build)
    sc = st_sub.add_parser("check", help="exit 2 if a built site breaks a draft-site rule")
    sc.add_argument("dir", help="built site directory")
    sc.add_argument("--profiles-dir", help="CV profile JSON directory to check coverage against (default: data/profiles/joburg-2026)")
    sc.add_argument("--no-data", action="store_true", help="skip the coverage check (page and claim rules only)")
    sc.set_defaults(func=cmd_site_check)
    lc = sub.add_parser("live-check", help="check the deployed draft site and write one nightly record (exit 2 = red)")
    lc.add_argument("--url", default="https://politicianwatch.grokforum.site", help="site base URL")
    lc.add_argument("--expect-manifest", help="tonight's built manifest.json (expected profile count and build id)")
    lc.add_argument("--dq", help="tonight's `pwatch dq` JSON output, summarised into the record")
    lc.add_argument("--build-result", default="success", help="result of tonight's build job")
    lc.add_argument("--publish-result", default="skipped", help="result of tonight's publish job (success/skipped/failure)")
    lc.add_argument("--publish-enabled", default="false", help="value of the PW_PUBLISH_ENABLED flag")
    lc.add_argument("--wait-seconds", type=int, default=0, help="after a publish, wait up to N s for the live build id")
    lc.add_argument("--run-url", help="link to the workflow run")
    lc.add_argument("--out", help="write the record to this JSON file")
    lc.add_argument("--log", help="append the record to this JSONL log")
    lc.set_defaults(func=cmd_live_check)
    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    sys.exit(main())
