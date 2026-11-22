"""
Regression and Integration Tests for Career Transitions Endpoints:
Verifies public occupation search, details, recommendations, analysis, and auth protection on goal adoption.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_public_search_occupations_no_auth():
    """Verify that search_occupations is accessible without authentication token."""
    response = client.get("/api/v1/career-transitions/occupations?q=software&limit=5")
    assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    first = data[0]
    assert "title" in first
    assert "source" in first
    assert "canonical_id" in first


def test_public_search_occupations_empty_query():
    """Verify that search_occupations returns default top occupations on empty query."""
    response = client.get("/api/v1/career-transitions/occupations?limit=5")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_public_recommendations_no_auth():
    """Verify that transition recommendations can be computed for guest users."""
    response = client.post(
        "/api/v1/career-transitions/recommendations",
        json={
            "current_occupation": "Software Developer",
            "candidate_skills": ["Python", "Algorithms", "Git"],
            "limit": 3,
        },
    )
    assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
    data = response.json()
    assert isinstance(data, list)
    if len(data) > 0:
        first = data[0]
        assert "target_title" in first
        assert "fit_percentage" in first
        assert "salary_range" in first


def test_public_analyze_no_auth():
    """Verify that transition analysis can be performed for guest users."""
    response = client.post(
        "/api/v1/career-transitions/analyze",
        json={
            "from_occupation": "Software Developer",
            "to_occupation": "Data Scientist",
            "candidate_skills": ["Python", "SQL"],
        },
    )
    assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
    data = response.json()
    assert "from_occupation_title" in data
    assert "to_occupation_title" in data
    assert "fit_percentage" in data
    assert "transferable_competencies" in data
    assert "bridgeable_competencies" in data


def test_adopt_goal_requires_authentication():
    """Verify that adopting a career goal strictly requires authentication."""
    response = client.post(
        "/api/v1/career-transitions/adopt-goal",
        json={
            "origin_occupation": "Software Developer",
            "destination_occupation": "Data Scientist",
            "fit_percentage": 78,
            "target_timeline_months": 6,
        },
    )
    assert response.status_code == 401
