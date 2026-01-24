"""
User database model.

This module defines the User model which represents authenticated users
in the system. Each user has a role and can have multiple refresh tokens.
"""

import uuid
from datetime import datetime
from typing import List, TYPE_CHECKING
from sqlalchemy import String, Boolean, ForeignKey, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.db.models.role import Role
    from app.db.models.refresh_token import RefreshToken


class User(Base):
    """
    User model representing an authenticated user in the system.
    
    Each user has:
    - A unique UUID identifier
    - Unique username and email
    - Password hash (never store plain passwords!)
    - A role (admin, user, etc.)
    - Active status flag
    - Timestamps for creation and updates
    - Multiple refresh tokens (for multi-device support)
    
    Attributes:
        id: UUID primary key
        username: Unique username for login
        email: Unique email address (required)
        password_hash: Bcrypt hashed password
        role_id: Foreign key to roles table
        is_active: Whether the user account is active
        created_at: When the user was created
        updated_at: When the user was last updated
        role: The user's role (relationship)
        refresh_tokens: List of user's refresh tokens (relationship)
    """
    
    __tablename__ = "users"
    
    # Primary Key (UUID)
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        comment="Unique user identifier (UUID)"
    )
    
    # User Credentials
    username: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
        index=True,
        comment="Unique username for login"
    )
    
    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
        comment="User's email address (required and unique)"
    )
    
    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment="Bcrypt hashed password (never store plain passwords!)"
    )
    
    # Role (Foreign Key)
    role_id: Mapped[int] = mapped_column(
        ForeignKey("roles.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
        comment="Foreign key to roles table"
    )
    
    # Account Status
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
        comment="Whether the user account is active"
    )
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow,
        nullable=False,
        comment="When this user was created"
    )
    
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
        comment="When this user was last updated"
    )
    
    # Relationships
    role: Mapped["Role"] = relationship(
        "Role",
        back_populates="users",
        lazy="joined"  # Always load role with user (common use case)
    )
    
    refresh_tokens: Mapped[List["RefreshToken"]] = relationship(
        "RefreshToken",
        back_populates="user",
        cascade="all, delete-orphan",  # Delete tokens when user is deleted
        lazy="select"  # Load tokens only when accessed
    )
    
    def __repr__(self) -> str:
        """String representation of User."""
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"
