from fastapi import HTTPException
from sqlalchemy.orm import Session

from models.User import User


def get_users(db: Session):
    return db.query(User).all()


def get_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


def create_user(db: Session, user_data: dict):
    existing_user = db.query(User).filter(User.email == user_data["email"]).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(
        name=user_data["name"], email=user_data["email"], password=user_data["password"]
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def update_user(db: Session, user_id: int, user_data: dict):
    user = get_user(db, user_id)

    if "name" in user_data:
        user.name = user_data["name"]

    if "email" in user_data:
        user.email = user_data["email"]

    if "password" in user_data:
        user.password = user_data["password"]

    db.commit()
    db.refresh(user)

    return user


def delete_user(db: Session, user_id: int):
    user = get_user(db, user_id)

    db.delete(user)
    db.commit()

    return {"message": "User deleted successfully"}
