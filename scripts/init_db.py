"""
Database initialization script.

This script initializes the database by:
1. Creating all tables (if they don't exist)
2. Creating default roles (admin, user)
"""

import sys
import os
from sqlalchemy.orm import Session

# Add project root to python path so we can import app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.session import engine, SessionLocal
from app.db.base import Base
from app.db.models.role import Role
from app.utils.logger import logger

def init_db(db: Session) -> None:
    """
    Initialize database with default data.
    """
    # 1. Create Tables
    # Note: In production, we use Alembic migrations. 
    # This is a fallback/dev convenience to ensure schema exists.
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created/verified.")

    # 2. Create Default Roles
    roles = ["admin", "user"]
    for role_name in roles:
        role = db.query(Role).filter(Role.name == role_name).first()
        if not role:
            role = Role(name=role_name, description=f"Default {role_name} role")
            db.add(role)
            logger.info(f"Created role: {role_name}")
        else:
            logger.info(f"Role exists: {role_name}")
    
    db.commit()

def main() -> None:
    logger.info("Initializing database...")
    db = SessionLocal()
    try:
        init_db(db)
        logger.info("Database initialization complete!")
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    main()
