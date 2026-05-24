from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.utils.current_user import get_current_user
from app.models.resume_model import Resume
from app.services.gemini_service import (
    generate_interview_questions
)
from app.models.interview_model import Interview
from app.services.gemini_service import generate_feedback

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

    new_interview = Interview(
        user_id=current_user.id,
        role=role,
        questions=questions
    )

    db.add(new_interview)
    db.commit()
    db.refresh(new_interview)

    return {
    "interview_id": new_interview.id,
    "role": role,
    "questions": questions
    }

@router.post("/submit-answers")
def submit_answers(
    interview_id: int,
    answers: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    interview = db.query(Interview).filter(
        Interview.id == interview_id,
        Interview.user_id == current_user.id
    ).first()

    if not interview:
        raise HTTPException(
            status_code=404,
            detail="Interview not found"
        )

    feedback = generate_feedback(
        interview.questions,
        answers
    )

    interview.answers = answers
    interview.feedback = feedback

    db.commit()

    return {
        "message": "Answers submitted",
        "feedback": feedback
    }