from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.utils.current_user import get_current_user
from app.models.resume_model import Resume
from app.services.gemini_service import (
    generate_interview_questions
)

router = APIRouter()

@router.post("/generate-questions")
def generate_questions(
    role: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    resume = db.query(Resume).filter(
        Resume.user_id == current_user.id
    ).first()

    if not resume:
        raise HTTPException(
            status_code=404,
            detail="Resume not found"
        )

    questions = generate_interview_questions(
        resume.extracted_text,
        role
    )

    return {
        "role": role,
        "questions": questions
    }