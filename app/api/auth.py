from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.auth import (
    RegisterRequest, RegisterResponse,
    LoginRequest, TokenResponse,
    RefreshRequest, PasswordRecoveryRequest,
    PasswordResetRequest, MessageResponse
)
from app.services.auth_service import auth_service

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=RegisterResponse, status_code=201)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    """Register a new user."""
    user = auth_service.register(db, payload.email, payload.password)
    return user

@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    """Authenticate user with email and password. Returns access and refresh token."""
    return auth_service.login(db, payload.email, payload.password)

@router.post("/refresh", response_model=dict)
def refresh_token(payload: RefreshRequest, db: Session = Depends(get_db)):
    """Get new access token using a valid refresh token."""
    return auth_service.refresh_access_token(db, payload.refresh_token)

@router.post("/logout", response_model=MessageResponse)
def logout(payload: RefreshRequest, db: Session = Depends(get_db)):
    """Logout user by revoking the refresh token."""
    auth_service.revoke_refresh_token(db, payload.refresh_token)
    return {"message": "Logged out successfully."}

@router.post("/password-recovery", response_model=MessageResponse)
def password_recovery(payload: PasswordRecoveryRequest, db: Session = Depends(get_db)):
    """Initiate password recovery process by sending a reset link to the user's email."""
    message = auth_service.request_password_recovery(db, payload.email)
    return {"message": message}

@router.post("/password-reset", response_model=MessageResponse)
def password_reset(payload: PasswordResetRequest, db: Session = Depends(get_db)):
    """Reset password using a valid recovery token."""
    auth_service.reset_password(db, payload.token, payload.new_password)
    return {"message": "Password has been reset successfully."}