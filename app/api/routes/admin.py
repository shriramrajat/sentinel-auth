from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.api.deps import get_db
from app.schemas.user import UserResponse
from app.services.user_service import UserService

router = APIRouter()

@router.get("/users", response_model=List[UserResponse])
def get_all_users(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    """
    Get all users (Admin only).
    """
    user_service = UserService(db)
    return user_service.get_all_users(skip=skip, limit=limit)
