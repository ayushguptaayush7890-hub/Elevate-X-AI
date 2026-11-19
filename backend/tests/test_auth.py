"""
Authentication and User Account Unit & Integration Tests.
"""

from fastapi.testclient import TestClient


def test_register_success(client: TestClient):
    """Verify clean user registration with password hashing and auto-initialized profile."""
    payload = {
        "email": "ramesh.tailor@example.com",
        "password": "StrongPassword123!",
        "full_name": "Ramesh Sharma",
        "trade_category": "Master Tailor & Pattern Artisan",
    }
    response = client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == 201

    data = response.json()
    assert "token" in data
    assert "user" in data
    assert data["token"]["token_type"] == "bearer"
    assert data["user"]["email"] == "ramesh.tailor@example.com"
    assert data["user"]["full_name"] == "Ramesh Sharma"
    assert "password" not in data["user"]
    assert "hashed_password" not in data["user"]


def test_register_duplicate_email(client: TestClient):
    """Verify duplicate email registration is rejected with 400 Bad Request."""
    payload = {
        "email": "duplicate.user@example.com",
        "password": "Password123!",
        "full_name": "Test User",
    }
    # First registration
    r1 = client.post("/api/v1/auth/register", json=payload)
    assert r1.status_code == 201

    # Duplicate registration
    r2 = client.post("/api/v1/auth/register", json=payload)
    assert r2.status_code == 400
    assert "already exists" in r2.json()["error"]["message"]


def test_login_success(client: TestClient):
    """Verify successful authentication with valid credentials."""
    # Register first
    client.post(
        "/api/v1/auth/register",
        json={"email": "sunita.baker@example.com", "password": "BakerSecret456!", "full_name": "Sunita Verma"},
    )

    # Login
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "sunita.baker@example.com", "password": "BakerSecret456!"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data["token"]
    assert "refresh_token" in data["token"]
    assert data["user"]["email"] == "sunita.baker@example.com"


def test_login_invalid_password(client: TestClient):
    """Verify login failure with incorrect password returns 401 Unauthorized."""
    client.post(
        "/api/v1/auth/register",
        json={"email": "arif.electrician@example.com", "password": "CorrectPassword123!"},
    )

    response = client.post(
        "/api/v1/auth/login",
        json={"email": "arif.electrician@example.com", "password": "WrongPassword999!"},
    )
    assert response.status_code == 401
    assert "Incorrect email or password" in response.json()["error"]["message"]


def test_login_nonexistent_user(client: TestClient):
    """Verify login failure with unmapped email returns 401 Unauthorized."""
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "does.not.exist@example.com", "password": "AnyPassword123!"},
    )
    assert response.status_code == 401


def test_get_me_authenticated(client: TestClient):
    """Verify /api/v1/auth/me returns current user details when authenticated."""
    reg = client.post(
        "/api/v1/auth/register",
        json={"email": "rajesh.diesel@example.com", "password": "DieselTech789!", "full_name": "Rajesh Kumar"},
    )
    token = reg.json()["token"]["access_token"]

    response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert response.json()["email"] == "rajesh.diesel@example.com"


def test_get_me_unauthorized(client: TestClient):
    """Verify /api/v1/auth/me rejects requests without bearer token."""
    response = client.get("/api/v1/auth/me")
    assert response.status_code == 401


def test_logout_revocation(client: TestClient):
    """Verify logout revokes the bearer token and prevents reuse."""
    reg = client.post(
        "/api/v1/auth/register",
        json={"email": "vikas.logistics@example.com", "password": "ColdChain321!", "full_name": "Vikas Singh"},
    )
    token = reg.json()["token"]["access_token"]

    # Verify access before logout
    r1 = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert r1.status_code == 200

    # Logout
    logout_res = client.post(
        "/api/v1/auth/logout",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert logout_res.status_code == 200

    # Verify access rejected after logout
    r2 = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert r2.status_code == 401


def test_token_refresh(client: TestClient):
    """Verify refresh token issues a new access token."""
    reg = client.post(
        "/api/v1/auth/register",
        json={"email": "anita.handloom@example.com", "password": "WeavingExpert999!", "full_name": "Anita Devi"},
    )
    refresh_token = reg.json()["token"]["refresh_token"]

    response = client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": refresh_token},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data


def test_forgot_password_and_reset_flow(client: TestClient):
    """Verify end-to-end forgot-password and password reset workflow."""
    email = "recovery.test@example.com"
    client.post(
        "/api/v1/auth/register",
        json={"email": email, "password": "OriginalPassword1!"},
    )

    # 1. Request password reset
    forgot_res = client.post(
        "/api/v1/auth/forgot-password",
        json={"email": email},
    )
    assert forgot_res.status_code == 200
    token_preview = forgot_res.json()["details"]["token_preview"]
    assert token_preview is not None

    # 2. Reset password using token
    reset_res = client.post(
        "/api/v1/auth/reset-password",
        json={"token": token_preview, "new_password": "NewSecretPassword2026!"},
    )
    assert reset_res.status_code == 200

    # 3. Old password should fail
    fail_res = client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": "OriginalPassword1!"},
    )
    assert fail_res.status_code == 401

    # 4. New password should succeed
    success_res = client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": "NewSecretPassword2026!"},
    )
    assert success_res.status_code == 200

