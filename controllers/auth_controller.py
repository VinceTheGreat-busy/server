from fastapi import HTTPException
from sqlalchemy.orm import Session

from models.User import User
from utils.auth_utils import hash_password, verify_password, create_access_token


def reset_password(db: Session, email: str, new_password: str):
    # Find user
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # Hash the new password
    user.password = hash_password(new_password)

    db.commit()
    db.refresh(user)

    return {"message": "Password reset successfully"}


def register_user(db: Session, name: str, email: str, password: str):

    # Check existing email
    existing_user = db.query(User).filter(User.email == email).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email is already registered")

    # Hash password
    hashed_password = hash_password(password)

    user = User(name=name, email=email, password=hashed_password)

    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_access_token({"sub": str(user.id)})

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {"id": user.id, "name": user.name, "email": user.email},
    }


def login_user(db: Session, email: str, password: str):

    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    if not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token({"sub": str(user.id)})

    return {"access_token": token, "token_type": "bearer"}
