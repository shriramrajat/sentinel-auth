"""
Security utilities.

This module handles password hashing, verification, and JWT operations.
"""

from datetime import datetime, timedelta
from typing import Any, Union, Dict, Optional
from jose import jwt, JWTError
from passlib.context import CryptContext

from app.core.config import settings
from app.utils.logger import logger

# Password hashing configuration
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password.
    
    Args:
        plain_password: The password provided by the user
        hashed_password: The hashed password stored in the database
        
    Returns:
        bool: True if password matches, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Hash a password using bcrypt.
    
    Args:
        password: The plain password to hash
        
    Returns:
        str: Hashed password
    """
    return pwd_context.hash(password)


def create_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT token (access or refresh).
    
    Args:
        data: Payload data (claims)
        expires_delta: Optional custom expiration time
        
    Returns:
        str: Encoded JWT token string
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        # Default fallback (should usually be provided by caller)
        expire = datetime.utcnow() + timedelta(minutes=15)
        
    to_encode.update({"exp": expire})
    
    # Add issued at time if not present
    if "iat" not in to_encode:
        to_encode["iat"] = datetime.utcnow()
        
    try:
        encoded_jwt = jwt.encode(
            to_encode, 
            settings.SECRET_KEY, 
            algorithm=settings.ALGORITHM
        )
        return encoded_jwt
    except Exception as e:
        logger.error(f"Error creating token: {e}")
        raise


def decode_token(token: str) -> Dict[str, Any]:
    """
    Decode and verify a JWT token.
    
    Args:
        token: The encoded JWT token string
        
    Returns:
        Dict[str, Any]: Decoded payload if valid
        
    Raises:
        JWTError: If token is invalid or expired
    """
    try:
        payload = jwt.decode(
            token, 
            settings.SECRET_KEY, 
            algorithms=[settings.ALGORITHM]
        )
        return payload
    except JWTError as e:
        # Caller should handle the specific error (expired, invalid signature, etc.)
        raise e
