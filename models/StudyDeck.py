from sqlalchemy import Column, Integer, String, ForeignKey, JSON, Boolean
from sqlalchemy.orm import relationship

from database import Base


class StudyDeck(Base):
    __tablename__ = "study_decks"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    title = Column(String(255), nullable=False)
    description = Column(String)
    notes = Column(JSON)
    key_points = Column(JSON)
    important_words = Column(JSON)
    quizzes = Column(JSON)

    is_public = Column(Boolean, default=False)

    owner = relationship("User", back_populates="study_decks")

    shares = relationship(
        "ShareDeck", back_populates="study_deck", cascade="all, delete-orphan"
    )
