from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session

from controllers.ai_controller import run_ai_test, process_upload
from database import get_db
from auth import get_current_user
from models.User import User

router = APIRouter(prefix="/api", tags=["AI"])


@router.get("/test-ai")
def test_ai():
    return {"response": run_ai_test()}


@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await process_upload(file=file, user_id=current_user.id, db=db)
