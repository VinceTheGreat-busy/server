from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db

from schemas.auth_schema import RegisterRequest, LoginRequest, TokenResponse, ResetPasswordRequest
from models.User import User
from utils.auth_dependency import get_current_user

from controllers.auth_controller import register_user, login_user, reset_password

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.post("/register")
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    return register_user(
        db=db, name=data.name, email=data.email, password=data.password
    )


@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    return login_user(db=db, email=data.email, password=data.password)


@router.post("/reset-password") 
def reset_password_route(data: ResetPasswordRequest, db: Session = Depends(get_db)):
    return reset_password(db=db, email=data.email, new_password=data.new_password)