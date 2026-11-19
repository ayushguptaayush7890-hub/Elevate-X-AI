"""
API Router for Skill Gap Analysis and Differential Capability Reporting.
"""

from typing import List
import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select

from app.core.database import get_db
from app.api.deps import get_current_active_user
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

router = APIRouter()


@router.post("", response_model=SkillGapReportResponse, status_code=status.HTTP_201_CREATED)
def generate_skill_gap_report(
    payload: SkillGapReportCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Evaluate candidate competencies against an occupation or job listing.
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

    # If caller provided explicit items, store them
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
        # Compute gap against occupation's required skills
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

    elif payload.target_job_id:
        # Compute gap against job listing required skills
        job_skills = db.execute(
            select(JobSkill).where(JobSkill.job_id == payload.target_job_id)
        ).scalars().all()

        total = len(job_skills)
        matched = 0

        for js in job_skills:
            if js.skill_id in user_skills_map:
                matched += 1
                curr_prof = user_skills_map[js.skill_id].proficiency_level
                items_to_save.append(
                    SkillGapItem(
                        report_id=report.id,
                        skill_id=js.skill_id,
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
                        skill_id=js.skill_id,
                        current_proficiency="none",
                        required_proficiency="intermediate",
                        gap_severity="missing",
                        priority="high" if js.is_mandatory else "medium",
                    )
                )

        report.overall_match_percentage = round((matched / total) * 100, 1) if total > 0 else 100.0

    for item in items_to_save:
        db.add(item)

    db.commit()
    db.refresh(report)

    # Reload with items
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

