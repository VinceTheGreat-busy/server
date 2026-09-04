from database import get_db
from models import User
from schemas.study_deck_schema import StudyDeckUpdate
from utils.auth_dependency import get_current_user
from sqlalchemy.orm import Session
from models.StudyDeck import StudyDeck
from fastapi import Depends, HTTPException


def get_all_decks(db: Session):
    return db.query(StudyDeck).all()


def get_deck(db: Session, deck_id: int):
    return db.query(StudyDeck).filter(StudyDeck.id == deck_id).first()


def get_user_decks(db: Session, user_id: int):
    return db.query(StudyDeck).filter(StudyDeck.user_id == user_id).all()


def create_deck(
    db: Session,
    user_id: int,
    title: str,
    description: str | None = None,
    notes=None,
    key_points=None,
    important_words=None,
    quizzes=None,
    is_public: bool = False,
):

    deck = StudyDeck(
        user_id=user_id,
        title=title,
        description=description,
        notes=notes or [],
        key_points=key_points or [],
        important_words=important_words or [],
        quizzes=quizzes or [],
        is_public=is_public,
    )

    db.add(deck)
    db.commit()
    db.refresh(deck)

    return deck


def update_deck(
    deck_id: int,
    deck_data: StudyDeckUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    deck = (
        db.query(StudyDeck)
        .filter(StudyDeck.id == deck_id, StudyDeck.user_id == current_user.id)
        .first()
    )

    if not deck:
        raise HTTPException(status_code=404, detail="Deck not found.")

    if deck_data.title is not None:
        deck.title = deck_data.title

    if deck_data.description is not None:
        deck.description = deck_data.description

    db.commit()
    db.refresh(deck)

    return deck


def edit_deck(db: Session, deck_id: int, deck_data: dict):
    deck = get_deck(db, deck_id)

    allowed_fields = [
        "title",
        "description",
        "notes",
        "key_points",
        "important_words",
        "quizzes",
        "is_public",
    ]

    for field in allowed_fields:
        if field in deck_data:
            setattr(deck, field, deck_data[field])

    db.commit()
    db.refresh(deck)

    return deck


def delete_deck(db: Session, deck_id: int):
    deck = db.query(StudyDeck).filter(StudyDeck.id == deck_id).first()

    if not deck:
        raise HTTPException(status_code=404, detail="Deck not found.")

    db.delete(deck)
    db.commit()

    return {"message": "Deck deleted successfully."}
