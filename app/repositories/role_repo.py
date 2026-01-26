"""
Role Repository.
"""

from typing import Optional
from sqlalchemy.orm import Session
from app.db.models.role import Role

class RoleRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_name(self, name: str) -> Optional[Role]:
        """Get a role by its unique name."""
        return self.db.query(Role).filter(Role.name == name).first()
    
    def get_by_id(self, role_id: int) -> Optional[Role]:
        """Get a role by ID."""
        return self.db.query(Role).filter(Role.id == role_id).first()
