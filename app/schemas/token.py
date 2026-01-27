"""
Token Schemas.
"""

from typing import Optional
from pydantic import BaseModel

class Token(BaseModel):
    """
    Schema for returning tokens to the client.
    Matches the expectation in auth_service.py
    """
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class TokenPayload(BaseModel):
    """
    Schema for the JWT payload content.
    """
    sub: Optional[str] = None
    type: Optional[str] = None
    role: Optional[str] = None
    exp: Optional[int] = None