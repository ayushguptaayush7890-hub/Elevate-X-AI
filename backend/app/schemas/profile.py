"""
Pydantic v2 schemas for User Profile, Education, Experience, and Career Preferences.
"""

from datetime import date, datetime
from typing import Optional, List
import uuid
from pydantic import BaseModel, ConfigDict, Field


# -----------------------------------------------------------------------------
# User Profile Schemas
# -----------------------------------------------------------------------------

class ProfileUpdateRequest(BaseModel):
    """Payload to update own vocational profile."""

    headline: Optional[str] = Field(None, max_length=255)
    bio: Optional[str] = None
    phone: Optional[str] = Field(None, max_length=50)
    location: Optional[str] = Field(None, max_length=255)
    trade_category: Optional[str] = Field(None, max_length=100)
    years_of_experience: Optional[int] = Field(None, ge=0, le=70)
    preferred_language: Optional[str] = Field("en", max_length=20)


class ProfileResponse(BaseModel):
    """Full user profile representation."""

    id: uuid.UUID
    user_id: uuid.UUID
    headline: Optional[str] = None
    bio: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    trade_category: Optional[str] = None
    years_of_experience: Optional[int] = 0
    preferred_language: str = "en"
    completion_percentage: int = 20
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# -----------------------------------------------------------------------------
# Education Schemas
# -----------------------------------------------------------------------------

class EducationCreate(BaseModel):
    """Payload to create an education record."""

    institution: str = Field(..., max_length=255)
    degree_or_certificate: str = Field(..., max_length=255)
    field_of_study: Optional[str] = Field(None, max_length=255)
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    is_current: bool = False
    grade_or_score: Optional[str] = Field(None, max_length=50)
    description: Optional[str] = None


class EducationResponse(BaseModel):
    """Education record response."""

    id: uuid.UUID
    profile_id: uuid.UUID
    institution: str
    degree_or_certificate: str
    field_of_study: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    is_current: bool
    grade_or_score: Optional[str] = None
    description: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# -----------------------------------------------------------------------------
# Work Experience Schemas
# -----------------------------------------------------------------------------

class WorkExperienceCreate(BaseModel):
    """Payload to create a work experience record."""

    job_title: str = Field(..., max_length=255)
    company_or_workshop: str = Field(..., max_length=255)
    location: Optional[str] = Field(None, max_length=255)
    employment_type: Optional[str] = Field("Full-time", max_length=50)
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    is_current: bool = False
    description: Optional[str] = None
    trade_tools_used: Optional[str] = Field(None, max_length=500)


class WorkExperienceUpdate(BaseModel):
    """Payload to update an existing work experience record."""

    job_title: Optional[str] = Field(None, max_length=255)
    company_or_workshop: Optional[str] = Field(None, max_length=255)
    location: Optional[str] = Field(None, max_length=255)
    employment_type: Optional[str] = Field(None, max_length=50)
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    is_current: Optional[bool] = None
    description: Optional[str] = None
    trade_tools_used: Optional[str] = Field(None, max_length=500)


class WorkExperienceResponse(BaseModel):
    """Work experience record response."""

    id: uuid.UUID
    profile_id: uuid.UUID
    job_title: str
    company_or_workshop: str
    location: Optional[str] = None
    employment_type: Optional[str] = "Full-time"
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    is_current: bool
    description: Optional[str] = None
    trade_tools_used: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# -----------------------------------------------------------------------------
# Career Preference Schemas
# -----------------------------------------------------------------------------

class CareerPreferenceUpdate(BaseModel):
    """Payload to set or update career preferences."""

    target_role: Optional[str] = Field(None, max_length=255)
    preferred_locations: Optional[str] = Field(None, max_length=255)
    expected_salary_min: Optional[int] = Field(None, ge=0)
    expected_salary_max: Optional[int] = Field(None, ge=0)
    open_to_relocation: bool = False
    preferred_shift: Optional[str] = Field(None, max_length=50)


class CareerPreferenceResponse(BaseModel):
    """Career preference response."""

    id: uuid.UUID
    profile_id: uuid.UUID
    target_role: Optional[str] = None
    preferred_locations: Optional[str] = None
    expected_salary_min: Optional[int] = None
    expected_salary_max: Optional[int] = None
    open_to_relocation: bool
    preferred_shift: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

