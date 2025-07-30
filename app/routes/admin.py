"""
Admin routes for managing users, roles, and permissions.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.models.user import User
from app.models.role import Role
from app.models.permission import Permission
from app.schemas.user import UserResponse, UserUpdate, UserWithRoles
from app.schemas.role import RoleCreate, RoleUpdate, RoleResponse, RoleWithPermissions
from app.schemas.permission import PermissionCreate, PermissionUpdate, PermissionResponse
from app.core.auth import get_current_superuser
from app.core.rbac import require_admin

router = APIRouter(prefix="/admin", tags=["admin"])


# User Management
@router.get("/users", response_model=List[UserResponse])
async def get_users(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_superuser),
    db: Session = Depends(get_db)
):
    """Get all users (admin only)."""
    users = db.query(User).offset(skip).limit(limit).all()
    return users


@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    current_user: User = Depends(get_current_superuser),
    db: Session = Depends(get_db)
):
    """Get a specific user by ID (admin only)."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/users/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_update: UserUpdate,
    current_user: User = Depends(get_current_superuser),
    db: Session = Depends(get_db)
):
    """Update a user (admin only)."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    update_data = user_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)
    
    db.commit()
    db.refresh(user)
    return user


@router.post("/users/{user_id}/roles")
async def assign_roles_to_user(
    user_id: int,
    user_roles: UserWithRoles,
    current_user: User = Depends(get_current_superuser),
    db: Session = Depends(get_db)
):
    """Assign roles to a user (admin only)."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    roles = db.query(Role).filter(Role.id.in_(user_roles.role_ids)).all()
    user.roles = roles
    db.commit()
    
    return {"message": "Roles assigned successfully"}


# Role Management
@router.get("/roles", response_model=List[RoleResponse])
async def get_roles(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_superuser),
    db: Session = Depends(get_db)
):
    """Get all roles (admin only)."""
    roles = db.query(Role).offset(skip).limit(limit).all()
    return roles


@router.post("/roles", response_model=RoleResponse)
async def create_role(
    role_data: RoleCreate,
    current_user: User = Depends(get_current_superuser),
    db: Session = Depends(get_db)
):
    """Create a new role (admin only)."""
    existing_role = db.query(Role).filter(Role.name == role_data.name).first()
    if existing_role:
        raise HTTPException(status_code=400, detail="Role name already exists")
    
    db_role = Role(**role_data.dict())
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role


@router.put("/roles/{role_id}", response_model=RoleResponse)
async def update_role(
    role_id: int,
    role_update: RoleUpdate,
    current_user: User = Depends(get_current_superuser),
    db: Session = Depends(get_db)
):
    """Update a role (admin only)."""
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    
    update_data = role_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(role, field, value)
    
    db.commit()
    db.refresh(role)
    return role


@router.delete("/roles/{role_id}")
async def delete_role(
    role_id: int,
    current_user: User = Depends(get_current_superuser),
    db: Session = Depends(get_db)
):
    """Delete a role (admin only)."""
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    
    db.delete(role)
    db.commit()
    return {"message": "Role deleted successfully"}


@router.post("/roles/{role_id}/permissions")
async def assign_permissions_to_role(
    role_id: int,
    role_permissions: RoleWithPermissions,
    current_user: User = Depends(get_current_superuser),
    db: Session = Depends(get_db)
):
    """Assign permissions to a role (admin only)."""
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    
    permissions = db.query(Permission).filter(Permission.id.in_(role_permissions.permission_ids)).all()
    role.permissions = permissions
    db.commit()
    
    return {"message": "Permissions assigned successfully"}


# Permission Management
@router.get("/permissions", response_model=List[PermissionResponse])
async def get_permissions(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_superuser),
    db: Session = Depends(get_db)
):
    """Get all permissions (admin only)."""
    permissions = db.query(Permission).offset(skip).limit(limit).all()
    return permissions


@router.post("/permissions", response_model=PermissionResponse)
async def create_permission(
    permission_data: PermissionCreate,
    current_user: User = Depends(get_current_superuser),
    db: Session = Depends(get_db)
):
    """Create a new permission (admin only)."""
    existing_permission = db.query(Permission).filter(Permission.name == permission_data.name).first()
    if existing_permission:
        raise HTTPException(status_code=400, detail="Permission name already exists")
    
    db_permission = Permission(**permission_data.dict())
    db.add(db_permission)
    db.commit()
    db.refresh(db_permission)
    return db_permission


@router.put("/permissions/{permission_id}", response_model=PermissionResponse)
async def update_permission(
    permission_id: int,
    permission_update: PermissionUpdate,
    current_user: User = Depends(get_current_superuser),
    db: Session = Depends(get_db)
):
    """Update a permission (admin only)."""
    permission = db.query(Permission).filter(Permission.id == permission_id).first()
    if not permission:
        raise HTTPException(status_code=404, detail="Permission not found")
    
    update_data = permission_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(permission, field, value)
    
    db.commit()
    db.refresh(permission)
    return permission


@router.delete("/permissions/{permission_id}")
async def delete_permission(
    permission_id: int,
    current_user: User = Depends(get_current_superuser),
    db: Session = Depends(get_db)
):
    """Delete a permission (admin only)."""
    permission = db.query(Permission).filter(Permission.id == permission_id).first()
    if not permission:
        raise HTTPException(status_code=404, detail="Permission not found")
    
    db.delete(permission)
    db.commit()
    return {"message": "Permission deleted successfully"} 