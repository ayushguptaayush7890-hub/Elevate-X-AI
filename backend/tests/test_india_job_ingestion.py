"""
Tests for Elevate X AI India-First Job Ingestion, Role-Based Matching, and Data Quality.
Validates:
1. Authentic Indian Tech Corporate ATS Ingestion (MongoDB, Databricks, InMobi, Elastic, Rubrik, Okta, Samsara, Datadog).
2. India-first default API results (no foreign German dominance in India feed).
3. Location filtering: Country-wide (India) and City-level (Bengaluru, Delhi NCR, Gurugram, Noida).
4. Strict International separation: overseas/European jobs only appear under International filter.
5. Role-based matching (AI Engineer, Python Developer, Data Analyst).
6. Explainable AI compatibility metrics (match score, matching verified skills, skill gaps, experience fit).
7. Data provenance & application fidelity (genuine employer links, direct ATS URLs).
"""

import pytest
from datetime import date
from sqlalchemy import select, func, or_
from fastapi.testclient import TestClient

from app.main import app
from app.core.database import SessionLocal
from app.models.job import JobListing, Employer
from app.services.job_aggregator.adapters import AuthorizedEmployerCareerFeedsAdapter
from app.services.job_aggregator.aggregator_service import JobAggregatorService
from app.services.job_matching_service import JobMatchingService


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c


def test_1_authorized_feeds_ingests_authentic_indian_tech_jobs():
    """Verify AuthorizedEmployerCareerFeedsAdapter ingests genuine India tech center vacancies."""
    adapter = AuthorizedEmployerCareerFeedsAdapter()
    jobs = adapter.fetch_jobs(location="India", limit=30)
    assert len(jobs) > 0, "Must fetch genuine Indian tech jobs"

    indian_cities = ["bengaluru", "bangalore", "delhi", "gurugram", "gurgaon", "noida", "mumbai", "pune", "hyderabad", "india"]
    for j in jobs:
        assert j.country == "India", f"Expected country 'India', got '{j.country}' for job {j.title}"
        assert any(city in j.location.lower() for city in indian_cities), f"Location '{j.location}' must be an Indian tech hub"
        assert j.source_url.startswith("http"), "Must have valid genuine external source URL"
        assert j.application_url.startswith("http"), "Must have valid genuine application URL"
        assert j.employer_name in ["MongoDB", "Databricks", "InMobi", "Elastic", "Rubrik", "Okta", "Samsara", "Datadog", "Verified Employer"]


def test_2_api_defaults_to_india_jobs(client):
    """Verify GET /api/v1/jobs defaults to Indian opportunities without foreign German dominance."""
    resp = client.get("/api/v1/jobs")
    assert resp.status_code == 200
    jobs = resp.json()
    assert len(jobs) > 0, "Default query must return active vacancies"

    for j in jobs:
        assert j["country"] == "India", f"Default feed must be India-first; encountered country '{j['country']}' ({j['title']})"
        # Verify Berlin, Munich, Hamburg do not appear in India results
        assert "berlin" not in j["location"].lower(), "German cities must not appear in India default feed"
        assert "munich" not in j["location"].lower(), "German cities must not appear in India default feed"
        assert "hamburg" not in j["location"].lower(), "German cities must not appear in India default feed"


def test_3_city_level_filtering_bengaluru_and_delhi_ncr(client):
    """Verify city-level filtering for Bengaluru and Delhi NCR hubs."""
    # 1. Bengaluru
    resp_blr = client.get("/api/v1/jobs?location=Bengaluru")
    assert resp_blr.status_code == 200
    blr_jobs = resp_blr.json()
    assert len(blr_jobs) > 0, "Must return Bengaluru jobs"
    for j in blr_jobs:
        assert j["country"] == "India"
        assert "bengaluru" in j["location"].lower() or "bangalore" in j["location"].lower()

    # 2. Delhi NCR
    resp_ncr = client.get("/api/v1/jobs?location=Delhi%20NCR")
    assert resp_ncr.status_code == 200
    ncr_jobs = resp_ncr.json()
    assert len(ncr_jobs) > 0, "Must return Delhi NCR jobs"
    ncr_tokens = ["delhi", "ncr", "noida", "gurugram", "gurgaon", "meerut"]
    for j in ncr_jobs:
        assert j["country"] == "India"
        assert any(t in j["location"].lower() for t in ncr_tokens)


def test_4_international_filter_isolates_overseas_vacancies(client):
    """Verify International filter returns overseas listings without polluting Indian feed."""
    resp = client.get("/api/v1/jobs?location=International")
    assert resp.status_code == 200
    intl_jobs = resp.json()
    assert len(intl_jobs) > 0, "International filter must return overseas listings"

    for j in intl_jobs:
        assert j["country"] == "International", f"Expected country 'International', got '{j['country']}'"


def test_5_role_category_search_ai_and_python(client):
    """Verify role-based search filters for AI Engineer and Python Developer roles."""
    # 1. AI Engineer
    resp_ai = client.get("/api/v1/jobs?role_category=AI%20Engineer")
    assert resp_ai.status_code == 200
    ai_jobs = resp_ai.json()
    assert len(ai_jobs) > 0, "Must find real AI-related tech jobs in India"
    for j in ai_jobs:
        text = (j["title"] + " " + " ".join(j.get("required_skills_list", []))).lower()
        assert any(k in text for k in ["ai", "machine learning", "ml", "data"]), f"Job {j['title']} must match AI category"

    # 2. Python Developer
    resp_py = client.get("/api/v1/jobs?role_category=Python%20Developer")
    assert resp_py.status_code == 200
    py_jobs = resp_py.json()
    assert len(py_jobs) > 0, "Must find real Python-related jobs in India"


def test_6_explainable_ai_matching_breakdown(client):
    """Verify explainable AI matching returns dynamic match score, matching skills, and missing skills."""
    resp = client.get("/api/v1/jobs?limit=5")
    assert resp.status_code == 200
    jobs = resp.json()
    assert len(jobs) > 0

    sample = jobs[0]
    match = sample.get("match_details")
    assert match is not None, "Job response must include explainable AI match details"
    assert "match_score" in match
    assert 0 <= match["match_score"] <= 100
    assert "matching_verified_skills" in match
    assert "missing_required_skills" in match
    assert "experience_fit" in match
    assert isinstance(match["matching_verified_skills"], list)
    assert isinstance(match["missing_required_skills"], list)


def test_7_transparent_empty_state_for_narrow_queries(client):
    """Verify that impossible query combinations return empty list and do not substitute German jobs."""
    resp = client.get("/api/v1/jobs?search=NonExistentSpecialtyTradeXyz12345&location=Bengaluru")
    assert resp.status_code == 200
    jobs = resp.json()
    assert len(jobs) == 0, "Must return empty array on zero matches; never silently inject German listings"


def test_8_direct_application_url_fidelity(client):
    """Verify direct external application URLs are authentic and point to genuine portals."""
    resp = client.get("/api/v1/jobs?limit=10")
    assert resp.status_code == 200
    jobs = resp.json()

    for j in jobs:
        apply_url = j.get("application_url") or j.get("source_url")
        assert apply_url is not None
        assert apply_url.startswith("http://") or apply_url.startswith("https://")
        # Ensure it does not point to internal fake submission endpoints
        assert "/api/v1/applications/fake" not in apply_url
