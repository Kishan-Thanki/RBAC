"""
Role model for RBAC system with permission relationships.
"""

from sqlalchemy import Column, String, Text, Table, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

# Association table for role-permission many-to-many relationship
role_permissions = Table(
    'role_permissions',
    BaseModel.metadata,
    Column('role_id', ForeignKey('roles.id'), primary_key=True),
    Column('permission_id', ForeignKey('permissions.id'), primary_key=True)
)


class Role(BaseModel):
    """
    Role model representing user roles in the system.
    
    Attributes:
        name: Unique role name (e.g., 'admin', 'user', 'moderator')
        description: Human-readable description of the role
        permissions: Many-to-many relationship with permissions
    """
    
    __tablename__ = "roles"
    
    name = Column(String(100), unique=True, index=True, nullable=False)
    description = Column(Text, nullable=True)
    
    # Many-to-many relationship with permissions
    permissions = relationship("Permission", secondary=role_permissions, back_populates="roles")
    # Many-to-many relationship with users
    users = relationship("User", secondary="user_roles", back_populates="roles")
    
    def __repr__(self):
        return f"<Role(id={self.id}, name='{self.name}')>" 