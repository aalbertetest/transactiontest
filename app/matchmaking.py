from __future__ import annotations

import asyncio
from collections import defaultdict, deque
from uuid import uuid4

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from .models import GameSession, MatchmakingTicket, Player


class QueueBackend:
    async def enqueue(self, region: str, ticket_id: str) -> None:
        raise NotImplementedError

    async def pop_batch(self, region: str, count: int) -> list[str]:
        raise NotImplementedError

    async def remove(self, region: str, ticket_id: str) -> None:
        raise NotImplementedError

    async def close(self) -> None:
        return None


class InMemoryQueueBackend(QueueBackend):
    def __init__(self) -> None:
        self.queues: dict[str, deque[str]] = defaultdict(deque)
        self.lock = asyncio.Lock()

    async def enqueue(self, region: str, ticket_id: str) -> None:
        async with self.lock:
            self.queues[region].append(ticket_id)

    async def pop_batch(self, region: str, count: int) -> list[str]:
        async with self.lock:
            queue = self.queues[region]
            if len(queue) < count:
                return []
            return [queue.popleft() for _ in range(count)]

    async def remove(self, region: str, ticket_id: str) -> None:
        async with self.lock:
            queue = self.queues.get(region)
            if not queue:
                return
            try:
                queue.remove(ticket_id)
            except ValueError:
                return


class RedisQueueBackend(QueueBackend):
    POP_SCRIPT = """
    local key = KEYS[1]
    local n = tonumber(ARGV[1])
    local len = redis.call('llen', key)
    if len < n then
        return {}
    end
    local result = redis.call('lrange', key, 0, n - 1)
    redis.call('ltrim', key, n, -1)
    return result
    """

    def __init__(self, redis_url: str) -> None:
        import redis.asyncio as redis

        self.redis = redis.from_url(redis_url, decode_responses=True)

    async def enqueue(self, region: str, ticket_id: str) -> None:
        await self.redis.rpush(self._key(region), ticket_id)

    async def pop_batch(self, region: str, count: int) -> list[str]:
        result = await self.redis.eval(self.POP_SCRIPT, 1, self._key(region), count)
        return list(result or [])

    async def remove(self, region: str, ticket_id: str) -> None:
        await self.redis.lrem(self._key(region), 0, ticket_id)

    async def close(self) -> None:
        await self.redis.close()

    @staticmethod
    def _key(region: str) -> str:
        return f"matchmaking:{region}"


class Matchmaker:
    def __init__(self, queue: QueueBackend, match_size: int) -> None:
        self.queue = queue
        self.match_size = match_size
        self.lock = asyncio.Lock()

    async def join(
        self, db: AsyncSession, player_id: str, region: str, skill: int
    ) -> MatchmakingTicket:
        async with self.lock:
            await self._ensure_player(db, player_id)
            ticket = MatchmakingTicket(
                id=str(uuid4()),
                player_id=player_id,
                region=region,
                skill=skill,
                status="queued",
            )
            db.add(ticket)
            await db.flush()

            await self.queue.enqueue(region, ticket.id)

            match_ids: list[str] = []
            session_id: str | None = None
            match_ids = await self.queue.pop_batch(region, self.match_size)
            if match_ids:
                session_id = str(uuid4())
                session = GameSession(id=session_id, region=region, status="active")
                db.add(session)
                await db.execute(
                    update(MatchmakingTicket)
                    .where(MatchmakingTicket.id.in_(match_ids))
                    .values(status="matched", session_id=session_id)
                )
            await db.commit()

            if ticket.id in match_ids:
                ticket.status = "matched"
                ticket.session_id = session_id

            return ticket

    async def status(
        self, db: AsyncSession, ticket_id: str, player_id: str
    ) -> MatchmakingTicket | None:
        result = await db.execute(
            select(MatchmakingTicket).where(
                MatchmakingTicket.id == ticket_id,
                MatchmakingTicket.player_id == player_id,
            )
        )
        return result.scalar_one_or_none()

    async def cancel(
        self, db: AsyncSession, ticket_id: str, player_id: str
    ) -> MatchmakingTicket | None:
        result = await db.execute(
            select(MatchmakingTicket).where(
                MatchmakingTicket.id == ticket_id,
                MatchmakingTicket.player_id == player_id,
            )
        )
        ticket = result.scalar_one_or_none()
        if not ticket:
            return None
        if ticket.status == "queued":
            await self.queue.remove(ticket.region, ticket.id)
            ticket.status = "cancelled"
        await db.commit()
        return ticket

    async def close(self) -> None:
        await self.queue.close()

    async def _ensure_player(self, db: AsyncSession, player_id: str) -> None:
        result = await db.execute(select(Player).where(Player.id == player_id))
        if result.scalar_one_or_none():
            return
        db.add(Player(id=player_id))
        await db.flush()
