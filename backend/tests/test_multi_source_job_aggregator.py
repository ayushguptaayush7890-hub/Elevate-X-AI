"""
Comprehensive Multi-Source Job Aggregator Test Suite.
Tests live ingestion, duplicate detection, URL preservation, explainable AI matching,
saved jobs bookmarks, provider telemetry, and multifaceted filtering.
"""

import os
import sys
import uuid
import json
import pytest
from datetime import date, datetime, timedelta
from sqlalchemy import select
from fastapi.testclient import TestClient

from app.main import app
from app.core.database import SessionLocal
from app.models.user import User
from app.models.job import Employer, JobListing, JobRequirement, AggregatorSyncLog
from app.models.application import SavedJob
from app.services.job_aggregator.aggregator_service import JobAggregatorService
from app.services.job_aggregator.adapters import (
    AuthorizedEmployerCareerFeedsAdapter,
    AdzunaAdapter,
    JoobleAdapter,
    NaukriAdapter,
    LinkedInJobsAdapter,
    IndeedAdapter,
    NationalCareerServiceAdapter,
)
from app.services.job_matching_service import JobMatchingService
from app.core.security import create_access_token


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c


def test_1_provider_metadata_and_documentation():
    """Verify all 12 providers have complete documentation and capability metadata."""
    aggregator = JobAggregatorService()
    db = SessionLocal()
    try:
        statuses = aggregator.get_all_provider_statuses(db)
        assert len(statuses) == 12, f"Must evaluate exactly 12 providers (got {len(statuses)})"

        provider_map = {p["provider_id"]: p for p in statuses}
        
        # Verify specific required providers
        assert "naukri" in provider_map
        assert "linkedin" in provider_map
        assert "indeed" in provider_map
        assert "internshala" in provider_map
        assert "foundit" in provider_map
        assert "apna" in provider_map
        assert "cutshort" in provider_map
        assert "adzuna" in provider_map
        assert "jooble" in provider_map
        assert "ncs" in provider_map
        assert "authorized_feeds" in provider_map
        assert "apify" in provider_map

        # Verify documentation fields
        for p in statuses:
            assert p["official_website"].startswith("http")
            assert isinstance(p["data_fields_available"], list)
            assert len(p["auth_requirements"]) > 5
            assert len(p["commercial_usage_permission"]) > 5

        # Verify unintegrated providers are NOT marked as active
        assert provider_map["naukri"]["status"] == "pending_partner_approval"
        assert provider_map["linkedin"]["status"] == "pending_partner_approval"
        assert provider_map["ncs"]["status"] == "pending_partner_approval"
        assert provider_map["authorized_feeds"]["status"] == "active"
    finally:
        db.close()


def test_2_authorized_feeds_real_ingestion():
    """Verify live fetching from Authorized Employer Career Feeds returns real vacancies."""
    adapter = AuthorizedEmployerCareerFeedsAdapter()
    jobs = adapter.fetch_jobs(limit=10)
    assert len(jobs) > 0, "Authorized feeds must return real live vacancies"

    # Verify real provenance and original URLs
    sample = jobs[0]
    assert sample.title is not None and len(sample.title) > 3
    assert sample.employer_name is not None and len(sample.employer_name) > 1
    assert sample.source_url.startswith("http"), "Original source URL must be valid HTTP/HTTPS"
    assert any(sp in sample.source_provider for sp in ["Authorized Feeds", "Arbeitnow", "RemoteOK", "Jobicy"])
    assert sample.listing_status == "active"
    print(f"\n[Test Evidence] Fetched real job: '{sample.title}' at '{sample.employer_name}' ({sample.source_provider})")
    print(f"  URL: {sample.source_url}")


def test_3_duplicate_detection_and_sync():
    """Verify synchronization deduplicates by (provider, provider_job_id) and source_url."""
    db = SessionLocal()
    try:
        aggregator = JobAggregatorService()
        initial_sync = aggregator.sync_active_providers(db, limit_per_source=15)
        assert initial_sync["total_fetched"] > 0
        imported_first_pass = initial_sync["total_imported"]

        # Run sync a second time immediately -> duplicate detection should update without creating duplicates
        second_sync = aggregator.sync_active_providers(db, limit_per_source=15)
        assert second_sync["total_updated"] >= imported_first_pass or second_sync["total_imported"] == 0
        print(f"\n[Test Evidence] Second sync duplicates prevented: {second_sync['total_updated']} updated, {second_sync['total_imported']} new")
    finally:
        db.close()


def test_4_original_url_preservation_and_application_link(client):
    """Verify every job card preserves genuine source URL and direct application URL."""
    resp = client.get("/api/v1/jobs?limit=5")
    assert resp.status_code == 200
    jobs = resp.json()
    assert len(jobs) > 0

    for job in jobs:
        assert job["source_url"] is not None and job["source_url"].startswith("http")
        assert job["application_url"] is not None and job["application_url"].startswith("http")
        assert any(sp in job["source_provider"] for sp in ["Authorized Feeds", "Arbeitnow", "RemoteOK", "Jobicy", "Adzuna", "Jooble", "Direct"])
        assert job["last_verified_at"] is not None


def test_5_ai_explainable_compatibility_matching():
    """Verify AI job matching computes explainable match scores and skill deltas."""
    db = SessionLocal()
    try:
        # Get demo user features
        features = JobMatchingService.get_candidate_profile_features(db)
        assert len(features["verified_skills"]) > 0

        # Query a real job from database
        job = db.execute(select(JobListing).where(JobListing.is_active == True)).scalars().first()
        assert job is not None

        match = JobMatchingService.calculate_compatibility(features, job)
        assert 0 <= match["match_score"] <= 100
        assert match["match_tier"] in ["Exceptional Match", "Strong Match", "Moderate Fit", "Developmental Opportunity"]
        assert isinstance(match["matching_verified_skills"], list)
        assert isinstance(match["missing_required_skills"], list)
        assert "Explainable" in match["matching_methodology"]

        print(f"\n[Test Evidence] AI Match Score: {match['match_score']}% ({match['match_tier']})")
        print(f"  Matching verified skills: {match['matching_verified_skills']}")
        print(f"  Missing bridge skills: {match['missing_required_skills']}")
        print(f"  Experience fit: {match['experience_fit']}")
    finally:
        db.close()


def test_6_multifaceted_filtering_endpoints(client):
    """Verify search, work mode, and provider filtering."""
    # Source filter
    resp_source = client.get("/api/v1/jobs?source=Arbeitnow")
    assert resp_source.status_code == 200
    for j in resp_source.json():
        assert j["source_provider"] == "Arbeitnow"

    # Work Mode filter
    resp_mode = client.get("/api/v1/jobs?work_mode=Remote")
    assert resp_mode.status_code == 200
    for j in resp_mode.json():
        assert j["work_mode"].lower() == "remote"

    # Search query
    resp_search = client.get("/api/v1/jobs?search=Engineer")
    assert resp_search.status_code == 200


def test_7_saved_jobs_bookmarking_lifecycle(client):
    """Verify saving/bookmarking a job and retrieving user saved list."""
    db = SessionLocal()
    try:
        user = db.execute(select(User).where(User.email == "live.demo@elevatex.ai")).scalar_one_or_none()
        assert user is not None
        token = create_access_token(subject=str(user.id))

        # Pick a job
        job = db.execute(select(JobListing).where(JobListing.is_active == True)).scalars().first()
        assert job is not None
        job_id = str(job.id)

        # Clear existing save for idempotency
        db.query(SavedJob).filter(SavedJob.user_id == user.id, SavedJob.job_id == job.id).delete()
        db.commit()

        # 1. Bookmark job
        save_res = client.post(
            f"/api/v1/jobs/{job_id}/save",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert save_res.status_code == 200
        assert save_res.json()["saved"] is True

        # 2. Get my saved jobs
        my_saved = client.get(
            "/api/v1/jobs/saved/my",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert my_saved.status_code == 200
        saved_list = my_saved.json()
        assert any(j["id"] == job_id for j in saved_list)

        # 3. Toggle off
        unsave_res = client.post(
            f"/api/v1/jobs/{job_id}/save",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert unsave_res.status_code == 200
        assert unsave_res.json()["saved"] is False
    finally:
        db.close()


def test_8_expired_listing_cleanup():
    """Verify that jobs with expired dates are marked inactive."""
    db = SessionLocal()
    try:
        # Create a mock expired job
        employer = db.execute(select(Employer)).scalars().first()
        expired_job = JobListing(
            employer_id=employer.id,
            title="Expired Legacy Role",
            location="Bangalore",
            description="Testing expiration cleanup",
            source_provider="Direct",
            source_url="https://example.com/expired",
            expiry_date=date.today() - timedelta(days=2),
            is_active=True,
            listing_status="active",
        )
        db.add(expired_job)
        db.commit()
        expired_id = expired_job.id

        # Run cleanup
        cleaned = JobAggregatorService.cleanup_expired_jobs(db)
        assert cleaned >= 1

        # Check status
        refreshed = db.execute(select(JobListing).where(JobListing.id == expired_id)).scalar_one()
        assert refreshed.is_active is False
        assert refreshed.listing_status == "expired"

        # Cleanup
        db.delete(refreshed)
        db.commit()
    finally:
        db.close()
