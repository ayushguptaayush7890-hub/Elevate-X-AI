"""
Pydantic Request and Response Schemas for Feature 2 Technical Assessment Engine.
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
import uuid

class SkillItem(BaseModel):
    skill_id: str
    name: str
    subtopics: List[str]

class RoleSummaryResponse(BaseModel):
    role_id: str
    title: str
    category: str
    description: str
    skill_count: int

class RoleDetailResponse(BaseModel):
    role_id: str
    title: str
    category: str
    description: str
    skills: List[SkillItem]

class TechnicalAssessmentStartRequest(BaseModel):
    role_id: str
    skill_id: Optional[str] = None
    assessment_type: Optional[str] = None
    difficulty: Optional[str] = "adaptive"  # "easy", "medium", "hard", "adaptive"
    question_count: int = Field(default=10, ge=1, le=50)

class TechnicalQuestionMasked(BaseModel):
    question_id: str
    role_id: str
    skill_id: str
    skill_name: str
    subtopic: Optional[str] = None
    assessment_type: str
    difficulty: str
    question_text: str
    options: Optional[List[Dict[str, Any]]] = None
    coding_language: Optional[str] = None
    sample_input: Optional[str] = None
    expected_output: Optional[str] = None
    visible_test_cases: Optional[List[Dict[str, Any]]] = None
    SQL_schema: Optional[str] = None
    sample_database: Optional[str] = None
    evaluation_rubric: Optional[Any] = None
    estimated_time: Optional[int] = 10
    marks: Optional[int] = 5

class TechnicalAssessmentStartResponse(BaseModel):
    session_id: str
    role_id: str
    role_title: str
    difficulty_mode: str
    duration_minutes: int
    expiry_timestamp: Optional[float] = None
    total_questions: int
    questions: List[TechnicalQuestionMasked]

class SingleAnswerSubmission(BaseModel):
    question_id: str
    answer: Any  # Option ID string, Python code string, SQL query string, or scenario text
    language: Optional[str] = None
    time_taken_seconds: Optional[int] = 0

class TechnicalAssessmentSubmitRequest(BaseModel):
    session_id: str
    role_id: str
    answers: List[SingleAnswerSubmission]

class SkillPerformanceItem(BaseModel):
    skill_id: str
    skill_name: str
    mastery_percentage: float
    confidence: float
    evidence_count: int
    correct_count: int
    status: str

class SkillGapItem(BaseModel):
    skill_id: str
    skill_name: str
    current_level: float
    target_level: float
    gap_delta: float
    priority: str
    confidence: float

class RoadmapMilestoneItem(BaseModel):
    milestone_id: str
    order_index: int
    skill_id: str
    skill_name: str
    priority: str
    current_mastery: float
    target_mastery: float
    gap_delta: float
    estimated_hours: int
    reason: str
    learning_objective: str
    hands_on_task: str
    resource_title: str
    resource_type: str
    resource_url: str
    status: str

class EvaluatedAnswerItem(BaseModel):
    question_id: str
    assessment_type: str
    is_correct: bool
    points_awarded: float
    max_points: float
    user_answer: Any
    correct_answer: Optional[str] = None
    explanation: Optional[str] = None
    feedback: Optional[str] = None

class TechnicalAssessmentResultResponse(BaseModel):
    result_id: str
    session_id: str
    user_id: str
    role_id: str
    role_title: str
    overall_score_percentage: float
    points_awarded: float
    total_points: float
    passed: bool
    status: str
    completed_at: datetime
    difficulty_mode: str
    ability_theta: Optional[float] = None
    skill_performances: List[SkillPerformanceItem]
    skill_gaps: List[SkillGapItem]
    roadmap_milestones: List[RoadmapMilestoneItem]
    narrative_summary: Optional[Dict[str, Any]] = None
    evaluated_answers: Optional[List[EvaluatedAnswerItem]] = None

class CodeRunRequest(BaseModel):
    question_id: Optional[str] = None
    language: str = "python"
    code: str
    visible_test_cases: Optional[List[Dict[str, Any]]] = None

class CodeRunResponse(BaseModel):
    passed: bool
    score: float
    total_tests: int
    passed_tests: int
    test_results: List[Dict[str, Any]]
    error: Optional[str] = None
    execution_time_ms: float

class SQLRunRequest(BaseModel):
    question_id: Optional[str] = None
    candidate_query: str
    schema_sql: Optional[str] = None
    sample_db_sql: Optional[str] = None

class SQLRunResponse(BaseModel):
    passed: bool
    score: float
    actual_rows: List[Dict[str, Any]]
    error: Optional[str] = None
    execution_time_ms: float

class AdaptiveStepRequest(BaseModel):
    session_id: str
    question_id: str
    answer: Any
    time_taken_seconds: Optional[int] = 0

class AdaptiveStepResponse(BaseModel):
    is_correct: bool
    points_awarded: float
    explanation: str
    current_theta: float
    recommended_difficulty: str
    next_question: Optional[TechnicalQuestionMasked] = None
    is_completed: bool

class AssessmentSessionProgressRequest(BaseModel):
    current_index: int
    answers: Dict[str, Any]

class AssessmentSessionStateResponse(BaseModel):
    session_id: str
    role_id: str
    role_title: str
    difficulty_mode: str
    questions: List[TechnicalQuestionMasked]
    current_index: int
    answers: Dict[str, Any]
    time_left_seconds: int
    remaining_seconds: Optional[int] = None
    is_expired: bool
    total_questions: int
