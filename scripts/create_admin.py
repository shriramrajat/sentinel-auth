"""
Create Admin Script.

This script creates a default superuser if one doesn't exist.
It ensures that an 'admin' role exists and assigns it to the user.
"""

import sys
import os
import logging

# Add project root to python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.session import SessionLocal
from app.db.models.user import User
from app.db.models.role import Role
from app.core.security import get_password_hash

# Simple logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_admin() -> None:
    db = SessionLocal()
    try:
        # 1. Check/Get Admin Role
        admin_role = db.query(Role).filter(Role.name == "admin").first()
        if not admin_role:
            logger.error("'admin' role not found! Run scripts/init_db.py first.")
            return

        # 2. Check if Admin User Exists
        username = "admin"
        email = "admin@example.com"
        password = "admin"
        
        user = db.query(User).filter(User.username == username).first()
        if user:
            logger.info(f"User '{username}' already exists. Skipping.")
            return

        # 3. Create Admin User
        logger.info(f"Creating user '{username}' with role 'admin'...")
        
        new_user = User(
            username=username,
            email=email,
            password_hash=get_password_hash(password),
            role_id=admin_role.id,
            is_active=True
        )
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        logger.info("Admin user created successfully!")
        logger.info(f"USERNAME: {username}")
        logger.info(f"EMAIL:    {email}")
        logger.info(f"PASSWORD: {password}") 
        logger.warning("PLEASE CHANGE THIS PASSWORD IMMEDIATELY!")

    except Exception as e:
        logger.error(f"Error creating admin: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_admin()
