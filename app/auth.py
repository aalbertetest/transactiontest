from __future__ import annotations

import base64
import hashlib
import hmac
import os
from datetime import datetime, timedelta
from typing import Optional

import jwt
from fastapi import Header, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import Settings
from app.models import User


def hash_password(password: str) -> str:
    salt = os.urandom(16)
    derived = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 100_000)
    return base64.b64encode(salt + derived).decode()


def verify_password(password: str, stored_hash: str) -> bool:
    raw = base64.b64decode(stored_hash.encode())
    salt = raw[:16]
    expected = raw[16:]
    derived = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 100_000)
    return hmac.compare_digest(expected, derived)


def create_token(user: User, settings: Settings) -> str:
    now = datetime.utcnow()
    payload = {
        "sub": user.id,
        "username": user.username,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(seconds=settings.access_token_ttl_seconds)).timestamp()),
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def decode_token(token: str, settings: Settings) -> dict:
    try:
        return jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
    except jwt.PyJWTError as exc:
        raise HTTPException(status_code=401, detail="Invalid token") from exc


def extract_bearer(authorization: Optional[str]) -> str:
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing authorization")
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    return parts[1]


async def get_current_user(
    session: AsyncSession,
    settings: Settings,
    authorization: Optional[str] = Header(default=None),
) -> User:
    token = extract_bearer(authorization)
    payload = decode_token(token, settings)
    user_id = payload.get("sub")
    result = await session.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user
