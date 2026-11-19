"""
User Profile, Education, Experience, and Career Preferences Management API.
Guarantees strict user isolation and profile ownership.
"""

from typing import List
import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.core.database import get_db
from app.models.profile import UserProfile, Education, WorkExperience, CareerPreference
from app.schemas.profile import (
    ProfileUpdateRequest,
    ProfileResponse,
    EducationCreate,
    EducationResponse,
    WorkExperienceCreate,
    WorkExperienceUpdate,
    WorkExperienceResponse,
    CareerPreferenceUpdate,
    CareerPreferenceResponse,
)
from app.schemas.auth import MessageResponse
from app.api.deps import get_current_user_profile

router = APIRouter()


# =============================================================================
# 1. User Profile (/me)
# =============================================================================

@router.get(
    "/me",
    response_model=ProfileResponse,
    summary="Get Current User Profile",
    description="Fetches the vocational profile of the authenticated user.",
)
async def get_my_profile(
    profile: UserProfile = Depends(get_current_user_profile),
) -> ProfileResponse:
    return ProfileResponse.model_validate(profile)


@router.put(
    "/me",
    response_model=ProfileResponse,
    summary="Update Current User Profile",
    description="Updates headline, bio, location, years of experience, or preferred trade.",
)
async def update_my_profile(
    payload: ProfileUpdateRequest,
    profile: UserProfile = Depends(get_current_user_profile),
    db: Session = Depends(get_db),
) -> ProfileResponse:
    update_data = payload.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(profile, field, value)

    # Recalculate completion percentage dynamically
    score = 20
    if profile.headline:
        score += 15
    if profile.bio:
        score += 15
    if profile.location:
        score += 10
    if profile.trade_category:
        score += 20
    if profile.years_of_experience and profile.years_of_experience > 0:
        score += 20
    profile.completion_percentage = min(score, 100)

    db.commit()
    db.refresh(profile)
    return ProfileResponse.model_validate(profile)


# =============================================================================
# 2. Education CRUD
# =============================================================================

@router.get(
    "/education",
    response_model=List[EducationResponse],
    summary="List User Education Records",
    description="Lists all formal and vocational education credentials for the current user.",
)
async def get_education_list(
    profile: UserProfile = Depends(get_current_user_profile),
    db: Session = Depends(get_db),
) -> List[EducationResponse]:
    records = db.execute(
        select(Education)
        .where(Education.profile_id == profile.id)
        .order_by(Education.start_date.desc().nullslast())
    ).scalars().all()

    return [EducationResponse.model_validate(r) for r in records]


@router.post(
    "/education",
    response_model=EducationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Add Education Credential",
    description="Creates a new vocational or academic education record under the authenticated profile.",
)
async def create_education(
    payload: EducationCreate,
    profile: UserProfile = Depends(get_current_user_profile),
    db: Session = Depends(get_db),
) -> EducationResponse:
    record = Education(
        profile_id=profile.id,
        institution=payload.institution,
        degree_or_certificate=payload.degree_or_certificate,
        field_of_study=payload.field_of_study,
        start_date=payload.start_date,
        end_date=payload.end_date,
        is_current=payload.is_current,
        grade_or_score=payload.grade_or_score,
        description=payload.description,
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return EducationResponse.model_validate(record)


@router.delete(
    "/education/{education_id}",
    response_model=MessageResponse,
    summary="Delete Education Credential",
    description="Safely deletes an education credential owned by the current user.",
)
async def delete_education(
    education_id: uuid.UUID,
    profile: UserProfile = Depends(get_current_user_profile),
    db: Session = Depends(get_db),
):
    record = db.execute(
        select(Education).where(
            Education.id == education_id,
            Education.profile_id == profile.id,
        )
    ).scalar_one_or_none()

    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Education record not found or not owned by you.",
        )

    db.delete(record)
    db.commit()
    return MessageResponse(success=True, message="Education record deleted successfully.")


# =============================================================================
# 3. Work Experience CRUD
# =============================================================================

@router.get(
    "/experience",
    response_model=List[WorkExperienceResponse],
    summary="List Work Experience Records",
    description="Lists all workplace, workshop, and informal trade experiences for the current user.",
)
async def get_experience_list(
    profile: UserProfile = Depends(get_current_user_profile),
    db: Session = Depends(get_db),
) -> List[WorkExperienceResponse]:
    records = db.execute(
        select(WorkExperience)
        .where(WorkExperience.profile_id == profile.id)
        .order_by(WorkExperience.start_date.desc().nullslast())
    ).scalars().all()

    return [WorkExperienceResponse.model_validate(r) for r in records]


@router.post(
    "/experience",
    response_model=WorkExperienceResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Add Work Experience Record",
    description="Logs a new formal or informal vocational experience record under the user profile.",
)
async def create_experience(
    payload: WorkExperienceCreate,
    profile: UserProfile = Depends(get_current_user_profile),
    db: Session = Depends(get_db),
) -> WorkExperienceResponse:
    record = WorkExperience(
        profile_id=profile.id,
        job_title=payload.job_title,
        company_or_workshop=payload.company_or_workshop,
        location=payload.location,
        employment_type=payload.employment_type or "Full-time",
        start_date=payload.start_date,
        end_date=payload.end_date,
        is_current=payload.is_current,
        description=payload.description,
        trade_tools_used=payload.trade_tools_used,
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return WorkExperienceResponse.model_validate(record)


@router.put(
    "/experience/{experience_id}",
    response_model=WorkExperienceResponse,
    summary="Update Work Experience Record",
    description="Updates an existing work experience record owned by the authenticated user.",
)
async def update_experience(
    experience_id: uuid.UUID,
    payload: WorkExperienceUpdate,
    profile: UserProfile = Depends(get_current_user_profile),
    db: Session = Depends(get_db),
) -> WorkExperienceResponse:
    record = db.execute(
        select(WorkExperience).where(
            WorkExperience.id == experience_id,
            WorkExperience.profile_id == profile.id,
        )
    ).scalar_one_or_none()

    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Work experience record not found or not owned by you.",
        )

    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(record, field, value)

    db.commit()
    db.refresh(record)
    return WorkExperienceResponse.model_validate(record)


@router.delete(
    "/experience/{experience_id}",
    response_model=MessageResponse,
    summary="Delete Work Experience Record",
    description="Deletes a work experience record owned by the authenticated user.",
)
async def delete_experience(
    experience_id: uuid.UUID,
    profile: UserProfile = Depends(get_current_user_profile),
    db: Session = Depends(get_db),
):
    record = db.execute(
        select(WorkExperience).where(
            WorkExperience.id == experience_id,
            WorkExperience.profile_id == profile.id,
        )
    ).scalar_one_or_none()

    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Work experience record not found or not owned by you.",
        )

    db.delete(record)
    db.commit()
    return MessageResponse(success=True, message="Work experience record deleted successfully.")


# =============================================================================
# 4. Career Preferences
# =============================================================================

@router.get(
    "/preferences",
    response_model=CareerPreferenceResponse,
    summary="Get Career Preferences",
    description="Retrieves the target role, expected salary, and shift preferences for the current user.",
)
async def get_career_preferences(
    profile: UserProfile = Depends(get_current_user_profile),
    db: Session = Depends(get_db),
) -> CareerPreferenceResponse:
    pref = db.execute(
        select(CareerPreference).where(CareerPreference.profile_id == profile.id)
    ).scalar_one_or_none()

    if not pref:
        pref = CareerPreference(
            profile_id=profile.id,
            target_role=profile.headline or "Target Vocational Role",
            open_to_relocation=False,
        )
        db.add(pref)
        db.commit()
        db.refresh(pref)

    return CareerPreferenceResponse.model_validate(pref)


@router.put(
    "/preferences",
    response_model=CareerPreferenceResponse,
    summary="Update Career Preferences",
    description="Updates target salary, location flexibility, and role goals for the current user.",
)
async def update_career_preferences(
    payload: CareerPreferenceUpdate,
    profile: UserProfile = Depends(get_current_user_profile),
    db: Session = Depends(get_db),
) -> CareerPreferenceResponse:
    pref = db.execute(
        select(CareerPreference).where(CareerPreference.profile_id == profile.id)
    ).scalar_one_or_none()

    if not pref:
        pref = CareerPreference(profile_id=profile.id)
        db.add(pref)

    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(pref, field, value)

    db.commit()
    db.refresh(pref)
    return CareerPreferenceResponse.model_validate(pref)

