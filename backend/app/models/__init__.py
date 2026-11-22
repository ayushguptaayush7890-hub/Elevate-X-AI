"""
Database Models Package.
Exports all SQLAlchemy 2.0 models for migration discovery across Phase 1, 2, and 3.
"""

from app.core.database import Base
from app.models.base import TimestampMixin
from app.models.user import User, PasswordResetToken, RevokedToken
from app.models.profile import UserProfile, Education, WorkExperience, CareerPreference
from app.models.skill import Skill, UserSkill, SkillEvidence
from app.models.occupation import Occupation, OccupationSkill
from app.models.job import Employer, JobListing, JobRequirement, JobSkill, AggregatorSyncLog
from app.models.assessment import (
    Assessment,
    AssessmentQuestion,
    AssessmentOption,
    AssessmentAttempt,
    AssessmentAnswer,
    AssessmentResult,
)
from app.models.skill_gap import SkillGapReport, SkillGapItem
from app.models.roadmap import CareerRoadmap, RoadmapMilestone, RoadmapTask
from app.models.career_transition import (
    CareerTransition,
    TransferableSkillMapping,
    TransitionRequirement,
    UserCareerTransitionGoal,
)
from app.models.resume import ResumeDocument, ResumeVersion, ResumeSection
from app.models.interview import (
    InterviewSession,
    InterviewQuestion,
    InterviewAnswer,
    InterviewFeedback,
)
from app.models.application import JobApplication, SavedJob, ApplicationNote
from app.models.learning_resource import ResourceProvider, LearningResource, ResourceSkill
from app.models.consultation import Consultation, ConsultationMessage

__all__ = [
    "Base",
    "TimestampMixin",
    "User",
    "PasswordResetToken",
    "RevokedToken",
    "UserProfile",
    "Education",
    "WorkExperience",
    "CareerPreference",
    "Skill",
    "UserSkill",
    "SkillEvidence",
    "Occupation",
    "OccupationSkill",
    "Employer",
    "JobListing",
    "JobRequirement",
    "JobSkill",
    "AggregatorSyncLog",
    "Assessment",
    "AssessmentQuestion",
    "AssessmentOption",
    "AssessmentAttempt",
    "AssessmentAnswer",
    "AssessmentResult",
    "SkillGapReport",
    "SkillGapItem",
    "CareerRoadmap",
    "RoadmapMilestone",
    "RoadmapTask",
    "CareerTransition",
    "TransferableSkillMapping",
    "TransitionRequirement",
    "UserCareerTransitionGoal",
    "ResumeDocument",
    "ResumeVersion",
    "ResumeSection",
    "InterviewSession",
    "InterviewQuestion",
    "InterviewAnswer",
    "InterviewFeedback",
    "JobApplication",
    "SavedJob",
    "ApplicationNote",
    "ResourceProvider",
    "LearningResource",
    "ResourceSkill",
    "Consultation",
    "ConsultationMessage",
]
