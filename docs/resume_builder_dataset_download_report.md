# Elevate X AI — Resume Builder Dataset Acquisition & Verification Report

**Project:** Elevate X AI — AI-Powered Multilingual Skill Verification & Career Platform  
**Component:** Resume Builder & Job-Resume Alignment Datasets  
**Execution Date:** November 21, 2026  
**Execution Environment:** macOS, Apple Silicon MPS, Python 3.13  
**Task Type:** Dataset Acquisition & Integrity Verification ONLY (No Model Training or Code Changes)  

---

## 1. Executive Summary & Verification Overview

All four target Hugging Face datasets have been successfully downloaded, cryptographically verified, cataloged, and organized into the designated repository structure:

```
datasets/resume_builder/
├── raw/                                 # Quarantined raw datasets (Git-ignored)
│   ├── structured_resumes/             # uhfew/resumes
│   ├── job_resume_matching/            # Shresth786/job-resume-matching
│   ├── job_resume_fit/                 # harsh72877287/job_resume_fit
│   └── resume_score_details/           # vadimas22/resume-score-details
├── metadata/                            # Manifests & upstream dataset cards
├── audit/                               # Checksum, integrity & privacy reports
└── README.md
```

### Dataset Acquisition Status Board

| Dataset ID | Destination Directory | Files Verified | Record / Row Count | Total Size | Primary Status |
|---|---|---|---|---|---|
| **`uhfew/resumes`** | `raw/structured_resumes/` | 3 / 3 | **4,817** JSONL records | 16.33 MB | **DOWNLOADED AND VERIFIED** |
| **`Shresth786/job-resume-matching`** | `raw/job_resume_matching/` | 5 / 5 | **122,560** Match pairs<br>(9,544 CVs, 1,167 Jobs) | 246.66 MB | **DOWNLOADED AND VERIFIED** |
| **`harsh72877287/job_resume_fit`** | `raw/job_resume_fit/` | 3 / 3 | **2,385** CSV rows | 30.50 MB | **DOWNLOADED AND VERIFIED**<br>*(QUARANTINED FOR TRAINING)* |
| **`vadimas22/resume-score-details`** | `raw/resume_score_details/` | 1,034 / 1,034 | **1,031** JSON samples | 13.69 MB | **DOWNLOADED AND VERIFIED**<br>*(LICENSE REVIEW REQUIRED)* |

**Total Data Volume:** **1,045 files**, **307.18 MB** stored in `datasets/resume_builder/`.  
**Disk Space Verification:** Available volume capacity remained healthy at **17 GiB** (used less than 2% of available space).

---

## 2. Dataset 1 — Structured Resumes (`uhfew/resumes`)

- **Hugging Face Repository:** [uhfew/resumes](https://huggingface.co/datasets/uhfew/resumes)
- **Destination:** `datasets/resume_builder/raw/structured_resumes/`
- **Declared License:** **MIT**
- **Status:** **DOWNLOADED AND VERIFIED**
- **Verified Record Count:** **4,817 structured resume records**

### 2.1 File Inventory & Integrity

| File Name | File Size (Bytes) | SHA-256 Checksum | Integrity Status |
|---|---|---|---|
| `master_resumes.jsonl` | 16,324,910 | `b8cb2810a5868dc03a6ab4ba49c495316d280996ce28d2ace97be1e0b6bda136` | Verified OK |
| `README.md` | 5,953 | `ac759bde480f6b2cd7a8174ccd0c7d3aad3f33b297932c6c854934eaf4bbbb05` | Verified OK |
| `.gitattributes` | 2,518 | `71fb723fd7cdf0fd5bf65d6bf47786b85a33935fee60ec77317030ec45f66659` | Verified OK |

### 2.2 Content & Structure Audit
Every single record was parsed. All 4,817 records consistently contain:
- `experience`: 4,817 / 4,817 (100%)
- `education`: 4,817 / 4,817 (100%)
- `skills`: 4,817 / 4,817 (100%)
- `certifications`: 4,817 / 4,817 (100%)
- `personal_info`: 4,816 / 4,817 (99.98%)

### 2.3 Provenance & Privacy Analysis
- **Data Type:** Mixed (Template-generated layout combined with realistic profile narratives).
- **PII Scan:** 4,607 email patterns, 4,607 phone number patterns, 4,610 LinkedIn URLs, and 4,652 names were identified.
- **Action:** Retained under quarantined raw directory; requires field redaction before any model fine-tuning.

---

## 3. Dataset 2 — Job Resume Matching (`Shresth786/job-resume-matching`)

- **Hugging Face Repository:** [Shresth786/job-resume-matching](https://huggingface.co/datasets/Shresth786/job-resume-matching)
- **Destination:** `datasets/resume_builder/raw/job_resume_matching/`
- **Declared License:** **MIT**
- **Status:** **DOWNLOADED AND VERIFIED**
- **Verified Record Counts:**
  - `cv.csv`: **9,544** candidate resumes
  - `job.csv`: **1,167** job postings
  - `matches.csv`: **122,560** candidate-job match evaluations

### 3.1 File Inventory & Integrity

| File Name | File Size (Bytes) | SHA-256 Checksum | Integrity Status |
|---|---|---|---|
| `cv.csv` | 194,020,617 (194.0 MB) | `67c81a4761516113dbebcd8c6acc1b692c4b20e54341187ff864d2d637099640` | Verified OK |
| `job.csv` | 32,930,476 (32.9 MB) | `301a382ebec72d574817cc3d4b9ee34cf08e7f8ecdfa3d373142767fe4f9f789` | Verified OK |
| `matches.csv` | 19,704,065 (19.7 MB) | `4ae60b5b134146235148557268c5e04f1fc5e7579b73c4ab59cb01073bce3338` | Verified OK |
| `README.md` | 9,935 | `5f0bece48a666e722f9780d349de60a6242297c46a2e78c83e4206dfc3852a2f` | Verified OK |
| `.gitattributes` | 2,639 | `8112ea19544538569a4d8ec93cfd0b9cec8a7321c46f135298a987f5ed4f410a` | Verified OK |

### 3.2 Technical Schema Mismatch Resolution
- **Issue in Hugging Face Viewer:** The Hugging Face dataset viewer fails because `cv.csv` (11 columns: `candidate_id`, `target_position`, `resume_text`, `clean_skills`, etc.) and `job.csv` (10 columns: `job_id`, `job_title`, `category`, `job_description`, etc.) have different schemas, which causes `datasets.load_dataset()` to throw an automatic schema union error.
- **Resolution:** By bypassing generic Hugging Face loaders and streaming each CSV individually via targeted HTTP requests, the original CSV files were downloaded with **zero data loss, zero altered columns, and zero dropped rows**.

---

## 4. Dataset 3 — Job Resume Fit (`harsh72877287/job_resume_fit`)

- **Hugging Face Repository:** [harsh72877287/job_resume_fit](https://huggingface.co/datasets/harsh72877287/job_resume_fit)
- **Destination:** `datasets/resume_builder/raw/job_resume_fit/`
- **Declared License:** **"other"**
- **Status:** **DOWNLOADED AND VERIFIED** *(QUARANTINED FOR TRAINING)*
- **Verified Record Count:** **2,385 rows**, 10 columns

### 4.1 File Inventory & Integrity

| File Name | File Size (Bytes) | SHA-256 Checksum | Integrity Status |
|---|---|---|---|
| `job_resume_fit.csv` | 30,498,433 (30.5 MB) | `ca0cb5d0bf93cce1d2ee448c4146a84c68832103f69904d9c02ff597c0f18833` | Verified OK |
| `README.md` | 1,364 | `3ecfaec5695cf643f82cb5ff1170725b84784a60037ebaa50e4a7a8d5c43d79e` | Verified OK |
| `.gitattributes` | 2,516 | `5a7f920fbbad9e634eb7b61ea553c3065a467f33221bfca752670d9703f848ce` | Verified OK |

### 4.2 Quarantine Justification & Licensing Warning
- **License Status:** The upstream repository marks the license as `"other"`. There is no formal license grant, author attribution, or terms of commercial use in the repository card.
- **Upstream Source Audit:** The dataset contains scraped job descriptions and candidate resumes. Because provenance is unverified and permissions are unclear, this dataset is formally marked:
  > **STATUS: QUARANTINED FOR TRAINING / LICENSE REVIEW REQUIRED**  
  > It may be used strictly for internal inspection, schema research, and offline feature evaluation, but must NOT be incorporated into production model weights.

---

## 5. Dataset 4 — Resume Score Details (`vadimas22/resume-score-details`)

- **Hugging Face Repository:** [vadimas22/resume-score-details](https://huggingface.co/datasets/vadimas22/resume-score-details)
- **Destination:** `datasets/resume_builder/raw/resume_score_details/`
- **Declared License:** **"cc" (Creative Commons)**
- **Status:** **DOWNLOADED AND VERIFIED** *(AI-GENERATED ASSESSMENTS / LICENSE REVIEW REQUIRED)*
- **Verified Total Files:** **1,034 files** (1,031 JSON samples, 1 dataset card YAML, 1 README, 1 gitattributes)

### 5.1 Structure & Viewer Failure Analysis
- **Hugging Face Viewer Inconsistency:** The Hugging Face viewer fails because the author stored each record as an individual JSON file in the repository root rather than in a consolidated table, and files have varying nested schemas (`match_*`, `mismatch_*`, `invalid_*`, `empty_*`).
- **Resolution:** All 1,034 individual files were acquired and verified with 100% completeness.

### 5.2 Exact Composition Breakdown

| Sample Category | File Prefix | Sample Count | Verified Structure |
|---|---|---|---|
| **Matched Records** | `match_*.json` | **648** | Complete resume, job description, and scoring rationale |
| **Mismatched Records** | `mismatch_*.json` | **201** | Negative pairings with gap explanations |
| **Invalid Records** | `invalid_*.json` | **142** | Synthetically degraded or gibberish test cases |
| **Empty Additional Info** | `empty_additional_info_*.json` | **40** | Resumes missing ancillary profile fields |
| **Total Evaluation Samples** | — | **1,031** | Total JSON sample files |

### 5.3 Provenance & AI-Generated Assessment Warning
- **AI Assessment Disclaimer:** The dataset documentation explicitly notes that all resume-job alignment scores and explanatory text were **generated by OpenAI GPT-4o**:
  > *"This dataset contains resume score details generated by GPT-4o..."*
- **Governance Impact:** These scores represent **model-generated predictions**, not verified human recruiter assessments. They cannot be treated as gold-standard recruiter ground truth for evaluating human hiring alignment.
- **Licensing Constraint:** Declared as `"cc"`. A formal legal review of Creative Commons terms and OpenAI model output licensing policies is required before any commercial usage.

---

## 6. Git Hygiene & Project Safety Confirmation

To protect the Elevate X AI repository integrity:
1. **Git Tracking Protection:** `.gitignore` was updated to explicitly ignore `datasets/resume_builder/raw/`, ensuring none of the 307 MB of raw datasets or PII are committed to Git.
2. **Untouched Features:** Feature 1, Feature 2, existing model weights, API routes, database schemas, and frontend interfaces were completely untouched during this operation.
3. **No Training Executed:** Zero model training, fine-tuning, or inference parameter modifications took place.
