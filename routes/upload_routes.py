from fastapi import APIRouter, UploadFile, File, HTTPException
import shutil
import os

from services.document_service import extract_pdf, extract_docx, extract_pptx

router = APIRouter(prefix="/upload", tags=["Upload"])


@router.post("/")
async def upload_file(file: UploadFile = File(...)):

    allowed_extensions = [".pdf", ".docx", ".pptx"]

    file_extension = os.path.splitext(file.filename)[1].lower()

    if file_extension not in allowed_extensions:
        raise HTTPException(
            status_code=400, detail="Only PDF, DOCX, and PPTX files are allowed."
        )

    upload_folder = "uploads"

    os.makedirs(upload_folder, exist_ok=True)

    file_path = os.path.join(upload_folder, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    if file_extension == ".pdf":
        extracted_text = extract_pdf(file_path)

    elif file_extension == ".docx":
        extracted_text = extract_docx(file_path)

    elif file_extension == ".pptx":
        extracted_text = extract_pptx(file_path)

    return {
        "filename": file.filename,
        "type": file_extension,
        "content": extracted_text,
    }