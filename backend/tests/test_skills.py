"""
Vocational Skills Catalog and User Skill Mapping Unit & Integration Tests.
"""

from fastapi.testclient import TestClient


def _get_auth_headers(client: TestClient, email: str, name: str) -> dict:
    res = client.post(
        "/api/v1/auth/register",
        json={"email": email, "password": "TestPassword123!", "full_name": name},
    )
    token = res.json()["token"]["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_skills_catalog_list_and_create(client: TestClient):
    """Verify listing and creating skills in the master catalog."""
    # Create skill in catalog
    skill_payload = {
        "name": "Lockstitch Machine Mastery",
        "category": "Apparel & Garment Manufacturing",
        "nsqf_level": 4,
        "description": "Operating single and multi-needle lockstitch machines for industrial garment export.",
    }
    create_res = client.post("/api/v1/skills", json=skill_payload)
    assert create_res.status_code == 201
    created = create_res.json()
    assert created["name"] == "Lockstitch Machine Mastery"
    skill_id = created["id"]

    # Retrieve skill details by ID
    get_res = client.get(f"/api/v1/skills/{skill_id}")
    assert get_res.status_code == 200
    assert get_res.json()["name"] == "Lockstitch Machine Mastery"

    # Search in catalog
    search_res = client.get("/api/v1/skills?search=Lockstitch")
    assert search_res.status_code == 200
    assert any(s["id"] == skill_id for s in search_res.json())


def test_user_skill_add_and_list(client: TestClient):
    """Verify adding a self-reported skill to a user's vocational profile."""
    headers = _get_auth_headers(client, "skill.user1@example.com", "Anil Sharma")

    # Add skill to profile by name (auto-registers if not in catalog)
    payload = {
        "skill_name": "Pattern Drafting & Grading",
        "category": "Pattern Engineering",
        "verification_status": "self_reported",
        "proficiency_level": "advanced",
        "years_practiced": 5.0,
        "confidence_score": 0.90,
    }
    add_res = client.post("/api/v1/profiles/me/skills", json=payload, headers=headers)
    assert add_res.status_code == 201
    user_skill = add_res.json()
    assert user_skill["verification_status"] == "self_reported"
    assert user_skill["proficiency_level"] == "advanced"
    assert user_skill["skill"]["name"] == "Pattern Drafting & Grading"

    # List profile skills
    list_res = client.get("/api/v1/profiles/me/skills", headers=headers)
    assert list_res.status_code == 200
    skills_list = list_res.json()
    assert len(skills_list) >= 1
    assert any(s["skill"]["name"] == "Pattern Drafting & Grading" for s in skills_list)


def test_user_skill_update_and_delete(client: TestClient):
    """Verify updating proficiency and removing skills from profile."""
    headers = _get_auth_headers(client, "skill.user2@example.com", "Pooja Verma")

    # Add skill
    add_res = client.post(
        "/api/v1/profiles/me/skills",
        json={"skill_name": "AQL 2.5 Quality Sampling Protocols", "proficiency_level": "intermediate"},
        headers=headers,
    )
    user_skill_id = add_res.json()["id"]

    # Update proficiency
    update_res = client.put(
        f"/api/v1/profiles/me/skills/{user_skill_id}",
        json={"proficiency_level": "expert", "years_practiced": 4.5},
        headers=headers,
    )
    assert update_res.status_code == 200
    assert update_res.json()["proficiency_level"] == "expert"
    assert update_res.json()["years_practiced"] == 4.5

    # Delete skill
    del_res = client.delete(f"/api/v1/profiles/me/skills/{user_skill_id}", headers=headers)
    assert del_res.status_code == 200

    # Verify skill is removed
    list_after = client.get("/api/v1/profiles/me/skills", headers=headers)
    assert not any(s["id"] == user_skill_id for s in list_after.json())


def test_duplicate_user_skill_rejected(client: TestClient):
    """Verify adding the same skill twice to the same profile is rejected with 400."""
    headers = _get_auth_headers(client, "skill.user3@example.com", "Vikas Kumar")

    # First addition
    r1 = client.post(
        "/api/v1/profiles/me/skills",
        json={"skill_name": "Hydraulic Brake Overhaul"},
        headers=headers,
    )
    assert r1.status_code == 201

    # Duplicate addition
    r2 = client.post(
        "/api/v1/profiles/me/skills",
        json={"skill_name": "Hydraulic Brake Overhaul"},
        headers=headers,
    )
    assert r2.status_code == 400
    assert "already listed" in r2.json()["error"]["message"]


def test_skill_evidence_attachment_and_upgrade(client: TestClient):
    """
    Verify practical diagnostic test scores >= 80% upgrade the skill status
    from 'self_reported' to 'assessed'.
    """
    headers = _get_auth_headers(client, "skill.user4@example.com", "Deepak Rao")

    # Add self-reported skill
    add_res = client.post(
        "/api/v1/profiles/me/skills",
        json={"skill_name": "Solar Inverter Synchronization", "verification_status": "self_reported"},
        headers=headers,
    )
    user_skill_id = add_res.json()["id"]
    assert add_res.json()["verification_status"] == "self_reported"

    # Attach diagnostic assessment evidence with score 92%
    evidence_payload = {
        "evidence_type": "diagnostic_assessment",
        "title": "Grid-Tied Micro-Inverter Scenario Assessment",
        "description": "Demonstrated correct voltage sequencing and harmonic distortion checks.",
        "score_achieved": 92.0,
    }
    ev_res = client.post(
        f"/api/v1/profiles/me/skills/{user_skill_id}/evidence",
        json=evidence_payload,
        headers=headers,
    )
    assert ev_res.status_code == 201

    # Verify user skill is now assessed
    list_res = client.get("/api/v1/profiles/me/skills", headers=headers)
    matching = [s for s in list_res.json() if s["id"] == user_skill_id][0]
    assert matching["verification_status"] == "assessed"
    assert len(matching["evidences"]) == 1
    assert matching["evidences"][0]["score_achieved"] == 92.0

