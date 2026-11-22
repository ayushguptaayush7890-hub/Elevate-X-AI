"""
API Router for Multi-Website Real Job Aggregator, Matching, and Saved Jobs.
Provides multifaceted search, provider telemetry, AI compatibility benchmarks,
and direct application links.
"""

from datetime import date, datetime, timedelta
from typing import List, Optional, Dict, Any
import uuid
import json
import logging
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select, or_, and_, func

from app.core.database import get_db
from app.api.deps import get_current_active_user, get_optional_current_user, require_admin
from app.models.user import User
from app.models.job import Employer, JobListing, JobRequirement, JobSkill
from app.models.application import SavedJob
from app.schemas.career_domain import (
    EmployerCreate,
    EmployerResponse,
    JobListingCreate,
    JobListingUpdate,
    JobListingResponse,
)
from app.services.job_aggregator.aggregator_service import JobAggregatorService
from app.services.job_matching_service import JobMatchingService

logger = logging.getLogger(__name__)

router = APIRouter()


def _format_job_response(
    job: JobListing,
    candidate_features: Dict[str, Any],
    saved_job_ids: set,
) -> JobListingResponse:
    """Helper to convert ORM JobListing to schema with AI matching and skills list."""
    # 1. Parse skills list
    skills_list = []
    if job.required_skills_json:
        try:
            skills_list = json.loads(job.required_skills_json)
        except Exception:
            skills_list = []

    if not skills_list and job.requirements:
        for r in job.requirements:
            skills_list.append(r.requirement_text.replace("Demonstrated proficiency in ", ""))

    # 2. Calculate explainable match details
    match_details = JobMatchingService.calculate_compatibility(candidate_features, job)

    is_saved = job.id in saved_job_ids

    return JobListingResponse(
        id=job.id,
        employer_id=job.employer_id,
        employer=job.employer,
        title=job.title,
        location=job.location,
        country=getattr(job, "country", "India") or "India",
        description=job.description,
        salary_min=job.salary_min,
        salary_max=job.salary_max,
        salary_currency=job.salary_currency or "INR",
        employment_type=job.employment_type or "Full-time",
        experience_required_years=job.experience_required_years or 0,
        experience_min_years=job.experience_min_years,
        experience_max_years=job.experience_max_years,
        education_required=job.education_required,
        source_type=job.source_type or "aggregator",
        source_provider=job.source_provider or "Direct",
        source_url=job.source_url,
        application_url=job.application_url or job.source_url,
        provider_job_id=job.provider_job_id,
        work_mode=job.work_mode or "On-site",
        required_skills_list=skills_list,
        last_verified_at=job.last_verified_at or job.created_at,
        listing_status=job.listing_status or "active",
        match_details=match_details,
        is_saved=is_saved,
        posted_date=job.posted_date or date.today(),
        expiry_date=job.expiry_date,
        is_verified=job.is_verified,
        is_active=job.is_active,
        requirements=job.requirements or [],
        skills=job.skills or [],
        created_at=job.created_at,
    )


# =============================================================================
# Provider Telemetry & Aggregation Synchronization
# =============================================================================

@router.get("/providers", response_model=List[Dict[str, Any]])
def get_providers_status(
    db: Session = Depends(get_db),
):
    """
    Returns live connection and evaluation metadata for all 12 job platforms.
    """
    aggregator = JobAggregatorService()
    return aggregator.get_all_provider_statuses(db)


@router.post("/sync", response_model=Dict[str, Any])
def sync_job_providers(
    limit_per_source: int = Query(50, ge=5, le=100),
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user),
):
    """
    Triggers live synchronization and duplicate-checked ingestion across active feeds.
    """
    aggregator = JobAggregatorService()
    result = aggregator.sync_active_providers(db, limit_per_source=limit_per_source)
    return result


# =============================================================================
# Job Search & Multifaceted Filtering
# =============================================================================

@router.get("", response_model=List[JobListingResponse])
def list_jobs(
    search: Optional[str] = Query(None, description="Search by job title, company, or skill"),
    location: Optional[str] = Query(None, description="Filter by location (e.g. India, Bengaluru, Noida, International)"),
    country: Optional[str] = Query("India", description="Filter by country: India (default), International, or All"),
    role_category: Optional[str] = Query(None, description="Filter by role category (e.g. AI Engineer, Python Developer)"),
    source: Optional[str] = Query(None, description="Filter by source provider (e.g. Authorized Feeds, Adzuna, Jooble, All)"),
    work_mode: Optional[str] = Query(None, description="Filter by work mode: Remote, Hybrid, On-site, All"),
    employment_type: Optional[str] = Query(None, description="Filter by employment type"),
    max_experience: Optional[int] = Query(None, ge=0, description="Maximum required years of experience"),
    min_salary: Optional[int] = Query(None, ge=0, description="Minimum salary threshold"),
    min_compatibility: Optional[int] = Query(None, ge=0, le=100, description="Minimum AI compatibility score (0-100)"),
    freshness_days: Optional[int] = Query(None, ge=1, le=90, description="Max age in days"),
    saved_only: bool = Query(False, description="Filter for saved jobs only"),
    include_expired: bool = Query(False, description="Whether to include expired jobs"),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user),
):
    """
    Search real aggregated opportunities across multiple external job boards.
    India-first by default with authentic corporate ATS and Indian portal feeds.
    Computes explainable AI compatibility scores for the active candidate profile.
    """
    # 1. Ensure initial real Indian jobs exist in DB
    indian_jobs_count = db.execute(
        select(func.count(JobListing.id)).where(JobListing.country == "India")
    ).scalar() or 0
    if indian_jobs_count < 10:
        logger.info(f"Database contains {indian_jobs_count} Indian jobs. Running active provider sync...")
        aggregator = JobAggregatorService()
        aggregator.sync_active_providers(db, limit_per_source=50)

    # 2. Extract Candidate Features for Explainable Matching
    user_id = current_user.id if current_user else None
    candidate_features = JobMatchingService.get_candidate_profile_features(db, user_id=user_id)

    # 3. Get Saved Job IDs for User
    saved_job_ids = set()
    if user_id:
        saved_rows = db.execute(
            select(SavedJob.job_id).where(SavedJob.user_id == user_id)
        ).scalars().all()
        saved_job_ids = set(saved_rows)
    else:
        demo_user = db.execute(select(User).where(User.email == "live.demo@elevatex.ai")).scalar_one_or_none()
        if demo_user:
            saved_rows = db.execute(
                select(SavedJob.job_id).where(SavedJob.user_id == demo_user.id)
            ).scalars().all()
            saved_job_ids = set(saved_rows)

    # 4. Build Filter Query
    query = (
        select(JobListing)
        .options(
            joinedload(JobListing.employer),
            joinedload(JobListing.requirements),
            joinedload(JobListing.skills),
        )
    )

    if not include_expired:
        today = date.today()
        query = query.where(
            and_(
                JobListing.is_active == True,
                or_(
                    JobListing.expiry_date.is_(None),
                    JobListing.expiry_date >= today,
                ),
            )
        )

    # Country & Location Filtering (India-First default)
    loc_clean = (location or "").strip()
    loc_lower = loc_clean.lower()
    c_lower = (country or "India").strip().lower()

    if loc_lower == "international" or c_lower == "international":
        query = query.where(JobListing.country == "International")
    elif c_lower == "all" and loc_lower in ["", "all"]:
        # Show all across globe
        pass
    else:
        # Default to India
        query = query.where(JobListing.country == "India")

        if loc_lower not in ["", "all", "india", "all indian cities"]:
            if loc_lower in ["delhi ncr", "delhi", "ncr"]:
                query = query.where(
                    or_(
                        JobListing.location.ilike("%delhi%"),
                        JobListing.location.ilike("%ncr%"),
                        JobListing.location.ilike("%noida%"),
                        JobListing.location.ilike("%gurugram%"),
                        JobListing.location.ilike("%gurgaon%"),
                        JobListing.location.ilike("%meerut%"),
                    )
                )
            elif loc_lower in ["gurugram", "gurgaon"]:
                query = query.where(
                    or_(
                        JobListing.location.ilike("%gurugram%"),
                        JobListing.location.ilike("%gurgaon%"),
                    )
                )
            elif loc_lower in ["bengaluru", "bangalore"]:
                query = query.where(
                    or_(
                        JobListing.location.ilike("%bengaluru%"),
                        JobListing.location.ilike("%bangalore%"),
                    )
                )
            elif loc_lower in ["noida", "greater noida"]:
                query = query.where(JobListing.location.ilike("%noida%"))
            else:
                query = query.where(JobListing.location.ilike(f"%{loc_clean}%"))

    # Role Category filter
    if role_category and role_category.strip().lower() not in ["all", "all roles"]:
        rc = role_category.strip().lower()
        if rc in ["ai engineer", "artificial intelligence", "ai"]:
            query = query.where(
                or_(
                    JobListing.title.ilike("%ai%"),
                    JobListing.title.ilike("%artificial intelligence%"),
                    JobListing.title.ilike("%machine learning%"),
                    JobListing.title.ilike("%ml%"),
                    JobListing.required_skills_json.ilike("%ai%"),
                    JobListing.required_skills_json.ilike("%machine learning%"),
                )
            )
        elif rc in ["machine learning engineer", "ml engineer"]:
            query = query.where(
                or_(
                    JobListing.title.ilike("%machine learning%"),
                    JobListing.title.ilike("%ml%"),
                    JobListing.required_skills_json.ilike("%machine learning%"),
                )
            )
        elif rc in ["data scientist"]:
            query = query.where(
                or_(
                    JobListing.title.ilike("%data scientist%"),
                    JobListing.title.ilike("%data science%"),
                    JobListing.required_skills_json.ilike("%data scientist%"),
                )
            )
        elif rc in ["data analyst"]:
            query = query.where(
                or_(
                    JobListing.title.ilike("%data analyst%"),
                    JobListing.title.ilike("%analytics%"),
                    JobListing.required_skills_json.ilike("%data analyst%"),
                    JobListing.required_skills_json.ilike("%sql%"),
                )
            )
        elif rc in ["python developer", "python"]:
            query = query.where(
                or_(
                    JobListing.title.ilike("%python%"),
                    JobListing.required_skills_json.ilike("%python%"),
                )
            )
        elif rc in ["java developer", "java"]:
            query = query.where(
                or_(
                    JobListing.title.ilike("%java%"),
                    JobListing.required_skills_json.ilike("%java%"),
                )
            )
        elif rc in ["software engineer"]:
            query = query.where(
                or_(
                    JobListing.title.ilike("%software%"),
                    JobListing.title.ilike("%engineer%"),
                    JobListing.title.ilike("%developer%"),
                )
            )
        elif rc in ["frontend developer", "frontend"]:
            query = query.where(
                or_(
                    JobListing.title.ilike("%frontend%"),
                    JobListing.title.ilike("%front-end%"),
                    JobListing.title.ilike("%react%"),
                    JobListing.required_skills_json.ilike("%react%"),
                )
            )
        elif rc in ["backend developer", "backend"]:
            query = query.where(
                or_(
                    JobListing.title.ilike("%backend%"),
                    JobListing.title.ilike("%back-end%"),
                    JobListing.title.ilike("%api%"),
                )
            )
        elif rc in ["full stack developer", "full stack"]:
            query = query.where(
                or_(
                    JobListing.title.ilike("%full stack%"),
                    JobListing.title.ilike("%fullstack%"),
                )
            )
        elif rc in ["devops engineer", "devops"]:
            query = query.where(
                or_(
                    JobListing.title.ilike("%devops%"),
                    JobListing.title.ilike("%site reliability%"),
                    JobListing.title.ilike("%sre%"),
                    JobListing.title.ilike("%infrastructure%"),
                )
            )
        elif rc in ["cloud engineer", "cloud"]:
            query = query.where(
                or_(
                    JobListing.title.ilike("%cloud%"),
                    JobListing.title.ilike("%aws%"),
                    JobListing.title.ilike("%azure%"),
                )
            )
        elif rc in ["cybersecurity analyst", "cybersecurity", "security"]:
            query = query.where(
                or_(
                    JobListing.title.ilike("%security%"),
                    JobListing.title.ilike("%cyber%"),
                )
            )
        elif rc in ["business analyst"]:
            query = query.where(
                or_(
                    JobListing.title.ilike("%business analyst%"),
                    JobListing.title.ilike("%product analyst%"),
                )
            )
        elif rc in ["ui/ux designer", "ui/ux", "ux designer"]:
            query = query.where(
                or_(
                    JobListing.title.ilike("%ui%"),
                    JobListing.title.ilike("%ux%"),
                    JobListing.title.ilike("%design%"),
                )
            )
        elif rc in ["internships", "internship", "intern"]:
            query = query.where(
                or_(
                    JobListing.title.ilike("%intern%"),
                    JobListing.employment_type.ilike("%intern%"),
                )
            )
        elif rc in ["fresher jobs", "fresher"]:
            query = query.where(
                or_(
                    JobListing.title.ilike("%associate%"),
                    JobListing.title.ilike("%early talent%"),
                    JobListing.title.ilike("%graduate%"),
                    JobListing.experience_required_years == 0,
                )
            )
        else:
            query = query.where(
                or_(
                    JobListing.title.ilike(f"%{rc}%"),
                    JobListing.description.ilike(f"%{rc}%"),
                    JobListing.required_skills_json.ilike(f"%{rc}%"),
                )
            )

    # Source filter
    if source and source.lower() != "all":
        query = query.where(JobListing.source_provider.ilike(f"%{source.strip()}%"))

    # Work Mode filter
    if work_mode and work_mode.lower() != "all":
        query = query.where(JobListing.work_mode.ilike(f"%{work_mode.strip()}%"))

    # Employment type
    if employment_type and employment_type.lower() != "all":
        query = query.where(JobListing.employment_type == employment_type)

    # Experience
    if max_experience is not None:
        query = query.where(JobListing.experience_required_years <= max_experience)

    # Salary
    if min_salary is not None:
        query = query.where(JobListing.salary_max >= min_salary)

    # Freshness
    if freshness_days is not None:
        cutoff = date.today() - timedelta(days=freshness_days)
        query = query.where(JobListing.posted_date >= cutoff)

    # Search keyword
    if search:
        search_filter = f"%{search.strip()}%"
        query = query.where(
            or_(
                JobListing.title.ilike(search_filter),
                JobListing.description.ilike(search_filter),
                JobListing.required_skills_json.ilike(search_filter),
                JobListing.location.ilike(search_filter),
            )
        )

    # Saved only
    if saved_only:
        if not saved_job_ids:
            return []
        query = query.where(JobListing.id.in_(list(saved_job_ids)))

    query = query.order_by(JobListing.posted_date.desc(), JobListing.created_at.desc())
    jobs = db.execute(query).unique().scalars().all()

    # 5. Format responses and filter by AI match score if requested
    results: List[JobListingResponse] = []
    for j in jobs:
        resp = _format_job_response(j, candidate_features, saved_job_ids)
        if min_compatibility is not None:
            score = (resp.match_details or {}).get("match_score", 0)
            if score < min_compatibility:
                continue
        results.append(resp)

    # Pagination
    return results[offset : offset + limit]


# =============================================================================
# Saved Jobs (Bookmarks)
# =============================================================================

@router.get("/saved/my", response_model=List[JobListingResponse])
def get_my_saved_jobs(
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user),
):
    """Returns saved bookmarks for the active user."""
    user = current_user
    if not user:
        user = db.execute(select(User).where(User.email == "live.demo@elevatex.ai")).scalar_one_or_none()

    if not user:
        return []

    saved_rows = db.execute(
        select(JobListing)
        .join(SavedJob, SavedJob.job_id == JobListing.id)
        .where(SavedJob.user_id == user.id)
        .options(
            joinedload(JobListing.employer),
            joinedload(JobListing.requirements),
            joinedload(JobListing.skills),
        )
        .order_by(SavedJob.saved_at.desc())
    ).unique().scalars().all()

    candidate_features = JobMatchingService.get_candidate_profile_features(db, user_id=user.id)
    saved_ids = {j.id for j in saved_rows}

    return [_format_job_response(j, candidate_features, saved_ids) for j in saved_rows]


@router.post("/{job_id}/save", response_model=Dict[str, Any])
def toggle_save_job(
    job_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user),
):
    """Toggles bookmarking a job listing."""
    user = current_user
    if not user:
        user = db.execute(select(User).where(User.email == "live.demo@elevatex.ai")).scalar_one_or_none()
        if not user:
            user = db.execute(select(User).where(User.is_active == True)).first()
            if user:
                user = user[0]

    if not user:
        raise HTTPException(status_code=401, detail="Authentication required to save jobs")

    job = db.execute(select(JobListing).where(JobListing.id == job_id)).scalar_one_or_none()
    if not job:
        raise HTTPException(status_code=404, detail="Job listing not found")

    existing_saved = db.execute(
        select(SavedJob).where(
            and_(SavedJob.user_id == user.id, SavedJob.job_id == job_id)
        )
    ).scalar_one_or_none()

    if existing_saved:
        db.delete(existing_saved)
        db.commit()
        return {"saved": False, "message": "Job removed from saved list", "job_id": str(job_id)}
    else:
        new_save = SavedJob(user_id=user.id, job_id=job.id)
        db.add(new_save)
        db.commit()
        return {"saved": True, "message": "Job saved to application tracker", "job_id": str(job_id)}


# =============================================================================
# Single Job Detail
# =============================================================================

@router.get("/{job_id}", response_model=JobListingResponse)
def get_job(
    job_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user),
):
    """Retrieve complete job listing details including requirements, skills, and AI match."""
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

    user_id = current_user.id if current_user else None
    candidate_features = JobMatchingService.get_candidate_profile_features(db, user_id=user_id)

    saved_job_ids = set()
    if user_id:
        saved_rows = db.execute(
            select(SavedJob.job_id).where(SavedJob.user_id == user_id)
        ).scalars().all()
        saved_job_ids = set(saved_rows)

    return _format_job_response(job, candidate_features, saved_job_ids)


# =============================================================================
# Employer Endpoints (Corporate/Admin)
# =============================================================================

@router.get("/employers", response_model=List[EmployerResponse])
def list_employers(
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user),
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

    candidate_features = JobMatchingService.get_candidate_profile_features(db)
    return _format_job_response(job, candidate_features, set())


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
