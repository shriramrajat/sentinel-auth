# Import the actual Base class first
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

# Import all models here so Alembic can detect them
from app.db.models.user import User
from app.db.models.role import Role
from app.db.models.refresh_token import RefreshToken
from app.db.models.request_log import RequestLog
