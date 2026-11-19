"""
Employer, Job Listing, Requirements, and Skill Mapping Database Models.
"""

from datetime import date
from typing import Optional, List
import uuid
from sqlalchemy import String, Integer, Float, Text, Boolean, Date, ForeignKey, Uuid, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from app.models.base import TimestampMixin


class Employer(Base, TimestampMixin):
    """Verified corporate or workshop employer."""

    __tablename__ = "employers"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    name: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False,
    )
    website: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
    )
    description: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )
    logo_url: Mapped[Optional[str]] = mapped_column(
        String(500),
        nullable=True,
    )
    location: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
    )
    is_verified: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    # Relationships
    jobs: Mapped[List["JobListing"]] = relationship(
        "JobListing",
        back_populates="employer",
        cascade="all, delete-orphan",
    )


class JobListing(Base, TimestampMixin):
    """Curated formal-sector trade job listing."""

    __tablename__ = "job_listings"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    employer_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("employers.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    title: Mapped[str] = mapped_column(
        String(255),
        index=True,
        nullable=False,
    )
    location: Mapped[str] = mapped_column(
        String(255),
        index=True,
        nullable=False,
    )
    description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    salary_min: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
    )
    salary_max: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
    )
    salary_currency: Mapped[str] = mapped_column(
        String(10),
        default="INR",
        nullable=False,
    )
    employment_type: Mapped[str] = mapped_column(
        String(50),
        default="Full-time",
        nullable=False,
    )
    experience_required_years: Mapped[Optional[int]] = mapped_column(
        Integer,
        default=0,
        nullable=True,
    )
    education_required: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
    )
    source_type: Mapped[str] = mapped_column(
        String(50),
        default="direct",
        nullable=False,
    )
    source_url: Mapped[Optional[str]] = mapped_column(
        String(500),
        nullable=True,
    )
    posted_date: Mapped[Optional[date]] = mapped_column(
        Date,
        default=date.today,
        nullable=True,
    )
    expiry_date: Mapped[Optional[date]] = mapped_column(
        Date,
        nullable=True,
    )
    is_verified: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    # Relationships
    employer: Mapped["Employer"] = relationship("Employer", back_populates="jobs")
    requirements: Mapped[List["JobRequirement"]] = relationship(
        "JobRequirement",
        back_populates="job",
        cascade="all, delete-orphan",
    )
    skills: Mapped[List["JobSkill"]] = relationship(
        "JobSkill",
        back_populates="job",
        cascade="all, delete-orphan",
    )


class JobRequirement(Base, TimestampMixin):
    """Specific line-item qualification or trade requirement for a job."""

    __tablename__ = "job_requirements"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    job_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("job_listings.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    requirement_text: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )
    is_mandatory: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    # Relationship
    job: Mapped["JobListing"] = relationship("JobListing", back_populates="requirements")


class JobSkill(Base, TimestampMixin):
    """Explicit competency requirement linking a job listing to the skill catalog."""

    __tablename__ = "job_skills"
    __table_args__ = (
        UniqueConstraint("job_id", "skill_id", name="uq_job_skill"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    job_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("job_listings.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    skill_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("skills.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    is_mandatory: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )
    min_years: Mapped[Optional[float]] = mapped_column(
        Float,
        default=1.0,
        nullable=True,
    )

    # Relationships
    job: Mapped["JobListing"] = relationship("JobListing", back_populates="skills")
    skill: Mapped["Skill"] = relationship("Skill")

