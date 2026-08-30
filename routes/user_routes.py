from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from controllers.user_controller import (
    get_users,
    get_user,
    create_user,
    update_user,
    delete_user,
)

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/")
def read_users(db: Session = Depends(get_db)):
    return get_users(db)


@router.get("/{user_id}")
def read_user(user_id: int, db: Session = Depends(get_db)):
    return get_user(db, user_id)


@router.post("/")
def add_user(user_data: dict, db: Session = Depends(get_db)):
    return create_user(db, user_data)


@router.put("/{user_id}")
def edit_user(user_id: int, user_data: dict, db: Session = Depends(get_db)):
    return update_user(db, user_id, user_data)


@router.delete("/{user_id}")
def remove_user(user_id: int, db: Session = Depends(get_db)):
    return delete_user(db, user_id)
