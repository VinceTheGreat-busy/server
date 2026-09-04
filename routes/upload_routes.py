from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
import os

from database import get_db
from models.User import User
from utils.auth_dependency import get_current_user

from controllers.ai_controller import process_upload

router = APIRouter(prefix="/upload", tags=["Upload"])


@router.post("/")
async def upload_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    allowed_extensions = [".pdf", ".docx", ".pptx"]

    file_extension = os.path.splitext(file.filename)[1].lower()

    if file_extension not in allowed_extensions:
        raise HTTPException(
            status_code=400, detail="Only PDF, DOCX, and PPTX files are allowed."
        )

    try:
        deck = await process_upload(file=file, user_id=current_user.id, db=db)

        return {"message": "Study deck created successfully.", "deck": deck}

    except Exception as e:
        print("Upload error:", e)

        raise HTTPException(status_code=500, detail=str(e))
