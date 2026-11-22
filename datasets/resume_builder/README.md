# Elevate X AI — Resume Builder & Matching Datasets

This directory contains external reference and research datasets for **Elevate X AI — Resume Builder & Career Ecosystem**.

> **GOVERNANCE POLICY:**  
> These raw datasets are acquired strictly for offline research, schema modeling, ontology crosswalks, and benchmarking.  
> Under no circumstances may raw datasets containing unverified personal information (PII) or restrictive licenses be directly fed into production training pipelines without sanitization and formal legal review.  
> All raw data files are quarantined under `raw/` and excluded from Git tracking via `.gitignore`.

---

## 1. Directory Structure

```
datasets/resume_builder/
├── raw/                                 # Quarantined raw datasets (Git-ignored)
│   ├── structured_resumes/             # uhfew/resumes (4,817 structured JSONL records)
│   ├── job_resume_matching/            # Shresth786/job-resume-matching (cv, job, matches CSVs)
│   ├── job_resume_fit/                 # harsh72877287/job_resume_fit (2,385 fit rows)
│   └── resume_score_details/           # vadimas22/resume-score-details (1,031 GPT-4o JSON samples)
├── metadata/                            # Dataset cards, upstream manifests, and metadata
│   ├── dataset_manifest.json           # Comprehensive dataset manifest with SHA-256 hashes
│   ├── structured_resumes_metadata.json
│   ├── job_resume_matching_metadata.json
│   ├── job_resume_fit_metadata.json
│   └── resume_score_details_metadata.json
├── audit/                               # Security, privacy, and integrity reports
│   ├── download_integrity_report.json  # Checksum, row count, and byte verification
│   └── privacy_license_audit.md        # PII exposure and license status audit
└── README.md                            # Directory documentation (this file)
```

---

## 2. Acquired Datasets Summary

| Dataset ID | Purpose | Records / Size | Status | License |
|---|---|---|---|---|
| **`uhfew/resumes`** | Structured resume parsing, section modeling, skills & certifications | 4,817 records / 16.3 MB | **DOWNLOADED AND VERIFIED** | MIT (Permissive) |
| **`Shresth786/job-resume-matching`** | Multi-table CV, Job description, and matching pairs | 9,544 CVs, 1,167 Jobs, 122,560 Matches / 246.6 MB | **DOWNLOADED AND VERIFIED** | MIT (Permissive) |
| **`harsh72877287/job_resume_fit`** | Resume-job fit score and skill overlap | 2,385 rows / 30.5 MB | **QUARANTINED FOR TRAINING** | "other" (Review Required) |
| **`vadimas22/resume-score-details`** | AI-generated resume scoring rationales & feedback | 1,031 samples (1,034 files) / 13.7 MB | **LICENSE REVIEW REQUIRED** | CC (AI-Generated Assessments) |

---

## 3. Usage & Access Guidelines

1. **No Application Coupling:** The active Next.js frontend and FastAPI backend operate independently of these raw research datasets.
2. **PII Sanitization:** The raw files contain contact information, email addresses, and phone numbers. Any transformation pipeline must redact sensitive fields before creating training tensors.
3. **Upstream Attribution:** All dataset cards and upstream authorship details are archived in `metadata/`.
