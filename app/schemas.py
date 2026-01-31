from __future__ import annotations

from pydantic import BaseModel, Field


class AuthRequest(BaseModel):
    player_id: str = Field(min_length=1)


class AuthResponse(BaseModel):
    player_id: str
    token: str


class JoinMatchRequest(BaseModel):
    player_id: str = Field(min_length=1)
    region: str = Field(default="global", min_length=1)
    skill: int = Field(default=0, ge=0)


class MatchTicketResponse(BaseModel):
    ticket_id: str
    status: str
    session_id: str | None = None


class MatchStatusResponse(BaseModel):
    ticket_id: str
    status: str
    session_id: str | None = None


class CancelTicketResponse(BaseModel):
    ticket_id: str
    status: str


class SessionInfoResponse(BaseModel):
    session_id: str
    region: str
    status: str
    created_at: str
