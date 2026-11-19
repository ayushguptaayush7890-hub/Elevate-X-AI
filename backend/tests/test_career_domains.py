"""
Integration & Unit Test Suite for Elevate X AI Phase 3 Career Intelligence Domains.
Covers RBAC, User Isolation, Scoring Logic, Progress Calculation, and CRUD Operations across:
- Occupations & NSQF Mapping
- Employers & Job Opportunities
- Skill Assessments & Objective Evaluation
- Skill Gap Delta Reporting
- Roadmaps & Progress Calculation
- Career Transition Corridors
- Structured Resumes & Versions
- Interview Practice Sessions
- Job Applications & Saved Jobs
- Curated Learning Resources
"""

import uuid
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.user import User


def _register_user(client: TestClient, email: str, name: str) -> tuple[dict, str]:
    """Helper to register a user and return auth headers and user ID."""
    res = client.post(
        "/api/v1/auth/register",
        json={"email": email, "password": "Password123!", "full_name": name},
    )
    assert res.status_code == 201
    data = res.json()
    token = data["token"]["access_token"]
    user_id = data["user"]["id"]
    return {"Authorization": f"Bearer {token}"}, user_id


def _make_admin(db: Session, user_id: str):
    """Elevate user to admin role in database."""
    u = db.execute(select(User).where(User.id == uuid.UUID(user_id))).scalar_one()
    u.role = "admin"
    db.commit()


# =============================================================================
# 1. Occupations & NSQF Catalog Tests
# =============================================================================

def test_occupation_admin_rbac_and_crud(client: TestClient, db_session: Session):
    """Test RBAC enforcement and CRUD for global occupations catalog."""
    user_headers, user_id = _register_user(client, "candidate.occ@example.com", "Ramesh Kumar")
    admin_headers, admin_id = _register_user(client, "admin.occ@example.com", "Admin Officer")
    _make_admin(db_session, admin_id)

    # 1. Non-admin cannot create occupation (403 Forbidden)
    occ_payload = {
        "title": "Industrial CNC Lathe Operator",
        "category": "Precision Machining",
        "code": "CNC-001",
        "recommended_experience_years": 2,
        "nsqf_level": 5,
        "description": "Programming and operating CNC turning centers for aerospace components.",
    }
    forbidden_res = client.post("/api/v1/occupations", json=occ_payload, headers=user_headers)
    assert forbidden_res.status_code == 403

    # 2. Admin creates occupation successfully
    create_res = client.post("/api/v1/occupations", json=occ_payload, headers=admin_headers)
    assert create_res.status_code == 201
    occ_id = create_res.json()["id"]

    # 3. Any active user can search and view occupations
    list_res = client.get("/api/v1/occupations?category=Precision Machining", headers=user_headers)
    assert list_res.status_code == 200
    assert any(o["id"] == occ_id for o in list_res.json())

    # 4. Get by ID
    get_res = client.get(f"/api/v1/occupations/{occ_id}", headers=user_headers)
    assert get_res.status_code == 200
    assert get_res.json()["nsqf_level"] == 5


# =============================================================================
# 2. Job Listings & Employers Tests
# =============================================================================

def test_jobs_and_employers_management(client: TestClient, db_session: Session):
    """Test employer registration and job opportunity lifecycle."""
    user_headers, _ = _register_user(client, "worker.job@example.com", "Sunil Verma")
    admin_headers, admin_id = _register_user(client, "admin.job@example.com", "Admin Employer")
    _make_admin(db_session, admin_id)

    # Admin creates employer
    emp_res = client.post(
        "/api/v1/jobs/employers",
        json={
            "name": "Tata Advanced Systems",
            "website": "https://tataadvancedsystems.com",
            "location": "Bengaluru, India",
            "is_verified": True,
        },
        headers=admin_headers,
    )
    assert emp_res.status_code == 201
    employer_id = emp_res.json()["id"]

    # Admin posts job
    job_payload = {
        "employer_id": employer_id,
        "title": "Senior Aerospace Machinist",
        "location": "Bengaluru",
        "description": "High precision machining of turbine discs and titanium alloys.",
        "salary_min": 45000,
        "salary_max": 65000,
        "salary_currency": "INR",
        "employment_type": "Full-time",
        "experience_required_years": 3,
        "requirements": [
            {"requirement_text": "Must understand engineering GD&T drawings", "is_mandatory": True}
        ],
        "skills": [],
    }
    job_res = client.post("/api/v1/jobs", json=job_payload, headers=admin_headers)
    assert job_res.status_code == 201
    job_id = job_res.json()["id"]

    # Candidate lists and filters jobs
    search_res = client.get("/api/v1/jobs?location=Bengaluru&min_salary=40000", headers=user_headers)
    assert search_res.status_code == 200
    assert any(j["id"] == job_id for j in search_res.json())


# =============================================================================
# 3. Assessment & Objective Verification Scoring Tests
# =============================================================================

def test_assessment_start_submit_and_verification(client: TestClient, db_session: Session):
    """Test assessment attempt, objective scoring, and profile skill verification."""
    candidate_headers, _ = _register_user(client, "mechanic@example.com", "Rajesh Patel")
    admin_headers, admin_id = _register_user(client, "admin.assess@example.com", "Admin Assessor")
    _make_admin(db_session, admin_id)

    # 1. Create a skill in the master catalog
    skill_res = client.post(
        "/api/v1/skills",
        json={"name": "Diagnostic Multimeter Calibration", "category": "Electrical & Electronics"},
    )
    skill_id = skill_res.json()["id"]

    # 2. Admin creates assessment with questions and options
    assess_payload = {
        "title": "Digital Multimeter Diagnostic Evaluation",
        "skill_id": skill_id,
        "difficulty_level": "intermediate",
        "duration_minutes": 15,
        "passing_score_percentage": 50.0,
        "questions": [
            {
                "question_text": "What setting should be used to measure harness continuity?",
                "points": 2,
                "order_index": 1,
                "options": [
                    {"option_text": "Resistance / Ohms (Buzzer)", "is_correct": True},
                    {"option_text": "Direct Current Amperes (10A)", "is_correct": False},
                ],
            },
            {
                "question_text": "What is the typical battery open circuit voltage for a fully charged lead-acid battery?",
                "points": 2,
                "order_index": 2,
                "options": [
                    {"option_text": "12.6V to 12.8V", "is_correct": True},
                    {"option_text": "9.5V", "is_correct": False},
                ],
            },
        ],
    }
    create_assess_res = client.post("/api/v1/assessments", json=assess_payload, headers=admin_headers)
    assert create_assess_res.status_code == 201
    assessment_id = create_assess_res.json()["id"]

    # 3. Candidate starts assessment attempt
    start_res = client.post(f"/api/v1/assessments/{assessment_id}/start", headers=candidate_headers)
    assert start_res.status_code == 200
    start_data = start_res.json()
    attempt_id = start_data["attempt_id"]
    questions = start_data["questions"]
    assert len(questions) == 2

    # Verify is_correct was NOT leaked to the candidate
    for q in questions:
        for opt in q["options"]:
            assert "is_correct" not in opt

    # 4. Candidate submits correct answers
    q1 = questions[0]
    q2 = questions[1]
    # Pick first option for each
    submit_payload = {
        "answers": [
            {"question_id": q1["id"], "selected_option_id": q1["options"][0]["id"]},
            {"question_id": q2["id"], "selected_option_id": q2["options"][0]["id"]},
        ]
    }
    submit_res = client.post(
        f"/api/v1/assessments/attempts/{attempt_id}/submit",
        json=submit_payload,
        headers=candidate_headers,
    )
    assert submit_res.status_code == 200
    scorecard = submit_res.json()
    assert scorecard["passed"] is True
    assert scorecard["score_percentage"] == 100.0

    # 5. Verify skill was marked as verified in candidate profile
    profile_skills_res = client.get("/api/v1/profiles/me/skills", headers=candidate_headers)
    assert profile_skills_res.status_code == 200
    verified_skills = [
        s for s in profile_skills_res.json()
        if s["skill_id"] == skill_id and s["verification_status"] == "verified"
    ]
    assert len(verified_skills) == 1

    # 6. Check history
    hist_res = client.get("/api/v1/assessments/history", headers=candidate_headers)
    assert hist_res.status_code == 200
    assert any(h["attempt_id"] == attempt_id for h in hist_res.json())


# =============================================================================
# 4. Skill Gap Analysis Tests
# =============================================================================

def test_skill_gap_report_generation(client: TestClient, db_session: Session):
    """Test generating a skill gap report comparing user competencies with target occupation."""
    candidate_headers, _ = _register_user(client, "gap.user@example.com", "Kiran Devi")
    admin_headers, admin_id = _register_user(client, "admin.gap@example.com", "Admin Gap")
    _make_admin(db_session, admin_id)

    # Create skills
    s1 = client.post("/api/v1/skills", json={"name": "Lockstitch Operation", "category": "Sewing"}).json()["id"]
    s2 = client.post("/api/v1/skills", json={"name": "Garment Quality Inspection", "category": "QA"}).json()["id"]

    # Candidate self-reports skill 1
    client.post(
        "/api/v1/profiles/me/skills",
        json={"skill_id": s1, "proficiency_level": "intermediate"},
        headers=candidate_headers,
    )

    # Create occupation requiring s1 and s2
    occ = client.post(
        "/api/v1/occupations",
        json={
            "title": "Garment Export Quality Checker",
            "category": "Apparel",
            "required_skills": [
                {"skill_id": s1, "is_required": True, "importance_weight": 1.0},
                {"skill_id": s2, "is_required": True, "importance_weight": 1.0},
            ],
        },
        headers=admin_headers,
    ).json()

    # Generate gap report
    gap_res = client.post(
        "/api/v1/skill-gaps",
        json={"target_occupation_id": occ["id"]},
        headers=candidate_headers,
    )
    assert gap_res.status_code == 201
    report = gap_res.json()
    assert report["overall_match_percentage"] == 50.0  # 1 of 2 skills matched
    assert len(report["items"]) == 2

    # Check gap priorities
    missing_items = [it for it in report["items"] if it["gap_severity"] == "missing"]
    assert len(missing_items) == 1
    assert missing_items[0]["skill_id"] == s2


# =============================================================================
# 5. Career Roadmap & Task Progress Recalculation Tests
# =============================================================================

def test_roadmap_task_toggle_and_progress(client: TestClient, db_session: Session):
    """Test roadmap creation, task completion toggle, and progress percentage math."""
    user_headers, _ = _register_user(client, "roadmap.user@example.com", "Vikram Singh")

    roadmap_payload = {
        "title": "Apparel Quality Specialist Transition",
        "target_role": "Apparel QA Specialist",
        "estimated_duration_weeks": 6,
        "milestones": [
            {
                "title": "Phase 1: Fabric Inspection Fundamentals",
                "order_index": 1,
                "tasks": [
                    {"title": "Study 4-point fabric defect grading", "estimated_hours": 3.0},
                    {"title": "Practice seam strength tension check", "estimated_hours": 2.0},
                ],
            }
        ],
    }
    create_res = client.post("/api/v1/roadmaps", json=roadmap_payload, headers=user_headers)
    assert create_res.status_code == 201
    roadmap = create_res.json()
    assert roadmap["progress_percentage"] == 0.0
    task1 = roadmap["milestones"][0]["tasks"][0]

    # Toggle task 1
    toggle_res = client.patch(f"/api/v1/roadmaps/tasks/{task1['id']}/toggle", headers=user_headers)
    assert toggle_res.status_code == 200
    assert toggle_res.json()["is_completed"] is True

    # Check updated roadmap progress (1 of 2 tasks = 50.0%)
    get_res = client.get(f"/api/v1/roadmaps/{roadmap['id']}", headers=user_headers)
    assert get_res.status_code == 200
    assert get_res.json()["progress_percentage"] == 50.0


# =============================================================================
# 6. Structured Resume & Snapshots Tests
# =============================================================================

def test_resume_document_and_versioning(client: TestClient, db_session: Session):
    """Test candidate resume container, versions, and discrete sections."""
    user1_headers, _ = _register_user(client, "resume.user1@example.com", "Pooja Hegde")
    user2_headers, _ = _register_user(client, "resume.user2@example.com", "Other Candidate")

    resume_payload = {
        "title": "Master Tailor & Garment Tech Resume",
        "is_primary": True,
        "initial_version": {
            "version_name": "v1.0 - Initial Draft",
            "sections": [
                {
                    "section_type": "summary",
                    "title": "Professional Summary",
                    "content_json": '{"text": "8+ years in industrial sewing and pattern drafting."}',
                    "order_index": 1,
                }
            ],
        },
    }
    res = client.post("/api/v1/resumes", json=resume_payload, headers=user1_headers)
    assert res.status_code == 201
    resume_id = res.json()["id"]

    # User isolation: user2 cannot access user1's resume
    isolated_res = client.get(f"/api/v1/resumes/{resume_id}", headers=user2_headers)
    assert isolated_res.status_code == 404

    # Add new snapshot version
    new_version_payload = {
        "version_name": "v2.0 - Certified QA Profile",
        "sections": [
            {
                "section_type": "certification",
                "title": "Trade Certifications",
                "content_json": '{"certs": ["NSQF Level 5 Sewing", "ISO 9001 QA"]}',
                "order_index": 2,
            }
        ],
    }
    ver_res = client.post(
        f"/api/v1/resumes/{resume_id}/versions",
        json=new_version_payload,
        headers=user1_headers,
    )
    assert ver_res.status_code == 201
    assert ver_res.json()["version_number"] == 2


# =============================================================================
# 7. Job Application Tracking & Saved Jobs Tests
# =============================================================================

def test_application_lifecycle_and_saved_jobs(client: TestClient, db_session: Session):
    """Test job saving, application lifecycle stages, duplicate rejection, and notes."""
    candidate_headers, _ = _register_user(client, "applicant@example.com", "Farhan Akhtar")
    admin_headers, admin_id = _register_user(client, "admin.app@example.com", "Admin Recruiter")
    _make_admin(db_session, admin_id)

    # Employer and Job
    emp = client.post(
        "/api/v1/jobs/employers",
        json={"name": "Raymond Exports Ltd", "location": "Thane, Maharashtra"},
        headers=admin_headers,
    ).json()

    job = client.post(
        "/api/v1/jobs",
        json={
            "employer_id": emp["id"],
            "title": "Industrial Cutting Master",
            "location": "Thane",
            "description": "Lead cutting floor team for precision pattern markers.",
        },
        headers=admin_headers,
    ).json()

    job_id = job["id"]

    # 1. Bookmark / Save Job
    save_res = client.post(f"/api/v1/saved-jobs/{job_id}", headers=candidate_headers)
    assert save_res.status_code == 201
    saved_list = client.get("/api/v1/saved-jobs", headers=candidate_headers)
    assert any(s["job_id"] == job_id for s in saved_list.json())

    # 2. Apply to job
    app_res = client.post(
        "/api/v1/applications",
        json={"job_id": job_id, "cover_note": "Ready for trade test."},
        headers=candidate_headers,
    )
    assert app_res.status_code == 201
    app_id = app_res.json()["id"]

    # 3. Duplicate application should fail
    dup_res = client.post(
        "/api/v1/applications",
        json={"job_id": job_id},
        headers=candidate_headers,
    )
    assert dup_res.status_code == 400

    # 4. Progress status to 'interview'
    status_res = client.put(
        f"/api/v1/applications/{app_id}/status",
        json={"status": "interview"},
        headers=candidate_headers,
    )
    assert status_res.status_code == 200
    assert status_res.json()["status"] == "interview"

    # 5. Add interview note
    note_res = client.post(
        f"/api/v1/applications/{app_id}/notes",
        json={"note_text": "Practical round scheduled on Thursday 10 AM."},
        headers=candidate_headers,
    )
    assert note_res.status_code == 201
    assert note_res.json()["note_text"] == "Practical round scheduled on Thursday 10 AM."

    # 6. Unsave job
    unsave_res = client.delete(f"/api/v1/saved-jobs/{job_id}", headers=candidate_headers)
    assert unsave_res.status_code == 204


# =============================================================================
# 8. Learning Resources Catalog Tests
# =============================================================================

def test_learning_resources_catalog(client: TestClient, db_session: Session):
    """Test training partner registration and course catalog queries."""
    user_headers, _ = _register_user(client, "student@example.com", "Sanjay Dutt")
    admin_headers, admin_id = _register_user(client, "admin.edu@example.com", "Admin Educator")
    _make_admin(db_session, admin_id)

    # Provider
    prov = client.post(
        "/api/v1/resources/providers",
        json={"name": "National Skill Development Corporation (NSDC)", "website": "https://nsdcindia.org"},
        headers=admin_headers,
    ).json()

    # Learning resource
    res_payload = {
        "title": "Industrial Sewing Machine Operator Certificate",
        "provider_id": prov["id"],
        "description": "Comprehensive practical module for garment factory floor readiness.",
        "url": "https://nsdcindia.org/courses/apparel-sewing",
        "language": "Hindi",
        "cost_type": "free",
        "duration_hours": 30.0,
    }
    course_res = client.post("/api/v1/resources", json=res_payload, headers=admin_headers)
    assert course_res.status_code == 201
    course_id = course_res.json()["id"]

    # Filter by language
    query_res = client.get("/api/v1/resources?language=Hindi", headers=user_headers)
    assert query_res.status_code == 200
    assert any(c["id"] == course_id for c in query_res.json())


# =============================================================================
# 9. Career Transition Pathways Tests
# =============================================================================

def test_career_transitions_flow(client: TestClient, db_session: Session):
    """Test creating and browsing transition pathways between trade sectors."""
    user_headers, _ = _register_user(client, "transition.user@example.com", "Ananya Roy")
    admin_headers, admin_id = _register_user(client, "admin.trans@example.com", "Admin Pathways")
    _make_admin(db_session, admin_id)

    # 1. Create two occupations
    occ1 = client.post(
        "/api/v1/occupations",
        json={"title": "Custom Tailor & Draper", "category": "Textile Crafts"},
        headers=admin_headers,
    ).json()

    occ2 = client.post(
        "/api/v1/occupations",
        json={"title": "Apparel Quality Assurance Lead", "category": "Industrial Manufacturing"},
        headers=admin_headers,
    ).json()

    # Create transferable skill
    skill = client.post(
        "/api/v1/skills",
        json={"name": "Garment Fault Detection", "category": "Quality Control"},
    ).json()

    # 2. Admin creates transition corridor
    trans_payload = {
        "from_occupation_id": occ1["id"],
        "to_occupation_id": occ2["id"],
        "transition_title": "Artisanal Tailor to Industrial QA Inspector",
        "feasibility_score": 88.5,
        "estimated_transition_months": 3,
        "description": "Leverages tactile fabric feel and stitching expertise into automated production QA.",
        "skills_mapping": [
            {
                "skill_id": skill["id"],
                "transferability_level": "direct",
                "notes": "Directly applicable to defect classification.",
            }
        ],
        "requirements": [
            {
                "title": "AQL 2.5 Sampling Bridge Certification",
                "requirement_type": "bridge_training",
                "description": "Learn statistical batch sampling methods.",
            }
        ],
    }
    create_res = client.post("/api/v1/career-transitions", json=trans_payload, headers=admin_headers)
    assert create_res.status_code == 201
    trans_id = create_res.json()["id"]

    # 3. User lists transition pathways
    list_res = client.get(f"/api/v1/career-transitions?from_occupation_id={occ1['id']}", headers=user_headers)
    assert list_res.status_code == 200
    assert any(t["id"] == trans_id for t in list_res.json())

    # 4. User retrieves transition detail
    detail_res = client.get(f"/api/v1/career-transitions/{trans_id}", headers=user_headers)
    assert detail_res.status_code == 200
    detail = detail_res.json()
    assert detail["feasibility_score"] == 88.5
    assert len(detail["skills_mapping"]) == 1
    assert len(detail["requirements"]) == 1


# =============================================================================
# 10. Interview Diagnostic Practice & Feedback Tests
# =============================================================================

def test_interview_sessions_and_feedback(client: TestClient, db_session: Session):
    """Test mock technical diagnostic interview workflow and candidate feedback scoring."""
    user_headers, _ = _register_user(client, "interviewee@example.com", "Devendra Jhajharia")

    # 1. Initialize interview session
    session_payload = {
        "target_role": "Industrial Solar Panel Technician",
        "trade_category": "Renewable Energy",
        "session_type": "technical_diagnostic",
        "questions": [
            {
                "question_text": "How do you test a bypass diode inside an open-circuit PV junction box?",
                "expected_competency": "PV Component Diagnostics",
                "order_index": 1,
            }
        ],
    }
    create_res = client.post("/api/v1/interviews/sessions", json=session_payload, headers=user_headers)
    assert create_res.status_code == 201
    session_data = create_res.json()
    session_id = session_data["id"]
    question_id = session_data["questions"][0]["id"]

    # 2. Candidate submits answer
    answer_res = client.post(
        f"/api/v1/interviews/sessions/{session_id}/answers",
        json={
            "question_id": question_id,
            "user_response_text": "Disconnect string, set DMM to diode test mode, verify forward voltage ~0.6V and reverse open.",
            "time_taken_seconds": 45,
        },
        headers=user_headers,
    )
    assert answer_res.status_code == 201
    assert answer_res.json()["user_response_text"] is not None

    # 3. Complete session and submit feedback
    feedback_payload = {
        "technical_accuracy_score": 92.0,
        "clarity_score": 88.0,
        "feedback_summary": "Strong diagnostic methodology and safety protocol adherence.",
        "areas_of_improvement": "Mention string isolation breaker precautions first.",
    }
    feed_res = client.post(
        f"/api/v1/interviews/sessions/{session_id}/feedback",
        json=feedback_payload,
        headers=user_headers,
    )
    assert feed_res.status_code == 201
    feed_data = feed_res.json()
    assert feed_data["technical_accuracy_score"] == 92.0

    # 4. Check completed session
    get_res = client.get(f"/api/v1/interviews/sessions/{session_id}", headers=user_headers)
    assert get_res.status_code == 200
    assert get_res.json()["status"] == "completed"
    assert get_res.json()["feedback"] is not None
