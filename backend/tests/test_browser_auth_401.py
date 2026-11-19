"""
Regression test suite specifically reproducing the live browser 401 Unauthorized root cause.
Ensures:
1. Public technical roles catalog can be retrieved without authentication (HTTP 200).
2. Starting an assessment without an Authorization header returns HTTP 401 Unauthorized.
3. Starting an assessment with a fake/non-JWT demo token returns HTTP 401 Unauthorized.
4. Starting an assessment with an authentic, signed JWT token returns HTTP 200 OK with session_id.
5. Assessment submission without authentication returns HTTP 401 Unauthorized.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.security import create_access_token


@pytest.fixture
def client():
    return TestClient(app)


def test_public_roles_catalog_accessible_without_auth(client):
    """Verifies that /roles does NOT require auth so candidates can browse tracks freely."""
    response = client.get("/api/v1/assessments/technical/roles")
    assert response.status_code == 200
    roles = response.json()
    assert len(roles) == 9
    role_ids = {r["role_id"] for r in roles}
    assert "software_engineer" in role_ids
    assert "ai_ml_engineer" in role_ids
    assert "backend_developer" in role_ids


def test_start_assessment_without_auth_header_fails_with_401(client):
    """
    CRITICAL REGRESSION:
    Reproduces the exact browser 401 root cause where a candidate clicked 'Start Assessment'
    without having logged in first (localStorage had no token).
    """
    payload = {
        "role_id": "backend_developer",
        "assessment_type": "mcq",
        "difficulty": "adaptive",
        "question_count": 5,
    }
    # Request without Authorization header
    response = client.post("/api/v1/assessments/technical/start", json=payload)
    assert response.status_code == 401
    assert "Not authenticated" in response.text or "detail" in response.json()


def test_start_assessment_with_fake_demo_token_fails_with_401(client):
    """
    REGRESSION:
    Reproduces the legacy bug where AuthContext wrote 'demo-token-TIMESTAMP' to localStorage,
    which failed backend JWT decoding.
    """
    payload = {
        "role_id": "backend_developer",
        "assessment_type": "mcq",
        "difficulty": "adaptive",
        "question_count": 5,
    }
    headers = {"Authorization": "Bearer demo-token-1731659421234"}
    response = client.post("/api/v1/assessments/technical/start", json=payload, headers=headers)
    assert response.status_code == 401


def test_start_assessment_with_valid_jwt_succeeds(client):
    """
    Verifies that a validly signed JWT token succeeds and returns a full diagnostic session.
    """
    import uuid
    unique_email = f"browser_test_{uuid.uuid4().hex[:8]}@example.com"
    reg = client.post(
        "/api/v1/auth/register",
        json={"email": unique_email, "password": "Password123!", "full_name": "Browser Test User"},
    )
    assert reg.status_code == 201
    token = reg.json()["token"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    payload = {
        "role_id": "backend_developer",
        "assessment_type": "mcq",
        "difficulty": "adaptive",
        "question_count": 5,
    }
    response = client.post("/api/v1/assessments/technical/start", json=payload, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "session_id" in data
    assert len(data["questions"]) > 0
    assert data["role_id"] == "backend_developer"


def test_submit_without_auth_fails_with_401(client):
    """Verifies that submitting answers without authentication is rejected."""
    payload = {
        "session_id": "00000000-0000-0000-0000-000000000000",
        "role_id": "backend_developer",
        "answers": [],
    }
    response = client.post("/api/v1/assessments/technical/submit", json=payload)
    assert response.status_code == 401

