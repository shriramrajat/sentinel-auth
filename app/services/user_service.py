from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.schemas.user import UserCreate, UserUpdate
from app.repositories.user_repo import UserRepository
from app.repositories.role_repo import RoleRepository
from app.core.security import get_password_hash
from app.db.models.user import User

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
        """
        return self.user_repo.get_all(skip=skip, limit=limit)

    def get_user_by_id(self, user_id: str):
        """Get user by ID."""
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    def update_user(self, current_user: User, user_in: UserUpdate):
        """
        Update user profile.
        """
        # 1. If updating email, check uniqueness
        if user_in.email and user_in.email != current_user.email:
            if self.user_repo.get_by_email(user_in.email):
                raise HTTPException(status_code=400, detail="Email already taken")

        # 2. If password provided, update the hash logic
        # We need to manually handle this because the Repo expects model fields
        if user_in.password:
            hashed_pw = get_password_hash(user_in.password)
            current_user.password_hash = hashed_pw
            # Remove password from the pydantic model so it doesn't try to update a non-existent field
            # We will use exclude_unset in repo, so we just set the specific field on the model we want
            # But the repo iterates over user_in. So we must clear user_in.password to None
            user_in.password = None 
            
        # 3. Call Repo
        return self.user_repo.update(current_user, user_in)