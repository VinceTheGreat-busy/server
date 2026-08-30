from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db

from controllers.deck_share_controller import (
    share_deck,
    get_shared_decks,
    get_deck_shares,
    remove_share,
)

router = APIRouter(prefix="/share-decks", tags=["Share Decks"])


@router.post("/")
def create_share(share_data: dict, db: Session = Depends(get_db)):
    return share_deck(
        db=db,
        deck_id=share_data["deck_id"],
        shared_with_user_id=share_data["shared_with_user_id"],
    )


@router.get("/user/{user_id}")
def read_shared_decks(user_id: int, db: Session = Depends(get_db)):
    return get_shared_decks(db, user_id)


@router.get("/deck/{deck_id}")
def read_deck_shares(deck_id: int, db: Session = Depends(get_db)):
    return get_deck_shares(db, deck_id)


@router.delete("/{share_id}")
def delete_share(share_id: int, db: Session = Depends(get_db)):
    return remove_share(db, share_id)
