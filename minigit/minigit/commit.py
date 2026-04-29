"""
Commit objects: encode the commit graph.

Wire format (plain text, easy to inspect)
------------------------------------------
    tree <tree-digest>
    parent <parent-digest>     # zero or more lines
    author <name> <email> <unix-timestamp> +0000
    committer <name> <email> <unix-timestamp> +0000

    <commit message>

This mirrors Git's commit format closely so the design rationale is
transparent, while staying simple enough to parse without a full parser.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from .objects import read_object, write_object


@dataclass
class CommitData:
    tree: str
    message: str
    author_name: str
    author_email: str
    parents: list[str] = field(default_factory=list)
    timestamp: int = field(default_factory=lambda: int(time.time()))


def serialise_commit(c: CommitData) -> bytes:
    lines: list[str] = []
    lines.append(f"tree {c.tree}")
    for p in c.parents:
        lines.append(f"parent {p}")
    ts = f"{c.timestamp} +0000"
    lines.append(f"author {c.author_name} <{c.author_email}> {ts}")
    lines.append(f"committer {c.author_name} <{c.author_email}> {ts}")
    lines.append("")
    lines.append(c.message)
    return "\n".join(lines).encode()


def deserialise_commit(data: bytes) -> CommitData:
    text = data.decode()
    header_block, _, message = text.partition("\n\n")

    tree = ""
    parents: list[str] = []
    author_name = ""
    author_email = ""
    timestamp = 0

    for line in header_block.splitlines():
        if line.startswith("tree "):
            tree = line[5:]
        elif line.startswith("parent "):
            parents.append(line[7:])
        elif line.startswith("author "):
            # author Name <email> timestamp tz
            rest = line[7:]
            lt = rest.index("<")
            gt = rest.index(">")
            author_name = rest[:lt].strip()
            author_email = rest[lt + 1 : gt]
            ts_part = rest[gt + 1 :].strip().split()[0]
            timestamp = int(ts_part)

    return CommitData(
        tree=tree,
        message=message,
        author_name=author_name,
        author_email=author_email,
        parents=parents,
        timestamp=timestamp,
    )


def write_commit(objects_dir: Path, c: CommitData) -> str:
    raw = serialise_commit(c)
    return write_object(objects_dir, "commit", raw)


def read_commit(objects_dir: Path, digest: str) -> CommitData:
    obj_type, raw = read_object(objects_dir, digest)
    if obj_type != "commit":
        raise TypeError(f"expected commit, got {obj_type}")
    return deserialise_commit(raw)


def iter_commits(objects_dir: Path, head_digest: str):
    """Walk the first-parent chain from *head_digest* back to the root."""
    current: Optional[str] = head_digest
    while current:
        c = read_commit(objects_dir, current)
        yield current, c
        current = c.parents[0] if c.parents else None
