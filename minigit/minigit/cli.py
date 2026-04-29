"""
Command-line interface for minigit.

Usage
-----
    minigit init [--name NAME] [--email EMAIL]
    minigit add <path> [<path> ...]
    minigit commit -m <message>
    minigit status
    minigit log
    minigit diff [--staged]
    minigit checkout <branch-or-digest>
"""

from __future__ import annotations

import argparse
import datetime
import sys
from pathlib import Path

from .repo import Repo, RepoError


def cmd_init(args: argparse.Namespace) -> None:
    repo = Repo(Path("."))
    repo.init(author_name=args.name, author_email=args.email)
    print(f"Initialised empty minigit repository in {repo.minigit_dir}")


def cmd_add(args: argparse.Namespace) -> None:
    repo = Repo.find()
    try:
        repo.add(args.paths)
        print(f"Added {len(args.paths)} path(s) to the index.")
    except RepoError as exc:
        _die(str(exc))


def cmd_commit(args: argparse.Namespace) -> None:
    repo = Repo.find()
    try:
        digest = repo.commit(args.message)
        print(f"[{digest[:12]}] {args.message}")
    except RepoError as exc:
        _die(str(exc))


def cmd_status(args: argparse.Namespace) -> None:
    repo = Repo.find()
    s = repo.status()

    if s["staged"]:
        print("Changes to be committed (staged):")
        for p in s["staged"]:
            print(f"    {p}")
    if s["unstaged"]:
        print("Changes not staged for commit:")
        for p in s["unstaged"]:
            print(f"    {p}")
    if s["untracked"]:
        print("Untracked files:")
        for p in s["untracked"]:
            print(f"    {p}")
    if not any(s.values()):
        print("nothing to commit, working tree clean")


def cmd_log(args: argparse.Namespace) -> None:
    repo = Repo.find()
    entries = repo.log()
    if not entries:
        print("No commits yet.")
        return
    for e in entries:
        dt = datetime.datetime.utcfromtimestamp(e["timestamp"]).strftime(
            "%a %b %d %H:%M:%S %Y +0000"
        )
        print(f"commit {e['digest']}")
        if e["parents"]:
            print(f"Merge: {' '.join(p[:12] for p in e['parents'])}")
        print(f"Author: {e['author']}")
        print(f"Date:   {dt}")
        print()
        for line in e["message"].splitlines():
            print(f"    {line}")
        print()


def cmd_diff(args: argparse.Namespace) -> None:
    repo = Repo.find()
    diffs = repo.diff(staged=args.staged)
    if not diffs:
        print("No differences.")
        return
    for _path, patch in diffs.items():
        print(patch, end="")


def cmd_checkout(args: argparse.Namespace) -> None:
    repo = Repo.find()
    try:
        repo.checkout(args.target)
        print(f"Switched to {args.target!r}")
    except RepoError as exc:
        _die(str(exc))


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        prog="minigit",
        description="A minimal Git-like version-control system.",
    )
    sub = parser.add_subparsers(dest="command", metavar="<command>")
    sub.required = True

    # init
    p_init = sub.add_parser("init", help="Initialise a new repository")
    p_init.add_argument("--name", default="You", help="Author name for config")
    p_init.add_argument("--email", default="you@example.com", help="Author email for config")
    p_init.set_defaults(func=cmd_init)

    # add
    p_add = sub.add_parser("add", help="Add file(s) to the staging area")
    p_add.add_argument("paths", nargs="+", metavar="<path>")
    p_add.set_defaults(func=cmd_add)

    # commit
    p_commit = sub.add_parser("commit", help="Record staged changes as a commit")
    p_commit.add_argument("-m", dest="message", required=True, metavar="<msg>")
    p_commit.set_defaults(func=cmd_commit)

    # status
    p_status = sub.add_parser("status", help="Show working-tree status")
    p_status.set_defaults(func=cmd_status)

    # log
    p_log = sub.add_parser("log", help="Show the commit history")
    p_log.set_defaults(func=cmd_log)

    # diff
    p_diff = sub.add_parser("diff", help="Show changes")
    p_diff.add_argument(
        "--staged",
        action="store_true",
        help="Show staged changes (index vs HEAD) instead of unstaged",
    )
    p_diff.set_defaults(func=cmd_diff)

    # checkout
    p_checkout = sub.add_parser("checkout", help="Restore working tree / switch branch")
    p_checkout.add_argument("target", metavar="<branch-or-digest>")
    p_checkout.set_defaults(func=cmd_checkout)

    args = parser.parse_args(argv)
    args.func(args)


def _die(msg: str) -> None:
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(1)


if __name__ == "__main__":
    main()
