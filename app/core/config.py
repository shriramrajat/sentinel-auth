"""
Application configuration and settings.

This module handles loading environment variables and providing
a centralized settings object for the entire application.
"""

from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    
    Uses Pydantic BaseSettings to automatically load and validate
    environment variables. Values can be overridden via .env file.
    """
    
    # Database Configuration
    DATABASE_URL: str
    
    # Security & JWT Configuration
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    
    # Token Expiration Settings
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # Application Settings
    PROJECT_NAME: str = "SentinelAuth"
    VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # API Configuration
    API_V1_PREFIX: str = "/api/v1"
    
    # CORS Settings
    ALLOWED_ORIGINS: str = "http://localhost:3000,http://localhost:8000"
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"  # Ignore extra env vars not defined here
    )
    
    @property
    def allowed_origins_list(self) -> List[str]:
        """
        Convert comma-separated ALLOWED_ORIGINS string to list.
        
        Returns:
            List of allowed CORS origins
        """
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]


# Global settings instance
# This will be imported throughout the application
settings = Settings()
