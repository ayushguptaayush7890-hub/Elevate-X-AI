"""
API Router for Career Transition Corridors, Transferable Skills, and Bridge Requirements.
"""

from typing import List, Optional
import uuid
from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
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
from app.schemas.career_transition import (
    OccupationSearchItem,
    AcademicCompetencyItem,
    AcademicProfileSummary,
    TransitionRecommendationItem,
    TransitionRecommendationsRequest,
    TransitionAnalysisRequest,
    TransitionAnalysisResponse,
    TransitionBlueprintRequest,
    TransitionBlueprintResponse,
    TransitionCompareRequest,
    AdoptGoalRequest,
    AdoptGoalResponse,
    UserGoalProgressItem,
)
from app.services.career_transition_service import CareerTransitionService

router = APIRouter()


def _get_optional_user(
    request: Request,
    db: Session = Depends(get_db)
) -> Optional[User]:
    """Helper to authenticate user if Bearer token is present, otherwise return None (guest mode)."""
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return None
    token = auth_header.split(" ")[1]
    try:
        from app.core.security import decode_token
        payload = decode_token(token)
        user_id_str = payload.get("sub")
        if user_id_str:
            user_id = uuid.UUID(user_id_str)
            return db.execute(select(User).where(User.id == user_id)).scalar_one_or_none()
    except Exception:
        return None
    return None


# -----------------------------------------------------------------------------
# Data-Driven Occupational Search & Mobility Endpoints
# -----------------------------------------------------------------------------

@router.get("/academic-profile", response_model=AcademicProfileSummary)
def get_user_academic_profile(
    request: Request,
    db: Session = Depends(get_db),
):
    """
    Retrieve candidate's verified academic background and extracted technical competencies.
    Preserves provenance across formal degrees, coursework, projects, and certifications.
    """
    current_user = _get_optional_user(request, db)
    return CareerTransitionService.get_candidate_academic_profile(
        user_id=current_user.id if current_user else None,
        db=db,
    )


@router.get("/occupations", response_model=List[OccupationSearchItem])
def search_occupations(
    q: str = Query("", description="Search term for occupation title or code"),
    limit: int = Query(15, ge=1, le=50),
    taxonomy: Optional[str] = Query(None, description="Optional taxonomy filter: ESCO, ONET, or NCO"),
):
    """Search master occupations catalog across ESCO, O*NET, and India NCO-2015."""
    return CareerTransitionService.search_occupations(q, limit=limit, taxonomy_filter=taxonomy)


@router.get("/occupations/{occupation_id}")
def get_occupation_details(
    occupation_id: str,
):
    """Retrieve detailed occupational profile and associated competency requirements."""
    occ = CareerTransitionService.resolve_occupation(occupation_id)
    if not occ:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Occupation '{occupation_id}' not found in master catalog.",
        )
    skills = CareerTransitionService.get_occupation_skills(occ)
    salary, demand, postings = CareerTransitionService.get_job_market_data(occ["occupation_title"])
    return {
        "occupation": occ,
        "skills": skills,
        "market": {
            "salary_range": salary,
            "demand_level": demand,
            "sample_postings_count": postings
        }
    }


@router.post("/recommendations", response_model=List[TransitionRecommendationItem])
def get_transition_recommendations(
    payload: TransitionRecommendationsRequest,
    request: Request,
    db: Session = Depends(get_db),
):
    """
    Generate explainable alternative career transition pathways ranked by graph structural
    similarity, transferable skill overlap, and real-market feasibility.
    """
    current_user = _get_optional_user(request, db)
    return CareerTransitionService.recommend_transitions(
        current_occ_name=payload.current_occupation,
        user_id=current_user.id if current_user else None,
        candidate_skills=payload.candidate_skills,
        limit=payload.limit,
        db=db,
    )


@router.post("/analyze", response_model=TransitionAnalysisResponse)
def analyze_career_transition(
    payload: TransitionAnalysisRequest,
    request: Request,
    db: Session = Depends(get_db),
):
    """
    Perform deep side-by-side skill transferability audit across 5-tier evidence states:
    assessment_verified, practically_demonstrated, mentioned_in_resume, self_reported,
    and related_taxonomy_evidence.
    """
    current_user = _get_optional_user(request, db)
    return CareerTransitionService.analyze_transition(
        from_occ_name=payload.from_occupation,
        to_occ_name=payload.to_occupation,
        user_id=current_user.id if current_user else None,
        candidate_skills_input=payload.candidate_skills,
        db=db,
    )


@router.post("/compare")
def compare_transitions(
    payload: TransitionCompareRequest,
    request: Request,
    db: Session = Depends(get_db),
):
    """Compare multiple potential transition target destinations side-by-side."""
    current_user = _get_optional_user(request, db)
    user_id = current_user.id if current_user else None
    comparisons = []
    for target in payload.target_occupations:
        analysis = CareerTransitionService.analyze_transition(
            from_occ_name=payload.current_occupation,
            to_occ_name=target,
            user_id=user_id,
            candidate_skills_input=payload.candidate_skills,
            db=db,
        )
        comparisons.append(analysis)
    return {"current_occupation": payload.current_occupation, "comparisons": comparisons}


@router.post("/blueprint", response_model=TransitionBlueprintResponse)
def generate_transition_blueprint(
    payload: TransitionBlueprintRequest,
    request: Request,
    db: Session = Depends(get_db),
):
    """
    Generate personalized 4-stage Transition Bridge Blueprint grounded in candidate evidence,
    authentic missing competencies, and official learning resources.
    """
    current_user = _get_optional_user(request, db)
    return CareerTransitionService.generate_blueprint(
        from_occ_name=payload.from_occupation,
        to_occ_name=payload.to_occupation,
        user_id=current_user.id if current_user else None,
        candidate_skills=payload.candidate_skills,
        recalibrate=payload.recalibrate or False,
        db=db,
    )


@router.post("/blueprint/recalibrate", response_model=TransitionBlueprintResponse)
def recalibrate_transition_blueprint(
    payload: TransitionBlueprintRequest,
    request: Request,
    db: Session = Depends(get_db),
):
    """
    Force recalibration of transition blueprint: invalidates existing cache and executes
    fresh model inference and verified resource matching.
    """
    current_user = _get_optional_user(request, db)
    return CareerTransitionService.generate_blueprint(
        from_occ_name=payload.from_occupation,
        to_occ_name=payload.to_occupation,
        user_id=current_user.id if current_user else None,
        candidate_skills=payload.candidate_skills,
        recalibrate=True,
        db=db,
    )


@router.post("/adopt-goal", response_model=AdoptGoalResponse)
@router.post("/goals/adopt", response_model=AdoptGoalResponse)
def adopt_transition_goal(
    payload: AdoptGoalRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Adopt destination occupation as active career goal. Automatically records progress
    and creates or links the personalized Career Roadmap.
    """
    return CareerTransitionService.adopt_goal(
        user_id=current_user.id,
        payload=payload,
        db=db,
    )


@router.get("/progress", response_model=List[UserGoalProgressItem])
def get_user_transition_progress(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Retrieve active and historical transition goals adopted by the user."""
    return CareerTransitionService.get_user_progress(
        user_id=current_user.id,
        db=db,
    )


# -----------------------------------------------------------------------------
# Curated Legacy Transition Corridors (Preserved for Backwards Compatibility)
# -----------------------------------------------------------------------------

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
