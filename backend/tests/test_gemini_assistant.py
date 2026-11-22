"""
Test suite for Elevate X AI Assistant powered by Google Gemini API.
Verifies service configuration, context aggregation, live inference,
multilingual capabilities (English/Hindi), and consultation persistence.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.config import settings
from app.services.gemini_assistant_service import GeminiAssistantService
from app.services.assistant_context_service import AssistantContextService
from app.core.database import SessionLocal


@pytest.fixture
def client():
    return TestClient(app)


def test_gemini_config_and_service_init():
    """Verify Gemini API key and model configuration."""
    assert settings.GEMINI_API_KEY, "GEMINI_API_KEY must be configured in settings"
    assert settings.GEMINI_MODEL, "GEMINI_MODEL must be configured in settings"
    service = GeminiAssistantService()
    assert service.api_key == settings.GEMINI_API_KEY


def test_assistant_context_service_retrieval():
    """Verify context aggregator extracts grounded candidate data."""
    db = SessionLocal()
    try:
        context = AssistantContextService.get_candidate_context(db)
        assert context, "Candidate context should not be empty"
        assert "Candidate Profile" in context
        # Should reference Ramesh or real user profile
        assert "Ramesh Sharma" in context or "Candidate" in context
    finally:
        db.close()


def test_consultation_lifecycle_api(client):
    """Verify consultation creation, retrieval, listing, and patching."""
    # 1. Create Consultation
    create_res = client.post(
        "/api/v1/assistant/consultations",
        json={"title": "Pytest Consultation Lifecycle", "language": "English"},
    )
    assert create_res.status_code == 200, create_res.text
    data = create_res.json()
    c_id = data["id"]
    assert data["title"] == "Pytest Consultation Lifecycle"
    assert len(data["messages"]) >= 1  # includes starter welcome greeting
    assert data["messages"][0]["sender"] == "assistant"
    assert len(data["messages"][0]["suggestions"]) > 0

    # 2. Get Consultation Detail
    get_res = client.get(f"/api/v1/assistant/consultations/{c_id}")
    assert get_res.status_code == 200
    assert get_res.json()["id"] == c_id

    # 3. List Consultations
    list_res = client.get("/api/v1/assistant/consultations")
    assert list_res.status_code == 200
    ids = [c["id"] for c in list_res.json()]
    assert c_id in ids

    # 4. Patch Consultation Title
    patch_res = client.patch(
        f"/api/v1/assistant/consultations/{c_id}",
        json={"title": "Updated Pytest Title", "language": "Hindi"},
    )
    assert patch_res.status_code == 200
    assert patch_res.json()["title"] == "Updated Pytest Title"
    assert patch_res.json()["language"] == "Hindi"

    # 5. Delete Consultation
    del_res = client.delete(f"/api/v1/assistant/consultations/{c_id}")
    assert del_res.status_code == 200


def test_gemini_inference_live_english(client):
    """Verify live Gemini API inference on an English vocational career question."""
    # Create fresh consultation
    c_res = client.post(
        "/api/v1/assistant/consultations",
        json={"title": "QA Transition Inquiry", "language": "English"},
    )
    assert c_res.status_code == 200
    c_id = c_res.json()["id"]

    # Send career question
    msg_res = client.post(
        f"/api/v1/assistant/consultations/{c_id}/messages",
        json={
            "content": "What are the most critical differences between informal tailoring and formal Apparel Quality Assurance?",
            "language": "English",
        },
    )
    assert msg_res.status_code == 200, msg_res.text
    bot_msg = msg_res.json()
    assert bot_msg["sender"] == "assistant"
    assert len(bot_msg["content"]) > 50
    assert bot_msg["model_used"] in ["gemini-3.1-flash-lite", "gemini-3.5-flash-lite", "gemini-3-flash-preview"]
    assert isinstance(bot_msg["suggestions"], list)
    assert len(bot_msg["suggestions"]) > 0


def test_gemini_inference_live_hindi(client):
    """Verify live Gemini API inference on a Hindi query."""
    c_res = client.post(
        "/api/v1/assistant/consultations",
        json={"title": "हिंदी करियर परामर्श", "language": "Hindi"},
    )
    assert c_res.status_code == 200
    c_id = c_res.json()["id"]

    msg_res = client.post(
        f"/api/v1/assistant/consultations/{c_id}/messages",
        json={
            "content": "कपड़ा उद्योग (Apparel QA) में AQL 2.5 सैंपलिंग का क्या महत्व है?",
            "language": "Hindi",
        },
    )
    assert msg_res.status_code == 200, msg_res.text
    bot_msg = msg_res.json()
    assert bot_msg["sender"] == "assistant"
    assert len(bot_msg["content"]) > 30
    # Must contain Devanagari characters
    has_devanagari = any("\u0900" <= ch <= "\u097F" for ch in bot_msg["content"])
    assert has_devanagari, "Response to Hindi inquiry must contain Devanagari text"
    assert len(bot_msg["suggestions"]) > 0


def test_multi_turn_conversation_persistence(client):
    """Verify multi-turn memory across consecutive user messages."""
    c_res = client.post(
        "/api/v1/assistant/consultations",
        json={"title": "Multi-turn Consultation", "language": "English"},
    )
    c_id = c_res.json()["id"]

    # Turn 1
    t1_res = client.post(
        f"/api/v1/assistant/consultations/{c_id}/messages",
        json={"content": "My name is Ayush and I have 3 years of electrical wiring experience.", "language": "English"},
    )
    assert t1_res.status_code == 200

    # Turn 2: Follow-up relying on prior turn
    t2_res = client.post(
        f"/api/v1/assistant/consultations/{c_id}/messages",
        json={"content": "Based on what I just told you, which certification should I get first?", "language": "English"},
    )
    assert t2_res.status_code == 200
    content = t2_res.json()["content"].lower()
    # Should reference electrician or electrical certification
    assert any(term in content for term in ["electric", "wire", "license", "certification", "safety"])

    # Verify all turns persisted in DB in order
    hist_res = client.get(f"/api/v1/assistant/consultations/{c_id}")
    assert hist_res.status_code == 200
    messages = hist_res.json()["messages"]
    # Welcome msg + User 1 + Bot 1 + User 2 + Bot 2 = 5 messages
    assert len(messages) >= 5
    senders = [m["sender"] for m in messages]
    assert senders == ["assistant", "user", "assistant", "user", "assistant"]
