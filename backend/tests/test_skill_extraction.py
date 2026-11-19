"""
Tests for AI Skill Extraction API endpoints:
- GET /api/v1/skills/extract/status
- POST /api/v1/skills/extract
"""

import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.mark.asyncio
async def test_get_skill_extraction_status():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/api/v1/skills/extract/status")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "operational"
        assert data["active_model"].startswith("xlm_roberta")
        assert "LOCKED" in data["training_safety_gate"]
        assert data["genuine_worker_records"] == 0
        assert data["minimum_required_records"] == 500
        assert data["supported_occupations_count"] == 10
        assert data["canonical_catalogue_size"] == 32

@pytest.mark.asyncio
async def test_post_skill_extract_hinglish_narrative():
    payload = {
        "text": "Main kapde ki cutting karta hu aur customer ke measurement ke according suit silta hu.",
        "occupation_hint": "TRD-01"
    }
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/api/v1/skills/extract", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["input_text"] == payload["text"]
        assert data["detected_occupation"]["occupation_id"] == "TRD-01"
        assert data["detected_occupation"]["occupation_title"] == "Tailor and Garment Worker"
        assert data["extracted_skills_count"] >= 1
        
        # Test character offset integrity on all extracted spans
        text = payload["text"]
        for span in data["extracted_skills"]:
            st = span["start_offset"]
            en = span["end_offset"]
            assert text[st:en] == span["extracted_skill"], f"Offset mismatch: '{text[st:en]}' != '{span['extracted_skill']}'"
            assert span["skill_category"] is not None
            assert "crosswalks" in span

@pytest.mark.asyncio
async def test_post_skill_extract_english_technical():
    payload = {
        "text": "I install concealed PVC electrical conduits and wire miniature circuit breaker distribution boards."
    }
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/api/v1/skills/extract", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["detected_occupation"]["occupation_id"] == "TRD-02"
        assert data["extracted_skills_count"] >= 1
        assert data["metadata"]["training_safety_gate_status"].startswith("LOCKED")

@pytest.mark.asyncio
async def test_post_skill_extract_empty_payload_validation():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/api/v1/skills/extract", json={"text": "   "})
        assert response.status_code == 422

