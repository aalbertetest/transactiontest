from __future__ import annotations

import asyncio

import pytest
from sqlalchemy import select

from app.config import Settings
from app.db import init_db
from app.main import create_app
from app.models import Channel, ChannelMember, Message, Outbox, User
from app.queue import DeliveryWorker, update_presence


class FlakyManager:
    def __init__(self) -> None:
        self.calls = 0
        self.payloads = []

    async def has_user(self, user_id: str) -> bool:
        return True

    async def send_to_user(self, user_id: str, payload: dict) -> None:
        self.calls += 1
        if self.calls == 1:
            raise RuntimeError("simulated failure")
        self.payloads.append(payload)


@pytest.mark.asyncio
async def test_retry_logic(tmp_path):
    settings = Settings(
        database_url=f"sqlite+aiosqlite:///{tmp_path/'retry.db'}",
        jwt_secret="test-secret",
        instance_id="retry-instance",
        delivery_poll_interval=0.01,
        presence_broadcast_interval=0.1,
        delivery_batch_size=5,
        max_retries=3,
        base_retry_seconds=0.0,
        max_retry_seconds=0.0,
        lease_seconds=1.0,
        offline_retry_seconds=0.01,
        enable_background_workers=False,
        enable_presence_broadcast=False,
    )

    app = create_app(settings)
    await init_db(app.state.engine)

    async with app.state.sessionmaker() as session:
        alice = User(username="alice", password_hash="x")
        bob = User(username="bob", password_hash="y")
        channel = Channel(name="general")
        session.add_all([alice, bob, channel])
        await session.flush()
        session.add(ChannelMember(channel_id=channel.id, user_id=alice.id))
        session.add(ChannelMember(channel_id=channel.id, user_id=bob.id))
        await session.commit()

    async with app.state.sessionmaker() as session:
        await update_presence(session, bob.id, "online", settings.instance_id)

    async with app.state.sessionmaker() as session:
        message = Message(channel_id=channel.id, sender_id=alice.id, content="retry")
        session.add(message)
        await session.flush()
        outbox = Outbox(
            message_id=message.id,
            recipient_id=bob.id,
            status="pending",
            target_instance_id=settings.instance_id,
        )
        session.add(outbox)
        await session.commit()

    manager = FlakyManager()
    worker = DeliveryWorker(app.state.sessionmaker, manager, settings)

    processed = await worker.process_once()
    assert processed == 1

    async with app.state.sessionmaker() as session:
        job = (await session.execute(select(Outbox))).scalars().one()
        assert job.status == "retry"
        assert job.attempts == 1

    await asyncio.sleep(0.02)
    processed = await worker.process_once()
    assert processed == 1

    async with app.state.sessionmaker() as session:
        job = (await session.execute(select(Outbox))).scalars().one()
        assert job.status == "delivered"
        assert job.attempts == 2

    await app.state.engine.dispose()
