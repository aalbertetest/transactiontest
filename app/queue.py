from __future__ import annotations

import asyncio
from datetime import datetime, timedelta

from sqlalchemy import and_, or_, select, update
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.config import Settings
from app.connection_manager import ConnectionManager, SendFailedError, UserOfflineError
from app.models import ChannelMember, Message, Outbox, Presence, User


def utcnow() -> datetime:
    return datetime.utcnow()


def backoff_delay(attempts: int, settings: Settings) -> timedelta:
    base = settings.base_retry_seconds * (2 ** max(0, attempts - 1))
    seconds = min(base, settings.max_retry_seconds)
    return timedelta(seconds=seconds)


async def create_message_with_outbox(
    session: AsyncSession,
    channel_id: str,
    sender_id: str,
    content: str,
) -> Message:
    members_result = await session.execute(
        select(ChannelMember.user_id).where(ChannelMember.channel_id == channel_id)
    )
    members = list({row[0] for row in members_result.all()})
    if sender_id not in members:
        members.append(sender_id)

    presence_result = await session.execute(
        select(Presence.user_id, Presence.status, Presence.instance_id).where(
            Presence.user_id.in_(members)
        )
    )
    presence_map = {
        row[0]: row[2] if row[1] == "online" else None for row in presence_result.all()
    }

    message = Message(channel_id=channel_id, sender_id=sender_id, content=content)
    session.add(message)
    await session.flush()

    now = utcnow()
    for recipient_id in members:
        outbox = Outbox(
            message_id=message.id,
            recipient_id=recipient_id,
            status="pending",
            attempts=0,
            next_attempt_at=now,
            target_instance_id=presence_map.get(recipient_id),
            updated_at=now,
        )
        session.add(outbox)

    await session.commit()
    return message


async def assign_outbox_to_instance(
    session: AsyncSession, user_id: str, instance_id: str
) -> None:
    now = utcnow()
    await session.execute(
        update(Outbox)
        .where(
            Outbox.recipient_id == user_id,
            Outbox.status.in_(["pending", "retry", "processing"]),
        )
        .values(
            status="pending",
            target_instance_id=instance_id,
            locked_until=None,
            next_attempt_at=now,
            updated_at=now,
        )
    )
    await session.commit()


async def update_presence(
    session: AsyncSession, user_id: str, status: str, instance_id: str | None
) -> None:
    now = utcnow()
    existing = await session.get(Presence, user_id)
    if existing:
        existing.status = status
        existing.instance_id = instance_id
        existing.last_seen = now
        existing.updated_at = now
    else:
        session.add(
            Presence(
                user_id=user_id,
                status=status,
                instance_id=instance_id,
                last_seen=now,
                updated_at=now,
            )
        )
    await session.commit()


async def build_message_payload(
    session: AsyncSession, message_id: str, recipient_id: str
) -> dict:
    message = await session.get(Message, message_id)
    sender = await session.get(User, message.sender_id)
    return {
        "type": "message",
        "message": {
            "id": message.id,
            "channel_id": message.channel_id,
            "sender_id": message.sender_id,
            "sender_username": sender.username if sender else "unknown",
            "recipient_id": recipient_id,
            "content": message.content,
            "created_at": message.created_at.isoformat(),
        },
    }


class DeliveryWorker:
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

    async def stop(self) -> None:
        self._stop.set()

    async def run(self) -> None:
        while not self._stop.is_set():
            processed = await self.process_once()
            if processed == 0:
                try:
                    await asyncio.wait_for(
                        self._stop.wait(), timeout=self._settings.delivery_poll_interval
                    )
                except asyncio.TimeoutError:
                    continue

    async def process_once(self) -> int:
        async with self._sessionmaker() as session:
            jobs = await self._claim_jobs(session)
        if not jobs:
            return 0

        processed = 0
        for job_id in jobs:
            processed += 1
            async with self._sessionmaker() as session:
                job = await session.get(Outbox, job_id)
                if not job:
                    continue
                await self._process_job(session, job)
        return processed

    async def _claim_jobs(self, session: AsyncSession) -> list[str]:
        now = utcnow()
        lease_until = now + timedelta(seconds=self._settings.lease_seconds)
        result = await session.execute(
            select(Outbox.id)
            .where(
                Outbox.target_instance_id == self._settings.instance_id,
                Outbox.next_attempt_at <= now,
                or_(
                    Outbox.status.in_(["pending", "retry"]),
                    and_(Outbox.status == "processing", Outbox.locked_until <= now),
                ),
            )
            .order_by(Outbox.next_attempt_at)
            .limit(self._settings.delivery_batch_size)
        )
        job_ids = [row[0] for row in result.all()]
        if not job_ids:
            return []
        await session.execute(
            update(Outbox)
            .where(Outbox.id.in_(job_ids))
            .values(status="processing", locked_until=lease_until, updated_at=now)
        )
        await session.commit()
        return job_ids

    async def _process_job(self, session: AsyncSession, job: Outbox) -> None:
        now = utcnow()
        if not await self._manager.has_user(job.recipient_id):
            job.status = "pending"
            job.target_instance_id = None
            job.next_attempt_at = now + timedelta(seconds=self._settings.offline_retry_seconds)
            job.locked_until = None
            job.updated_at = now
            await session.commit()
            return

        payload = await build_message_payload(session, job.message_id, job.recipient_id)
        try:
            await self._manager.send_to_user(job.recipient_id, payload)
        except UserOfflineError:
            job.status = "pending"
            job.target_instance_id = None
            job.next_attempt_at = now + timedelta(seconds=self._settings.offline_retry_seconds)
            job.locked_until = None
            job.updated_at = now
        except SendFailedError:
            job.status = "pending"
            job.target_instance_id = None
            job.next_attempt_at = now + timedelta(seconds=self._settings.offline_retry_seconds)
            job.locked_until = None
            job.updated_at = now
        except Exception as exc:  # noqa: BLE001 - best effort retries for transport errors
            await self._schedule_retry(job, now, exc)
        else:
            job.attempts += 1
            job.status = "delivered"
            job.delivered_at = now
            job.locked_until = None
            job.last_error = None
            job.updated_at = now
        await session.commit()

    async def _schedule_retry(self, job: Outbox, now: datetime, exc: Exception) -> None:
        job.attempts += 1
        if job.attempts >= self._settings.max_retries:
            job.status = "failed"
        else:
            job.status = "retry"
            job.next_attempt_at = now + backoff_delay(job.attempts, self._settings)
        job.locked_until = None
        job.last_error = str(exc)[:240]
        job.updated_at = now
