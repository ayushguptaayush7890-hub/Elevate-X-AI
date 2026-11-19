"""
Structured Resume Document, Versioning, and Sections Database Models.
"""

from typing import Optional, List
import uuid
from sqlalchemy import String, Integer, Boolean, Text, ForeignKey, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from app.models.base import TimestampMixin


class ResumeDocument(Base, TimestampMixin):
    """Resume container representing a candidate's formal resume asset."""

    __tablename__ = "resume_documents"

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
        default="My Trade Resume",
        nullable=False,
    )
    is_primary: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    # Relationships
    user: Mapped["User"] = relationship("User")
    versions: Mapped[List["ResumeVersion"]] = relationship(
        "ResumeVersion",
        back_populates="resume",
        cascade="all, delete-orphan",
        order_by="ResumeVersion.version_number.desc()",
    )


class ResumeVersion(Base, TimestampMixin):
    """Immutable or editable version snapshot of a candidate's resume."""

    __tablename__ = "resume_versions"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    resume_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("resume_documents.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    version_number: Mapped[int] = mapped_column(
        Integer,
        default=1,
        nullable=False,
    )
    version_name: Mapped[str] = mapped_column(
        String(100),
        default="v1.0 - Initial Draft",
        nullable=False,
    )
    raw_content_json: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    # Relationships
    resume: Mapped["ResumeDocument"] = relationship("ResumeDocument", back_populates="versions")
    sections: Mapped[List["ResumeSection"]] = relationship(
        "ResumeSection",
        back_populates="version",
        cascade="all, delete-orphan",
        order_by="ResumeSection.order_index",
    )


class ResumeSection(Base, TimestampMixin):
    """Discrete structured block of resume data (Summary, Skills, Work History, Certifications)."""

    __tablename__ = "resume_sections"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    version_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("resume_versions.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    section_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,  # header, summary, skills, experience, education, certifications
    )
    title: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    content_json: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    order_index: Mapped[int] = mapped_column(
        Integer,
        default=1,
        nullable=False,
    )

    # Relationship
    version: Mapped["ResumeVersion"] = relationship("ResumeVersion", back_populates="sections")

