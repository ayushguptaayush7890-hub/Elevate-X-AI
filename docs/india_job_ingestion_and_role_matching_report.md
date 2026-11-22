# ELEVATE X AI — FIND JOBS: INDIA-FIRST JOB INGESTION, ROLE-BASED MATCHING & DATA QUALITY REPAIR
**Verification & Technical Audit Report**  
**Date:** November 22, 2026  
**System Status:** Fully Operational & Verified (`/jobs` and `/find-jobs`)  
**Backend:** FastAPI v1.0.0 (`http://localhost:8000/api/v1/jobs`)  
**Frontend:** Next.js 16.4.6 (`http://localhost:3002/find-jobs` and `http://localhost:3002/jobs`)  

---

## 1. Executive Summary & Root Cause Analysis

### 1.1 The Issue
The previous implementation of the job aggregator displayed 25 listings dominated exclusively by European and German cities (`Berlin`, `Hamburg`, `Munich`, `Cologne`, `Magdeburg`, `Germany`). The location dropdown only exposed these German locations, failing to serve Indian vocational candidates and technical learners.

### 1.2 Root Cause Analysis
1. **Single Foreign Source Configuration:** The previous `AuthorizedEmployerCareerFeedsAdapter` pulled exclusively from `Arbeitnow` (`www.arbeitnow.com/api/job-board-api`), an EU/German-centric job board.
2. **Missing Market Partitioning:** The database table `job_listings` lacked a `country` attribute, preventing isolation between domestic Indian listings and international opportunities.
3. **Dynamic Location Scraping in UI:** The frontend dynamically extracted locations from the imported listings. Because only German jobs were synced, the dropdown showed only German cities.
4. **Missing Role-Based Categorization:** The API and frontend lacked role category query capabilities (e.g. AI Engineer, Python Developer, Data Analyst).

---

## 2. India-First Architecture & Authentic ATS Ingestion

### 2.1 Authorized Corporate ATS Feeds (Greenhouse)
To respect the **Absolute Data Integrity Rules** (zero synthetic jobs, zero manual fabrication, genuine employer links), Elevate X AI integrated direct, open public ATS developer feeds for major enterprise tech employers with authorized Indian engineering operations:

| Employer | ATS Platform | Indian Office Hubs | Authentic Application Link |
| :--- | :--- | :--- | :--- |
| **MongoDB** | Greenhouse Open Feed (`mongodb`) | Gurugram (Delhi NCR), Bengaluru, Noida | `https://www.mongodb.com/careers/job/?gh_jid=...` |
| **Databricks** | Greenhouse Open Feed (`databricks`) | Bengaluru (Karnataka), Mumbai (Maharashtra) | `https://boards.greenhouse.io/databricks/jobs/...` |
| **InMobi** | Greenhouse Open Feed (`inmobi`) | Bengaluru (Karnataka) | `https://boards.greenhouse.io/inmobi/jobs/...` |
| **Elastic** | Greenhouse Open Feed (`elastic`) | Bengaluru (Karnataka) | `https://boards.greenhouse.io/elastic/jobs/...` |
| **Rubrik** | Greenhouse Open Feed (`rubrik`) | Bengaluru (Karnataka), India | `https://boards.greenhouse.io/rubrik/jobs/...` |
| **Okta** | Greenhouse Open Feed (`okta`) | Bengaluru (Karnataka) | `https://boards.greenhouse.io/okta/jobs/...` |
| **Samsara** | Greenhouse Open Feed (`samsara`) | Bengaluru (Karnataka) | `https://boards.greenhouse.io/samsara/jobs/...` |
| **Datadog** | Greenhouse Open Feed (`datadog`) | Bengaluru (Karnataka) | `https://boards.greenhouse.io/datadog/jobs/...` |

### 2.2 Status of All 12 Evaluated Platforms

| # | Platform | Official Website | API Status | Auth & Permissions Requirements | Ingested Live |
|---|---|---|---|---|---|
| 1 | **Authorized Employer Feeds** | `https://boards.greenhouse.io` | **Active** | Open ATS developer feeds; genuine corporate links | **150+ India, 25 International** |
| 2 | **Adzuna India** | `https://developer.adzuna.com` | **Ready for Key** | `country=in`, `ADZUNA_APP_ID`, `ADZUNA_APP_KEY` | Configured |
| 3 | **Jooble** | `https://jooble.org/api/about` | **Ready for Key** | Free partner key (`JOOBLE_API_KEY`) | Configured |
| 4 | **Naukri.com** | `https://www.naukri.com` | **Pending Partner** | Info Edge Enterprise e-Hire Corporate OAuth | 0 (No unauthorized scraping) |
| 5 | **LinkedIn Jobs** | `https://www.linkedin.com/jobs` | **Pending Partner** | Microsoft LinkedIn Talent Solutions Certification | 0 (No unauthorized scraping) |
| 6 | **Indeed India** | `https://in.indeed.com` | **Pending Partner** | Indeed Developer Integration Agreement | 0 (No unauthorized scraping) |
| 7 | **Internshala** | `https://internshala.com` | **Pending Partner** | Institutional University/Employer Agreement | 0 (No unauthorized scraping) |
| 8 | **Foundit (Monster)** | `https://www.foundit.in` | **Pending Partner** | Foundit Recruiter Commercial API | 0 (No unauthorized scraping) |
| 9 | **Apna** | `https://apna.co` | **Pending Partner** | Apna for Business Recruiter API | 0 (No unauthorized scraping) |
| 10 | **Cutshort** | `https://cutshort.io` | **Pending Partner** | Cutshort Enterprise Recruiter Gateway | 0 (No unauthorized scraping) |
| 11 | **National Career Service (NCS)** | `https://www.ncs.gov.in` | **Pending Partner** | Ministry of Labour & Employment Govt API | 0 (No unauthorized scraping) |
| 12 | **Apify India Jobs** | `https://apify.com` | **Pending Partner** | Paid Apify Actor Token (`APIFY_API_TOKEN`) | 0 (No unauthorized scraping) |

---

## 3. Location & Market Filtering

### 3.1 Country-Level Isolation
- `job_listings.country` added to database schema: `"India"` vs `"International"`.
- Default query `GET /api/v1/jobs` defaults strictly to `country="India"`.
- European and foreign listings are quarantined under the `International` filter and never bleed into Indian searches.

### 3.2 Indian City Hubs Supported
The location dropdown now explicitly supports Indian metropolitan tech clusters:
1. **India (Default - Country-wide)**: Aggregates across all Indian states.
2. **All Indian Cities**: Returns all domestic vacancies.
3. **Delhi NCR**: Aggregates Delhi, Noida, Greater Noida, Gurugram, Meerut.
4. **Noida, Delhi NCR**: Ingests direct engineering center vacancies in Noida.
5. **Greater Noida, Delhi NCR**: Ingests Greater Noida opportunities.
6. **Gurugram, Delhi NCR**: Ingests MongoDB, Databricks, and tech listings in Gurugram.
7. **Meerut, Uttar Pradesh**: Regional UP NCR opportunities.
8. **Bengaluru, Karnataka**: Silicon Valley of India (MongoDB, InMobi, Databricks, Rubrik, Okta, Samsara, Datadog).
9. **Hyderabad, Telangana**: HITEC City technology postings.
10. **Pune, Maharashtra**: Magarpatta & Hinjewadi engineering listings.
11. **Mumbai, Maharashtra**: Financial and enterprise tech centers.
12. **Chennai, Tamil Nadu**: OMR tech corridor postings.
13. **Kolkata, West Bengal**: Salt Lake Sector V technology postings.
14. **Jaipur, Lucknow, Ahmedabad, Chandigarh**: Tier-2 emerging innovation hubs.
15. **International**: Separates Europe, Germany, and overseas remote postings.

---

## 4. Role-Based Search & Specializations

Interactive role pills enable single-click filtering across primary technical specializations:
- **AI Engineer**: Machine Learning, Python, PyTorch, LLMs, Deep Learning, Data Modeling.
- **Machine Learning Engineer**: ML pipelines, model deployment, algorithms.
- **Data Scientist**: Statistical analysis, Python, Pandas, feature engineering.
- **Data Analyst**: SQL, Tableau, PowerBI, business analytics, Python.
- **Python Developer**: FastAPI, Django, REST APIs, Git, database querying.
- **Java Developer**: Spring Boot, microservices, Hibernate, system architecture.
- **Software Engineer / Application Engineer**: Distributed systems, REST APIs, problem solving.
- **Frontend Developer**: React, Next.js, TypeScript, Tailwind CSS, web performance.
- **Backend Developer**: Microservices, PostgreSQL, distributed systems, API architecture.
- **Full Stack Developer**: End-to-end React, Node.js, TypeScript, relational databases.
- **DevOps Engineer**: Kubernetes, Docker, CI/CD, AWS, Terraform, Linux.
- **Cloud Engineer**: Cloud architecture, AWS / GCP, IAM, scalable infrastructure.
- **Cybersecurity Analyst**: Security operations, vulnerability assessment, IAM, SIEM.
- **Business Analyst**: Requirements engineering, agile workflows, data modeling.
- **UI/UX Designer**: Figma, wireframing, user research, design systems.
- **Internships**: Entry-level trade apprenticeships and technical university internships.
- **Fresher Jobs**: 0-1 year experience threshold for college graduates.

---

## 5. Transparent Data Quality & Explainable AI Matching

### 5.1 Transparent Empty State
When a narrow search combination yields zero results (e.g. searching for a non-existent role in a specific city), the system displays:
> **"No verified Indian vacancies found for this search. Try another role or location."**  
> *With a one-click button to "Reset to All Indian Vacancies".*

The platform **never** silently substitutes German or foreign jobs into an Indian search.

### 5.2 Explainable AI Compatibility Scores
Every card displays an explainable compatibility breakdown:
- **Dynamic Match Score (0–100%)**: Calculated by comparing candidate verified competencies (from NSQF / BGE embedding extraction) against job skill requirements.
- **Matching Verified Skills**: List of candidate competencies matching job requirements.
- **Missing Required Skills / Bridge Competencies**: Identified skill gaps required for target role.
- **Experience Alignment**: Years of experience compared to job seniority requirement.
- **Direct External Application Guarantee**: Clicking "Apply on Original Website" opens the genuine external employer career portal (`window.open(job.application_url, '_blank')`). Zero fake submissions.

---

## 6. Verification & Test Evidence

### 6.1 Pytest Suite Results
Executed:
`DATABASE_URL="sqlite:///./elevate_x_local.db" python3 -m pytest tests/test_india_job_ingestion.py tests/test_multi_source_job_aggregator.py -v`

```
tests/test_india_job_ingestion.py::test_1_authorized_feeds_ingests_authentic_indian_tech_jobs PASSED [  6%]
tests/test_india_job_ingestion.py::test_2_api_defaults_to_india_jobs PASSED [ 12%]
tests/test_india_job_ingestion.py::test_3_city_level_filtering_bengaluru_and_delhi_ncr PASSED [ 18%]
tests/test_india_job_ingestion.py::test_4_international_filter_isolates_overseas_vacancies PASSED [ 25%]
tests/test_india_job_ingestion.py::test_5_role_category_search_ai_and_python PASSED [ 31%]
tests/test_india_job_ingestion.py::test_6_explainable_ai_matching_breakdown PASSED [ 37%]
tests/test_india_job_ingestion.py::test_7_transparent_empty_state_for_narrow_queries PASSED [ 43%]
tests/test_india_job_ingestion.py::test_8_direct_application_url_fidelity PASSED [ 50%]
tests/test_multi_source_job_aggregator.py::test_1_provider_metadata_and_documentation PASSED [ 56%]
tests/test_multi_source_job_aggregator.py::test_2_authorized_feeds_real_ingestion PASSED [ 62%]
tests/test_multi_source_job_aggregator.py::test_3_duplicate_detection_and_sync PASSED [ 68%]
tests/test_multi_source_job_aggregator.py::test_4_original_url_preservation_and_application_link PASSED [ 75%]
tests/test_multi_source_job_aggregator.py::test_5_ai_explainable_compatibility_matching PASSED [ 81%]
tests/test_multi_source_job_aggregator.py::test_6_multifaceted_filtering_endpoints PASSED [ 87%]
tests/test_multi_source_job_aggregator.py::test_7_saved_jobs_bookmarking_lifecycle PASSED [ 93%]
tests/test_multi_source_job_aggregator.py::test_8_expired_listing_cleanup PASSED [100%]

======================= 16 passed in 19.85s =======================
```

### 6.2 TypeScript Compilation
Executed:
`npx tsc --noEmit`  
**Result:** Clean build, 0 errors.

---

## 7. Modified & Created Files

1. [adapters.py](file:///Users/ayushgupta/Desktop/Resume_Ai/backend/app/services/job_aggregator/adapters.py) — Implemented India tech employer Greenhouse ATS feeds, location normalization, role skills extraction, and Adzuna/Jooble India metadata.
2. [aggregator_service.py](file:///Users/ayushgupta/Desktop/Resume_Ai/backend/app/services/job_aggregator/aggregator_service.py) — Integrated `country` field persistence and provider count tracking.
3. [job.py](file:///Users/ayushgupta/Desktop/Resume_Ai/backend/app/models/job.py) — Added `country` column with default `'India'`.
4. [career_domain.py](file:///Users/ayushgupta/Desktop/Resume_Ai/backend/app/schemas/career_domain.py) — Added `country` to `JobListingCreate` and `JobListingResponse`.
5. [jobs.py](file:///Users/ayushgupta/Desktop/Resume_Ai/backend/app/api/v1/jobs.py) — Implemented default India filtering, city aliases (`Delhi NCR`, `Bengaluru`, `Gurugram`, `Noida`), role categories, and isolated `International` filter.
6. [find-jobs/page.tsx](file:///Users/ayushgupta/Desktop/Resume_Ai/src/app/find-jobs/page.tsx) — Replaced German dropdown with Indian cities, added role category filter pills, transparent empty states, and India Verified badges.
7. [api-service.ts](file:///Users/ayushgupta/Desktop/Resume_Ai/src/services/api-service.ts) — Extended `getAggregatedJobs` parameters with `country` and `role_category`.
8. [types/index.ts](file:///Users/ayushgupta/Desktop/Resume_Ai/src/types/index.ts) — Added `country` to `AggregatedJobListing`.
9. [test_india_job_ingestion.py](file:///Users/ayushgupta/Desktop/Resume_Ai/backend/tests/test_india_job_ingestion.py) — 8 new end-to-end tests for India-first ingestion, role search, and data quality.
10. [test_multi_source_job_aggregator.py](file:///Users/ayushgupta/Desktop/Resume_Ai/backend/tests/test_multi_source_job_aggregator.py) — Verified all 8 multi-source aggregator tests pass.
