"""Stable CLI for agents. Only read-only GitHub API calls; file output stays private."""
import argparse
import json
import sys

from .analysis import analyze
from .frontier import compare
from .github_reader import collect
from .private_io import read_json, write_private_json
from .quality import review_controls


def main(argv=None):
    parser = argparse.ArgumentParser(prog="aco")
    sub = parser.add_subparsers(dest="command", required=True)
    gather = sub.add_parser("collect", help="read existing GitHub Actions runs")
    gather.add_argument("--repo", required=True)
    gather.add_argument("--max-runs", type=int, default=50)
    gather.add_argument("--output", required=True, help="new private file OUTSIDE any git checkout")
    for command in ("analyze", "review-controls", "frontier"):
        opt = sub.add_parser(command)
        opt.add_argument("--input", required=True)
        opt.add_argument("--output", required=True, help="new private file OUTSIDE any git checkout")
    args = parser.parse_args(argv)
    try:
        if args.command == "collect":
            payload = collect(args.repo, args.max_runs)
        else:
            source = read_json(args.input)
            payload = {"analyze": analyze, "review-controls": review_controls,
                       "frontier": compare}[args.command](source)
        target = write_private_json(args.output, payload)
        # Deliberately do not print source identity, run IDs, logs or the report.
        print(json.dumps({"written": True, "command": args.command,
                          "schema": payload["schema"], "private_output": True}))
        return 0
    except (ValueError, OSError, RuntimeError, KeyError) as exc:
        # Do not include exception details that could expose private content.
        print(json.dumps({"written": False, "command": args.command,
                          "error": type(exc).__name__,
                          "status": "unknown_or_refused"}), file=sys.stderr)
        return 3


if __name__ == "__main__":
    raise SystemExit(main())
