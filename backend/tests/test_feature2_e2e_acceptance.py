"""
Comprehensive End-to-End Acceptance Test for Feature 2:
Technical Assessment & Career Intelligence Engine.
Simulates the real 19-step candidate journey across all 9 IT roles and 6 assessment types.
"""

import pytest
import uuid
from fastapi.testclient import TestClient

def _register(client: TestClient, email: str, name: str) -> tuple[dict, str]:
    res = client.post(
        "/api/v1/auth/register",
        json={"email": email, "password": "Password123!", "full_name": name},
    )
    assert res.status_code == 201
    data = res.json()
    token = data["token"]["access_token"]
    user_id = data["user"]["id"]
    return {"Authorization": f"Bearer {token}"}, user_id


def test_e2e_all_nine_roles_availability(client: TestClient):
    """E2E Check: Verify all 9 roles are retrievable and have full competency mappings."""
    all_roles = [
        "software_engineer", "ai_ml_engineer", "data_scientist", "frontend_developer",
        "backend_developer", "devops_engineer", "data_analyst", "cybersecurity_engineer", "cloud_engineer"
    ]
    for rid in all_roles:
        res = client.get(f"/api/v1/assessments/technical/roles/{rid}")
        assert res.status_code == 200, f"Role {rid} retrieval failed"
        data = res.json()
        assert data["role_id"] == rid
        assert len(data["skills"]) == 5
        for s in data["skills"]:
            assert len(s["subtopics"]) >= 5


def test_e2e_all_six_assessment_types(client: TestClient):
    """E2E Check: Verify question selection and delivery for all 6 assessment types."""
    auth, _ = _register(client, "e2e.alltypes@example.com", "Types Evaluator")
    types = ["mcq", "coding", "debugging", "scenario", "sql", "system_design"]
    
    for t in types:
        res = client.post(
            "/api/v1/assessments/technical/start",
            json={"role_id": "software_engineer", "assessment_type": t, "question_count": 2},
            headers=auth
        )
        assert res.status_code == 200, f"Failed to start assessment for type: {t}"
        data = res.json()
        assert len(data["questions"]) > 0
        for q in data["questions"]:
            assert q["assessment_type"] == t


def test_e2e_candidate_full_journey(client: TestClient):
    """
    Simulate the complete 19-step candidate journey for AI/ML Engineer:
    - Step 1: Login/Register
    - Step 2-4: Select Role & View Skills
    - Step 5-7: Configure Adaptive Assessment
    - Step 8-10: Start Assessment & Receive Masked Questions
    - Step 11: Execute Code Sandbox & SQL Sandbox Tests
    - Step 12: Submit Complete Assessment
    - Step 13-16: Server-calculated scores, Skill Mastery, Skill Gaps, Roadmap
    - Step 17-18: Verify Persistence in History
    - Step 19: Cross-User Data Isolation
    """
    # Step 1: Candidate registers and authenticates
    candidate_headers, candidate_id = _register(
        client, "e2e.candidate.aiml@example.com", "Priya Sharma"
    )

    # Step 2-4: View AI/ML Engineer skills
    role_res = client.get("/api/v1/assessments/technical/roles/ai_ml_engineer")
    assert role_res.status_code == 200
    role_data = role_res.json()
    assert role_data["title"] == "AI/ML Engineer"

    # Step 5-10: Start adaptive assessment
    start_payload = {
        "role_id": "ai_ml_engineer",
        "difficulty": "adaptive",
        "question_count": 6
    }
    start_res = client.post(
        "/api/v1/assessments/technical/start",
        json=start_payload,
        headers=candidate_headers
    )
    assert start_res.status_code == 200
    sess = start_res.json()
    session_id = sess["session_id"]
    questions = sess["questions"]
    assert len(questions) == 6

    # Verify answers are never leaked
    for q in questions:
        assert "correct_answer" not in q
        assert "hidden_test_cases" not in q

    # Step 11: Interactive sandbox tests
    code_res = client.post(
        "/api/v1/assessments/technical/sandbox/run-code",
        json={
            "language": "python",
            "code": "def forward(x):\n    return x\n",
            "visible_test_cases": [{"input": "forward(1)", "output": "1"}]
        },
        headers=candidate_headers
    )
    assert code_res.status_code == 200
    assert code_res.json()["passed"] is True

    sql_res = client.post(
        "/api/v1/assessments/technical/sandbox/run-sql",
        json={
            "candidate_query": "SELECT model_id, accuracy FROM models WHERE accuracy > 0.8;",
            "schema_sql": "CREATE TABLE models (model_id INT, accuracy FLOAT);",
            "sample_db_sql": "INSERT INTO models VALUES (1, 0.92), (2, 0.74);"
        },
        headers=candidate_headers
    )
    assert sql_res.status_code == 200
    assert sql_res.json()["passed"] is True
    assert len(sql_res.json()["actual_rows"]) == 1

    # Step 12: Submit all answers
    submit_answers = []
    for q in questions:
        atype = q["assessment_type"]
        if atype in ("mcq", "scenario"):
            ans_val = "A"
        elif atype in ("coding", "debugging"):
            ans_val = "def model_routine():\n    return True\n"
        elif atype == "sql":
            ans_val = "SELECT * FROM model_predictions_1 WHERE confidence_score > 0.9;"
        else:
            ans_val = "Detailed scalable architecture with microservices, Kafka event bus, and Redis caching."
            
        submit_answers.append({
            "question_id": q["question_id"],
            "answer": ans_val,
            "language": "python",
            "time_taken_seconds": 40
        })

    sub_res = client.post(
        "/api/v1/assessments/technical/submit",
        json={
            "session_id": session_id,
            "role_id": "ai_ml_engineer",
            "answers": submit_answers
        },
        headers=candidate_headers
    )
    assert sub_res.status_code == 200
    result = sub_res.json()
    result_id = result["result_id"]

    # Step 13-16: Server-calculated scorecard, mastery, gaps, roadmap
    assert "overall_score_percentage" in result
    assert "points_awarded" in result
    assert "total_points" in result
    assert result["total_points"] > 0
    assert len(result["skill_performances"]) >= 1
    assert len(result["roadmap_milestones"]) >= 1
    for m in result["roadmap_milestones"]:
        assert m["resource_title"]
        assert m["resource_url"].startswith("http")

    # Step 17-18: Verify persistence in history
    hist_res = client.get("/api/v1/assessments/technical/history", headers=candidate_headers)
    assert hist_res.status_code == 200
    history = hist_res.json()
    assert any(h["result_id"] == result_id for h in history)

    # Step 19: Cross-user data isolation
    other_headers, other_id = _register(client, "other.user@example.com", "Other User")
    isolated_res = client.get(f"/api/v1/assessments/technical/results/{result_id}", headers=other_headers)
    assert isolated_res.status_code == 404, "User isolation violated: other user was able to access result"

