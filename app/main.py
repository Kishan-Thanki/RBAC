"""
Main file that starts the web application.
This is where everything comes together.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.core.config import settings
from app.routes import auth, admin, protected
from app.db.base import engine
from app.models import base, user, role, permission

# Create all the database tables when we start
# This makes sure all our tables exist
base.Base.metadata.create_all(bind=engine)

# Create our web application
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="A simple user management system with roles and permissions",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Allow other websites to talk to our API
# This is needed if your frontend is on a different domain
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api")
async def root():
    """Show basic info about our API."""
    return {
        "message": "Welcome to the RBAC System API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health")
async def health_check():
    """Check if our system is running properly."""
    return {"status": "healthy", "message": "RBAC System is running"}


# Serve our web dashboard files
# This makes the HTML/CSS/JS files available
app.mount("/static", StaticFiles(directory="static"), name="static")

# Add all our API routes
# These are the endpoints that handle different requests
app.include_router(auth.router, prefix=settings.API_V1_STR)
app.include_router(admin.router, prefix=settings.API_V1_STR)
app.include_router(protected.router, prefix=settings.API_V1_STR)

@app.get("/")
async def serve_dashboard():
    """Show the main web dashboard when someone visits the root URL."""
    return FileResponse("static/index.html")


# This runs when we start the file directly
if __name__ == "__main__":
    import uvicorn
    # Start the web server
    uvicorn.run(app, host="0.0.0.0", port=8000) 