from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
import os
import tempfile
import uuid

from sqlalchemy.orm import Session

from utils.auth_dependency import get_current_user

from database import get_db

from controllers.ai_controller import process_upload

from services.supabase_service import supabase, SUPABASE_BUCKET

from models.User import User

router = APIRouter(prefix="/upload", tags=["Upload"])


@router.post("/")
async def upload_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    allowed_extensions = [".pdf", ".docx", ".pptx"]

    import os

    extension = os.path.splitext(file.filename)[1].lower()

    if extension not in allowed_extensions:
        raise HTTPException(
            status_code=400, detail="Only PDF, DOCX, and PPTX files are allowed."
        )

    try:
        deck = await process_upload(file=file, user_id=current_user.id, db=db)

        return deck

    except Exception as e:
        print("Upload error:", e)

        raise HTTPException(status_code=500, detail="Failed to process uploaded file.")
