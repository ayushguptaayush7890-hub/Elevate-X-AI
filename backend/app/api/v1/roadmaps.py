"""
API Router for Career Roadmaps, Milestones, and Hands-on Task Progression.
"""

from typing import List
import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select

from app.core.database import get_db
from app.api.deps import get_current_active_user
from app.models.user import User
from app.models.roadmap import CareerRoadmap, RoadmapMilestone, RoadmapTask
from app.schemas.career_domain import (
    RoadmapCreate,
    RoadmapResponse,
    TaskResponse,
)

router = APIRouter()


@router.post("", response_model=RoadmapResponse, status_code=status.HTTP_201_CREATED)
def create_roadmap(
    payload: RoadmapCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Create a structured vocational career roadmap with milestones and actionable tasks."""
    roadmap = CareerRoadmap(
        user_id=current_user.id,
        title=payload.title,
        target_role=payload.target_role,
        target_occupation_id=payload.target_occupation_id,
        estimated_duration_weeks=payload.estimated_duration_weeks,
        progress_percentage=0.0,
        status="active",
    )
    db.add(roadmap)
    db.flush()

    for m_data in payload.milestones:
        milestone = RoadmapMilestone(
            roadmap_id=roadmap.id,
            title=m_data.title,
            description=m_data.description,
            order_index=m_data.order_index,
            due_date=m_data.due_date,
            is_completed=False,
        )
        db.add(milestone)
        db.flush()

        for t_data in m_data.tasks:
            task = RoadmapTask(
                milestone_id=milestone.id,
                title=t_data.title,
                description=t_data.description,
                task_type=t_data.task_type,
                estimated_hours=t_data.estimated_hours,
                resource_url=t_data.resource_url,
                is_completed=False,
            )
            db.add(task)

    db.commit()

    roadmap = db.execute(
        select(CareerRoadmap)
        .options(
            joinedload(CareerRoadmap.milestones).joinedload(RoadmapMilestone.tasks)
        )
        .where(CareerRoadmap.id == roadmap.id)
    ).unique().scalar_one()

    return roadmap


@router.get("", response_model=List[RoadmapResponse])
def list_user_roadmaps(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Retrieve all active and completed roadmaps for the authenticated candidate."""
    return db.execute(
        select(CareerRoadmap)
        .options(
            joinedload(CareerRoadmap.milestones).joinedload(RoadmapMilestone.tasks)
        )
        .where(CareerRoadmap.user_id == current_user.id)
        .order_by(CareerRoadmap.created_at.desc())
    ).unique().scalars().all()


@router.get("/{roadmap_id}", response_model=RoadmapResponse)
def get_roadmap(
    roadmap_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Retrieve a single career roadmap with all milestones and tasks."""
    roadmap = db.execute(
        select(CareerRoadmap)
        .options(
            joinedload(CareerRoadmap.milestones).joinedload(RoadmapMilestone.tasks)
        )
        .where(
            CareerRoadmap.id == roadmap_id,
            CareerRoadmap.user_id == current_user.id,
        )
    ).unique().scalar_one_or_none()

    if not roadmap:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Career roadmap not found.",
        )
    return roadmap


@router.patch("/tasks/{task_id}/toggle", response_model=TaskResponse)
def toggle_roadmap_task(
    task_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Toggle a task's completion state.
    Automatically re-evaluates milestone completion and updates roadmap overall progress.
    """
    task = db.execute(
        select(RoadmapTask)
        .join(RoadmapMilestone, RoadmapTask.milestone_id == RoadmapMilestone.id)
        .join(CareerRoadmap, RoadmapMilestone.roadmap_id == CareerRoadmap.id)
        .where(
            RoadmapTask.id == task_id,
            CareerRoadmap.user_id == current_user.id,
        )
    ).scalar_one_or_none()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Roadmap task not found or access denied.",
        )

    task.is_completed = not task.is_completed
    db.flush()

    # Recalculate milestone and roadmap progress
    milestone = db.execute(
        select(RoadmapMilestone)
        .options(joinedload(RoadmapMilestone.tasks))
        .where(RoadmapMilestone.id == task.milestone_id)
    ).unique().scalar_one()

    milestone.is_completed = all(t.is_completed for t in milestone.tasks) if milestone.tasks else False

    # Roadmap overall progress
    roadmap = db.execute(
        select(CareerRoadmap)
        .options(joinedload(CareerRoadmap.milestones).joinedload(RoadmapMilestone.tasks))
        .where(CareerRoadmap.id == milestone.roadmap_id)
    ).unique().scalar_one()

    all_tasks = [t for m in roadmap.milestones for t in m.tasks]
    if all_tasks:
        completed_count = sum(1 for t in all_tasks if t.is_completed)
        progress = round((completed_count / len(all_tasks)) * 100, 1)
        roadmap.progress_percentage = progress
        if progress >= 100.0:
            roadmap.status = "completed"
        elif roadmap.status == "completed" and progress < 100.0:
            roadmap.status = "active"

    db.commit()
    db.refresh(task)
    return task


@router.delete("/{roadmap_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_roadmap(
    roadmap_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Delete a career roadmap and associated milestones."""
    roadmap = db.execute(
        select(CareerRoadmap).where(
            CareerRoadmap.id == roadmap_id,
            CareerRoadmap.user_id == current_user.id,
        )
    ).scalar_one_or_none()

    if not roadmap:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Career roadmap not found.",
        )

    db.delete(roadmap)
    db.commit()
    return None

