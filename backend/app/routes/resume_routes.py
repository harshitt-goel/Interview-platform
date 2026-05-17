from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
import shutil

from app.database.dependencies import get_db
from app.utils.current_user import get_current_user
from app.utils.pdf_extractor import extract_text_from_pdf
from app.models.resume_model import Resume
import os

router = APIRouter()

@router.post("/upload-resume")
def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    os.makedirs("uploads", exist_ok=True)
    file_path = f"uploads/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    extracted_text = extract_text_from_pdf(file_path)

    new_resume = Resume(
        user_id=current_user.id,
        extracted_text=extracted_text
    )

    db.add(new_resume)
    db.commit()

    return {
        "message": "Resume uploaded successfully",
        "preview": extracted_text[:500]
    }