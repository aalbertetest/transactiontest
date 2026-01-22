from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict, Optional


@dataclass
class ReplicationMessage:
    op: str
    key: Optional[str] = None
    value: object = None
    ttl_ms: Optional[int] = None
    expires_at: Optional[int] = None
    version: Optional[int] = None
    channel: Optional[str] = None
    payload: object = None


class Transport:
    def send(self, peer_id: str, message: ReplicationMessage) -> None:
        raise NotImplementedError


class InMemoryTransport(Transport):
    def __init__(self) -> None:
        self._handlers: Dict[str, Callable[[ReplicationMessage], None]] = {}

    def register(self, peer_id: str, handler: Callable[[ReplicationMessage], None]) -> None:
        self._handlers[peer_id] = handler

    def send(self, peer_id: str, message: ReplicationMessage) -> None:
        handler = self._handlers.get(peer_id)
        if handler:
            handler(message)
