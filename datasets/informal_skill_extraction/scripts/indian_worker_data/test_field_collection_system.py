#!/usr/bin/env python3
"""
ELEVATE X AI — FIELD WORKER DATA COLLECTION SYSTEM TEST SUITE
Verifies all functional and ethical invariants of the Phase 1 collection platform:
1. Web Console HTML loads properly.
2. Taxonomy & 4-Trade Configuration returns correctly.
3. Draft creation, retrieval, and deletion in interim workspace.
4. DPDP Act 2023 consent validation gate (blocks submission if text consent missing).
5. Character offset exactness gate (blocks submission if text[start:end] != extracted_skill).
6. Multi-task description ingestion with valid offsets.
7. Record annotation & workflow lifecycle (transcribed -> annotated -> reviewed -> approved).
8. JSONL and CSV stream exports.
9. Live Quality Audit detection.
10. Partition Isolation: Confirms test records are cleaned up, leaving ZERO fake records in genuine partition!
"""

import sys
import json
from pathlib import Path
from starlette.testclient import TestClient

BASE_DIR = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(BASE_DIR))

from datasets.informal_skill_extraction.scripts.indian_worker_data.collection_dashboard import (
    app, REAL_DATA_DIR, DRAFTS_DIR, PHASE1_OCCUPATIONS, get_genuine_records
)

def run_collection_system_tests():
    print("=" * 65)
    print("ELEVATE X AI — FIELD DATA COLLECTION SYSTEM TEST SUITE")
    print("=" * 65)

    client = TestClient(app)

    # 1. Test Console UI Serving
    print("[Test 1] Testing Web Console HTML Endpoint...")
    res = client.get("/")
    assert res.status_code == 200, f"Expected 200, got {res.status_code}"
    assert "ELEVATE X AI" in res.text
    assert "Phase 1: 100 Real Worker Pilot Field Station" in res.text
    assert "DPDP Act 2023" in res.text
    print("  ✓ PASS: Web Console HTML5 UI serves successfully.")

    # 2. Test Taxonomy Endpoint
    print("[Test 2] Testing Taxonomy & Four-Trade Configuration...")
    res = client.get("/api/taxonomy")
    assert res.status_code == 200
    data = res.json()
    assert "TRD-01" in data["occupations"]
    assert "TRD-02" in data["occupations"]
    assert "TRD-03" in data["occupations"]
    assert "TRD-04" in data["occupations"]
    assert len(data["canonical_skills"]) >= 32
    print(f"  ✓ PASS: 4 Target Occupations and {len(data['canonical_skills'])} Canonical Skills verified.")

    # 3. Test Overview Endpoint
    print("[Test 3] Testing Overview Metrics...")
    res = client.get("/api/overview")
    assert res.status_code == 200
    overview = res.json()
    assert overview["target_total_workers"] == 100
    print(f"  ✓ PASS: Overview returned (Target: {overview['target_total_workers']}, Actual Genuine: {overview['total_genuine_workers']}).")

    # 4. Test Draft Management
    print("[Test 4] Testing Draft Workspace Management...")
    draft_worker_id = "WRK-TEST-PILOT-DRAFT-999"
    draft_payload = {
        "worker_id": draft_worker_id,
        "occupation_id": "TRD-01",
        "region": "Karol Bagh Delhi",
        "experience_years": 4.5,
        "work_context": "micro_workshop",
        "original_language": "hinglish",
        "script_type": "latin",
        "tasks": [{"task_id": "TSK-01", "description": "Drafting unfinished task..."}],
        "consent_text_confirmed": False
    }
    # Save draft
    res = client.post("/api/draft", json=draft_payload)
    assert res.status_code == 200
    draft_file = DRAFTS_DIR / f"{draft_worker_id}_draft.json"
    assert draft_file.exists(), "Draft file should exist on disk."

    # List drafts
    res = client.get("/api/drafts")
    assert res.status_code == 200
    drafts = res.json()
    assert any(d["worker_id"] == draft_worker_id for d in drafts)

    # Delete draft
    res = client.delete(f"/api/drafts/{draft_worker_id}")
    assert res.status_code == 200
    assert not draft_file.exists(), "Draft file should be deleted."
    print("  ✓ PASS: Draft creation, disk storage, listing, and deletion passed.")

    # 5. Test Consent Gate Enforcement
    print("[Test 5] Testing DPDP Act 2023 Consent Enforcement Gate...")
    no_consent_payload = {
        "worker_id": "WRK-TEST-NOCONSENT-001",
        "occupation_id": "TRD-02",
        "region": "Mayapuri Delhi",
        "experience_years": 6.0,
        "work_context": "independent_repair_shop",
        "original_language": "hindi",
        "script_type": "devanagari",
        "tasks": [{"task_id": "TSK-01", "description": "हम एमसीबी बॉक्स लगाते हैं।"}],
        "consent_text_confirmed": False  # VIOLATION: NO CONSENT
    }
    res = client.post("/api/interview/submit", json=no_consent_payload)
    assert res.status_code == 400, "Submission without consent MUST fail with HTTP 400."
    assert "DPDP Consent Required" in res.json()["detail"]
    print("  ✓ PASS: Mandatory DPDP consent gate successfully blocked non-consented interview.")

    # 6. Test Character Offset Validation Enforcement
    print("[Test 6] Testing Verbatim Character Offset Verification Gate...")
    bad_offset_payload = {
        "worker_id": "WRK-TEST-BAD-OFFSET-001",
        "occupation_id": "TRD-03",
        "region": "Karol Bagh Delhi",
        "experience_years": 3.0,
        "work_context": "customer_site",
        "original_language": "hinglish",
        "script_type": "latin",
        "consent_text_confirmed": True,
        "tasks": [{
            "task_id": "TSK-01",
            "description": "Main CPVC pipe mein solvent lagakar fitting karta hu.",
            "skill_spans": [{
                "span_id": "SP-01",
                "extracted_skill": "WRONG_SPAN_TEXT",  # Mismatch with text[0:15]
                "start_offset": 0,
                "end_offset": 15,
                "skill_category": "technical_tactile",
                "canonical_skill": "CPVC Pipe Solvent Cement Jointing"
            }]
        }]
    }
    res = client.post("/api/interview/submit", json=bad_offset_payload)
    assert res.status_code == 400, "Submission with invalid offset slice MUST fail with HTTP 400."
    assert "offset mismatch" in res.json()["detail"].lower()
    print("  ✓ PASS: Verbatim character slice mismatch correctly rejected with HTTP 400.")

    # 7. Test Multi-Task Submission & Lifecycle with Test Fixture
    print("[Test 7] Testing Multi-Task Submission & Lifecycle Ingestion...")
    fixture_worker_id = "WRK-TEST-FIXTURE-PILOT-01"
    desc1 = "Main inch tape se naap lekar fabric cutting karta hu."
    sub1 = "inch tape se naap lekar fabric cutting"
    st1 = desc1.find(sub1)
    en1 = st1 + len(sub1)

    desc2 = "Overlock machine se kinari band karke silai pack karta hu."
    sub2 = "Overlock machine se kinari band karke silai"
    st2 = desc2.find(sub2)
    en2 = st2 + len(sub2)

    valid_payload = {
        "worker_id": fixture_worker_id,
        "occupation_id": "TRD-01",
        "region": "Karol Bagh Delhi",
        "experience_years": 5.0,
        "work_context": "micro_workshop",
        "original_language": "hinglish",
        "script_type": "latin",
        "consent_text_confirmed": True,
        "tasks": [
            {
                "task_id": "TSK-01",
                "description": desc1,
                "skill_spans": [{
                    "span_id": "SP-01",
                    "extracted_skill": sub1,
                    "start_offset": st1,
                    "end_offset": en1,
                    "skill_category": "measurement_planning",
                    "canonical_skill": "Garment Pattern Measurement and Fabric Cutting"
                }]
            },
            {
                "task_id": "TSK-02",
                "description": desc2,
                "skill_spans": [{
                    "span_id": "SP-01",
                    "extracted_skill": sub2,
                    "start_offset": st2,
                    "end_offset": en2,
                    "skill_category": "tool_operation",
                    "canonical_skill": "Overlock Seam Edging and Finishing"
                }]
            }
        ]
    }

    res = client.post("/api/interview/submit", json=valid_payload)
    assert res.status_code == 200, f"Submission failed: {res.text}"
    created_records = res.json()["records"]
    assert len(created_records) == 2
    rec1_id = created_records[0]["record_id"]
    rec2_id = created_records[1]["record_id"]
    print(f"  ✓ Ingested 2 tasks for {fixture_worker_id}: {rec1_id}, {rec2_id}")

    # 8. Test Export JSONL and CSV
    print("[Test 8] Testing Batch Stream Exports...")
    res_jsonl = client.get("/api/export/jsonl")
    assert res_jsonl.status_code == 200
    assert rec1_id in res_jsonl.text

    res_csv = client.get("/api/export/csv")
    assert res_csv.status_code == 200
    assert rec1_id in res_csv.text
    print("  ✓ PASS: JSONL and CSV stream exports validated.")

    # 9. Test In-App Annotation & Status Update
    print("[Test 9] Testing In-App Annotation Update & Review Workflow...")
    # Add an additional span to rec1
    new_sub = "naap lekar"
    new_st = desc1.find(new_sub)
    new_en = new_st + len(new_sub)
    new_spans = [
        {
            "span_id": "SP-01",
            "extracted_skill": sub1,
            "start_offset": st1,
            "end_offset": en1,
            "skill_category": "measurement_planning",
            "canonical_skill": "Garment Pattern Measurement and Fabric Cutting"
        },
        {
            "span_id": "SP-02",
            "extracted_skill": new_sub,
            "start_offset": new_st,
            "end_offset": new_en,
            "skill_category": "measurement_planning",
            "canonical_skill": "Garment Pattern Measurement and Fabric Cutting"
        }
    ]
    res_ann = client.post(f"/api/records/{rec1_id}/annotate", json=new_spans)
    assert res_ann.status_code == 200
    assert len(res_ann.json()["record"]["skill_spans"]) == 2

    # Status transition
    res_st = client.post("/api/records/{rec1_id}/status", json={
        "record_id": rec1_id,
        "new_status": "reviewed",
        "reviewer_status": "approved",
        "reviewer_id": "REV-TEST-01"
    })
    assert res_st.status_code == 200
    assert res_st.json()["record"]["annotation_status"] == "reviewed"
    print("  ✓ PASS: In-app annotation offset update and status transition verified.")

    # 10. Test Quality Audit
    print("[Test 10] Testing Quality Audit Endpoint...")
    res_q = client.get("/api/quality")
    assert res_q.status_code == 200
    q_data = res_q.json()
    assert q_data["offset_errors_count"] == 0, f"Offset errors detected: {q_data['offset_errors']}"
    assert q_data["missing_consent_count"] == 0
    print("  ✓ PASS: Quality audit confirmed zero offset errors and zero missing consents.")

    # 11. CRUCIAL CLEANUP: Zero Fake Records In Genuine Partition
    print("[Test 11] Performing Strict Cleanup of Test Fixtures from Genuine Batches...")
    tailor_file = REAL_DATA_DIR / "pilot_tailor_batch1.jsonl"
    if tailor_file.exists():
        with open(tailor_file, "r", encoding="utf-8") as f:
            lines = [l.strip() for l in f if l.strip()]
        # Remove any line with fixture_worker_id
        clean_lines = [l for l in lines if fixture_worker_id not in l]
        with open(tailor_file, "w", encoding="utf-8") as f:
            for l in clean_lines:
                f.write(l + "\n")

    # Verify real count is EXACTLY 0
    remaining_genuine = get_genuine_records()
    assert len(remaining_genuine) == 0, f"Expected 0 genuine records after cleanup, got {len(remaining_genuine)}"
    print("  ✓ PASS: Cleanup complete. Exactly 0 fake records remain in the genuine partition.")

    print("\n" + "=" * 65)
    print("ALL 11 FIELD COLLECTION SYSTEM TESTS PASSED SUCCESSFULLY!")
    print("=" * 65)

if __name__ == "__main__":
    run_collection_system_tests()
