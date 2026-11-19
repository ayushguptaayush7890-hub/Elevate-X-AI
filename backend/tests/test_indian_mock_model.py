"""
ELEVATE X AI — FEATURE 1 PHASE 2: EXTENDED INTEGRATION AND MULTILINGUAL REGRESSION TEST SUITE

Tests:
1. Multilingual Extraction across 5 linguistic modes (Devanagari, Roman Hindi, Hinglish, English, Mixed-script).
2. All 10 occupations coverage (TRD-01 to TRD-10).
3. Offset slicing invariant: assert input_text[start:end] == extracted_skill.
4. Functional skill category assignment across the 8 taxonomy classes.
5. Unmapped skill handling (similarity < 0.65 flags human_review_required: true).
6. Provenance and safety gate lock integrity.
"""

import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

OCCUPATION_TEST_CASES = [
    {
        "trade_id": "TRD-01",
        "lang": "hi_deva",
        "text": "हम कटोरी ब्लाउज की डार्ट सिलाई और ओवरलॉक फिनिशिंग करते हैं।"
    },
    {
        "trade_id": "TRD-02",
        "lang": "hi_latn",
        "text": "Main concealed conduit wiring aur MCB distribution board installation karta hu."
    },
    {
        "trade_id": "TRD-03",
        "lang": "hinglish",
        "text": "Bathroom me CPVC pipe solvent welding aur submersible pump repair ka kaam kiya."
    },
    {
        "trade_id": "TRD-04",
        "lang": "mixed",
        "text": "Car engine me brake pad replacement aur carburetor cleaning ki जांच करते हैं।"
    },
    {
        "trade_id": "TRD-05",
        "lang": "en",
        "text": "I perform teak wood mortise and tenon joint framing and laminate edge trimming."
    },
    {
        "trade_id": "TRD-06",
        "lang": "hi_deva",
        "text": "कार्यशाला में शील्ड मेटल आर्क वेल्डिंग और ग्राइंडिंग फिनिशिंग का काम करते हैं।"
    },
    {
        "trade_id": "TRD-07",
        "lang": "hi_latn",
        "text": "Hum cement mortar mixing aur 9 inch brick wall masonry karte hain."
    },
    {
        "trade_id": "TRD-08",
        "lang": "hinglish",
        "text": "Wall putty application aur emulsion paint roller application karte hain."
    },
    {
        "trade_id": "TRD-09",
        "lang": "mixed",
        "text": "Khet me drip irrigation lateral line laying aur tractor disc harrow chalate hain."
    },
    {
        "trade_id": "TRD-10",
        "lang": "en",
        "text": "I handle smartphone SMD component desoldering and cracked AMOLED display replacement."
    }
]

@pytest.mark.asyncio
async def test_extraction_status_metadata():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        res = await ac.get("/api/v1/skills/extract/status")
        assert res.status_code == 200
        data = res.json()
        assert data["status"] == "operational"
        assert data["genuine_worker_records"] == 0
        assert data["minimum_required_records"] == 500
        assert "LOCKED" in data["training_safety_gate"]
        assert data["supported_occupations_count"] == 10


@pytest.mark.asyncio
async def test_extraction_across_all_ten_occupations_and_languages():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        for case in OCCUPATION_TEST_CASES:
            payload = {
                "text": case["text"],
                "occupation_hint": case["trade_id"]
            }
            res = await ac.post("/api/v1/skills/extract", json=payload)
            assert res.status_code == 200, f"Failed for {case['trade_id']}: {res.text}"
            data = res.json()
            assert data["detected_occupation"]["occupation_id"] == case["trade_id"]
            assert data["extracted_skills_count"] >= 1, f"No skills extracted for {case['trade_id']}"

            # Strict character offset invariant verification
            for s in data["extracted_skills"]:
                st, en = s["start_offset"], s["end_offset"]
                assert case["text"][st:en] == s["extracted_skill"], (
                    f"Offset invariant failed: '{case['text'][st:en]}' != '{s['extracted_skill']}'"
                )
                assert s["skill_category"] is not None
                assert s["category_confidence"] >= 0.0


@pytest.mark.asyncio
async def test_unmapped_skill_confidence_threshold_behavior():
    # Provide a fictional / non-standard task phrase that should fall below 0.65 canonical similarity
    novel_text = "Main interstellar hyperdrive quantum flux calibration karta hu workshop me."
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        res = await ac.post("/api/v1/skills/extract", json={"text": novel_text, "occupation_hint": "TRD-02"})
        assert res.status_code == 200
        data = res.json()
        for s in data["extracted_skills"]:
            if s.get("mapping_confidence", 0.0) < 0.65:
                assert s["canonical_skill"] is None or s["mapping_status"] == "unmapped"
                assert s["human_review_required"] is True


@pytest.mark.asyncio
async def test_empty_and_whitespace_error_handling():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        res = await ac.post("/api/v1/skills/extract", json={"text": ""})
        assert res.status_code == 422
        res2 = await ac.post("/api/v1/skills/extract", json={"text": "   \n\t  "})
        assert res2.status_code == 422

