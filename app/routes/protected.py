"""
Protected resource routes demonstrating RBAC permission checking.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from app.models.user import User
from app.core.auth import get_current_active_user
from app.core.rbac import (
    require_permission_dependency,
    require_role_dependency,
    get_user_permissions
)

router = APIRouter(prefix="/protected", tags=["protected"])


@router.get("/user-dashboard")
async def user_dashboard(current_user: User = Depends(get_current_active_user)):
    """
    User dashboard - accessible to all authenticated users.
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        dict: User dashboard data
    """
    return {
        "message": "Welcome to your dashboard!",
        "user": {
            "id": current_user.id,
            "username": current_user.username,
            "email": current_user.email,
            "roles": [role.name for role in current_user.roles],
            "permissions": list(current_user.permissions)
        }
    }


@router.get("/admin-only")
async def admin_only(current_user: User = Depends(require_permission_dependency("admin_access"))):
    """
    Admin only endpoint - requires admin_access permission.
    
    Args:
        current_user: Current authenticated user with admin access
        
    Returns:
        dict: Admin only data
    """
    return {
        "message": "Admin access granted!",
        "admin_data": "This is sensitive admin information",
        "user": current_user.username
    }


@router.get("/manage-users")
async def manage_users(current_user: User = Depends(require_permission_dependency("manage_users"))):
    """
    User management endpoint - requires manage_users permission.
    
    Args:
        current_user: Current authenticated user with user management permission
        
    Returns:
        dict: User management data
    """
    return {
        "message": "User management access granted!",
        "management_data": "User management interface data",
        "user": current_user.username
    }


@router.get("/manage-roles")
async def manage_roles(current_user: User = Depends(require_permission_dependency("manage_roles"))):
    """
    Role management endpoint - requires manage_roles permission.
    
    Args:
        current_user: Current authenticated user with role management permission
        
    Returns:
        dict: Role management data
    """
    return {
        "message": "Role management access granted!",
        "management_data": "Role management interface data",
        "user": current_user.username
    }


@router.get("/manage-permissions")
async def manage_permissions(current_user: User = Depends(require_permission_dependency("manage_permissions"))):
    """
    Permission management endpoint - requires manage_permissions permission.
    
    Args:
        current_user: Current authenticated user with permission management permission
        
    Returns:
        dict: Permission management data
    """
    return {
        "message": "Permission management access granted!",
        "management_data": "Permission management interface data",
        "user": current_user.username
    }


@router.get("/moderator-only")
async def moderator_only(current_user: User = Depends(require_role_dependency("moderator"))):
    """
    Moderator only endpoint - requires moderator role.
    
    Args:
        current_user: Current authenticated user with moderator role
        
    Returns:
        dict: Moderator only data
    """
    return {
        "message": "Moderator access granted!",
        "moderator_data": "This is moderator-specific information",
        "user": current_user.username
    }


@router.get("/my-permissions")
async def get_my_permissions(permissions: list = Depends(get_user_permissions)):
    """
    Get current user's permissions.
    
    Args:
        permissions: List of user permissions
        
    Returns:
        dict: User permissions data
    """
    return {
        "message": "Your permissions",
        "permissions": permissions,
        "permission_count": len(permissions)
    }


@router.get("/custom-permission/{permission_name}")
async def custom_permission_endpoint(
    permission_name: str,
    current_user: User = Depends(get_current_active_user)
):
    """
    Custom permission endpoint - requires the specified permission.
    
    Args:
        permission_name: Name of the permission required
        current_user: Current authenticated user with the required permission
        
    Returns:
        dict: Custom permission data
    """
    # Check if user has the required permission
    if not current_user.has_permission(permission_name):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Permission '{permission_name}' required"
        )
    
    return {
        "message": f"Access granted for permission: {permission_name}",
        "permission": permission_name,
        "user": current_user.username,
        "data": f"Data specific to {permission_name} permission"
    } 