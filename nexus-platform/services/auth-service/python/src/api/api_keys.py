# =============================================================================
# NEXUS PLATFORM - AUTHENTICATION SERVICE - API KEYS API
# =============================================================================
# API key management endpoints.
# =============================================================================

"""
API Keys API Routes

Provides endpoints for:
- Create new API keys
- List API keys
- Get API key details
- Revoke API keys
- Verify API keys
"""

from datetime import datetime, timedelta, timezone
from typing import List, Optional
import uuid

from fastapi import APIRouter, Depends, HTTPException, status, Request
from pydantic import BaseModel, Field
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
import structlog

from ..config import settings
from ..core.database import get_db
from ..core.security import (
    decode_token,
    generate_api_key,
    hash_api_key,
    verify_api_key,
)
from ..models.user import User
from ..models.api_key import APIKey

logger = structlog.get_logger(__name__)
router = APIRouter()


# =============================================================================
# SCHEMAS
# =============================================================================

class CreateAPIKeyRequest(BaseModel):
    """Create API key request."""
    name: str = Field(min_length=1, max_length=100)
    scopes: List[str] = Field(default=["read"])
    allowed_ips: List[str] = Field(default=[])
    rate_limit: Optional[int] = Field(default=None, ge=1, le=10000)
    expires_in_days: Optional[int] = Field(default=None, ge=1, le=365)


class APIKeyResponse(BaseModel):
    """API key response (without full key)."""
    id: str
    name: str
    key_prefix: str
    scopes: List[str]
    allowed_ips: List[str]
    rate_limit: Optional[int] = None
    is_active: bool
    revoked: bool
    created_at: datetime
    expires_at: Optional[datetime] = None
    last_used_at: Optional[datetime] = None
    usage_count: int


class CreateAPIKeyResponse(BaseModel):
    """Create API key response (includes full key - shown only once)."""
    id: str
    name: str
    key: str  # Full key - shown only once
    key_prefix: str
    scopes: List[str]
    allowed_ips: List[str]
    rate_limit: Optional[int] = None
    created_at: datetime
    expires_at: Optional[datetime] = None


class APIKeyListResponse(BaseModel):
    """API key list response."""
    keys: List[APIKeyResponse]
    total: int


class UpdateAPIKeyRequest(BaseModel):
    """Update API key request."""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    scopes: Optional[List[str]] = None
    allowed_ips: Optional[List[str]] = None
    rate_limit: Optional[int] = Field(default=None, ge=1, le=10000)
    is_active: Optional[bool] = None


class VerifyAPIKeyRequest(BaseModel):
    """Verify API key request."""
    key: str


class VerifyAPIKeyResponse(BaseModel):
    """Verify API key response."""
    valid: bool
    user_id: Optional[str] = None
    scopes: Optional[List[str]] = None
    rate_limit: Optional[int] = None
    error: Optional[str] = None


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
    
    if not user or not user.is_active():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"code": "ACCOUNT_DISABLED", "message": "Account is disabled"},
        )
    
    return user


def key_to_response(key: APIKey) -> APIKeyResponse:
    """Convert APIKey model to APIKeyResponse."""
    return APIKeyResponse(
        id=str(key.id),
        name=key.name,
        key_prefix=key.key_prefix,
        scopes=key.scopes,
        allowed_ips=key.allowed_ips,
        rate_limit=key.rate_limit,
        is_active=key.is_active,
        revoked=key.revoked,
        created_at=key.created_at,
        expires_at=key.expires_at,
        last_used_at=key.last_used_at,
        usage_count=key.usage_count,
    )


# =============================================================================
# ENDPOINTS
# =============================================================================

@router.post("", response_model=CreateAPIKeyResponse, status_code=status.HTTP_201_CREATED)
async def create_api_key(
    request: CreateAPIKeyRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> CreateAPIKeyResponse:
    """
    Create a new API key.
    
    The full key is returned only once. Store it securely.
    """
    # Check for existing keys with same name
    result = await db.execute(
        select(APIKey)
        .where(APIKey.user_id == user.id)
        .where(APIKey.name == request.name)
        .where(APIKey.revoked == False)
    )
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"code": "NAME_EXISTS", "message": "API key with this name already exists"},
        )
    
    # Check key limit
    result = await db.execute(
        select(func.count())
        .select_from(APIKey)
        .where(APIKey.user_id == user.id)
        .where(APIKey.is_active == True)
        .where(APIKey.revoked == False)
    )
    key_count = result.scalar()
    
    if key_count >= 50:  # Max 50 active keys per user
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"code": "KEY_LIMIT", "message": "Maximum number of API keys reached"},
        )
    
    # Generate key
    full_key, key_hash = generate_api_key(prefix="nxp_")
    key_prefix = full_key[:12]  # Store prefix for identification
    
    # Calculate expiration
    expires_at = None
    if request.expires_in_days:
        expires_at = datetime.now(timezone.utc) + timedelta(days=request.expires_in_days)
    
    # Create key record
    api_key = APIKey(
        user_id=user.id,
        name=request.name,
        key_prefix=key_prefix,
        key_hash=key_hash,
        scopes=request.scopes,
        allowed_ips=request.allowed_ips,
        rate_limit=request.rate_limit,
        expires_at=expires_at,
    )
    
    db.add(api_key)
    await db.flush()
    
    logger.info(
        "API key created",
        user_id=str(user.id),
        key_id=str(api_key.id),
        name=request.name,
        scopes=request.scopes,
    )
    
    return CreateAPIKeyResponse(
        id=str(api_key.id),
        name=api_key.name,
        key=full_key,  # Full key - only shown once
        key_prefix=key_prefix,
        scopes=api_key.scopes,
        allowed_ips=api_key.allowed_ips,
        rate_limit=api_key.rate_limit,
        created_at=api_key.created_at,
        expires_at=api_key.expires_at,
    )


@router.get("", response_model=APIKeyListResponse)
async def list_api_keys(
    include_revoked: bool = False,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> APIKeyListResponse:
    """
    List all API keys for the current user.
    """
    query = select(APIKey).where(APIKey.user_id == user.id)
    
    if not include_revoked:
        query = query.where(APIKey.revoked == False)
    
    query = query.order_by(APIKey.created_at.desc())
    
    result = await db.execute(query)
    keys = result.scalars().all()
    
    return APIKeyListResponse(
        keys=[key_to_response(k) for k in keys],
        total=len(keys),
    )


@router.get("/{key_id}", response_model=APIKeyResponse)
async def get_api_key(
    key_id: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> APIKeyResponse:
    """
    Get details of a specific API key.
    """
    try:
        kid = uuid.UUID(key_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"code": "INVALID_ID", "message": "Invalid key ID format"},
        )
    
    result = await db.execute(
        select(APIKey)
        .where(APIKey.id == kid)
        .where(APIKey.user_id == user.id)
    )
    key = result.scalar_one_or_none()
    
    if not key:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "KEY_NOT_FOUND", "message": "API key not found"},
        )
    
    return key_to_response(key)


@router.patch("/{key_id}", response_model=APIKeyResponse)
async def update_api_key(
    key_id: str,
    request: UpdateAPIKeyRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> APIKeyResponse:
    """
    Update an API key's settings.
    """
    try:
        kid = uuid.UUID(key_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"code": "INVALID_ID", "message": "Invalid key ID format"},
        )
    
    result = await db.execute(
        select(APIKey)
        .where(APIKey.id == kid)
        .where(APIKey.user_id == user.id)
    )
    key = result.scalar_one_or_none()
    
    if not key:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "KEY_NOT_FOUND", "message": "API key not found"},
        )
    
    if key.revoked:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"code": "KEY_REVOKED", "message": "Cannot update revoked key"},
        )
    
    # Update fields
    update_data = request.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(key, field, value)
    
    logger.info(
        "API key updated",
        user_id=str(user.id),
        key_id=str(key.id),
        updated_fields=list(update_data.keys()),
    )
    
    return key_to_response(key)


@router.delete("/{key_id}", status_code=status.HTTP_204_NO_CONTENT)
async def revoke_api_key(
    key_id: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Revoke an API key.
    """
    try:
        kid = uuid.UUID(key_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"code": "INVALID_ID", "message": "Invalid key ID format"},
        )
    
    result = await db.execute(
        select(APIKey)
        .where(APIKey.id == kid)
        .where(APIKey.user_id == user.id)
    )
    key = result.scalar_one_or_none()
    
    if not key:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "KEY_NOT_FOUND", "message": "API key not found"},
        )
    
    key.is_active = False
    key.revoked = True
    key.revoked_at = datetime.now(timezone.utc)
    
    logger.info(
        "API key revoked",
        user_id=str(user.id),
        key_id=str(key.id),
        name=key.name,
    )


@router.post("/revoke-all", status_code=status.HTTP_204_NO_CONTENT)
async def revoke_all_api_keys(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Revoke all API keys for the current user.
    """
    result = await db.execute(
        select(APIKey)
        .where(APIKey.user_id == user.id)
        .where(APIKey.is_active == True)
        .where(APIKey.revoked == False)
    )
    keys = result.scalars().all()
    
    for key in keys:
        key.is_active = False
        key.revoked = True
        key.revoked_at = datetime.now(timezone.utc)
    
    logger.info(
        "All API keys revoked",
        user_id=str(user.id),
        count=len(keys),
    )


# =============================================================================
# INTERNAL VERIFICATION ENDPOINT
# =============================================================================

@router.post("/verify", response_model=VerifyAPIKeyResponse)
async def verify_api_key_endpoint(
    request: VerifyAPIKeyRequest,
    http_request: Request,
    db: AsyncSession = Depends(get_db),
) -> VerifyAPIKeyResponse:
    """
    Verify an API key (internal use by other services).
    
    Returns key metadata if valid.
    """
    # Extract prefix for lookup
    if not request.key.startswith("nxp_"):
        return VerifyAPIKeyResponse(valid=False, error="Invalid key format")
    
    key_prefix = request.key[:12]
    
    # Find key by prefix
    result = await db.execute(
        select(APIKey).where(APIKey.key_prefix == key_prefix)
    )
    key = result.scalar_one_or_none()
    
    if not key:
        return VerifyAPIKeyResponse(valid=False, error="Key not found")
    
    # Verify hash
    if not verify_api_key(request.key, key.key_hash):
        return VerifyAPIKeyResponse(valid=False, error="Invalid key")
    
    # Check if key is valid
    if not key.is_valid():
        if key.revoked:
            return VerifyAPIKeyResponse(valid=False, error="Key revoked")
        if not key.is_active:
            return VerifyAPIKeyResponse(valid=False, error="Key inactive")
        if key.expires_at and key.expires_at < datetime.now(timezone.utc):
            return VerifyAPIKeyResponse(valid=False, error="Key expired")
        return VerifyAPIKeyResponse(valid=False, error="Key invalid")
    
    # Check IP restrictions
    if key.allowed_ips:
        client_ip = http_request.client.host if http_request.client else None
        if client_ip and client_ip not in key.allowed_ips:
            return VerifyAPIKeyResponse(valid=False, error="IP not allowed")
    
    # Update usage stats
    key.last_used_at = datetime.now(timezone.utc)
    key.usage_count += 1
    
    return VerifyAPIKeyResponse(
        valid=True,
        user_id=str(key.user_id),
        scopes=key.scopes,
        rate_limit=key.rate_limit,
    )


# =============================================================================
# ADMIN ENDPOINTS
# =============================================================================

async def require_admin(request: Request, db: AsyncSession = Depends(get_db)) -> User:
    """Require admin role."""
    user = await get_current_user(request, db)
    
    if "admin" not in user.roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"code": "FORBIDDEN", "message": "Admin access required"},
        )
    
    return user


@router.get("/admin/user/{user_id}", response_model=APIKeyListResponse)
async def admin_list_user_api_keys(
    user_id: str,
    include_revoked: bool = False,
    admin: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
) -> APIKeyListResponse:
    """
    List all API keys for a specific user (admin only).
    """
    try:
        uid = uuid.UUID(user_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"code": "INVALID_ID", "message": "Invalid user ID format"},
        )
    
    query = select(APIKey).where(APIKey.user_id == uid)
    
    if not include_revoked:
        query = query.where(APIKey.revoked == False)
    
    query = query.order_by(APIKey.created_at.desc())
    
    result = await db.execute(query)
    keys = result.scalars().all()
    
    return APIKeyListResponse(
        keys=[key_to_response(k) for k in keys],
        total=len(keys),
    )


@router.delete("/admin/{key_id}", status_code=status.HTTP_204_NO_CONTENT)
async def admin_revoke_api_key(
    key_id: str,
    admin: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    """
    Revoke any API key (admin only).
    """
    try:
        kid = uuid.UUID(key_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"code": "INVALID_ID", "message": "Invalid key ID format"},
        )
    
    result = await db.execute(
        select(APIKey).where(APIKey.id == kid)
    )
    key = result.scalar_one_or_none()
    
    if not key:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "KEY_NOT_FOUND", "message": "API key not found"},
        )
    
    key.is_active = False
    key.revoked = True
    key.revoked_at = datetime.now(timezone.utc)
    
    logger.info(
        "API key revoked by admin",
        admin_id=str(admin.id),
        key_id=str(key.id),
        owner_id=str(key.user_id),
    )
