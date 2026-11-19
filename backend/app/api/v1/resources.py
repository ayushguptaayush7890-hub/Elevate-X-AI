"""
API Router for Verified Training Providers, Learning Resources, and Skill Mappings.
"""

from typing import List, Optional
import uuid
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select, or_

from app.core.database import get_db
from app.api.deps import get_current_active_user, require_admin
from app.models.user import User
from app.models.learning_resource import (
    ResourceProvider,
    LearningResource,
    ResourceSkill,
)
from app.schemas.career_domain import (
    ResourceProviderCreate,
    ResourceProviderResponse,
    LearningResourceCreate,
    LearningResourceResponse,
)

router = APIRouter()


# =============================================================================
# Resource Provider Endpoints
# =============================================================================

@router.get("/providers", response_model=List[ResourceProviderResponse])
def list_providers(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """List verified training partners, guilds, and vocational academies."""
    return db.execute(
        select(ResourceProvider).order_by(ResourceProvider.name.asc())
    ).scalars().all()


@router.post("/providers", response_model=ResourceProviderResponse, status_code=status.HTTP_201_CREATED)
def create_provider(
    payload: ResourceProviderCreate,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    """Administrator endpoint: register a verified training organization or content partner."""
    existing = db.execute(
        select(ResourceProvider).where(ResourceProvider.name == payload.name)
    ).scalar_one_or_none()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A provider with this name already exists.",
        )

    provider = ResourceProvider(
        name=payload.name,
        website=payload.website,
        is_verified=payload.is_verified,
    )
    db.add(provider)
    db.commit()
    db.refresh(provider)
    return provider


# =============================================================================
# Learning Resource Endpoints
# =============================================================================

@router.get("", response_model=List[LearningResourceResponse])
def list_resources(
    language: Optional[str] = Query(None, description="Filter by language (e.g. English, Hindi)"),
    cost_type: Optional[str] = Query(None, description="Filter by cost (free, paid, subsidized)"),
    skill_id: Optional[uuid.UUID] = Query(None, description="Filter by targeted skill"),
    search: Optional[str] = Query(None, description="Search term for course title or description"),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Search and browse curated vocational courses and learning resources."""
    query = (
        select(LearningResource)
        .options(joinedload(LearningResource.provider))
        .where(LearningResource.is_active == True)  # noqa: E712
    )

    if language:
        query = query.where(LearningResource.language == language)
    if cost_type:
        query = query.where(LearningResource.cost_type == cost_type)
    if skill_id:
        query = query.join(ResourceSkill, LearningResource.id == ResourceSkill.resource_id).where(
            ResourceSkill.skill_id == skill_id
        )
    if search:
        search_filter = f"%{search.strip()}%"
        query = query.where(
            or_(
                LearningResource.title.ilike(search_filter),
                LearningResource.description.ilike(search_filter),
            )
        )

    query = query.order_by(LearningResource.created_at.desc()).offset(offset).limit(limit)
    return db.execute(query).unique().scalars().all()


@router.get("/{resource_id}", response_model=LearningResourceResponse)
def get_resource(
    resource_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Retrieve full detail of a specific learning resource."""
    resource = db.execute(
        select(LearningResource)
        .options(joinedload(LearningResource.provider))
        .where(LearningResource.id == resource_id)
    ).unique().scalar_one_or_none()

    if not resource:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Learning resource not found.",
        )
    return resource


@router.post("", response_model=LearningResourceResponse, status_code=status.HTTP_201_CREATED)
def create_resource(
    payload: LearningResourceCreate,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    """Administrator endpoint: catalog a new vocational learning course or module."""
    provider = db.execute(
        select(ResourceProvider).where(ResourceProvider.id == payload.provider_id)
    ).scalar_one_or_none()

    if not provider:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Provider specified for resource does not exist.",
        )

    resource = LearningResource(
        title=payload.title,
        provider_id=payload.provider_id,
        description=payload.description,
        url=payload.url,
        language=payload.language,
        cost_type=payload.cost_type,
        cost_amount=payload.cost_amount,
        duration_hours=payload.duration_hours,
        is_active=True,
    )
    db.add(resource)
    db.flush()

    for s_id in payload.skill_ids:
        db.add(
            ResourceSkill(
                resource_id=resource.id,
                skill_id=s_id,
            )
        )

    db.commit()

    return db.execute(
        select(LearningResource)
        .options(joinedload(LearningResource.provider))
        .where(LearningResource.id == resource.id)
    ).unique().scalar_one()


@router.delete("/{resource_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_resource(
    resource_id: uuid.UUID,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    """Administrator endpoint: delete a learning resource."""
    resource = db.execute(
        select(LearningResource).where(LearningResource.id == resource_id)
    ).scalar_one_or_none()

    if not resource:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Learning resource not found.",
        )

    db.delete(resource)
    db.commit()
    return None

