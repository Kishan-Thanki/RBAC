"""
Role schemas for request and response models.
"""

from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from .permission import PermissionResponse


class RoleBase(BaseModel):
    """Base role schema."""
    
    name: str
    description: Optional[str] = None


class RoleCreate(RoleBase):
    """Schema for creating a role."""
    pass


class RoleUpdate(BaseModel):
    """Schema for updating a role."""
    
    name: Optional[str] = None
    description: Optional[str] = None


class RoleResponse(RoleBase):
    """Schema for role response."""
    
    id: int
    permissions: List[PermissionResponse] = []
    
    model_config = ConfigDict(from_attributes=True)


class RoleWithPermissions(BaseModel):
    """Schema for role with permission assignments."""
    
    role_id: int
    permission_ids: List[int] 