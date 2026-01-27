# =============================================================================
# NEXUS PLATFORM - AUTHENTICATION SERVICE - SESSIONS API
# =============================================================================
# Session management endpoints.
# =============================================================================

"""
Sessions API Routes

Provides endpoints for:
- List active sessions
- View session details
- Revoke sessions
- Revoke all other sessions
"""

from datetime import datetime, timezone
from typing import List, Optional
import uuid

from fastapi import APIRouter, Depends, HTTPException, status, Request
from pydantic import BaseModel
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
import structlog

from ..config import settings
from ..core.database import get_db
from ..core.security import decode_token
from ..core.redis import add_to_blacklist
from ..models.user import User
from ..models.session import Session

logger = structlog.get_logger(__name__)
router = APIRouter()


# =============================================================================
# SCHEMAS
# =============================================================================

class SessionResponse(BaseModel):
    """Session response."""
    id: str
    device_type: Optional[str] = None
    device_name: Optional[str] = None
    browser: Optional[str] = None
    os: Optional[str] = None
    ip_address: Optional[str] = None
    location: Optional[str] = None
    country: Optional[str] = None
    is_current: bool = False
    created_at: datetime
    last_active_at: datetime
    expires_at: datetime


class SessionListResponse(BaseModel):
    """Session list response."""
    sessions: List[SessionResponse]
    current_session_id: Optional[str] = None
    total: int


class RevokeSessionRequest(BaseModel):
    """Revoke session request."""
    reason: Optional[str] = None


class RevokeAllSessionsRequest(BaseModel):
    """Revoke all sessions request."""
    exclude_current: bool = True
    reason: Optional[str] = None


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

async def get_current_user_and_session(
    request: Request,
    db: AsyncSession = Depends(get_db),
) -> tuple[User, Optional[str]]:
    """Get the current authenticated user and their session ID."""
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"code": "UNAUTHORIZED", "message": "Authentication required"},
        )
    
    token = auth_header.split(" ")[1]
    
    try:
        payload = decode_token(token, verify_type="access")
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"code": "INVALID_TOKEN", "message": "Invalid or expired token"},
        )
    
    user_id = payload.get("sub")
    session_id = payload.get("session_id")
    
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"code": "INVALID_TOKEN", "message": "Invalid token payload"},
        )
    
    result = await db.execute(
        select(User).where(User.id == uuid.UUID(user_id))
    )
    user = result.scalar_one_or_none()
    
    if not user or not user.is_active():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"code": "ACCOUNT_DISABLED", "message": "Account is disabled"},
        )
    
    return user, session_id


def session_to_response(session: Session, current_session_id: Optional[str] = None) -> SessionResponse:
    """Convert Session model to SessionResponse."""
    return SessionResponse(
        id=str(session.id),
        device_type=session.device_type,
        device_name=session.device_name,
        browser=session.browser,
        os=session.os,
        ip_address=session.ip_address,
        location=session.location,
        country=session.country,
        is_current=session.refresh_token_jti == current_session_id,
        created_at=session.created_at,
        last_active_at=session.last_active_at,
        expires_at=session.expires_at,
    )


# =============================================================================
# ENDPOINTS
# =============================================================================

@router.get("", response_model=SessionListResponse)
async def list_sessions(
    request: Request,
    db: AsyncSession = Depends(get_db),
) -> SessionListResponse:
    """
    List all active sessions for the current user.
    """
    user, current_session_id = await get_current_user_and_session(request, db)
    
    result = await db.execute(
        select(Session)
        .where(Session.user_id == user.id)
        .where(Session.is_active == True)
        .where(Session.revoked == False)
        .where(Session.expires_at > datetime.now(timezone.utc))
        .order_by(Session.last_active_at.desc())
    )
    sessions = result.scalars().all()
    
    return SessionListResponse(
        sessions=[session_to_response(s, current_session_id) for s in sessions],
        current_session_id=current_session_id,
        total=len(sessions),
    )


@router.get("/current", response_model=SessionResponse)
async def get_current_session(
    request: Request,
    db: AsyncSession = Depends(get_db),
) -> SessionResponse:
    """
    Get the current session details.
    """
    user, current_session_id = await get_current_user_and_session(request, db)
    
    if not current_session_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "NO_SESSION", "message": "No active session"},
        )
    
    result = await db.execute(
        select(Session).where(Session.refresh_token_jti == current_session_id)
    )
    session = result.scalar_one_or_none()
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "SESSION_NOT_FOUND", "message": "Session not found"},
        )
    
    return session_to_response(session, current_session_id)


@router.get("/{session_id}", response_model=SessionResponse)
async def get_session(
    session_id: str,
    request: Request,
    db: AsyncSession = Depends(get_db),
) -> SessionResponse:
    """
    Get a specific session by ID.
    """
    user, current_session_id = await get_current_user_and_session(request, db)
    
    try:
        sid = uuid.UUID(session_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"code": "INVALID_ID", "message": "Invalid session ID format"},
        )
    
    result = await db.execute(
        select(Session)
        .where(Session.id == sid)
        .where(Session.user_id == user.id)
    )
    session = result.scalar_one_or_none()
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "SESSION_NOT_FOUND", "message": "Session not found"},
        )
    
    return session_to_response(session, current_session_id)


@router.delete("/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
async def revoke_session(
    session_id: str,
    request: Request,
    revoke_request: Optional[RevokeSessionRequest] = None,
    db: AsyncSession = Depends(get_db),
):
    """
    Revoke a specific session.
    """
    user, current_session_id = await get_current_user_and_session(request, db)
    
    try:
        sid = uuid.UUID(session_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"code": "INVALID_ID", "message": "Invalid session ID format"},
        )
    
    result = await db.execute(
        select(Session)
        .where(Session.id == sid)
        .where(Session.user_id == user.id)
    )
    session = result.scalar_one_or_none()
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "SESSION_NOT_FOUND", "message": "Session not found"},
        )
    
    # Revoke session
    session.is_active = False
    session.revoked = True
    session.revoked_at = datetime.now(timezone.utc)
    session.revoked_reason = revoke_request.reason if revoke_request else "user_revoked"
    
    # Add to blacklist
    ttl = int((session.expires_at - datetime.now(timezone.utc)).total_seconds())
    if ttl > 0:
        await add_to_blacklist(session.refresh_token_jti, ttl)
    
    logger.info(
        "Session revoked",
        user_id=str(user.id),
        session_id=str(session.id),
        is_current=session.refresh_token_jti == current_session_id,
    )


@router.post("/revoke-all", status_code=status.HTTP_204_NO_CONTENT)
async def revoke_all_sessions(
    request: Request,
    revoke_request: Optional[RevokeAllSessionsRequest] = None,
    db: AsyncSession = Depends(get_db),
):
    """
    Revoke all sessions for the current user.
    
    Optionally excludes the current session.
    """
    user, current_session_id = await get_current_user_and_session(request, db)
    
    exclude_current = revoke_request.exclude_current if revoke_request else True
    reason = revoke_request.reason if revoke_request else "user_revoked_all"
    
    # Get all active sessions
    query = (
        select(Session)
        .where(Session.user_id == user.id)
        .where(Session.is_active == True)
        .where(Session.revoked == False)
    )
    
    if exclude_current and current_session_id:
        query = query.where(Session.refresh_token_jti != current_session_id)
    
    result = await db.execute(query)
    sessions = result.scalars().all()
    
    # Revoke all sessions
    for session in sessions:
        session.is_active = False
        session.revoked = True
        session.revoked_at = datetime.now(timezone.utc)
        session.revoked_reason = reason
        
        # Add to blacklist
        ttl = int((session.expires_at - datetime.now(timezone.utc)).total_seconds())
        if ttl > 0:
            await add_to_blacklist(session.refresh_token_jti, ttl)
    
    logger.info(
        "All sessions revoked",
        user_id=str(user.id),
        count=len(sessions),
        exclude_current=exclude_current,
    )


@router.post("/refresh-current", response_model=SessionResponse)
async def refresh_current_session(
    request: Request,
    db: AsyncSession = Depends(get_db),
) -> SessionResponse:
    """
    Refresh the current session's activity timestamp.
    """
    user, current_session_id = await get_current_user_and_session(request, db)
    
    if not current_session_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "NO_SESSION", "message": "No active session"},
        )
    
    result = await db.execute(
        select(Session).where(Session.refresh_token_jti == current_session_id)
    )
    session = result.scalar_one_or_none()
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "SESSION_NOT_FOUND", "message": "Session not found"},
        )
    
    # Update last active time
    session.last_active_at = datetime.now(timezone.utc)
    
    # Update IP and other info if available
    if request.client:
        session.ip_address = request.client.host
    
    return session_to_response(session, current_session_id)


# =============================================================================
# ADMIN ENDPOINTS
# =============================================================================

async def require_admin(request: Request, db: AsyncSession = Depends(get_db)) -> User:
    """Require admin role."""
    user, _ = await get_current_user_and_session(request, db)
    
    if "admin" not in user.roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"code": "FORBIDDEN", "message": "Admin access required"},
        )
    
    return user


@router.get("/admin/user/{user_id}", response_model=SessionListResponse)
async def admin_list_user_sessions(
    user_id: str,
    request: Request,
    admin: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
) -> SessionListResponse:
    """
    List all sessions for a specific user (admin only).
    """
    try:
        uid = uuid.UUID(user_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"code": "INVALID_ID", "message": "Invalid user ID format"},
        )
    
    result = await db.execute(
        select(Session)
        .where(Session.user_id == uid)
        .where(Session.is_active == True)
        .where(Session.revoked == False)
        .order_by(Session.last_active_at.desc())
    )
    sessions = result.scalars().all()
    
    return SessionListResponse(
        sessions=[session_to_response(s) for s in sessions],
        current_session_id=None,
        total=len(sessions),
    )


@router.delete("/admin/user/{user_id}/all", status_code=status.HTTP_204_NO_CONTENT)
async def admin_revoke_all_user_sessions(
    user_id: str,
    request: Request,
    admin: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    """
    Revoke all sessions for a specific user (admin only).
    """
    try:
        uid = uuid.UUID(user_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"code": "INVALID_ID", "message": "Invalid user ID format"},
        )
    
    result = await db.execute(
        select(Session)
        .where(Session.user_id == uid)
        .where(Session.is_active == True)
        .where(Session.revoked == False)
    )
    sessions = result.scalars().all()
    
    for session in sessions:
        session.is_active = False
        session.revoked = True
        session.revoked_at = datetime.now(timezone.utc)
        session.revoked_reason = f"admin_revoked:{admin.id}"
        
        ttl = int((session.expires_at - datetime.now(timezone.utc)).total_seconds())
        if ttl > 0:
            await add_to_blacklist(session.refresh_token_jti, ttl)
    
    logger.info(
        "Admin revoked all user sessions",
        admin_id=str(admin.id),
        target_user_id=user_id,
        count=len(sessions),
    )
