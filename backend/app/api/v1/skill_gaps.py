"""
API Router for Skill Gap Analysis and Differential Capability Reporting.
Features:
- Authentic ESCO v1.1.1 and O*NET 31.0 Occupational Competency Benchmarking
- BAAI/bge-small-en-v1.5 Dense 384-dimensional Semantic Embedding Matching
- mlx-community/Qwen2.5-1.5B-Instruct-4bit Apple Silicon MLX Learning Roadmap Synthesis
- Verified Official Documentation & Course Catalogs (Python, PyTorch, React, Microsoft, AWS, GCP, freeCodeCamp)
"""

from typing import List, Optional
import uuid
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select

from app.core.database import get_db
from app.api.deps import get_current_active_user, get_current_user
from app.models.user import User
from app.models.profile import UserProfile
from app.models.skill import UserSkill
from app.models.occupation import Occupation, OccupationSkill
from app.models.job import JobListing, JobSkill
from app.models.skill_gap import SkillGapReport, SkillGapItem
from app.schemas.career_domain import (
    SkillGapReportCreate,
    SkillGapReportResponse,
)
from app.schemas.skill_gap import (
    SkillGapAnalyzeRequest,
    SkillGapAnalyzeResponse,
    OccupationSearchItem,
    LearningResourceItem,
)
from app.services.skill_gap_service import SkillGapService

router = APIRouter()


def _get_optional_user(
    request: Request,
    db: Session = Depends(get_db)
) -> Optional[User]:
    """Helper to authenticate user if Bearer token present, otherwise return None (guest mode)."""
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


# =============================================================================
# 1. AI-Powered Skill Gap Analysis Endpoints (Feature 4 Core)
# =============================================================================

@router.post(
    "/analyze",
    response_model=SkillGapAnalyzeResponse,
    summary="AI Semantic Skill Gap Analysis",
    description="Matches candidate skills against authentic ESCO / O*NET occupational competencies using BGE embeddings and synthesizes a personalized learning roadmap via local Qwen2.5 LLM."
)
def analyze_skill_gap(
    payload: SkillGapAnalyzeRequest,
    request: Request,
    db: Session = Depends(get_db)
):
    try:
        # If no skills supplied directly, check if authenticated candidate has saved skills
        if not payload.candidateSkills:
            user = _get_optional_user(request, db)
            if user:
                profile = db.execute(select(UserProfile).where(UserProfile.user_id == user.id)).scalar_one_or_none()
                if profile:
                    u_skills = db.execute(select(UserSkill).where(UserSkill.profile_id == profile.id)).scalars().all()
                    # Retrieve skill names if available
                    payload.candidateSkills = [us.skill.name for us in u_skills if hasattr(us, "skill") and us.skill]

        result = SkillGapService.analyze_skill_gap(payload)
        return result
    except ValueError as ve:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(ve)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Skill Gap Analysis failed: {str(e)}"
        )


@router.get(
    "/occupations",
    response_model=List[OccupationSearchItem],
    summary="Search Authentic Occupations from ESCO / O*NET",
    description="Searches genuine European Commission ESCO or O*NET occupational titles with verified competency counts."
)
def search_occupations(
    query: str = "",
    source: str = "esco",
    limit: int = 20
):
    try:
        return SkillGapService.search_occupations(query=query, source=source, limit=limit)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve occupations: {str(e)}"
        )


@router.post(
    "/learning-resources",
    response_model=List[LearningResourceItem],
    summary="Get Verified Learning Resources for Competency",
    description="Retrieves genuine official documentation and course links for specific skill gaps."
)
def get_learning_resources(
    skills: List[str]
):
    try:
        results = []
        seen = set()
        for s in skills:
            for r in SkillGapService.get_resources_for_skill(s):
                if r.id not in seen:
                    results.append(r)
                    seen.add(r.id)
        return results[:10]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve learning resources: {str(e)}"
        )


# =============================================================================
# 2. Legacy / Database Persistence Endpoints
# =============================================================================

@router.post("", response_model=SkillGapReportResponse, status_code=status.HTTP_201_CREATED)
def generate_skill_gap_report(
    payload: SkillGapReportCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Evaluate candidate competencies against an occupation or job listing in database.
    Calculates missing skills, priority levels, and overall match percentage.
    """
    profile = db.execute(
        select(UserProfile).where(UserProfile.user_id == current_user.id)
    ).scalar_one_or_none()

    user_skills_map = {}
    if profile:
        u_skills = db.execute(
            select(UserSkill).where(UserSkill.profile_id == profile.id)
        ).scalars().all()
        user_skills_map = {us.skill_id: us for us in u_skills}

    report = SkillGapReport(
        user_id=current_user.id,
        target_occupation_id=payload.target_occupation_id,
        target_job_id=payload.target_job_id,
        overall_match_percentage=payload.overall_match_percentage,
    )
    db.add(report)
    db.flush()

    items_to_save = []

    if payload.items:
        for it in payload.items:
            items_to_save.append(
                SkillGapItem(
                    report_id=report.id,
                    skill_id=it.skill_id,
                    current_proficiency=it.current_proficiency,
                    required_proficiency=it.required_proficiency,
                    gap_severity=it.gap_severity,
                    priority=it.priority,
                    assessment_reference_id=it.assessment_reference_id,
                )
            )
    elif payload.target_occupation_id:
        req_skills = db.execute(
            select(OccupationSkill).where(
                OccupationSkill.occupation_id == payload.target_occupation_id
            )
        ).scalars().all()

        total = len(req_skills)
        matched = 0

        for os in req_skills:
            if os.skill_id in user_skills_map:
                matched += 1
                curr_prof = user_skills_map[os.skill_id].proficiency_level
                items_to_save.append(
                    SkillGapItem(
                        report_id=report.id,
                        skill_id=os.skill_id,
                        current_proficiency=curr_prof,
                        required_proficiency="intermediate",
                        gap_severity="aligned" if curr_prof in ["intermediate", "expert"] else "low",
                        priority="low" if curr_prof in ["intermediate", "expert"] else "medium",
                    )
                )
            else:
                items_to_save.append(
                    SkillGapItem(
                        report_id=report.id,
                        skill_id=os.skill_id,
                        current_proficiency="none",
                        required_proficiency="intermediate",
                        gap_severity="missing",
                        priority="high" if os.is_required else "medium",
                    )
                )

        report.overall_match_percentage = round((matched / total) * 100, 1) if total > 0 else 100.0

    for item in items_to_save:
        db.add(item)

    db.commit()
    db.refresh(report)

    report = db.execute(
        select(SkillGapReport)
        .options(joinedload(SkillGapReport.items))
        .where(SkillGapReport.id == report.id)
    ).unique().scalar_one()

    return report


@router.get("", response_model=List[SkillGapReportResponse])
def list_user_skill_gap_reports(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Retrieve all skill gap evaluation reports generated for the authenticated candidate."""
    return db.execute(
        select(SkillGapReport)
        .options(joinedload(SkillGapReport.items))
        .where(SkillGapReport.user_id == current_user.id)
        .order_by(SkillGapReport.created_at.desc())
    ).unique().scalars().all()


@router.get("/{report_id}", response_model=SkillGapReportResponse)
def get_skill_gap_report(
    report_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Retrieve specific skill gap report detail."""
    report = db.execute(
        select(SkillGapReport)
        .options(joinedload(SkillGapReport.items))
        .where(
            SkillGapReport.id == report_id,
            SkillGapReport.user_id == current_user.id,
        )
    ).unique().scalar_one_or_none()

    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Skill gap report not found or access denied.",
        )
    return report
