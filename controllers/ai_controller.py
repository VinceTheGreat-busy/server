from fastapi import UploadFile
from services.document_service import extract_document
from services.ai_service import generate_study_material
from services.ai_service import test_ai
from controllers.study_deck_controller import create_deck


async def process_upload(file: UploadFile, user_id: int, db):

    # Read file
    file_content = await file.read()

    # Generate storage path
    extension = os.path.splitext(file.filename)[1].lower()

    storage_filename = f"{uuid.uuid4()}{extension}"

    storage_path = f"user_{user_id}/{storage_filename}"

    # Upload to Supabase
    upload_file(
        file_content=file_content,
        storage_path=storage_path,
        content_type=file.content_type or "application/octet-stream",
    )

    # Extract
    text = await extract_document(file)

    # Gemini
    study_material = generate_study_material(text)

    # Create deck
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


def run_ai_test():

    return test_ai()
