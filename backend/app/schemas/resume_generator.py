"""
Pydantic schemas for Feature 3: AI-Powered Resume Generator.
Covers personal info, education, categorized skills, work experience,
internships, projects, certifications, additional sections, and AI generation contracts.
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, EmailStr, HttpUrl


class PersonalInfo(BaseModel):
    fullName: str = Field("Candidate", description="Full name of candidate")
    professionalTitle: str = Field("", description="e.g. Senior Software Engineer / AI Researcher")
    email: str = Field("", description="Contact email")
    phone: str = Field("", description="Contact phone")
    location: str = Field("", description="City, State / Country")
    linkedIn: Optional[str] = Field(None, description="LinkedIn profile URL")
    gitHub: Optional[str] = Field(None, description="GitHub profile URL")
    portfolio: Optional[str] = Field(None, description="Portfolio website URL")
    summary: str = Field("", description="Professional executive summary")


class EducationEntry(BaseModel):
    id: str = Field("", description="Unique entry ID")
    institution: str = Field("", description="University / College / School")
    degree: str = Field("", description="Degree (e.g. B.Tech, B.S., M.S.)")
    fieldOfStudy: str = Field("", description="Specialization / Major")
    startDate: str = Field("", description="Start date / year")
    endDate: str = Field("", description="Graduation date / expected graduation")
    grade: Optional[str] = Field(None, description="CGPA / Percentage (e.g. 8.9/10, 3.8/4.0)")
    coursework: List[str] = Field(default_factory=list, description="Relevant coursework topics")


class SkillCategories(BaseModel):
    programmingLanguages: List[str] = Field(default_factory=list)
    frameworks: List[str] = Field(default_factory=list)
    databases: List[str] = Field(default_factory=list)
    developerTools: List[str] = Field(default_factory=list)
    aiMlSkills: List[str] = Field(default_factory=list)
    otherSkills: List[str] = Field(default_factory=list)


class ExperienceEntry(BaseModel):
    id: str = Field("", description="Unique entry ID")
    company: str = Field("", description="Employer company name")
    role: str = Field("", description="Job title")
    employmentType: str = Field("Full-time", description="Full-time, Part-time, Contract, Freelance")
    location: Optional[str] = Field(None, description="Location / Remote")
    startDate: str = Field("", description="Start date")
    endDate: str = Field("", description="End date or 'Present'")
    current: bool = Field(False, description="Is currently working here")
    responsibilities: List[str] = Field(default_factory=list, description="Key responsibilities and bullet points")


class InternshipEntry(BaseModel):
    id: str = Field("", description="Unique entry ID")
    organization: str = Field("", description="Company / Institute name")
    role: str = Field("", description="Intern role title")
    duration: str = Field("", description="e.g. May 2024 - July 2024 (3 months)")
    workPerformed: List[str] = Field(default_factory=list, description="Bullet points of contributions")
    achievements: List[str] = Field(default_factory=list, description="Key deliverables or outcomes")


class ProjectEntry(BaseModel):
    id: str = Field("", description="Unique entry ID")
    title: str = Field("", description="Project name")
    description: str = Field("", description="Brief overview of project")
    technologies: List[str] = Field(default_factory=list, description="Tech stack used")
    contributions: List[str] = Field(default_factory=list, description="Key contributions and achievements")
    projectUrl: Optional[str] = Field(None, description="Live deployment URL")
    githubUrl: Optional[str] = Field(None, description="Source code repository URL")


class CertificationEntry(BaseModel):
    id: str = Field("", description="Unique entry ID")
    name: str = Field("", description="Certificate name")
    issuingOrganization: str = Field("", description="Issuing organization")
    issueDate: str = Field("", description="Date of issuance")
    credentialUrl: Optional[str] = Field(None, description="Verification URL")


class AdditionalSections(BaseModel):
    achievements: List[str] = Field(default_factory=list)
    awards: List[str] = Field(default_factory=list)
    publications: List[str] = Field(default_factory=list)
    volunteerExperience: List[str] = Field(default_factory=list)
    extracurricular: List[str] = Field(default_factory=list)
    languages: List[str] = Field(default_factory=list)
    interests: List[str] = Field(default_factory=list)


class ResumeFullData(BaseModel):
    personalInfo: PersonalInfo
    education: List[EducationEntry] = Field(default_factory=list)
    skills: SkillCategories = Field(default_factory=SkillCategories)
    experience: List[ExperienceEntry] = Field(default_factory=list)
    internships: List[InternshipEntry] = Field(default_factory=list)
    projects: List[ProjectEntry] = Field(default_factory=list)
    certifications: List[CertificationEntry] = Field(default_factory=list)
    additional: AdditionalSections = Field(default_factory=AdditionalSections)
    templateId: str = Field("modern", description="Template identifier")
    accentColor: str = Field("#17233F", description="Hex accent color")
    typography: str = Field("sans", description="sans, serif, or mono")
    spacing: str = Field("normal", description="compact, normal, or relaxed")


class AIGenerateResumeRequest(BaseModel):
    rawResumeData: ResumeFullData
    targetRole: Optional[str] = Field(None, description="Optional target job title to steer tone")
    instruction: Optional[str] = Field(None, description="Specific customization instruction")


class AIGenerateResumeResponse(BaseModel):
    enhancedResumeData: ResumeFullData
    recommendedTemplate: str
    recommendationReason: str
    generationLatencyMs: float
    modelName: str
    modificationsSummary: List[str]


class RecommendDesignRequest(BaseModel):
    resumeData: ResumeFullData
    targetRole: Optional[str] = Field(None, description="Target job title to steer design selection")
    candidateDesignCatalog: Optional[List[Dict[str, Any]]] = Field(None, description="Optional subset of design specifications")


class RecommendDesignResponse(BaseModel):
    recommendedDesignId: str
    explanation: str
    matchingProfileCharacteristics: List[str]
    whyAppropriate: str
    isFallback: bool = False
    fallbackReason: Optional[str] = None
    latencyMs: float
    modelName: str


class AIEnhanceTextRequest(BaseModel):
    text: str = Field(..., min_length=3)
    sectionType: str = Field(..., description="summary, experience, project, achievement")
    contextRole: Optional[str] = None


class AIEnhanceTextResponse(BaseModel):
    originalText: str
    enhancedText: str
    suggestedBullets: List[str] = Field(default_factory=list)
    latencyMs: float


class SaveResumeRequest(BaseModel):
    resumeId: Optional[str] = None
    title: str = "My Professional Resume"
    resumeData: ResumeFullData
    isPrimary: bool = True


class SaveResumeResponse(BaseModel):
    success: bool
    resumeId: str
    versionId: str
    title: str
    updatedAt: str
    message: str


# =====================================================================
# ATS INTELLIGENCE & RESUME UPLOAD SCHEMAS
# =====================================================================

class ATSJobDescriptionAnalysisRequest(BaseModel):
    jobDescriptionText: str = Field(..., min_length=20, description="Raw job description text")
    jobTitle: Optional[str] = Field(None, description="Job title if known")


class ATSJobDescriptionAnalysisResponse(BaseModel):
    jobTitle: str
    seniorityLevel: str
    requiredSkills: List[str]
    preferredSkills: List[str]
    qualifications: List[str]
    keyResponsibilities: List[str]
    sourceEvidence: Dict[str, List[str]] = Field(default_factory=dict)
    analysisLatencyMs: float


class RequirementMatch(BaseModel):
    requirement: str
    category: str  # required_skill, preferred_skill, qualification, responsibility
    status: str    # explicitly_matched, partially_supported, not_found_in_resume, uncertain_extraction, confirmed_missing
    statusLabel: str = "Not Found in Text"
    similarityScore: float
    resumeEvidence: Optional[str] = None
    jdEvidence: Optional[str] = None
    auditNote: Optional[str] = None


class PartADetails(BaseModel):
    requiredSkillsScore: float = Field(..., description="Max 25 points")
    preferredSkillsScore: float = Field(..., description="Max 10 points")
    responsibilitiesScore: float = Field(..., description="Max 15 points")
    qualificationsScore: float = Field(..., description="Max 10 points")


class PartBDetails(BaseModel):
    actionVerbsAndImpactScore: float = Field(..., description="Max 15 points")
    formattingAndParseabilityScore: float = Field(..., description="Max 10 points")
    sectionCompletenessScore: float = Field(..., description="Max 15 points")


class ATSScoreBreakdown(BaseModel):
    rubricName: str = "Elevate X Internal Compatibility Rubric (Deterministic 100-Point Audit)"
    partAScore: float = Field(..., description="Job Requirement Alignment (Max 60)")
    partBScore: float = Field(..., description="Resume Document Quality (Max 40)")
    totalScore: float = Field(..., description="Total ATS Score (Max 100)")
    partADetails: PartADetails
    partBDetails: PartBDetails
    explanation: str
    methodologyDisclaimer: str = (
        "This score is an internal deterministic algorithmic audit based on text similarity and document structure. "
        "It is not an official or proprietary vendor ATS algorithm."
    )


class ATSMatchRequest(BaseModel):
    resumeData: Optional[ResumeFullData] = None
    parsedResume: Optional[Dict[str, Any]] = None
    jobDescription: str = Field(..., min_length=20)
    jobTitle: Optional[str] = None


class ATSMatchResponse(BaseModel):
    overallScore: float
    breakdown: ATSScoreBreakdown
    explicitMatches: List[RequirementMatch] = Field(default_factory=list)
    partialMatches: List[RequirementMatch] = Field(default_factory=list)
    notFoundRequirements: List[RequirementMatch] = Field(default_factory=list)
    uncertainExtractions: List[RequirementMatch] = Field(default_factory=list)
    confirmedMissing: List[RequirementMatch] = Field(default_factory=list)
    # Backwards compatibility aliases
    strongMatches: List[RequirementMatch] = Field(default_factory=list)
    missingRequirements: List[RequirementMatch] = Field(default_factory=list)
    strengthsSummary: List[str]
    criticalGapsSummary: List[str]
    evaluatedAt: str


class AIImprovementRequest(BaseModel):
    resumeData: ResumeFullData
    jobDescription: str
    gapRequirements: List[str] = Field(default_factory=list)


class AIImprovementSuggestion(BaseModel):
    id: str
    targetSection: str
    originalText: str
    suggestedText: str
    starMethodologyNotes: str
    missingEvidenceQuestion: Optional[str] = None
    rationale: str
    status: str = "pending"  # pending, accepted, rejected


class AIImprovementResponse(BaseModel):
    suggestions: List[AIImprovementSuggestion]
    targetedQuestions: List[str]
    groundingDisclaimer: str

