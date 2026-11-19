"""
API Router for Structured Trade Resumes, Version Snapshotting, and Discrete Sections.
"""

from typing import List
import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select

from app.core.database import get_db
from app.api.deps import get_current_active_user
from app.models.user import User
from app.models.resume import (
    ResumeDocument,
    ResumeVersion,
    ResumeSection,
)
from app.schemas.career_domain import (
    ResumeDocumentCreate,
    ResumeDocumentResponse,
    ResumeVersionCreate,
    ResumeVersionResponse,
)

router = APIRouter()


@router.get("", response_model=List[ResumeDocumentResponse])
def list_resumes(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """List all resume portfolios owned by the authenticated candidate."""
    return db.execute(
        select(ResumeDocument)
        .options(
            joinedload(ResumeDocument.versions).joinedload(ResumeVersion.sections)
        )
        .where(ResumeDocument.user_id == current_user.id)
        .order_by(ResumeDocument.created_at.desc())
    ).unique().scalars().all()


@router.post("", response_model=ResumeDocumentResponse, status_code=status.HTTP_201_CREATED)
def create_resume(
    payload: ResumeDocumentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Create a structured trade resume container, optionally populating the initial version."""
    if payload.is_primary:
        # Demote existing primary resumes to non-primary
        existing_primaries = db.execute(
            select(ResumeDocument).where(
                ResumeDocument.user_id == current_user.id,
                ResumeDocument.is_primary == True,  # noqa: E712
            )
        ).scalars().all()
        for doc in existing_primaries:
            doc.is_primary = False

    resume = ResumeDocument(
        user_id=current_user.id,
        title=payload.title,
        is_primary=payload.is_primary,
    )
    db.add(resume)
    db.flush()

    if payload.initial_version:
        ver = ResumeVersion(
            resume_id=resume.id,
            version_number=1,
            version_name=payload.initial_version.version_name,
            raw_content_json=payload.initial_version.raw_content_json,
        )
        db.add(ver)
        db.flush()

        for sec in payload.initial_version.sections:
            db.add(
                ResumeSection(
                    version_id=ver.id,
                    section_type=sec.section_type,
                    title=sec.title,
                    content_json=sec.content_json,
                    order_index=sec.order_index,
                )
            )

    db.commit()

    resume = db.execute(
        select(ResumeDocument)
        .options(
            joinedload(ResumeDocument.versions).joinedload(ResumeVersion.sections)
        )
        .where(ResumeDocument.id == resume.id)
    ).unique().scalar_one()

    return resume


@router.get("/{resume_id}", response_model=ResumeDocumentResponse)
def get_resume(
    resume_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Retrieve full resume details including all versions and structured sections."""
    resume = db.execute(
        select(ResumeDocument)
        .options(
            joinedload(ResumeDocument.versions).joinedload(ResumeVersion.sections)
        )
        .where(
            ResumeDocument.id == resume_id,
            ResumeDocument.user_id == current_user.id,
        )
    ).unique().scalar_one_or_none()

    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume document not found or access denied.",
        )
    return resume


@router.post("/{resume_id}/versions", response_model=ResumeVersionResponse, status_code=status.HTTP_201_CREATED)
def create_resume_version(
    resume_id: uuid.UUID,
    payload: ResumeVersionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Add a new incremental snapshot version to an existing resume document."""
    resume = db.execute(
        select(ResumeDocument).where(
            ResumeDocument.id == resume_id,
            ResumeDocument.user_id == current_user.id,
        )
    ).scalar_one_or_none()

    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume document not found.",
        )

    last_version = db.execute(
        select(ResumeVersion)
        .where(ResumeVersion.resume_id == resume.id)
        .order_by(ResumeVersion.version_number.desc())
    ).scalars().first()

    next_ver_num = (last_version.version_number + 1) if last_version else 1

    version = ResumeVersion(
        resume_id=resume.id,
        version_number=next_ver_num,
        version_name=payload.version_name,
        raw_content_json=payload.raw_content_json,
    )
    db.add(version)
    db.flush()

    for sec in payload.sections:
        db.add(
            ResumeSection(
                version_id=version.id,
                section_type=sec.section_type,
                title=sec.title,
                content_json=sec.content_json,
                order_index=sec.order_index,
            )
        )

    db.commit()

    version = db.execute(
        select(ResumeVersion)
        .options(joinedload(ResumeVersion.sections))
        .where(ResumeVersion.id == version.id)
    ).unique().scalar_one()

    return version


@router.delete("/{resume_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_resume(
    resume_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Delete a resume document portfolio."""
    resume = db.execute(
        select(ResumeDocument).where(
            ResumeDocument.id == resume_id,
            ResumeDocument.user_id == current_user.id,
        )
    ).scalar_one_or_none()

    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume document not found.",
        )

    db.delete(resume)
    db.commit()
    return None

