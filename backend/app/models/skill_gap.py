"""
Skill Gap Analysis, Reports, and Delta Evaluation Database Models.
"""

from typing import Optional, List
import uuid
from sqlalchemy import String, Float, ForeignKey, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from app.models.base import TimestampMixin


class SkillGapReport(Base, TimestampMixin):
    """Evaluation comparing user competencies against target vocational occupations or formal job listings."""

    __tablename__ = "skill_gap_reports"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    target_occupation_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("occupations.id", ondelete="SET NULL"),
        nullable=True,
    )
    target_job_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("job_listings.id", ondelete="SET NULL"),
        nullable=True,
    )
    overall_match_percentage: Mapped[float] = mapped_column(
        Float,
        default=0.0,
        nullable=False,
    )

    # Relationships
    items: Mapped[List["SkillGapItem"]] = relationship(
        "SkillGapItem",
        back_populates="report",
        cascade="all, delete-orphan",
    )
    user: Mapped["User"] = relationship("User")
    target_occupation: Mapped[Optional["Occupation"]] = relationship("Occupation")
    target_job: Mapped[Optional["JobListing"]] = relationship("JobListing")


class SkillGapItem(Base, TimestampMixin):
    """Specific line-item delta representing a missing or under-developed skill competency."""

    __tablename__ = "skill_gap_items"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    report_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("skill_gap_reports.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    skill_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("skills.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    current_proficiency: Mapped[str] = mapped_column(
        String(50),
        default="none",
        nullable=False,
    )
    required_proficiency: Mapped[str] = mapped_column(
        String(50),
        default="intermediate",
        nullable=False,
    )
    gap_severity: Mapped[str] = mapped_column(
        String(50),
        default="missing",  # missing, low, medium, aligned
        nullable=False,
    )
    priority: Mapped[str] = mapped_column(
        String(50),
        default="high",  # high, medium, low
        nullable=False,
    )
    assessment_reference_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("assessments.id", ondelete="SET NULL"),
        nullable=True,
    )

    # Relationships
    report: Mapped["SkillGapReport"] = relationship("SkillGapReport", back_populates="items")
    skill: Mapped["Skill"] = relationship("Skill")
    assessment_reference: Mapped[Optional["Assessment"]] = relationship("Assessment")

