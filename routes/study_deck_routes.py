from http.client import HTTPException

from fastapi import APIRouter, Depends
from schemas.study_deck_schema import StudyDeckCreate
from utils.auth_dependency import get_current_user
from models import User
from models.StudyDeck import StudyDeck
from sqlalchemy.orm import Session

from database import get_db

from controllers.study_deck_controller import (
    get_all_decks,
    get_deck,
    get_user_decks,
    create_deck,
    edit_deck,
    update_deck,
    delete_deck,
)

router = APIRouter(prefix="/study-decks", tags=["Study Decks"])


@router.get("/")
def get_my_decks(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    return (
        db.query(StudyDeck)
        .filter(StudyDeck.user_id == current_user.id)
        .order_by(StudyDeck.id.desc())
        .all()
    )


@router.get("/all")
def read_decks(db: Session = Depends(get_db)):
    return get_all_decks(db)


@router.get("/{deck_id}")
def read_deck(deck_id: int, db: Session = Depends(get_db)):
    return get_deck(db, deck_id)


@router.get("/user/{user_id}")
def read_user_decks(user_id: int, db: Session = Depends(get_db)):
    return get_user_decks(db, user_id)


@router.post("/")
def add_deck(
    deck_data: StudyDeckCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_deck(db=db, user_id=current_user.id, **deck_data.model_dump())


@router.put("/{deck_id}")
def edit_deck(deck_id: int, deck_data: dict, db: Session = Depends(get_db)):
    return edit_deck(db=db, deck_id=deck_id, deck_data=deck_data)


@router.patch("/{deck_id}")
def update_deck(deck_id: int, deck_data: dict, db: Session = Depends(get_db)):
    return update_deck(db=db, deck_id=deck_id, deck_data=deck_data)


@router.delete("/{deck_id}")
def remove_deck(deck_id: int, db: Session = Depends(get_db)):
    return delete_deck(db, deck_id)
