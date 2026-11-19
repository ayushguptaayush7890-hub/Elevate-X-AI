"""
Pydantic v2 schemas for Skills, User-Skill Mapping, and Skill Evidence.
"""

from datetime import datetime
from typing import Optional, List
import uuid
from pydantic import BaseModel, ConfigDict, Field


# -----------------------------------------------------------------------------
# Skill Catalog Schemas
# -----------------------------------------------------------------------------

class SkillCreate(BaseModel):
    """Payload to register a new competency in the catalog."""

    name: str = Field(..., min_length=2, max_length=150)
    category: str = Field(..., max_length=100)
    nsqf_level: Optional[int] = Field(None, ge=1, le=8)
    description: Optional[str] = None


class SkillResponse(BaseModel):
    """Catalog skill representation."""

    id: uuid.UUID
    name: str
    category: str
    nsqf_level: Optional[int] = None
    description: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# -----------------------------------------------------------------------------
# User Skill Schemas
# -----------------------------------------------------------------------------

class UserSkillCreate(BaseModel):
    """Payload to associate a skill with a user's profile."""

    skill_id: Optional[uuid.UUID] = None
    skill_name: Optional[str] = Field(None, description="Creates or links skill by name if skill_id not provided")
    category: Optional[str] = Field("Vocational Skill", description="Category if creating a new skill by name")
    verification_status: str = Field("self_reported", pattern="^(self_reported|assessed|verified)$")
    proficiency_level: str = Field("intermediate", pattern="^(beginner|intermediate|advanced|expert)$")
    years_practiced: Optional[float] = Field(1.0, ge=0.0, le=70.0)
    confidence_score: Optional[float] = Field(0.85, ge=0.0, le=1.0)


class UserSkillUpdate(BaseModel):
    """Payload to update an existing user skill link."""

    verification_status: Optional[str] = Field(None, pattern="^(self_reported|assessed|verified)$")
    proficiency_level: Optional[str] = Field(None, pattern="^(beginner|intermediate|advanced|expert)$")
    years_practiced: Optional[float] = Field(None, ge=0.0, le=70.0)
    confidence_score: Optional[float] = Field(None, ge=0.0, le=1.0)


# -----------------------------------------------------------------------------
# Skill Evidence Schemas
# -----------------------------------------------------------------------------

class SkillEvidenceCreate(BaseModel):
    """Payload to attach verifiable evidence to a user skill."""

    evidence_type: str = Field(..., pattern="^(diagnostic_assessment|workplace_photo|supervisor_endorsement|certificate)$")
    title: str = Field(..., max_length=255)
    description: Optional[str] = None
    file_url: Optional[str] = Field(None, max_length=500)
    score_achieved: Optional[float] = Field(None, ge=0.0, le=100.0)


class SkillEvidenceResponse(BaseModel):
    """Skill evidence response."""

    id: uuid.UUID
    user_skill_id: uuid.UUID
    evidence_type: str
    title: str
    description: Optional[str] = None
    file_url: Optional[str] = None
    score_achieved: Optional[float] = None
    verified_at: Optional[datetime] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserSkillResponse(BaseModel):
    """User skill response including nested skill catalog metadata."""

    id: uuid.UUID
    profile_id: uuid.UUID
    skill_id: uuid.UUID
    skill: SkillResponse
    verification_status: str
    proficiency_level: str
    years_practiced: Optional[float] = 1.0
    confidence_score: Optional[float] = 0.85
    evidences: List[SkillEvidenceResponse] = []
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# -----------------------------------------------------------------------------
# AI Skill Extraction Schemas (Feature 1)
# -----------------------------------------------------------------------------

class ExtractedSkillCrosswalks(BaseModel):
    esco_uri: Optional[str] = None
    onet_soc_code: Optional[str] = None
    nsqf_reference: Optional[str] = None


class ExtractedSkillSpan(BaseModel):
    span_id: str = Field(..., description="Unique span identifier (e.g. SP-01)")
    extracted_skill: str = Field(..., description="Verbatim extracted skill text exactly matching input text slice")
    normalized_skill: Optional[str] = Field(None, description="Normalized professional vocational competency name")
    evidence_text: Optional[str] = Field(None, description="Exact source substring matching text[start_offset:end_offset]")
    start_offset: int = Field(..., ge=0, description="Unicode start character offset in input text")
    end_offset: int = Field(..., ge=0, description="Unicode end character offset in input text")
    skill_category: str = Field(..., description="Functional skill category (e.g. tool_operation, technical_tactile)")
    category_confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence in functional category")
    canonical_skill: Optional[str] = Field(None, description="Mapped canonical competency label")
    canonical_skill_id: Optional[str] = Field(None, description="Identifier of mapped canonical skill")
    mapping_status: str = Field(..., description="Status of ontology mapping: mapped or unmapped")
    is_unmapped_skill: bool = Field(False, description="True if similarity below threshold (0.65)")
    mapping_confidence: float = Field(..., ge=0.0, le=1.0, description="Cosine similarity confidence score")
    human_review_required: bool = Field(False, description="Flag indicating human-in-the-loop review needed")
    crosswalks: ExtractedSkillCrosswalks = Field(default_factory=ExtractedSkillCrosswalks)


class DetectedOccupation(BaseModel):
    occupation_id: str = Field(..., description="Occupation trade code (e.g. TRD-01)")
    occupation_title: str = Field(..., description="Standardized occupation trade title")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Classification confidence")


class SkillExtractionMetadata(BaseModel):
    model_version: str = Field(..., description="Model version or architecture key")
    inference_device: str = Field(..., description="Compute hardware used (MPS / CPU)")
    latency_ms: float = Field(..., description="Inference latency in milliseconds")
    training_safety_gate_status: str = Field("LOCKED", description="Safety gate state for genuine worker data")
    model_provenance: Optional[str] = Field("synthetic_mock_development", description="Training data provenance")
    benchmark_type: Optional[str] = Field("SYNTHETIC DEVELOPMENT BENCHMARK", description="Validation benchmark category")


class SkillExtractionRequest(BaseModel):
    text: str = Field(..., min_length=2, max_length=5000, description="Informal work description (Hindi, Hinglish, English)")
    occupation_hint: Optional[str] = Field(None, description="Optional occupation hint (e.g. TRD-01 or trade name)")
    language_preference: Optional[str] = Field("auto", description="Preferred output language or auto-detect")


class SkillExtractionResponse(BaseModel):
    input_text: str
    detected_occupation: DetectedOccupation
    extracted_skills_count: int
    extracted_skills: List[ExtractedSkillSpan]
    metadata: SkillExtractionMetadata


class SkillExtractionServiceStatus(BaseModel):
    status: str
    active_model: str
    device: str
    training_safety_gate: str
    genuine_worker_records: int
    minimum_required_records: int
    supported_occupations_count: int
    canonical_catalogue_size: int
    model_provenance: Optional[str] = "synthetic_mock_development"
    benchmark_type: Optional[str] = "SYNTHETIC DEVELOPMENT BENCHMARK"


