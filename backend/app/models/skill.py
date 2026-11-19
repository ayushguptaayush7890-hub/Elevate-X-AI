"""
Vocational Skill, User-Skill Mapping, and Skill Evidence Models.
"""

from datetime import datetime
from typing import Optional, List, TYPE_CHECKING
import uuid
from sqlalchemy import String, Integer, Float, Text, DateTime, ForeignKey, Uuid, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from app.models.base import TimestampMixin

if TYPE_CHECKING:
    from app.models.profile import UserProfile


class Skill(Base, TimestampMixin):
    """Catalog of formal and informal trade competencies."""

    __tablename__ = "skills"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    name: Mapped[str] = mapped_column(
        String(150),
        unique=True,
        index=True,
        nullable=False,
    )
    category: Mapped[str] = mapped_column(
        String(100),
        index=True,
        nullable=False,
    )
    nsqf_level: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
    )
    description: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    # Relationships
    user_skills: Mapped[List["UserSkill"]] = relationship(
        "UserSkill",
        back_populates="skill",
        cascade="all, delete-orphan",
    )


class UserSkill(Base, TimestampMixin):
    """
    Mapping between a user's vocational profile and a skill.
    Strictly distinguishes self-reported from assessed and verified competencies.
    """

    __tablename__ = "user_skills"
    __table_args__ = (
        UniqueConstraint("profile_id", "skill_id", name="uq_user_profile_skill"),
    )

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
    skill_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("skills.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    # Verification tiers: self_reported, assessed, verified
    verification_status: Mapped[str] = mapped_column(
        String(50),
        default="self_reported",
        nullable=False,
    )
    # Proficiency tiers: beginner, intermediate, advanced, expert
    proficiency_level: Mapped[str] = mapped_column(
        String(50),
        default="intermediate",
        nullable=False,
    )
    years_practiced: Mapped[Optional[float]] = mapped_column(
        Float,
        default=1.0,
        nullable=True,
    )
    confidence_score: Mapped[Optional[float]] = mapped_column(
        Float,
        default=0.85,
        nullable=True,
    )

    # Relationships
    profile: Mapped["UserProfile"] = relationship("UserProfile", back_populates="user_skills")
    skill: Mapped["Skill"] = relationship("Skill", back_populates="user_skills")
    evidences: Mapped[List["SkillEvidence"]] = relationship(
        "SkillEvidence",
        back_populates="user_skill",
        cascade="all, delete-orphan",
    )


class SkillEvidence(Base, TimestampMixin):
    """Verifiable proof, practical diagnostic test result, or workplace artifact."""

    __tablename__ = "skill_evidences"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    user_skill_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("user_skills.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    # evidence_type: diagnostic_assessment, workplace_photo, supervisor_endorsement, certificate
    evidence_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )
    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    description: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )
    file_url: Mapped[Optional[str]] = mapped_column(
        String(500),
        nullable=True,
    )
    score_achieved: Mapped[Optional[float]] = mapped_column(
        Float,
        nullable=True,
    )
    verified_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    # Relationship
    user_skill: Mapped["UserSkill"] = relationship("UserSkill", back_populates="evidences")

