"""
User model - this represents a user in our system.
Each user has an email, username, password, and can have roles.
"""

from sqlalchemy import Column, String, Boolean, Table, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

# This table connects users to their roles
# A user can have many roles, and a role can have many users
user_roles = Table(
    'user_roles',
    BaseModel.metadata,
    Column('user_id', ForeignKey('users.id'), primary_key=True),
    Column('role_id', ForeignKey('roles.id'), primary_key=True)
)


class User(BaseModel):
    """
    A user in our system.
    
    Each user has:
    - email: their email address (must be unique)
    - username: their username (must be unique)
    - hashed_password: their password (stored securely)
    - is_active: whether their account is active
    - is_superuser: whether they have admin powers
    - roles: what roles they have (admin, user, etc.)
    """
    
    __tablename__ = "users"
    
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    
    # Connect users to their roles
    roles = relationship("Role", secondary=user_roles, back_populates="users")
    
    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', username='{self.username}')>"
    
    @property
    def permissions(self):
        """
        Get all the permissions this user has through their roles.
        
        For example, if a user has the "admin" role, and that role
        has "manage_users" permission, then this user can manage users.
        """
        permissions = set()
        for role in self.roles:
            for permission in role.permissions:
                permissions.add(permission.name)
        return permissions
    
    def has_permission(self, permission_name: str) -> bool:
        """
        Check if this user has a specific permission.
        
        Args:
            permission_name: the permission we're checking for
            
        Returns:
            True if the user has this permission, False otherwise
        """
        return permission_name in self.permissions
    
    def has_role(self, role_name: str) -> bool:
        """
        Check if this user has a specific role.
        
        Args:
            role_name: the role we're checking for
            
        Returns:
            True if the user has this role, False otherwise
        """
        return any(role.name == role_name for role in self.roles) 