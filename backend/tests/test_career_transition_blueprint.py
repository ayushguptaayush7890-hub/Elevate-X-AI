"""
Regression and Integration Tests for Career Transition Blueprint Generation:
Verifies dynamic occupation-specific blueprints, authentic dataset competencies,
isolated caching, duration consistency, and verified learning resource matching.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.services.career_transition_service import CareerTransitionService

client = TestClient(app)


def test_different_occupation_pairs_produce_different_competency_sets():
    """Requirement 1: Verify different occupation pairs produce completely distinct competency sets."""
    bp_tech = client.post(
        "/api/v1/career-transitions/blueprint",
        json={"from_occupation": "Software Developer", "to_occupation": "Integration Engineer", "recalibrate": True}
    ).json()

    bp_elec = client.post(
        "/api/v1/career-transitions/blueprint",
        json={"from_occupation": "Electrician", "to_occupation": "Building Electrician", "recalibrate": True}
    ).json()

    bp_tailor = client.post(
        "/api/v1/career-transitions/blueprint",
        json={"from_occupation": "Custom Tailor", "to_occupation": "Patternmaker", "recalibrate": True}
    ).json()

    comps_tech = {c.lower() for s in bp_tech["stages"] for c in s["target_competencies"]}
    comps_elec = {c.lower() for s in bp_elec["stages"] for c in s["target_competencies"]}
    comps_tailor = {c.lower() for s in bp_tailor["stages"] for c in s["target_competencies"]}

    # Ensure intersection between unrelated domains is empty
    assert len(comps_tech & comps_elec) == 0, f"Tech and Electrical share competencies: {comps_tech & comps_elec}"
    assert len(comps_tech & comps_tailor) == 0, f"Tech and Tailor share competencies: {comps_tech & comps_tailor}"
    assert len(comps_elec & comps_tailor) == 0, f"Electrical and Tailor share competencies: {comps_elec & comps_tailor}"


def test_different_occupation_pairs_produce_relevant_practical_tasks():
    """Requirement 2: Verify practical tasks are tailored specifically to the destination occupation."""
    bp_elec = client.post(
        "/api/v1/career-transitions/blueprint",
        json={"from_occupation": "Electrician", "to_occupation": "Building Electrician", "recalibrate": True}
    ).json()

    bp_tailor = client.post(
        "/api/v1/career-transitions/blueprint",
        json={"from_occupation": "Custom Tailor", "to_occupation": "Patternmaker", "recalibrate": True}
    ).json()

    elec_tasks_text = " ".join([t for s in bp_elec["stages"] for t in s.get("practical_tasks", s.get("tasks", []))]).lower()
    tailor_tasks_text = " ".join([t for s in bp_tailor["stages"] for t in s.get("practical_tasks", s.get("tasks", []))]).lower()

    # Electrician tasks should mention electrical / wiring / circuits / building
    assert any(w in elec_tasks_text for w in ["electric", "wiring", "building", "system", "installation", "equipment"])
    # Tailor tasks should mention garment / apparel / pattern / fabric / sewing
    assert any(w in tailor_tasks_text for w in ["apparel", "pattern", "textile", "fabric", "garment", "cutting"])


def test_destination_occupation_changes_prompt_and_duration():
    """Requirement 3: Verify destination occupation changes the generated blueprint timeline and stages."""
    bp_elec = client.post(
        "/api/v1/career-transitions/blueprint",
        json={"from_occupation": "Electrician", "to_occupation": "Building Electrician", "recalibrate": True}
    ).json()

    bp_tailor = client.post(
        "/api/v1/career-transitions/blueprint",
        json={"from_occupation": "Custom Tailor", "to_occupation": "Patternmaker", "recalibrate": True}
    ).json()

    assert bp_elec["target_occupation"] != bp_tailor["target_occupation"]
    assert bp_elec["total_estimated_weeks"] != bp_tailor["total_estimated_weeks"]


def test_cache_keys_distinguish_different_transitions():
    """Requirement 6: Verify cache keys distinguish transitions and cache hit sets cached=True."""
    res1 = client.post(
        "/api/v1/career-transitions/blueprint",
        json={"from_occupation": "Software Developer", "to_occupation": "Integration Engineer", "recalibrate": True}
    ).json()
    assert res1.get("cached") is False

    res2 = client.post(
        "/api/v1/career-transitions/blueprint",
        json={"from_occupation": "Software Developer", "to_occupation": "Integration Engineer", "recalibrate": False}
    ).json()
    assert res2.get("cached") is True


def test_recalibration_updates_affected_blueprints():
    """Requirement 7: Verify calling recalibrate forces fresh generation (cached=False)."""
    res1 = client.post(
        "/api/v1/career-transitions/blueprint",
        json={"from_occupation": "Electrician", "to_occupation": "Building Electrician", "recalibrate": False}
    ).json()

    res2 = client.post(
        "/api/v1/career-transitions/blueprint/recalibrate",
        json={"from_occupation": "Electrician", "to_occupation": "Building Electrician"}
    ).json()
    assert res2.get("cached") is False


def test_duration_totals_remain_consistent():
    """Requirement 9: Ensure stage duration totals match the displayed total duration."""
    for pair in [
        ("Software Developer", "Integration Engineer"),
        ("Electrician", "Building Electrician"),
        ("Custom Tailor", "Patternmaker")
    ]:
        bp = client.post(
            "/api/v1/career-transitions/blueprint",
            json={"from_occupation": pair[0], "to_occupation": pair[1], "recalibrate": False}
        ).json()

        total_weeks = bp["total_estimated_weeks"]
        stage_sum = sum([s["duration_weeks"] for s in bp["stages"]])
        assert stage_sum == total_weeks, f"Stage weeks sum {stage_sum} != total {total_weeks} for {pair}"


def test_verified_resources_match_destination_occupation():
    """Requirement 10: Verify learning resources match destination domain and reject mismatched domains."""
    bp_elec = client.post(
        "/api/v1/career-transitions/blueprint",
        json={"from_occupation": "Electrician", "to_occupation": "Building Electrician", "recalibrate": False}
    ).json()

    bp_tailor = client.post(
        "/api/v1/career-transitions/blueprint",
        json={"from_occupation": "Custom Tailor", "to_occupation": "Patternmaker", "recalibrate": False}
    ).json()

    elec_resources = [r["title"].lower() for s in bp_elec["stages"] for r in s.get("recommended_resources", [])]
    tailor_resources = [r["title"].lower() for s in bp_tailor["stages"] for r in s.get("recommended_resources", [])]

    # Electrical blueprint must NEVER recommend Python or PyTorch
    for r in elec_resources:
        assert "python" not in r and "pytorch" not in r, f"Electrical received software resource: {r}"

    # Tailoring blueprint must NEVER recommend Python or PyTorch
    for r in tailor_resources:
        assert "python" not in r and "pytorch" not in r, f"Tailoring received software resource: {r}"

    # Tailoring must receive textile/apparel resources
    assert any("pattern" in r or "textile" in r or "garment" in r for r in tailor_resources)
    # Electrical must receive electrical/standards resources
    assert any("electric" in r or "dgt" in r or "cea" in r or "bis" in r or "osha" in r for r in elec_resources)
