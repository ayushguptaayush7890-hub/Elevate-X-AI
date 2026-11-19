"""
API Router for Vocational Interview Simulations, Questions, Candidate Responses, and Feedback.
"""

from typing import List
import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select

from app.core.database import get_db
from app.api.deps import get_current_active_user
from app.models.user import User
from app.models.interview import (
    InterviewSession,
    InterviewQuestion,
    InterviewAnswer,
    InterviewFeedback,
)
from app.schemas.career_domain import (
    InterviewSessionCreate,
    InterviewSessionResponse,
    InterviewAnswerCreate,
    InterviewAnswerResponse,
    InterviewFeedbackCreate,
    InterviewFeedbackResponse,
)

router = APIRouter()


@router.post("/sessions", response_model=InterviewSessionResponse, status_code=status.HTTP_201_CREATED)
def create_interview_session(
    payload: InterviewSessionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Initialize a structured trade mock or diagnostic interview session."""
    session = InterviewSession(
        user_id=current_user.id,
        target_role=payload.target_role,
        trade_category=payload.trade_category,
        session_type=payload.session_type,
        status="in_progress",
    )
    db.add(session)
    db.flush()

    for q_data in payload.questions:
        db.add(
            InterviewQuestion(
                session_id=session.id,
                question_text=q_data.question_text,
                expected_competency=q_data.expected_competency,
                order_index=q_data.order_index,
            )
        )

    db.commit()

    session = db.execute(
        select(InterviewSession)
        .options(
            joinedload(InterviewSession.questions),
            joinedload(InterviewSession.answers),
            joinedload(InterviewSession.feedback),
        )
        .where(InterviewSession.id == session.id)
    ).unique().scalar_one()

    return session


@router.get("/sessions", response_model=List[InterviewSessionResponse])
def list_interview_sessions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Retrieve all interview practice sessions conducted by the authenticated candidate."""
    return db.execute(
        select(InterviewSession)
        .options(
            joinedload(InterviewSession.questions),
            joinedload(InterviewSession.answers),
            joinedload(InterviewSession.feedback),
        )
        .where(InterviewSession.user_id == current_user.id)
        .order_by(InterviewSession.created_at.desc())
    ).unique().scalars().all()


@router.get("/sessions/{session_id}", response_model=InterviewSessionResponse)
def get_interview_session(
    session_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Retrieve detailed state of an interview session."""
    session = db.execute(
        select(InterviewSession)
        .options(
            joinedload(InterviewSession.questions),
            joinedload(InterviewSession.answers),
            joinedload(InterviewSession.feedback),
        )
        .where(
            InterviewSession.id == session_id,
            InterviewSession.user_id == current_user.id,
        )
    ).unique().scalar_one_or_none()

    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interview session not found or access denied.",
        )
    return session


@router.post("/sessions/{session_id}/answers", response_model=InterviewAnswerResponse, status_code=status.HTTP_201_CREATED)
def submit_interview_answer(
    session_id: uuid.UUID,
    payload: InterviewAnswerCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Record candidate answer response to a specific interview prompt."""
    session = db.execute(
        select(InterviewSession).where(
            InterviewSession.id == session_id,
            InterviewSession.user_id == current_user.id,
        )
    ).scalar_one_or_none()

    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interview session not found.",
        )

    # Validate question belongs to this session
    question = db.execute(
        select(InterviewQuestion).where(
            InterviewQuestion.id == payload.question_id,
            InterviewQuestion.session_id == session.id,
        )
    ).scalar_one_or_none()

    if not question:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Question does not belong to this interview session.",
        )

    answer = InterviewAnswer(
        session_id=session.id,
        question_id=payload.question_id,
        user_response_text=payload.user_response_text,
        time_taken_seconds=payload.time_taken_seconds,
    )
    db.add(answer)
    db.commit()
    db.refresh(answer)
    return answer


@router.post("/sessions/{session_id}/feedback", response_model=InterviewFeedbackResponse, status_code=status.HTTP_201_CREATED)
def submit_interview_feedback(
    session_id: uuid.UUID,
    payload: InterviewFeedbackCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Complete an interview session and record candidate evaluation scorecard."""
    session = db.execute(
        select(InterviewSession).where(
            InterviewSession.id == session_id,
            InterviewSession.user_id == current_user.id,
        )
    ).scalar_one_or_none()

    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interview session not found.",
        )

    # Check if feedback already exists
    existing = db.execute(
        select(InterviewFeedback).where(InterviewFeedback.session_id == session.id)
    ).scalar_one_or_none()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Feedback for this interview session has already been submitted.",
        )

    feedback = InterviewFeedback(
        session_id=session.id,
        technical_accuracy_score=payload.technical_accuracy_score,
        clarity_score=payload.clarity_score,
        feedback_summary=payload.feedback_summary,
        areas_of_improvement=payload.areas_of_improvement,
    )
    db.add(feedback)
    session.status = "completed"
    db.commit()
    db.refresh(feedback)
    return feedback


@router.delete("/sessions/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_interview_session(
    session_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Delete an interview practice session."""
    session = db.execute(
        select(InterviewSession).where(
            InterviewSession.id == session_id,
            InterviewSession.user_id == current_user.id,
        )
    ).scalar_one_or_none()

    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interview session not found.",
        )

    db.delete(session)
    db.commit()
    return None

