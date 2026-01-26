"""
User Repository.
"""

from typing import Optional
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.db.models.user import User
from app.schemas.user import UserCreate

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_username(self, username: str) -> Optional[User]:
        """Get user by username."""
        return self.db.query(User).filter(User.username == username).first()

    def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        return self.db.query(User).filter(User.email == email).first()
    
    def get_by_id(self, user_id: UUID) -> Optional[User]:
        """Get user by UUID."""
        return self.db.query(User).filter(User.id == user_id).first()
    
    def get_by_username_or_email(self, identifier: str) -> Optional[User]:
        """Get user by username OR email (for login)."""
        return self.db.query(User).filter(
            or_(User.username == identifier, User.email == identifier)
        ).first()

    def create(self, user_in: UserCreate, password_hash: str, role_id: int) -> User:
        """
        Create a new user.
        NOTE: Repository expects already hashed password.
        """
        db_user = User(
            username=user_in.username,
            email=user_in.email,
            password_hash=password_hash,
            role_id=role_id,
            is_active=True
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
