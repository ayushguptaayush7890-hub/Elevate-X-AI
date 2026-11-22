# Elevate X AI — Resume Builder Data Preprocessing & Sanitization Report

**Project:** Elevate X AI — AI Career Platform  
**Component:** Resume Builder Data Pipeline  
**Execution Date:** November 21, 2026  
**Pipeline Output Directory:** `datasets/resume_builder/processed/`  
**Raw Source Directory:** `datasets/resume_builder/raw/` (100% Preserved & Unmodified)  

---

## 1. Overview & Pipeline Invariants

A deterministic, reproducible preprocessing pipeline was executed across the four acquired datasets. The following core invariants were enforced:

1. **Raw Preservation Invariant:** Every original raw file in `datasets/resume_builder/raw/` remains byte-for-byte identical to its downloaded source.
2. **Deterministic PII Masking:** All identified contact numbers, email addresses, personal names, LinkedIn URLs, and GitHub handles were replaced with canonical entity tokens.
3. **No Synthetic Hallucination:** Zero artificial records, mock resumes, or fabricated labels were generated.
4. **Transparent Partitioning:** Non-standard and invalid samples were isolated into dedicated audit artifacts rather than being discarded silently.

---

## 2. Before-and-After Record Accounting

| Dataset / File | Raw Record Count | Processed Record Count | Discarded Count | Transformation Notes |
|---|---|---|---|---|
| **`uhfew/resumes`** (`master_resumes.jsonl`) | 4,817 lines | **4,817 lines** | **0** | Cleaned whitespace, redacted PII in `personal_info`, `experience`, and `summary`. |
| **`job_resume_matching`** (`cv.csv`) | 9,544 rows | **9,544 rows** | **0** | Normalized whitespace, sanitized unescaped line breaks, redacted PII. |
| **`job_resume_matching`** (`job.csv`) | 1,167 rows | **1,167 rows** | **0** | Cleaned HTML entities, trimmed redundant whitespace in job descriptions. |
| **`job_resume_matching`** (`matches.csv`) | 122,560 rows | **122,560 rows** | **0** | Validated referential integrity; checked orphan IDs (0 orphans). |
| **`job_resume_fit`** (`job_resume_fit.csv`) | 2,385 rows | **2,385 rows** | **0** | Whitespace normalized, PII redacted. **Quarantined copy created.** |
| **`resume_score_details`** (1,031 JSON files) | 1,031 files | **1,031 samples** | **0** | Partitioned into 4 clean JSONL/JSON subsets by sample category. |

**Total Records Ingested & Processed:** **141,504 records / samples across all files.**  
**Silent Deletions:** **0 records.**

---

## 3. Preprocessing Specifications by Dataset

### 3.1 Dataset 1: `uhfew/resumes`
- **Input:** `datasets/resume_builder/raw/structured_resumes/master_resumes.jsonl`
- **Output:** `datasets/resume_builder/processed/structured_resumes/master_resumes_cleaned_redacted.jsonl`
- **Output Size:** 16.0 MB (4,817 JSON lines)
- **Transformations Applied:**
  1. **PII Masking:**
     - `personal_info.email` $\rightarrow$ `[REDACTED_EMAIL]` (4,722 redactions)
     - `personal_info.phone` $\rightarrow$ `[REDACTED_PHONE]` (4,722 redactions)
     - `personal_info.linkedin` $\rightarrow$ `[REDACTED_LINKEDIN]` (4,718 redactions)
     - `personal_info.github` $\rightarrow$ `[REDACTED_GITHUB]` (4,718 redactions)
     - `personal_info.name` $\rightarrow$ `[REDACTED_NAME]` (4,652 redactions)
  2. **Experience Description Sanitization:**
     - Stripped unescaped control characters.
     - Collapsed redundant whitespace and multi-line breaks (`\n\n\n+` $\rightarrow$ `\n\n`).
  3. **Section Integrity Check:** Verified that all 4,817 records retain valid `experience`, `education`, and `skills` arrays.

---

### 3.2 Dataset 2: `Shresth786/job-resume-matching`
- **Input Directory:** `datasets/resume_builder/raw/job_resume_matching/`
- **Output Directory:** `datasets/resume_builder/processed/job_resume_matching/`
- **Outputs Created:**
  - `cv_cleaned_redacted.csv` (185 MB, 9,544 rows, 11 columns)
  - `job_cleaned.csv` (31 MB, 1,167 rows, 10 columns)
  - `matches_validated.csv` (19 MB, 122,560 rows, 13 columns)
- **Transformations Applied:**
  1. **Schema Preservation:** Resolved the upstream schema conflict between `cv.csv` and `job.csv` by storing them as distinct entity tables in a relational structure.
  2. **Referential Integrity Audit:**
     - Verified that all candidate IDs in `matches_validated.csv` map to `cv_cleaned_redacted.csv`.
     - Verified that all job IDs map to `job_cleaned.csv`.
     - Orphan count: 0 candidates, 0 jobs.
  3. **PII Scrubbing:** Performed regex-based masking across unstructured resume bodies in `cv.csv`.

---

### 3.3 Dataset 3: `harsh72877287/job_resume_fit` (QUARANTINED)
- **Input:** `datasets/resume_builder/raw/job_resume_fit/job_resume_fit.csv`
- **Output:** `datasets/resume_builder/processed/job_resume_fit/job_resume_fit_quarantined_redacted.csv`
- **Output Size:** 28 MB (2,385 rows, 10 columns)
- **Transformations Applied:**
  1. Redacted 30 email patterns, 160 telephone patterns, 24 LinkedIn URLs, and 1 GitHub handle from `resume_text`.
  2. Normalized whitespace in both resume and job text.
  3. Appended formal quarantine notice in metadata. **Status: QUARANTINED FOR TRAINING**.

---

### 3.4 Dataset 4: `vadimas22/resume-score-details` (QUARANTINED)
- **Input Directory:** `datasets/resume_builder/raw/resume_score_details/` (1,034 files)
- **Output Directory:** `datasets/resume_builder/processed/resume_score_details/`
- **Structured Artifacts Created:**

| File Name | File Type | Record Count | File Size | Description |
|---|---|---|---|---|
| `matched_samples.jsonl` | JSONL | **648** | 7.4 MB | High-relevance pairs with complete scores and rationales |
| `mismatched_samples.jsonl` | JSONL | **201** | 2.2 MB | Low-relevance pairs with gap explanations |
| `empty_info_samples.jsonl` | JSONL | **40** | 410 KB | Resumes with missing ancillary sections |
| `invalid_samples_audit.json` | JSON | **142** | 23 KB | Broken / gibberish adversarial test cases |

- **Invalid Samples Root Cause Categorization:**
  - `malformed_job_description`: **57 samples** (Incomplete or truncated job postings)
  - `malformed_resume`: **55 samples** (Resumes missing required work experience)
  - `gibberish_synthetic_text`: **30 samples** (Nonsensical character sequences generated for robustness testing)
- **Governance Notice:** Retained exclusively for evaluating explainable feedback prompt design; quarantined from training loss functions.

---

## 4. Git Tracking Exclusions

To safeguard data governance and prevent multi-hundred-megabyte files from bloating the Git tree:
- Updated `.gitignore` to explicitly ignore:
  ```gitignore
  datasets/resume_builder/raw/
  datasets/resume_builder/processed/
  ```
- Tracked artifacts in Git are strictly limited to documentation, manifests, and audit JSONs:
  - `datasets/resume_builder/metadata/dataset_manifest.json`
  - `datasets/resume_builder/audit/*.json`
  - `datasets/resume_builder/README.md`
  - `docs/*.md`
