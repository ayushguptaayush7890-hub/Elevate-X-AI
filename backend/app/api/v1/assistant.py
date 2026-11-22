"""
AI Career Mentor & Consultations API Endpoints.
Provides persistent multi-turn consultations powered by Google Gemini API.
"""

from typing import List, Optional
import uuid
import json
import logging
from datetime import datetime, date
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import select, desc

from app.core.database import get_db
from app.api.deps import get_optional_current_user
from app.models.user import User
from app.models.consultation import Consultation, ConsultationMessage
from app.schemas.assistant import (
    ConsultationCreate,
    ConsultationUpdate,
    ConsultationListItem,
    ConsultationDetailResponse,
    MessageCreate,
    MessageResponse,
)
from app.services.assistant_context_service import AssistantContextService
from app.services.gemini_assistant_service import GeminiAssistantService

logger = logging.getLogger(__name__)

router = APIRouter()


def format_relative_date(dt: datetime) -> str:
    """Formats a datetime as 'Today', 'Yesterday', or 'Month Day'."""
    today = date.today()
    target = dt.date()
    delta = (today - target).days
    if delta == 0:
        return "Today"
    elif delta == 1:
        return "Yesterday"
    else:
        return dt.strftime("%b %d")


def serialize_message(msg: ConsultationMessage) -> MessageResponse:
    """Serializes a ConsultationMessage ORM model to Pydantic MessageResponse."""
    suggestions = []
    if msg.suggestions_json:
        try:
            suggestions = json.loads(msg.suggestions_json)
        except Exception:
            suggestions = []

    return MessageResponse(
        id=str(msg.id),
        consultation_id=str(msg.consultation_id),
        sender=msg.sender,
        content=msg.content,
        language=msg.language or "English",
        timestamp=msg.created_at.strftime("%I:%M %p"),
        model_used=msg.model_used,
        tokens_used=msg.tokens_used,
        suggestions=suggestions,
    )


@router.get("/consultations", response_model=List[ConsultationListItem])
def list_consultations(
    current_user: Optional[User] = Depends(get_optional_current_user),
    db: Session = Depends(get_db),
):
    """
    Lists consultation history for the user.
    If authenticated, returns the user's saved consultations.
    If guest, returns available active consultations or creates a starter one.
    """
    stmt = select(Consultation)
    if current_user:
        stmt = stmt.where(Consultation.user_id == current_user.id)
    stmt = stmt.order_by(desc(Consultation.updated_at))
    consultations = db.execute(stmt).scalars().all()

    # If empty, create an initial consultation
    if not consultations:
        initial = Consultation(
            user_id=current_user.id if current_user else None,
            title="Apparel QA Interview Prep",
            language="English",
        )
        db.add(initial)
        db.commit()
        db.refresh(initial)

        # Starter greeting message
        welcome_content = (
            "Hello! I am your **Elevate X AI Career Mentor**.\n\n"
            "I'm here to support your vocational growth, guide your career transition, prepare you for job interviews, "
            "and refine your resume based on your verified skills.\n\n"
            "What would you like to focus on today?"
        )
        welcome_msg = ConsultationMessage(
            consultation_id=initial.id,
            sender="assistant",
            content=welcome_content,
            language="English",
            model_used="gemini-3.1-flash-lite",
            suggestions_json=json.dumps([
                "How do I prepare for Apparel QA Manager interview?",
                "What are the top 5 defects in AQL 2.5 sampling?",
                "How do I explain my informal tailoring workshop years?",
            ]),
        )
        db.add(welcome_msg)
        db.commit()
        consultations = [initial]

    items: List[ConsultationListItem] = []
    for c in consultations:
        # Get message count and last message
        last_msg = db.execute(
            select(ConsultationMessage)
            .where(ConsultationMessage.consultation_id == c.id)
            .order_by(desc(ConsultationMessage.created_at))
            .limit(1)
        ).scalar_one_or_none()

        count = len(c.messages) if c.messages else 0
        preview = last_msg.content[:80] + "..." if last_msg else None

        items.append(
            ConsultationListItem(
                id=str(c.id),
                title=c.title,
                language=c.language,
                date=format_relative_date(c.updated_at or c.created_at),
                last_message_preview=preview,
                message_count=count,
                updated_at=c.updated_at or c.created_at,
            )
        )

    return items


@router.post("/consultations", response_model=ConsultationDetailResponse)
def create_consultation(
    payload: ConsultationCreate,
    current_user: Optional[User] = Depends(get_optional_current_user),
    db: Session = Depends(get_db),
):
    """Creates a new consultation session and seeds a personalized opening greeting."""
    lang = payload.language or "English"
    consultation = Consultation(
        user_id=current_user.id if current_user else None,
        title=payload.title or "New Career Consultation",
        language=lang,
    )
    db.add(consultation)
    db.commit()
    db.refresh(consultation)

    # Candidate profile context
    user_id = current_user.id if current_user else None
    context_str = AssistantContextService.get_candidate_context(db, user_id=user_id)

    # Opening greeting
    if lang.lower() in ["hindi", "hi"]:
        welcome_content = (
            "नमस्ते! मैं आपका **Elevate X AI Career Mentor** हूँ।\n\n"
            "मैं आपके कार्य अनुभव, कौशल मूल्यांकन, साक्षात्कार की तैयारी और करियर विकास में आपका मार्गदर्शन करने के लिए उपस्थित हूँ।\n\n"
            "आज आप अपने करियर के किस विषय पर चर्चा करना चाहते हैं?"
        )
        suggestions = [
            "इंटरव्यू के लिए आत्म-परिचय (Self-Introduction) कैसे तैयार करें?",
            "मेरे व्यावहारिक अनुभव को औपचारिक प्रमाणन में कैसे बदलें?",
            "अपने रिज्यूमे को उद्योग मानकों के अनुसार कैसे सुधारें?",
        ]
    else:
        welcome_content = (
            "Hello! I am your **Elevate X AI Career Mentor**.\n\n"
            "I am ready to help you navigate your career path, prepare for technical & behavioral interviews, "
            "translate your hands-on experience into formal credentials, and optimize your resume.\n\n"
            "What career goal or question shall we tackle today?"
        )
        suggestions = [
            "Generate my self-introduction for interviews",
            "What are top 5 questions for my target occupation?",
            "How do I explain informal workshop years on my resume?",
        ]

    welcome_msg = ConsultationMessage(
        consultation_id=consultation.id,
        sender="assistant",
        content=welcome_content,
        language=lang,
        model_used="gemini-3.1-flash-lite",
        suggestions_json=json.dumps(suggestions),
    )
    db.add(welcome_msg)
    db.commit()
    db.refresh(welcome_msg)

    return ConsultationDetailResponse(
        id=str(consultation.id),
        title=consultation.title,
        language=consultation.language,
        created_at=consultation.created_at,
        updated_at=consultation.updated_at,
        messages=[serialize_message(welcome_msg)],
    )


@router.get("/consultations/{consultation_id}", response_model=ConsultationDetailResponse)
def get_consultation(
    consultation_id: str,
    current_user: Optional[User] = Depends(get_optional_current_user),
    db: Session = Depends(get_db),
):
    """Retrieves consultation details with full message history in chronological order."""
    try:
        c_uuid = uuid.UUID(consultation_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid consultation ID format")

    consultation = db.execute(
        select(Consultation).where(Consultation.id == c_uuid)
    ).scalar_one_or_none()

    if not consultation:
        raise HTTPException(status_code=404, detail="Consultation not found")

    # User isolation: If owned by a registered user, restrict access to that user
    if consultation.user_id is not None:
        if not current_user or current_user.id != consultation.user_id:
            raise HTTPException(status_code=404, detail="Consultation not found")

    messages = db.execute(
        select(ConsultationMessage)
        .where(ConsultationMessage.consultation_id == consultation.id)
        .order_by(ConsultationMessage.created_at.asc())
    ).scalars().all()

    return ConsultationDetailResponse(
        id=str(consultation.id),
        title=consultation.title,
        language=consultation.language,
        created_at=consultation.created_at,
        updated_at=consultation.updated_at,
        messages=[serialize_message(m) for m in messages],
    )


@router.post("/consultations/{consultation_id}/messages", response_model=MessageResponse)
def send_message(
    consultation_id: str,
    payload: MessageCreate,
    current_user: Optional[User] = Depends(get_optional_current_user),
    db: Session = Depends(get_db),
):
    """
    Submits a user message, runs Google Gemini inference with authentic candidate context
    and conversation history, stores both user and assistant messages, and returns the response.
    """
    try:
        c_uuid = uuid.UUID(consultation_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid consultation ID format")

    consultation = db.execute(
        select(Consultation).where(Consultation.id == c_uuid)
    ).scalar_one_or_none()

    if not consultation:
        raise HTTPException(status_code=404, detail="Consultation not found")

    # User isolation: If owned by a registered user, restrict access to that user
    if consultation.user_id is not None:
        if not current_user or current_user.id != consultation.user_id:
            raise HTTPException(status_code=404, detail="Consultation not found")

    lang = payload.language or consultation.language or "English"

    # 1. Save User Message
    user_msg = ConsultationMessage(
        consultation_id=consultation.id,
        sender="user",
        content=payload.content.strip(),
        language=lang,
    )
    db.add(user_msg)
    db.commit()

    # Auto-update title if it's default
    if consultation.title in ["New Career Consultation", "Apparel QA Interview Prep"]:
        words = payload.content.strip().split()
        if len(words) > 0:
            short_title = " ".join(words[:5])
            if len(short_title) > 40:
                short_title = short_title[:40] + "..."
            consultation.title = short_title

    # 2. Retrieve Conversation History
    prev_messages = db.execute(
        select(ConsultationMessage)
        .where(ConsultationMessage.consultation_id == consultation.id)
        .order_by(ConsultationMessage.created_at.asc())
    ).scalars().all()

    chat_history = [
        {"sender": m.sender, "content": m.content}
        for m in prev_messages[:-1]  # exclude the newly added message from history list since passed as current
    ]

    # 3. Retrieve Candidate Profile Context
    user_id = current_user.id if current_user else consultation.user_id
    candidate_context = AssistantContextService.get_candidate_context(db, user_id=user_id)

    # 4. Invoke Google Gemini API
    mentor_service = GeminiAssistantService()
    try:
        result = mentor_service.generate_mentor_response(
            user_message=payload.content.strip(),
            language=lang,
            candidate_context=candidate_context,
            conversation_history=chat_history,
        )
    except Exception as e:
        logger.error(f"Error during Gemini inference: {e}", exc_info=True)
        raise HTTPException(
            status_code=502,
            detail=f"Google Gemini inference error: {str(e)}",
        )

    # 5. Save Assistant Message
    assistant_msg = ConsultationMessage(
        consultation_id=consultation.id,
        sender="assistant",
        content=result["content"],
        language=lang,
        model_used=result["model_used"],
        tokens_used=result.get("tokens_used"),
        suggestions_json=json.dumps(result.get("suggestions", [])),
    )
    consultation.updated_at = datetime.utcnow()
    db.add(assistant_msg)
    db.commit()
    db.refresh(assistant_msg)

    return serialize_message(assistant_msg)


@router.patch("/consultations/{consultation_id}", response_model=ConsultationDetailResponse)
def update_consultation(
    consultation_id: str,
    payload: ConsultationUpdate,
    current_user: Optional[User] = Depends(get_optional_current_user),
    db: Session = Depends(get_db),
):
    """Updates title or language of a consultation."""
    try:
        c_uuid = uuid.UUID(consultation_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid consultation ID format")

    consultation = db.execute(
        select(Consultation).where(Consultation.id == c_uuid)
    ).scalar_one_or_none()

    if not consultation:
        raise HTTPException(status_code=404, detail="Consultation not found")

    # User isolation: If owned by a registered user, restrict access to that user
    if consultation.user_id is not None:
        if not current_user or current_user.id != consultation.user_id:
            raise HTTPException(status_code=404, detail="Consultation not found")

    if payload.title is not None:
        consultation.title = payload.title
    if payload.language is not None:
        consultation.language = payload.language
    consultation.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(consultation)

    messages = db.execute(
        select(ConsultationMessage)
        .where(ConsultationMessage.consultation_id == consultation.id)
        .order_by(ConsultationMessage.created_at.asc())
    ).scalars().all()

    return ConsultationDetailResponse(
        id=str(consultation.id),
        title=consultation.title,
        language=consultation.language,
        created_at=consultation.created_at,
        updated_at=consultation.updated_at,
        messages=[serialize_message(m) for m in messages],
    )


@router.delete("/consultations/{consultation_id}")
def delete_consultation(
    consultation_id: str,
    current_user: Optional[User] = Depends(get_optional_current_user),
    db: Session = Depends(get_db),
):
    """Deletes a consultation and its messages."""
    try:
        c_uuid = uuid.UUID(consultation_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid consultation ID format")

    consultation = db.execute(
        select(Consultation).where(Consultation.id == c_uuid)
    ).scalar_one_or_none()

    if not consultation:
        raise HTTPException(status_code=404, detail="Consultation not found")

    # User isolation: If owned by a registered user, restrict access to that user
    if consultation.user_id is not None:
        if not current_user or current_user.id != consultation.user_id:
            raise HTTPException(status_code=404, detail="Consultation not found")

    db.delete(consultation)
    db.commit()
    return {"message": "Consultation deleted successfully", "id": consultation_id}
