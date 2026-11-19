"""
Objective Skill Diagnostic Assessment, Questions, Attempts, and Results Database Models.
"""

from datetime import datetime, timezone
from typing import Optional, List
import uuid
from sqlalchemy import String, Integer, Float, Text, Boolean, DateTime, ForeignKey, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from app.models.base import TimestampMixin


class Assessment(Base, TimestampMixin):
    """Standardized scenario and diagnostic assessment for vocational trade skills."""

    __tablename__ = "assessments"

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
    description: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )
    skill_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("skills.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    difficulty_level: Mapped[str] = mapped_column(
        String(50),
        default="intermediate",
        nullable=False,
    )
    duration_minutes: Mapped[int] = mapped_column(
        Integer,
        default=20,
        nullable=False,
    )
    passing_score_percentage: Mapped[float] = mapped_column(
        Float,
        default=75.0,
        nullable=False,
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    # Relationships
    skill: Mapped["Skill"] = relationship("Skill")
    questions: Mapped[List["AssessmentQuestion"]] = relationship(
        "AssessmentQuestion",
        back_populates="assessment",
        cascade="all, delete-orphan",
        order_by="AssessmentQuestion.order_index",
    )
    attempts: Mapped[List["AssessmentAttempt"]] = relationship(
        "AssessmentAttempt",
        back_populates="assessment",
        cascade="all, delete-orphan",
    )


class AssessmentQuestion(Base, TimestampMixin):
    """Multiple-choice or scenario diagnostic question."""

    __tablename__ = "assessment_questions"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    assessment_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("assessments.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    question_text: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    question_type: Mapped[str] = mapped_column(
        String(50),
        default="scenario",
        nullable=False,
    )
    points: Mapped[int] = mapped_column(
        Integer,
        default=1,
        nullable=False,
    )
    order_index: Mapped[int] = mapped_column(
        Integer,
        default=1,
        nullable=False,
    )

    # Relationships
    assessment: Mapped["Assessment"] = relationship("Assessment", back_populates="questions")
    options: Mapped[List["AssessmentOption"]] = relationship(
        "AssessmentOption",
        back_populates="question",
        cascade="all, delete-orphan",
    )


class AssessmentOption(Base, TimestampMixin):
    """Answer choice for an assessment question."""

    __tablename__ = "assessment_options"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    question_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("assessment_questions.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    option_text: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    is_correct: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )
    explanation: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    # Relationship
    question: Mapped["AssessmentQuestion"] = relationship("AssessmentQuestion", back_populates="options")


class AssessmentAttempt(Base, TimestampMixin):
    """Live or historical assessment attempt instance executed by a user."""

    __tablename__ = "assessment_attempts"

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
    assessment_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("assessments.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    completed_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    score_achieved: Mapped[Optional[float]] = mapped_column(
        Float,
        nullable=True,
    )
    passed: Mapped[Optional[bool]] = mapped_column(
        Boolean,
        nullable=True,
    )
    status: Mapped[str] = mapped_column(
        String(50),
        default="in_progress",
        nullable=False,
    )

    # Relationships
    assessment: Mapped["Assessment"] = relationship("Assessment", back_populates="attempts")
    answers: Mapped[List["AssessmentAnswer"]] = relationship(
        "AssessmentAnswer",
        back_populates="attempt",
        cascade="all, delete-orphan",
    )


class AssessmentAnswer(Base, TimestampMixin):
    """User response submitted for a specific question."""

    __tablename__ = "assessment_answers"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    attempt_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("assessment_attempts.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    question_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("assessment_questions.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    selected_option_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("assessment_options.id", ondelete="SET NULL"),
        nullable=True,
    )
    is_correct: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )
    points_awarded: Mapped[float] = mapped_column(
        Float,
        default=0.0,
        nullable=False,
    )

    # Relationships
    attempt: Mapped["AssessmentAttempt"] = relationship("AssessmentAttempt", back_populates="answers")
    question: Mapped["AssessmentQuestion"] = relationship("AssessmentQuestion")
    selected_option: Mapped[Optional["AssessmentOption"]] = relationship("AssessmentOption")


class AssessmentResult(Base, TimestampMixin):
    """Archival diagnostic scorecard and capability badge trigger."""

    __tablename__ = "assessment_results"

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
    assessment_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("assessments.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    attempt_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("assessment_attempts.id", ondelete="CASCADE"),
        unique=True,
        index=True,
        nullable=False,
    )
    score_percentage: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )
    passed: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
    )
    completed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    # Relationships
    assessment: Mapped["Assessment"] = relationship("Assessment")
    attempt: Mapped["AssessmentAttempt"] = relationship("AssessmentAttempt")


class TechnicalAssessmentResult(Base, TimestampMixin):
    """Archival persistent record for Feature 2 Technical Assessment sessions, skill gaps, and roadmaps."""

    __tablename__ = "technical_assessment_results"

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
    session_id: Mapped[str] = mapped_column(
        String(100),
        index=True,
        nullable=False,
    )
    role_id: Mapped[str] = mapped_column(
        String(100),
        index=True,
        nullable=False,
    )
    role_title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    overall_score_percentage: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )
    points_awarded: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )
    total_points: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )
    passed: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
    )
    difficulty_mode: Mapped[str] = mapped_column(
        String(50),
        default="adaptive",
        nullable=False,
    )
    ability_theta: Mapped[Optional[float]] = mapped_column(
        Float,
        nullable=True,
    )
    skill_performances: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )
    skill_gaps: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )
    roadmap_milestones: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )
    narrative_summary: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )
    evaluated_answers: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )
    completed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    # Relationships
    user: Mapped["User"] = relationship("User")


