"""
ELEVATE X AI — FEATURE 1: EXPERIENCE RECOGNITION REGRESSION TEST SUITE
Guarantees:
1. Electrician input never returns unrelated tailor or garment skills.
2. Tailor input returns garment skills and Tailor occupation.
3. Plumber input returns plumbing skills and Plumber occupation.
4. Motor mechanic input returns automotive repair skills.
5. Every extracted span strictly satisfies the verbatim character slicing invariant: text[start:end] == extracted_skill.
6. Detected occupations correctly separate trades and avoid cross-contamination.
"""

import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

TAILOR_SPECIFIC_KEYWORDS = {
    "tailor", "silai", "kapda", "fabric", "overlock", "needle", "suit", "shirt", 
    "blouse", "dart", "bakram", "cutting blouse", "sewing machine"
}

ELECTRICIAN_SPECIFIC_KEYWORDS = {
    "electrician", "wiring", "mcb", "multimeter", "electrical faults", "distribution board", "conduit"
}

PLUMBER_SPECIFIC_KEYWORDS = {
    "plumber", "cpvc", "pipe", "solvent cement", "leakage", "fittings", "drainage"
}

@pytest.mark.asyncio
async def test_canonical_mapping_quality_audit_suspicious_cases():
    """
    Specifically verify that:
    1. 'CPVC pipe cutting' is NOT mapped to 'CPVC Pipe Solvent Cement Jointing' (must be unmapped).
    2. 'leakage repair' is NOT mapped to 'Flush Cistern Float Valve Inspection and Leak Testing' (must be unmapped).
    3. 'engine repair' is NOT mapped to 'Motorcycle Engine Oil Drain and Replacement' (must be unmapped).
    4. 'spark plug gap check' is correctly UNMAPPED (no equivalent in 32 catalogue).
    5. Valid counterparts DO map accurately:
       - 'solvent cement' -> 'CPVC Pipe Solvent Cement Jointing'
       - 'engine oil change' -> 'Motorcycle Engine Oil Drain and Replacement'
    """
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # Plumber test: CPVC pipe cutting vs solvent cement vs leakage repair
        res_plm = await ac.post(
            "/api/v1/skills/extract",
            json={"text": "Main CPVC pipe cutting karta hu, solvent cement lagata hu aur leakage repair karta hu."}
        )
        assert res_plm.status_code == 200
        plm_data = res_plm.json()
        spans_by_phrase = {s["extracted_skill"]: s for s in plm_data["extracted_skills"]}
        
        # 1. CPVC pipe cutting must be unmapped (cutting is prep, not chemical solvent jointing)
        assert "CPVC pipe cutting" in spans_by_phrase
        assert spans_by_phrase["CPVC pipe cutting"]["canonical_skill"] is None
        assert spans_by_phrase["CPVC pipe cutting"]["mapping_status"] == "unmapped"
        assert spans_by_phrase["CPVC pipe cutting"]["human_review_required"] is True
        
        # 2. Solvent cement MUST be mapped to SKL-PLM-001
        assert "solvent cement" in spans_by_phrase
        assert spans_by_phrase["solvent cement"]["canonical_skill"] == "CPVC Pipe Solvent Cement Jointing"
        assert spans_by_phrase["solvent cement"]["canonical_skill_id"] == "SKL-PLM-001"
        assert spans_by_phrase["solvent cement"]["mapping_status"] == "mapped"
        
        # 3. Leakage repair must be unmapped (general leak is not flush cistern valve)
        assert "leakage repair" in spans_by_phrase
        assert spans_by_phrase["leakage repair"]["canonical_skill"] is None
        assert spans_by_phrase["leakage repair"]["mapping_status"] == "unmapped"
        assert spans_by_phrase["leakage repair"]["human_review_required"] is True

        # Mechanic test: engine repair vs spark plug gap check vs engine oil change
        res_mec = await ac.post(
            "/api/v1/skills/extract",
            json={"text": "Main bike ka engine repair karta hu, spark plug gap check karta hu aur engine oil change karta hu."}
        )
        assert res_mec.status_code == 200
        mec_data = res_mec.json()
        mec_spans = {s["extracted_skill"]: s for s in mec_data["extracted_skills"]}
        
        # 4. Engine repair must be unmapped (engine overhaul is not oil drain/replacement)
        assert "engine repair" in mec_spans
        assert mec_spans["engine repair"]["canonical_skill"] is None
        assert mec_spans["engine repair"]["mapping_status"] == "unmapped"
        assert mec_spans["engine repair"]["human_review_required"] is True
        
        # 5. Spark plug gap check must be unmapped (not in 32 catalogue)
        assert "spark plug gap check" in mec_spans
        assert mec_spans["spark plug gap check"]["canonical_skill"] is None
        assert mec_spans["spark plug gap check"]["mapping_status"] == "unmapped"
        assert mec_spans["spark plug gap check"]["human_review_required"] is True
        
        # 6. Oil change / Engine oil change MUST be mapped to SKL-MEC-001
        oil_key = "engine oil change" if "engine oil change" in mec_spans else "oil change"
        assert oil_key in mec_spans
        assert mec_spans[oil_key]["canonical_skill"] == "Motorcycle Engine Oil Drain and Replacement"
        assert mec_spans[oil_key]["canonical_skill_id"] == "SKL-MEC-001"
        assert mec_spans[oil_key]["mapping_status"] == "mapped"


@pytest.mark.asyncio
async def test_electrician_quality_refinement_and_generic_pruning():
    """
    Verify that electrician input:
    1. Prunes standalone generic words ('electrician', standalone 'check', 'kaam', 'repair').
    2. Groups compound tasks ('MCB install', 'electrical faults check').
    3. Provides normalized competency names and exact evidence text.
    4. Slices text verbatim with exact character offsets.
    """
    electrician_text = "Main electrician ka kaam karta hu. Gharon mein wiring karta hu, MCB install karta hu aur multimeter se electrical faults check karta hu."
    
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/api/v1/skills/extract", json={"text": electrician_text})
        assert response.status_code == 200
        data = response.json()
        
        extracted_phrases = [s["extracted_skill"] for s in data["extracted_skills"]]
        normalized_names = [s.get("normalized_skill") for s in data["extracted_skills"]]
        
        # 1. Standalone disallowed words MUST NOT appear as standalone competencies
        assert "electrician" not in extracted_phrases, "Occupation title 'electrician' should not be extracted as a skill"
        assert "check" not in extracted_phrases, "Isolated verb 'check' should not be extracted without object"
        assert "kaam" not in extracted_phrases, "Generic word 'kaam' should not be extracted"
        
        # 2. Compound tasks and normalized names
        assert "wiring" in extracted_phrases
        assert "MCB install" in extracted_phrases
        assert "multimeter" in extracted_phrases
        assert "electrical faults check" in extracted_phrases
        
        assert "Electrical Wiring Installation" in normalized_names
        assert "MCB Installation" in normalized_names
        assert "Multimeter Operation" in normalized_names
        assert "Electrical Fault Diagnosis & Checking" in normalized_names
        
        # 3. Verbatim evidence text and character slicing
        for span in data["extracted_skills"]:
            st = span["start_offset"]
            en = span["end_offset"]
            ex = span["extracted_skill"]
            ev = span["evidence_text"]
            assert electrician_text[st:en] == ex, f"Character slice mismatch: '{electrician_text[st:en]}' != '{ex}'"
            assert ev == ex, f"Evidence text mismatch: '{ev}' != '{ex}'"
            assert span["normalized_skill"] is not None


@pytest.mark.asyncio
async def test_unmapped_threshold_gating():
    """Verify that skills with confidence < 0.65 are marked unmapped and require human review."""
    vague_text = "Main factory me random kaam karta hu."
    
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/api/v1/skills/extract", json={"text": vague_text})
        assert response.status_code == 200
        data = response.json()
        
        for span in data["extracted_skills"]:
            if span["mapping_confidence"] < 0.65:
                assert span["canonical_skill"] is None
                assert span["canonical_skill_id"] is None
                assert span["mapping_status"] == "unmapped"
                assert span["is_unmapped_skill"] is True
                assert span["human_review_required"] is True


@pytest.mark.asyncio
async def test_electrician_never_returns_tailor_skills():
    """Verify that electrician input never returns tailor or garment skills."""
    electrician_text = "Main electrician ka kaam karta hu. Gharon mein wiring karta hu, MCB install karta hu aur multimeter se electrical faults check karta hu."
    
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/api/v1/skills/extract", json={"text": electrician_text})
        assert response.status_code == 200
        data = response.json()
        
        # 1. Occupation must be Electrician (TRD-02)
        assert data["detected_occupation"]["occupation_id"] == "TRD-02"
        assert "Electrician" in data["detected_occupation"]["occupation_title"]
        assert "Tailor" not in data["detected_occupation"]["occupation_title"]
        
        # 2. None of the extracted skills should be garment/tailor specific
        extracted_skills = [s["extracted_skill"].lower() for s in data["extracted_skills"]]
        for skill in extracted_skills:
            assert "tailor" not in skill, f"Tailor skill '{skill}' incorrectly extracted from electrician testimony"
            assert "blouse" not in skill, f"Blouse skill '{skill}' incorrectly extracted from electrician testimony"
            assert "sewing" not in skill, f"Sewing skill '{skill}' incorrectly extracted from electrician testimony"
            
        # 3. Relevant electrical skills must be present
        assert any(e in extracted_skills for e in ["wiring", "mcb", "multimeter", "check", "electrician"]), \
            f"Expected electrical skills, got: {extracted_skills}"
            
        # 4. Strict slicing invariant on 100% of spans
        for span in data["extracted_skills"]:
            st = span["start_offset"]
            en = span["end_offset"]
            assert electrician_text[st:en] == span["extracted_skill"], \
                f"Slicing invariant failed: '{electrician_text[st:en]}' != '{span['extracted_skill']}'"

@pytest.mark.asyncio
async def test_tailor_returns_garment_skills():
    """Verify that tailor input returns relevant garment skills and TRD-01 occupation."""
    tailor_text = "Main kapde ki cutting karta hu, customer ke measurement leta hu aur sewing machine se suit silta hu."
    
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/api/v1/skills/extract", json={"text": tailor_text})
        assert response.status_code == 200
        data = response.json()
        
        assert data["detected_occupation"]["occupation_id"] == "TRD-01"
        assert "Tailor" in data["detected_occupation"]["occupation_title"]
        
        extracted_skills = [s["extracted_skill"].lower() for s in data["extracted_skills"]]
        assert any(k in " ".join(extracted_skills) for k in ["cutting", "measurement", "sewing", "suit", "silta"])
        
        for span in data["extracted_skills"]:
            st = span["start_offset"]
            en = span["end_offset"]
            assert tailor_text[st:en] == span["extracted_skill"]

@pytest.mark.asyncio
async def test_plumber_returns_plumbing_skills():
    """Verify that plumber input returns relevant plumbing skills and TRD-03 occupation."""
    plumber_text = "Main CPVC pipe cutting karta hu, solvent cement lagata hu aur leakage repair karta hu."
    
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/api/v1/skills/extract", json={"text": plumber_text})
        assert response.status_code == 200
        data = response.json()
        
        assert data["detected_occupation"]["occupation_id"] == "TRD-03"
        assert "Plumber" in data["detected_occupation"]["occupation_title"]
        
        extracted_skills = [s["extracted_skill"].lower() for s in data["extracted_skills"]]
        assert any(k in " ".join(extracted_skills) for k in ["cpvc", "pipe", "solvent", "cement", "leakage", "repair"])
        
        for span in data["extracted_skills"]:
            st = span["start_offset"]
            en = span["end_offset"]
            assert plumber_text[st:en] == span["extracted_skill"]

@pytest.mark.asyncio
async def test_motor_mechanic_returns_mechanic_skills():
    """Verify that motor mechanic input returns relevant automotive skills and TRD-04 occupation."""
    mechanic_text = "Main bike ka engine repair karta hu, spark plug gap check karta hu aur brake service karta hu."
    
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/api/v1/skills/extract", json={"text": mechanic_text})
        assert response.status_code == 200
        data = response.json()
        
        assert data["detected_occupation"]["occupation_id"] == "TRD-04"
        assert "Motor Mechanic" in data["detected_occupation"]["occupation_title"]
        
        extracted_skills = [s["extracted_skill"].lower() for s in data["extracted_skills"]]
        assert any(k in " ".join(extracted_skills) for k in ["engine", "repair", "spark plug", "brake"])
        
        for span in data["extracted_skills"]:
            st = span["start_offset"]
            en = span["end_offset"]
            assert mechanic_text[st:en] == span["extracted_skill"]

