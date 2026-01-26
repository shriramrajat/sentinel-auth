"""
Verify Patterns Layer (Schemas & Repositories).
"""

import sys
import os
from sqlalchemy.orm import Session

# Add project root to python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.session import SessionLocal
from app.repositories import UserRepository, RoleRepository, TokenRepository
from app.schemas import UserCreate, LoginRequest

def test_imports():
    print("Testing Repository Instantiation...")
    db = SessionLocal()
    try:
        user_repo = UserRepository(db)
        role_repo = RoleRepository(db)
        token_repo = TokenRepository(db)
        print("✅ Repositories instantiated successfully.")
        
        # Test basic Schema validation
        print("Testing Schema Validation...")
        user_in = UserCreate(username="testuser", email="test@example.com", password="password123")
        print(f"✅ UserCreate Schema Valid: {user_in.username}")
        
        login_req = LoginRequest(username="admin", password="password")
        print(f"✅ LoginRequest Schema Valid: {login_req.username}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    test_imports()
