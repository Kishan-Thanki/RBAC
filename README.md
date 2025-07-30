# RBAC System - Simple User Management

A simple user management system that handles authentication and permissions. This project was built as a learning exercise to understand how role-based access control works.

## What it does

- User login/logout with JWT tokens
- Role-based access control (admin, user, moderator)
- Permission management
- Simple web interface for testing
- API endpoints for integration

## Quick setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up configuration:
   ```bash
   cp env.example .env
   ```

3. Start the server:
   ```bash
   python start.py
   ```

4. Access the system:
   - Web interface: http://localhost:8000
   - API docs: http://localhost:8000/docs
   - Default admin: admin@example.com / admin123

## Project structure

```
app/
├── main.py                 # Application entry point
├── core/                   # Core functionality
│   ├── config.py          # Settings
│   ├── auth.py            # Authentication
│   ├── rbac.py            # Permission checking
│   └── security.py        # Password hashing
├── models/                 # Database models
│   ├── user.py            # User model
│   ├── role.py            # Role model
│   ├── permission.py      # Permission model
│   └── base.py            # Base model
├── schemas/                # Data validation
│   ├── auth.py            # Auth schemas
│   ├── user.py            # User schemas
│   ├── role.py            # Role schemas
│   └── permission.py      # Permission schemas
├── routes/                 # API endpoints
│   ├── auth.py            # Login/logout
│   ├── admin.py           # Admin management
│   └── protected.py       # Protected endpoints
└── db/                     # Database setup
    └── base.py            # Database connection
```

## API endpoints

### Authentication
- `POST /auth/register` - Create account
- `POST /auth/login` - Login
- `POST /auth/refresh` - Refresh token
- `POST /auth/logout` - Logout

### Admin (admin only)
- `GET /admin/users` - List users
- `POST /admin/users` - Create user
- `GET /admin/roles` - List roles
- `POST /admin/roles` - Create role
- `GET /admin/permissions` - List permissions
- `POST /admin/permissions` - Create permission

### Protected
- `GET /protected/user-dashboard` - User dashboard
- `GET /protected/admin-only` - Admin only
- `GET /protected/manage-users` - User management

## How to use in your app

### Check permissions
```python
from app.core.rbac import require_permission_dependency

@router.get("/my-page")
async def my_page(
    current_user: User = Depends(require_permission_dependency("read_data"))
):
    return {"message": "Access granted!"}
```

### Create permissions
```python
# Via API
POST /admin/permissions
{
    "name": "edit_posts",
    "description": "Can edit blog posts"
}
```

## Testing

Run the basic tests:
```bash
python test_system.py
```

## Environment variables

Create a `.env` file:
```env
DATABASE_URL=sqlite:///./rbac.db
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
DEBUG=True
API_V1_STR=/api/v1
PROJECT_NAME=RBAC System
BACKEND_CORS_ORIGINS=["http://localhost:3000"]
FIRST_ADMIN_EMAIL=admin@example.com
FIRST_ADMIN_PASSWORD=admin123
```

## Default setup

When you first start the system:
- Admin user: admin@example.com / admin123
- Roles: admin, moderator, user
- Permissions: 19 default permissions

## License

MIT License 