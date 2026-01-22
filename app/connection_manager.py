from __future__ import annotations

import asyncio
from dataclasses import dataclass
from typing import Any, Dict, Set

from fastapi import WebSocket


class UserOfflineError(Exception):
    pass


class SendFailedError(Exception):
    pass


@dataclass
class ConnectionSnapshot:
    user_id: str
    connections: Set[WebSocket]


class ConnectionManager:
    def __init__(self) -> None:
        self._connections: Dict[str, Set[WebSocket]] = {}
        self._lock = asyncio.Lock()

    async def connect(self, user_id: str, websocket: WebSocket) -> None:
        await websocket.accept()
        async with self._lock:
            self._connections.setdefault(user_id, set()).add(websocket)

    async def disconnect(self, user_id: str, websocket: WebSocket) -> None:
        async with self._lock:
            sockets = self._connections.get(user_id)
            if not sockets:
                return
            sockets.discard(websocket)
            if not sockets:
                self._connections.pop(user_id, None)

    async def snapshot(self) -> list[ConnectionSnapshot]:
        async with self._lock:
            return [
                ConnectionSnapshot(user_id=user_id, connections=set(sockets))
                for user_id, sockets in self._connections.items()
            ]

    async def has_user(self, user_id: str) -> bool:
        async with self._lock:
            return user_id in self._connections and bool(self._connections[user_id])

    async def broadcast(self, payload: Dict[str, Any]) -> None:
        snapshots = await self.snapshot()
        for snapshot in snapshots:
            await self._send_to_sockets(snapshot.connections, payload)

    async def send_to_user(self, user_id: str, payload: Dict[str, Any]) -> None:
        async with self._lock:
            sockets = set(self._connections.get(user_id, set()))
        if not sockets:
            raise UserOfflineError(f"user {user_id} is offline")
        await self._send_to_sockets(sockets, payload)

    async def _send_to_sockets(
        self, sockets: Set[WebSocket], payload: Dict[str, Any]
    ) -> None:
        failures: list[WebSocket] = []
        sent = 0
        for socket in sockets:
            try:
                await socket.send_json(payload)
                sent += 1
            except Exception:
                failures.append(socket)
        if failures:
            async with self._lock:
                for socket in failures:
                    for user_id, existing in list(self._connections.items()):
                        if socket in existing:
                            existing.discard(socket)
                            if not existing:
                                self._connections.pop(user_id, None)
                            break
        if sent == 0:
            raise SendFailedError("no active connections")
