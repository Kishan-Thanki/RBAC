"""
Settings and configuration for our application.
This file handles all the settings that can be changed.
"""

from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import validator, ConfigDict
import os


class Settings(BaseSettings):
    """All the settings our application needs."""
    
    # Database connection
    DATABASE_URL: str = "sqlite:///./rbac.db"
    
    # JWT token settings
    SECRET_KEY: str = "your-super-secret-key-change-this-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # Application settings
    DEBUG: bool = True
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "RBAC System"
    
    # Which websites can access our API
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8080"]
    
    # Default admin user
    FIRST_ADMIN_EMAIL: str = "admin@example.com"
    FIRST_ADMIN_PASSWORD: str = "admin123"
    
    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v):
        """Convert CORS origins from string to list if needed."""
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)
    
    @validator("DATABASE_URL", pre=True)
    def validate_database_url(cls, v):
        """Make sure we have a database URL, use SQLite if none provided."""
        if not v:
            return "sqlite:///./rbac.db"
        return v
    
    model_config = ConfigDict(env_file=".env", case_sensitive=True)


# Create a global settings object that we can use everywhere
settings = Settings() 