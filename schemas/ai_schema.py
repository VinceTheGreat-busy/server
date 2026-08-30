from pydantic import BaseModel
from typing import List


class Note(BaseModel):
    title: str
    content: str


class ImportantWord(BaseModel):
    word: str
    definition: str


class Quiz(BaseModel):
    question: str
    choices: List[str]
    answer: str


class StudyMaterial(BaseModel):
    notes: List[Note]
    key_points: List[str]
    important_words: List[ImportantWord]
    quizzes: List[Quiz]
