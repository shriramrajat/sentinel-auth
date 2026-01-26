"""
Role Schemas.
"""

from datetime import datetime
from pydantic import BaseModel, ConfigDict

class RoleBase(BaseModel):
    name: str
    description: str | None = None

class RoleResponse(RoleBase):
    """
    Schema for Role response.
    """
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
