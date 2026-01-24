"""
RefreshToken database model.

This module defines the RefreshToken model for managing JWT refresh tokens.
Each user can have multiple refresh tokens (multi-device support).
"""

import uuid
from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy import String, Boolean, ForeignKey, UUID, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.db.models.user import User


class RefreshToken(Base):
    """
    RefreshToken model for managing JWT refresh tokens.
    
    Refresh tokens allow users to obtain new access tokens without
    re-authenticating. Each user can have multiple refresh tokens
    to support multiple devices/sessions.
    
    Security features:
    - Tokens are hashed before storage (like passwords)
    - Tokens can be revoked
    - Tokens have expiration dates
    - Tokens are deleted when user is deleted (cascade)
    
    Attributes:
        id: Primary key
        user_id: Foreign key to users table (UUID)
        token_hash: Hashed refresh token (never store plain tokens!)
        expires_at: When this token expires
        is_revoked: Whether this token has been revoked
        created_at: When this token was created
        user: The user who owns this token (relationship)
    """
    
    __tablename__ = "refresh_tokens"
    
    # Primary Key
    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
        comment="Unique token identifier"
    )
    
    # User Reference (Foreign Key - UUID)
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="Foreign key to users table (UUID)"
    )
    
    # Token Information
    token_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True,
        comment="Hashed refresh token (never store plain tokens!)"
    )
    
    expires_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        index=True,
        comment="When this token expires (for cleanup queries)"
    )
    
    is_revoked: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
        index=True,
        comment="Whether this token has been revoked (logout)"
    )
    
    # Timestamp
    created_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow,
        nullable=False,
        comment="When this token was created"
    )
    
    # Relationships
    user: Mapped["User"] = relationship(
        "User",
        back_populates="refresh_tokens",
        lazy="joined"  # Always load user with token (common use case)
    )
    
    def __repr__(self) -> str:
        """String representation of RefreshToken."""
        return (
            f"<RefreshToken(id={self.id}, user_id={self.user_id}, "
            f"expires_at={self.expires_at}, is_revoked={self.is_revoked})>"
        )
    
    @property
    def is_expired(self) -> bool:
        """
        Check if this token has expired.
        
        Returns:
            True if token is expired, False otherwise
        """
        return datetime.utcnow() > self.expires_at
    
    @property
    def is_valid(self) -> bool:
        """
        Check if this token is valid (not expired and not revoked).
        
        Returns:
            True if token is valid, False otherwise
        """
        return not self.is_expired and not self.is_revoked
