"""
Vocational Skills Catalog and User Skill Mapping API.
Strictly distinguishes self-reported from assessed and independently verified competencies.
"""

import time
from typing import List, Optional
import uuid
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select, or_
from app.core.database import get_db
from app.models.profile import UserProfile
from app.models.skill import Skill, UserSkill, SkillEvidence
from app.schemas.skill import (
    SkillCreate,
    SkillResponse,
    UserSkillCreate,
    UserSkillUpdate,
    UserSkillResponse,
    SkillEvidenceCreate,
    SkillEvidenceResponse,
    SkillExtractionRequest,
    SkillExtractionResponse,
    SkillExtractionServiceStatus,
    DetectedOccupation,
    ExtractedSkillSpan,
    ExtractedSkillCrosswalks,
    SkillExtractionMetadata,
)
from app.schemas.auth import MessageResponse
from app.api.deps import get_current_user_profile
import sys
from pathlib import Path

# Ensure repo root is in sys.path for datasets package import
_repo_root = str(Path(__file__).resolve().parents[4])
if _repo_root not in sys.path:
    sys.path.insert(0, _repo_root)

# Lazy-load heavy ML dependencies to prevent 10+ minute cold-start blocking uvicorn
# These are only loaded on first request to /skills/extract endpoints
_SkillExtractionService = None
_default_config = None


def _get_skill_extraction_service():
    global _SkillExtractionService
    if _SkillExtractionService is None:
        from datasets.informal_skill_extraction.models.model_service import SkillExtractionService as _SES
        _SkillExtractionService = _SES
    return _SkillExtractionService


def _get_default_config():
    global _default_config
    if _default_config is None:
        from datasets.informal_skill_extraction.models.model_config import default_config as _dc
        _default_config = _dc
    return _default_config


catalog_router = APIRouter()
profile_skills_router = APIRouter()


# =============================================================================
# 0. AI Skill Extraction Endpoints (/skills/extract)
# =============================================================================

@catalog_router.get(
    "/extract/status",
    response_model=SkillExtractionServiceStatus,
    summary="Get AI Skill Extraction Service Status",
    description="Returns model architecture status, hardware execution device, and training safety gate condition.",
)
async def get_skill_extraction_status() -> SkillExtractionServiceStatus:
    SkillExtractionService = _get_skill_extraction_service()
    default_config = _get_default_config()
    status_info = SkillExtractionService.get_service_status()
    device_str = "Apple Silicon MPS" if default_config.get_device() == "mps" else "CPU"
    return SkillExtractionServiceStatus(
        status=status_info.get("status", "operational"),
        active_model="xlm_roberta_indian_mock_v1",
        device=device_str,
        training_safety_gate=status_info.get("training_safety_gate", "LOCKED (Genuine Indian worker records = 0, threshold = 500)"),
        genuine_worker_records=0,
        minimum_required_records=500,
        supported_occupations_count=10,
        canonical_catalogue_size=32,
        model_provenance="synthetic_mock_development",
        benchmark_type="SYNTHETIC DEVELOPMENT BENCHMARK",
    )


@catalog_router.post(
    "/extract",
    response_model=SkillExtractionResponse,
    summary="Extract Vocational Skills from Narrative",
    description=(
        "Extracts practical vocational competencies, tool proficiencies, and tasks from natural language "
        "descriptions across Hindi, Hinglish, and English, mapping each to canonical ontologies."
    ),
)
async def extract_skills_endpoint(
    payload: SkillExtractionRequest
) -> SkillExtractionResponse:
    SkillExtractionService = _get_skill_extraction_service()
    if not payload.text or not payload.text.strip():
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Input narrative text cannot be blank."
        )

    t0 = time.time()
    raw_res = SkillExtractionService.extract_from_narrative(
        text=payload.text,
        occupation_hint=payload.occupation_hint
    )
    latency_ms = (time.time() - t0) * 1000.0

    detected_occ = DetectedOccupation(
        occupation_id=raw_res["detected_occupation"]["occupation_id"],
        occupation_title=raw_res["detected_occupation"]["occupation_title"],
        confidence=raw_res["detected_occupation"]["confidence"],
    )

    extracted_spans = []
    for sp in raw_res.get("extracted_skills", []):
        crosswalks_data = sp.get("crosswalks", {})
        extracted_spans.append(
            ExtractedSkillSpan(
                span_id=sp["span_id"],
                extracted_skill=sp["extracted_skill"],
                normalized_skill=sp.get("normalized_skill", sp["extracted_skill"]),
                evidence_text=sp.get("evidence_text", sp["extracted_skill"]),
                start_offset=sp["start_offset"],
                end_offset=sp["end_offset"],
                skill_category=sp["skill_category"],
                category_confidence=sp["category_confidence"],
                canonical_skill=sp["canonical_skill"],
                canonical_skill_id=sp["canonical_skill_id"],
                mapping_status=sp["mapping_status"],
                is_unmapped_skill=sp["is_unmapped_skill"],
                mapping_confidence=sp["mapping_confidence"],
                human_review_required=sp["human_review_required"],
                crosswalks=ExtractedSkillCrosswalks(
                    esco_uri=crosswalks_data.get("esco_uri"),
                    onet_soc_code=crosswalks_data.get("onet_soc_code"),
                    nsqf_reference=crosswalks_data.get("nsqf_reference"),
                ),
            )
        )

    device_name = "Apple Silicon MPS" if default_config.get_device() == "mps" else "CPU"

    metadata = SkillExtractionMetadata(
        model_version="xlm_roberta_indian_mock_v1",
        inference_device=device_name,
        latency_ms=round(latency_ms, 2),
        training_safety_gate_status="LOCKED (Genuine Indian worker records = 0, threshold = 500)",
        model_provenance="synthetic_mock_development",
        benchmark_type="SYNTHETIC DEVELOPMENT BENCHMARK",
    )

    return SkillExtractionResponse(
        input_text=payload.text,
        detected_occupation=detected_occ,
        extracted_skills_count=len(extracted_spans),
        extracted_skills=extracted_spans,
        metadata=metadata,
    )



# =============================================================================
# 1. Global Skill Catalog Endpoints (/skills)
# =============================================================================

@catalog_router.get(
    "",
    response_model=List[SkillResponse],
    summary="List Standardized Skills Catalog",
    description="Searches and filters the global vocational competency catalog aligned to NSQF standards.",
)
async def list_skills_catalog(
    category: Optional[str] = Query(None, description="Filter by skill category"),
    search: Optional[str] = Query(None, description="Search skill name or description"),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
) -> List[SkillResponse]:
    stmt = select(Skill)

    if category:
        stmt = stmt.where(Skill.category == category)
    if search:
        pattern = f"%{search.strip()}%"
        stmt = stmt.where(or_(Skill.name.ilike(pattern), Skill.description.ilike(pattern)))

    stmt = stmt.order_by(Skill.name.asc()).limit(limit)
    skills = db.execute(stmt).scalars().all()
    return [SkillResponse.model_validate(s) for s in skills]


@catalog_router.post(
    "",
    response_model=SkillResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Add Skill to Catalog",
    description="Registers a new standardized trade or technical competency in the master catalog.",
)
async def create_catalog_skill(
    payload: SkillCreate,
    db: Session = Depends(get_db),
) -> SkillResponse:
    existing = db.execute(
        select(Skill).where(Skill.name.ilike(payload.name.strip()))
    ).scalar_one_or_none()

    if existing:
        return SkillResponse.model_validate(existing)

    new_skill = Skill(
        name=payload.name.strip(),
        category=payload.category.strip(),
        nsqf_level=payload.nsqf_level,
        description=payload.description,
    )
    db.add(new_skill)
    db.commit()
    db.refresh(new_skill)
    return SkillResponse.model_validate(new_skill)


@catalog_router.get(
    "/{skill_id}",
    response_model=SkillResponse,
    summary="Get Skill Details",
    description="Fetches full metadata and NSQF vocational level for a specific competency.",
)
async def get_skill_by_id(
    skill_id: uuid.UUID,
    db: Session = Depends(get_db),
) -> SkillResponse:
    skill = db.execute(select(Skill).where(Skill.id == skill_id)).scalar_one_or_none()
    if not skill:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Skill with ID {skill_id} not found in catalog.",
        )
    return SkillResponse.model_validate(skill)


# =============================================================================
# 2. User Profile Skills (/profiles/me/skills)
# =============================================================================

@profile_skills_router.get(
    "/me/skills",
    response_model=List[UserSkillResponse],
    summary="List Authenticated User's Skills",
    description="Lists all competencies mapped to the user profile with verification status, proficiency, and evidence.",
)
async def get_my_skills(
    profile: UserProfile = Depends(get_current_user_profile),
    db: Session = Depends(get_db),
) -> List[UserSkillResponse]:
    user_skills = db.execute(
        select(UserSkill)
        .options(
            joinedload(UserSkill.skill),
            joinedload(UserSkill.evidences),
        )
        .where(UserSkill.profile_id == profile.id)
        .order_by(UserSkill.created_at.desc())
    ).unique().scalars().all()

    return [UserSkillResponse.model_validate(us) for us in user_skills]


@profile_skills_router.post(
    "/me/skills",
    response_model=UserSkillResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Add Skill to User Profile",
    description="Links a catalog competency to the user's vocational profile.",
)
async def add_skill_to_profile(
    payload: UserSkillCreate,
    profile: UserProfile = Depends(get_current_user_profile),
    db: Session = Depends(get_db),
) -> UserSkillResponse:
    target_skill_id = payload.skill_id

    # If skill_name provided instead of skill_id, resolve or create it
    if not target_skill_id:
        if not payload.skill_name or not payload.skill_name.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Either skill_id or skill_name must be provided.",
            )
        skill_name = payload.skill_name.strip()
        matched = db.execute(
            select(Skill).where(Skill.name.ilike(skill_name))
        ).scalar_one_or_none()

        if matched:
            target_skill_id = matched.id
        else:
            new_skill = Skill(
                name=skill_name,
                category=payload.category or "Vocational Skill",
                description=f"User-reported competency: {skill_name}",
            )
            db.add(new_skill)
            db.flush()
            target_skill_id = new_skill.id

    # Check for duplicate link
    existing_link = db.execute(
        select(UserSkill).where(
            UserSkill.profile_id == profile.id,
            UserSkill.skill_id == target_skill_id,
        )
    ).scalar_one_or_none()

    if existing_link:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This skill is already listed on your profile.",
        )

    user_skill = UserSkill(
        profile_id=profile.id,
        skill_id=target_skill_id,
        verification_status=payload.verification_status,
        proficiency_level=payload.proficiency_level,
        years_practiced=payload.years_practiced,
        confidence_score=payload.confidence_score,
    )
    db.add(user_skill)
    db.commit()
    db.refresh(user_skill)

    # Re-fetch with joined relationships
    full_user_skill = db.execute(
        select(UserSkill)
        .options(joinedload(UserSkill.skill), joinedload(UserSkill.evidences))
        .where(UserSkill.id == user_skill.id)
    ).unique().scalar_one()

    return UserSkillResponse.model_validate(full_user_skill)


@profile_skills_router.put(
    "/me/skills/{skill_id}",
    response_model=UserSkillResponse,
    summary="Update User Skill Level or Verification",
    description="Updates proficiency level, years practiced, or assessment status for a user skill.",
)
async def update_user_skill(
    skill_id: uuid.UUID,
    payload: UserSkillUpdate,
    profile: UserProfile = Depends(get_current_user_profile),
    db: Session = Depends(get_db),
) -> UserSkillResponse:
    # skill_id can match either the UserSkill.id or UserSkill.skill_id
    user_skill = db.execute(
        select(UserSkill)
        .options(joinedload(UserSkill.skill), joinedload(UserSkill.evidences))
        .where(
            UserSkill.profile_id == profile.id,
            or_(UserSkill.id == skill_id, UserSkill.skill_id == skill_id),
        )
    ).unique().scalar_one_or_none()

    if not user_skill:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Skill record not found on your profile.",
        )

    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user_skill, field, value)

    db.commit()
    db.refresh(user_skill)
    return UserSkillResponse.model_validate(user_skill)


@profile_skills_router.delete(
    "/me/skills/{skill_id}",
    response_model=MessageResponse,
    summary="Remove Skill from Profile",
    description="Removes a skill competency from the authenticated user's profile.",
)
async def delete_user_skill(
    skill_id: uuid.UUID,
    profile: UserProfile = Depends(get_current_user_profile),
    db: Session = Depends(get_db),
):
    user_skill = db.execute(
        select(UserSkill).where(
            UserSkill.profile_id == profile.id,
            or_(UserSkill.id == skill_id, UserSkill.skill_id == skill_id),
        )
    ).scalar_one_or_none()

    if not user_skill:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Skill record not found on your profile.",
        )

    db.delete(user_skill)
    db.commit()
    return MessageResponse(success=True, message="Skill removed from profile successfully.")


# =============================================================================
# 3. Skill Evidence (/profiles/me/skills/{user_skill_id}/evidence)
# =============================================================================

@profile_skills_router.post(
    "/me/skills/{user_skill_id}/evidence",
    response_model=SkillEvidenceResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Attach Practical Evidence to Skill",
    description="Attaches diagnostic test scores, work photos, or supervisor endorsements.",
)
async def attach_skill_evidence(
    user_skill_id: uuid.UUID,
    payload: SkillEvidenceCreate,
    profile: UserProfile = Depends(get_current_user_profile),
    db: Session = Depends(get_db),
) -> SkillEvidenceResponse:
    user_skill = db.execute(
        select(UserSkill).where(
            UserSkill.id == user_skill_id,
            UserSkill.profile_id == profile.id,
        )
    ).scalar_one_or_none()

    if not user_skill:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User skill not found under your profile.",
        )

    evidence = SkillEvidence(
        user_skill_id=user_skill.id,
        evidence_type=payload.evidence_type,
        title=payload.title,
        description=payload.description,
        file_url=payload.file_url,
        score_achieved=payload.score_achieved,
    )
    db.add(evidence)

    # If practical score is above 80%, upgrade status to assessed
    if payload.score_achieved and payload.score_achieved >= 80:
        user_skill.verification_status = "assessed"

    db.commit()
    db.refresh(evidence)
    return SkillEvidenceResponse.model_validate(evidence)
