"""
Content-addressed object store.

Every piece of data (blob, tree, commit) is hashed with SHA-256 and stored
under  .minigit/objects/<first-2-hex>/<remaining-62-hex>.

Object format on disk
---------------------
The file is the raw, zlib-compressed payload.  The payload is:

    <type> <size>\0<raw-content>

This mirrors Git's loose-object layout so the design is easy to explain.
"""

from __future__ import annotations

import hashlib
import zlib
from pathlib import Path
from typing import Literal

ObjectType = Literal["blob", "tree", "commit"]


def _hash_object(obj_type: ObjectType, data: bytes) -> tuple[str, bytes]:
    """Return (hex-digest, compressed-payload) for *data* of *obj_type*."""
    header = f"{obj_type} {len(data)}\0".encode()
    payload = header + data
    digest = hashlib.sha256(payload).hexdigest()
    return digest, zlib.compress(payload)


def _object_path(objects_dir: Path, digest: str) -> Path:
    return objects_dir / digest[:2] / digest[2:]


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def write_object(objects_dir: Path, obj_type: ObjectType, data: bytes) -> str:
    """Compress and store *data*; return its SHA-256 hex digest."""
    digest, compressed = _hash_object(obj_type, data)
    path = _object_path(objects_dir, digest)
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(compressed)
    return digest


def read_object(objects_dir: Path, digest: str) -> tuple[ObjectType, bytes]:
    """Decompress and return *(type, raw-data)* for the given digest."""
    path = _object_path(objects_dir, digest)
    if not path.exists():
        raise KeyError(f"object not found: {digest}")
    payload = zlib.decompress(path.read_bytes())
    null_idx = payload.index(b"\0")
    header = payload[:null_idx].decode()
    obj_type, _ = header.split(" ", 1)
    data = payload[null_idx + 1 :]
    return obj_type, data  # type: ignore[return-value]


def object_exists(objects_dir: Path, digest: str) -> bool:
    return _object_path(objects_dir, digest).exists()
