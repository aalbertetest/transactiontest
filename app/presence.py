from __future__ import annotations

import asyncio
from datetime import datetime, timedelta

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.config import Settings
from app.connection_manager import ConnectionManager
from app.models import Presence


def utcnow() -> datetime:
    return datetime.utcnow()


class PresenceBroadcaster:
    def __init__(
        self,
        sessionmaker: async_sessionmaker[AsyncSession],
        manager: ConnectionManager,
        settings: Settings,
    ) -> None:
        self._sessionmaker = sessionmaker
        self._manager = manager
        self._settings = settings
        self._stop = asyncio.Event()
        self._last_sync = utcnow() - timedelta(seconds=5)

    async def stop(self) -> None:
        self._stop.set()

    async def run(self) -> None:
        while not self._stop.is_set():
            await self._broadcast_updates()
            try:
                await asyncio.wait_for(
                    self._stop.wait(), timeout=self._settings.presence_broadcast_interval
                )
            except asyncio.TimeoutError:
                continue

    async def _broadcast_updates(self) -> None:
        async with self._sessionmaker() as session:
            updates = await self._fetch_updates(session)
        for presence in updates:
            await self._manager.broadcast(
                {
                    "type": "presence",
                    "user_id": presence.user_id,
                    "status": presence.status,
                    "instance_id": presence.instance_id,
                    "last_seen": presence.last_seen.isoformat(),
                }
            )

    async def _fetch_updates(self, session: AsyncSession) -> list[Presence]:
        result = await session.execute(
            select(Presence).where(Presence.updated_at > self._last_sync)
        )
        rows = result.scalars().all()
        if rows:
            self._last_sync = max(row.updated_at for row in rows)
        return rows
