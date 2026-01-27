from fastapi import APIRouter
from app.api.routes import auth, users, admin

api_router = APIRouter()

# Group: Authentication (Login)
api_router.include_router(auth.router, tags=["Authentication"])

# Group: Users (Signup, Profile)
api_router.include_router(users.router, prefix="/users", tags=["Users"])

# Group: Admin (for future use)
api_router.include_router(admin.router, prefix="/admin", tags=["Admin"])