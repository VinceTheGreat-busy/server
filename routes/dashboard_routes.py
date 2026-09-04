from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from models.StudyDeck import StudyDeck
from models.DeckShare import ShareDeck
from models.User import User
from utils.auth_dependency import get_current_user

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/")
def get_dashboard(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    decks = (
        db.query(StudyDeck)
        .filter(StudyDeck.user_id == current_user.id)
        .order_by(StudyDeck.id.desc())
        .all()
    )

    quiz_count = sum(len(deck.quizzes or []) for deck in decks)

    shared_count = (
        db.query(ShareDeck)
        .filter(ShareDeck.shared_with_user_id == current_user.id)
        .count()
    )

    return {
        "stats": {
            "study_decks": len(decks),
            "quizzes": quiz_count,
            "shared_decks": shared_count,
        },
        "recent_decks": decks[:3],
    }
