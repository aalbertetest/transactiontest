# =============================================================================
# NEXUS PLATFORM - AUTHENTICATION SERVICE - MFA API
# =============================================================================
# Multi-factor authentication endpoints.
# =============================================================================

"""
MFA API Routes

Provides endpoints for:
- TOTP (authenticator app) setup and verification
- SMS MFA setup and verification
- Email MFA setup and verification
- WebAuthn/FIDO2 setup and verification
- Backup codes management
- MFA verification during login
"""

import base64
import io
from datetime import datetime, timezone
from typing import List, Optional
import uuid

from fastapi import APIRouter, Depends, HTTPException, status, Request
from pydantic import BaseModel, Field
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
import pyotp
import qrcode
import structlog

from ..config import settings
from ..core.database import get_db
from ..core.security import (
    generate_backup_codes,
    generate_otp_code,
    hash_api_key,
    verify_api_key,
    decode_token,
    create_token_pair,
)
from ..core.redis import set_cache, get_cache, delete_cache
from ..models.user import User
from ..models.mfa import MFADevice, MFAMethod, MFABackupCode
from ..models.session import Session

logger = structlog.get_logger(__name__)
router = APIRouter()


# =============================================================================
# SCHEMAS
# =============================================================================

class MFADeviceResponse(BaseModel):
    """MFA device response."""
    id: str
    name: str
    method: str
    is_primary: bool
    is_verified: bool
    created_at: datetime
    last_used_at: Optional[datetime] = None


class TOTPSetupResponse(BaseModel):
    """TOTP setup response with QR code."""
    device_id: str
    secret: str
    qr_code: str  # Base64 encoded QR code image
    uri: str  # otpauth:// URI


class TOTPVerifyRequest(BaseModel):
    """TOTP verification request."""
    device_id: str
    code: str = Field(min_length=6, max_length=6)


class SMSSetupRequest(BaseModel):
    """SMS MFA setup request."""
    phone_number: str = Field(min_length=10, max_length=20)


class SMSVerifyRequest(BaseModel):
    """SMS verification request."""
    device_id: str
    code: str = Field(min_length=6, max_length=6)


class EmailSetupRequest(BaseModel):
    """Email MFA setup request."""
    email: Optional[str] = None  # Uses user's email if not provided


class EmailVerifyRequest(BaseModel):
    """Email verification request."""
    device_id: str
    code: str = Field(min_length=6, max_length=6)


class BackupCodesResponse(BaseModel):
    """Backup codes response."""
    codes: List[str]
    count: int


class MFAChallengeVerifyRequest(BaseModel):
    """MFA challenge verification request."""
    challenge_id: str
    method: str
    code: str


class MFAChallengeVerifyResponse(BaseModel):
    """MFA challenge verification response."""
    success: bool
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"
    expires_in: int


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


def device_to_response(device: MFADevice) -> MFADeviceResponse:
    """Convert MFADevice to response model."""
    return MFADeviceResponse(
        id=str(device.id),
        name=device.name,
        method=device.method.value,
        is_primary=device.is_primary,
        is_verified=device.is_verified,
        created_at=device.created_at,
        last_used_at=device.last_used_at,
    )


def generate_totp_uri(secret: str, email: str) -> str:
    """Generate otpauth:// URI for TOTP."""
    return pyotp.TOTP(secret).provisioning_uri(
        name=email,
        issuer_name=settings.mfa.totp_issuer,
    )


def generate_qr_code_base64(uri: str) -> str:
    """Generate QR code as base64 encoded PNG."""
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(uri)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    
    return base64.b64encode(buffer.getvalue()).decode()


def verify_totp_code(secret: str, code: str) -> bool:
    """Verify a TOTP code."""
    totp = pyotp.TOTP(secret)
    # Allow 1 time step variance for clock drift
    return totp.verify(code, valid_window=1)


# =============================================================================
# LIST/STATUS ENDPOINTS
# =============================================================================

@router.get("/devices", response_model=List[MFADeviceResponse])
async def list_mfa_devices(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> List[MFADeviceResponse]:
    """
    List all MFA devices for the current user.
    """
    result = await db.execute(
        select(MFADevice)
        .where(MFADevice.user_id == user.id)
        .where(MFADevice.is_active == True)
        .order_by(MFADevice.created_at)
    )
    devices = result.scalars().all()
    
    return [device_to_response(d) for d in devices]


@router.get("/status")
async def get_mfa_status(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Get MFA status for the current user.
    """
    result = await db.execute(
        select(MFADevice)
        .where(MFADevice.user_id == user.id)
        .where(MFADevice.is_active == True)
        .where(MFADevice.is_verified == True)
    )
    verified_devices = result.scalars().all()
    
    # Get backup codes count
    result = await db.execute(
        select(MFABackupCode)
        .where(MFABackupCode.user_id == user.id)
        .where(MFABackupCode.is_used == False)
    )
    backup_codes = result.scalars().all()
    
    return {
        "mfa_enabled": user.mfa_enabled,
        "devices": [
            {
                "id": str(d.id),
                "name": d.name,
                "method": d.method.value,
                "is_primary": d.is_primary,
            }
            for d in verified_devices
        ],
        "backup_codes_remaining": len(backup_codes),
    }


# =============================================================================
# TOTP (AUTHENTICATOR APP) ENDPOINTS
# =============================================================================

@router.post("/totp/setup", response_model=TOTPSetupResponse)
async def setup_totp(
    name: str = "Authenticator",
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> TOTPSetupResponse:
    """
    Set up TOTP MFA (authenticator app).
    
    Returns a QR code to scan with an authenticator app.
    Must be verified before becoming active.
    """
    # Generate secret
    secret = pyotp.random_base32()
    
    # Create device
    device = MFADevice(
        user_id=user.id,
        name=name,
        method=MFAMethod.TOTP,
        secret=secret,
        is_primary=not user.mfa_enabled,  # First device is primary
        is_verified=False,
    )
    
    db.add(device)
    await db.flush()
    
    # Generate QR code
    uri = generate_totp_uri(secret, user.email)
    qr_code = generate_qr_code_base64(uri)
    
    logger.info(
        "TOTP setup initiated",
        user_id=str(user.id),
        device_id=str(device.id),
    )
    
    return TOTPSetupResponse(
        device_id=str(device.id),
        secret=secret,
        qr_code=qr_code,
        uri=uri,
    )


@router.post("/totp/verify")
async def verify_totp_setup(
    request: TOTPVerifyRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Verify TOTP setup by providing a code from the authenticator app.
    """
    # Get device
    try:
        device_id = uuid.UUID(request.device_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"code": "INVALID_ID", "message": "Invalid device ID"},
        )
    
    result = await db.execute(
        select(MFADevice)
        .where(MFADevice.id == device_id)
        .where(MFADevice.user_id == user.id)
        .where(MFADevice.method == MFAMethod.TOTP)
    )
    device = result.scalar_one_or_none()
    
    if not device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "DEVICE_NOT_FOUND", "message": "MFA device not found"},
        )
    
    if device.is_verified:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"code": "ALREADY_VERIFIED", "message": "Device already verified"},
        )
    
    # Verify code
    if not verify_totp_code(device.secret, request.code):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"code": "INVALID_CODE", "message": "Invalid verification code"},
        )
    
    # Mark as verified
    device.is_verified = True
    device.verified_at = datetime.now(timezone.utc)
    
    # Enable MFA for user if this is first device
    if not user.mfa_enabled:
        user.mfa_enabled = True
        user.updated_at = datetime.now(timezone.utc)
    
    logger.info(
        "TOTP setup verified",
        user_id=str(user.id),
        device_id=str(device.id),
    )
    
    return {
        "success": True,
        "message": "TOTP device verified successfully",
        "device_id": str(device.id),
    }


# =============================================================================
# SMS MFA ENDPOINTS
# =============================================================================

@router.post("/sms/setup")
async def setup_sms_mfa(
    request: SMSSetupRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Set up SMS MFA.
    
    Sends a verification code to the provided phone number.
    """
    # Create device
    device = MFADevice(
        user_id=user.id,
        name=f"SMS ({request.phone_number[-4:]})",
        method=MFAMethod.SMS,
        secret=generate_otp_code(6),  # Temporary OTP for verification
        phone_number=request.phone_number,
        is_primary=not user.mfa_enabled,
        is_verified=False,
    )
    
    db.add(device)
    await db.flush()
    
    # Store OTP in cache
    await set_cache(
        f"mfa_sms_verify:{device.id}",
        device.secret,
        ttl=600,  # 10 minutes
    )
    
    # Send SMS (placeholder - would use Twilio or similar)
    logger.info(
        "SMS MFA setup initiated",
        user_id=str(user.id),
        device_id=str(device.id),
        phone=request.phone_number[-4:],  # Log only last 4 digits
    )
    
    return {
        "success": True,
        "device_id": str(device.id),
        "message": "Verification code sent to phone",
    }


@router.post("/sms/verify")
async def verify_sms_setup(
    request: SMSVerifyRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Verify SMS MFA setup.
    """
    try:
        device_id = uuid.UUID(request.device_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"code": "INVALID_ID", "message": "Invalid device ID"},
        )
    
    result = await db.execute(
        select(MFADevice)
        .where(MFADevice.id == device_id)
        .where(MFADevice.user_id == user.id)
        .where(MFADevice.method == MFAMethod.SMS)
    )
    device = result.scalar_one_or_none()
    
    if not device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "DEVICE_NOT_FOUND", "message": "MFA device not found"},
        )
    
    # Verify code from cache
    cached_code = await get_cache(f"mfa_sms_verify:{device.id}")
    if not cached_code or cached_code != request.code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"code": "INVALID_CODE", "message": "Invalid or expired code"},
        )
    
    # Clear verification code
    await delete_cache(f"mfa_sms_verify:{device.id}")
    
    # Generate new secret for future OTPs
    device.secret = pyotp.random_base32()
    device.is_verified = True
    device.verified_at = datetime.now(timezone.utc)
    
    if not user.mfa_enabled:
        user.mfa_enabled = True
        user.updated_at = datetime.now(timezone.utc)
    
    logger.info(
        "SMS MFA setup verified",
        user_id=str(user.id),
        device_id=str(device.id),
    )
    
    return {
        "success": True,
        "message": "SMS MFA verified successfully",
    }


# =============================================================================
# EMAIL MFA ENDPOINTS
# =============================================================================

@router.post("/email/setup")
async def setup_email_mfa(
    request: EmailSetupRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Set up email MFA.
    """
    email = request.email or user.email
    
    # Create device
    device = MFADevice(
        user_id=user.id,
        name=f"Email ({email})",
        method=MFAMethod.EMAIL,
        secret=generate_otp_code(6),
        email=email,
        is_primary=not user.mfa_enabled,
        is_verified=False,
    )
    
    db.add(device)
    await db.flush()
    
    # Store OTP in cache
    await set_cache(
        f"mfa_email_verify:{device.id}",
        device.secret,
        ttl=600,
    )
    
    # Send email (placeholder)
    logger.info(
        "Email MFA setup initiated",
        user_id=str(user.id),
        device_id=str(device.id),
    )
    
    return {
        "success": True,
        "device_id": str(device.id),
        "message": "Verification code sent to email",
    }


@router.post("/email/verify")
async def verify_email_setup(
    request: EmailVerifyRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Verify email MFA setup.
    """
    try:
        device_id = uuid.UUID(request.device_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"code": "INVALID_ID", "message": "Invalid device ID"},
        )
    
    result = await db.execute(
        select(MFADevice)
        .where(MFADevice.id == device_id)
        .where(MFADevice.user_id == user.id)
        .where(MFADevice.method == MFAMethod.EMAIL)
    )
    device = result.scalar_one_or_none()
    
    if not device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "DEVICE_NOT_FOUND", "message": "MFA device not found"},
        )
    
    cached_code = await get_cache(f"mfa_email_verify:{device.id}")
    if not cached_code or cached_code != request.code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"code": "INVALID_CODE", "message": "Invalid or expired code"},
        )
    
    await delete_cache(f"mfa_email_verify:{device.id}")
    
    device.secret = pyotp.random_base32()
    device.is_verified = True
    device.verified_at = datetime.now(timezone.utc)
    
    if not user.mfa_enabled:
        user.mfa_enabled = True
        user.updated_at = datetime.now(timezone.utc)
    
    return {
        "success": True,
        "message": "Email MFA verified successfully",
    }


# =============================================================================
# BACKUP CODES
# =============================================================================

@router.post("/backup-codes/generate", response_model=BackupCodesResponse)
async def generate_new_backup_codes(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> BackupCodesResponse:
    """
    Generate new backup codes.
    
    This invalidates any existing backup codes.
    """
    if not user.mfa_enabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"code": "MFA_NOT_ENABLED", "message": "MFA must be enabled first"},
        )
    
    # Delete existing backup codes
    await db.execute(
        delete(MFABackupCode).where(MFABackupCode.user_id == user.id)
    )
    
    # Generate new codes
    codes = generate_backup_codes(settings.mfa.backup_codes_count)
    
    # Store hashed codes
    for code in codes:
        backup_code = MFABackupCode(
            user_id=user.id,
            code_hash=hash_api_key(code),
        )
        db.add(backup_code)
    
    logger.info(
        "Backup codes generated",
        user_id=str(user.id),
        count=len(codes),
    )
    
    return BackupCodesResponse(
        codes=codes,
        count=len(codes),
    )


@router.get("/backup-codes/count")
async def get_backup_codes_count(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Get the number of remaining backup codes.
    """
    result = await db.execute(
        select(MFABackupCode)
        .where(MFABackupCode.user_id == user.id)
        .where(MFABackupCode.is_used == False)
    )
    codes = result.scalars().all()
    
    return {
        "remaining": len(codes),
    }


# =============================================================================
# DEVICE MANAGEMENT
# =============================================================================

@router.delete("/devices/{device_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_mfa_device(
    device_id: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Delete an MFA device.
    """
    try:
        did = uuid.UUID(device_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"code": "INVALID_ID", "message": "Invalid device ID"},
        )
    
    result = await db.execute(
        select(MFADevice)
        .where(MFADevice.id == did)
        .where(MFADevice.user_id == user.id)
    )
    device = result.scalar_one_or_none()
    
    if not device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "DEVICE_NOT_FOUND", "message": "MFA device not found"},
        )
    
    # Check if this is the last verified device
    result = await db.execute(
        select(MFADevice)
        .where(MFADevice.user_id == user.id)
        .where(MFADevice.id != did)
        .where(MFADevice.is_verified == True)
        .where(MFADevice.is_active == True)
    )
    other_devices = result.scalars().all()
    
    # Deactivate device
    device.is_active = False
    
    # Disable MFA if no other verified devices
    if not other_devices:
        user.mfa_enabled = False
        user.updated_at = datetime.now(timezone.utc)
    
    logger.info(
        "MFA device deleted",
        user_id=str(user.id),
        device_id=device_id,
    )


@router.post("/devices/{device_id}/primary", status_code=status.HTTP_204_NO_CONTENT)
async def set_primary_device(
    device_id: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Set a device as the primary MFA device.
    """
    try:
        did = uuid.UUID(device_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"code": "INVALID_ID", "message": "Invalid device ID"},
        )
    
    result = await db.execute(
        select(MFADevice)
        .where(MFADevice.id == did)
        .where(MFADevice.user_id == user.id)
        .where(MFADevice.is_verified == True)
    )
    device = result.scalar_one_or_none()
    
    if not device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "DEVICE_NOT_FOUND", "message": "Verified device not found"},
        )
    
    # Remove primary from all other devices
    result = await db.execute(
        select(MFADevice)
        .where(MFADevice.user_id == user.id)
        .where(MFADevice.is_primary == True)
    )
    for d in result.scalars().all():
        d.is_primary = False
    
    device.is_primary = True


# =============================================================================
# MFA CHALLENGE VERIFICATION
# =============================================================================

@router.post("/verify", response_model=MFAChallengeVerifyResponse)
async def verify_mfa_challenge(
    request: MFAChallengeVerifyRequest,
    http_request: Request,
    db: AsyncSession = Depends(get_db),
) -> MFAChallengeVerifyResponse:
    """
    Verify MFA challenge during login.
    
    Called after initial login returns mfa_required=true.
    """
    # Get challenge from cache
    challenge_data = await get_cache(f"mfa_challenge:{request.challenge_id}")
    
    if not challenge_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"code": "INVALID_CHALLENGE", "message": "Challenge expired or invalid"},
        )
    
    user_id = challenge_data.get("user_id")
    
    # Get user
    result = await db.execute(
        select(User).where(User.id == uuid.UUID(user_id))
    )
    user = result.scalar_one_or_none()
    
    if not user or not user.is_active():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"code": "USER_INVALID", "message": "User account is invalid"},
        )
    
    # Handle backup code
    if request.method == "backup":
        result = await db.execute(
            select(MFABackupCode)
            .where(MFABackupCode.user_id == user.id)
            .where(MFABackupCode.is_used == False)
        )
        backup_codes = result.scalars().all()
        
        code_valid = False
        for bc in backup_codes:
            if verify_api_key(request.code, bc.code_hash):
                bc.is_used = True
                bc.used_at = datetime.now(timezone.utc)
                code_valid = True
                break
        
        if not code_valid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"code": "INVALID_CODE", "message": "Invalid backup code"},
            )
    else:
        # Get device for the method
        method = MFAMethod(request.method)
        result = await db.execute(
            select(MFADevice)
            .where(MFADevice.user_id == user.id)
            .where(MFADevice.method == method)
            .where(MFADevice.is_verified == True)
            .where(MFADevice.is_active == True)
        )
        device = result.scalar_one_or_none()
        
        if not device:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"code": "NO_DEVICE", "message": f"No verified {request.method} device"},
            )
        
        # Verify based on method
        if method == MFAMethod.TOTP:
            if not verify_totp_code(device.secret, request.code):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail={"code": "INVALID_CODE", "message": "Invalid TOTP code"},
                )
        elif method in (MFAMethod.SMS, MFAMethod.EMAIL):
            cached_code = await get_cache(f"mfa_login:{request.challenge_id}")
            if not cached_code or cached_code != request.code:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail={"code": "INVALID_CODE", "message": "Invalid or expired code"},
                )
            await delete_cache(f"mfa_login:{request.challenge_id}")
        
        device.last_used_at = datetime.now(timezone.utc)
    
    # Clear challenge
    await delete_cache(f"mfa_challenge:{request.challenge_id}")
    
    # Create session
    client_ip = http_request.client.host if http_request.client else "unknown"
    session_id = str(uuid.uuid4())
    
    session = Session(
        user_id=user.id,
        refresh_token_jti=session_id,
        ip_address=client_ip,
        expires_at=datetime.now(timezone.utc) + settings.jwt.refresh_token_expire_days,
    )
    db.add(session)
    
    # Generate tokens
    access_token, refresh_token = create_token_pair(
        user_id=str(user.id),
        session_id=session_id,
        email=user.email,
        roles=user.roles,
        permissions=user.permissions,
        tenant_id=str(user.tenant_id) if user.tenant_id else None,
    )
    
    # Update user
    user.last_login_at = datetime.now(timezone.utc)
    user.failed_login_attempts = 0
    
    logger.info(
        "MFA verification successful",
        user_id=str(user.id),
        method=request.method,
    )
    
    return MFAChallengeVerifyResponse(
        success=True,
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="Bearer",
        expires_in=settings.jwt.access_token_expire_minutes * 60,
    )


# =============================================================================
# DISABLE MFA
# =============================================================================

@router.post("/disable")
async def disable_mfa(
    password: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Disable MFA for the account.
    
    Requires password confirmation.
    """
    from ..core.security import verify_password
    
    if not verify_password(password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"code": "INVALID_PASSWORD", "message": "Password is incorrect"},
        )
    
    # Deactivate all devices
    result = await db.execute(
        select(MFADevice).where(MFADevice.user_id == user.id)
    )
    for device in result.scalars().all():
        device.is_active = False
    
    # Delete backup codes
    await db.execute(
        delete(MFABackupCode).where(MFABackupCode.user_id == user.id)
    )
    
    # Disable MFA
    user.mfa_enabled = False
    user.updated_at = datetime.now(timezone.utc)
    
    logger.info(
        "MFA disabled",
        user_id=str(user.id),
    )
    
    return {
        "success": True,
        "message": "MFA has been disabled",
    }
