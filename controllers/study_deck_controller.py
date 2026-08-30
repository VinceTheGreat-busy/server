from sqlalchemy.orm import Session
from models.StudyDeck import StudyDeck


def get_all_decks(db: Session):
    return db.query(StudyDeck).all()


def get_deck(db: Session, deck_id: int):
    return db.query(StudyDeck).filter(StudyDeck.id == deck_id).first()


def get_user_decks(db: Session, user_id: int):
    return (
        db.query(StudyDeck)
        .filter(StudyDeck.user_id == user_id)
        .all()
    )
    

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


def update_deck(db: Session, deck_id: int, deck_data: dict):
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
    deck = get_deck(db, deck_id)

    db.delete(deck)
    db.commit()

    return {"message": "Study deck deleted successfully"}
