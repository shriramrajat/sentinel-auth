"""
SQLAlchemy declarative base.

This module provides the base class for all ORM models.
All models should inherit from this Base class.
"""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """
    Base class for all database models.
    
    All ORM models in the application should inherit from this class.
    SQLAlchemy will use this to track all models and generate migrations.
    """
    pass
