"""
Job Application Tracking, Saved Jobs, and Candidate Notes Database Models.
"""

from datetime import datetime, timezone
from typing import Optional, List
import uuid
from sqlalchemy import String, Text, DateTime, ForeignKey, Uuid, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from app.models.base import TimestampMixin


class JobApplication(Base, TimestampMixin):
    """Candidate job application tracking state across pipeline stages."""

    __tablename__ = "job_applications"
    __table_args__ = (
        UniqueConstraint("user_id", "job_id", name="uq_user_job_application"),
    )

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
    job_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("job_listings.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    # Stages: saved, applied, interview, shortlisted, rejected, offer
    status: Mapped[str] = mapped_column(
        String(50),
        default="applied",
        nullable=False,
    )
    applied_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    cover_note: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    # Relationships
    user: Mapped["User"] = relationship("User")
    job: Mapped["JobListing"] = relationship("JobListing")
    notes: Mapped[List["ApplicationNote"]] = relationship(
        "ApplicationNote",
        back_populates="application",
        cascade="all, delete-orphan",
    )


class SavedJob(Base, TimestampMixin):
    """Bookmarks for opportunities saved by candidates."""

    __tablename__ = "saved_jobs"
    __table_args__ = (
        UniqueConstraint("user_id", "job_id", name="uq_user_saved_job"),
    )

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
    job_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("job_listings.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    saved_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # Relationships
    user: Mapped["User"] = relationship("User")
    job: Mapped["JobListing"] = relationship("JobListing")


class ApplicationNote(Base, TimestampMixin):
    """Personal notes or interview reminders logged by candidate on an application."""

    __tablename__ = "application_notes"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    application_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("job_applications.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    note_text: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    # Relationship
    application: Mapped["JobApplication"] = relationship("JobApplication", back_populates="notes")

