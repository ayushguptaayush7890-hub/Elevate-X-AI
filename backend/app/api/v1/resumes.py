"""
API Router for Feature 3: AI-Powered Resume Generator, Structured Templates,
Versioning, and Multi-Format Exports (PDF/DOCX).
"""

from typing import List, Optional
import uuid
import json
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Response, Request, UploadFile, File
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select

from app.core.database import get_db
from app.api.deps import get_current_user, get_current_active_user, oauth2_scheme
from app.models.user import User
from app.models.resume import (
    ResumeDocument,
    ResumeVersion,
    ResumeSection,
)
from app.schemas.career_domain import (
    ResumeDocumentCreate,
    ResumeDocumentResponse,
    ResumeVersionCreate,
    ResumeVersionResponse,
)
from app.schemas.resume_generator import (
    ResumeFullData,
    AIGenerateResumeRequest,
    AIGenerateResumeResponse,
    AIEnhanceTextRequest,
    AIEnhanceTextResponse,
    SaveResumeRequest,
    SaveResumeResponse,
    RecommendDesignRequest,
    RecommendDesignResponse,
    ATSJobDescriptionAnalysisRequest,
    ATSJobDescriptionAnalysisResponse,
    ATSMatchRequest,
    ATSMatchResponse,
    AIImprovementRequest,
    AIImprovementResponse,
)
from app.services.resume_ai_generator import ResumeAIGeneratorService
from app.services.resume_docx_service import ResumeDocxService
from app.services.resume_parser_service import ResumeParserService
from app.services.ats_matcher_service import ATSMatcherService
from app.services.ats_improvement_service import ATSImprovementService

router = APIRouter()


def _get_optional_user(
    request: Request,
    db: Session = Depends(get_db)
) -> Optional[User]:
    """Helper to authenticate user if Bearer token present, otherwise return None (guest mode)."""
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return None
    token = auth_header.split(" ")[1]
    try:
        from app.core.security import decode_token
        payload = decode_token(token)
        user_id_str = payload.get("sub")
        if user_id_str:
            user_id = uuid.UUID(user_id_str)
            return db.execute(select(User).where(User.id == user_id)).scalar_one_or_none()
    except Exception:
        return None
    return None


# =============================================================================
# 1. AI Generation & Text Enhancement Endpoints
# =============================================================================

@router.post(
    "/ai-generate",
    response_model=AIGenerateResumeResponse,
    summary="Generate & Enhance Full Resume via Genuine LLM",
    description="Processes raw user input and uses instruction-following LLM to polish summary, responsibilities, and projects while strictly preserving facts.",
)
def ai_generate_resume(payload: AIGenerateResumeRequest):
    try:
        return ResumeAIGeneratorService.generate_full_resume(
            raw_resume=payload.rawResumeData,
            target_role=payload.targetRole,
            instruction=payload.instruction,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"AI Resume Generation inference error: {str(e)}"
        )


@router.post(
    "/enhance-text",
    response_model=AIEnhanceTextResponse,
    summary="Enhance Single Text Snippet via AI",
    description="Polishes a specific summary or bullet point using active verbs and STAR framing without hallucinating facts.",
)
def ai_enhance_text(payload: AIEnhanceTextRequest):
    try:
        return ResumeAIGeneratorService.enhance_single_text(
            text=payload.text,
            section_type=payload.sectionType,
            context_role=payload.contextRole,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Text enhancement inference error: {str(e)}"
        )


@router.post(
    "/recommend-design",
    response_model=RecommendDesignResponse,
    summary="Recommend Optimal Resume Design via Genuine LLM",
    description="Analyzes user's technical skills, experience, education, and projects to select optimal resume design from the 1000+ catalog using local Qwen2.5-1.5B MLX model.",
)
def recommend_resume_design(payload: RecommendDesignRequest):
    try:
        return ResumeAIGeneratorService.recommend_design_with_ai(
            resume_data=payload.resumeData,
            target_role=payload.targetRole,
            candidate_designs=payload.candidateDesignCatalog,
        )
    except Exception as e:
        return ResumeAIGeneratorService.fallback_heuristic_recommendation(
            resume_data=payload.resumeData,
            reason=f"Recommendation error: {str(e)}"
        )


# =============================================================================
# 2. DOCX Export Endpoint
# =============================================================================

@router.post(
    "/export-docx",
    summary="Export Structured Resume to DOCX",
    description="Generates an ATS-compliant, formatted Word (.docx) document matching user data and accent styling.",
)
def export_resume_docx(payload: ResumeFullData):
    try:
        stream = ResumeDocxService.generate_docx(payload)
        candidate_name = payload.personalInfo.fullName or "Candidate"
        safe_name = "".join(c for c in candidate_name if c.isalnum() or c in (" ", "_", "-")).strip().replace(" ", "_")
        filename = f"{safe_name}_Resume.docx"

        return Response(
            content=stream.getvalue(),
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            headers={"Content-Disposition": f"attachment; filename=\"{filename}\""}
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"DOCX Generation failed: {str(e)}"
        )


# =============================================================================
# 3. Resume Persistence Endpoints (Save / Retrieve / List)
# =============================================================================

@router.post(
    "/save",
    response_model=SaveResumeResponse,
    summary="Save Complete Resume Portfolio",
    description="Persists structured resume JSON, creates version snapshot, and stores discrete sections in database.",
)
def save_resume_full(
    payload: SaveResumeRequest,
    request: Request,
    db: Session = Depends(get_db),
):
    current_user = _get_optional_user(request, db)
    
    # If unauthenticated, bind to default primary demo candidate in database
    if not current_user:
        current_user = db.execute(
            select(User).order_by(User.created_at.asc())
        ).scalars().first()
        if not current_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No user context available to associate saved resume."
            )

    resume_doc = None
    if payload.resumeId:
        try:
            r_uuid = uuid.UUID(payload.resumeId)
            resume_doc = db.execute(
                select(ResumeDocument).where(
                    ResumeDocument.id == r_uuid,
                    ResumeDocument.user_id == current_user.id
                )
            ).scalar_one_or_none()
        except Exception:
            resume_doc = None

    if not resume_doc:
        resume_doc = ResumeDocument(
            user_id=current_user.id,
            title=payload.title or f"{payload.resumeData.personalInfo.fullName}'s Resume",
            is_primary=payload.isPrimary,
        )
        db.add(resume_doc)
        db.flush()
    else:
        resume_doc.title = payload.title or resume_doc.title
        resume_doc.is_primary = payload.isPrimary

    # Determine next version number
    last_ver = db.execute(
        select(ResumeVersion)
        .where(ResumeVersion.resume_id == resume_doc.id)
        .order_by(ResumeVersion.version_number.desc())
    ).scalars().first()
    next_ver_num = (last_ver.version_number + 1) if last_ver else 1

    # Store full JSON in raw_content_json
    full_json_str = payload.resumeData.model_dump_json()

    version = ResumeVersion(
        resume_id=resume_doc.id,
        version_number=next_ver_num,
        version_name=f"v{next_ver_num}.0 - {datetime.utcnow().strftime('%Y-%m-%d %H:%M')}",
        raw_content_json=full_json_str,
    )
    db.add(version)
    db.flush()

    # Create discrete sections
    sec_map = [
        ("personal_info", "Personal Information", payload.resumeData.personalInfo.model_dump_json(), 1),
        ("skills", "Technical Skills", payload.resumeData.skills.model_dump_json(), 2),
        ("education", "Education", json.dumps([e.model_dump() for e in payload.resumeData.education]), 3),
        ("experience", "Work Experience", json.dumps([e.model_dump() for e in payload.resumeData.experience]), 4),
        ("projects", "Projects", json.dumps([p.model_dump() for p in payload.resumeData.projects]), 5),
        ("internships", "Internships", json.dumps([i.model_dump() for i in payload.resumeData.internships]), 6),
        ("certifications", "Certifications", json.dumps([c.model_dump() for c in payload.resumeData.certifications]), 7),
        ("additional", "Additional Sections", payload.resumeData.additional.model_dump_json(), 8),
    ]

    for s_type, s_title, s_json, s_order in sec_map:
        db.add(
            ResumeSection(
                version_id=version.id,
                section_type=s_type,
                title=s_title,
                content_json=s_json,
                order_index=s_order,
            )
        )

    db.commit()

    return SaveResumeResponse(
        success=True,
        resumeId=str(resume_doc.id),
        versionId=str(version.id),
        title=resume_doc.title,
        updatedAt=datetime.utcnow().isoformat(),
        message="Resume successfully saved and versioned in database."
    )


@router.post("", response_model=ResumeDocumentResponse, status_code=status.HTTP_201_CREATED)
def create_resume(
    payload: ResumeDocumentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Create a structured trade resume container, optionally populating the initial version."""
    if payload.is_primary:
        existing_primaries = db.execute(
            select(ResumeDocument).where(
                ResumeDocument.user_id == current_user.id,
                ResumeDocument.is_primary == True,
            )
        ).scalars().all()
        for doc in existing_primaries:
            doc.is_primary = False

    resume = ResumeDocument(
        user_id=current_user.id,
        title=payload.title,
        is_primary=payload.is_primary,
    )
    db.add(resume)
    db.flush()

    if payload.initial_version:
        ver = ResumeVersion(
            resume_id=resume.id,
            version_number=1,
            version_name=payload.initial_version.version_name,
            raw_content_json=payload.initial_version.raw_content_json,
        )
        db.add(ver)
        db.flush()

        for sec in payload.initial_version.sections:
            db.add(
                ResumeSection(
                    version_id=ver.id,
                    section_type=sec.section_type,
                    title=sec.title,
                    content_json=sec.content_json,
                    order_index=sec.order_index,
                )
            )

    db.commit()

    resume = db.execute(
        select(ResumeDocument)
        .options(
            joinedload(ResumeDocument.versions).joinedload(ResumeVersion.sections)
        )
        .where(ResumeDocument.id == resume.id)
    ).unique().scalar_one()

    return resume


@router.post("/{resume_id}/versions", response_model=ResumeVersionResponse, status_code=status.HTTP_201_CREATED)
def create_resume_version(
    resume_id: uuid.UUID,
    payload: ResumeVersionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Add a new incremental snapshot version to an existing resume document."""
    resume = db.execute(
        select(ResumeDocument).where(
            ResumeDocument.id == resume_id,
            ResumeDocument.user_id == current_user.id,
        )
    ).scalar_one_or_none()

    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume document not found.",
        )

    last_version = db.execute(
        select(ResumeVersion)
        .where(ResumeVersion.resume_id == resume.id)
        .order_by(ResumeVersion.version_number.desc())
    ).scalars().first()

    next_ver_num = (last_version.version_number + 1) if last_version else 1

    version = ResumeVersion(
        resume_id=resume.id,
        version_number=next_ver_num,
        version_name=payload.version_name,
        raw_content_json=payload.raw_content_json,
    )
    db.add(version)
    db.flush()

    for sec in payload.sections:
        db.add(
            ResumeSection(
                version_id=version.id,
                section_type=sec.section_type,
                title=sec.title,
                content_json=sec.content_json,
                order_index=sec.order_index,
            )
        )

    db.commit()

    version = db.execute(
        select(ResumeVersion)
        .options(joinedload(ResumeVersion.sections))
        .where(ResumeVersion.id == version.id)
    ).unique().scalar_one()

    return version


@router.get("", response_model=List[ResumeDocumentResponse])
def list_resumes(
    request: Request,
    db: Session = Depends(get_db),
):
    """List all resume portfolios owned by the authenticated candidate or guest user."""
    current_user = _get_optional_user(request, db)
    if not current_user:
        current_user = db.execute(select(User).order_by(User.created_at.asc())).scalars().first()

    if not current_user:
        return []

    return db.execute(
        select(ResumeDocument)
        .options(
            joinedload(ResumeDocument.versions).joinedload(ResumeVersion.sections)
        )
        .where(ResumeDocument.user_id == current_user.id)
        .order_by(ResumeDocument.created_at.desc())
    ).unique().scalars().all()


@router.get("/{resume_id}/json", response_model=ResumeFullData)
def get_resume_json(
    resume_id: uuid.UUID,
    request: Request,
    db: Session = Depends(get_db),
):
    """Retrieve full parsed ResumeFullData JSON from the latest version with IDOR protection."""
    current_user = _get_optional_user(request, db)
    resume = db.execute(
        select(ResumeDocument)
        .options(joinedload(ResumeDocument.versions))
        .where(ResumeDocument.id == resume_id)
    ).unique().scalar_one_or_none()

    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume document not found."
        )

    # IDOR ownership enforcement: authenticated users can only access their own documents
    if current_user and resume.user_id and resume.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden: You do not have permission to view this resume portfolio."
        )

    if not resume.versions or not resume.versions[0].raw_content_json:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume has no valid content version."
        )

    latest_ver = sorted(resume.versions, key=lambda v: v.version_number, reverse=True)[0]
    data_dict = json.loads(latest_ver.raw_content_json)
    return ResumeFullData(**data_dict)


@router.get("/{resume_id}", response_model=ResumeDocumentResponse)
def get_resume(
    resume_id: uuid.UUID,
    request: Request,
    db: Session = Depends(get_db),
):
    """Retrieve full resume details with IDOR protection."""
    current_user = _get_optional_user(request, db)
    resume = db.execute(
        select(ResumeDocument)
        .options(
            joinedload(ResumeDocument.versions).joinedload(ResumeVersion.sections)
        )
        .where(ResumeDocument.id == resume_id)
    ).unique().scalar_one_or_none()

    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume document not found.",
        )

    # IDOR ownership enforcement: do not disclose existence to unauthorized users
    if current_user and resume.user_id and resume.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume document not found.",
        )
    return resume


@router.delete("/{resume_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_resume(
    resume_id: uuid.UUID,
    request: Request,
    db: Session = Depends(get_db),
):
    """Delete a resume document portfolio with IDOR protection."""
    current_user = _get_optional_user(request, db)
    stmt = select(ResumeDocument).where(ResumeDocument.id == resume_id)
    if current_user:
        stmt = stmt.where(ResumeDocument.user_id == current_user.id)

    resume = db.execute(stmt).scalar_one_or_none()
    if not resume:
        # Check if resume exists under another user to distinguish 403 from 404
        existing = db.execute(select(ResumeDocument).where(ResumeDocument.id == resume_id)).scalar_one_or_none()
        if existing and current_user and existing.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access forbidden: You cannot delete another candidate's resume portfolio."
            )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume document not found.",
        )

    db.delete(resume)
    db.commit()
    return None


# =====================================================================
# ATS INTELLIGENCE & RESUME UPLOAD ENDPOINTS
# =====================================================================

@router.post("/upload-parse")
async def upload_and_parse_resume(
    file: UploadFile = File(...)
):
    """
    Ingests PDF or DOCX file, applies deterministic text extraction,
    and runs the trained neural section classifier with line-level evidence tracking.
    """
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No filename provided in upload payload."
        )

    ext = file.filename.lower().split(".")[-1]
    if ext not in ["pdf", "docx"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported format '.{ext}'. Please upload a valid .pdf or .docx resume document."
        )

    try:
        content_bytes = await file.read()
        if len(content_bytes) > 15 * 1024 * 1024:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail="Resume file exceeds 15MB limit."
            )

        parsed = ResumeParserService.parse_document(file.filename, content_bytes)
        return parsed
    except ValueError as ve:
        err_msg = str(ve)
        status_code = (
            status.HTTP_400_BAD_REQUEST
            if any(k in err_msg for k in ["Invalid file signature", "Unsupported", "empty", "Password-protected"])
            else status.HTTP_422_UNPROCESSABLE_ENTITY
        )
        raise HTTPException(
            status_code=status_code,
            detail=err_msg
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to parse resume document: {str(e)}"
        )


@router.post("/analyze-jd", response_model=ATSJobDescriptionAnalysisResponse)
def analyze_job_description(
    payload: ATSJobDescriptionAnalysisRequest
):
    """
    Analyzes job description to extract required/preferred skills, qualifications,
    responsibilities, and seniority level with source citations.
    """
    try:
        analysis = ATSMatcherService.analyze_job_description(
            payload.jobDescriptionText,
            payload.jobTitle
        )
        return analysis
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to analyze job description: {str(e)}"
        )


@router.post("/match-ats", response_model=ATSMatchResponse)
def match_resume_ats(
    payload: ATSMatchRequest
):
    """
    Performs cosine semantic matching between resume and job description,
    producing an explainable 100-point score (Part A: 0-60, Part B: 0-40) with evidence citations.
    """
    try:
        jd_analysis = ATSMatcherService.analyze_job_description(
            payload.jobDescription,
            payload.jobTitle
        )
        result = ATSMatcherService.match_resume(
            jd_analysis=jd_analysis,
            resume_data=payload.resumeData,
            parsed_resume=payload.parsedResume,
            raw_jd_text=payload.jobDescription
        )
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to compute ATS match: {str(e)}"
        )


@router.post("/ai-improve", response_model=AIImprovementResponse)
def generate_ai_improvements(
    payload: AIImprovementRequest
):
    """
    Generates grounded STAR bullet improvements and missing evidence interview questions
    using local instruction-following LLM without hallucinating unverified facts.
    """
    try:
        res = ATSImprovementService.generate_improvements(
            resume_data=payload.resumeData,
            job_description=payload.jobDescription,
            gap_requirements=payload.gapRequirements
        )
        return res
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate improvements: {str(e)}"
        )

