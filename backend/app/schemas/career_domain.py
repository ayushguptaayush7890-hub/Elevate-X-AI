"""
Pydantic v2 Schemas for Phase 3 Career Intelligence Domain Entities.
"""

from datetime import date, datetime
from typing import Optional, List, Dict, Any
import uuid
from pydantic import BaseModel, ConfigDict, Field


# =============================================================================
# 1. Occupation Schemas
# =============================================================================

class OccupationSkillCreate(BaseModel):
    skill_id: uuid.UUID
    is_required: bool = True
    importance_weight: float = Field(1.0, ge=0.1, le=1.0)


class OccupationSkillResponse(BaseModel):
    id: uuid.UUID
    skill_id: uuid.UUID
    is_required: bool
    importance_weight: float
    model_config = ConfigDict(from_attributes=True)


class OccupationCreate(BaseModel):
    title: str = Field(..., max_length=255)
    category: str = Field(..., max_length=100)
    code: Optional[str] = Field(None, max_length=50)
    description: Optional[str] = None
    recommended_experience_years: Optional[int] = Field(0, ge=0)
    education_requirements: Optional[str] = None
    nsqf_level: Optional[int] = Field(None, ge=1, le=8)
    is_active: bool = True
    required_skills: List[OccupationSkillCreate] = []


class OccupationUpdate(BaseModel):
    title: Optional[str] = None
    category: Optional[str] = None
    code: Optional[str] = None
    description: Optional[str] = None
    recommended_experience_years: Optional[int] = None
    education_requirements: Optional[str] = None
    nsqf_level: Optional[int] = None
    is_active: Optional[bool] = None


class OccupationResponse(BaseModel):
    id: uuid.UUID
    code: Optional[str] = None
    title: str
    category: str
    description: Optional[str] = None
    recommended_experience_years: Optional[int] = 0
    education_requirements: Optional[str] = None
    nsqf_level: Optional[int] = None
    is_active: bool
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


# =============================================================================
# 2. Employer & Job Listing Schemas
# =============================================================================

class EmployerCreate(BaseModel):
    name: str = Field(..., max_length=255)
    website: Optional[str] = None
    description: Optional[str] = None
    logo_url: Optional[str] = None
    location: Optional[str] = None
    is_verified: bool = True


class EmployerResponse(BaseModel):
    id: uuid.UUID
    name: str
    website: Optional[str] = None
    description: Optional[str] = None
    logo_url: Optional[str] = None
    location: Optional[str] = None
    is_verified: bool
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class JobRequirementCreate(BaseModel):
    requirement_text: str = Field(..., max_length=500)
    is_mandatory: bool = True


class JobRequirementResponse(BaseModel):
    id: uuid.UUID
    requirement_text: str
    is_mandatory: bool
    model_config = ConfigDict(from_attributes=True)


class JobSkillCreate(BaseModel):
    skill_id: uuid.UUID
    is_mandatory: bool = True
    min_years: Optional[float] = 1.0


class JobSkillResponse(BaseModel):
    id: uuid.UUID
    skill_id: uuid.UUID
    is_mandatory: bool
    min_years: Optional[float] = 1.0
    model_config = ConfigDict(from_attributes=True)


class JobListingCreate(BaseModel):
    title: str = Field(..., max_length=255)
    employer_id: uuid.UUID
    location: str = Field(..., max_length=255)
    country: str = "India"
    description: str
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    salary_currency: str = "INR"
    employment_type: str = "Full-time"
    experience_required_years: Optional[int] = 0
    education_required: Optional[str] = None
    source_type: str = "direct"
    source_url: Optional[str] = None
    expiry_date: Optional[date] = None
    requirements: List[JobRequirementCreate] = []
    skills: List[JobSkillCreate] = []


class JobListingUpdate(BaseModel):
    title: Optional[str] = None
    location: Optional[str] = None
    description: Optional[str] = None
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    employment_type: Optional[str] = None
    experience_required_years: Optional[int] = None
    education_required: Optional[str] = None
    expiry_date: Optional[date] = None
    is_active: Optional[bool] = None


class JobListingResponse(BaseModel):
    id: uuid.UUID
    employer_id: uuid.UUID
    employer: Optional[EmployerResponse] = None
    title: str
    location: str
    country: str = "India"
    description: str
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    salary_currency: str = "INR"
    employment_type: str = "Full-time"
    experience_required_years: Optional[int] = 0
    experience_min_years: Optional[int] = None
    experience_max_years: Optional[int] = None
    education_required: Optional[str] = None
    source_type: str = "direct"
    source_provider: str = "Direct"
    source_url: Optional[str] = None
    application_url: Optional[str] = None
    provider_job_id: Optional[str] = None
    work_mode: str = "On-site"
    required_skills_list: List[str] = []
    last_verified_at: Optional[datetime] = None
    listing_status: str = "active"
    match_details: Optional[Dict[str, Any]] = None
    is_saved: bool = False
    posted_date: Optional[date] = None
    expiry_date: Optional[date] = None
    is_verified: bool = True
    is_active: bool = True
    requirements: List[JobRequirementResponse] = []
    skills: List[JobSkillResponse] = []
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


# =============================================================================
# 3. Assessment Schemas
# =============================================================================

class OptionCreate(BaseModel):
    option_text: str
    is_correct: bool = False
    explanation: Optional[str] = None


class OptionResponse(BaseModel):
    id: uuid.UUID
    option_text: str
    model_config = ConfigDict(from_attributes=True)


class QuestionCreate(BaseModel):
    question_text: str
    question_type: str = "scenario"
    points: int = 1
    order_index: int = 1
    options: List[OptionCreate]


class QuestionResponse(BaseModel):
    id: uuid.UUID
    question_text: str
    question_type: str
    points: int
    order_index: int
    options: List[OptionResponse]
    model_config = ConfigDict(from_attributes=True)


class AssessmentCreate(BaseModel):
    title: str
    description: Optional[str] = None
    skill_id: uuid.UUID
    difficulty_level: str = "intermediate"
    duration_minutes: int = 20
    passing_score_percentage: float = 75.0
    questions: List[QuestionCreate] = []


class AssessmentResponse(BaseModel):
    id: uuid.UUID
    title: str
    description: Optional[str] = None
    skill_id: uuid.UUID
    difficulty_level: str
    duration_minutes: int
    passing_score_percentage: float
    is_active: bool
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class AssessmentStartResponse(BaseModel):
    attempt_id: uuid.UUID
    assessment_id: uuid.UUID
    title: str
    duration_minutes: int
    questions: List[QuestionResponse]


class AnswerSubmission(BaseModel):
    question_id: uuid.UUID
    selected_option_id: uuid.UUID


class AssessmentSubmissionPayload(BaseModel):
    answers: List[AnswerSubmission]


class AssessmentResultResponse(BaseModel):
    attempt_id: uuid.UUID
    assessment_id: uuid.UUID
    score_percentage: float
    points_awarded: float
    total_points: float
    passed: bool
    status: str
    completed_at: datetime


# =============================================================================
# 4. Skill Gap Schemas
# =============================================================================

class SkillGapItemCreate(BaseModel):
    skill_id: uuid.UUID
    current_proficiency: str = "none"
    required_proficiency: str = "intermediate"
    gap_severity: str = "missing"
    priority: str = "high"
    assessment_reference_id: Optional[uuid.UUID] = None


class SkillGapItemResponse(BaseModel):
    id: uuid.UUID
    skill_id: uuid.UUID
    current_proficiency: str
    required_proficiency: str
    gap_severity: str
    priority: str
    assessment_reference_id: Optional[uuid.UUID] = None
    model_config = ConfigDict(from_attributes=True)


class SkillGapReportCreate(BaseModel):
    target_occupation_id: Optional[uuid.UUID] = None
    target_job_id: Optional[uuid.UUID] = None
    overall_match_percentage: float = 0.0
    items: List[SkillGapItemCreate] = []


class SkillGapReportResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    target_occupation_id: Optional[uuid.UUID] = None
    target_job_id: Optional[uuid.UUID] = None
    overall_match_percentage: float
    items: List[SkillGapItemResponse] = []
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


# =============================================================================
# 5. Career Roadmap Schemas
# =============================================================================

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    task_type: str = "practical"
    estimated_hours: Optional[float] = 2.0
    resource_url: Optional[str] = None


class TaskResponse(BaseModel):
    id: uuid.UUID
    title: str
    description: Optional[str] = None
    task_type: str
    estimated_hours: Optional[float] = 2.0
    is_completed: bool
    resource_url: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)


class MilestoneCreate(BaseModel):
    title: str
    description: Optional[str] = None
    order_index: int = 1
    due_date: Optional[date] = None
    tasks: List[TaskCreate] = []


class MilestoneResponse(BaseModel):
    id: uuid.UUID
    title: str
    description: Optional[str] = None
    order_index: int
    due_date: Optional[date] = None
    is_completed: bool
    tasks: List[TaskResponse] = []
    model_config = ConfigDict(from_attributes=True)


class RoadmapCreate(BaseModel):
    title: str
    target_role: str
    target_occupation_id: Optional[uuid.UUID] = None
    estimated_duration_weeks: int = 8
    milestones: List[MilestoneCreate] = []


class RoadmapResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    title: str
    target_role: str
    target_occupation_id: Optional[uuid.UUID] = None
    estimated_duration_weeks: int
    progress_percentage: float
    status: str
    milestones: List[MilestoneResponse] = []
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


# =============================================================================
# 6. Career Transition Schemas
# =============================================================================

class TransferableSkillCreate(BaseModel):
    skill_id: uuid.UUID
    transferability_level: str = "direct"
    notes: Optional[str] = None


class TransferableSkillResponse(BaseModel):
    id: uuid.UUID
    skill_id: uuid.UUID
    transferability_level: str
    notes: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)


class TransitionRequirementCreate(BaseModel):
    title: str
    description: Optional[str] = None
    requirement_type: str = "bridge_training"


class TransitionRequirementResponse(BaseModel):
    id: uuid.UUID
    title: str
    description: Optional[str] = None
    requirement_type: str
    model_config = ConfigDict(from_attributes=True)


class CareerTransitionCreate(BaseModel):
    from_occupation_id: uuid.UUID
    to_occupation_id: uuid.UUID
    transition_title: str
    feasibility_score: float = 85.0
    estimated_transition_months: int = 3
    description: Optional[str] = None
    skills_mapping: List[TransferableSkillCreate] = []
    requirements: List[TransitionRequirementCreate] = []


class CareerTransitionResponse(BaseModel):
    id: uuid.UUID
    from_occupation_id: uuid.UUID
    to_occupation_id: uuid.UUID
    transition_title: str
    feasibility_score: float
    estimated_transition_months: int
    description: Optional[str] = None
    skills_mapping: List[TransferableSkillResponse] = []
    requirements: List[TransitionRequirementResponse] = []
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


# =============================================================================
# 7. Resume Schemas
# =============================================================================

class ResumeSectionCreate(BaseModel):
    section_type: str
    title: str
    content_json: str
    order_index: int = 1


class ResumeSectionResponse(BaseModel):
    id: uuid.UUID
    section_type: str
    title: str
    content_json: str
    order_index: int
    model_config = ConfigDict(from_attributes=True)


class ResumeVersionCreate(BaseModel):
    version_name: str = "v1.0 - Initial Draft"
    raw_content_json: Optional[str] = None
    sections: List[ResumeSectionCreate] = []


class ResumeVersionResponse(BaseModel):
    id: uuid.UUID
    version_number: int
    version_name: str
    raw_content_json: Optional[str] = None
    sections: List[ResumeSectionResponse] = []
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class ResumeDocumentCreate(BaseModel):
    title: str = "My Vocational Trade Resume"
    is_primary: bool = True
    initial_version: Optional[ResumeVersionCreate] = None


class ResumeDocumentResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    title: str
    is_primary: bool
    versions: List[ResumeVersionResponse] = []
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


# =============================================================================
# 8. Interview Schemas
# =============================================================================

class InterviewAnswerCreate(BaseModel):
    question_id: uuid.UUID
    user_response_text: str
    time_taken_seconds: Optional[int] = None


class InterviewAnswerResponse(BaseModel):
    id: uuid.UUID
    question_id: uuid.UUID
    user_response_text: str
    time_taken_seconds: Optional[int] = None
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class InterviewFeedbackCreate(BaseModel):
    technical_accuracy_score: float = 80.0
    clarity_score: float = 85.0
    feedback_summary: str
    areas_of_improvement: Optional[str] = None


class InterviewFeedbackResponse(BaseModel):
    id: uuid.UUID
    technical_accuracy_score: float
    clarity_score: float
    feedback_summary: str
    areas_of_improvement: Optional[str] = None
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class InterviewQuestionCreate(BaseModel):
    question_text: str
    expected_competency: Optional[str] = None
    order_index: int = 1


class InterviewQuestionResponse(BaseModel):
    id: uuid.UUID
    question_text: str
    expected_competency: Optional[str] = None
    order_index: int
    model_config = ConfigDict(from_attributes=True)


class InterviewSessionCreate(BaseModel):
    target_role: str
    trade_category: str
    session_type: str = "technical_diagnostic"
    questions: List[InterviewQuestionCreate] = []


class InterviewSessionResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    target_role: str
    trade_category: str
    session_type: str
    status: str
    questions: List[InterviewQuestionResponse] = []
    answers: List[InterviewAnswerResponse] = []
    feedback: Optional[InterviewFeedbackResponse] = None
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


# =============================================================================
# 9. Application Tracking Schemas
# =============================================================================

class ApplicationNoteCreate(BaseModel):
    note_text: str


class ApplicationNoteResponse(BaseModel):
    id: uuid.UUID
    note_text: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class JobApplicationCreate(BaseModel):
    job_id: uuid.UUID
    cover_note: Optional[str] = None


class JobApplicationStatusUpdate(BaseModel):
    status: str = Field(..., pattern="^(saved|applied|interview|shortlisted|rejected|offer)$")


class JobApplicationResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    job_id: uuid.UUID
    status: str
    applied_at: datetime
    cover_note: Optional[str] = None
    job: Optional[JobListingResponse] = None
    notes: List[ApplicationNoteResponse] = []
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class SavedJobResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    job_id: uuid.UUID
    saved_at: datetime
    job: Optional[JobListingResponse] = None
    model_config = ConfigDict(from_attributes=True)


# =============================================================================
# 10. Learning Resource Schemas
# =============================================================================

class ResourceProviderCreate(BaseModel):
    name: str = Field(..., max_length=255)
    website: Optional[str] = None
    is_verified: bool = True


class ResourceProviderResponse(BaseModel):
    id: uuid.UUID
    name: str
    website: Optional[str] = None
    is_verified: bool
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class LearningResourceCreate(BaseModel):
    title: str = Field(..., max_length=255)
    provider_id: uuid.UUID
    description: Optional[str] = None
    url: str = Field(..., max_length=500)
    language: str = "English"
    cost_type: str = "free"
    cost_amount: Optional[int] = 0
    duration_hours: Optional[float] = 4.0
    skill_ids: List[uuid.UUID] = []


class LearningResourceResponse(BaseModel):
    id: uuid.UUID
    provider_id: uuid.UUID
    provider: Optional[ResourceProviderResponse] = None
    title: str
    description: Optional[str] = None
    url: str
    language: str
    cost_type: str
    cost_amount: Optional[int] = 0
    duration_hours: Optional[float] = 4.0
    is_active: bool
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

