"""
Security utilities.

This module handles password hashing, verification, and JWT operations.
"""

from datetime import datetime, timedelta
from typing import Any, Union
from passlib.context import CryptContext

from app.core.config import settings

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
