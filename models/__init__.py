from .User import User
from .StudyDeck import StudyDeck
from .DeckShare import ShareDeck

from database import Base, engine

Base.metadata.create_all(bind=engine)