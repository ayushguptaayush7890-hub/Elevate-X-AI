# Elevate X AI — Resume Builder Dataset Quality & Integrity Audit

**Project:** Elevate X AI — AI Career Platform  
**Component:** Resume Builder & Intelligent Job-Resume Alignment  
**Audit Date:** November 21, 2026  
**Auditor:** Elevate X AI Autonomous Data Governance & ML Engineering Agent  
**Execution Environment:** macOS, Apple Silicon MPS, Python 3.13  

---

## 1. Executive Summary

A comprehensive quality audit was conducted across the four downloaded reference corpora residing in `datasets/resume_builder/raw/`. The audit evaluated schema integrity, section presence, missing fields, duplicate rates, synthetic markers, PII exposure, and task suitability.

### Key Audit Findings:

| Dataset ID | Records Inspected | Duplicate Count | Invalid / Malformed | PII Exposure Level | Governance Status |
|---|---|---|---|---|---|
| **`uhfew/resumes`** | 4,817 JSONL | 38 Exact<br>4,655 Template Duplicates | 0 Parse Errors | High (Contact metadata) | **APPROVED FOR RESEARCH (Redacted)** |
| **`Shresth786/job-resume-matching`** | 9,544 CVs<br>1,167 Jobs<br>122,560 Pairs | 0 Duplicate Pairs<br>0 Duplicate IDs | 0 Orphan IDs | Moderate (Unstructured CVs) | **APPROVED FOR MATCHING BENCHMARKS** |
| **`harsh72877287/job_resume_fit`** | 2,385 Rows | 2 Exact Pairs | 0 Parse Errors | Low-Moderate | **QUARANTINED FOR TRAINING** |
| **`vadimas22/resume-score-details`** | 1,031 Samples | 0 Duplicate Files | 142 Invalid / Gibberish | Low (Synthetic cases) | **QUARANTINED FOR TRAINING (AI-Generated)** |

---

## 2. Dataset 1 — Structured Resumes (`uhfew/resumes`)

- **File Inspected:** `master_resumes.jsonl` (16,324,910 bytes)
- **Total Records:** **4,817**
- **Format:** JSON Lines, nested dictionary schema.

### 2.1 Section Completeness Audit
Every single record was parsed and validated against the expected resume schema:

| Section Field | Present Records | Completeness Rate | Structural Notes |
|---|---|---|---|
| `experience` | 4,817 | **100.0%** | Array of dicts (`title`, `company`, `dates`, `description`) |
| `education` | 4,817 | **100.0%** | Array of dicts (`degree`, `institution`, `dates`) |
| `skills` | 4,817 | **100.0%** | Array of string skill tokens (median: 18 skills/record) |
| `certifications` | 4,817 | **100.0%** | Array of credential strings |
| `personal_info` | 4,816 | **99.98%** | Dict (`name`, `email`, `phone`, `location`, `links`) |
| `summary` | 3,842 | **79.76%** | Free-text executive summary paragraph |
| `projects` | 2,118 | **43.97%** | Optional portfolio / academic projects |
| `achievements` | 1,402 | **29.10%** | Optional award bullet points |

### 2.2 Synthetic vs. Real-World Extraction Analysis
- **Exact Duplicates:** 38 records have 100% identical byte-for-byte serialized JSON payloads.
- **Near-Duplicate Templates:** **4,655 out of 4,817 records (96.6%)** share identical syntactic structures in their job descriptions and timeline progressions, indicating that this dataset was produced using a **combinatorial template generator** with slot-filling over a curated terminology lexicon.
- **Implication:** While excellent for **section segmentation and entity labeling**, it lacks the natural syntactic variance of free-form human resumes.

### 2.3 PII Scan & Redaction
- **Detected PII:** 4,607 standard emails, 4,607 phone numbers, 4,610 LinkedIn URLs, 4,617 GitHub handles, and 4,652 personal names.
- **Redaction Applied:** All personal identifiers in `master_resumes_cleaned_redacted.jsonl` were replaced with canonical masking tokens (`[REDACTED_EMAIL]`, `[REDACTED_PHONE]`, `[REDACTED_LINKEDIN]`, `[REDACTED_GITHUB]`, `[REDACTED_NAME]`).

---

## 3. Dataset 2 — Job Resume Matching (`Shresth786/job-resume-matching`)

- **Files Inspected:** `cv.csv` (194 MB), `job.csv` (32.9 MB), `matches.csv` (19.7 MB)
- **Record Counts:** 9,544 candidates, 1,167 job postings, 122,560 pairing evaluations.

### 3.1 Referential Integrity & Bipartite Graph Structure
- **Candidate Integrity:** All 122,560 records in `matches.csv` reference a valid `candidate_id` in `cv.csv`. **Orphan candidates: 0**.
- **Job Integrity:** All 122,560 records reference a valid `job_id` in `job.csv`. **Orphan jobs: 0**.
- **Bipartite Density:** On average, each job posting is linked to **105 candidate resumes**, creating a dense candidate-ranking graph.
- **Duplicate Pairs:** **0 duplicate `(candidate_id, job_id)` pairs** exist.

### 3.2 Match Label Quality & Mechanical Stratification Analysis
An inspection of `final_score` and `label_strength` revealed that the labels **are not human recruiter evaluations**:
- **Distribution:**
  - `medium_positive`: **70,636 pairs (57.64%)** — Final score $[0.40, 0.70)$
  - `weak_positive`: **51,150 pairs (41.74%)** — Final score $[0.10, 0.40)$
  - `strong_positive`: **774 pairs (0.63%)** — Final score $\ge 0.70$
  - `negative` / `mismatch`: **0 pairs (0.0%)**
- **Critical Finding:** The dataset has **zero negative examples**. All pairings are stratified strictly by mechanical TF-IDF/embeddings similarity thresholds into three positive buckets.
- **Risk:** Training a binary match/mismatch classifier directly on this dataset without generating hard negative pairs will cause severe false-positive bias.

---

## 4. Dataset 3 — Job Resume Fit (`harsh72877287/job_resume_fit`)

- **File Inspected:** `job_resume_fit.csv` (30.5 MB, 2,385 rows, 10 columns)
- **Status:** **QUARANTINED FOR TRAINING**

### 4.1 Schema & Score Audit
The dataset pairs raw resume text with scraped job postings and computes three similarity metrics:
- `ai_match_score`: Ranging from $0.0$ to $100.0$ (mean: $62.4$, std: $14.2$).
- `skill_string_match_score`: Token intersection percentage.
- `fuzzy_match_score`: Levenshtein distance ratio.

### 4.2 Quality & Missing Value Audit
- Missing `category`: 12 rows.
- Empty `ai_matched_skills`: 10 rows.
- Duplicate pairs: 2 exact duplicates.

### 4.3 Quarantine Justification
The declared license is `"other"` with zero terms provided. Upstream provenance cannot be confirmed. To protect Elevate X AI intellectual property and prevent licensing taint, this dataset is **quarantined from production training pipelines**.

---

## 5. Dataset 4 — Resume Score Details (`vadimas22/resume-score-details`)

- **Total Samples Inspected:** 1,031 JSON files (13.7 MB)
- **Status:** **QUARANTINED FOR TRAINING (AI-Generated Assessments)**

### 5.1 Partition Breakdown

| Partition | File Prefix | Count | Description & Characteristics |
|---|---|---|---|
| **Matched** | `match_*.json` | **648** | Complete resume + JD with positive evaluation score ($>70$) |
| **Mismatched** | `mismatch_*.json` | **201** | Resume + JD with negative score ($<40$) and skill gap explanation |
| **Invalid / Adversarial** | `invalid_*.json` | **142** | Intentionally broken test cases (30 gibberish, 57 malformed JDs, 55 malformed resumes) |
| **Empty Additional Info** | `empty_additional_info_*.json` | **40** | Resumes lacking certifications or ancillary sections |

### 5.2 AI-Generated Assessment Warning
- **Model Provenance:** All scores, feedback rationales, and evaluation metrics were generated by **OpenAI GPT-4o**.
- **Self-Preference Loop Risk:** Using GPT-4o outputs to train an automated resume scorer risks circular confirmation bias. These labels are valuable as **demonstration explanations** for ATS feedback UI, but **cannot be used as ground-truth candidate selection labels**.

---

## 6. Cross-Dataset Leakage & Disjoint Splitting Strategy

### 6.1 Cross-Dataset Overlap Scan
Hash comparisons were executed across all four datasets:
- Overlap between Dataset 1 resumes and Dataset 2 CVs: **0 matches**.
- Overlap between Dataset 2 jobs and Dataset 3 jobs: **0 matches**.
- Conclusion: The four corpora represent completely disjoint upstream collections.

### 6.2 Data Leakage Prevention in Matching Models
Because Dataset 2 contains 122,560 pairs across 1,167 jobs:
- A standard random $k$-fold cross-validation will cause **severe data leakage**: candidate resumes will be tested against job descriptions the model has already memorized during training.
- **Mandatory Splitting Strategy:** **Disjoint GroupKFold by Entity ID**.
  $$\text{Split Criteria: } \text{Jobs}_{\text{train}} \cap \text{Jobs}_{\text{test}} = \emptyset \quad \text{AND} \quad \text{Candidates}_{\text{train}} \cap \text{Candidates}_{\text{test}} = \emptyset$$
  No candidate and no job description may appear in both the training and evaluation splits.

---

## 7. Dataset Suitability Matrix

| Task / Capability | `uhfew/resumes` | `Shresth786` | `harsh72877287` | `vadimas22` |
|---|---|---|---|---|
| **A. Resume Parsing** | **HIGH (Optimal)** | MEDIUM | LOW | LOW |
| **B. Section Classification** | **HIGH (Optimal)** | LOW | LOW | LOW |
| **C. Skill Extraction** | **HIGH** | **HIGH** | MEDIUM | MEDIUM |
| **D. Job Description Parsing** | LOW (No JDs) | **HIGH (Optimal)** | MEDIUM | MEDIUM |
| **E. Resume-Job Matching** | NOT SUITABLE | **HIGH (With Negatives)** | QUARANTINED | QUARANTINED |
| **F. ATS Scoring & Explanations** | LOW | MEDIUM | QUARANTINED | **HIGH (Feedback UI)** |
| **G. Resume Generation** | **HIGH (Optimal)** | MEDIUM | QUARANTINED | LOW |
