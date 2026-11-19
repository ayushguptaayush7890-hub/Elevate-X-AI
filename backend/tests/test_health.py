"""
Unit & Integration Tests for API Health & Diagnostics Endpoints.
"""

from unittest.mock import patch
from fastapi.testclient import TestClient


def test_api_health_endpoint(client: TestClient):
    """Verify general /api/v1/health returns 200 OK with operational metadata."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data
    assert "timestamp" in data
    assert "environment" in data
    assert data["version"] == "1.0.0"


def test_api_alias_health_endpoint(client: TestClient):
    """Verify convenience /api/health alias functions identically."""
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_database_health_connected(client: TestClient):
    """Verify /api/v1/health/database reports healthy when database is reachable."""
    with patch("app.api.v1.health.check_db_connection") as mock_check:
        mock_check.return_value = (True, "postgresql", None)

        response = client.get("/api/v1/health/database")
        assert response.status_code == 200

        data = response.json()
        assert data["status"] == "healthy"
        assert data["database"] == "connected"
        assert data["dialect"] == "postgresql"
        assert data["error"] is None
        assert "timestamp" in data


def test_database_health_disconnected(client: TestClient):
    """
    Verify /api/v1/health/database strictly returns 503 Service Unavailable
    when the database connection is unreachable (NEVER reports healthy).
    """
    with patch("app.api.v1.health.check_db_connection") as mock_check:
        mock_check.return_value = (False, None, "Connection refused: PostgreSQL host down")

        response = client.get("/api/v1/health/database")
        assert response.status_code == 503

        data = response.json()
        assert data["status"] == "unhealthy"
        assert data["database"] == "disconnected"
        assert "Connection refused" in data["error"]
        assert "timestamp" in data


def test_openapi_schema_endpoint(client: TestClient):
    """Verify OpenAPI v1 specification schema is reachable."""
    response = client.get("/api/v1/openapi.json")
    assert response.status_code == 200
    schema = response.json()
    assert schema["info"]["title"] == "Elevate X AI API"
    assert "/api/v1/health" in schema["paths"]
    assert "/api/v1/health/database" in schema["paths"]


def test_root_redirect_to_docs(client: TestClient):
    """Verify root / redirects to /docs."""
    response = client.get("/", follow_redirects=False)
    assert response.status_code in (301, 302, 307, 308)
    assert response.headers["location"] == "/docs"


def test_cors_headers(client: TestClient):
    """Verify CORS middleware returns correct allow-origin headers."""
    response = client.options(
        "/api/v1/health",
        headers={
            "Origin": "http://localhost:3002",
            "Access-Control-Request-Method": "GET",
        },
    )
    assert response.status_code == 200
    assert response.headers.get("access-control-allow-origin") == "http://localhost:3002"


def test_404_error_handling(client: TestClient):
    """Verify centralized exception handler catches non-existent routes with structured JSON."""
    response = client.get("/api/v1/unmapped-endpoint-xyz")
    assert response.status_code == 404

    data = response.json()
    assert data["success"] is False
    assert "error" in data
    assert data["error"]["code"] == "HTTPException"

