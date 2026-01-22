from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=80)
    password: str = Field(min_length=8, max_length=128)


class UserLogin(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    id: str
    username: str


class ChannelCreate(BaseModel):
    name: str = Field(min_length=1, max_length=80)


class ChannelResponse(BaseModel):
    id: str
    name: str


class MessageCreate(BaseModel):
    channel_id: str
    content: str = Field(min_length=1, max_length=4000)


class MessageResponse(BaseModel):
    id: str
    channel_id: str
    sender_id: str
    content: str
    created_at: datetime


class PresenceEvent(BaseModel):
    user_id: str
    status: str
    last_seen: datetime
    instance_id: str | None = None
