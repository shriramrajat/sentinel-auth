import pytest
from typing import Generator
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.base import Base
from app.api.deps import get_db
from app.main import app

# Use SQLite for testing (fast, in-memory)
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="module")
def db_session():
    # Create the database tables
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    
    # Pre-seed roles since they are required for user creation
    from app.db.models.role import Role
    if not db.query(Role).first():
        db.add(Role(name="user", description="Normal User"))
        db.add(Role(name="admin", description="Admin User"))
        db.commit()

    try:
        yield db
    finally:
        db.close()
        # Drop tables after tests (optional, but good for cleanup)
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="module")
def client(db_session) -> Generator:
    # Override the get_db dependency to use our test database
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
