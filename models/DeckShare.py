from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class ShareDeck(Base):
    __tablename__ = "deck_shares"

    id = Column(Integer, primary_key=True, index=True)

    deck_id = Column(Integer, ForeignKey("study_decks.id"), nullable=False)

    shared_with_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    study_deck = relationship("StudyDeck", back_populates="shares")

    shared_with_user = relationship(
        "User", foreign_keys=[shared_with_user_id], back_populates="shared_decks"
    )