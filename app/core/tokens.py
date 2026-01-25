"""
Token Lifecycle Management.

This module handles the creation of specific token types (access/refresh)
and defines their expiration policies.
"""

from datetime import timedelta
from typing import Dict, Any

from app.core.config import settings
from app.core.security import create_token
from app.core.constants import TOKEN_TYPE_ACCESS, TOKEN_TYPE_REFRESH

def create_access_token(user_id: str, role: str) -> str:
    """
    Create a short-lived access token.
    
    Payload includes:
    - sub (subject): user_id
    - type: "access"
    - role: user role
    
    Args:
        user_id: The UUID string of the user
        role: The role name of the user
        
    Returns:
        str: Encoded JWT access token
    """
    expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    payload = {
        "sub": str(user_id),
        "type": TOKEN_TYPE_ACCESS,
        "role": role
    }
    
    return create_token(payload, expires)


def create_refresh_token(user_id: str) -> str:
    """
    Create a long-lived refresh token.
    
    Payload includes:
    - sub (subject): user_id
    - type: "refresh"
    
    Args:
        user_id: The UUID string of the user
        
    Returns:
        str: Encoded JWT refresh token
    """
    expires = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    
    payload = {
        "sub": str(user_id),
        "type": TOKEN_TYPE_REFRESH
    }
    
    return create_token(payload, expires)
