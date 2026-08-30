from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db

from controllers.study_deck_controller import (
    get_all_decks,
    get_deck,
    get_user_decks,
    create_deck,
    update_deck,
    delete_deck,
)

router = APIRouter(prefix="/study-decks", tags=["Study Decks"])


@router.get("/")
def read_decks(db: Session = Depends(get_db)):
    return get_all_decks(db)


@router.get("/{deck_id}")
def read_deck(deck_id: int, db: Session = Depends(get_db)):
    return get_deck(db, deck_id)


@router.get("/user/{user_id}")
def read_user_decks(user_id: int, db: Session = Depends(get_db)):
    return get_user_decks(db, user_id)


@router.post("/")
def add_deck(deck_data: dict, db: Session = Depends(get_db)):
    return create_deck(db=db, **deck_data)


@router.put("/{deck_id}")
def edit_deck(deck_id: int, deck_data: dict, db: Session = Depends(get_db)):
    return update_deck(db=db, deck_id=deck_id, deck_data=deck_data)


@router.delete("/{deck_id}")
def remove_deck(deck_id: int, db: Session = Depends(get_db)):
    return delete_deck(db, deck_id)
