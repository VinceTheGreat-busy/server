from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = "users"

    # Individuals
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)

    # Relationships
    study_decks = relationship(
        "StudyDeck", back_populates="owner", cascade="all, delete-orphan"
    )

    shared_decks = relationship(
        "ShareDeck",
        foreign_keys="ShareDeck.shared_with_user_id",
        back_populates="shared_with_user",
        cascade="all, delete-orphan",
    )
