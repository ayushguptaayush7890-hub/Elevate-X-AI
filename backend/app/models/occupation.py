"""
Occupation Catalog and Occupation-to-Skill Taxonomy Database Models.
"""

from typing import Optional, List
import uuid
from sqlalchemy import String, Integer, Float, Text, Boolean, ForeignKey, Uuid, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from app.models.base import TimestampMixin


class Occupation(Base, TimestampMixin):
    """Standardized vocational or formal occupation profile."""

    __tablename__ = "occupations"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    code: Mapped[Optional[str]] = mapped_column(
        String(50),
        unique=True,
        index=True,
        nullable=True,
    )
    title: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False,
    )
    category: Mapped[str] = mapped_column(
        String(100),
        index=True,
        nullable=False,
    )
    description: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )
    recommended_experience_years: Mapped[Optional[int]] = mapped_column(
        Integer,
        default=0,
        nullable=True,
    )
    education_requirements: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
    )
    nsqf_level: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    # Relationships
    required_skills: Mapped[List["OccupationSkill"]] = relationship(
        "OccupationSkill",
        back_populates="occupation",
        cascade="all, delete-orphan",
    )


class OccupationSkill(Base, TimestampMixin):
    """Mapping between an occupation and its mandatory or recommended skills."""

    __tablename__ = "occupation_skills"
    __table_args__ = (
        UniqueConstraint("occupation_id", "skill_id", name="uq_occupation_skill"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    occupation_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("occupations.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    skill_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("skills.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    is_required: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )
    importance_weight: Mapped[float] = mapped_column(
        Float,
        default=1.0,
        nullable=False,
    )

    # Relationships
    occupation: Mapped["Occupation"] = relationship("Occupation", back_populates="required_skills")
    skill: Mapped["Skill"] = relationship("Skill")

