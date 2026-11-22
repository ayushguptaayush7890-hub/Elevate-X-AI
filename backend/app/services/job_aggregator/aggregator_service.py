"""
Job Aggregation Orchestrator Service.
Coordinates multi-source ingestion, duplicate detection, normalization, employer resolution,
and status tracking across all 12 evaluated platforms.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime, date
import uuid
import json
import logging
from sqlalchemy.orm import Session
from sqlalchemy import select, func, and_, or_

from app.models.job import Employer, JobListing, JobRequirement, AggregatorSyncLog
from app.services.job_aggregator.base_adapter import JobProviderAdapter, ProviderMetadata, UnifiedJob
from app.services.job_aggregator.adapters import (
    NaukriAdapter,
    LinkedInJobsAdapter,
    IndeedAdapter,
    InternshalaAdapter,
    FounditAdapter,
    ApnaAdapter,
    CutshortAdapter,
    AdzunaAdapter,
    JoobleAdapter,
    NationalCareerServiceAdapter,
    AuthorizedEmployerCareerFeedsAdapter,
    ApifyIndiaJobsAdapter,
)

logger = logging.getLogger(__name__)


class JobAggregatorService:
    """Central engine managing multi-source job ingestion, caching, and synchronization."""

    def __init__(self):
        self.adapters: Dict[str, JobProviderAdapter] = {
            "authorized_feeds": AuthorizedEmployerCareerFeedsAdapter(),
            "adzuna": AdzunaAdapter(),
            "jooble": JoobleAdapter(),
            "naukri": NaukriAdapter(),
            "linkedin": LinkedInJobsAdapter(),
            "indeed": IndeedAdapter(),
            "internshala": InternshalaAdapter(),
            "foundit": FounditAdapter(),
            "apna": ApnaAdapter(),
            "cutshort": CutshortAdapter(),
            "ncs": NationalCareerServiceAdapter(),
            "apify": ApifyIndiaJobsAdapter(),
        }

    def get_all_provider_statuses(self, db: Session) -> List[Dict[str, Any]]:
        """Returns the status and documentation metadata for all 12 evaluated platforms."""
        statuses = []
        for key, adapter in self.adapters.items():
            meta = adapter.metadata.model_dump()

            # Query real count of jobs in DB for this provider
            provider_display = meta["name"]
            # Check various source tags (e.g. Arbeitnow, RemoteOK, Jobicy belong to authorized_feeds)
            if key == "authorized_feeds":
                imported_count = db.execute(
                    select(func.count(JobListing.id)).where(
                        or_(
                            JobListing.source_provider.in_(["Arbeitnow", "RemoteOK", "Jobicy", "Authorized Feeds"]),
                            JobListing.source_provider.ilike("%Authorized Feeds%"),
                            JobListing.source_provider.ilike("%Greenhouse%"),
                        )
                    )
                ).scalar() or 0
            else:
                imported_count = db.execute(
                    select(func.count(JobListing.id)).where(
                        JobListing.source_provider.ilike(f"%{provider_display}%")
                    )
                ).scalar() or 0

            # Query last sync log
            last_log = db.execute(
                select(AggregatorSyncLog)
                .where(AggregatorSyncLog.provider_name == meta["name"])
                .order_by(AggregatorSyncLog.sync_completed_at.desc())
            ).scalars().first()

            meta["jobs_imported_count"] = imported_count
            meta["last_sync_timestamp"] = last_log.sync_completed_at if last_log else None
            statuses.append(meta)

        return statuses

    def sync_active_providers(self, db: Session, limit_per_source: int = 50) -> Dict[str, Any]:
        """
        Executes ingestion across all operational feeds with duplicate detection,
        provenance preservation, and atomic database commits.
        """
        total_fetched = 0
        total_imported = 0
        total_updated = 0
        provider_results = {}

        for key, adapter in self.adapters.items():
            if not adapter.is_enabled():
                continue

            provider_name = adapter.metadata.name
            sync_start = datetime.utcnow()
            fetched_count = 0
            imported_count = 0
            updated_count = 0
            error_msg = None

            try:
                logger.info(f"Starting real job sync for provider: {provider_name}")
                real_jobs: List[UnifiedJob] = adapter.fetch_jobs(limit=limit_per_source)
                fetched_count = len(real_jobs)
                total_fetched += fetched_count

                for job_data in real_jobs:
                    # 1. Duplicate Detection by provider_job_id or source_url
                    existing = db.execute(
                        select(JobListing).where(
                            or_(
                                and_(
                                    JobListing.source_provider == job_data.source_provider,
                                    JobListing.provider_job_id == job_data.provider_job_id,
                                ),
                                JobListing.source_url == job_data.source_url,
                            )
                        )
                    ).scalars().first()

                    if existing:
                        # Re-verify and update timestamp
                        existing.last_verified_at = datetime.utcnow()
                        existing.is_active = True
                        existing.listing_status = "active"
                        if job_data.application_url and not existing.application_url:
                            existing.application_url = job_data.application_url
                        updated_count += 1
                        total_updated += 1
                        continue

                    # 2. Employer Resolution (find or register verified employer)
                    employer_name = job_data.employer_name.strip()
                    employer = db.execute(
                        select(Employer).where(Employer.name == employer_name)
                    ).scalar_one_or_none()

                    if not employer:
                        employer = Employer(
                            name=employer_name,
                            website=job_data.employer_website,
                            location=job_data.location,
                            is_verified=True,
                        )
                        db.add(employer)
                        db.flush()

                    # 3. Create Unified Job Listing
                    new_job = JobListing(
                        employer_id=employer.id,
                        title=job_data.title,
                        location=job_data.location,
                        country=job_data.country or "India",
                        description=job_data.description,
                        salary_min=job_data.salary_min,
                        salary_max=job_data.salary_max,
                        salary_currency=job_data.salary_currency,
                        employment_type=job_data.employment_type,
                        experience_required_years=job_data.experience_min_years or 0,
                        experience_min_years=job_data.experience_min_years,
                        experience_max_years=job_data.experience_max_years,
                        source_type="aggregator",
                        source_provider=job_data.source_provider,
                        source_url=job_data.source_url,
                        application_url=job_data.application_url or job_data.source_url,
                        provider_job_id=job_data.provider_job_id,
                        work_mode=job_data.work_mode,
                        required_skills_json=json.dumps(job_data.required_skills),
                        posted_date=job_data.posted_date or date.today(),
                        expiry_date=job_data.expiry_date,
                        last_verified_at=datetime.utcnow(),
                        listing_status="active",
                        is_verified=True,
                        is_active=True,
                    )
                    db.add(new_job)
                    db.flush()

                    # Add parsed requirements
                    if job_data.required_skills:
                        for skill_name in job_data.required_skills[:6]:
                            db.add(
                                JobRequirement(
                                    job_id=new_job.id,
                                    requirement_text=f"Demonstrated proficiency in {skill_name}",
                                    is_mandatory=True,
                                )
                            )

                    imported_count += 1
                    total_imported += 1

                db.commit()
                status_str = "success"

            except Exception as e:
                db.rollback()
                logger.error(f"Error during job sync for {provider_name}: {e}", exc_info=True)
                error_msg = str(e)
                status_str = "failed"

            # Record sync log
            sync_log = AggregatorSyncLog(
                provider_name=provider_name,
                status=status_str,
                jobs_fetched=fetched_count,
                jobs_imported=imported_count,
                error_message=error_msg,
                sync_started_at=sync_start,
                sync_completed_at=datetime.utcnow(),
            )
            db.add(sync_log)
            db.commit()

            provider_results[provider_name] = {
                "status": status_str,
                "fetched": fetched_count,
                "imported": imported_count,
                "updated": updated_count,
                "error": error_msg,
            }

        # Expired job cleanup
        self.cleanup_expired_jobs(db)

        return {
            "total_fetched": total_fetched,
            "total_imported": total_imported,
            "total_updated": total_updated,
            "providers": provider_results,
            "synced_at": datetime.utcnow().isoformat(),
        }

    @staticmethod
    def cleanup_expired_jobs(db: Session) -> int:
        """Deactivates jobs whose expiration date has lapsed."""
        today = date.today()
        stmt = (
            select(JobListing)
            .where(
                and_(
                    JobListing.expiry_date.is_not(None),
                    JobListing.expiry_date < today,
                    JobListing.is_active == True,
                )
            )
        )
        expired_jobs = db.execute(stmt).scalars().all()
        count = 0
        for job in expired_jobs:
            job.is_active = False
            job.listing_status = "expired"
            count += 1
        if count > 0:
            db.commit()
            logger.info(f"Cleaned up {count} expired job listings.")
        return count
