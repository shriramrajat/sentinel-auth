"""
User Repository.
"""

from typing import Optional
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.db.models.user import User
from app.schemas.user import UserCreate, UserUpdate

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

    def get_all(self, skip: int = 0, limit: int = 100) -> list[User]:
        """Get all users with pagination."""
        return self.db.query(User).offset(skip).limit(limit).all()

    def update(self, user: User, user_in: UserUpdate) -> User:
        """
        Update user fields.
        """
        update_data = user_in.model_dump(exclude_unset=True)
        
        # If password is being updated, it should be hashed by the service layer first
        # But for safety, we assume the service handles the hashing logic and passes 
        # the HASHED string if it was 'password', or we separate concerns.
        # Let's keep it simple: The repo just saves data.
        
        for field, value in update_data.items():
            setattr(user, field, value)

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
