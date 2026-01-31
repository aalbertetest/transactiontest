from __future__ import annotations

import asyncio
import contextlib
import math
import time
from dataclasses import dataclass
from typing import Any
from uuid import uuid4

from fastapi import WebSocket

from .config import Settings
from .db import Database
from .models import GameEvent


MAX_VIOLATIONS = 5


class TokenBucket:
    def __init__(self, rate: float, capacity: float) -> None:
        self.rate = rate
        self.capacity = capacity
        self.tokens = capacity
        self.last_check = time.monotonic()

    def consume(self, amount: float = 1.0) -> bool:
        now = time.monotonic()
        elapsed = now - self.last_check
        self.last_check = now
        self.tokens = min(self.capacity, self.tokens + elapsed * self.rate)
        if self.tokens >= amount:
            self.tokens -= amount
            return True
        return False


@dataclass
class PlayerRuntime:
    player_id: str
    websocket: WebSocket
    x: float = 0.0
    y: float = 0.0
    last_seq: int = 0
    violations: int = 0
    rate_limiter: TokenBucket | None = None


class EventLogger:
    def __init__(self, db: Database) -> None:
        self.db = db

    async def log(
        self, session_id: str, player_id: str, event_type: str, payload: dict[str, Any]
    ) -> None:
        async with self.db.sessionmaker() as session:
            session.add(
                GameEvent(
                    id=str(uuid4()),
                    session_id=session_id,
                    player_id=player_id,
                    event_type=event_type,
                    payload=payload,
                )
            )
            await session.commit()


class GameSessionRuntime:
    def __init__(self, session_id: str, settings: Settings, logger: EventLogger) -> None:
        self.session_id = session_id
        self.settings = settings
        self.logger = logger
        self.players: dict[str, PlayerRuntime] = {}
        self.state_version = 0
        self.lock = asyncio.Lock()
        self.last_activity = time.monotonic()

    async def connect(self, player_id: str, websocket: WebSocket) -> None:
        await websocket.accept()
        async with self.lock:
            if player_id in self.players:
                old = self.players[player_id]
                with contextlib.suppress(Exception):
                    await old.websocket.close(code=4002)
            self.players[player_id] = PlayerRuntime(
                player_id=player_id,
                websocket=websocket,
                rate_limiter=TokenBucket(
                    self.settings.max_input_rate, self.settings.max_input_rate
                ),
            )
            self.last_activity = time.monotonic()
            await websocket.send_json(self._serialize_state())
        self._fire_and_forget(
            player_id, "connect", {"session_id": self.session_id}
        )

    async def disconnect(self, player_id: str) -> None:
        async with self.lock:
            if player_id in self.players:
                self.players.pop(player_id, None)
                self.last_activity = time.monotonic()
        self._fire_and_forget(
            player_id, "disconnect", {"session_id": self.session_id}
        )

    async def handle_message(self, player_id: str, message: dict[str, Any]) -> None:
        message_type = message.get("type")
        if message_type == "input":
            await self._handle_input(player_id, message)
        elif message_type == "ping":
            await self._send_to_player(
                player_id, {"type": "pong", "server_ts": time.time()}
            )

    async def _handle_input(self, player_id: str, message: dict[str, Any]) -> None:
        async with self.lock:
            player = self.players.get(player_id)
            if not player:
                return
            seq = int(message.get("seq", 0))
            if seq <= player.last_seq:
                await self._record_violation(player, "sequence")
                return
            if player.rate_limiter and not player.rate_limiter.consume():
                await self._record_violation(player, "rate_limit")
                return

            dx = float(message.get("dx", 0.0))
            dy = float(message.get("dy", 0.0))
            if abs(dx) > 1.0 or abs(dy) > 1.0:
                await self._record_violation(player, "input_bounds")
                return

            dt = float(message.get("dt", 0.05))
            dt = max(0.0, min(dt, 0.1))
            norm = math.hypot(dx, dy)
            if norm > 1.0:
                dx /= norm
                dy /= norm

            player.x += dx * self.settings.max_speed * dt
            player.y += dy * self.settings.max_speed * dt
            player.last_seq = seq
            self.state_version += 1
            self.last_activity = time.monotonic()

            state_payload = self._serialize_state()

        self._fire_and_forget(
            player_id,
            "input",
            {
                "seq": seq,
                "dx": dx,
                "dy": dy,
                "dt": dt,
                "version": self.state_version,
            },
        )
        await self._broadcast(state_payload)

    async def _record_violation(self, player: PlayerRuntime, reason: str) -> None:
        player.violations += 1
        self._fire_and_forget(
            player.player_id, "violation", {"reason": reason, "count": player.violations}
        )
        if player.violations >= MAX_VIOLATIONS:
            with contextlib.suppress(Exception):
                await player.websocket.close(code=4003)
            self.players.pop(player.player_id, None)

    async def _broadcast(self, payload: dict[str, Any]) -> None:
        tasks = []
        for runtime in self.players.values():
            tasks.append(runtime.websocket.send_json(payload))
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)

    async def _send_to_player(self, player_id: str, payload: dict[str, Any]) -> None:
        runtime = self.players.get(player_id)
        if runtime:
            with contextlib.suppress(Exception):
                await runtime.websocket.send_json(payload)

    def _serialize_state(self) -> dict[str, Any]:
        return {
            "type": "state",
            "session_id": self.session_id,
            "version": self.state_version,
            "server_ts": time.time(),
            "players": {
                player_id: {"x": runtime.x, "y": runtime.y}
                for player_id, runtime in self.players.items()
            },
        }

    def _fire_and_forget(
        self, player_id: str, event_type: str, payload: dict[str, Any]
    ) -> None:
        asyncio.create_task(
            self.logger.log(self.session_id, player_id, event_type, payload)
        )

    def is_inactive(self, now: float, ttl_seconds: int) -> bool:
        if self.players:
            return False
        return now - self.last_activity > ttl_seconds


class SessionRegistry:
    def __init__(self, settings: Settings, logger: EventLogger) -> None:
        self.settings = settings
        self.logger = logger
        self.sessions: dict[str, GameSessionRuntime] = {}
        self.lock = asyncio.Lock()
        self.cleanup_task: asyncio.Task | None = None

    async def get_or_create(self, session_id: str) -> GameSessionRuntime:
        async with self.lock:
            if session_id not in self.sessions:
                self.sessions[session_id] = GameSessionRuntime(
                    session_id, self.settings, self.logger
                )
            return self.sessions[session_id]

    def start(self) -> None:
        if not self.cleanup_task:
            self.cleanup_task = asyncio.create_task(self._cleanup_loop())

    async def stop(self) -> None:
        if self.cleanup_task:
            self.cleanup_task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await self.cleanup_task

    async def _cleanup_loop(self) -> None:
        while True:
            await asyncio.sleep(self.settings.state_ttl_seconds)
            now = time.monotonic()
            async with self.lock:
                stale_sessions = [
                    session_id
                    for session_id, session in self.sessions.items()
                    if session.is_inactive(now, self.settings.state_ttl_seconds)
                ]
                for session_id in stale_sessions:
                    self.sessions.pop(session_id, None)
