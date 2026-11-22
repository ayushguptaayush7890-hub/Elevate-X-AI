"""
Pydantic Schemas for Skill Gap Analyzer (Feature 4).
Supports authentic ESCO, O*NET, and verified learning resource catalogs with BGE & Qwen ML inference.
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class LearningResourceItem(BaseModel):
    id: str = Field(..., description="Unique resource identifier")
    title: str = Field(..., description="Genuine title of documentation or course")
    provider: str = Field(..., description="Official provider (e.g. Python Foundation, PyTorch, Microsoft Learn)")
    url: str = Field(..., description="Verified official URL")
    skills: List[str] = Field(default_factory=list, description="Skills covered")
    difficulty: str = Field("Intermediate", description="Beginner, Intermediate, Advanced")
    type: str = Field("Documentation", description="Official Documentation, Tutorial, Certification")
    verified: bool = Field(True, description="Strictly true only if link is officially verified")


class SkillCompetencyItem(BaseModel):
    skillName: str = Field(..., description="Occupation requirement or skill phrase")
    canonicalName: str = Field(..., description="Canonical ESCO / O*NET name")
    category: str = Field("Technical Skill", description="Category label")
    status: str = Field("skill_gap", description="verified_match, partially_supported, skill_gap, not_assessed")
    importance: str = Field("essential", description="essential, optional, in_demand")
    candidateLevel: str = Field("Not Assessed", description="None, Foundational, Intermediate, Advanced, Not Assessed")
    expectedLevel: str = Field("Intermediate", description="Expected proficiency level")
    similarityScore: float = Field(0.0, description="Genuine cosine similarity (0.0 to 1.0) via BGE embeddings")
    lexicalMatch: bool = Field(False, description="Whether an exact canonical or verified alternative label matched")
    competencySource: str = Field("ESCO Essential", description="Source specification of the competency requirement")
    evidence: Optional[str] = Field(None, description="Verifiable candidate evidence or source line citation")
    priorityRank: int = Field(1, description="1 (Critical Priority) to 5 (Elective)")
    recommendedResources: List[LearningResourceItem] = Field(default_factory=list)


class WeeklyMilestone(BaseModel):
    week: int
    title: str
    focusSkills: List[str]
    actionItems: List[str]
    suggestedResourceUrl: Optional[str] = None


class AILearningRoadmap(BaseModel):
    targetRole: str
    overallMatchScore: float
    executiveSummary: str
    weeklyMilestones: List[WeeklyMilestone] = Field(default_factory=list)
    practicalProjects: List[str] = Field(default_factory=list)
    assessmentMilestones: List[str] = Field(default_factory=list)
    generatedByModel: str = Field("mlx-community/Qwen2.5-1.5B-Instruct-4bit", description="ML model responsible for generation")
    resourceValidationPassed: bool = Field(True, description="True if all suggested URLs verified against official catalog")
    validatedUrlsCount: int = Field(0, description="Number of verified URLs matched in roadmap")
    error: Optional[str] = Field(None, description="Reported model generation or validation error, if any")
    groundingDisclaimer: str = Field(
        "Roadmap synthesized strictly from verified candidate skills and authentic occupational requirements without hallucinated qualifications."
    )


class SkillGapAnalyzeRequest(BaseModel):
    candidateSkills: List[str] = Field(default_factory=list, description="List of verified candidate skills")
    targetOccupationTitle: str = Field("AI / Machine Learning Engineer", description="Target role or occupation title")
    targetOccupationSource: Optional[str] = Field("esco", description="esco, onet, or job_description")
    customJobDescription: Optional[str] = Field(None, description="Optional authentic raw job description text")
    includeAiStrategy: Optional[bool] = Field(True, description="Whether to invoke local LLM (Qwen2.5) for strategy")


class SkillGapAnalyzeResponse(BaseModel):
    targetOccupation: str
    sourceTaxonomy: str
    overallMatchScore: float
    totalCompetenciesRequired: int
    verifiedSkillsCount: int
    partialSkillsCount: int
    gapSkillsCount: int
    unmatchedSkillsCount: int = 0
    coverageScoreExplanation: str = Field(
        "Transparent competency coverage score based on authentic ESCO essential (weight 1.0) and optional (weight 0.5) requirements. Not a calibrated job-readiness probability."
    )
    competencies: List[SkillCompetencyItem] = Field(default_factory=list)
    learningResources: List[LearningResourceItem] = Field(default_factory=list)
    aiStrategy: Optional[AILearningRoadmap] = None
    evaluatedAt: str


class OccupationSearchItem(BaseModel):
    title: str
    source: str
    totalCompetencies: int
    description: Optional[str] = None
