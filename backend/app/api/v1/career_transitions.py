"""
API Router for Career Transition Corridors, Transferable Skills, and Bridge Requirements.
"""

from typing import List, Optional
import uuid
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select

from app.core.database import get_db
from app.api.deps import get_current_active_user, require_admin
from app.models.user import User
from app.models.occupation import Occupation
from app.models.career_transition import (
    CareerTransition,
    TransferableSkillMapping,
    TransitionRequirement,
)
from app.schemas.career_domain import (
    CareerTransitionCreate,
    CareerTransitionResponse,
)

router = APIRouter()


@router.get("", response_model=List[CareerTransitionResponse])
def list_career_transitions(
    from_occupation_id: Optional[uuid.UUID] = Query(None, description="Starting informal/vocational trade"),
    to_occupation_id: Optional[uuid.UUID] = Query(None, description="Destination target occupation"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """List curated transition pathways bridging trade workers into formal industries."""
    query = (
        select(CareerTransition)
        .options(
            joinedload(CareerTransition.skills_mapping),
            joinedload(CareerTransition.requirements),
        )
    )

    if from_occupation_id:
        query = query.where(CareerTransition.from_occupation_id == from_occupation_id)
    if to_occupation_id:
        query = query.where(CareerTransition.to_occupation_id == to_occupation_id)

    query = query.order_by(CareerTransition.feasibility_score.desc())
    return db.execute(query).unique().scalars().all()


@router.get("/{transition_id}", response_model=CareerTransitionResponse)
def get_career_transition(
    transition_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Retrieve detailed specification of a career transition corridor."""
    transition = db.execute(
        select(CareerTransition)
        .options(
            joinedload(CareerTransition.skills_mapping),
            joinedload(CareerTransition.requirements),
        )
        .where(CareerTransition.id == transition_id)
    ).unique().scalar_one_or_none()

    if not transition:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Career transition corridor not found.",
        )
    return transition


@router.post("", response_model=CareerTransitionResponse, status_code=status.HTTP_201_CREATED)
def create_career_transition(
    payload: CareerTransitionCreate,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    """Administrator endpoint: map an official transition corridor between occupations."""
    from_occ = db.execute(
        select(Occupation).where(Occupation.id == payload.from_occupation_id)
    ).scalar_one_or_none()
    to_occ = db.execute(
        select(Occupation).where(Occupation.id == payload.to_occupation_id)
    ).scalar_one_or_none()

    if not from_occ or not to_occ:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Source or target occupation does not exist.",
        )

    transition = CareerTransition(
        from_occupation_id=payload.from_occupation_id,
        to_occupation_id=payload.to_occupation_id,
        transition_title=payload.transition_title,
        feasibility_score=payload.feasibility_score,
        estimated_transition_months=payload.estimated_transition_months,
        description=payload.description,
    )
    db.add(transition)
    db.flush()

    for sk in payload.skills_mapping:
        db.add(
            TransferableSkillMapping(
                transition_id=transition.id,
                skill_id=sk.skill_id,
                transferability_level=sk.transferability_level,
                notes=sk.notes,
            )
        )

    for req in payload.requirements:
        db.add(
            TransitionRequirement(
                transition_id=transition.id,
                title=req.title,
                description=req.description,
                requirement_type=req.requirement_type,
            )
        )

    db.commit()

    transition = db.execute(
        select(CareerTransition)
        .options(
            joinedload(CareerTransition.skills_mapping),
            joinedload(CareerTransition.requirements),
        )
        .where(CareerTransition.id == transition.id)
    ).unique().scalar_one()

    return transition


@router.delete("/{transition_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_career_transition(
    transition_id: uuid.UUID,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    """Administrator endpoint: delete a transition corridor."""
    transition = db.execute(
        select(CareerTransition).where(CareerTransition.id == transition_id)
    ).scalar_one_or_none()

    if not transition:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Career transition corridor not found.",
        )

    db.delete(transition)
    db.commit()
    return None

