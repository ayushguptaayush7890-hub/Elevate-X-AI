"""
Pydantic schemas for Dynamic Career Roadmaps, Progressive Milestones, and Hands-on Tasks.
"""

from datetime import datetime, date
from typing import List, Optional, Any, Dict
import uuid
from pydantic import BaseModel, Field, ConfigDict, model_validator


class LearningResourceRef(BaseModel):
    name: str
    title: Optional[str] = None
    type: str = "Official Documentation"
    duration: str = "Self-paced"
    free: bool = True
    url: Optional[str] = None
    source_domain: Optional[str] = None


class TaskDetail(BaseModel):
    id: str
    milestone_id: Optional[str] = None
    title: str
    description: Optional[str] = None
    task_type: str = "practical"  # practical, learning, assessment, portfolio
    estimated_hours: float = 2.0
    is_completed: bool = False
    resource_url: Optional[str] = None
    resource_title: Optional[str] = None


class MilestoneDetail(BaseModel):
    id: str
    stage_number: int = 1
    stageNumber: int = 1
    order_index: Optional[int] = None
    title: str
    description: str
    rationale: Optional[str] = None
    time_estimate: str = "3-4 Weeks"
    timeEstimate: str = "3-4 Weeks"
    status: str = "upcoming"  # completed, in_progress, upcoming, blocked
    is_completed: bool = False
    competency_evidence: Dict[str, str] = Field(default_factory=dict)
    competencyEvidence: Dict[str, str] = Field(default_factory=dict)
    skills_to_acquire: List[str] = Field(default_factory=list)
    skillsToAcquire: List[str] = Field(default_factory=list)
    practical_tasks: List[str] = Field(default_factory=list)
    practicalTasks: List[str] = Field(default_factory=list)
    tasks: List[TaskDetail] = Field(default_factory=list)
    resources: List[LearningResourceRef] = Field(default_factory=list)

    model_config = ConfigDict(populate_by_name=True, from_attributes=True)

    @model_validator(mode="before")
    @classmethod
    def sync_dual_fields(cls, data: Any):
        if isinstance(data, dict):
            num = data.get("stage_number") or data.get("stageNumber") or data.get("order_index") or 1
            data["stage_number"] = int(num)
            data["stageNumber"] = int(num)
            data["order_index"] = int(num)

            time_val = data.get("time_estimate") or data.get("timeEstimate") or "3-4 Weeks"
            data["time_estimate"] = str(time_val)
            data["timeEstimate"] = str(time_val)

            skills = data.get("skills_to_acquire") or data.get("skillsToAcquire") or []
            data["skills_to_acquire"] = list(skills)
            data["skillsToAcquire"] = list(skills)

            tasks = data.get("practical_tasks") or data.get("practicalTasks") or []
            data["practical_tasks"] = list(tasks)
            data["practicalTasks"] = list(tasks)

            ev = data.get("competency_evidence") or data.get("competencyEvidence") or {}
            data["competency_evidence"] = dict(ev)
            data["competencyEvidence"] = dict(ev)
        return data


class CareerRoadmapDetailResponse(BaseModel):
    id: str
    user_id: Optional[str] = None
    title: str
    target_role: str
    target_occupation_id: Optional[str] = None
    resolved_canonical_title: Optional[str] = None
    occupation_domain: Optional[str] = None
    resolution_confidence: Optional[float] = None
    estimated_duration_weeks: int = 8
    progress_percentage: float = 0.0
    status: str = "active"
    total_milestones: int = 0
    completed_milestones: int = 0
    total_tasks: int = 0
    completed_tasks: int = 0
    estimated_total_hours: float = 0.0
    milestones: List[MilestoneDetail] = Field(default_factory=list)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(populate_by_name=True, from_attributes=True)


class CareerRoadmapGenerateRequest(BaseModel):
    target_role: str
    candidate_skills: Optional[List[str]] = None
    experience_level: Optional[str] = "mid"


class CareerRoadmapGoalUpdateRequest(BaseModel):
    target_role: str


class CareerRoadmapRecalibrateRequest(BaseModel):
    target_role: Optional[str] = None
    candidate_skills: Optional[List[str]] = None
