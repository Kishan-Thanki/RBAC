"""
Permission model for RBAC system.
"""

from sqlalchemy import Column, String, Text
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class Permission(BaseModel):
    """
    Permission model representing system permissions.
    
    Attributes:
        name: Unique permission name (e.g., 'read_users', 'create_roles')
        description: Human-readable description of the permission
    """
    
    __tablename__ = "permissions"
    
    name = Column(String(100), unique=True, index=True, nullable=False)
    description = Column(Text, nullable=True)
    
    # Many-to-many relationship with roles
    roles = relationship("Role", secondary="role_permissions", back_populates="permissions")
    
    def __repr__(self):
        return f"<Permission(id={self.id}, name='{self.name}')>" 