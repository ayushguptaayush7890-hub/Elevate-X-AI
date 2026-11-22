"""
AI Career Consultation and Conversation History Database Models.
"""

from datetime import datetime
from typing import Optional, List
import uuid
from sqlalchemy import String, Integer, Text, DateTime, ForeignKey, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from app.models.base import TimestampMixin


class Consultation(Base, TimestampMixin):
    """Represents a career consultation chat thread between a user and the AI Mentor."""

    __tablename__ = "consultations"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    user_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True,
        nullable=True,
    )
    title: Mapped[str] = mapped_column(
        String(255),
        default="New Career Consultation",
        nullable=False,
    )
    language: Mapped[str] = mapped_column(
        String(20),
        default="English",
        nullable=False,
    )
    summary: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    # Relationships
    messages: Mapped[List["ConsultationMessage"]] = relationship(
        "ConsultationMessage",
        back_populates="consultation",
        cascade="all, delete-orphan",
        order_by="ConsultationMessage.created_at",
    )


class ConsultationMessage(Base):
    """Single message within a career consultation conversation."""

    __tablename__ = "consultation_messages"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    consultation_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("consultations.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    sender: Mapped[str] = mapped_column(
        String(20),  # 'user' | 'assistant'
        nullable=False,
    )
    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    language: Mapped[str] = mapped_column(
        String(20),
        default="English",
        nullable=False,
    )
    model_used: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
    )
    tokens_used: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
    )
    suggestions_json: Mapped[Optional[str]] = mapped_column(
        Text,  # Stored as JSON array string
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    # Relationships
    consultation: Mapped["Consultation"] = relationship(
        "Consultation",
        back_populates="messages",
    )
