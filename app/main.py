from __future__ import annotations

from typing import AsyncIterator

from fastapi import Depends, FastAPI, Header, HTTPException, Request, WebSocket
from fastapi.websockets import WebSocketDisconnect
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .config import Settings
from .db import Database
from .matchmaking import InMemoryQueueBackend, Matchmaker, RedisQueueBackend
from .models import GameSession, MatchmakingTicket
from .schemas import (
    AuthRequest,
    AuthResponse,
    CancelTicketResponse,
    JoinMatchRequest,
    MatchStatusResponse,
    MatchTicketResponse,
    SessionInfoResponse,
)
from .security import issue_token, verify_token
from .state import EventLogger, SessionRegistry


def create_app(settings: Settings) -> FastAPI:
    app = FastAPI(title="Multiplayer Game Backend", version="1.0.0")
    db = Database(settings.database_url)
    if settings.redis_url:
        queue_backend = RedisQueueBackend(settings.redis_url)
    else:
        queue_backend = InMemoryQueueBackend()
    matchmaker = Matchmaker(queue_backend, settings.matchmaking_size)
    event_logger = EventLogger(db)
    registry = SessionRegistry(settings, event_logger)

    app.state.settings = settings
    app.state.db = db
    app.state.matchmaker = matchmaker
    app.state.registry = registry
    app.state.event_logger = event_logger

    @app.on_event("startup")
    async def startup() -> None:
        await db.init()
        registry.start()

    @app.on_event("shutdown")
    async def shutdown() -> None:
        await registry.stop()
        await matchmaker.close()
        await db.close()

    async def get_db(request: Request) -> AsyncIterator[AsyncSession]:
        async for session in request.app.state.db.session():
            yield session

    async def require_player(
        request: Request,
        x_player_id: str = Header(..., alias="X-Player-Id"),
        x_player_token: str = Header(..., alias="X-Player-Token"),
    ) -> str:
        if not verify_token(
            x_player_id, x_player_token, request.app.state.settings.secret_key
        ):
            raise HTTPException(status_code=401, detail="Invalid token")
        return x_player_id

    @app.get("/health")
    async def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.post("/auth/issue", response_model=AuthResponse)
    async def issue_auth(payload: AuthRequest, request: Request) -> AuthResponse:
        token = issue_token(payload.player_id, request.app.state.settings.secret_key)
        return AuthResponse(player_id=payload.player_id, token=token)

    @app.post("/matchmaking/join", response_model=MatchTicketResponse)
    async def join_match(
        payload: JoinMatchRequest,
        request: Request,
        player_id: str = Depends(require_player),
        db_session: AsyncSession = Depends(get_db),
    ) -> MatchTicketResponse:
        if payload.player_id != player_id:
            raise HTTPException(status_code=403, detail="Player mismatch")
        matchmaker_local = request.app.state.matchmaker
        ticket = await matchmaker_local.join(
            db_session, player_id, payload.region, payload.skill
        )
        return MatchTicketResponse(
            ticket_id=ticket.id, status=ticket.status, session_id=ticket.session_id
        )

    @app.get("/matchmaking/status/{ticket_id}", response_model=MatchStatusResponse)
    async def match_status(
        ticket_id: str,
        request: Request,
        player_id: str = Depends(require_player),
        db_session: AsyncSession = Depends(get_db),
    ) -> MatchStatusResponse:
        matchmaker_local = request.app.state.matchmaker
        ticket = await matchmaker_local.status(db_session, ticket_id, player_id)
        if not ticket:
            raise HTTPException(status_code=404, detail="Ticket not found")
        return MatchStatusResponse(
            ticket_id=ticket.id, status=ticket.status, session_id=ticket.session_id
        )

    @app.post("/matchmaking/cancel/{ticket_id}", response_model=CancelTicketResponse)
    async def cancel_ticket(
        ticket_id: str,
        request: Request,
        player_id: str = Depends(require_player),
        db_session: AsyncSession = Depends(get_db),
    ) -> CancelTicketResponse:
        matchmaker_local = request.app.state.matchmaker
        ticket = await matchmaker_local.cancel(db_session, ticket_id, player_id)
        if not ticket:
            raise HTTPException(status_code=404, detail="Ticket not found")
        return CancelTicketResponse(ticket_id=ticket.id, status=ticket.status)

    @app.get("/sessions/{session_id}", response_model=SessionInfoResponse)
    async def get_session(
        session_id: str,
        _player_id: str = Depends(require_player),
        db_session: AsyncSession = Depends(get_db),
    ) -> SessionInfoResponse:
        session = await db_session.get(GameSession, session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        return SessionInfoResponse(
            session_id=session.id,
            region=session.region,
            status=session.status,
            created_at=session.created_at.isoformat(),
        )

    @app.websocket("/ws/game/{session_id}")
    async def game_socket(websocket: WebSocket, session_id: str) -> None:
        player_id = websocket.query_params.get("player_id")
        token = websocket.query_params.get("token")
        settings_local: Settings = websocket.app.state.settings

        if not player_id or not token:
            await websocket.close(code=4401)
            return
        if not verify_token(player_id, token, settings_local.secret_key):
            await websocket.close(code=4401)
            return

        async with websocket.app.state.db.sessionmaker() as db_session:
            session = await db_session.get(GameSession, session_id)
            if not session:
                await websocket.close(code=4404)
                return
            result = await db_session.execute(
                select(MatchmakingTicket).where(
                    MatchmakingTicket.session_id == session_id,
                    MatchmakingTicket.player_id == player_id,
                    MatchmakingTicket.status == "matched",
                )
            )
            if not result.scalar_one_or_none():
                await websocket.close(code=4403)
                return

        registry_local: SessionRegistry = websocket.app.state.registry
        runtime = await registry_local.get_or_create(session_id)
        await runtime.connect(player_id, websocket)

        try:
            while True:
                data = await websocket.receive_json()
                await runtime.handle_message(player_id, data)
        except WebSocketDisconnect:
            await runtime.disconnect(player_id)

    return app


app = create_app(Settings.from_env())
