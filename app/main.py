from __future__ import annotations

import asyncio
import json
from datetime import datetime
from typing import Optional

from fastapi import Depends, FastAPI, Header, HTTPException, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import create_token, decode_token, extract_bearer, get_current_user, hash_password, verify_password
from app.config import Settings, get_settings
from app.connection_manager import ConnectionManager
from app.db import build_engine, build_sessionmaker, get_session, init_db
from app.models import Channel, ChannelMember, Message, User
from app.presence import PresenceBroadcaster
from app.queue import DeliveryWorker, assign_outbox_to_instance, create_message_with_outbox, update_presence
from app.schemas import ChannelCreate, ChannelResponse, MessageResponse, TokenResponse, UserCreate, UserLogin, UserResponse


def create_app(settings: Optional[Settings] = None) -> FastAPI:
    settings = settings or get_settings()
    app = FastAPI(title="Realtime Chat Platform")

    engine = build_engine(settings.database_url)
    sessionmaker = build_sessionmaker(engine)
    manager = ConnectionManager()
    delivery_worker = DeliveryWorker(sessionmaker, manager, settings)
    presence_broadcaster = PresenceBroadcaster(sessionmaker, manager, settings)

    app.state.settings = settings
    app.state.engine = engine
    app.state.sessionmaker = sessionmaker
    app.state.manager = manager
    app.state.delivery_worker = delivery_worker
    app.state.presence_broadcaster = presence_broadcaster
    app.state.worker_task = None
    app.state.presence_task = None

    @app.on_event("startup")
    async def startup() -> None:
        await init_db(engine)
        if settings.enable_background_workers:
            app.state.worker_task = asyncio.create_task(delivery_worker.run())
        if settings.enable_presence_broadcast:
            app.state.presence_task = asyncio.create_task(presence_broadcaster.run())

    @app.on_event("shutdown")
    async def shutdown() -> None:
        await delivery_worker.stop()
        await presence_broadcaster.stop()
        tasks = [app.state.worker_task, app.state.presence_task]
        for task in tasks:
            if task:
                task.cancel()
                try:
                    await task
                except asyncio.CancelledError:
                    pass
        await engine.dispose()

    async def current_user_dep(
        request: Request,
        session: AsyncSession = Depends(get_session),
        authorization: Optional[str] = Header(default=None),
    ) -> User:
        return await get_current_user(
            session=session,
            settings=request.app.state.settings,
            authorization=authorization,
        )

    @app.post("/auth/register", response_model=TokenResponse)
    async def register(
        payload: UserCreate,
        request: Request,
        session: AsyncSession = Depends(get_session),
    ) -> TokenResponse:
        existing = await session.execute(select(User).where(User.username == payload.username))
        if existing.scalar_one_or_none():
            raise HTTPException(status_code=409, detail="Username already exists")
        user = User(username=payload.username, password_hash=hash_password(payload.password))
        session.add(user)
        try:
            await session.commit()
        except IntegrityError as exc:
            await session.rollback()
            raise HTTPException(status_code=409, detail="Username already exists") from exc
        token = create_token(user, request.app.state.settings)
        return TokenResponse(access_token=token)

    @app.post("/auth/login", response_model=TokenResponse)
    async def login(
        payload: UserLogin,
        request: Request,
        session: AsyncSession = Depends(get_session),
    ) -> TokenResponse:
        result = await session.execute(select(User).where(User.username == payload.username))
        user = result.scalar_one_or_none()
        if not user or not verify_password(payload.password, user.password_hash):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        token = create_token(user, request.app.state.settings)
        return TokenResponse(access_token=token)

    @app.get("/me", response_model=UserResponse)
    async def me(current_user: User = Depends(current_user_dep)) -> UserResponse:
        return UserResponse(id=current_user.id, username=current_user.username)

    @app.post("/channels", response_model=ChannelResponse)
    async def create_channel(
        payload: ChannelCreate,
        current_user: User = Depends(current_user_dep),
        session: AsyncSession = Depends(get_session),
    ) -> ChannelResponse:
        channel = Channel(name=payload.name)
        session.add(channel)
        try:
            await session.flush()
            session.add(ChannelMember(channel_id=channel.id, user_id=current_user.id))
            await session.commit()
        except IntegrityError as exc:
            await session.rollback()
            raise HTTPException(status_code=409, detail="Channel already exists") from exc
        return ChannelResponse(id=channel.id, name=channel.name)

    @app.get("/channels", response_model=list[ChannelResponse])
    async def list_channels(
        current_user: User = Depends(current_user_dep),
        session: AsyncSession = Depends(get_session),
    ) -> list[ChannelResponse]:
        result = await session.execute(
            select(Channel)
            .join(ChannelMember, ChannelMember.channel_id == Channel.id)
            .where(ChannelMember.user_id == current_user.id)
            .order_by(Channel.name)
        )
        return [ChannelResponse(id=channel.id, name=channel.name) for channel in result.scalars().all()]

    @app.post("/channels/{channel_id}/join")
    async def join_channel(
        channel_id: str,
        current_user: User = Depends(current_user_dep),
        session: AsyncSession = Depends(get_session),
    ) -> JSONResponse:
        channel = await session.get(Channel, channel_id)
        if not channel:
            raise HTTPException(status_code=404, detail="Channel not found")
        existing = await session.execute(
            select(ChannelMember).where(
                ChannelMember.channel_id == channel_id,
                ChannelMember.user_id == current_user.id,
            )
        )
        if not existing.scalar_one_or_none():
            session.add(ChannelMember(channel_id=channel_id, user_id=current_user.id))
            await session.commit()
        return JSONResponse({"status": "joined"})

    @app.get("/channels/{channel_id}/messages", response_model=list[MessageResponse])
    async def list_messages(
        channel_id: str,
        current_user: User = Depends(current_user_dep),
        session: AsyncSession = Depends(get_session),
        limit: int = 50,
        before: Optional[str] = None,
    ) -> list[MessageResponse]:
        membership = await session.execute(
            select(ChannelMember).where(
                ChannelMember.channel_id == channel_id,
                ChannelMember.user_id == current_user.id,
            )
        )
        if not membership.scalar_one_or_none():
            raise HTTPException(status_code=403, detail="Not a channel member")
        limit = min(max(limit, 1), 200)
        query = select(Message).where(Message.channel_id == channel_id)
        if before:
            try:
                before_dt = datetime.fromisoformat(before)
                query = query.where(Message.created_at < before_dt)
            except ValueError as exc:
                raise HTTPException(status_code=400, detail="Invalid 'before' timestamp") from exc
        query = query.order_by(Message.created_at.desc()).limit(limit)
        result = await session.execute(query)
        return [
            MessageResponse(
                id=message.id,
                channel_id=message.channel_id,
                sender_id=message.sender_id,
                content=message.content,
                created_at=message.created_at,
            )
            for message in result.scalars().all()
        ]

    async def _authenticate_ws(websocket: WebSocket) -> User:
        token = websocket.query_params.get("token")
        if not token:
            auth_header = websocket.headers.get("authorization")
            if auth_header:
                token = extract_bearer(auth_header)
        if not token:
            raise HTTPException(status_code=401, detail="Missing token")
        payload = decode_token(token, settings)
        user_id = payload.get("sub")
        async with sessionmaker() as session:
            user = await session.get(User, user_id)
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        return user

    async def _send_ws_error(websocket: WebSocket, message: str) -> None:
        await websocket.send_json({"type": "error", "message": message})

    @app.websocket("/ws")
    async def websocket_endpoint(websocket: WebSocket) -> None:
        try:
            user = await _authenticate_ws(websocket)
        except HTTPException:
            await websocket.close(code=1008)
            return

        await manager.connect(user.id, websocket)
        async with sessionmaker() as session:
            await update_presence(session, user.id, "online", settings.instance_id)
            await assign_outbox_to_instance(session, user.id, settings.instance_id)
        await manager.broadcast(
            {
                "type": "presence",
                "user_id": user.id,
                "status": "online",
                "instance_id": settings.instance_id,
                "last_seen": datetime.utcnow().isoformat(),
            }
        )

        try:
            while True:
                raw = await websocket.receive_text()
                try:
                    payload = json.loads(raw)
                except json.JSONDecodeError:
                    await _send_ws_error(websocket, "Invalid JSON")
                    continue

                msg_type = payload.get("type")
                if msg_type == "ping":
                    await websocket.send_json({"type": "pong"})
                    continue
                if msg_type != "message":
                    await _send_ws_error(websocket, "Unsupported message type")
                    continue

                channel_id = payload.get("channel_id")
                content = payload.get("content")
                if not channel_id or not isinstance(content, str) or not content.strip():
                    await _send_ws_error(websocket, "Invalid message payload")
                    continue

                async with sessionmaker() as session:
                    membership = await session.execute(
                        select(ChannelMember).where(
                            ChannelMember.channel_id == channel_id,
                            ChannelMember.user_id == user.id,
                        )
                    )
                    if not membership.scalar_one_or_none():
                        await _send_ws_error(websocket, "Not a channel member")
                        continue
                    message = await create_message_with_outbox(
                        session=session,
                        channel_id=channel_id,
                        sender_id=user.id,
                        content=content,
                    )

                await websocket.send_json({"type": "ack", "message_id": message.id})
        except WebSocketDisconnect:
            pass
        finally:
            await manager.disconnect(user.id, websocket)
            async with sessionmaker() as session:
                await update_presence(session, user.id, "offline", None)
            await manager.broadcast(
                {
                    "type": "presence",
                    "user_id": user.id,
                    "status": "offline",
                    "instance_id": None,
                    "last_seen": datetime.utcnow().isoformat(),
                }
            )

    return app


app = create_app()
