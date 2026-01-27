# =============================================================================
# NEXUS PLATFORM - AUTHENTICATION SERVICE - API KEY MODEL
# =============================================================================
# SQLAlchemy model for API keys.
# =============================================================================

from datetime import datetime
from typing import List, Optional
import uuid

from sqlalchemy import Boolean, DateTime, String, Integer, JSON, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

from ..core.database import Base


class APIKey(Base):
    """
    API key model.
    
    Stores API keys for programmatic access to the platform.
    """
    __tablename__ = "api_keys"
    
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
    
    # Key details
    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    key_prefix: Mapped[str] = mapped_column(
        String(12),
        nullable=False,
    )
    key_hash: Mapped[str] = mapped_column(
        String(64),
        unique=True,
        nullable=False,
        index=True,
    )
    
    # Permissions
    scopes: Mapped[List[str]] = mapped_column(
        JSON,
        default=list,
        nullable=False,
    )
    
    # Restrictions
    allowed_ips: Mapped[List[str]] = mapped_column(
        JSON,
        default=list,
        nullable=False,
    )
    rate_limit: Mapped[Optional[int]] = mapped_column(
        Integer,
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
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False,
    )
    expires_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    last_used_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    
    # Usage stats
    usage_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
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
        back_populates="api_keys",
    )
    
    # Indexes
    __table_args__ = (
        Index("ix_api_keys_user_active", "user_id", "is_active"),
    )
    
    def __repr__(self) -> str:
        return f"<APIKey {self.name} ({self.key_prefix}...)>"
    
    def is_valid(self) -> bool:
        """Check if API key is valid."""
        if self.revoked:
            return False
        if not self.is_active:
            return False
        if self.expires_at and self.expires_at < datetime.utcnow():
            return False
        return True
    
    def has_scope(self, scope: str) -> bool:
        """Check if key has a specific scope."""
        return scope in self.scopes or "*" in self.scopes


# Import for type hints
from .user import User
