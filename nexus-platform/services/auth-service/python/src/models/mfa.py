# =============================================================================
# NEXUS PLATFORM - AUTHENTICATION SERVICE - MFA MODELS
# =============================================================================
# SQLAlchemy models for multi-factor authentication.
# =============================================================================

import enum
from datetime import datetime
from typing import Optional
import uuid

from sqlalchemy import Boolean, DateTime, String, Enum, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

from ..core.database import Base


class MFAMethod(str, enum.Enum):
    """MFA method types."""
    TOTP = "totp"           # Time-based One-Time Password
    SMS = "sms"             # SMS OTP
    EMAIL = "email"         # Email OTP
    WEBAUTHN = "webauthn"   # WebAuthn/FIDO2


class MFADevice(Base):
    """
    MFA device model.
    
    Stores MFA devices and secrets for users.
    """
    __tablename__ = "mfa_devices"
    
    # Primary key
    id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    
    # User reference
    user_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    
    # Device details
    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    method: Mapped[MFAMethod] = mapped_column(
        Enum(MFAMethod),
        nullable=False,
    )
    
    # Secret (encrypted in production)
    secret: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    
    # For WebAuthn
    credential_id: Mapped[Optional[str]] = mapped_column(
        String(500),
        nullable=True,
    )
    public_key: Mapped[Optional[str]] = mapped_column(
        String(2000),
        nullable=True,
    )
    sign_count: Mapped[int] = mapped_column(
        default=0,
        nullable=False,
    )
    
    # For phone/email
    phone_number: Mapped[Optional[str]] = mapped_column(
        String(20),
        nullable=True,
    )
    email: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
    )
    
    # Status
    is_primary: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )
    is_verified: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False,
    )
    verified_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    last_used_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    
    # Relationships
    user: Mapped["User"] = relationship(
        "User",
        back_populates="mfa_devices",
    )
    
    # Indexes
    __table_args__ = (
        Index("ix_mfa_devices_user_method", "user_id", "method"),
    )
    
    def __repr__(self) -> str:
        return f"<MFADevice {self.name} ({self.method})>"


class MFABackupCode(Base):
    """
    MFA backup code model.
    
    Stores one-time backup codes for MFA recovery.
    """
    __tablename__ = "mfa_backup_codes"
    
    # Primary key
    id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    
    # User reference
    user_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    
    # Code (hashed)
    code_hash: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
    )
    
    # Status
    is_used: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )
    used_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False,
    )
    
    def __repr__(self) -> str:
        return f"<MFABackupCode user={self.user_id}>"


# Import for type hints
from .user import User
