"""
User Schemas.
"""

from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, EmailStr, ConfigDict, Field
from typing import Optional

from app.schemas.role import RoleResponse

class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr

class UserCreate(UserBase):
    """
    Schema for User creation (Signup).
    """
    password: str = Field(..., min_length=8, description="Plain text password")

class UserUpdate(BaseModel):
    """
    Schema for updating user details.
    All fields are optional.
    """
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=8)
    first_name: Optional[str] = None
    last_name: Optional[str] = None

class UserResponse(UserBase):
    """
    Schema for User response.
    excludes password_hash.
    """
    id: UUID
    is_active: bool
    created_at: datetime
    role: RoleResponse

    model_config = ConfigDict(from_attributes=True)
