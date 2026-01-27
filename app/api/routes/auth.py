from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.auth import LoginRequest
from app.schemas.token import Token
from app.services.auth_service import AuthService
from app.schemas.auth import LoginRequest, RefreshTokenRequest

router = APIRouter()

@router.post("/login", response_model=Token)
def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    """
    OAuth2 compatible token login, get an access token for future requests.
    """
    auth_service = AuthService(db)
    return auth_service.login(
        username=login_data.username,
        password=login_data.password
    )

@router.post("/refresh", response_model=Token)
def refresh_token(request: RefreshTokenRequest, db: Session = Depends(get_db)):
    """
    Get a new access token using a refresh token.
    """
    auth_service = AuthService(db)
    return auth_service.refresh_access_token(request.refresh_token)