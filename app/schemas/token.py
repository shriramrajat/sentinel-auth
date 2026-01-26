"""
Token Schemas.
"""

from typing import Optional
from pydantic import BaseModel

class TokenResponse(BaseModel):
    """
    Schema for returning tokens to the client.
    """
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int  # Seconds

class TokenPayload(BaseModel):
    """
    Schema for the JWT payload content.
    """
    sub: Optional[str] = None
    type: Optional[str] = None
    role: Optional[str] = None
    exp: Optional[int] = None
