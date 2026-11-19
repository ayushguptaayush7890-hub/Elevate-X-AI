"""
API Router for Objective Skill Diagnostics, Attempts, and Verification Scoring.
"""

from datetime import datetime, timezone
from typing import List, Optional
import uuid
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select

from app.core.database import get_db
from app.api.deps import get_current_active_user, require_admin
from app.models.user import User
from app.models.profile import UserProfile
from app.models.skill import Skill, UserSkill, SkillEvidence
from app.models.assessment import (
    Assessment,
    AssessmentQuestion,
    AssessmentOption,
    AssessmentAttempt,
    AssessmentAnswer,
    AssessmentResult,
)
from app.schemas.career_domain import (
    AssessmentCreate,
    AssessmentResponse,
    AssessmentStartResponse,
    AssessmentSubmissionPayload,
    AssessmentResultResponse,
    QuestionResponse,
    OptionResponse,
)

router = APIRouter()


@router.get("", response_model=List[AssessmentResponse])
def list_assessments(
    skill_id: Optional[uuid.UUID] = Query(None, description="Filter assessments by skill"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """List available standardized skill diagnostic assessments."""
    query = select(Assessment).where(Assessment.is_active == True)  # noqa: E712
    if skill_id:
        query = query.where(Assessment.skill_id == skill_id)

    query = query.order_by(Assessment.title.asc())
    return db.execute(query).scalars().all()


@router.post("", response_model=AssessmentResponse, status_code=status.HTTP_201_CREATED)
def create_assessment(
    payload: AssessmentCreate,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    """Administrator endpoint: create a new skill assessment with questions and options."""
    skill = db.execute(select(Skill).where(Skill.id == payload.skill_id)).scalar_one_or_none()
    if not skill:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Skill specified for assessment does not exist.",
        )

    assessment = Assessment(
        title=payload.title,
        description=payload.description,
        skill_id=payload.skill_id,
        difficulty_level=payload.difficulty_level,
        duration_minutes=payload.duration_minutes,
        passing_score_percentage=payload.passing_score_percentage,
        is_active=True,
    )
    db.add(assessment)
    db.flush()

    for q_data in payload.questions:
        q = AssessmentQuestion(
            assessment_id=assessment.id,
            question_text=q_data.question_text,
            question_type=q_data.question_type,
            points=q_data.points,
            order_index=q_data.order_index,
        )
        db.add(q)
        db.flush()

        for opt in q_data.options:
            db.add(
                AssessmentOption(
                    question_id=q.id,
                    option_text=opt.option_text,
                    is_correct=opt.is_correct,
                    explanation=opt.explanation,
                )
            )

    db.commit()
    db.refresh(assessment)
    return assessment


@router.get("/history", response_model=List[AssessmentResultResponse])
def get_user_assessment_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Retrieve all completed assessment results for the authenticated candidate."""
    results = db.execute(
        select(AssessmentResult)
        .where(AssessmentResult.user_id == current_user.id)
        .order_by(AssessmentResult.completed_at.desc())
    ).scalars().all()

    response_items = []
    for r in results:
        attempt = db.execute(
            select(AssessmentAttempt).where(AssessmentAttempt.id == r.attempt_id)
        ).scalar_one_or_none()
        total_points = 0.0
        points_awarded = 0.0
        if attempt:
            for ans in attempt.answers:
                points_awarded += ans.points_awarded
                total_points += ans.question.points if ans.question else 1.0

        response_items.append(
            AssessmentResultResponse(
                attempt_id=r.attempt_id,
                assessment_id=r.assessment_id,
                score_percentage=r.score_percentage,
                points_awarded=points_awarded,
                total_points=max(total_points, 1.0),
                passed=r.passed,
                status="completed",
                completed_at=r.completed_at,
            )
        )
    return response_items


@router.get("/{assessment_id}", response_model=AssessmentResponse)
def get_assessment(
    assessment_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Retrieve assessment overview."""
    assessment = db.execute(
        select(Assessment).where(Assessment.id == assessment_id)
    ).scalar_one_or_none()

    if not assessment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment not found.",
        )
    return assessment


@router.post("/{assessment_id}/start", response_model=AssessmentStartResponse)
def start_assessment_attempt(
    assessment_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Initialize a timed assessment session for the candidate.
    Delivers questions and choices with correct answer keys stripped.
    """
    assessment = db.execute(
        select(Assessment)
        .options(
            joinedload(Assessment.questions).joinedload(AssessmentQuestion.options)
        )
        .where(Assessment.id == assessment_id, Assessment.is_active == True)  # noqa: E712
    ).unique().scalar_one_or_none()

    if not assessment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment not found or inactive.",
        )

    attempt = AssessmentAttempt(
        user_id=current_user.id,
        assessment_id=assessment.id,
        started_at=datetime.now(timezone.utc),
        status="in_progress",
    )
    db.add(attempt)
    db.commit()
    db.refresh(attempt)

    # Format questions and options without leaking `is_correct`
    question_payloads = []
    for q in assessment.questions:
        options_payload = [
            OptionResponse(id=opt.id, option_text=opt.option_text)
            for opt in q.options
        ]
        question_payloads.append(
            QuestionResponse(
                id=q.id,
                question_text=q.question_text,
                question_type=q.question_type,
                points=q.points,
                order_index=q.order_index,
                options=options_payload,
            )
        )

    return AssessmentStartResponse(
        attempt_id=attempt.id,
        assessment_id=assessment.id,
        title=assessment.title,
        duration_minutes=assessment.duration_minutes,
        questions=question_payloads,
    )


@router.post("/attempts/{attempt_id}/submit", response_model=AssessmentResultResponse)
def submit_assessment_attempt(
    attempt_id: uuid.UUID,
    payload: AssessmentSubmissionPayload,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Submit answers for evaluation.
    Computes objective scorecard, passes/fails candidate, and triggers skill verification.
    """
    attempt = db.execute(
        select(AssessmentAttempt)
        .options(
            joinedload(AssessmentAttempt.assessment).joinedload(Assessment.questions).joinedload(AssessmentQuestion.options)
        )
        .where(
            AssessmentAttempt.id == attempt_id,
            AssessmentAttempt.user_id == current_user.id,
        )
    ).unique().scalar_one_or_none()

    if not attempt:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment attempt not found or not owned by user.",
        )

    if attempt.status == "completed":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Assessment attempt has already been submitted and scored.",
        )

    assessment = attempt.assessment
    questions_map = {q.id: q for q in assessment.questions}
    total_possible_points = sum(q.points for q in assessment.questions)
    earned_points = 0.0

    # Evaluate each submitted answer
    for submission in payload.answers:
        question = questions_map.get(submission.question_id)
        if not question:
            continue

        selected_option = next(
            (opt for opt in question.options if opt.id == submission.selected_option_id),
            None,
        )

        is_correct = bool(selected_option and selected_option.is_correct)
        pts = float(question.points) if is_correct else 0.0
        earned_points += pts

        answer = AssessmentAnswer(
            attempt_id=attempt.id,
            question_id=question.id,
            selected_option_id=submission.selected_option_id,
            is_correct=is_correct,
            points_awarded=pts,
        )
        db.add(answer)

    score_pct = (
        round((earned_points / total_possible_points) * 100, 2)
        if total_possible_points > 0
        else 0.0
    )
    passed = score_pct >= assessment.passing_score_percentage
    completed_time = datetime.now(timezone.utc)

    # Update attempt status
    attempt.completed_at = completed_time
    attempt.score_achieved = score_pct
    attempt.passed = passed
    attempt.status = "completed"

    # Save final scorecard
    result = AssessmentResult(
        user_id=current_user.id,
        assessment_id=assessment.id,
        attempt_id=attempt.id,
        score_percentage=score_pct,
        passed=passed,
        completed_at=completed_time,
    )
    db.add(result)

    # If passed, verify or add skill to user's profile
    if passed and assessment.skill_id:
        profile = db.execute(
            select(UserProfile).where(UserProfile.user_id == current_user.id)
        ).scalar_one_or_none()

        if profile:
            user_skill = db.execute(
                select(UserSkill).where(
                    UserSkill.profile_id == profile.id,
                    UserSkill.skill_id == assessment.skill_id,
                )
            ).scalar_one_or_none()

            if user_skill:
                user_skill.verification_status = "verified"
                user_skill.confidence_score = 0.95
            else:
                user_skill = UserSkill(
                    profile_id=profile.id,
                    skill_id=assessment.skill_id,
                    proficiency_level="intermediate",
                    verification_status="verified",
                    confidence_score=0.95,
                )
                db.add(user_skill)
                db.flush()

            # Record diagnostic assessment proof as verifiable skill evidence
            db.add(
                SkillEvidence(
                    user_skill_id=user_skill.id,
                    evidence_type="diagnostic_assessment",
                    title=f"Diagnostic Passed: {assessment.title}",
                    score_achieved=score_pct,
                    verified_at=completed_time,
                )
            )

    db.commit()

    return AssessmentResultResponse(
        attempt_id=attempt.id,
        assessment_id=assessment.id,
        score_percentage=score_pct,
        points_awarded=earned_points,
        total_points=float(total_possible_points),
        passed=passed,
        status="completed",
        completed_at=completed_time,
    )
