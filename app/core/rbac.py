"""
RBAC (Role-Based Access Control) utilities.
This file has functions to check if users have the right permissions.
"""

from functools import wraps
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional, Callable, Any
from app.db.base import get_db
from app.models.user import User
from app.models.permission import Permission
from app.core.auth import get_current_active_user


def require_permission(permission_name: str):
    """
    A decorator that makes sure a user has a specific permission.
    
    You can use this like:
    @require_permission("read_data")
    def my_function():
        # only users with "read_data" permission can access this
        pass
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Get the current user from the function arguments
            current_user = kwargs.get('current_user')
            if not current_user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="You need to log in first"
                )
            
            # Check if the user has the permission we need
            if not current_user.has_permission(permission_name):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"You need the '{permission_name}' permission to do this"
                )
            
            return await func(*args, **kwargs)
        return wrapper
    return decorator


def require_role(role_name: str):
    """
    A decorator that makes sure a user has a specific role.
    
    You can use this like:
    @require_role("admin")
    def admin_function():
        # only admins can access this
        pass
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Get the current user from the function arguments
            current_user = kwargs.get('current_user')
            if not current_user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="You need to log in first"
                )
            
            # Check if the user has the role we need
            if not current_user.has_role(role_name):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"You need the '{role_name}' role to do this"
                )
            
            return await func(*args, **kwargs)
        return wrapper
    return decorator


def check_permission(permission_name: str, current_user: User) -> bool:
    """
    Check if a user has a specific permission.
    
    Args:
        permission_name: the permission we're checking for
        current_user: the user we're checking
        
    Returns:
        True if the user has the permission, False otherwise
    """
    return current_user.has_permission(permission_name)


def check_role(role_name: str, current_user: User) -> bool:
    """
    Check if a user has a specific role.
    
    Args:
        role_name: the role we're checking for
        current_user: the user we're checking
        
    Returns:
        True if the user has the role, False otherwise
    """
    return current_user.has_role(role_name)


def get_user_permissions(current_user: User = Depends(get_current_active_user)) -> List[str]:
    """
    Get all the permissions that a user has.
    
    Args:
        current_user: the user we're getting permissions for
        
    Returns:
        A list of permission names that the user has
    """
    return list(current_user.permissions)


def require_permission_dependency(permission_name: str):
    """
    A dependency that makes sure a user has a specific permission.
    
    You can use this in FastAPI routes like:
    def my_route(current_user: User = Depends(require_permission_dependency("read_data"))):
        # only users with "read_data" permission can access this route
        pass
    """
    def dependency(current_user: User = Depends(get_current_active_user)) -> User:
        if not current_user.has_permission(permission_name):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"You need the '{permission_name}' permission to do this"
            )
        return current_user
    return dependency


def require_role_dependency(role_name: str):
    """
    A dependency that makes sure a user has a specific role.
    
    You can use this in FastAPI routes like:
    def admin_route(current_user: User = Depends(require_role_dependency("admin"))):
        # only admins can access this route
        pass
    """
    def dependency(current_user: User = Depends(get_current_active_user)) -> User:
        if not current_user.has_role(role_name):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"You need the '{role_name}' role to do this"
            )
        return current_user
    return dependency


# Some common permission dependencies that you might use often
require_admin = require_permission_dependency("admin_access")
require_user_management = require_permission_dependency("manage_users")
require_role_management = require_permission_dependency("manage_roles")
require_permission_management = require_permission_dependency("manage_permissions") 