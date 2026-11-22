"""
Base Job Provider Adapter and Unified Schema Definitions.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from datetime import datetime, date
from pydantic import BaseModel, Field


class UnifiedJob(BaseModel):
    """Normalized multi-source job vacancy schema."""
    provider_job_id: str
    source_provider: str
    title: str
    employer_name: str
    employer_website: Optional[str] = None
    employer_logo: Optional[str] = None
    source_url: str
    application_url: Optional[str] = None
    description: str
    location: str
    country: str = "India"
    work_mode: str = "On-site"  # "Remote", "Hybrid", "On-site"
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    salary_currency: str = "INR"
    employment_type: str = "Full-time"
    experience_min_years: Optional[int] = None
    experience_max_years: Optional[int] = None
    required_skills: List[str] = Field(default_factory=list)
    posted_date: Optional[date] = None
    expiry_date: Optional[date] = None
    listing_status: str = "active"


class ProviderMetadata(BaseModel):
    """Metadata and compliance documentation for an external job board."""
    provider_id: str
    name: str
    official_website: str
    api_docs_url: Optional[str] = None
    status: str  # "active", "ready_for_key", "pending_partner_approval"
    public_api_available: bool
    auth_requirements: str
    commercial_usage_permission: str
    data_fields_available: List[str]
    original_listing_url_available: bool
    direct_application_url_available: bool
    refresh_restrictions: str
    jobs_imported_count: int = 0
    last_sync_timestamp: Optional[datetime] = None


class JobProviderAdapter(ABC):
    """Abstract interface that every job portal adapter must implement."""

    @property
    @abstractmethod
    def metadata(self) -> ProviderMetadata:
        """Returns the official documentation and capability metadata for this provider."""
        pass

    @abstractmethod
    def fetch_jobs(
        self,
        search: Optional[str] = None,
        location: Optional[str] = None,
        limit: int = 50,
    ) -> List[UnifiedJob]:
        """Fetches real vacancies from the provider and normalizes them into UnifiedJob format."""
        pass

    def is_enabled(self) -> bool:
        """Returns whether this adapter is active and operational."""
        return self.metadata.status == "active"
