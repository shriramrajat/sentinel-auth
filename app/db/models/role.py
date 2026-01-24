"""
Role database model.

This module defines the Role model for role-based access control (RBAC).
Roles define what permissions a user has in the system.
"""

from datetime import datetime
from typing import List, TYPE_CHECKING
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.db.models.user import User


class Role(Base):
    """
    Role model for RBAC (Role-Based Access Control).
    
    Defines user roles in the system. Each user has exactly one role.
    Common roles: 'admin', 'user'
    
    Attributes:
        id: Primary key
        name: Unique role name (e.g., 'admin', 'user')
        description: Optional description of the role
        created_at: Timestamp when role was created
        users: List of users with this role (relationship)
    """
    
    __tablename__ = "roles"
    
    # Primary Key
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    
    # Role Information
    name: Mapped[str] = mapped_column(
        String(50), 
        unique=True, 
        nullable=False,
        index=True,
        comment="Unique role name (e.g., 'admin', 'user')"
    )
    
    description: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        comment="Optional description of the role"
    )
    
    # Timestamp
    created_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow,
        nullable=False,
        comment="When this role was created"
    )
    
    # Relationships
    users: Mapped[List["User"]] = relationship(
        "User",
        back_populates="role",
        cascade="all, delete-orphan"  # Delete users if role deleted (careful!)
    )
    
    def __repr__(self) -> str:
        """String representation of Role."""
        return f"<Role(id={self.id}, name='{self.name}')>"
