"""
API Router for Occupation Catalog & NSQF Taxonomy Management.
"""

from typing import List, Optional
import uuid
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import select, or_, func

from app.core.database import get_db
from app.api.deps import get_current_active_user, require_admin
from app.models.user import User
from app.models.occupation import Occupation, OccupationSkill
from app.schemas.career_domain import (
    OccupationCreate,
    OccupationUpdate,
    OccupationResponse,
)

router = APIRouter()


@router.get("", response_model=List[OccupationResponse])
def list_occupations(
    category: Optional[str] = Query(None, description="Filter by occupational category"),
    nsqf_level: Optional[int] = Query(None, ge=1, le=8, description="Filter by NSQF level"),
    search: Optional[str] = Query(None, description="Search term for title or description"),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """List standardized vocational occupations with search and category filtering."""
    query = select(Occupation).where(Occupation.is_active == True)  # noqa: E712

    if category:
        query = query.where(Occupation.category == category)
    if nsqf_level is not None:
        query = query.where(Occupation.nsqf_level == nsqf_level)
    if search:
        search_filter = f"%{search.strip()}%"
        query = query.where(
            or_(
                Occupation.title.ilike(search_filter),
                Occupation.description.ilike(search_filter),
                Occupation.category.ilike(search_filter),
            )
        )

    query = query.order_by(Occupation.title.asc()).offset(offset).limit(limit)
    return db.execute(query).scalars().all()


@router.get("/{occupation_id}", response_model=OccupationResponse)
def get_occupation(
    occupation_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Retrieve detailed occupation information by unique identifier."""
    occupation = db.execute(
        select(Occupation).where(Occupation.id == occupation_id)
    ).scalar_one_or_none()

    if not occupation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Occupation with ID '{occupation_id}' not found.",
        )
    return occupation


@router.post("", response_model=OccupationResponse, status_code=status.HTTP_201_CREATED)
def create_occupation(
    payload: OccupationCreate,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    """Administrator endpoint: create a new standardized occupation profile."""
    existing = db.execute(
        select(Occupation).where(
            or_(
                func.lower(Occupation.title) == payload.title.lower(),
                Occupation.code == payload.code if payload.code else False,
            )
        )
    ).scalar_one_or_none()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An occupation with this title or code already exists.",
        )

    occupation = Occupation(
        code=payload.code,
        title=payload.title,
        category=payload.category,
        description=payload.description,
        recommended_experience_years=payload.recommended_experience_years,
        education_requirements=payload.education_requirements,
        nsqf_level=payload.nsqf_level,
        is_active=payload.is_active,
    )
    db.add(occupation)
    db.flush()

    for skill_spec in payload.required_skills:
        req_skill = OccupationSkill(
            occupation_id=occupation.id,
            skill_id=skill_spec.skill_id,
            is_required=skill_spec.is_required,
            importance_weight=skill_spec.importance_weight,
        )
        db.add(req_skill)

    db.commit()
    db.refresh(occupation)
    return occupation


@router.put("/{occupation_id}", response_model=OccupationResponse)
def update_occupation(
    occupation_id: uuid.UUID,
    payload: OccupationUpdate,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    """Administrator endpoint: update an existing occupation profile."""
    occupation = db.execute(
        select(Occupation).where(Occupation.id == occupation_id)
    ).scalar_one_or_none()

    if not occupation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Occupation not found.",
        )

    for field, val in payload.model_dump(exclude_unset=True).items():
        setattr(occupation, field, val)

    db.commit()
    db.refresh(occupation)
    return occupation


@router.delete("/{occupation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_occupation(
    occupation_id: uuid.UUID,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    """Administrator endpoint: delete an occupation profile from the catalog."""
    occupation = db.execute(
        select(Occupation).where(Occupation.id == occupation_id)
    ).scalar_one_or_none()

    if not occupation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Occupation not found.",
        )

    db.delete(occupation)
    db.commit()
    return None

