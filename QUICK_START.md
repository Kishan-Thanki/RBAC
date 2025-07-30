# Quick Start Guide - RBAC System

## Get up and running in 5 minutes

This guide will help you get the RBAC system running quickly.

### What you need
- Python 3.8 or higher
- pip (comes with Python)

### Step 1: Get the code
```bash
# Download the project
git clone https://github.com/yourusername/rbac-system.git
cd rbac-system

# Or if you have a ZIP file, extract it and go to the folder
```

### Step 2: Set up the environment
```bash
# Create a virtual environment (keeps your project separate)
python3 -m venv venv

# Activate it
# On Mac/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### Step 3: Install dependencies
```bash
# Install all the Python packages we need
pip install -r requirements.txt
```

### Step 4: Configure the system
```bash
# Copy the example config file
cp env.example .env

# Edit the .env file if you want to change anything
# For now, the defaults should work fine
```

### Step 5: Start the system
```bash
# This will set up the database and start the server
python start.py
```

### Step 6: Check it out
Once it's running, you can visit:
- Main page: http://localhost:8000
- API docs: http://localhost:8000/docs
- Default login: admin@example.com / admin123

## What you get

### Basic features
- User login/logout - Users can sign in and out
- Role-based access - Different users have different permissions
- Admin panel - Manage users, roles, and permissions through a web interface
- API endpoints - Use it in your own applications

### Ready to use
- SQLAlchemy ORM - Works with databases
- Pydantic validation - Makes sure data is correct
- Testing suite - Tests to make sure everything works
- CORS support - Works with frontend applications
- Environment configuration - Easy to configure
- Security best practices - Safe to use

### Easy to integrate
- Modular design - Use only what you need
- Dependency injection - Easy to add permission checking
- RESTful API - Standard web API
- JavaScript examples - For frontend integration
- Python examples - For backend integration

## Using the dashboard

### Login
1. Go to http://localhost:8000
2. Use the default admin login:
   - Email: admin@example.com
   - Password: admin123

### Dashboard features
1. Dashboard - See your user info, roles, and permissions
2. User Management - Create and manage users
3. Role Management - Create and manage roles
4. Permission Management - Create and manage permissions
5. API Examples - See code examples for integration

## Integration examples

### Frontend (JavaScript)
```javascript
// Login
const login = async (email, password) => {
    const response = await fetch('/api/v1/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
    });
    const data = await response.json();
    localStorage.setItem('access_token', data.access_token);
    return data;
};

// Call protected API
const callProtectedAPI = async (endpoint) => {
    const token = localStorage.getItem('access_token');
    const response = await fetch(`/api/v1/protected/${endpoint}`, {
        headers: { 'Authorization': `Bearer ${token}` }
    });
    return response.json();
};
```

### Backend (FastAPI)
```python
from app.core.rbac import require_permission_dependency

@router.get("/my-protected-endpoint")
async def protected_endpoint(
    current_user: User = Depends(require_permission_dependency("read_data"))
):
    return {"message": "Access granted!"}
```

## Customization

### Adding new permissions
1. Go to the Permissions tab in the dashboard
2. Click "Create New Permission"
3. Enter permission name and description
4. Assign to roles as needed

### Creating custom roles
1. Go to the Roles tab in the dashboard
2. Click "Create New Role"
3. Enter role name and description
4. Assign permissions to the role

### Database configuration
For production, update the `DATABASE_URL` in your `.env` file:

```env
# PostgreSQL (recommended for production)
DATABASE_URL=postgresql://user:password@localhost/rbac_db

# SQLite (for development)
DATABASE_URL=sqlite:///./rbac.db
```

## Production deployment

1. Change default credentials in `.env`
2. Use PostgreSQL instead of SQLite
3. Set strong SECRET_KEY in `.env`
4. Configure CORS for your domain
5. Use HTTPS in production
6. Set up proper logging

## API reference

### Authentication endpoints
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login and get tokens
- `POST /api/v1/auth/refresh` - Refresh access token
- `POST /api/v1/auth/logout` - Logout

### Protected endpoints
- `GET /api/v1/protected/user-dashboard` - User dashboard
- `GET /api/v1/protected/admin-only` - Admin only (requires admin_access)
- `GET /api/v1/protected/manage-users` - User management (requires manage_users)
- `GET /api/v1/protected/my-permissions` - Get user permissions

### Admin endpoints
- `GET /api/v1/admin/users` - List all users
- `POST /api/v1/admin/users` - Create user
- `GET /api/v1/admin/roles` - List all roles
- `POST /api/v1/admin/roles` - Create role
- `GET /api/v1/admin/permissions` - List all permissions
- `POST /api/v1/admin/permissions` - Create permission

## Troubleshooting

### Common issues
1. Import errors - Make sure you're in the virtual environment
2. Database errors - Check your `DATABASE_URL` in `.env`
3. Port already in use - Change the port in `start.py` or kill the process using port 8000
4. CORS errors - Update `BACKEND_CORS_ORIGINS` in `.env`

### Getting help
1. Check the API documentation at `/docs`
2. Review the test files for usage examples
3. Check the logs for detailed error messages

## License

This project is open source and available under the MIT License.

---

You're all set! The RBAC system is now ready to use. 