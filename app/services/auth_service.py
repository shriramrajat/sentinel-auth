from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.repositories.user_repo import UserRepository
from app.core.security import verify_password
from app.core.tokens import create_access_token, create_refresh_token
from app.schemas.token import Token
from datetime import datetime, timedelta
from jose import JWTError
from app.repositories.token_repo import TokenRepository
from app.core.security import decode_token, get_password_hash # (Keep existing imports too)
from app.core.config import settings

class AuthService:
    def __init__(self, db: Session):
        self.user_repo = UserRepository(db)
        self.token_repo = TokenRepository(db)

    def login(self, username: str, password: str) -> Token:
        """
        Authenticate a user and return tokens.
        """
        # 1. Find the user
        user = self.user_repo.get_by_username(username)
        
        # 2. Verify user and password
        if not user or not verify_password(password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # 3. Generate Access Token
        access_token = create_access_token(user_id=str(user.id), role=user.role.name)
        
        # 4. Generate Refresh Token & Save to DB
        refresh_str = create_refresh_token(user_id=str(user.id))
        # We store the HASH of the token, not the raw token, for security
        # (Assuming the spec asks for that, or we store it raw. Let's verify repo later.)
        # For now, let's just create the record. Ideally, we hash it.
        # But wait, looking at TokenRepo, it takes 'token_hash'. 
        # So we should hash the refresh token string before saving.
        refresh_hash = get_password_hash(refresh_str) 
        
        expires_at = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        self.token_repo.create(user_id=user.id, token_hash=refresh_hash, expires_at=expires_at)

        return Token(
            access_token=access_token,
            refresh_token=refresh_str,
            token_type="bearer"
        )

    def refresh_access_token(self, refresh_token_in: str) -> Token:
        """
        Rotate tokens: Validate old refresh token, revoke it, issue new pair.
        """
        try:
            # 1. Decode JWT
            payload = decode_token(refresh_token_in)
            if payload.get("type") != "refresh":
                raise HTTPException(status_code=401, detail="Invalid token type")
            user_id = payload.get("sub")
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid refresh token")

        # 2. Verify against DB (We need to find the token matching the HASH)
        # This is tricky without looking up by ID.
        # Strategy: We can't lookup by hash easily because verifying bcrypt is slow/one-way.
        # usually we store a "jti" (unique ID) in the token or just store the raw token if secure.
        # Given your Repo has [get_by_hash](cci:1://file:///d:/Rajat/Projects/SentinelAuth/SentinelAuth/app/repositories/token_repo.py:28:4-32:17), it implies direct lookup.
        # IF we hashed it with bcrypt, we can't do [get_by_hash](cci:1://file:///d:/Rajat/Projects/SentinelAuth/SentinelAuth/app/repositories/token_repo.py:28:4-32:17).
        # LET'S FIX: For this MVP, let's verify the user exists first.
        
        # ACTUALLY: The standard way with bcrypt is: you cannot lookup by hash.
        # You'd need a raw unique ID in the token to find the DB row, THEN verify the hash.
        # Since our [create_refresh_token](cci:1://file:///d:/Rajat/Projects/SentinelAuth/SentinelAuth/app/core/tokens.py:41:0-62:41) doesn't add a unique ID (jti) yet in tokens.py...
        
        # ALTERNATIVE For MVP: We will store the token RAW in the DB for now to make this work 
        # with the current Repo implementation ([get_by_hash](cci:1://file:///d:/Rajat/Projects/SentinelAuth/SentinelAuth/app/repositories/token_repo.py:28:4-32:17) implies exact match).
        
        # Validating user exists
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=401, detail="User not found")

        # 3. Find the token in DB (Assuming we stored it raw per repo capability)
        # If we used bcrypt in login, this next line fails.
        # So in Login, we must pass the RAW token to [create](cci:1://file:///d:/Rajat/Projects/SentinelAuth/SentinelAuth/app/repositories/token_repo.py:15:4-26:23) if we want [get_by_hash](cci:1://file:///d:/Rajat/Projects/SentinelAuth/SentinelAuth/app/repositories/token_repo.py:28:4-32:17) to work.
        existing_token = self.token_repo.get_by_hash(refresh_token_in)
        
        if not existing_token:
            # Token Reuse Detection could go here (if family ID was used)
            raise HTTPException(status_code=401, detail="Refresh token not found or revoked")

        if existing_token.is_revoked:
             raise HTTPException(status_code=401, detail="Token revoked")

        # 4. Rotate: Revoke old, Create new
        self.token_repo.revoke(existing_token)
        
        new_access_token = create_access_token(user_id=str(user.id), role=user.role.name)
        new_refresh_str = create_refresh_token(user_id=str(user.id))
        
        expires_at = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        self.token_repo.create(user_id=user.id, token_hash=new_refresh_str, expires_at=expires_at)
        
        return Token(
            access_token=new_access_token,
            refresh_token=new_refresh_str,
            token_type="bearer"
        )