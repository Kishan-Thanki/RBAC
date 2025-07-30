"""
User schemas for request and response models.
"""

from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional, List
from .role import RoleResponse


class UserBase(BaseModel):
    """Base user schema."""
    
    email: EmailStr
    username: str


class UserCreate(UserBase):
    """Schema for creating a user."""
    
    password: str


class UserUpdate(BaseModel):
    """Schema for updating a user."""
    
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None


class UserResponse(UserBase):
    """Schema for user response."""
    
    id: int
    is_active: bool
    is_superuser: bool
    roles: List[RoleResponse] = []
    
    model_config = ConfigDict(from_attributes=True)


class UserWithRoles(BaseModel):
    """Schema for user with role assignments."""
    
    user_id: int
    role_ids: List[int] 