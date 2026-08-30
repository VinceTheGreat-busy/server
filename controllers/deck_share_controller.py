from fastapi import HTTPException
from sqlalchemy.orm import Session

from models.DeckShare import ShareDeck
from models.StudyDeck import StudyDeck
from models.User import User


def share_deck(db: Session, deck_id: int, shared_with_user_id: int):
    deck = db.query(StudyDeck).filter(StudyDeck.id == deck_id).first()

    if not deck:
        raise HTTPException(status_code=404, detail="Study deck not found")

    user = db.query(User).filter(User.id == shared_with_user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    existing_share = (
        db.query(ShareDeck)
        .filter(
            ShareDeck.deck_id == deck_id,
            ShareDeck.shared_with_user_id == shared_with_user_id,
        )
        .first()
    )

    if existing_share:
        raise HTTPException(
            status_code=400, detail="Deck already shared with this user"
        )

    share = ShareDeck(deck_id=deck_id, shared_with_user_id=shared_with_user_id)

    db.add(share)
    db.commit()
    db.refresh(share)

    return share


def get_shared_decks(db: Session, user_id: int):
    return db.query(ShareDeck).filter(ShareDeck.shared_with_user_id == user_id).all()


def get_deck_shares(db: Session, deck_id: int):
    return db.query(ShareDeck).filter(ShareDeck.deck_id == deck_id).all()


def remove_share(db: Session, share_id: int):
    share = db.query(ShareDeck).filter(ShareDeck.id == share_id).first()

    if not share:
        raise HTTPException(status_code=404, detail="Share not found")

    db.delete(share)
    db.commit()

    return {"message": "Deck share removed successfully"}
