from __future__ import annotations

from datetime import datetime

from sqlalchemy import JSON, Column, DateTime, ForeignKey, Integer, String

from .db import Base


class Player(Base):
    __tablename__ = "players"

    id = Column(String, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class GameSession(Base):
    __tablename__ = "game_sessions"

    id = Column(String, primary_key=True)
    region = Column(String, nullable=False, index=True)
    status = Column(String, nullable=False, index=True, default="active")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class MatchmakingTicket(Base):
    __tablename__ = "matchmaking_tickets"

    id = Column(String, primary_key=True)
    player_id = Column(String, ForeignKey("players.id"), nullable=False, index=True)
    region = Column(String, nullable=False, index=True)
    skill = Column(Integer, default=0, nullable=False)
    status = Column(String, nullable=False, index=True, default="queued")
    session_id = Column(String, ForeignKey("game_sessions.id"), nullable=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )


class GameEvent(Base):
    __tablename__ = "game_events"

    id = Column(String, primary_key=True)
    session_id = Column(String, ForeignKey("game_sessions.id"), nullable=False, index=True)
    player_id = Column(String, ForeignKey("players.id"), nullable=False, index=True)
    event_type = Column(String, nullable=False, index=True)
    payload = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
