# =============================================================================
# NEXUS PLATFORM - AUTHENTICATION SERVICE - USERS API
# =============================================================================
# User profile management endpoints.
# =============================================================================

"""
Users API Routes

Provides endpoints for:
- Get current user profile
- Update user profile
- Change password
- Delete account
- Admin user management
"""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import uuid

from fastapi import APIRouter, Depends, HTTPException, status, Request
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
import structlog

from ..config import settings
from ..core.database import get_db
from ..core.security import (
    hash_password,
    verify_password,
    decode_token,
)
from ..models.user import User, UserStatus

logger = structlog.get_logger(__name__)
router = APIRouter()


# =============================================================================
# SCHEMAS
# =============================================================================

class UserProfile(BaseModel):
    """User profile response."""
    id: str
    email: str
    email_verified: bool
    username: Optional[str] = None
    display_name: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    phone_verified: bool = False
    avatar_url: Optional[str] = None
    status: str
    roles: List[str]
    mfa_enabled: bool
    created_at: datetime
    last_login_at: Optional[datetime] = None


class UpdateProfileRequest(BaseModel):
    """Update profile request."""
    display_name: Optional[str] = Field(None, max_length=100)
    first_name: Optional[str] = Field(None, max_length=100)
    last_name: Optional[str] = Field(None, max_length=100)
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    avatar_url: Optional[str] = Field(None, max_length=500)


class ChangePasswordRequest(BaseModel):
    """Change password request."""
    current_password: str
    new_password: str = Field(min_length=12)


class UpdateEmailRequest(BaseModel):
    """Update email request."""
    new_email: EmailStr
    password: str


class UserListResponse(BaseModel):
    """User list response."""
    users: List[UserProfile]
    total: int
    page: int
    page_size: int


class AdminUpdateUserRequest(BaseModel):
    """Admin user update request."""
    status: Optional[UserStatus] = None
    roles: Optional[List[str]] = None
    permissions: Optional[List[str]] = None
    mfa_enabled: Optional[bool] = None


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

async def get_current_user(
    request: Request,
    db: AsyncSession = Depends(get_db),
) -> User:
    """Get the current authenticated user from the request."""
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
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"code": "INVALID_TOKEN", "message": "Invalid token payload"},
        )
    
    result = await db.execute(
        select(User).where(User.id == uuid.UUID(user_id))
    )
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "USER_NOT_FOUND", "message": "User not found"},
        )
    
    if not user.is_active():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"code": "ACCOUNT_DISABLED", "message": "Account is disabled"},
        )
    
    return user


def user_to_profile(user: User) -> UserProfile:
    """Convert User model to UserProfile response."""
    return UserProfile(
        id=str(user.id),
        email=user.email,
        email_verified=user.email_verified,
        username=user.username,
        display_name=user.display_name,
        first_name=user.first_name,
        last_name=user.last_name,
        phone=user.phone,
        phone_verified=user.phone_verified,
        avatar_url=user.avatar_url,
        status=user.status.value,
        roles=user.roles,
        mfa_enabled=user.mfa_enabled,
        created_at=user.created_at,
        last_login_at=user.last_login_at,
    )


def require_role(role: str):
    """Dependency to require a specific role."""
    async def checker(user: User = Depends(get_current_user)) -> User:
        if role not in user.roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={"code": "FORBIDDEN", "message": f"Role '{role}' required"},
            )
        return user
    return checker


# =============================================================================
# ENDPOINTS
# =============================================================================

@router.get("/me", response_model=UserProfile)
async def get_current_user_profile(
    user: User = Depends(get_current_user),
) -> UserProfile:
    """
    Get the current authenticated user's profile.
    """
    return user_to_profile(user)


@router.patch("/me", response_model=UserProfile)
async def update_current_user_profile(
    request: UpdateProfileRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> UserProfile:
    """
    Update the current user's profile.
    """
    # Check username uniqueness if changed
    if request.username and request.username != user.username:
        result = await db.execute(
            select(User).where(User.username == request.username)
        )
        if result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={"code": "USERNAME_EXISTS", "message": "Username already taken"},
            )
    
    # Update fields
    update_data = request.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)
    
    user.updated_at = datetime.now(timezone.utc)
    
    logger.info(
        "User profile updated",
        user_id=str(user.id),
        updated_fields=list(update_data.keys()),
    )
    
    return user_to_profile(user)


@router.post("/me/change-password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(
    request: ChangePasswordRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Change the current user's password.
    """
    # Verify current password
    if not verify_password(request.current_password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"code": "INVALID_PASSWORD", "message": "Current password is incorrect"},
        )
    
    # Update password
    user.password_hash = hash_password(request.new_password)
    user.password_changed_at = datetime.now(timezone.utc)
    user.updated_at = datetime.now(timezone.utc)
    
    logger.info(
        "User password changed",
        user_id=str(user.id),
    )
    
    # TODO: Optionally revoke all other sessions


@router.post("/me/change-email")
async def change_email(
    request: UpdateEmailRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Request email change. Requires verification of new email.
    """
    # Verify password
    if not verify_password(request.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"code": "INVALID_PASSWORD", "message": "Password is incorrect"},
        )
    
    new_email = request.new_email.lower()
    
    # Check if new email is already in use
    result = await db.execute(
        select(User).where(User.email == new_email)
    )
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"code": "EMAIL_EXISTS", "message": "Email already in use"},
        )
    
    # Generate verification token and send email
    # In production, would store pending email change and require verification
    
    logger.info(
        "Email change requested",
        user_id=str(user.id),
        old_email=user.email,
        new_email=new_email,
    )
    
    return {
        "success": True,
        "message": "Verification email sent to new address",
    }


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_account(
    password: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Delete the current user's account (soft delete).
    """
    # Verify password
    if not verify_password(password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"code": "INVALID_PASSWORD", "message": "Password is incorrect"},
        )
    
    # Soft delete
    user.status = UserStatus.DELETED
    user.deleted_at = datetime.now(timezone.utc)
    user.updated_at = datetime.now(timezone.utc)
    
    logger.info(
        "User account deleted",
        user_id=str(user.id),
        email=user.email,
    )


# =============================================================================
# ADMIN ENDPOINTS
# =============================================================================

@router.get("", response_model=UserListResponse)
async def list_users(
    page: int = 1,
    page_size: int = 20,
    status_filter: Optional[UserStatus] = None,
    search: Optional[str] = None,
    admin: User = Depends(require_role("admin")),
    db: AsyncSession = Depends(get_db),
) -> UserListResponse:
    """
    List all users (admin only).
    """
    query = select(User)
    
    # Apply filters
    if status_filter:
        query = query.where(User.status == status_filter)
    
    if search:
        search_filter = f"%{search}%"
        query = query.where(
            (User.email.ilike(search_filter)) |
            (User.username.ilike(search_filter)) |
            (User.display_name.ilike(search_filter))
        )
    
    # Get total count
    count_query = select(func.count()).select_from(query.subquery())
    result = await db.execute(count_query)
    total = result.scalar()
    
    # Apply pagination
    offset = (page - 1) * page_size
    query = query.offset(offset).limit(page_size).order_by(User.created_at.desc())
    
    result = await db.execute(query)
    users = result.scalars().all()
    
    return UserListResponse(
        users=[user_to_profile(u) for u in users],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get("/{user_id}", response_model=UserProfile)
async def get_user(
    user_id: str,
    admin: User = Depends(require_role("admin")),
    db: AsyncSession = Depends(get_db),
) -> UserProfile:
    """
    Get a specific user by ID (admin only).
    """
    try:
        uid = uuid.UUID(user_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"code": "INVALID_ID", "message": "Invalid user ID format"},
        )
    
    result = await db.execute(
        select(User).where(User.id == uid)
    )
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "USER_NOT_FOUND", "message": "User not found"},
        )
    
    return user_to_profile(user)


@router.patch("/{user_id}", response_model=UserProfile)
async def update_user(
    user_id: str,
    request: AdminUpdateUserRequest,
    admin: User = Depends(require_role("admin")),
    db: AsyncSession = Depends(get_db),
) -> UserProfile:
    """
    Update a user's administrative fields (admin only).
    """
    try:
        uid = uuid.UUID(user_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"code": "INVALID_ID", "message": "Invalid user ID format"},
        )
    
    result = await db.execute(
        select(User).where(User.id == uid)
    )
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "USER_NOT_FOUND", "message": "User not found"},
        )
    
    # Update fields
    update_data = request.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)
    
    user.updated_at = datetime.now(timezone.utc)
    
    logger.info(
        "User updated by admin",
        user_id=str(user.id),
        admin_id=str(admin.id),
        updated_fields=list(update_data.keys()),
    )
    
    return user_to_profile(user)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: str,
    admin: User = Depends(require_role("admin")),
    db: AsyncSession = Depends(get_db),
):
    """
    Delete a user (admin only, soft delete).
    """
    try:
        uid = uuid.UUID(user_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"code": "INVALID_ID", "message": "Invalid user ID format"},
        )
    
    result = await db.execute(
        select(User).where(User.id == uid)
    )
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "USER_NOT_FOUND", "message": "User not found"},
        )
    
    # Prevent self-deletion
    if user.id == admin.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"code": "SELF_DELETE", "message": "Cannot delete your own account via admin API"},
        )
    
    # Soft delete
    user.status = UserStatus.DELETED
    user.deleted_at = datetime.now(timezone.utc)
    user.updated_at = datetime.now(timezone.utc)
    
    logger.info(
        "User deleted by admin",
        user_id=str(user.id),
        admin_id=str(admin.id),
    )
