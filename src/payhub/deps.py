"""FastAPI dependencies."""

from __future__ import annotations

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError
from sqlalchemy.orm import Session

from payhub.api_keys import verify_api_key
from payhub.auth import decode_token, parse_bearer
from payhub.db import get_db
from payhub.models import User, UserRole

security = HTTPBearer(auto_error=False)


def get_db_session(db: Session = Depends(get_db)) -> Session:
    return db


def _user_from_token(db: Session, token: str) -> User | None:
    try:
        payload = decode_token(token)
        sub = payload.get("sub")
        if not sub:
            return None
    except JWTError:
        return None
    return db.get(User, sub)


def get_current_user_optional(
    request: Request,
    db: Session = Depends(get_db),
    creds: HTTPAuthorizationCredentials | None = Depends(security),
) -> User | None:
    auth = request.headers.get("Authorization")
    bearer = parse_bearer(auth)
    if creds and creds.credentials:
        bearer = creds.credentials
    if bearer and bearer.startswith("pk_live_"):
        return verify_api_key(db, bearer)
    if bearer:
        return _user_from_token(db, bearer)
    return None


def require_user(user: User | None = Depends(get_current_user_optional)) -> User:
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="not_authenticated")
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="inactive_user")
    return user


def require_admin(user: User = Depends(require_user)) -> User:
    if user.role != UserRole.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="admin_only")
    return user
