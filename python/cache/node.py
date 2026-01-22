from __future__ import annotations

import time
from typing import Any, Iterable, Optional

from .persistence import Persistence
from .pubsub import PubSub
from .replication import Replicator
from .storage import Store
from .transport import InMemoryTransport, ReplicationMessage, Transport


class Node:
    def __init__(
        self,
        node_id: str,
        *,
        capacity: int = 1024,
        clock: Optional[callable] = None,
        transport: Optional[Transport] = None,
        persistence: Optional[Persistence] = None,
    ) -> None:
        self.id = node_id
        self._clock = clock or (lambda: int(time.time() * 1000))
        self._store = Store(capacity=capacity, clock=self._clock)
        self._pubsub = PubSub()
        self._replicator = Replicator(transport)
        self._persistence = persistence
        self._version = 0
        if isinstance(transport, InMemoryTransport):
            transport.register(self.id, self.apply_replication)

    def load(self) -> None:
        if self._persistence:
            self._persistence.load(self._store)
            self._sync_version()

    def get(self, key: str) -> Optional[Any]:
        return self._store.get(key)

    def set(
        self,
        key: str,
        value: Any,
        ttl_ms: Optional[int] = None,
        *,
        replica_ids: Optional[Iterable[str]] = None,
    ) -> int:
        version = self._next_version()
        version, evicted = self._store.set(key, value, ttl_ms=ttl_ms, version=version)
        entry = self._store.get_entry(key)
        if self._persistence and entry:
            self._persistence.append_set(key, value, entry.expires_at, version)
        self._replicate(
            replica_ids,
            ReplicationMessage(
                op="set",
                key=key,
                value=value,
                expires_at=entry.expires_at if entry else None,
                version=version,
            ),
        )
        self._record_evictions(evicted, replica_ids)
        return version

    def delete(self, key: str, *, replica_ids: Optional[Iterable[str]] = None) -> bool:
        existed = self._store.delete(key)
        if not existed:
            return False
        version = self._next_version()
        if self._persistence:
            self._persistence.append_delete(key, version)
        self._replicate(
            replica_ids,
            ReplicationMessage(op="del", key=key, version=version),
        )
        return True

    def expire(self, key: str, ttl_ms: int, *, replica_ids: Optional[Iterable[str]] = None) -> bool:
        version = self._next_version()
        ok = self._store.expire(key, ttl_ms, version=version)
        if not ok:
            return False
        entry = self._store.get_entry(key)
        if self._persistence and entry and entry.expires_at is not None:
            self._persistence.append_expire(key, entry.expires_at, version)
        self._replicate(
            replica_ids,
            ReplicationMessage(
                op="expire",
                key=key,
                expires_at=entry.expires_at if entry else None,
                version=version,
            ),
        )
        return True

    def publish(
        self,
        channel: str,
        payload: Any,
        *,
        replica_ids: Optional[Iterable[str]] = None,
    ) -> int:
        delivered = self._pubsub.publish(channel, payload)
        self._replicate(
            replica_ids,
            ReplicationMessage(op="pub", channel=channel, payload=payload),
        )
        return delivered

    def subscribe(self, channel: str, handler) -> callable:
        return self._pubsub.subscribe(channel, handler)

    def sweep_expired(self) -> None:
        self._store.sweep_expired()

    def snapshot(self) -> None:
        if self._persistence:
            self._persistence.snapshot(self._store)

    def apply_replication(self, message: ReplicationMessage) -> None:
        if message.op == "set":
            if not message.key:
                return
            if self._should_skip(message.key, message.version):
                return
            ttl_ms = None
            if message.expires_at is not None:
                ttl_ms = max(message.expires_at - self._clock(), 0)
            self._store.set(
                message.key,
                message.value,
                ttl_ms=ttl_ms,
                version=message.version or 0,
            )
            self._bump_version(message.version)
        elif message.op == "del":
            if not message.key:
                return
            if self._should_skip(message.key, message.version):
                return
            self._store.delete(message.key)
            self._bump_version(message.version)
        elif message.op == "expire":
            if not message.key or message.expires_at is None:
                return
            if self._should_skip(message.key, message.version):
                return
            ttl_ms = max(message.expires_at - self._clock(), 0)
            self._store.expire(message.key, ttl_ms, version=message.version or 0)
            self._bump_version(message.version)
        elif message.op == "pub":
            if message.channel is None:
                return
            self._pubsub.publish(message.channel, message.payload)

    def _should_skip(self, key: str, incoming_version: Optional[int]) -> bool:
        if incoming_version is None:
            return False
        existing = self._store.get_entry(key)
        return existing is not None and incoming_version <= existing.version

    def _replicate(
        self, replica_ids: Optional[Iterable[str]], message: ReplicationMessage
    ) -> None:
        if not replica_ids:
            return
        self._replicator.replicate(replica_ids, message)

    def _record_evictions(self, evicted: Iterable[str], replica_ids: Optional[Iterable[str]]) -> None:
        for key in evicted:
            version = self._next_version()
            if self._persistence:
                self._persistence.append_delete(key, version)
            self._replicate(replica_ids, ReplicationMessage(op="del", key=key, version=version))

    def _next_version(self) -> int:
        self._version += 1
        return self._version

    def _bump_version(self, incoming: Optional[int]) -> None:
        if incoming is not None and incoming > self._version:
            self._version = incoming

    def _sync_version(self) -> None:
        max_version = 0
        for _, entry in self._store.items():
            if entry.version > max_version:
                max_version = entry.version
        self._version = max_version
