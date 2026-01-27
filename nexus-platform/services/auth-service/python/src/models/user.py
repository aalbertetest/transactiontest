# =============================================================================
# NEXUS PLATFORM - AUTHENTICATION SERVICE - USER MODEL
# =============================================================================
# SQLAlchemy model for user accounts.
# =============================================================================

import enum
from datetime import datetime
from typing import List, Optional

from sqlalchemy import Boolean, DateTime, Enum, String, Integer, Text, JSON, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
import uuid

from ..core.database import Base


class UserStatus(str, enum.Enum):
    """User account status."""
    PENDING = "pending"        # Email verification pending
    ACTIVE = "active"          # Normal active state
    INACTIVE = "inactive"      # Manually deactivated
    SUSPENDED = "suspended"    # Temporarily suspended
    LOCKED = "locked"          # Locked due to failed attempts
    DELETED = "deleted"        # Soft deleted


class User(Base):
    """
    User account model.
    
    Stores user credentials and profile information for authentication.
    """
    __tablename__ = "users"
    
    # Primary key
    id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    
    # Credentials
    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
    )
    email_verified: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )
    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    
    # Profile
    username: Mapped[Optional[str]] = mapped_column(
        String(50),
        unique=True,
        nullable=True,
        index=True,
    )
    display_name: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
    )
    first_name: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
    )
    last_name: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
    )
    phone: Mapped[Optional[str]] = mapped_column(
        String(20),
        nullable=True,
    )
    phone_verified: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )
    avatar_url: Mapped[Optional[str]] = mapped_column(
        String(500),
        nullable=True,
    )
    
    # Status
    status: Mapped[UserStatus] = mapped_column(
        Enum(UserStatus),
        default=UserStatus.PENDING,
        nullable=False,
        index=True,
    )
    
    # Organization/Tenant
    tenant_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        PG_UUID(as_uuid=True),
        nullable=True,
        index=True,
    )
    
    # Roles and permissions (stored as JSON array)
    roles: Mapped[List[str]] = mapped_column(
        JSON,
        default=list,
        nullable=False,
    )
    permissions: Mapped[List[str]] = mapped_column(
        JSON,
        default=list,
        nullable=False,
    )
    
    # MFA
    mfa_enabled: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )
    
    # Security
    failed_login_attempts: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )
    locked_until: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    password_changed_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )
    last_login_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    deleted_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    
    # Metadata
    metadata: Mapped[dict] = mapped_column(
        JSON,
        default=dict,
        nullable=False,
    )
    
    # Relationships
    sessions: Mapped[List["Session"]] = relationship(
        "Session",
        back_populates="user",
        cascade="all, delete-orphan",
    )
    api_keys: Mapped[List["APIKey"]] = relationship(
        "APIKey",
        back_populates="user",
        cascade="all, delete-orphan",
    )
    mfa_devices: Mapped[List["MFADevice"]] = relationship(
        "MFADevice",
        back_populates="user",
        cascade="all, delete-orphan",
    )
    
    # Indexes
    __table_args__ = (
        Index("ix_users_email_lower", "email"),
        Index("ix_users_status_created", "status", "created_at"),
    )
    
    def __repr__(self) -> str:
        return f"<User {self.email}>"
    
    @property
    def full_name(self) -> Optional[str]:
        """Get user's full name."""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.display_name or self.username
    
    def has_role(self, role: str) -> bool:
        """Check if user has a specific role."""
        return role in self.roles
    
    def has_permission(self, permission: str) -> bool:
        """Check if user has a specific permission."""
        return permission in self.permissions
    
    def is_active(self) -> bool:
        """Check if user account is active."""
        return self.status == UserStatus.ACTIVE
    
    def is_locked(self) -> bool:
        """Check if user account is locked."""
        if self.status == UserStatus.LOCKED:
            return True
        if self.locked_until and self.locked_until > datetime.utcnow():
            return True
        return False


# Import for relationship type hints (avoid circular imports)
from .session import Session
from .api_key import APIKey
from .mfa import MFADevice
