"""
User Profile, Education, Work Experience, and Career Preference Models.
"""

from datetime import date
from typing import Optional, List, TYPE_CHECKING
import uuid
from sqlalchemy import String, Integer, Boolean, Text, Date, ForeignKey, Uuid, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from app.models.base import TimestampMixin

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.skill import UserSkill


class UserProfile(Base, TimestampMixin):
    """Vocational profile attached to a registered user."""

    __tablename__ = "user_profiles"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        index=True,
        nullable=False,
    )
    headline: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    bio: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    phone: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    location: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    trade_category: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    years_of_experience: Mapped[Optional[int]] = mapped_column(Integer, default=0, nullable=True)
    preferred_language: Mapped[str] = mapped_column(String(20), default="en", nullable=False)
    completion_percentage: Mapped[int] = mapped_column(Integer, default=20, nullable=False)

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="profile")
    educations: Mapped[List["Education"]] = relationship(
        "Education",
        back_populates="profile",
        cascade="all, delete-orphan",
        order_by="desc(Education.start_date)",
    )
    work_experiences: Mapped[List["WorkExperience"]] = relationship(
        "WorkExperience",
        back_populates="profile",
        cascade="all, delete-orphan",
        order_by="desc(WorkExperience.start_date)",
    )
    user_skills: Mapped[List["UserSkill"]] = relationship(
        "UserSkill",
        back_populates="profile",
        cascade="all, delete-orphan",
    )
    career_preference: Mapped[Optional["CareerPreference"]] = relationship(
        "CareerPreference",
        back_populates="profile",
        uselist=False,
        cascade="all, delete-orphan",
    )


class Education(Base, TimestampMixin):
    """Formal, vocational, or technical education record."""

    __tablename__ = "educations"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    profile_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("user_profiles.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    institution: Mapped[str] = mapped_column(String(255), nullable=False)
    degree_or_certificate: Mapped[str] = mapped_column(String(255), nullable=False)
    field_of_study: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    start_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    end_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    is_current: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    grade_or_score: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Relationship
    profile: Mapped["UserProfile"] = relationship("UserProfile", back_populates="educations")


class WorkExperience(Base, TimestampMixin):
    """Hands-on informal or formal work experience."""

    __tablename__ = "work_experiences"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    profile_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("user_profiles.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    job_title: Mapped[str] = mapped_column(String(255), nullable=False)
    company_or_workshop: Mapped[str] = mapped_column(String(255), nullable=False)
    location: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    employment_type: Mapped[Optional[str]] = mapped_column(String(50), default="Full-time", nullable=True)
    start_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    end_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    is_current: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    trade_tools_used: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    # Relationship
    profile: Mapped["UserProfile"] = relationship("UserProfile", back_populates="work_experiences")


class CareerPreference(Base, TimestampMixin):
    """Target career aspirations and job preferences."""

    __tablename__ = "career_preferences"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    profile_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("user_profiles.id", ondelete="CASCADE"),
        unique=True,
        index=True,
        nullable=False,
    )
    target_role: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    preferred_locations: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    expected_salary_min: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    expected_salary_max: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    open_to_relocation: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    preferred_shift: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)

    # Relationship
    profile: Mapped["UserProfile"] = relationship("UserProfile", back_populates="career_preference")

