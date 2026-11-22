"""
Pydantic schemas for the AI Career Mentor and Consultations.
"""

from typing import List, Optional
import uuid
from datetime import datetime
from pydantic import BaseModel, Field


class MessageBase(BaseModel):
    sender: str = Field(..., description="'user' or 'assistant'")
    content: str = Field(..., description="Message text or markdown")
    language: str = Field(default="English", description="'English' or 'Hindi'")


class MessageCreate(BaseModel):
    content: str = Field(..., min_length=1, max_length=10000, description="User prompt or inquiry")
    language: Optional[str] = Field(default="English", description="'English' or 'Hindi'")


class MessageResponse(BaseModel):
    id: str
    consultation_id: str
    sender: str
    content: str
    language: str
    timestamp: str
    model_used: Optional[str] = None
    tokens_used: Optional[int] = None
    suggestions: List[str] = Field(default_factory=list)


class ConsultationCreate(BaseModel):
    title: Optional[str] = Field(default="New Career Consultation", max_length=255)
    language: Optional[str] = Field(default="English")


class ConsultationUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=255)
    language: Optional[str] = Field(None)


class ConsultationListItem(BaseModel):
    id: str
    title: str
    language: str
    date: str
    last_message_preview: Optional[str] = None
    message_count: int = 0
    updated_at: datetime


class ConsultationDetailResponse(BaseModel):
    id: str
    title: str
    language: str
    created_at: datetime
    updated_at: datetime
    messages: List[MessageResponse] = Field(default_factory=list)


class SuggestedQuestionsRequest(BaseModel):
    language: Optional[str] = "English"
