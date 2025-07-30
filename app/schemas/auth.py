"""
Authentication schemas for request and response models.
"""

from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional


class UserRegister(BaseModel):
    """Schema for user registration."""
    
    email: EmailStr
    username: str
    password: str


class UserLogin(BaseModel):
    """Schema for user login."""
    
    email: EmailStr
    password: str


class Token(BaseModel):
    """Schema for JWT token response."""
    
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Schema for token payload data."""
    
    user_id: Optional[int] = None
    email: Optional[str] = None


class RefreshToken(BaseModel):
    """Schema for refresh token request."""
    
    refresh_token: str


class UserResponse(BaseModel):
    """Schema for user response (without password)."""
    
    id: int
    email: str
    username: str
    is_active: bool
    is_superuser: bool
    
    model_config = ConfigDict(from_attributes=True) 