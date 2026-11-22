"""
Pydantic Schemas for Career Transition & Skill Transferability Engine.
Includes Academic Background, Competency Evidence, and Model-Driven Recommendations.
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class OccupationSearchItem(BaseModel):
    canonical_id: str
    title: str
    source: str
    code: Optional[str] = None
    description: Optional[str] = None
    isco_group: Optional[str] = None


class AcademicCompetencyItem(BaseModel):
    competency_name: str
    original_evidence: str
    evidence_type: str = Field(
        ...,
        description="One of: academic_degree, academic_coursework, academic_project, academic_certification"
    )
    source_record: str
    confidence_score: float = Field(default=0.7, ge=0.0, le=1.0)
    requires_practical_validation: bool = True
    matched_target_skills: List[str] = []
    semantic_similarity: Optional[float] = None


class AcademicProfileSummary(BaseModel):
    has_academic_profile: bool = False
    institution: Optional[str] = None
    degree: Optional[str] = None
    field_of_study: Optional[str] = None
    academic_competencies: List[AcademicCompetencyItem] = []
    academic_projects: List[str] = []
    source_notice: Optional[str] = None


class CompetencyEvidenceItem(BaseModel):
    name: str
    skill_id: Optional[str] = None
    evidence_state: str = Field(
        ...,
        description="One of: assessment_verified, practically_demonstrated, academic_evidence, mentioned_in_resume, self_reported, related_taxonomy_evidence, not_assessed",
    )
    evidence_score: float = Field(default=0.0, ge=0.0, le=1.0)
    importance: str = Field(default="essential", description="essential or optional")
    notes: Optional[str] = None
    requires_practical_validation: bool = False


class TransitionRecommendationItem(BaseModel):
    target_occupation_id: str
    target_title: str
    target_source: str
    target_code: Optional[str] = None
    target_description: Optional[str] = None
    fit_percentage: float = Field(..., ge=0.0, le=100.0)
    transition_delta: float = Field(..., ge=0.0, le=100.0)
    difficulty_category: str = Field(..., description="Low Friction, Moderate Bridge, or High Pivot")
    estimated_months: int = Field(default=3, ge=1)
    salary_range: Optional[str] = None
    demand_level: str = Field(default="Moderate", description="High, Moderate, or Emerging")
    demand_postings_count: int = 0
    transferable_skills_count: int = 0
    bridgeable_skills_count: int = 0
    missing_skills_count: int = 0
    academic_relevance_score: float = Field(default=0.0, ge=0.0, le=100.0)
    academic_matched_skills_count: int = 0
    transferable_competencies_preview: List[str] = []
    bridgeable_competencies_preview: List[str] = []
    scoring_basis: Optional[str] = "Multi-Factor (BGE Semantic + Graph Structure + Academic Relevance)"


class TransitionRecommendationsRequest(BaseModel):
    current_occupation: str
    candidate_skills: Optional[List[str]] = None
    limit: int = Field(default=6, ge=1, le=20)


class TransitionAnalysisRequest(BaseModel):
    from_occupation: str
    to_occupation: str
    candidate_skills: Optional[List[str]] = None


class TransitionAnalysisResponse(BaseModel):
    from_occupation_id: str
    from_occupation_title: str
    to_occupation_id: str
    to_occupation_title: str
    to_taxonomy: str
    fit_percentage: float
    transition_delta: float
    difficulty_category: str
    estimated_months: int
    salary_range: Optional[str] = None
    demand_level: str
    demand_postings_count: int = 0
    transferable_competencies: List[CompetencyEvidenceItem]
    bridgeable_competencies: List[CompetencyEvidenceItem]
    missing_competencies: List[CompetencyEvidenceItem]
    academic_profile: Optional[AcademicProfileSummary] = None
    academic_matches: List[AcademicCompetencyItem] = []
    scoring_explanation: Optional[Dict[str, Any]] = None


class TransitionBlueprintStage(BaseModel):
    stage_id: Optional[str] = None
    stage_number: int
    stage_name: str
    timeframe: str
    duration_weeks: Optional[int] = None
    workload_hours_per_week: Optional[int] = 12
    objective: str
    target_competencies: List[str] = []
    competency_ids: List[str] = []
    candidate_evidence: Optional[str] = None
    practical_tasks: List[str] = []
    milestones: List[str] = []
    tasks: List[str] = []
    measurable_deliverables: List[str] = []
    recommended_resources: List[Dict[str, Any]] = []


class TransitionBlueprintRequest(BaseModel):
    from_occupation: str
    to_occupation: str
    candidate_skills: Optional[List[str]] = None
    recalibrate: Optional[bool] = False


class TransitionBlueprintResponse(BaseModel):
    transition_id: Optional[str] = None
    from_occupation_id: Optional[str] = None
    from_occupation: str
    target_occupation_id: Optional[str] = None
    target_occupation: str
    overall_fit: float
    total_estimated_weeks: int
    stages: List[TransitionBlueprintStage]
    generated_by: str
    model_used: str
    blueprint_version: str = "v2.0-dynamic"
    evidence_fingerprint: Optional[str] = None
    personalization_summary: Optional[str] = None
    cached: bool = False


class TransitionCompareRequest(BaseModel):
    current_occupation: str
    target_occupations: List[str]
    candidate_skills: Optional[List[str]] = None


class AdoptGoalRequest(BaseModel):
    from_occupation_title: str
    target_occupation_id: str
    target_occupation_title: str
    fit_percentage: float
    transition_delta: float
    difficulty_category: str
    blueprint: Optional[Dict[str, Any]] = None
    academic_evidence: Optional[List[Dict[str, Any]]] = None
    transferable_competencies: Optional[List[str]] = None
    missing_competencies: Optional[List[str]] = None
    scoring_methodology: Optional[str] = "BGE-Small v1.5 + Node2Vec Graph v2.1"


class AdoptGoalResponse(BaseModel):
    success: bool
    goal_id: str
    message: str
    roadmap_id: Optional[str] = None
    target_occupation_title: Optional[str] = None
    fit_percentage: Optional[float] = None
    status: Optional[str] = "active"


class UserGoalProgressItem(BaseModel):
    goal_id: str
    from_occupation_title: str
    target_occupation_title: str
    fit_percentage: float
    difficulty_category: str
    status: str
    progress_percentage: float
    created_at: str
    academic_evidence_summary: Optional[str] = None
