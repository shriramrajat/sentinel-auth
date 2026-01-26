"""
Token Repository.
"""

from datetime import datetime
from typing import Optional, List
from uuid import UUID
from sqlalchemy.orm import Session

from app.db.models.refresh_token import RefreshToken

class TokenRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, user_id: UUID, token_hash: str, expires_at: datetime) -> RefreshToken:
        """Create and store a new refresh token."""
        db_token = RefreshToken(
            user_id=user_id,
            token_hash=token_hash,
            expires_at=expires_at,
            is_revoked=False
        )
        self.db.add(db_token)
        self.db.commit()
        self.db.refresh(db_token)
        return db_token

    def get_by_hash(self, token_hash: str) -> Optional[RefreshToken]:
        """Get a refresh token by its hash."""
        return self.db.query(RefreshToken).filter(
            RefreshToken.token_hash == token_hash
        ).first()
    
    def revoke(self, token_obj: RefreshToken) -> None:
        """Revoke a specific token."""
        token_obj.is_revoked = True
        self.db.commit()
        self.db.refresh(token_obj)
        
    def revoke_all_for_user(self, user_id: UUID) -> None:
        """Revoke ALL tokens for a user (Global Logout)."""
        self.db.query(RefreshToken).filter(
            RefreshToken.user_id == user_id,
            RefreshToken.is_revoked == False
        ).update({"is_revoked": True})
        self.db.commit()
