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
    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    sys.exit(main())
