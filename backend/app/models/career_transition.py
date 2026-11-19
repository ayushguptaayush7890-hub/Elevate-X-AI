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

