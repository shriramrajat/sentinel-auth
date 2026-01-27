from typing import Generator
from app.db.session import SessionLocal

def get_db() -> Generator:
    """
    Dependency that creates a new database session for a request
    and closes it after the request is finished.
    """
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()