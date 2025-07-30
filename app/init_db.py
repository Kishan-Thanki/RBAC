"""
Set up the database with some default data.
This creates the initial roles, permissions, and admin user.
"""

from sqlalchemy.orm import Session
from app.db.base import SessionLocal
from app.models.user import User
from app.models.role import Role
from app.models.permission import Permission
from app.core.security import get_password_hash
from app.core.config import settings


def init_db():
    """Create the initial database with default roles, permissions, and admin user."""
    db = SessionLocal()
    
    try:
        # Create some basic permissions that users can have
        permissions = [
            {"name": "admin_access", "description": "Full administrative access"},
            {"name": "manage_users", "description": "Manage user accounts"},
            {"name": "manage_roles", "description": "Manage roles and role assignments"},
            {"name": "manage_permissions", "description": "Manage permissions"},
            {"name": "read_users", "description": "Read user information"},
            {"name": "create_users", "description": "Create new users"},
            {"name": "update_users", "description": "Update user information"},
            {"name": "delete_users", "description": "Delete users"},
            {"name": "read_roles", "description": "Read role information"},
            {"name": "create_roles", "description": "Create new roles"},
            {"name": "update_roles", "description": "Update role information"},
            {"name": "delete_roles", "description": "Delete roles"},
            {"name": "read_permissions", "description": "Read permission information"},
            {"name": "create_permissions", "description": "Create new permissions"},
            {"name": "update_permissions", "description": "Update permission information"},
            {"name": "delete_permissions", "description": "Delete permissions"},
            {"name": "moderate_content", "description": "Moderate user content"},
            {"name": "view_reports", "description": "View system reports"},
            {"name": "export_data", "description": "Export system data"},
        ]
        
        # Add each permission to the database if it doesn't exist
        for perm_data in permissions:
            existing_perm = db.query(Permission).filter(Permission.name == perm_data["name"]).first()
            if not existing_perm:
                permission = Permission(**perm_data)
                db.add(permission)
                print(f"Created permission: {perm_data['name']}")
        
        db.commit()
        
        # Create some basic roles that users can have
        roles = [
            {
                "name": "admin",
                "description": "System administrator with full access",
                "permissions": [
                    "admin_access", "manage_users", "manage_roles", "manage_permissions",
                    "read_users", "create_users", "update_users", "delete_users",
                    "read_roles", "create_roles", "update_roles", "delete_roles",
                    "read_permissions", "create_permissions", "update_permissions", "delete_permissions",
                    "moderate_content", "view_reports", "export_data"
                ]
            },
            {
                "name": "moderator",
                "description": "Content moderator with limited administrative access",
                "permissions": [
                    "read_users", "update_users", "moderate_content", "view_reports"
                ]
            },
            {
                "name": "user",
                "description": "Regular user with basic access",
                "permissions": []
            }
        ]
        
        # Add each role to the database if it doesn't exist
        for role_data in roles:
            existing_role = db.query(Role).filter(Role.name == role_data["name"]).first()
            if not existing_role:
                role = Role(
                    name=role_data["name"],
                    description=role_data["description"]
                )
                db.add(role)
                db.flush()  # This gets us the role ID
                
                # Give this role the permissions it should have
                for perm_name in role_data["permissions"]:
                    permission = db.query(Permission).filter(Permission.name == perm_name).first()
                    if permission:
                        role.permissions.append(permission)
                
                print(f"Created role: {role_data['name']}")
        
        db.commit()
        
        # Create the default admin user if it doesn't exist
        admin_user = db.query(User).filter(User.email == settings.FIRST_ADMIN_EMAIL).first()
        if not admin_user:
            admin_user = User(
                email=settings.FIRST_ADMIN_EMAIL,
                username="admin",
                hashed_password=get_password_hash(settings.FIRST_ADMIN_PASSWORD),
                is_active=True,
                is_superuser=True
            )
            db.add(admin_user)
            db.flush()
            
            # Give the admin user the admin role
            admin_role = db.query(Role).filter(Role.name == "admin").first()
            if admin_role:
                admin_user.roles.append(admin_role)
            
            print(f"Created admin user: {settings.FIRST_ADMIN_EMAIL}")
        
        db.commit()
        print("Database setup completed successfully!")
        
    except Exception as e:
        print(f"Error setting up database: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    init_db() 