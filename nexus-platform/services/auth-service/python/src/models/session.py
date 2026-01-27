# =============================================================================
# NEXUS PLATFORM - AUTHENTICATION SERVICE - SESSION MODEL
# =============================================================================
# SQLAlchemy model for user sessions.
# =============================================================================

from datetime import datetime
from typing import Optional
import uuid

from sqlalchemy import Boolean, DateTime, String, Text, JSON, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

from ..core.database import Base


class Session(Base):
    """
    User session model.
    
    Tracks active user sessions for security and session management.
    """
    __tablename__ = "sessions"
    
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
    
    # Session details
    refresh_token_jti: Mapped[str] = mapped_column(
        String(64),
        unique=True,
        nullable=False,
        index=True,
    )
    
    # Device information
    device_id: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
    )
    device_type: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
    )
    device_name: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
    )
    os: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
    )
    os_version: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
    )
    browser: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
    )
    browser_version: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
    )
    
    # Location
    ip_address: Mapped[Optional[str]] = mapped_column(
        String(45),
        nullable=True,
    )
    location: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
    )
    country: Mapped[Optional[str]] = mapped_column(
        String(2),
        nullable=True,
    )
    
    # Status
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )
    revoked: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )
    revoked_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    revoked_reason: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
    )
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False,
    )
    last_active_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False,
    )
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )
    
    # Metadata
    metadata: Mapped[dict] = mapped_column(
        JSON,
        default=dict,
        nullable=False,
    )
    
    # Relationships
    user: Mapped["User"] = relationship(
        "User",
        back_populates="sessions",
    )
    
    # Indexes
    __table_args__ = (
        Index("ix_sessions_user_active", "user_id", "is_active"),
        Index("ix_sessions_expires", "expires_at"),
    )
    
    def __repr__(self) -> str:
        return f"<Session {self.id} user={self.user_id}>"
    
    def is_valid(self) -> bool:
        """Check if session is still valid."""
        if self.revoked:
            return False
        if not self.is_active:
            return False
        if self.expires_at < datetime.utcnow():
            return False
        return True


# Import for type hints
from .user import User
