#!/usr/bin/env python3
"""
Simple test script to check if the RBAC system is working.
This script tests the main components to make sure everything is set up correctly.
"""

import sys
import os
from pathlib import Path

# Add the app directory to the Python path
sys.path.insert(0, str(Path(__file__).parent / "app"))


def test_imports():
    """Test if we can import all the modules we need."""
    print("Testing imports...")
    
    try:
        from app.core.config import settings
        print("Config imported")
    except ImportError as e:
        print(f"Config import failed: {e}")
        return False
    
    try:
        from app.core.security import get_password_hash, verify_password
        print("Security functions imported")
    except ImportError as e:
        print(f"Security import failed: {e}")
        return False
    
    try:
        from app.core.auth import get_current_user
        print("Auth functions imported")
    except ImportError as e:
        print(f"Auth import failed: {e}")
        return False
    
    try:
        from app.models.user import User
        from app.models.role import Role
        from app.models.permission import Permission
        print("Models imported")
    except ImportError as e:
        print(f"Models import failed: {e}")
        return False
    
    try:
        from app.db.base import engine, SessionLocal
        print("Database imported")
    except ImportError as e:
        print(f"Database import failed: {e}")
        return False
    
    return True


def test_password_hashing():
    """Test if password hashing works correctly."""
    print("\nTesting password hashing...")
    
    try:
        from app.core.security import get_password_hash, verify_password
        
        # Test password hashing
        password = "test_password_123"
        hashed = get_password_hash(password)
        
        if hashed != password:  # Make sure it's actually hashed
            print("Password hashing works")
        else:
            print("Password hashing failed - password not hashed")
            return False
        
        # Test password verification
        if verify_password(password, hashed):
            print("Password verification works")
        else:
            print("Password verification failed")
            return False
        
        # Test wrong password
        if not verify_password("wrong_password", hashed):
            print("Wrong password correctly rejected")
        else:
            print("Wrong password incorrectly accepted")
            return False
        
        return True
        
    except Exception as e:
        print(f"Password hashing test failed: {e}")
        return False


def test_jwt_tokens():
    """Test if JWT token creation and verification works."""
    print("\nTesting JWT tokens...")
    
    try:
        from app.core.security import create_access_token, verify_token
        
        # Test token creation
        data = {"user_id": 1, "email": "test@example.com"}
        token = create_access_token(data=data)
        
        if token:
            print("Token creation works")
        else:
            print("Token creation failed")
            return False
        
        # Test token verification
        payload = verify_token(token)
        if payload and payload.get("user_id") == 1:
            print("Token verification works")
        else:
            print("Token verification failed")
            return False
        
        return True
        
    except Exception as e:
        print(f"JWT token test failed: {e}")
        return False


def test_database_connection():
    """Test if we can connect to the database."""
    print("\nTesting database connection...")
    
    try:
        from app.db.base import engine, SessionLocal
        from app.models.base import Base
        
        # Test if we can create tables
        Base.metadata.create_all(bind=engine)
        print("Database tables created")
        
        # Test if we can create a session
        db = SessionLocal()
        db.close()
        print("Database session works")
        
        return True
        
    except Exception as e:
        print(f"Database connection failed: {e}")
        return False


def test_rbac_logic():
    """Test if the RBAC logic works correctly."""
    print("\nTesting RBAC logic...")
    
    try:
        from app.db.base import SessionLocal
        from app.models.user import User
        from app.models.role import Role
        from app.models.permission import Permission
        from app.core.security import get_password_hash
        
        db = SessionLocal()
        
        # Clean up any existing test data first
        existing_user = db.query(User).filter(User.email == "test_rbac@example.com").first()
        if existing_user:
            db.delete(existing_user)
            db.commit()
        
        existing_role = db.query(Role).filter(Role.name == "test_role_rbac").first()
        if existing_role:
            db.delete(existing_role)
            db.commit()
        
        existing_permission = db.query(Permission).filter(Permission.name == "test_permission_rbac").first()
        if existing_permission:
            db.delete(existing_permission)
            db.commit()
        
        # Create a test permission
        test_permission = Permission(name="test_permission_rbac", description="Test permission for RBAC")
        db.add(test_permission)
        db.flush()
        
        # Create a test role
        test_role = Role(name="test_role_rbac", description="Test role for RBAC")
        test_role.permissions.append(test_permission)
        db.add(test_role)
        db.flush()
        
        # Create a test user with unique email
        test_user = User(
            email="test_rbac@example.com",
            username="testuser_rbac",
            hashed_password=get_password_hash("testpass")
        )
        test_user.roles.append(test_role)
        db.add(test_user)
        db.flush()
        
        # Test permission checking
        if test_user.has_permission("test_permission_rbac"):
            print("Permission checking works")
        else:
            print("Permission checking failed")
            db.rollback()
            db.close()
            return False
        
        # Test role checking
        if test_user.has_role("test_role_rbac"):
            print("Role checking works")
        else:
            print("Role checking failed")
            db.rollback()
            db.close()
            return False
        
        # Clean up
        db.delete(test_user)
        db.delete(test_role)
        db.delete(test_permission)
        db.commit()
        db.close()
        
        return True
        
    except Exception as e:
        print(f"RBAC logic test failed: {e}")
        return False


def test_configuration():
    """Test if the configuration is set up correctly."""
    print("\nTesting configuration...")
    
    try:
        from app.core.config import settings
        
        # Check if we have the required settings
        if settings.DATABASE_URL:
            print("Database URL configured")
        else:
            print("Database URL not configured")
            return False
        
        if settings.SECRET_KEY and settings.SECRET_KEY != "your-super-secret-key-change-this-in-production":
            print("Secret key configured")
        else:
            print("Using default secret key - change this in production")
        
        if settings.FIRST_ADMIN_EMAIL:
            print("Admin email configured")
        else:
            print("Admin email not configured")
            return False
        
        return True
        
    except Exception as e:
        print(f"Configuration test failed: {e}")
        return False


def main():
    """Run all the tests and show results."""
    print("RBAC System Test")
    print("=" * 40)
    
    tests = [
        ("Imports", test_imports),
        ("Password Hashing", test_password_hashing),
        ("JWT Tokens", test_jwt_tokens),
        ("Database Connection", test_database_connection),
        ("RBAC Logic", test_rbac_logic),
        ("Configuration", test_configuration),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n--- {test_name} ---")
        if test_func():
            passed += 1
        else:
            print(f"{test_name} failed")
    
    print("\n" + "=" * 40)
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("All tests passed! The RBAC system is ready to use.")
        return True
    else:
        print("Some tests failed. Please check the errors above.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 