"""
API Router for Job Applications, Status Lifecycle Tracking, Application Notes, and Saved Jobs.
"""

from typing import List
import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select

from app.core.database import get_db
from app.api.deps import get_current_active_user
from app.models.user import User
from app.models.job import JobListing
from app.models.application import (
    JobApplication,
    SavedJob,
    ApplicationNote,
)
from app.schemas.career_domain import (
    JobApplicationCreate,
    JobApplicationStatusUpdate,
    JobApplicationResponse,
    ApplicationNoteCreate,
    ApplicationNoteResponse,
    SavedJobResponse,
)

router = APIRouter()


# =============================================================================
# Job Application Endpoints
# =============================================================================

@router.get("", response_model=List[JobApplicationResponse])
def list_applications(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Retrieve all job applications submitted or tracked by the authenticated user."""
    return db.execute(
        select(JobApplication)
        .options(
            joinedload(JobApplication.job).joinedload(JobListing.employer),
            joinedload(JobApplication.notes),
        )
        .where(JobApplication.user_id == current_user.id)
        .order_by(JobApplication.created_at.desc())
    ).unique().scalars().all()


@router.post("", response_model=JobApplicationResponse, status_code=status.HTTP_201_CREATED)
def create_application(
    payload: JobApplicationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Submit a formal application for a job opportunity."""
    job = db.execute(
        select(JobListing).where(JobListing.id == payload.job_id)
    ).scalar_one_or_none()

    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Target job listing not found.",
        )

    # Check for duplicate
    existing = db.execute(
        select(JobApplication).where(
            JobApplication.user_id == current_user.id,
            JobApplication.job_id == payload.job_id,
        )
    ).scalar_one_or_none()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have already applied for this job listing.",
        )

    application = JobApplication(
        user_id=current_user.id,
        job_id=payload.job_id,
        status="applied",
        cover_note=payload.cover_note,
    )
    db.add(application)
    db.commit()

    application = db.execute(
        select(JobApplication)
        .options(
            joinedload(JobApplication.job).joinedload(JobListing.employer),
            joinedload(JobApplication.notes),
        )
        .where(JobApplication.id == application.id)
    ).unique().scalar_one()

    return application


@router.get("/{application_id}", response_model=JobApplicationResponse)
def get_application(
    application_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Retrieve application status, notes, and associated job specification."""
    application = db.execute(
        select(JobApplication)
        .options(
            joinedload(JobApplication.job).joinedload(JobListing.employer),
            joinedload(JobApplication.notes),
        )
        .where(
            JobApplication.id == application_id,
            JobApplication.user_id == current_user.id,
        )
    ).unique().scalar_one_or_none()

    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found or access denied.",
        )
    return application


@router.put("/{application_id}/status", response_model=JobApplicationResponse)
def update_application_status(
    application_id: uuid.UUID,
    payload: JobApplicationStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Progress an application through pipeline stages (saved, applied, interview, shortlisted, rejected, offer)."""
    application = db.execute(
        select(JobApplication).where(
            JobApplication.id == application_id,
            JobApplication.user_id == current_user.id,
        )
    ).scalar_one_or_none()

    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found.",
        )

    application.status = payload.status
    db.commit()

    return db.execute(
        select(JobApplication)
        .options(
            joinedload(JobApplication.job).joinedload(JobListing.employer),
            joinedload(JobApplication.notes),
        )
        .where(JobApplication.id == application.id)
    ).unique().scalar_one()


@router.post("/{application_id}/notes", response_model=ApplicationNoteResponse, status_code=status.HTTP_201_CREATED)
def add_application_note(
    application_id: uuid.UUID,
    payload: ApplicationNoteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Add an interview preparation or follow-up note to a specific job application."""
    application = db.execute(
        select(JobApplication).where(
            JobApplication.id == application_id,
            JobApplication.user_id == current_user.id,
        )
    ).scalar_one_or_none()

    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found.",
        )

    note = ApplicationNote(
        application_id=application.id,
        note_text=payload.note_text,
    )
    db.add(note)
    db.commit()
    db.refresh(note)
    return note


@router.delete("/{application_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_application(
    application_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Withdraw or delete a job application tracking record."""
    application = db.execute(
        select(JobApplication).where(
            JobApplication.id == application_id,
            JobApplication.user_id == current_user.id,
        )
    ).scalar_one_or_none()

    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found.",
        )

    db.delete(application)
    db.commit()
    return None


# =============================================================================
# Saved Jobs Endpoints
# =============================================================================

saved_router = APIRouter()


@saved_router.get("", response_model=List[SavedJobResponse])
def list_saved_jobs(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """List all opportunities bookmarked by the authenticated user."""
    return db.execute(
        select(SavedJob)
        .options(
            joinedload(SavedJob.job).joinedload(JobListing.employer),
        )
        .where(SavedJob.user_id == current_user.id)
        .order_by(SavedJob.saved_at.desc())
    ).unique().scalars().all()


@saved_router.post("/{job_id}", response_model=SavedJobResponse, status_code=status.HTTP_201_CREATED)
def save_job(
    job_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Bookmark a job opportunity for future application."""
    job = db.execute(select(JobListing).where(JobListing.id == job_id)).scalar_one_or_none()
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job listing not found.",
        )

    existing = db.execute(
        select(SavedJob).where(
            SavedJob.user_id == current_user.id,
            SavedJob.job_id == job_id,
        )
    ).scalar_one_or_none()

    if existing:
        return existing

    saved = SavedJob(
        user_id=current_user.id,
        job_id=job_id,
    )
    db.add(saved)
    db.commit()

    return db.execute(
        select(SavedJob)
        .options(joinedload(SavedJob.job).joinedload(JobListing.employer))
        .where(SavedJob.id == saved.id)
    ).unique().scalar_one()


@saved_router.delete("/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
def unsave_job(
    job_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Remove a bookmarked job opportunity."""
    saved = db.execute(
        select(SavedJob).where(
            SavedJob.user_id == current_user.id,
            SavedJob.job_id == job_id,
        )
    ).scalar_one_or_none()

    if not saved:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Saved job bookmark not found.",
        )

    db.delete(saved)
    db.commit()
    return None

