# =============================================================================
# NEXUS PLATFORM - AUTHENTICATION SERVICE - AUTH API
# =============================================================================
# Authentication endpoints for login, register, and token management.
# =============================================================================

"""
Authentication API Routes

Provides endpoints for:
- User registration
- User login (email/password)
- Token refresh
- Password reset
- Email verification
- Logout
"""

from datetime import datetime, timedelta, timezone
from typing import Optional
import uuid

from fastapi import APIRouter, Depends, HTTPException, status, Request, Response
from pydantic import BaseModel, EmailStr, Field, field_validator
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import structlog

from ..config import settings
from ..core.database import get_db
from ..core.security import (
    hash_password,
    verify_password,
    needs_rehash,
    create_token_pair,
    decode_token,
    generate_verification_token,
    generate_password_reset_token,
)
from ..core.redis import (
    increment_failed_attempts,
    get_failed_attempts,
    clear_failed_attempts,
    add_to_blacklist,
    is_blacklisted,
)
from ..models.user import User, UserStatus
from ..models.session import Session

logger = structlog.get_logger(__name__)
router = APIRouter()


# =============================================================================
# REQUEST/RESPONSE SCHEMAS
# =============================================================================

class RegisterRequest(BaseModel):
    """User registration request."""
    email: EmailStr
    password: str = Field(min_length=12)
    display_name: Optional[str] = Field(None, max_length=100)
    first_name: Optional[str] = Field(None, max_length=100)
    last_name: Optional[str] = Field(None, max_length=100)
    
    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        """Validate password meets requirements."""
        errors = []
        
        if len(v) < settings.password.min_length:
            errors.append(f"Password must be at least {settings.password.min_length} characters")
        if settings.password.require_uppercase and not any(c.isupper() for c in v):
            errors.append("Password must contain at least one uppercase letter")
        if settings.password.require_lowercase and not any(c.islower() for c in v):
            errors.append("Password must contain at least one lowercase letter")
        if settings.password.require_numbers and not any(c.isdigit() for c in v):
            errors.append("Password must contain at least one number")
        if settings.password.require_special and not any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in v):
            errors.append("Password must contain at least one special character")
        
        if errors:
            raise ValueError("; ".join(errors))
        
        return v


class RegisterResponse(BaseModel):
    """User registration response."""
    success: bool
    user_id: str
    email: str
    message: str
    email_verification_required: bool


class LoginRequest(BaseModel):
    """Login request."""
    email: EmailStr
    password: str
    remember_me: bool = False
    device_info: Optional[dict] = None


class LoginResponse(BaseModel):
    """Login response."""
    success: bool
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
    token_type: str = "Bearer"
    expires_in: int
    user: Optional[dict] = None
    mfa_required: bool = False
    mfa_challenge_id: Optional[str] = None


class RefreshTokenRequest(BaseModel):
    """Token refresh request."""
    refresh_token: str


class RefreshTokenResponse(BaseModel):
    """Token refresh response."""
    success: bool
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"
    expires_in: int


class PasswordResetRequest(BaseModel):
    """Password reset request."""
    email: EmailStr


class PasswordResetConfirm(BaseModel):
    """Password reset confirmation."""
    token: str
    new_password: str = Field(min_length=12)


class ChangePasswordRequest(BaseModel):
    """Change password request."""
    current_password: str
    new_password: str = Field(min_length=12)


# =============================================================================
# ENDPOINTS
# =============================================================================

@router.post("/register", response_model=RegisterResponse, status_code=status.HTTP_201_CREATED)
async def register(
    request: RegisterRequest,
    db: AsyncSession = Depends(get_db),
) -> RegisterResponse:
    """
    Register a new user account.
    
    Creates a new user with email/password credentials.
    Email verification is required before the account is activated.
    """
    logger.info("Registration attempt", email=request.email)
    
    # Check if email already exists
    result = await db.execute(
        select(User).where(User.email == request.email.lower())
    )
    existing_user = result.scalar_one_or_none()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "code": "EMAIL_EXISTS",
                "message": "An account with this email already exists",
            },
        )
    
    # Create user
    user = User(
        email=request.email.lower(),
        password_hash=hash_password(request.password),
        display_name=request.display_name,
        first_name=request.first_name,
        last_name=request.last_name,
        status=UserStatus.PENDING,
        roles=["user"],
        permissions=[],
    )
    
    db.add(user)
    await db.flush()
    
    # Generate verification token
    verification_token = generate_verification_token()
    # Store token in Redis with TTL (would send via email in production)
    
    logger.info(
        "User registered",
        user_id=str(user.id),
        email=user.email,
    )
    
    return RegisterResponse(
        success=True,
        user_id=str(user.id),
        email=user.email,
        message="Registration successful. Please verify your email.",
        email_verification_required=True,
    )


@router.post("/login", response_model=LoginResponse)
async def login(
    request: LoginRequest,
    http_request: Request,
    db: AsyncSession = Depends(get_db),
) -> LoginResponse:
    """
    Authenticate with email and password.
    
    Returns JWT tokens on successful authentication.
    May require MFA if enabled for the user.
    """
    email = request.email.lower()
    client_ip = http_request.client.host if http_request.client else "unknown"
    
    logger.info("Login attempt", email=email, ip=client_ip)
    
    # Check rate limiting
    failed_attempts = await get_failed_attempts(f"login:{email}")
    if failed_attempts >= 5:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail={
                "code": "TOO_MANY_ATTEMPTS",
                "message": "Too many failed login attempts. Please try again later.",
            },
        )
    
    # Find user
    result = await db.execute(
        select(User).where(User.email == email)
    )
    user = result.scalar_one_or_none()
    
    if not user or not verify_password(request.password, user.password_hash):
        await increment_failed_attempts(f"login:{email}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "code": "INVALID_CREDENTIALS",
                "message": "Invalid email or password",
            },
        )
    
    # Check user status
    if user.status == UserStatus.PENDING:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "code": "EMAIL_NOT_VERIFIED",
                "message": "Please verify your email before logging in",
            },
        )
    
    if user.status in (UserStatus.SUSPENDED, UserStatus.LOCKED, UserStatus.DELETED):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "code": "ACCOUNT_DISABLED",
                "message": "Your account has been disabled",
            },
        )
    
    if user.is_locked():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "code": "ACCOUNT_LOCKED",
                "message": "Your account is temporarily locked",
            },
        )
    
    # Check if MFA is required
    if user.mfa_enabled:
        # Create MFA challenge
        challenge_id = str(uuid.uuid4())
        # Store challenge in Redis
        
        return LoginResponse(
            success=True,
            expires_in=0,
            mfa_required=True,
            mfa_challenge_id=challenge_id,
        )
    
    # Clear failed attempts
    await clear_failed_attempts(f"login:{email}")
    
    # Check if password needs rehashing
    if needs_rehash(user.password_hash):
        user.password_hash = hash_password(request.password)
    
    # Create session
    session_id = str(uuid.uuid4())
    token_expiry = timedelta(days=7) if request.remember_me else timedelta(days=1)
    
    session = Session(
        user_id=user.id,
        refresh_token_jti=session_id,
        ip_address=client_ip,
        device_id=request.device_info.get("device_id") if request.device_info else None,
        device_type=request.device_info.get("device_type") if request.device_info else None,
        browser=request.device_info.get("browser") if request.device_info else None,
        os=request.device_info.get("os") if request.device_info else None,
        expires_at=datetime.now(timezone.utc) + token_expiry,
    )
    db.add(session)
    
    # Update last login
    user.last_login_at = datetime.now(timezone.utc)
    user.failed_login_attempts = 0
    
    # Generate tokens
    access_token, refresh_token = create_token_pair(
        user_id=str(user.id),
        session_id=session_id,
        email=user.email,
        roles=user.roles,
        permissions=user.permissions,
        tenant_id=str(user.tenant_id) if user.tenant_id else None,
    )
    
    logger.info(
        "Login successful",
        user_id=str(user.id),
        email=user.email,
        session_id=session_id,
    )
    
    return LoginResponse(
        success=True,
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="Bearer",
        expires_in=settings.jwt.access_token_expire_minutes * 60,
        user={
            "id": str(user.id),
            "email": user.email,
            "display_name": user.display_name,
            "roles": user.roles,
            "mfa_enabled": user.mfa_enabled,
        },
        mfa_required=False,
    )


@router.post("/refresh", response_model=RefreshTokenResponse)
async def refresh_token(
    request: RefreshTokenRequest,
    db: AsyncSession = Depends(get_db),
) -> RefreshTokenResponse:
    """
    Refresh an access token using a refresh token.
    """
    try:
        payload = decode_token(request.refresh_token, verify_type="refresh")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "code": "INVALID_TOKEN",
                "message": "Invalid or expired refresh token",
            },
        )
    
    # Check if token is blacklisted
    jti = payload.get("jti")
    if jti and await is_blacklisted(jti):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "code": "TOKEN_REVOKED",
                "message": "Token has been revoked",
            },
        )
    
    # Find session
    session_id = payload.get("session_id") or jti
    result = await db.execute(
        select(Session).where(Session.refresh_token_jti == session_id)
    )
    session = result.scalar_one_or_none()
    
    if not session or not session.is_valid():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "code": "SESSION_INVALID",
                "message": "Session is invalid or expired",
            },
        )
    
    # Get user
    result = await db.execute(
        select(User).where(User.id == session.user_id)
    )
    user = result.scalar_one_or_none()
    
    if not user or not user.is_active():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "code": "USER_INVALID",
                "message": "User account is not active",
            },
        )
    
    # Update session
    session.last_active_at = datetime.now(timezone.utc)
    
    # Generate new tokens
    access_token, new_refresh_token = create_token_pair(
        user_id=str(user.id),
        session_id=session_id,
        email=user.email,
        roles=user.roles,
        permissions=user.permissions,
        tenant_id=str(user.tenant_id) if user.tenant_id else None,
    )
    
    return RefreshTokenResponse(
        success=True,
        access_token=access_token,
        refresh_token=new_refresh_token,
        token_type="Bearer",
        expires_in=settings.jwt.access_token_expire_minutes * 60,
    )


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(
    http_request: Request,
    db: AsyncSession = Depends(get_db),
):
    """
    Logout and invalidate the current session.
    """
    auth_header = http_request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    
    token = auth_header.split(" ")[1]
    
    try:
        payload = decode_token(token)
        session_id = payload.get("session_id")
        jti = payload.get("jti")
        exp = payload.get("exp")
        
        # Add token to blacklist
        if jti and exp:
            ttl = exp - int(datetime.now(timezone.utc).timestamp())
            if ttl > 0:
                await add_to_blacklist(jti, ttl)
        
        # Revoke session
        if session_id:
            result = await db.execute(
                select(Session).where(Session.refresh_token_jti == session_id)
            )
            session = result.scalar_one_or_none()
            if session:
                session.revoked = True
                session.revoked_at = datetime.now(timezone.utc)
                session.revoked_reason = "user_logout"
        
        logger.info(
            "User logged out",
            user_id=payload.get("sub"),
            session_id=session_id,
        )
        
    except Exception:
        pass  # Ignore errors during logout
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/password-reset")
async def request_password_reset(
    request: PasswordResetRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    Request a password reset email.
    
    Always returns success to prevent email enumeration.
    """
    email = request.email.lower()
    
    # Find user (don't reveal if exists)
    result = await db.execute(
        select(User).where(User.email == email)
    )
    user = result.scalar_one_or_none()
    
    if user:
        # Generate reset token
        reset_token = generate_password_reset_token()
        # Store token and send email (not implemented here)
        
        logger.info(
            "Password reset requested",
            user_id=str(user.id),
            email=email,
        )
    
    # Always return success
    return {
        "success": True,
        "message": "If an account exists with this email, a password reset link has been sent.",
    }


@router.post("/verify-email")
async def verify_email(
    token: str,
    db: AsyncSession = Depends(get_db),
):
    """
    Verify email address with verification token.
    """
    # Verify token from Redis (not implemented here)
    # Update user status
    
    return {
        "success": True,
        "message": "Email verified successfully",
    }
