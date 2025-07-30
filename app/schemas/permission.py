"""
Permission schemas for request and response models.
"""

from pydantic import BaseModel, ConfigDict
from typing import Optional


class PermissionBase(BaseModel):
    """Base permission schema."""
    
    name: str
    description: Optional[str] = None


class PermissionCreate(PermissionBase):
    """Schema for creating a permission."""
    pass


class PermissionUpdate(BaseModel):
    """Schema for updating a permission."""
    
    name: Optional[str] = None
    description: Optional[str] = None


class PermissionResponse(PermissionBase):
    """Schema for permission response."""
    
    id: int
    
    model_config = ConfigDict(from_attributes=True) 