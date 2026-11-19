"""
User Profile, Education, Experience, and Isolation Unit & Integration Tests.
"""

from fastapi.testclient import TestClient


def _get_auth_headers(client: TestClient, email: str, name: str) -> dict:
    res = client.post(
        "/api/v1/auth/register",
        json={"email": email, "password": "TestPassword123!", "full_name": name},
    )
    token = res.json()["token"]["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_get_and_update_profile(client: TestClient):
    """Verify fetching and updating the authenticated user's profile."""
    headers = _get_auth_headers(client, "profile.user@example.com", "Rohan Verma")

    # Fetch initial profile
    res1 = client.get("/api/v1/profiles/me", headers=headers)
    assert res1.status_code == 200
    p1 = res1.json()
    assert p1["headline"] is not None

    # Update profile
    update_payload = {
        "headline": "Lead Industrial Electrician & Solar Installer",
        "bio": "Over 6 years installing grid-tied commercial solar arrays.",
        "location": "Greater Noida, UP",
        "years_of_experience": 6,
        "trade_category": "Electrical & Solar Installations",
    }
    res2 = client.put("/api/v1/profiles/me", json=update_payload, headers=headers)
    assert res2.status_code == 200
    p2 = res2.json()
    assert p2["headline"] == update_payload["headline"]
    assert p2["years_of_experience"] == 6
    assert p2["completion_percentage"] >= 80


def test_education_crud(client: TestClient):
    """Verify creating, listing, and deleting education records."""
    headers = _get_auth_headers(client, "edu.user@example.com", "Kavita S.")

    # Create education
    edu_data = {
        "institution": "National Skill Training Institute (NSTI)",
        "degree_or_certificate": "Craft Instructor Training Scheme (CITS) Certificate",
        "field_of_study": "Garment Manufacturing Technology",
        "start_date": "2020-07-01",
        "end_date": "2021-06-30",
        "is_current": False,
        "grade_or_score": "First Class with Distinction",
    }
    create_res = client.post("/api/v1/profiles/education", json=edu_data, headers=headers)
    assert create_res.status_code == 201
    created_id = create_res.json()["id"]

    # List education
    list_res = client.get("/api/v1/profiles/education", headers=headers)
    assert list_res.status_code == 200
    items = list_res.json()
    assert len(items) >= 1
    assert any(i["id"] == created_id for i in items)

    # Delete education
    del_res = client.delete(f"/api/v1/profiles/education/{created_id}", headers=headers)
    assert del_res.status_code == 200

    # List again -> should be empty
    list_after = client.get("/api/v1/profiles/education", headers=headers)
    assert not any(i["id"] == created_id for i in list_after.json())


def test_experience_crud(client: TestClient):
    """Verify creating, listing, updating, and deleting work experience records."""
    headers = _get_auth_headers(client, "exp.user@example.com", "Manoj Singh")

    # Create work experience
    exp_data = {
        "job_title": "Master Tailor & Pattern Draper",
        "company_or_workshop": "Shree Ram Tailoring Workshop",
        "location": "Noida Sector 63",
        "employment_type": "Workshop Lead",
        "start_date": "2019-03-01",
        "is_current": True,
        "description": "Led a team of 4 junior artisans drafting patterns for bespoke formal suits.",
        "trade_tools_used": "Juki Lockstitch Machine DDL-8700, Pattern Grading Rulers",
    }
    create_res = client.post("/api/v1/profiles/experience", json=exp_data, headers=headers)
    assert create_res.status_code == 201
    exp_id = create_res.json()["id"]

    # List experience
    list_res = client.get("/api/v1/profiles/experience", headers=headers)
    assert list_res.status_code == 200
    assert len(list_res.json()) >= 1

    # Update experience
    update_data = {
        "job_title": "Senior Quality & Pattern Lead",
        "is_current": True,
    }
    update_res = client.put(f"/api/v1/profiles/experience/{exp_id}", json=update_data, headers=headers)
    assert update_res.status_code == 200
    assert update_res.json()["job_title"] == "Senior Quality & Pattern Lead"

    # Delete experience
    del_res = client.delete(f"/api/v1/profiles/experience/{exp_id}", headers=headers)
    assert del_res.status_code == 200


def test_profile_ownership_isolation(client: TestClient):
    """
    CRITICAL SECURITY TEST: Ensure User A cannot modify or delete User B's records.
    """
    headers_user_a = _get_auth_headers(client, "user.a@example.com", "User Alpha")
    headers_user_b = _get_auth_headers(client, "user.b@example.com", "User Beta")

    # User A creates an experience record
    exp_a = client.post(
        "/api/v1/profiles/experience",
        json={"job_title": "Artisan A", "company_or_workshop": "Workshop A"},
        headers=headers_user_a,
    ).json()
    exp_a_id = exp_a["id"]

    # User B attempts to UPDATE User A's experience -> must be rejected (404 / not owned)
    b_update_attempt = client.put(
        f"/api/v1/profiles/experience/{exp_a_id}",
        json={"job_title": "Malicious Hijack"},
        headers=headers_user_b,
    )
    assert b_update_attempt.status_code == 404

    # User B attempts to DELETE User A's experience -> must be rejected (404 / not owned)
    b_delete_attempt = client.delete(
        f"/api/v1/profiles/experience/{exp_a_id}",
        headers=headers_user_b,
    )
    assert b_delete_attempt.status_code == 404

    # Verify User A's record was NOT modified
    verify_a = client.get("/api/v1/profiles/experience", headers=headers_user_a)
    assert any(e["id"] == exp_a_id and e["job_title"] == "Artisan A" for e in verify_a.json())

