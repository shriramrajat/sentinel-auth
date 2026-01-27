from typing import Generator
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.core.config import settings
from app.core.security import decode_token
from app.repositories.user_repo import UserRepository
from app.schemas.token import TokenPayload
from app.db.models.user import User

# This tells FastAPI that the token is sent in the Authorization header as "Bearer <token>"
reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_PREFIX}/auth/login"
)

def get_db() -> Generator:
    """
    Dependency that creates a new database session for a request
    and closes it after the request is finished.
    """
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(reusable_oauth2)
) -> User:
    """
    Validate the token and return the current user.
    """
    try:
        payload = decode_token(token)
        token_data = TokenPayload(**payload)
    except (JWTError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
        
    user_repo = UserRepository(db)
    user = user_repo.get_by_id(token_data.sub)
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
        
    return user

def get_current_active_superuser(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Check if the current user has admin privileges.
    """
    # Assuming the role loaded via relationship is accessible as .role.name
    # Since we eager load or access it, this depends on the model definition.
    # In User model: role = relationship("Role", ...)
    if current_user.role.name != "admin":
        raise HTTPException(
            status_code=403, detail="The user doesn't have enough privileges"
        )
    return current_user