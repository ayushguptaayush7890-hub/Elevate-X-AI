"""
Learning Resources, Verified Providers, and Competency Mapping Database Models.
"""

from typing import Optional, List
import uuid
from sqlalchemy import String, Integer, Float, Text, Boolean, ForeignKey, Uuid, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from app.models.base import TimestampMixin


class ResourceProvider(Base, TimestampMixin):
    """Verified vocational training provider, guild, or educational partner."""

    __tablename__ = "resource_providers"

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
    is_verified: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    # Relationships
    resources: Mapped[List["LearningResource"]] = relationship(
        "LearningResource",
        back_populates="provider",
        cascade="all, delete-orphan",
    )


class LearningResource(Base, TimestampMixin):
    """Curated vocational course, hands-on workshop, or learning sandbox."""

    __tablename__ = "learning_resources"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    title: Mapped[str] = mapped_column(
        String(255),
        index=True,
        nullable=False,
    )
    provider_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("resource_providers.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    description: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )
    url: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )
    language: Mapped[str] = mapped_column(
        String(50),
        default="English",
        nullable=False,
    )
    cost_type: Mapped[str] = mapped_column(
        String(50),
        default="free",  # free, paid, subsidized
        nullable=False,
    )
    cost_amount: Mapped[Optional[int]] = mapped_column(
        Integer,
        default=0,
        nullable=True,
    )
    duration_hours: Mapped[Optional[float]] = mapped_column(
        Float,
        default=4.0,
        nullable=True,
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    # Relationships
    provider: Mapped["ResourceProvider"] = relationship("ResourceProvider", back_populates="resources")
    skills: Mapped[List["ResourceSkill"]] = relationship(
        "ResourceSkill",
        back_populates="resource",
        cascade="all, delete-orphan",
    )


class ResourceSkill(Base, TimestampMixin):
    """Mapping between a learning resource and the competency it addresses."""

    __tablename__ = "resource_skills"
    __table_args__ = (
        UniqueConstraint("resource_id", "skill_id", name="uq_resource_skill"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    resource_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("learning_resources.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    skill_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("skills.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )

    # Relationships
    resource: Mapped["LearningResource"] = relationship("LearningResource", back_populates="skills")
    skill: Mapped["Skill"] = relationship("Skill")

