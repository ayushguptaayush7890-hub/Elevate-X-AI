"""
Career Roadmap, Milestones, and Hands-on Tasks Database Models.
"""

from datetime import date
from typing import Optional, List
import uuid
from sqlalchemy import String, Integer, Float, Text, Boolean, Date, ForeignKey, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from app.models.base import TimestampMixin


class CareerRoadmap(Base, TimestampMixin):
    """Personalized career milestones roadmap for vocational transitions."""

    __tablename__ = "career_roadmaps"

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
    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    target_occupation_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("occupations.id", ondelete="SET NULL"),
        nullable=True,
    )
    target_role: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    estimated_duration_weeks: Mapped[int] = mapped_column(
        Integer,
        default=8,
        nullable=False,
    )
    progress_percentage: Mapped[float] = mapped_column(
        Float,
        default=0.0,
        nullable=False,
    )
    status: Mapped[str] = mapped_column(
        String(50),
        default="active",  # active, completed, paused
        nullable=False,
    )

    # Relationships
    user: Mapped["User"] = relationship("User")
    target_occupation: Mapped[Optional["Occupation"]] = relationship("Occupation")
    milestones: Mapped[List["RoadmapMilestone"]] = relationship(
        "RoadmapMilestone",
        back_populates="roadmap",
        cascade="all, delete-orphan",
        order_by="RoadmapMilestone.order_index",
    )


class RoadmapMilestone(Base, TimestampMixin):
    """Major phase or milestone along a user's roadmap."""

    __tablename__ = "roadmap_milestones"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    roadmap_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("career_roadmaps.id", ondelete="CASCADE"),
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
    order_index: Mapped[int] = mapped_column(
        Integer,
        default=1,
        nullable=False,
    )
    due_date: Mapped[Optional[date]] = mapped_column(
        Date,
        nullable=True,
    )
    is_completed: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    # Relationships
    roadmap: Mapped["CareerRoadmap"] = relationship("CareerRoadmap", back_populates="milestones")
    tasks: Mapped[List["RoadmapTask"]] = relationship(
        "RoadmapTask",
        back_populates="milestone",
        cascade="all, delete-orphan",
    )


class RoadmapTask(Base, TimestampMixin):
    """Specific actionable task (practical, assessment, or portfolio building)."""

    __tablename__ = "roadmap_tasks"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    milestone_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("roadmap_milestones.id", ondelete="CASCADE"),
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
    task_type: Mapped[str] = mapped_column(
        String(50),
        default="practical",  # learning, practical, assessment, portfolio
        nullable=False,
    )
    estimated_hours: Mapped[Optional[float]] = mapped_column(
        Float,
        default=2.0,
        nullable=True,
    )
    is_completed: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )
    resource_url: Mapped[Optional[str]] = mapped_column(
        String(500),
        nullable=True,
    )

    # Relationship
    milestone: Mapped["RoadmapMilestone"] = relationship("RoadmapMilestone", back_populates="tasks")

