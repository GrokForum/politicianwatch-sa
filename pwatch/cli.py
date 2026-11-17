"""Command-line entry point."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path

from pwatch import __version__
from pwatch.dq import exit_code, run
from pwatch.roster import load_csv, load_joburg_roster
from pwatch.settings import REPO_ROOT


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
    print(json.dumps(result, indent=2))
    return exit_code(result)


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="pwatch", description="PoliticianWatch SA pipeline")
    p.add_argument("--version", action="version", version=__version__)
    sub = p.add_subparsers(dest="command", required=True)
    dq = sub.add_parser("dq", help="run the data-quality gate (exit 2 = not releasable)")
    dq.add_argument("--profiles", help="CSV or JSON profiles (default: committed Joburg roster)")
    dq.add_argument("--drafts-root", help="repo root used to resolve right-of-reply draft paths")
    dq.add_argument("--as-of", help="YYYY-MM-DD, for no_response deadline checks (default: today)")
    dq.set_defaults(func=cmd_dq)
    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    sys.exit(main())
