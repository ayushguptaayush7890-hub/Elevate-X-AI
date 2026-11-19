"""
Technical and Behavioral Interview Sessions, Questions, Answers, and Feedback Database Models.
"""

from typing import Optional, List
import uuid
from sqlalchemy import String, Integer, Float, Text, ForeignKey, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from app.models.base import TimestampMixin


class InterviewSession(Base, TimestampMixin):
    """Interview preparation or technical evaluation practice session."""

    __tablename__ = "interview_sessions"

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
    target_role: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    trade_category: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    session_type: Mapped[str] = mapped_column(
        String(50),
        default="technical_diagnostic",  # technical_diagnostic, behavioral, mock
        nullable=False,
    )
    status: Mapped[str] = mapped_column(
        String(50),
        default="scheduled",  # scheduled, in_progress, completed
        nullable=False,
    )

    # Relationships
    user: Mapped["User"] = relationship("User")
    questions: Mapped[List["InterviewQuestion"]] = relationship(
        "InterviewQuestion",
        back_populates="session",
        cascade="all, delete-orphan",
        order_by="InterviewQuestion.order_index",
    )
    answers: Mapped[List["InterviewAnswer"]] = relationship(
        "InterviewAnswer",
        back_populates="session",
        cascade="all, delete-orphan",
    )
    feedback: Mapped[Optional["InterviewFeedback"]] = relationship(
        "InterviewFeedback",
        back_populates="session",
        uselist=False,
        cascade="all, delete-orphan",
    )


class InterviewQuestion(Base, TimestampMixin):
    """Scenario or technical question asked during an interview session."""

    __tablename__ = "interview_questions"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    session_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("interview_sessions.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    question_text: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    expected_competency: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
    )
    order_index: Mapped[int] = mapped_column(
        Integer,
        default=1,
        nullable=False,
    )

    # Relationship
    session: Mapped["InterviewSession"] = relationship("InterviewSession", back_populates="questions")


class InterviewAnswer(Base, TimestampMixin):
    """Transcript or text response submitted by the candidate."""

    __tablename__ = "interview_answers"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    session_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("interview_sessions.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    question_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("interview_questions.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    user_response_text: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    time_taken_seconds: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
    )

    # Relationships
    session: Mapped["InterviewSession"] = relationship("InterviewSession", back_populates="answers")
    question: Mapped["InterviewQuestion"] = relationship("InterviewQuestion")


class InterviewFeedback(Base, TimestampMixin):
    """Structured evaluation scorecard for an interview session."""

    __tablename__ = "interview_feedback"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    session_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("interview_sessions.id", ondelete="CASCADE"),
        unique=True,
        index=True,
        nullable=False,
    )
    technical_accuracy_score: Mapped[float] = mapped_column(
        Float,
        default=80.0,
        nullable=False,
    )
    clarity_score: Mapped[float] = mapped_column(
        Float,
        default=85.0,
        nullable=False,
    )
    feedback_summary: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    areas_of_improvement: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    # Relationship
    session: Mapped["InterviewSession"] = relationship("InterviewSession", back_populates="feedback")

