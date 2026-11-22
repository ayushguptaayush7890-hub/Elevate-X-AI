"""
Career Transition Pathways, Transferable Skills, and Bridge Requirements Database Models.
"""

from typing import Optional, List
import uuid
from sqlalchemy import String, Integer, Float, Text, ForeignKey, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from app.models.base import TimestampMixin


class CareerTransition(Base, TimestampMixin):
    """Potential vocational transition corridor from an informal trade to formal employment."""

    __tablename__ = "career_transitions"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    from_occupation_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("occupations.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    to_occupation_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("occupations.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    transition_title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    feasibility_score: Mapped[float] = mapped_column(
        Float,
        default=85.0,
        nullable=False,
    )
    estimated_transition_months: Mapped[int] = mapped_column(
        Integer,
        default=3,
        nullable=False,
    )
    description: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    # Relationships
    from_occupation: Mapped["Occupation"] = relationship(
        "Occupation", foreign_keys=[from_occupation_id]
    )
    to_occupation: Mapped["Occupation"] = relationship(
        "Occupation", foreign_keys=[to_occupation_id]
    )
    skills_mapping: Mapped[List["TransferableSkillMapping"]] = relationship(
        "TransferableSkillMapping",
        back_populates="transition",
        cascade="all, delete-orphan",
    )
    requirements: Mapped[List["TransitionRequirement"]] = relationship(
        "TransitionRequirement",
        back_populates="transition",
        cascade="all, delete-orphan",
    )


class TransferableSkillMapping(Base, TimestampMixin):
    """Mapping of tactile and transferable skills across the transition boundary."""

    __tablename__ = "transferable_skill_mappings"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    transition_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("career_transitions.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    skill_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("skills.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    transferability_level: Mapped[str] = mapped_column(
        String(50),
        default="direct",  # direct, partial, complementary
        nullable=False,
    )
    notes: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    # Relationships
    transition: Mapped["CareerTransition"] = relationship("CareerTransition", back_populates="skills_mapping")
    skill: Mapped["Skill"] = relationship("Skill")


class TransitionRequirement(Base, TimestampMixin):
    """Specific bridge requirement (training module, licensing, diagnostic verification)."""

    __tablename__ = "transition_requirements"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    transition_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("career_transitions.id", ondelete="CASCADE"),
        index=True,
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
    requirement_type: Mapped[str] = mapped_column(
        String(50),
        default="bridge_training",  # licensing, bridge_training, assessment
        nullable=False,
    )

    # Relationship
    transition: Mapped["CareerTransition"] = relationship("CareerTransition", back_populates="requirements")


class UserCareerTransitionGoal(Base, TimestampMixin):
    """User adopted career transition goal and learning blueprint tracking."""

    __tablename__ = "user_career_transition_goals"

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
    from_occupation_title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    target_occupation_id: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    target_occupation_title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    target_taxonomy: Mapped[str] = mapped_column(
        String(100),
        default="ESCO v1.2.1",
        nullable=False,
    )
    fit_percentage: Mapped[float] = mapped_column(
        Float,
        default=0.0,
        nullable=False,
    )
    transition_delta: Mapped[float] = mapped_column(
        Float,
        default=0.0,
        nullable=False,
    )
    difficulty_category: Mapped[str] = mapped_column(
        String(50),
        default="Moderate Bridge",
        nullable=False,
    )
    status: Mapped[str] = mapped_column(
        String(50),
        default="active",  # active, paused, completed
        nullable=False,
    )
    blueprint_json: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )
    progress_percentage: Mapped[float] = mapped_column(
        Float,
        default=0.0,
        nullable=False,
    )
    academic_evidence_json: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )
    scoring_methodology: Mapped[Optional[str]] = mapped_column(
        String(100),
        default="BGE-Small v1.5 + Node2Vec Graph v2.1",
        nullable=True,
    )
    transferable_skills_json: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )
    missing_skills_json: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    # Relationship
    user: Mapped["User"] = relationship("User")


