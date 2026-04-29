"""
Tree objects: map filenames → blob/tree digests.

Binary wire format (similar to Git's tree)
------------------------------------------
Each entry is a NUL-terminated record:

    <mode> <name>\0<20-or-32-byte raw digest>

We use 32-byte (256-bit) raw digests since we hash with SHA-256.

Helper functions here serialise/deserialise that format, and provide a
convenience wrapper that recursively writes a directory tree to the object
store.
"""

from __future__ import annotations

import struct
from pathlib import Path
from typing import Iterator

from .objects import ObjectType, read_object, write_object

# Mode strings – keep it simple: regular file or sub-tree.
MODE_BLOB = "100644"
MODE_TREE = "040000"

DIGEST_BYTES = 32  # SHA-256


def _encode_entry(mode: str, name: str, digest: str) -> bytes:
    raw_digest = bytes.fromhex(digest)
    return f"{mode} {name}\0".encode() + raw_digest


def _iter_entries(data: bytes) -> Iterator[tuple[str, str, str]]:
    """Yield (mode, name, hex-digest) tuples from raw tree data."""
    i = 0
    while i < len(data):
        null_pos = data.index(b"\0", i)
        header = data[i:null_pos].decode()
        mode, name = header.split(" ", 1)
        raw = data[null_pos + 1 : null_pos + 1 + DIGEST_BYTES]
        digest = raw.hex()
        yield mode, name, digest
        i = null_pos + 1 + DIGEST_BYTES


def serialise_tree(entries: dict[str, tuple[str, str]]) -> bytes:
    """
    Serialise a mapping of  name → (mode, digest)  into raw tree bytes.
    Entries are sorted by name for deterministic hashing.
    """
    parts: list[bytes] = []
    for name in sorted(entries):
        mode, digest = entries[name]
        parts.append(_encode_entry(mode, name, digest))
    return b"".join(parts)


def deserialise_tree(data: bytes) -> dict[str, tuple[str, str]]:
    """Return  name → (mode, digest)  from raw tree bytes."""
    return {name: (mode, digest) for mode, name, digest in _iter_entries(data)}


def write_tree_from_index(
    objects_dir: Path,
    index: dict[str, str],
) -> str:
    """
    Build a flat tree object from a staging index (path → blob-digest)
    and write it to the object store.  Returns the tree's digest.

    For simplicity the index only tracks top-level files; paths with '/'
    are stored as nested trees built on the fly.
    """
    # Split index into top-level files and sub-directories.
    top_level: dict[str, tuple[str, str]] = {}
    subdirs: dict[str, dict[str, str]] = {}

    for path, blob_digest in index.items():
        parts = Path(path).parts
        if len(parts) == 1:
            top_level[parts[0]] = (MODE_BLOB, blob_digest)
        else:
            subdir = parts[0]
            rest = str(Path(*parts[1:]))
            subdirs.setdefault(subdir, {})[rest] = blob_digest

    for subdir, sub_index in subdirs.items():
        sub_tree_digest = write_tree_from_index(objects_dir, sub_index)
        top_level[subdir] = (MODE_TREE, sub_tree_digest)

    raw = serialise_tree(top_level)
    return write_object(objects_dir, "tree", raw)


def read_tree_flat(objects_dir: Path, tree_digest: str) -> dict[str, str]:
    """
    Recursively expand a tree object and return a flat  path → blob-digest
    mapping (same shape as the index).
    """
    _, raw = read_object(objects_dir, tree_digest)
    entries = deserialise_tree(raw)
    result: dict[str, str] = {}
    for name, (mode, digest) in entries.items():
        if mode == MODE_BLOB:
            result[name] = digest
        else:
            for sub_path, blob in read_tree_flat(objects_dir, digest).items():
                result[f"{name}/{sub_path}"] = blob
    return result
