"""
API Router for Dynamic Career Roadmaps, Milestones, and Hands-on Tasks.
"""

from typing import List, Optional
import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.deps import get_current_active_user
from app.models.user import User
from app.schemas.career_roadmap import (
    CareerRoadmapDetailResponse,
    CareerRoadmapGenerateRequest,
    CareerRoadmapGoalUpdateRequest,
    CareerRoadmapRecalibrateRequest,
)
from app.services.career_roadmap_service import CareerRoadmapService

router = APIRouter()


@router.get("/current", response_model=CareerRoadmapDetailResponse)
def get_current_career_roadmap(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Retrieve the current active personalized career roadmap for the authenticated candidate.
    If no active roadmap exists, automatically initializes one from candidate's profile.
    """
    return CareerRoadmapService.get_or_create_roadmap(db=db, user=current_user)


@router.post("/generate", response_model=CareerRoadmapDetailResponse, status_code=status.HTTP_201_CREATED)
def generate_career_roadmap(
    payload: CareerRoadmapGenerateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Generate and persist a new tailored career roadmap based on target role,
    assessed candidate skills, and authentic competency tiers.
    """
    try:
        return CareerRoadmapService.get_or_create_roadmap(
            db=db,
            user=current_user,
            target_role=payload.target_role,
            candidate_skills=payload.candidate_skills,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e),
        )


@router.patch("/goal", response_model=CareerRoadmapDetailResponse)
def update_career_goal(
    payload: CareerRoadmapGoalUpdateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Update candidate's target career occupation and recalibrate all roadmap milestones.
    """
    try:
        return CareerRoadmapService.get_or_create_roadmap(
            db=db,
            user=current_user,
            target_role=payload.target_role,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e),
        )


@router.post("/recalibrate", response_model=CareerRoadmapDetailResponse)
def recalibrate_career_roadmap(
    payload: Optional[CareerRoadmapRecalibrateRequest] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Recalibrates current career roadmap using AI model inference and latest candidate profile.
    """
    target_role = payload.target_role if payload else None
    candidate_skills = payload.candidate_skills if payload else None
    try:
        return CareerRoadmapService.get_or_create_roadmap(
            db=db,
            user=current_user,
            target_role=target_role,
            candidate_skills=candidate_skills,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e),
        )


@router.patch("/milestones/{milestone_id}/toggle", response_model=CareerRoadmapDetailResponse)
def toggle_milestone_completion(
    milestone_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Toggles completion status of a milestone, updating all child tasks and overall roadmap progress.
    """
    try:
        return CareerRoadmapService.toggle_milestone(
            db=db, milestone_id=milestone_id, user_id=current_user.id
        )
    except ValueError as e:
        status_code = status.HTTP_404_NOT_FOUND if "not found" in str(e).lower() else status.HTTP_400_BAD_REQUEST
        raise HTTPException(status_code=status_code, detail=str(e))


@router.patch("/tasks/{task_id}/toggle", response_model=CareerRoadmapDetailResponse)
def toggle_task_completion(
    task_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Toggles completion status of an individual task, recalculating milestone status and overall progress.
    """
    try:
        return CareerRoadmapService.toggle_task(
            db=db, task_id=task_id, user_id=current_user.id
        )
    except ValueError as e:
        status_code = status.HTTP_404_NOT_FOUND if "not found" in str(e).lower() else status.HTTP_400_BAD_REQUEST
        raise HTTPException(status_code=status_code, detail=str(e))
