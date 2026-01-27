from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.api.deps import get_db, get_current_active_superuser
from app.schemas.user import UserResponse
from app.services.user_service import UserService
from app.db.models.user import User

router = APIRouter()

@router.get("/users", response_model=List[UserResponse])
def get_all_users(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_superuser) # <--- Security added here
):
    """
    Get all users (Admin only).
    """
    user_service = UserService(db)
    return user_service.get_all_users(skip=skip, limit=limit)
