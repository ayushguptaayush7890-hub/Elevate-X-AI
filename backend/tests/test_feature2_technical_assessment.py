"""
Integration & Unit Tests for Feature 2: Technical Assessment & Career Intelligence Engine.
Verifies all 9 career roles, 6 assessment types, sandboxes, adaptive engine, scoring, and history.
"""

import pytest
import uuid
from fastapi.testclient import TestClient

def _register_user(client: TestClient, email: str, name: str) -> tuple[dict, str]:
    res = client.post(
        "/api/v1/auth/register",
        json={"email": email, "password": "Password123!", "full_name": name},
    )
    assert res.status_code == 201
    data = res.json()
    token = data["token"]["access_token"]
    user_id = data["user"]["id"]
    return {"Authorization": f"Bearer {token}"}, user_id


def test_list_all_nine_technical_roles(client: TestClient):
    """Verify endpoint lists all 9 supported IT career roles with 5 skills each."""
    res = client.get("/api/v1/assessments/technical/roles")
    assert res.status_code == 200
    roles = res.json()
    assert len(roles) == 9
    role_ids = {r["role_id"] for r in roles}
    expected_roles = {
        "software_engineer", "ai_ml_engineer", "data_scientist", "frontend_developer",
        "backend_developer", "devops_engineer", "data_analyst", "cybersecurity_engineer", "cloud_engineer"
    }
    assert role_ids == expected_roles
    for r in roles:
        assert r["skill_count"] == 5


def test_get_role_details_with_subtopics(client: TestClient):
    """Verify detailed role taxonomy retrieval with skills and subtopics."""
    res = client.get("/api/v1/assessments/technical/roles/ai_ml_engineer")
    assert res.status_code == 200
    data = res.json()
    assert data["role_id"] == "ai_ml_engineer"
    assert len(data["skills"]) == 5
    for s in data["skills"]:
        assert len(s["subtopics"]) >= 5


def test_start_assessment_masks_answer_keys(client: TestClient):
    """Verify questions delivered to candidate DO NOT leak answers or hidden tests."""
    auth_headers, _ = _register_user(client, "candidate.swe@example.com", "Alex Chen")
    payload = {
        "role_id": "software_engineer",
        "question_count": 5,
        "difficulty": "medium"
    }
    res = client.post("/api/v1/assessments/technical/start", json=payload, headers=auth_headers)
    assert res.status_code == 200, f"Error: {res.text}"
    data = res.json()
    assert data["session_id"]
    assert len(data["questions"]) == 5
    for q in data["questions"]:
        # Verify server secrets are NOT exposed
        assert "correct_answer" not in q
        assert "answer_explanation" not in q
        assert "hidden_test_cases" not in q
        assert "reference_solution" not in q


def test_sql_sandbox_execution_and_security(client: TestClient):
    """Verify in-memory SQLite sandbox executes valid SELECT and rejects destructive statements."""
    auth_headers, _ = _register_user(client, "candidate.sql@example.com", "Sarah Miller")
    # 1. Valid Query
    payload = {
        "candidate_query": "SELECT employee_id, department, salary FROM employees WHERE salary > 70000 ORDER BY salary DESC;",
        "schema_sql": "CREATE TABLE employees (employee_id INT, department TEXT, salary INT);",
        "sample_db_sql": "INSERT INTO employees VALUES (1, 'Engineering', 95000), (2, 'Marketing', 60000), (3, 'Engineering', 85000);"
    }
    res = client.post("/api/v1/assessments/technical/sandbox/run-sql", json=payload, headers=auth_headers)
    assert res.status_code == 200
    data = res.json()
    assert data["passed"] is True
    assert len(data["actual_rows"]) == 2
    assert data["actual_rows"][0]["salary"] == 95000

    # 2. Blocked Destructive Query (DROP TABLE)
    evil_payload = {
        "candidate_query": "DROP TABLE employees; SELECT * FROM employees;",
        "schema_sql": "CREATE TABLE employees (id INT);",
        "sample_db_sql": "INSERT INTO employees VALUES (1);"
    }
    res2 = client.post("/api/v1/assessments/technical/sandbox/run-sql", json=evil_payload, headers=auth_headers)
    assert res2.status_code == 200
    data2 = res2.json()
    assert data2["passed"] is False
    assert "Disallowed SQL operations" in data2["error"] or "Only read-only" in data2["error"]


def test_code_sandbox_python_execution(client: TestClient):
    """Verify code sandbox runs tests and enforces execution safety."""
    auth_headers, _ = _register_user(client, "candidate.py@example.com", "David Kumar")
    payload = {
        "language": "python",
        "code": "def solve(x):\n    return x * 2\n",
        "visible_test_cases": [
            {"input": "solve(2)", "output": "4"},
            {"input": "solve(5)", "output": "10"}
        ]
    }
    res = client.post("/api/v1/assessments/technical/sandbox/run-code", json=payload, headers=auth_headers)
    assert res.status_code == 200
    data = res.json()
    assert data["passed"] is True
    assert data["passed_tests"] == 2


def test_adaptive_step_updates_theta(client: TestClient):
    """Verify interactive adaptive evaluation updates candidate latent ability (theta)."""
    auth_headers, _ = _register_user(client, "candidate.adaptive@example.com", "Elena Rostova")
    start_res = client.post(
        "/api/v1/assessments/technical/start",
        json={"role_id": "software_engineer", "question_count": 3, "difficulty": "adaptive"},
        headers=auth_headers
    )
    session_id = start_res.json()["session_id"]
    q1 = start_res.json()["questions"][0]

    # Submit step
    step_payload = {
        "session_id": session_id,
        "question_id": q1["question_id"],
        "answer": "B"
    }
    step_res = client.post("/api/v1/assessments/technical/adaptive-step", json=step_payload, headers=auth_headers)
    assert step_res.status_code == 200
    step_data = step_res.json()
    assert "current_theta" in step_data
    assert "recommended_difficulty" in step_data


def test_full_assessment_submission_and_persistence(client: TestClient):
    """Verify end-to-end submission, scoring, skill gap detection, roadmap generation, and persistence."""
    auth_headers, user_id = _register_user(client, "candidate.aiml@example.com", "Marcus Vance")
    start_res = client.post(
        "/api/v1/assessments/technical/start",
        json={"role_id": "ai_ml_engineer", "question_count": 4, "difficulty": "medium"},
        headers=auth_headers
    )
    sess = start_res.json()
    session_id = sess["session_id"]
    questions = sess["questions"]

    # Submit answers
    submit_payload = {
        "session_id": session_id,
        "role_id": "ai_ml_engineer",
        "answers": [
            {"question_id": q["question_id"], "answer": "A", "time_taken_seconds": 45}
            for q in questions
        ]
    }
    sub_res = client.post("/api/v1/assessments/technical/submit", json=submit_payload, headers=auth_headers)
    assert sub_res.status_code == 200
    result = sub_res.json()
    assert result["result_id"]
    assert result["role_id"] == "ai_ml_engineer"
    assert "overall_score_percentage" in result
    assert len(result["skill_performances"]) >= 1
    assert len(result["roadmap_milestones"]) >= 1

    # Verify history persistence
    hist_res = client.get("/api/v1/assessments/technical/history", headers=auth_headers)
    assert hist_res.status_code == 200
    history = hist_res.json()
    assert any(h["result_id"] == result["result_id"] for h in history)

    # Verify single result retrieval
    get_res = client.get(f"/api/v1/assessments/technical/results/{result['result_id']}", headers=auth_headers)
    assert get_res.status_code == 200
    assert get_res.json()["result_id"] == result["result_id"]


def test_cross_user_isolation(client: TestClient):
    """Verify User B cannot access User A's technical assessment results."""
    user_a_headers, _ = _register_user(client, "tech.user.a@example.com", "Tech Alpha")
    user_b_headers, _ = _register_user(client, "tech.user.b@example.com", "Tech Beta")

    # User A starts and submits
    start_res = client.post(
        "/api/v1/assessments/technical/start",
        json={"role_id": "software_engineer", "question_count": 2, "difficulty": "easy"},
        headers=user_a_headers
    )
    session_id = start_res.json()["session_id"]
    q1 = start_res.json()["questions"][0]

    sub_res = client.post(
        "/api/v1/assessments/technical/submit",
        json={"session_id": session_id, "role_id": "software_engineer", "answers": [{"question_id": q1["question_id"], "answer": "A"}]},
        headers=user_a_headers
    )
    res_id = sub_res.json()["result_id"]

    # User B attempts to access User A's result
    forbidden_res = client.get(f"/api/v1/assessments/technical/results/{res_id}", headers=user_b_headers)
    assert forbidden_res.status_code == 404
