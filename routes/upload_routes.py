from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
import os
import tempfile
import uuid

from utils.auth_dependency import get_current_user

from services.document_service import extract_pdf, extract_docx, extract_pptx

from services.supabase_service import supabase, SUPABASE_BUCKET

from models.User import User

router = APIRouter(prefix="/upload", tags=["Upload"])


@router.post("/")
async def upload_file(
    file: UploadFile = File(...), current_user: User = Depends(get_current_user)
):

    allowed_extensions = [".pdf", ".docx", ".pptx"]

    file_extension = os.path.splitext(file.filename)[1].lower()

    if file_extension not in allowed_extensions:
        raise HTTPException(
            status_code=400, detail="Only PDF, DOCX, and PPTX files are allowed."
        )

    # Generate a unique filename
    unique_filename = f"{uuid.uuid4()}{file_extension}"

    # Organize files by user
    storage_path = f"user_{current_user.id}/{unique_filename}"

    try:

        # Read uploaded file
        file_content = await file.read()

        # Upload to Supabase Storage
        supabase.storage.from_(SUPABASE_BUCKET).upload(
            storage_path,
            file_content,
            {"content-type": file.content_type or "application/octet-stream"},
        )

    except Exception as e:

        print("Supabase upload error:", e)

        raise HTTPException(status_code=500, detail="Failed to upload file to storage.")

    # Temporary local file for text extraction
    temp_file_path = None

    try:

        with tempfile.NamedTemporaryFile(
            delete=False, suffix=file_extension
        ) as temp_file:

            temp_file.write(file_content)
            temp_file_path = temp_file.name

        # Extract text
        if file_extension == ".pdf":
            extracted_text = extract_pdf(temp_file_path)

        elif file_extension == ".docx":
            extracted_text = extract_docx(temp_file_path)

        elif file_extension == ".pptx":
            extracted_text = extract_pptx(temp_file_path)

        return {
            "filename": file.filename,
            "type": file_extension,
            "storage_path": storage_path,
            "content": extracted_text,
        }

    except Exception as e:

        print("Document extraction error:", e)

        raise HTTPException(
            status_code=500, detail="Failed to extract document content."
        )

    finally:

        # Delete temporary local file
        if temp_file_path and os.path.exists(temp_file_path):
            os.remove(temp_file_path)
