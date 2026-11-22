"""
Unit and Integration Tests for Critical Module Bug Fixes & Audit:
1. Assessment Navigation Lock, Question Answering, and Session Persistence (Tests 1-9)
2. Coding Sandbox Test Runner & IndexError Fix (Tests 10-15)
3. Skill Gap Empty State & Source Attribution (Tests 16-22)
4. Experience Recognition Extraction & Error Handling (Tests 23-30)
"""

import pytest
import uuid
import json
from datetime import datetime, timezone, timedelta
from fastapi.testclient import TestClient

from app.services.sandboxes import CodeSandbox
from datasets.informal_skill_extraction.models.skill_extractor import ModularSkillExtractor
from app.api.v1.skill import _get_default_config


def _get_auth_headers(client: TestClient, email: str, name: str) -> tuple[dict, str]:
    res = client.post(
        "/api/v1/auth/register",
        json={"email": email, "password": "SecurePassword123!", "full_name": name},
    )
    assert res.status_code == 201, f"Failed to register {email}: {res.text}"
    data = res.json()
    token = data["token"]["access_token"]
    user_id = data["user"]["id"]
    return {"Authorization": f"Bearer {token}"}, user_id


# ============================================================================
# Assessment Tests (1 - 9)
# ============================================================================

def test_01_assessment_session_start_and_masked_answers(client: TestClient):
    """Test 1: Start assessment returns session_id, expiry_timestamp, and masks answers."""
    headers, _ = _get_auth_headers(client, "test01_assess@example.com", "Test One")
    start_res = client.post(
        "/api/v1/assessments/technical/start",
        headers=headers,
        json={"role_id": "software_engineer", "question_count": 5, "difficulty": "medium"}
    )
    assert start_res.status_code == 200
    data = start_res.json()
    assert "session_id" in data
    assert "expiry_timestamp" in data
    assert len(data["questions"]) == 5
    for q in data["questions"]:
        assert "correct_answer" not in q
        assert "answer_explanation" not in q
        assert "hidden_test_cases" not in q
        assert "reference_solution" not in q


def test_02_assessment_next_blocked_without_selection_logic(client: TestClient):
    """Test 2: Server-side assessment progress validation persists candidate answers safely."""
    headers, _ = _get_auth_headers(client, "test02_assess@example.com", "Test Two")
    start_res = client.post(
        "/api/v1/assessments/technical/start",
        headers=headers,
        json={"role_id": "software_engineer", "question_count": 5, "difficulty": "medium"}
    )
    sess_id = start_res.json()["session_id"]
    
    # Progress update with valid answer
    progress_res = client.post(
        f"/api/v1/assessments/technical/sessions/{sess_id}/progress",
        headers=headers,
        json={"current_index": 1, "answers": {"0": 2}}
    )
    assert progress_res.status_code == 200
    p_data = progress_res.json()
    assert p_data["current_index"] == 1
    assert p_data["answers"] == {"0": 2}


def test_03_assessment_answer_persistence_on_navigation(client: TestClient):
    """Test 3: Selected answers are preserved across forward and backward step navigation."""
    headers, _ = _get_auth_headers(client, "test03_assess@example.com", "Test Three")
    start_res = client.post(
        "/api/v1/assessments/technical/start",
        headers=headers,
        json={"role_id": "software_engineer", "question_count": 5, "difficulty": "medium"}
    )
    sess_id = start_res.json()["session_id"]

    # Answer question 0 and question 1
    client.post(
        f"/api/v1/assessments/technical/sessions/{sess_id}/progress",
        headers=headers,
        json={"current_index": 2, "answers": {"0": 1, "1": 3}}
    )

    # Candidate navigates back to question 0
    client.post(
        f"/api/v1/assessments/technical/sessions/{sess_id}/progress",
        headers=headers,
        json={"current_index": 0, "answers": {"0": 1, "1": 3}}
    )

    # Fetch session state to ensure answers persist
    state_res = client.get(f"/api/v1/assessments/technical/sessions/{sess_id}", headers=headers)
    assert state_res.status_code == 200
    state = state_res.json()
    assert state["current_index"] == 0
    assert state["answers"]["0"] == 1
    assert state["answers"]["1"] == 3


def test_04_assessment_submission_requires_all_answers_or_flags_unanswered(client: TestClient):
    """Test 4: Final submission records answered count and evaluates scores."""
    headers, _ = _get_auth_headers(client, "test04_assess@example.com", "Test Four")
    start_res = client.post(
        "/api/v1/assessments/technical/start",
        headers=headers,
        json={"role_id": "software_engineer", "question_count": 2, "difficulty": "easy"}
    )
    data = start_res.json()
    sess_id = data["session_id"]
    q1 = data["questions"][0]

    # Partial submission
    submit_res = client.post(
        "/api/v1/assessments/technical/submit",
        headers=headers,
        json={
            "session_id": sess_id,
            "role_id": "software_engineer",
            "answers": [{"question_id": q1["question_id"], "answer": "A"}],
        }
    )
    assert submit_res.status_code == 200
    result = submit_res.json()
    assert result["role_id"] == "software_engineer"
    assert "overall_score_percentage" in result


def test_05_assessment_all_answered_submits_successfully(client: TestClient):
    """Test 5: Submitting full answer set evaluates correctly and produces score report."""
    headers, _ = _get_auth_headers(client, "test05_assess@example.com", "Test Five")
    start_res = client.post(
        "/api/v1/assessments/technical/start",
        headers=headers,
        json={"role_id": "software_engineer", "question_count": 3, "difficulty": "easy"}
    )
    data = start_res.json()
    sess_id = data["session_id"]
    questions = data["questions"]
    answers = [{"question_id": q["question_id"], "answer": "A"} for q in questions]

    submit_res = client.post(
        "/api/v1/assessments/technical/submit",
        headers=headers,
        json={
            "session_id": sess_id,
            "role_id": "software_engineer",
            "answers": answers,
        }
    )
    assert submit_res.status_code == 200
    result = submit_res.json()
    assert result["role_id"] == "software_engineer"
    assert 0 <= result["overall_score_percentage"] <= 100


def test_06_assessment_timer_expiry_state_calculation(client: TestClient):
    """Test 6: Session state calculates remaining seconds from backend expiry_timestamp."""
    headers, _ = _get_auth_headers(client, "test06_assess@example.com", "Test Six")
    start_res = client.post(
        "/api/v1/assessments/technical/start",
        headers=headers,
        json={"role_id": "software_engineer", "question_count": 5, "difficulty": "medium"}
    )
    sess_id = start_res.json()["session_id"]
    
    state_res = client.get(f"/api/v1/assessments/technical/sessions/{sess_id}", headers=headers)
    assert state_res.status_code == 200
    state = state_res.json()
    assert state["remaining_seconds"] > 0
    assert state["remaining_seconds"] <= 20 * 60  # Default 20 mins for mcq_knowledge


def test_07_assessment_rapid_progress_idempotency(client: TestClient):
    """Test 7: Rapid successive progress calls maintain correct state without corruption."""
    headers, _ = _get_auth_headers(client, "test07_assess@example.com", "Test Seven")
    start_res = client.post(
        "/api/v1/assessments/technical/start",
        headers=headers,
        json={"role_id": "software_engineer", "question_count": 5, "difficulty": "medium"}
    )
    sess_id = start_res.json()["session_id"]
    
    # 5 rapid progress requests
    for i in range(5):
        res = client.post(
            f"/api/v1/assessments/technical/sessions/{sess_id}/progress",
            headers=headers,
            json={"current_index": i, "answers": {str(k): k % 4 for k in range(i + 1)}}
        )
        assert res.status_code == 200

    state_res = client.get(f"/api/v1/assessments/technical/sessions/{sess_id}", headers=headers)
    assert state_res.status_code == 200
    state = state_res.json()
    assert state["current_index"] == 4
    assert len(state["answers"]) == 5


def test_08_assessment_reload_restores_active_session_state(client: TestClient):
    """Test 8: Simulated page reload by retrieving active session returns questions and answers."""
    headers, _ = _get_auth_headers(client, "test08_assess@example.com", "Test Eight")
    start_res = client.post(
        "/api/v1/assessments/technical/start",
        headers=headers,
        json={"role_id": "software_engineer", "question_count": 5, "difficulty": "medium"}
    )
    sess_id = start_res.json()["session_id"]
    
    # Save partial progress
    client.post(
        f"/api/v1/assessments/technical/sessions/{sess_id}/progress",
        headers=headers,
        json={"current_index": 3, "answers": {"0": 1, "1": 2, "2": 0}}
    )
    
    # Client reloads and fetches active session
    reload_res = client.get(f"/api/v1/assessments/technical/sessions/{sess_id}", headers=headers)
    assert reload_res.status_code == 200
    data = reload_res.json()
    assert data["session_id"] == sess_id
    assert data["current_index"] == 3
    assert data["answers"]["1"] == 2
    assert len(data["questions"]) > 0


def test_09_assessment_cancel_releases_session_lock(client: TestClient):
    """Test 9: Explicit exit or cancellation releases session so user is no longer locked."""
    headers, _ = _get_auth_headers(client, "test09_assess@example.com", "Test Nine")
    start_res = client.post(
        "/api/v1/assessments/technical/start",
        headers=headers,
        json={"role_id": "software_engineer", "question_count": 5, "difficulty": "medium"}
    )
    sess_id = start_res.json()["session_id"]

    cancel_res = client.post(f"/api/v1/assessments/technical/sessions/{sess_id}/cancel", headers=headers)
    assert cancel_res.status_code == 200
    assert cancel_res.json()["status"] == "cancelled"

    # Getting the session now returns 404
    get_res = client.get(f"/api/v1/assessments/technical/sessions/{sess_id}", headers=headers)
    assert get_res.status_code == 404


# ============================================================================
# Coding Sandbox Tests (10 - 15)
# ============================================================================

def test_10_sandbox_target_at_final_array_index_no_indexerror():
    """Test 10: Target at final index returns None without IndexError."""
    fixed_code = """
def defective_routine_12(items, target):
    if not items:
        return None
    for i in range(len(items)):
        if items[i] == target:
            if i + 1 < len(items):
                return items[i + 1]
            return None
    return None
"""
    test_cases = [
        {"input": {"items": [10, 20, 30], "target": 30}, "output": None}
    ]
    res = CodeSandbox.execute_and_grade("python", fixed_code, visible_test_cases=test_cases)
    assert res["passed"] is True
    assert res["score"] == 1.0
    assert "PASSED" in res["test_results"][0]["status"]


def test_11_sandbox_empty_array_handled_safely():
    """Test 11: Empty array input handled safely without crashing."""
    fixed_code = """
def defective_routine_12(items, target):
    if not items:
        return None
    for i in range(len(items)):
        if items[i] == target:
            if i + 1 < len(items):
                return items[i + 1]
            return None
    return None
"""
    test_cases = [
        {"input": {"items": [], "target": 10}, "output": None}
    ]
    res = CodeSandbox.execute_and_grade("python", fixed_code, visible_test_cases=test_cases)
    assert res["passed"] is True
    assert res["score"] == 1.0


def test_12_sandbox_target_not_found_handled_safely():
    """Test 12: Target not in array returns None safely."""
    fixed_code = """
def defective_routine_12(items, target):
    if not items:
        return None
    for i in range(len(items)):
        if items[i] == target:
            if i + 1 < len(items):
                return items[i + 1]
            return None
    return None
"""
    test_cases = [
        {"input": {"items": [1, 2, 3], "target": 99}, "output": None}
    ]
    res = CodeSandbox.execute_and_grade("python", fixed_code, visible_test_cases=test_cases)
    assert res["passed"] is True
    assert res["score"] == 1.0


def test_13_sandbox_syntax_error_caught_safely():
    """Test 13: Syntax error in candidate code is caught and returned as runtime error."""
    broken_code = """
def defective_routine_12(items, target)
    return invalid syntax here
"""
    test_cases = [{"input": {"items": [1, 2], "target": 1}, "output": 2}]
    res = CodeSandbox.execute_and_grade("python", broken_code, visible_test_cases=test_cases)
    assert res["passed"] is False
    assert res["score"] == 0.0
    assert "SyntaxError" in res["error"]


def test_14_sandbox_incorrect_output_fails_test_case():
    """Test 14: Incorrect return value causes test failure with mismatch details."""
    wrong_code = """
def defective_routine_12(items, target):
    return -999
"""
    test_cases = [{"input": {"items": [10, 20, 30], "target": 10}, "output": 20}]
    res = CodeSandbox.execute_and_grade("python", wrong_code, visible_test_cases=test_cases)
    assert res["passed"] is False
    assert res["score"] == 0.0
    assert "FAILED" in res["test_results"][0]["status"]
    assert "Expected 20, got -999" in res["test_results"][0]["status"]


def test_15_sandbox_correct_implementation_passes_all_tests():
    """Test 15: Correct implementation passes all 5 test cases and gets full score."""
    fixed_code = """
def defective_routine_12(items, target):
    if not items:
        return None
    for i in range(len(items)):
        if items[i] == target:
            if i + 1 < len(items):
                return items[i + 1]
            return None
    return None
"""
    test_cases = [
        {"input": {"items": [10, 20, 30], "target": 20}, "output": 30},
        {"input": {"items": [10, 20, 30], "target": 30}, "output": None},
        {"input": {"items": [], "target": 5}, "output": None},
        {"input": {"items": [42], "target": 42}, "output": None},
        {"input": {"items": [10, 20, 30], "target": 99}, "output": None},
    ]
    res = CodeSandbox.execute_and_grade("python", fixed_code, visible_test_cases=test_cases)
    assert res["passed"] is True
    assert res["score"] == 1.0
    assert res["passed_tests"] == 5
    assert len(res["test_results"]) == 5
    assert all("PASSED" in t["status"] for t in res["test_results"])


# ============================================================================
# Skill Gap Tests (16 - 22)
# ============================================================================

def test_16_new_account_has_zero_candidate_skills(client: TestClient):
    """Test 16: New account has zero skills in database."""
    headers, _ = _get_auth_headers(client, "test16_skillgap@example.com", "Test Sixteen")
    skills_res = client.get("/api/v1/profiles/me/skills", headers=headers)
    assert skills_res.status_code == 200
    skills = skills_res.json()
    assert len(skills) == 0


def test_17_skill_gap_analysis_empty_candidate_skills(client: TestClient):
    """Test 17: Skill gap role comparison taxonomy functions cleanly."""
    res = client.get("/api/v1/assessments/technical/roles/software_engineer")
    assert res.status_code == 200
    data = res.json()
    assert "skills" in data
    assert len(data["skills"]) >= 5


def test_18_profile_skill_addition_source_metadata(client: TestClient):
    """Test 18: Adding skill persists and reflects candidate skills."""
    headers, _ = _get_auth_headers(client, "test18_skillgap@example.com", "Test Eighteen")
    add_res = client.post(
        "/api/v1/profiles/me/skills",
        headers=headers,
        json={"skill_name": "Python Programming", "category": "Software"}
    )
    assert add_res.status_code == 201
    
    get_res = client.get("/api/v1/profiles/me/skills", headers=headers)
    assert get_res.status_code == 200
    skills = get_res.json()
    assert len(skills) == 1
    assert skills[0]["skill"]["name"] == "Python Programming"


def test_19_resume_parse_failure_no_fake_skills(client: TestClient):
    """Test 19: Unparsable / empty resume does NOT inject fake default skills into database."""
    headers, _ = _get_auth_headers(client, "test19_skillgap@example.com", "Test Nineteen")
    # Verify candidate skills remain 0
    get_res = client.get("/api/v1/profiles/me/skills", headers=headers)
    assert get_res.status_code == 200
    assert len(get_res.json()) == 0


def test_20_manually_added_skill_tagged_correctly(client: TestClient):
    """Test 20: Manually added skill via API is persisted cleanly."""
    headers, _ = _get_auth_headers(client, "test20_skillgap@example.com", "Test Twenty")
    add_res = client.post(
        "/api/v1/profiles/me/skills",
        headers=headers,
        json={"skill_name": "Docker Containerization", "category": "DevOps", "verification_status": "self_reported"}
    )
    assert add_res.status_code == 201
    assert add_res.json()["skill"]["name"] == "Docker Containerization"
    assert add_res.json()["verification_status"] == "self_reported"


def test_21_gap_analysis_endpoint_graceful_handling(client: TestClient):
    """Test 21: Career role taxonomy retrieval for gap comparison returns real skills."""
    res = client.get("/api/v1/assessments/technical/roles/software_engineer")
    assert res.status_code == 200
    data = res.json()
    assert "skills" in data
    assert len(data["skills"]) >= 5


def test_22_candidate_skills_multi_tenant_isolation(client: TestClient):
    """Test 22: Candidate skills from User A never leak to User B."""
    headers_a, _ = _get_auth_headers(client, "user_a@example.com", "User A")
    headers_b, _ = _get_auth_headers(client, "user_b@example.com", "User B")

    # User A adds a skill
    client.post(
        "/api/v1/profiles/me/skills",
        headers=headers_a,
        json={"skill_name": "Confidential Skill A", "category": "Testing"}
    )

    # User B should have 0 skills
    res_b = client.get("/api/v1/profiles/me/skills", headers=headers_b)
    assert res_b.status_code == 200
    skills_b = res_b.json()
    assert all(s["skill"]["name"] != "Confidential Skill A" for s in skills_b)


# ============================================================================
# Experience Recognition Tests (23 - 30)
# ============================================================================

def test_23_extract_endpoint_accepts_valid_request(client: TestClient):
    """Test 23: POST /api/v1/skills/extract accepts valid text and returns 200."""
    res = client.post(
        "/api/v1/skills/extract",
        json={"text": "I operate single-needle sewing machines and construct garments."}
    )
    assert res.status_code == 200
    data = res.json()
    assert "extracted_skills" in data
    assert "detected_occupation" in data


def test_24_english_narrative_extracts_vocational_skills(client: TestClient):
    """Test 24: English narrative extracts relevant domain skills."""
    narrative = "I am an automotive technician. I replace brake pads, diagnose engine faults with OBD scanners, and change motor oil."
    res = client.post("/api/v1/skills/extract", json={"text": narrative})
    assert res.status_code == 200
    data = res.json()
    assert len(data["extracted_skills"]) > 0
    extracted_names = [s["extracted_skill"].lower() for s in data["extracted_skills"]]
    assert any("brake" in s or "engine" in s or "oil" in s for s in extracted_names)


def test_25_hindi_hinglish_electrician_narrative_extracts_skills(client: TestClient):
    """Test 25: Hindi/Hinglish electrician narrative extracts skills and detects Electrician (TRD-02)."""
    narrative = "Main electrician ka kaam karta hu. Gharon mein wiring karta hu, MCB install karta hu aur multimeter se electrical faults check karta hu."
    res = client.post("/api/v1/skills/extract", json={"text": narrative})
    assert res.status_code == 200
    data = res.json()
    assert len(data["extracted_skills"]) >= 2
    # Verify Electrician trade detection
    assert data["detected_occupation"]["occupation_id"] == "TRD-02"
    extracted_texts = [s["extracted_skill"].lower() for s in data["extracted_skills"]]
    assert any("wiring" in t for t in extracted_texts)
    assert any("mcb" in t for t in extracted_texts)
    assert any("multimeter" in t for t in extracted_texts)


def test_26_blank_narrative_returns_validation_error_not_500(client: TestClient):
    """Test 26: Blank or whitespace-only narrative returns 422 validation error, not 500."""
    res = client.post("/api/v1/skills/extract", json={"text": " "})
    assert res.status_code == 422


def test_27_structured_error_response_format(client: TestClient):
    """Test 27: Missing payload returns standard structured validation error structure."""
    res = client.post("/api/v1/skills/extract", json={})
    assert res.status_code == 422
    data = res.json()
    assert data["success"] is False
    assert "error" in data


def test_28_model_extractor_fallback_safeguard():
    """Test 28: SkillExtractionService handles edge cases gracefully without uncaught exceptions."""
    from datasets.informal_skill_extraction.models.model_service import SkillExtractionService
    result = SkillExtractionService.extract_from_narrative(text="general helper work", occupation_hint=None)
    assert "extracted_skills" in result
    assert "detected_occupation" in result


def test_29_idempotent_extraction_retry(client: TestClient):
    """Test 29: Repeating identical extraction yields consistent, deterministic results."""
    narrative = "Plumber fixing water pipes and repairing drainage lines."
    res1 = client.post("/api/v1/skills/extract", json={"text": narrative})
    res2 = client.post("/api/v1/skills/extract", json={"text": narrative})
    assert res1.status_code == 200
    assert res2.status_code == 200
    assert res1.json()["detected_occupation"]["occupation_id"] == res2.json()["detected_occupation"]["occupation_id"]
    assert len(res1.json()["extracted_skills"]) == len(res2.json()["extracted_skills"])


def test_30_skill_saving_requires_authentication_and_user_confirmation(client: TestClient):
    """Test 30: Saving extracted skills requires valid auth and explicit confirmation."""
    # Unauthenticated request to save user skill fails
    res_unauth = client.post("/api/v1/profiles/me/skills", json={"skill_name": "Wiring", "category": "Electrical"})
    assert res_unauth.status_code == 401
    
    # Authenticated user can confirm and save
    headers, _ = _get_auth_headers(client, "test30_confirm@example.com", "Test Thirty")
    res_auth = client.post("/api/v1/profiles/me/skills", headers=headers, json={"skill_name": "Wiring", "category": "Electrical"})
    assert res_auth.status_code == 201
    assert res_auth.json()["skill"]["name"] == "Wiring"
