from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.schemas.user import UserCreate
from app.repositories.user_repo import UserRepository
from app.repositories.role_repo import RoleRepository
from app.core.security import get_password_hash

class UserService:
    def __init__(self, db: Session):
        self.user_repo = UserRepository(db)
        self.role_repo = RoleRepository(db)

    def register_user(self, user_in: UserCreate):
        """
        Register a new user in the system.
        """
        # 1. Check if user already exists
        if self.user_repo.get_by_email(user_in.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        if self.user_repo.get_by_username(user_in.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )

        # 2. Get the default role (assuming "user" role exists from init_db)
        user_role = self.role_repo.get_by_name("user")
        if not user_role:
            # Fallback or error if roles weren't seeded
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Default role 'user' not found in database"
            )

        # 3. Hash the password
        hashed_password = get_password_hash(user_in.password)

        # 4. Create the user
        return self.user_repo.create(
            user_in=user_in,
            password_hash=hashed_password,
            role_id=user_role.id
        )

    def get_all_users(self, skip: int = 0, limit: int = 100):
        """
        Get all users.
        Future: We will add a check here to ensure only Admins can call this.
        """
        return self.user_repo.get_all(skip=skip, limit=limit)