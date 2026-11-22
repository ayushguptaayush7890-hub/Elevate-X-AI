"""
API Router for Feature 2 Technical Assessment & Career Intelligence Engine.
Provides role selection, question delivery, sandbox code/SQL execution, adaptive testing,
skill mastery evaluation, gap analysis, and personalized roadmapping.
"""

from datetime import datetime, timezone
from typing import List, Optional, Dict, Any
import uuid
import json
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.core.database import get_db
from app.api.deps import get_current_active_user
from app.models.user import User
from app.models.assessment import TechnicalAssessmentResult
from app.schemas.technical_assessment import (
    RoleSummaryResponse,
    RoleDetailResponse,
    SkillItem,
    TechnicalAssessmentStartRequest,
    TechnicalAssessmentStartResponse,
    TechnicalQuestionMasked,
    TechnicalAssessmentSubmitRequest,
    TechnicalAssessmentResultResponse,
    SkillPerformanceItem,
    SkillGapItem,
    RoadmapMilestoneItem,
    EvaluatedAnswerItem,
    CodeRunRequest,
    CodeRunResponse,
    SQLRunRequest,
    SQLRunResponse,
    AdaptiveStepRequest,
    AdaptiveStepResponse,
    AssessmentSessionProgressRequest,
    AssessmentSessionStateResponse,
)
from app.services.question_service import question_service
from app.services.adaptive_engine import adaptive_engine
from app.services.sandboxes import SQLSandbox, CodeSandbox
from app.services.skill_mastery_service import skill_mastery_service
from app.services.roadmap_service import roadmap_service
from app.services.llm_feedback_service import llm_feedback_service

router = APIRouter()

# In-memory adaptive session state cache (session_id -> dict)
_ACTIVE_SESSIONS: Dict[str, Dict[str, Any]] = {}


@router.get("/roles", response_model=List[RoleSummaryResponse])
def list_technical_roles():
    """List all 9 supported technical career roles with skill counts."""
    roles = question_service.get_roles()
    return [
        RoleSummaryResponse(
            role_id=r["role_id"],
            title=r["title"],
            category=r.get("category", "Technology"),
            description=r.get("description", ""),
            skill_count=len(r.get("skills", [])),
        )
        for r in roles
    ]


@router.get("/roles/{role_id}", response_model=RoleDetailResponse)
def get_technical_role_details(role_id: str):
    """Retrieve full details, skills, and subtopics for a technical career role."""
    role = question_service.get_role_by_id(role_id)
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Technical role '{role_id}' not found.",
        )
    return RoleDetailResponse(
        role_id=role["role_id"],
        title=role["title"],
        category=role.get("category", "Technology"),
        description=role.get("description", ""),
        skills=[
            SkillItem(
                skill_id=s["skill_id"],
                name=s["name"],
                subtopics=s.get("subtopics", []),
            )
            for s in role.get("skills", [])
        ],
    )


@router.post("/start", response_model=TechnicalAssessmentStartResponse)
def start_technical_assessment(
    payload: TechnicalAssessmentStartRequest,
    current_user: User = Depends(get_current_active_user),
):
    """
    Initiate a technical assessment attempt.
    Selects balanced questions matching filters and returns masked questions (no answer keys).
    """
    role = question_service.get_role_by_id(payload.role_id)
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Role '{payload.role_id}' not found.",
        )

    # If adaptive, start at medium difficulty
    initial_diff = "medium" if payload.difficulty == "adaptive" else payload.difficulty
    
    questions = question_service.select_questions(
        role_id=payload.role_id,
        skill_id=payload.skill_id,
        assessment_type=payload.assessment_type,
        difficulty=initial_diff,
        count=payload.question_count,
    )

    if not questions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No questions available matching the specified criteria.",
        )

    session_id = str(uuid.uuid4())
    masked_questions = [
        TechnicalQuestionMasked(**question_service.mask_question_for_client(q))
        for q in questions
    ]

    # Calculate estimated duration (approx 2 mins per question)
    duration_mins = max(10, len(questions) * 2)
    start_dt = datetime.now(timezone.utc)
    expiry_ts = start_dt.timestamp() + (duration_mins * 60)

    # Store active session metadata
    _ACTIVE_SESSIONS[session_id] = {
        "session_id": session_id,
        "user_id": str(current_user.id),
        "role_id": payload.role_id,
        "role_title": role["title"],
        "difficulty_mode": payload.difficulty or "adaptive",
        "theta": 0.0,
        "question_ids": [q["question_id"] for q in questions],
        "masked_questions": [q.model_dump() for q in masked_questions],
        "answered_ids": [],
        "current_index": 0,
        "answers": {},
        "duration_minutes": duration_mins,
        "started_at": start_dt.isoformat(),
        "expiry_timestamp": expiry_ts,
        "is_completed": False,
    }

    return TechnicalAssessmentStartResponse(
        session_id=session_id,
        role_id=payload.role_id,
        role_title=role["title"],
        difficulty_mode=payload.difficulty or "adaptive",
        duration_minutes=duration_mins,
        expiry_timestamp=expiry_ts,
        total_questions=len(masked_questions),
        questions=masked_questions,
    )


@router.get("/sessions/{session_id}", response_model=AssessmentSessionStateResponse)
def get_assessment_session(
    session_id: str,
    current_user: User = Depends(get_current_active_user),
):
    """Retrieve an active assessment session to resume state and timer after reload."""
    session = _ACTIVE_SESSIONS.get(session_id)
    if not session or session["user_id"] != str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment session not found or access denied.",
        )

    if session.get("is_completed", False):
        raise HTTPException(
            status_code=status.HTTP_410_GONE,
            detail="Assessment session has already been completed.",
        )

    now_ts = datetime.now(timezone.utc).timestamp()
    time_left = max(0, int(session["expiry_timestamp"] - now_ts))

    return AssessmentSessionStateResponse(
        session_id=session_id,
        role_id=session["role_id"],
        role_title=session["role_title"],
        difficulty_mode=session["difficulty_mode"],
        questions=[TechnicalQuestionMasked(**mq) for mq in session["masked_questions"]],
        current_index=session.get("current_index", 0),
        answers=session.get("answers", {}),
        time_left_seconds=time_left,
        remaining_seconds=time_left,
        is_expired=time_left <= 0,
        total_questions=len(session["masked_questions"]),
    )


@router.post("/sessions/{session_id}/progress")
def save_assessment_session_progress(
    session_id: str,
    payload: AssessmentSessionProgressRequest,
    current_user: User = Depends(get_current_active_user),
):
    """Persist current question index and candidate answers during an active timed assessment."""
    session = _ACTIVE_SESSIONS.get(session_id)
    if not session or session["user_id"] != str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment session not found.",
        )

    if session.get("is_completed", False):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot update a completed session.",
        )

    session["current_index"] = payload.current_index
    session["answers"].update(payload.answers)
    return {
        "success": True,
        "saved_answers_count": len(session["answers"]),
        "current_index": session["current_index"],
        "answers": session["answers"]
    }


@router.post("/sessions/{session_id}/cancel")
def cancel_assessment_session(
    session_id: str,
    current_user: User = Depends(get_current_active_user),
):
    """Explicitly release assessment lock and discard active test session."""
    session = _ACTIVE_SESSIONS.get(session_id)
    if session and session["user_id"] == str(current_user.id):
        _ACTIVE_SESSIONS.pop(session_id, None)
    return {"success": True, "status": "cancelled", "message": "Assessment session released."}


@router.post("/sandbox/run-code", response_model=CodeRunResponse)
def run_code_sandbox(
    payload: CodeRunRequest,
    current_user: User = Depends(get_current_active_user),
):
    """Run candidate code in a secure sandbox against visible test cases."""
    visible_tests = payload.visible_test_cases or []
    if payload.question_id:
        q = question_service.get_question(payload.question_id)
        if q and not visible_tests:
            visible_tests = q.get("visible_test_cases") or []

    res = CodeSandbox.execute_and_grade(
        language=payload.language,
        candidate_code=payload.code,
        visible_test_cases=visible_tests,
        hidden_test_cases=None,  # Do not run hidden tests in interactive sandbox
        timeout_seconds=4.0,
    )
    return CodeRunResponse(**res)


@router.post("/sandbox/run-sql", response_model=SQLRunResponse)
def run_sql_sandbox(
    payload: SQLRunRequest,
    current_user: User = Depends(get_current_active_user),
):
    """Run candidate SQL query in an isolated, read-only in-memory SQLite sandbox."""
    schema = payload.schema_sql or ""
    sample_db = payload.sample_db_sql or ""

    if payload.question_id:
        q = question_service.get_question(payload.question_id)
        if q:
            schema = schema or q.get("SQL_schema", "")
            sample_db = sample_db or q.get("sample_database", "")

    res = SQLSandbox.execute_and_grade(
        schema_sql=schema,
        sample_db_sql=sample_db,
        candidate_query=payload.candidate_query,
    )
    return SQLRunResponse(
        passed=res["passed"],
        score=res["score"],
        actual_rows=res["actual_rows"],
        error=res["error"],
        execution_time_ms=res["execution_time_ms"],
    )


@router.post("/adaptive-step", response_model=AdaptiveStepResponse)
def evaluate_adaptive_step(
    payload: AdaptiveStepRequest,
    current_user: User = Depends(get_current_active_user),
):
    """
    Interactive single-question evaluation for adaptive assessment mode.
    Updates candidate ability (theta) and selects the next question.
    """
    session = _ACTIVE_SESSIONS.get(payload.session_id)
    if not session or session["user_id"] != str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Active assessment session not found.",
        )

    q = question_service.get_question(payload.question_id)
    if not q:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Question '{payload.question_id}' not found.",
        )

    # Evaluate question
    is_correct = False
    pts = 0.0
    max_pts = float(q.get("marks", 5))
    atype = q.get("assessment_type", "mcq")

    if atype in ("mcq", "scenario"):
        is_correct = (str(payload.answer).strip().upper() == str(q.get("correct_answer")).strip().upper())
        pts = max_pts if is_correct else 0.0
    elif atype == "sql":
        res = SQLSandbox.execute_and_grade(
            q.get("SQL_schema", ""),
            q.get("sample_database", ""),
            str(payload.answer),
            q.get("expected_SQL_result"),
            q.get("reference_solution"),
        )
        is_correct = res["passed"]
        pts = max_pts * res["score"]
    elif atype in ("coding", "debugging"):
        res = CodeSandbox.execute_and_grade(
            q.get("coding_language", "python"),
            str(payload.answer),
            q.get("visible_test_cases", []),
            q.get("hidden_test_cases", []),
        )
        is_correct = res["passed"]
        pts = max_pts * res["score"]
    else:
        is_correct = len(str(payload.answer).strip()) > 50
        pts = max_pts if is_correct else (max_pts * 0.5)

    # Update ability theta via 1PL IRT
    current_theta = session.get("theta", 0.0)
    new_theta = adaptive_engine.update_ability(current_theta, q.get("difficulty", "medium"), is_correct)
    session["theta"] = new_theta
    session["answered_ids"].append(q["question_id"])

    rec_diff = adaptive_engine.get_recommended_difficulty(new_theta)

    # Select next question if any remain
    next_masked = None
    remaining_count = len(session["question_ids"]) - len(session["answered_ids"])
    if remaining_count > 0:
        candidates = question_service.select_questions(
            role_id=session["role_id"],
            difficulty=rec_diff,
            count=1,
            exclude_ids=session["answered_ids"],
        )
        if candidates:
            next_masked = TechnicalQuestionMasked(
                **question_service.mask_question_for_client(candidates[0])
            )

    return AdaptiveStepResponse(
        is_correct=is_correct,
        points_awarded=pts,
        explanation=q.get("answer_explanation", "Response evaluated against standard criteria."),
        current_theta=new_theta,
        recommended_difficulty=rec_diff,
        next_question=next_masked,
        is_completed=(next_masked is None),
    )


@router.post("/submit", response_model=TechnicalAssessmentResultResponse)
def submit_technical_assessment(
    payload: TechnicalAssessmentSubmitRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Submit full technical assessment attempt.
    Executes code/SQL sandboxes, calculates skill mastery, identifies skill gaps,
    generates personalized roadmap, and persists the result.
    """
    role = question_service.get_role_by_id(payload.role_id)
    role_title = role["title"] if role else payload.role_id.replace("_", " ").title()

    evaluated_answers: List[Dict[str, Any]] = []
    total_points = 0.0
    earned_points = 0.0

    current_theta = 0.0
    session_data = _ACTIVE_SESSIONS.pop(payload.session_id, None)
    if session_data:
        current_theta = session_data.get("theta", 0.0)

    # Evaluate each submitted answer
    for sub in payload.answers:
        q = question_service.get_question(sub.question_id)
        if not q:
            continue

        qtype = q.get("assessment_type", "mcq")
        max_pts = float(q.get("marks", 5))
        total_points += max_pts

        is_correct = False
        pts = 0.0
        sandbox_res = None

        if qtype in ("mcq", "scenario"):
            correct_ans = str(q.get("correct_answer", "")).strip().upper()
            user_ans = str(sub.answer).strip().upper()
            is_correct = (user_ans == correct_ans)
            pts = max_pts if is_correct else 0.0

        elif qtype == "sql":
            sandbox_res = SQLSandbox.execute_and_grade(
                schema_sql=q.get("SQL_schema", ""),
                sample_db_sql=q.get("sample_database", ""),
                candidate_query=str(sub.answer),
                expected_result=q.get("expected_SQL_result"),
                reference_sql=q.get("reference_solution"),
            )
            is_correct = sandbox_res["passed"]
            pts = round(max_pts * sandbox_res["score"], 1)

        elif qtype in ("coding", "debugging"):
            sandbox_res = CodeSandbox.execute_and_grade(
                language=sub.language or q.get("coding_language", "python"),
                candidate_code=str(sub.answer),
                visible_test_cases=q.get("visible_test_cases", []),
                hidden_test_cases=q.get("hidden_test_cases", []),
            )
            is_correct = sandbox_res["passed"]
            pts = round(max_pts * sandbox_res["score"], 1)

        elif qtype == "system_design":
            # Rubric-based scoring: minimum length & architectural keywords check
            content = str(sub.answer).strip()
            word_count = len(content.split())
            if word_count >= 80:
                is_correct = True
                pts = max_pts
            elif word_count >= 40:
                is_correct = True
                pts = round(max_pts * 0.7, 1)
            else:
                is_correct = False
                pts = round(max_pts * 0.3, 1)
        else:
            is_correct = bool(sub.answer)
            pts = max_pts if is_correct else 0.0

        earned_points += pts
        current_theta = adaptive_engine.update_ability(
            current_theta, q.get("difficulty", "medium"), is_correct
        )

        # Generate individual feedback
        fb = llm_feedback_service.generate_question_feedback(
            question=q,
            user_answer=sub.answer,
            is_correct=is_correct,
            points_awarded=pts,
            sandbox_result=sandbox_res,
        )

        evaluated_answers.append({
            "question_id": q["question_id"],
            "skill_id": q.get("skill_id", "GEN"),
            "skill_name": q.get("skill_name", "General Engineering"),
            "difficulty": q.get("difficulty", "medium"),
            "assessment_type": qtype,
            "is_correct": is_correct,
            "points_awarded": pts,
            "max_points": max_pts,
            "user_answer": sub.answer,
            "correct_answer": q.get("correct_answer"),
            "explanation": q.get("answer_explanation"),
            "feedback": fb["feedback_summary"],
        })

    # Overall percentage
    overall_score_pct = (
        round((earned_points / max(1.0, total_points)) * 100.0, 1)
        if total_points > 0
        else 0.0
    )
    passed = overall_score_pct >= 65.0  # Technical passing threshold

    # Calculate skill-wise performance and gaps
    role_skills = role.get("skills") if role else None
    skill_performances = skill_mastery_service.calculate_skill_performances(
        evaluated_answers=evaluated_answers,
        role_skills=role_skills,
    )
    skill_gaps = skill_mastery_service.identify_skill_gaps(
        skill_performances=skill_performances,
        target_proficiency_threshold=75.0,
    )

    # Generate personalized career roadmap
    roadmap_data = roadmap_service.generate_roadmap(
        target_role_id=payload.role_id,
        target_role_title=role_title,
        skill_gaps=skill_gaps,
        overall_score=overall_score_pct,
    )
    roadmap_milestones = roadmap_data.get("milestones", [])

    # Synthesize AI summary feedback
    narrative_summary = llm_feedback_service.generate_assessment_summary_feedback(
        role_title=role_title,
        overall_score=overall_score_pct,
        skill_performances=skill_performances,
        gaps=skill_gaps,
    )

    completed_at = datetime.now(timezone.utc)
    result_id = str(uuid.uuid4())

    # Persist to database
    db_result = TechnicalAssessmentResult(
        id=uuid.UUID(result_id),
        user_id=current_user.id,
        session_id=payload.session_id,
        role_id=payload.role_id,
        role_title=role_title,
        overall_score_percentage=overall_score_pct,
        points_awarded=earned_points,
        total_points=total_points,
        passed=passed,
        difficulty_mode="adaptive",
        ability_theta=current_theta,
        skill_performances=json.dumps(skill_performances),
        skill_gaps=json.dumps(skill_gaps),
        roadmap_milestones=json.dumps(roadmap_milestones),
        narrative_summary=json.dumps(narrative_summary),
        evaluated_answers=json.dumps(evaluated_answers),
        completed_at=completed_at,
    )
    db.add(db_result)
    db.commit()

    return TechnicalAssessmentResultResponse(
        result_id=result_id,
        session_id=payload.session_id,
        user_id=str(current_user.id),
        role_id=payload.role_id,
        role_title=role_title,
        overall_score_percentage=overall_score_pct,
        points_awarded=earned_points,
        total_points=total_points,
        passed=passed,
        status="completed",
        completed_at=completed_at,
        difficulty_mode="adaptive",
        ability_theta=current_theta,
        skill_performances=[SkillPerformanceItem(**sp) for sp in skill_performances],
        skill_gaps=[SkillGapItem(**sg) for sg in skill_gaps],
        roadmap_milestones=[RoadmapMilestoneItem(**rm) for rm in roadmap_milestones],
        narrative_summary=narrative_summary,
        evaluated_answers=[EvaluatedAnswerItem(**ea) for ea in evaluated_answers],
    )


@router.get("/history", response_model=List[TechnicalAssessmentResultResponse])
def get_user_technical_assessment_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Retrieve all historical technical assessments for the authenticated candidate."""
    results = db.execute(
        select(TechnicalAssessmentResult)
        .where(TechnicalAssessmentResult.user_id == current_user.id)
        .order_by(TechnicalAssessmentResult.completed_at.desc())
    ).scalars().all()

    response_items = []
    for r in results:
        sp = json.loads(r.skill_performances) if r.skill_performances else []
        sg = json.loads(r.skill_gaps) if r.skill_gaps else []
        rm = json.loads(r.roadmap_milestones) if r.roadmap_milestones else []
        ns = json.loads(r.narrative_summary) if r.narrative_summary else {}
        ea = json.loads(r.evaluated_answers) if r.evaluated_answers else []

        response_items.append(
            TechnicalAssessmentResultResponse(
                result_id=str(r.id),
                session_id=r.session_id,
                user_id=str(r.user_id),
                role_id=r.role_id,
                role_title=r.role_title,
                overall_score_percentage=r.overall_score_percentage,
                points_awarded=r.points_awarded,
                total_points=r.total_points,
                passed=r.passed,
                status="completed",
                completed_at=r.completed_at,
                difficulty_mode=r.difficulty_mode,
                ability_theta=r.ability_theta,
                skill_performances=[SkillPerformanceItem(**item) for item in sp],
                skill_gaps=[SkillGapItem(**item) for item in sg],
                roadmap_milestones=[RoadmapMilestoneItem(**item) for item in rm],
                narrative_summary=ns,
                evaluated_answers=[EvaluatedAnswerItem(**item) for item in ea],
            )
        )
    return response_items


@router.get("/results/{result_id}", response_model=TechnicalAssessmentResultResponse)
def get_technical_assessment_result(
    result_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Retrieve detailed assessment result, skill gaps, and learning roadmap by result ID."""
    r = db.execute(
        select(TechnicalAssessmentResult).where(
            TechnicalAssessmentResult.id == result_id,
            TechnicalAssessmentResult.user_id == current_user.id,
        )
    ).scalar_one_or_none()

    if not r:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Technical assessment result not found or access denied.",
        )

    sp = json.loads(r.skill_performances) if r.skill_performances else []
    sg = json.loads(r.skill_gaps) if r.skill_gaps else []
    rm = json.loads(r.roadmap_milestones) if r.roadmap_milestones else []
    ns = json.loads(r.narrative_summary) if r.narrative_summary else {}
    ea = json.loads(r.evaluated_answers) if r.evaluated_answers else []

    return TechnicalAssessmentResultResponse(
        result_id=str(r.id),
        session_id=r.session_id,
        user_id=str(r.user_id),
        role_id=r.role_id,
        role_title=r.role_title,
        overall_score_percentage=r.overall_score_percentage,
        points_awarded=r.points_awarded,
        total_points=r.total_points,
        passed=r.passed,
        status="completed",
        completed_at=r.completed_at,
        difficulty_mode=r.difficulty_mode,
        ability_theta=r.ability_theta,
        skill_performances=[SkillPerformanceItem(**item) for item in sp],
        skill_gaps=[SkillGapItem(**item) for item in sg],
        roadmap_milestones=[RoadmapMilestoneItem(**item) for item in rm],
        narrative_summary=ns,
        evaluated_answers=[EvaluatedAnswerItem(**item) for item in ea],
    )

