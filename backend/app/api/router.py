"""
Central API Router uniting all versioned API endpoints for Elevate X AI.
"""

from fastapi import APIRouter
from app.api.v1 import (
    health,
    auth,
    profile,
    skill,
    occupations,
    jobs,
    assessments,
    technical_assessments,
    skill_gaps,
    roadmaps,
    career_transitions,
    resumes,
    interviews,
    applications,
    resources,
)

api_router = APIRouter()

# 1. Health & Diagnostics
api_router.include_router(health.router, prefix="/health", tags=["Health & Diagnostics"])

# 2. Authentication & User Management
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])

# 3. User Profiles, Education, and Work Experience
api_router.include_router(profile.router, prefix="/profiles", tags=["User Profiles"])

# 4. User Profile Skills
api_router.include_router(skill.profile_skills_router, prefix="/profiles", tags=["Profile Skills"])

# 5. Global Skills Catalog
api_router.include_router(skill.catalog_router, prefix="/skills", tags=["Skills Catalog"])

# 6. Occupation Catalog & NSQF Taxonomy
api_router.include_router(occupations.router, prefix="/occupations", tags=["Occupation Management"])

# 7. Job Opportunities & Employers
api_router.include_router(jobs.router, prefix="/jobs", tags=["Job Management"])

# 8. Skill Assessments & Verification
api_router.include_router(technical_assessments.router, prefix="/assessments/technical", tags=["Feature 2: Technical Assessments"])
api_router.include_router(technical_assessments.router, prefix="/technical-assessments", tags=["Feature 2: Technical Assessments"])
api_router.include_router(assessments.router, prefix="/assessments", tags=["Skill Assessment Foundation"])



# 9. Skill Gap Analysis & Delta Evaluation
api_router.include_router(skill_gaps.router, prefix="/skill-gaps", tags=["Skill Gap Management"])

# 10. Career Roadmaps & Progress Tracking
api_router.include_router(roadmaps.router, prefix="/roadmaps", tags=["Career Roadmap"])

# 11. Career Transition Pathways
api_router.include_router(career_transitions.router, prefix="/career-transitions", tags=["Career Transition"])

# 12. Structured Resume Documents
api_router.include_router(resumes.router, prefix="/resumes", tags=["Resume Management"])

# 13. Interview Diagnostic Sessions & Feedback
api_router.include_router(interviews.router, prefix="/interviews", tags=["Interview Management"])

# 14. Job Application Tracking & Saved Jobs
api_router.include_router(applications.router, prefix="/applications", tags=["Application Tracking"])
api_router.include_router(applications.saved_router, prefix="/saved-jobs", tags=["Saved Jobs"])

# 15. Curated Learning Resources & Providers
api_router.include_router(resources.router, prefix="/resources", tags=["Learning Resources"])
