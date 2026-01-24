"""
Database session management.

This module handles SQLAlchemy engine creation, session factory,
and provides a dependency for FastAPI routes to get database sessions.
"""

from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.core.config import settings


# Create SQLAlchemy engine
# echo=True will log all SQL statements (useful for debugging)
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,  # Log SQL in debug mode
    pool_pre_ping=True,   # Verify connections before using them
    pool_size=5,          # Number of connections to maintain
    max_overflow=10       # Max connections beyond pool_size
)

# Create session factory
# autocommit=False: We manually control transactions
# autoflush=False: We manually control when to flush changes
# bind=engine: Bind this session factory to our engine
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def get_db() -> Generator[Session, None, None]:
    """
    FastAPI dependency that provides a database session.
    
    This function creates a new database session for each request
    and ensures it's properly closed after the request completes.
    
    Usage in FastAPI routes:
        @app.get("/users")
        def get_users(db: Session = Depends(get_db)):
            # Use db here
            pass
    
    Yields:
        Session: SQLAlchemy database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
