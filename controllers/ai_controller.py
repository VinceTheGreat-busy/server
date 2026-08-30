from fastapi import UploadFile
from services.document_service import extract_document
from services.ai_service import generate_study_material
from services.ai_service import test_ai
from controllers.study_deck_controller import create_deck


async def process_upload(file: UploadFile, user_id: int, db):

    # 1. Extract document
    text = await extract_document(file)

    # 2. Send extracted text to Gemini
    study_material = generate_study_material(text)

    # 4. Create StudyDeck
    deck = create_deck(
        db=db,
        user_id=user_id,
        title=file.filename,
        notes=[note.model_dump() for note in study_material.notes],
        key_points=study_material.key_points,
        important_words=[word.model_dump() for word in study_material.important_words],
        quizzes=[quiz.model_dump() for quiz in study_material.quizzes],
    )

    return deck


def run_ai_test():

    return test_ai()
