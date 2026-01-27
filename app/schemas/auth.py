"""
Auth Schemas.
"""

from pydantic import BaseModel, EmailStr, Field

class LoginRequest(BaseModel):
    """
    Schema for Login request.
    Can accept username OR email eventually, but for now we'll support one or both.
    Typically OAuth2PasswordRequestForm is used in FastAPI, but a JSON body is often preferred for REST.
    We will strictly use username/password for simplicity or support email.
    Let's stick to username for now based on spec "username/email".
    """
    username: str
    password: str

class RefreshTokenRequest(BaseModel):
    refresh_token: str