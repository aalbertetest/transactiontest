from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Optional

from .storage import Store


class Persistence:
    def __init__(self, snapshot_path: str, log_path: str) -> None:
        self._snapshot_path = Path(snapshot_path)
        self._log_path = Path(log_path)

    def append_set(self, key: str, value: Any, expires_at: Optional[int], version: int) -> None:
        self._append(
            {
                "op": "set",
                "key": key,
                "value": value,
                "expires_at": expires_at,
                "version": version,
            }
        )

    def append_delete(self, key: str, version: int) -> None:
        self._append({"op": "del", "key": key, "version": version})

    def append_expire(self, key: str, expires_at: int, version: int) -> None:
        self._append(
            {"op": "expire", "key": key, "expires_at": expires_at, "version": version}
        )

    def snapshot(self, store: Store) -> None:
        data: Dict[str, Dict[str, Any]] = {}
        for key, entry in store.items():
            if entry.expires_at is not None and store._clock() >= entry.expires_at:
                continue
            data[key] = {
                "value": entry.value,
                "expires_at": entry.expires_at,
                "version": entry.version,
            }
        self._snapshot_path.parent.mkdir(parents=True, exist_ok=True)
        self._snapshot_path.write_text(json.dumps(data))
        if self._log_path.exists():
            self._log_path.write_text("")

    def load(self, store: Store) -> None:
        if self._snapshot_path.exists():
            raw = self._snapshot_path.read_text()
            if raw.strip():
                snapshot = json.loads(raw)
                self._apply_snapshot(store, snapshot)
        if self._log_path.exists():
            for line in self._log_path.read_text().splitlines():
                if line.strip():
                    self._apply_log_entry(store, json.loads(line))

    def _append(self, record: Dict[str, Any]) -> None:
        self._log_path.parent.mkdir(parents=True, exist_ok=True)
        with self._log_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record))
            handle.write("\n")

    def _apply_snapshot(self, store: Store, snapshot: Dict[str, Any]) -> None:
        now = store._clock()
        for key, data in snapshot.items():
            expires_at = data.get("expires_at")
            if expires_at is not None and now >= expires_at:
                continue
            ttl_ms = None if expires_at is None else max(expires_at - now, 0)
            version = int(data.get("version", 0))
            existing = store.get_entry(key)
            if existing and version <= existing.version:
                continue
            store.set(key, data.get("value"), ttl_ms=ttl_ms, version=version)

    def _apply_log_entry(self, store: Store, record: Dict[str, Any]) -> None:
        op = record.get("op")
        key = record.get("key")
        version = int(record.get("version", 0))
        existing = store.get_entry(key) if key else None
        if existing and version <= existing.version:
            return
        if op == "set":
            expires_at = record.get("expires_at")
            ttl_ms = None
            if expires_at is not None:
                ttl_ms = max(expires_at - store._clock(), 0)
            store.set(key, record.get("value"), ttl_ms=ttl_ms, version=version)
        elif op == "del":
            store.delete(key)
        elif op == "expire":
            expires_at = record.get("expires_at")
            if expires_at is None:
                return
            ttl_ms = max(expires_at - store._clock(), 0)
            store.expire(key, ttl_ms, version=version)
