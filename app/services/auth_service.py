from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.repositories.user_repo import UserRepository
from app.core.security import verify_password
from app.core.tokens import create_access_token, create_refresh_token
from app.schemas.token import Token

class AuthService:
    def __init__(self, db: Session):
        self.user_repo = UserRepository(db)

    def login(self, username: str, password: str) -> Token:
        """
        Authenticate a user and return tokens.
        """
        # 1. Find the user (allowing login by username)
        user = self.user_repo.get_by_username(username)
        
        # 2. Verify user and password
        if not user or not verify_password(password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # 3. Generate tokens
        access_token = create_access_token(user_id=str(user.id), role=user.role.name)
        refresh_token = create_refresh_token(user_id=str(user.id))

        return Token(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer"
        )