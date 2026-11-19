"""
API Router for Employer and Job Opportunity Management.
"""

from datetime import date
from typing import List, Optional
import uuid
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select, or_

from app.core.database import get_db
from app.api.deps import get_current_active_user, require_admin
from app.models.user import User
from app.models.job import Employer, JobListing, JobRequirement, JobSkill
from app.schemas.career_domain import (
    EmployerCreate,
    EmployerResponse,
    JobListingCreate,
    JobListingUpdate,
    JobListingResponse,
)

router = APIRouter()


# =============================================================================
# Employer Endpoints
# =============================================================================

@router.get("/employers", response_model=List[EmployerResponse])
def list_employers(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """List verified corporate, industrial, and workshop employers."""
    return db.execute(select(Employer).order_by(Employer.name.asc())).scalars().all()


@router.post("/employers", response_model=EmployerResponse, status_code=status.HTTP_201_CREATED)
def create_employer(
    payload: EmployerCreate,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    """Administrator endpoint: register a new verified employer."""
    existing = db.execute(
        select(Employer).where(Employer.name == payload.name)
    ).scalar_one_or_none()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An employer with this name already exists.",
        )

    employer = Employer(
        name=payload.name,
        website=payload.website,
        description=payload.description,
        logo_url=payload.logo_url,
        location=payload.location,
        is_verified=payload.is_verified,
    )
    db.add(employer)
    db.commit()
    db.refresh(employer)
    return employer


# =============================================================================
# Job Listing Endpoints
# =============================================================================

@router.get("", response_model=List[JobListingResponse])
def list_jobs(
    search: Optional[str] = Query(None, description="Search term for job title or description"),
    location: Optional[str] = Query(None, description="Filter by geographic location"),
    employment_type: Optional[str] = Query(None, description="Filter by employment type"),
    max_experience: Optional[int] = Query(None, ge=0, description="Maximum required years of experience"),
    min_salary: Optional[int] = Query(None, ge=0, description="Minimum salary threshold"),
    include_expired: bool = Query(False, description="Whether to include expired jobs"),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Search and browse formal trade opportunities with multifaceted filtering."""
    query = (
        select(JobListing)
        .options(
            joinedload(JobListing.employer),
            joinedload(JobListing.requirements),
            joinedload(JobListing.skills),
        )
        .where(JobListing.is_active == True)  # noqa: E712
    )

    if not include_expired:
        today = date.today()
        query = query.where(
            or_(
                JobListing.expiry_date.is_(None),
                JobListing.expiry_date >= today,
            )
        )

    if location:
        query = query.where(JobListing.location.ilike(f"%{location.strip()}%"))
    if employment_type:
        query = query.where(JobListing.employment_type == employment_type)
    if max_experience is not None:
        query = query.where(JobListing.experience_required_years <= max_experience)
    if min_salary is not None:
        query = query.where(JobListing.salary_max >= min_salary)
    if search:
        search_filter = f"%{search.strip()}%"
        query = query.where(
            or_(
                JobListing.title.ilike(search_filter),
                JobListing.description.ilike(search_filter),
            )
        )

    query = query.order_by(JobListing.created_at.desc()).offset(offset).limit(limit)
    return db.execute(query).unique().scalars().all()


@router.get("/{job_id}", response_model=JobListingResponse)
def get_job(
    job_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Retrieve complete job listing details including requirements and skills."""
    job = db.execute(
        select(JobListing)
        .options(
            joinedload(JobListing.employer),
            joinedload(JobListing.requirements),
            joinedload(JobListing.skills),
        )
        .where(JobListing.id == job_id)
    ).unique().scalar_one_or_none()

    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Job listing '{job_id}' not found.",
        )
    return job


@router.post("", response_model=JobListingResponse, status_code=status.HTTP_201_CREATED)
def create_job(
    payload: JobListingCreate,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    """Administrator endpoint: create a formal vocational trade job listing."""
    employer = db.execute(
        select(Employer).where(Employer.id == payload.employer_id)
    ).scalar_one_or_none()
    if not employer:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Specified employer does not exist.",
        )

    job = JobListing(
        employer_id=payload.employer_id,
        title=payload.title,
        location=payload.location,
        description=payload.description,
        salary_min=payload.salary_min,
        salary_max=payload.salary_max,
        salary_currency=payload.salary_currency,
        employment_type=payload.employment_type,
        experience_required_years=payload.experience_required_years,
        education_required=payload.education_required,
        source_type=payload.source_type,
        source_url=payload.source_url,
        posted_date=date.today(),
        expiry_date=payload.expiry_date,
        is_verified=True,
        is_active=True,
    )
    db.add(job)
    db.flush()

    for req in payload.requirements:
        db.add(
            JobRequirement(
                job_id=job.id,
                requirement_text=req.requirement_text,
                is_mandatory=req.is_mandatory,
            )
        )

    for sk in payload.skills:
        db.add(
            JobSkill(
                job_id=job.id,
                skill_id=sk.skill_id,
                is_mandatory=sk.is_mandatory,
                min_years=sk.min_years,
            )
        )

    db.commit()
    db.refresh(job)
    return job


@router.put("/{job_id}", response_model=JobListingResponse)
def update_job(
    job_id: uuid.UUID,
    payload: JobListingUpdate,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    """Administrator endpoint: update an existing job listing."""
    job = db.execute(
        select(JobListing).where(JobListing.id == job_id)
    ).scalar_one_or_none()

    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job listing not found.",
        )

    for field, val in payload.model_dump(exclude_unset=True).items():
        setattr(job, field, val)

    db.commit()
    db.refresh(job)
    return job


@router.delete("/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_job(
    job_id: uuid.UUID,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    """Administrator endpoint: delete a job listing."""
    job = db.execute(
        select(JobListing).where(JobListing.id == job_id)
    ).scalar_one_or_none()

    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job listing not found.",
        )

    db.delete(job)
    db.commit()
    return None

