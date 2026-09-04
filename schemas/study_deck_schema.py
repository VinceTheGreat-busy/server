from pydantic import BaseModel
from typing import Any, Optional


class StudyDeckCreate(BaseModel):
    title: str
    description: str | None = None
    notes: list[Any] | None = None
    key_points: list[Any] | None = None
    important_words: list[Any] | None = None
    quizzes: list[Any] | None = None
    is_public: bool = False


class StudyDeckUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    notes: list[Any] | None = None
    key_points: list[Any] | None = None
    important_words: list[Any] | None = None
    quizzes: list[Any] | None = None
    is_public: bool | None = None


class StudyDeckResponse(BaseModel):
    id: int
    user_id: int
    title: str
    description: str | None
    notes: list[Any] | None
    key_points: list[Any] | None
    important_words: list[Any] | None
    quizzes: list[Any] | None
    is_public: bool

    class Config:
        from_attributes = True
