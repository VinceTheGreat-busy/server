from fastapi import UploadFile
from sqlalchemy.orm import Session

from services.document_service import extract_document
from services.ai_service import generate_study_material
from controllers.study_deck_controller import create_deck


async def process_upload(
    file: UploadFile, file_bytes: bytes, user_id: int, db: Session
):
    # Extract document using the bytes we already read
    text = await extract_document(file.filename, file_bytes)

    if not text or not text.strip():
        raise ValueError("Could not extract text from the document.")

    print(f"Extracted {len(text)} characters " f"from {file.filename}")

    # Send extracted text to Gemini
    study_material = generate_study_material(text)

    # Create StudyDeck
    deck = create_deck(
        db=db,
        user_id=user_id,
        title=file.filename,
        notes=[note.model_dump() for note in study_material.notes],
        key_points=study_material.key_points,
        important_words=[word.model_dump() for word in study_material.important_words],
        quizzes=[quiz.model_dump() for quiz in study_material.quizzes],
        is_public=False,
    )

    return deck
