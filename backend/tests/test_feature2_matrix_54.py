"""
Comprehensive 54-Matrix Test Suite for Feature 2:
Tests all 9 Career Roles x 6 Assessment Types = 54 Combinations.
Verifies question selection, masking, sandbox interaction, scoring, and persistence.
"""

import pytest
import json
import os
from fastapi.testclient import TestClient

ROLES = [
    "software_engineer",
    "ai_ml_engineer",
    "data_scientist",
    "frontend_developer",
    "backend_developer",
    "devops_engineer",
    "data_analyst",
    "cybersecurity_engineer",
    "cloud_engineer",
]

ASSESSMENT_TYPES = [
    "mcq",
    "coding",
    "debugging",
    "scenario",
    "sql",
    "system_design",
]

# Track results for reporting
MATRIX_RESULTS = []

def _register_matrix_user(client: TestClient, role_id: str, assessment_type: str) -> tuple[dict, str]:
    email = f"auditor.{role_id}.{assessment_type}@elevate.ai"
    res = client.post(
        "/api/v1/auth/register",
        json={"email": email, "password": "Password123!", "full_name": f"Auditor {role_id}"},
    )
    assert res.status_code == 201, f"User registration failed: {res.text}"
    data = res.json()
    token = data["token"]["access_token"]
    return {"Authorization": f"Bearer {token}"}, data["user"]["id"]


@pytest.mark.parametrize("role_id", ROLES)
@pytest.mark.parametrize("assessment_type", ASSESSMENT_TYPES)
def test_matrix_combination(client: TestClient, role_id: str, assessment_type: str):
    """Verifies that every single role x type combination delivers valid masked questions and processes answers."""
    auth_headers, _ = _register_matrix_user(client, role_id, assessment_type)

    # 1. Start assessment filtering by role and type
    req_body = {
        "role_id": role_id,
        "assessment_type": assessment_type,
        "question_count": 3,
        "difficulty": "adaptive"
    }
    start_res = client.post("/api/v1/assessments/technical/start", json=req_body, headers=auth_headers)
    assert start_res.status_code == 200, f"Failed start for {role_id} / {assessment_type}: {start_res.text}"
    start_data = start_res.json()
    session_id = start_data["session_id"]
    questions = start_data["questions"]

    assert len(questions) > 0, f"No questions returned for {role_id} / {assessment_type}"
    for q in questions:
        assert q["role_id"] == role_id
        assert q["assessment_type"] == assessment_type
        # Verify strict masking: answers not exposed
        assert "correct_answer" not in q
        assert "reference_solution" not in q
        assert "hidden_test_cases" not in q

    # 2. Submit mock candidate answers
    submitted_answers = []
    for q in questions:
        if assessment_type == "mcq":
            ans_val = "A"
        elif assessment_type in ("coding", "debugging"):
            ans_val = "def solution():\n    return True"
        elif assessment_type == "sql":
            ans_val = "SELECT * FROM sample_table;"
        else:
            ans_val = "Candidate structured response following production design best practices."

        submitted_answers.append({
            "question_id": q["question_id"],
            "answer": ans_val,
            "time_spent_seconds": 45
        })

    submit_req = {
        "session_id": session_id,
        "role_id": role_id,
        "answers": submitted_answers
    }
    submit_res = client.post("/api/v1/assessments/technical/submit", json=submit_req, headers=auth_headers)
    assert submit_res.status_code == 200, f"Failed submit for {role_id} / {assessment_type}: {submit_res.text}"
    result_data = submit_res.json()

    assert result_data["result_id"]
    assert result_data["role_id"] == role_id
    assert 0.0 <= result_data["overall_score_percentage"] <= 100.0
    assert -3.0 <= result_data["ability_theta"] <= 3.0
    assert isinstance(result_data["skill_performances"], list)
    assert isinstance(result_data["skill_gaps"], list)
    assert isinstance(result_data["roadmap_milestones"], list)

    MATRIX_RESULTS.append({
        "role_id": role_id,
        "assessment_type": assessment_type,
        "questions_verified": len(questions),
        "status": "PASSED",
        "session_id": session_id,
        "result_id": result_data["result_id"]
    })
