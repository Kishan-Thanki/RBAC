#!/usr/bin/env python3
"""
Startup script for the RBAC system.
This script sets up the database and starts the web server.
"""

import os
import sys
from pathlib import Path

# Add the app directory to Python path so we can import our modules
sys.path.insert(0, str(Path(__file__).parent / "app"))

from app.init_db import init_db
from app.main import app
import uvicorn


def main():
    """Main function that starts everything up."""
    print("Starting RBAC System...")
    
    # Set up the database with initial data
    print("Setting up database...")
    try:
        init_db()
        print("Database is ready!")
    except Exception as e:
        print(f"Error setting up database: {e}")
        return
    
    # Start the web server
    print("Starting web server...")
    print("API Documentation: http://localhost:8000/docs")
    print("ReDoc: http://localhost:8000/redoc")
    print("Default admin login:")
    print(f"   Email: {os.getenv('FIRST_ADMIN_EMAIL', 'admin@example.com')}")
    print(f"   Password: {os.getenv('FIRST_ADMIN_PASSWORD', 'admin123')}")
    print("\n" + "="*50)
    
    # Start the server with uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )


if __name__ == "__main__":
    main() 