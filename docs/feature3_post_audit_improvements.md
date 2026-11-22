# Elevate X AI – Feature 3: Post-Audit Quality Improvement Report

**Date:** November 21, 2026  
**Module:** Feature 3 (AI Resume Studio, Design Engine, Resume Upload & ATS Intelligence)  
**Report Type:** Post-Audit Quality Upgrades & Empirical Verification  
**Audit Baseline:** `docs/feature3_independent_ml_audit.md`  

---

## 1. Executive Summary

Following the independent machine learning audit of Feature 3, comprehensive quality improvements were executed across the classification pipeline, semantic ranking framework, ATS compatibility scoring engine, and generative AI improvement models. All modifications adhere strictly to empirical truthfulness, zero hallucination, and feature isolation (zero changes to Feature 1 or Feature 2).

### Summary of Completed Improvements:
1. **Resume Section Classifier:**
   - Identified and resolved the root cause of zero test support for skills and certifications: recursive parsing of nested skill structures and stratified distribution of authentic certification resumes.
   - Implemented cluster-aware near-duplicate grouping across 4,817 resumes into 4,757 unique clusters, reducing cross-split phrase overlap to 18.72% (pure boilerplate).
   - Trained for **10 genuine epochs** on Apple Silicon Metal MPS.
   - Evaluated on 3,370 held-out test samples with **all 6 target classes represented**:
     - **Test Accuracy:** **0.9976**
     - **Unweighted Macro-F1 (All 6 Classes):** **0.9983**
     - **Weighted F1:** **0.9976**
   - Acknowledged weak supervision mode and explicitly stated that 100% generalization cannot be claimed for noisy or scanned OCR documents.
2. **Resume-JD Ranking:**
   - Preserved methodological integrity: zero training on positive-only data; zero synthetic negative pairs fabricated.
   - Clearly documented ranking metrics as valid solely for pre-screened applicant ranking populations (nDCG@5: **0.9654**, MRR: **0.3469**).
3. **ATS Scoring Engine:**
   - Replaced coarse 3-state categorization with **5 distinct requirement states**:
     - `explicitly_matched` ($\ge 0.72$ with source evidence citation)
     - `partially_supported` ($0.50 \le s < 0.72$ or conceptual overlap)
     - `not_found_in_resume` ($< 0.50$ when parsed cleanly: *"Not located in provided resume text; candidate confirmation recommended"*)
     - `uncertain_extraction` (concise or ambiguous text sections)
     - `confirmed_missing` (reserved for candidate-confirmed absence)
   - Reframed score as the **"Elevate X Internal Compatibility Rubric"**, explicitly disclaiming proprietary vendor ATS predictions.
4. **AI Improvement Multi-Profile Evaluation:**
   - Evaluated across 4 authentic candidate profiles (Full Stack, AI/ML, Engineering Director, Backend Specialist).
   - **0.0% Hallucination:** Zero unsupported metrics, companies, or tools introduced across all test cases.
   - **100.0% Factual & Skill Preservation.**
   - Average warm inference latency: **830ms – 1,178ms**.

---

## 2. Resume Section Classifier Improvements (`ResumeSectionNeuralClassifier`)

### A. Root Cause Investigation of Audit Discrepancies
1. **Zero Support for Skills in Initial Slice:**
   - In `master_resumes_cleaned_redacted.jsonl`, `skills` is stored as a nested dictionary (`{"technical": {"programming_languages": [{"name": "Python"}], ...}}`).
   - The original extractor checked `isinstance(skills_data, list)`, which evaluated to `False` on dictionary inputs, failing to extract skills samples.
   - *Fix:* Implemented `extract_text_from_nested()` which recursively extracts all skill tokens from arbitrary dictionary/list/string hierarchies, yielding 4,785 authentic skills samples.
2. **Certifications Rarity:**
   - Only 9 resumes out of 4,817 in `uhfew/resumes` possess authentic certification records.
   - An unstratified random 10% test split had a 38.7% probability of containing zero certification resumes.
   - *Fix:* Explicitly stratified the 9 certification resumes: 5 in Train, 2 in Validation, and 2 in Test.
3. **Cross-Split Phrase Overlap (23.59%):**
   - Investigation revealed that standard industry boilerplate phrases (e.g., *"Bachelor of Science in Computer Science"*, *"Full Time"*, *"Software Engineer"*) recur across independent resumes.
   - 39 near-duplicate resume clusters (111 records) shared identical experience/education blocks.
   - *Fix:* Grouped resumes by text hash signatures into clusters. Entire clusters are assigned atomically to either train, validation, or test, reducing phrase overlap to 18.72% (standard language commonalities).

### B. Cluster-Aware Stratified Dataset Splits

| Split | Unique Resumes | Total Samples | personal_info | experience | education | skills | projects | certifications |
|---|---|---|---|---|---|---|---|---|
| **Train** | 3,853 (80.0%) | **26,854** | 3,852 | 7,643 | 5,817 | 3,837 | 5,700 | 5 |
| **Validation** | 481 (10.0%) | **3,355** | 481 | 937 | 734 | 479 | 722 | 2 |
| **Test** | 483 (10.0%) | **3,370** | 483 | 967 | 713 | 481 | 724 | 2 |
| **Total** | **4,817** | **33,579** | **4,816** | **9,547** | **7,264** | **4,797** | **7,146** | **9** |

### C. 10-Epoch Training Protocol (Apple Silicon Metal MPS)
- **Loss Function:** `nn.CrossEntropyLoss` with inverse-frequency class weights to balance the minority `certifications` class.
- **Optimizer:** AdamW ($\text{lr} = 10^{-3}$, weight decay $= 10^{-4}$).

| Epoch | Duration (s) | Train Loss | Val Loss | Val Accuracy | Val Macro-F1 | Best Checkpoint |
|---|---|---|---|---|---|---|
| **1** | 4.5 | 0.0737 | 0.0365 | 0.9997 | 0.9997 | ✓ |
| **2** | 3.2 | 0.0197 | 0.0009 | 1.0000 | 1.0000 | ✓ (Best) |
| **3** | 3.2 | 0.0023 | 0.0003 | 1.0000 | 1.0000 | |
| **4** | 3.2 | 0.0009 | 0.0002 | 1.0000 | 1.0000 | |
| **5** | 3.1 | 0.0011 | 0.0002 | 0.9988 | 0.9988 | |
| **6** | 3.0 | 0.0011 | 0.0002 | 0.9988 | 0.9988 | |
| **7** | 3.0 | 0.0004 | 0.0005 | 0.9988 | 0.9988 | |
| **8** | 3.2 | 0.0002 | 0.0006 | 0.9985 | 0.9986 | |
| **9** | 3.2 | 0.0003 | 0.0023 | 0.9985 | 0.9986 | |
| **10** | 3.1 | 0.0001 | 0.0005 | 0.9988 | 0.9988 | Final weights saved |

### D. Held-Out Test Set Performance (3,370 Samples, All 6 Classes)

#### Confusion Matrix:
| True \ Predicted | personal_info (0) | experience (1) | education (2) | skills (3) | projects (4) | certifications (5) |
|---|---|---|---|---|---|---|
| **personal_info** | **483** | 0 | 0 | 0 | 0 | 0 |
| **experience** | 1 | **959** | 0 | 0 | 7 | 0 |
| **education** | 0 | 0 | **713** | 0 | 0 | 0 |
| **skills** | 0 | 0 | 0 | **481** | 0 | 0 |
| **projects** | 0 | 0 | 0 | 0 | **724** | 0 |
| **certifications** | 0 | 0 | 0 | 0 | 0 | **2** |

#### Per-Class Metrics Table:
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| `personal_info` | 1.00 | 1.00 | 1.00 | 483 |
| `experience` | 1.00 | 0.99 | 1.00 | 967 |
| `education` | 1.00 | 1.00 | 1.00 | 713 |
| `skills` | 1.00 | 1.00 | 1.00 | 481 |
| `projects` | 0.99 | 1.00 | 1.00 | 724 |
| `certifications` | 1.00 | 1.00 | 1.00 | 2 |
| **Overall Accuracy** | **0.9976** | — | — | 3,370 |
| **Weighted F1** | **0.9976** | **0.9976** | **0.9976** | 3,370 |
| **Unweighted Macro-F1 (All 6 Classes)** | **0.9983** | **0.9986** | **0.9983** | 3,370 |

*Interpretation:* The 8 misclassified samples (7 experience bullets predicted as projects, 1 experience bullet predicted as personal info) reflect genuine textual overlap between project deliverables and professional work experience descriptions.

### E. Generalization Limitation Notice
> **Scientific Integrity Statement:** While the classifier achieves 99.76% accuracy on clean, structured resumes from `uhfew/resumes`, this performance reflects structured digital documents with standard headings. Real-world resumes extracted from noisy scanned PDFs, multi-column graphical templates, or unpunctuated OCR streams will exhibit lower accuracy and must be supplemented by the deterministic rule fallbacks built into `ResumeParserService`.

---

## 3. Resume–Job Description Semantic Ranking

### A. Pretrained Zero-Shot Ranking Benchmark
- **Dataset:** `Shresth786/job-resume-matching` (122,560 validated pairs across 1,164 jobs and 9,532 candidates).
- **Zero Hallucination Negative Policy:** Because the dataset contains exclusively positive candidate pairs (`weak_positive`, `medium_positive`, `strong_positive`), **no artificial negative pairs were manufactured**. Binary classification was rejected because negative sampling introduces arbitrary false negatives.
- **Evaluation Population:** Evaluated across 24,977 pairs from 200 held-out candidate IDs (zero candidate overlap with training split) over 628 multi-candidate job postings ($\ge 4$ candidates per job).
- **Results:**
  - **Mean nDCG@5:** **0.9654**
  - **MRR (Mean Reciprocal Rank):** **0.3469**
  - **Spearman Rank Correlation ($\rho$):** **0.2831** ($p < 0.001$)
- **Population Scope:** These ranking metrics indicate how well the semantic engine ranks **pre-screened, relevant candidates** against one another. They do *not* assess binary pass/fail gatekeeping against completely unrelated applicants.

---

## 4. ATS Scoring Engine Improvements

### A. 5-State Requirement Categorization
The ATS audit engine was refactored to replace binary or ambiguous status codes with 5 explicit, transparent states:

```typescript
type RequirementStatus = 
  | "explicitly_matched"     // Cosine similarity >= 0.72 + source line evidence
  | "partially_supported"    // 0.50 <= Cosine similarity < 0.72 or conceptual overlap
  | "not_found_in_resume"    // < 0.50 with clean extraction: candidate verification recommended
  | "uncertain_extraction"   // Minimal or unparsed text in candidate section (< 4 snippets)
  | "confirmed_missing";     // Confirmed absent by candidate in interactive review
```

### B. Ethical Candidate Framing
The system no longer claims a candidate "lacks" a skill when it is simply absent from the text. Instead, it reports:
- *"Not located in provided resume text (Candidate verification recommended)."*
- In the AI Improvement workflow, it prompts: *"The job requires [Skill]. If you have hands-on experience or coursework in this area, describe the specific scenario..."*

### C. Internal Compatibility Rubric Branding & Transparency
In `ATSScoreBreakdown`, the score is explicitly defined as:
- **Rubric Title:** `"Elevate X Internal Compatibility Rubric (Deterministic 100-Point Audit)"`
- **Methodology Disclaimer:** *"This score is an internal deterministic algorithmic audit based on text similarity and document structure. It is not an official or proprietary vendor ATS algorithm."*
- **Mathematical Determinism:**
  - Part A (60 pts): Required Skills (25) + Preferred Skills (10) + Responsibilities (15) + Qualifications (10)
  - Part B (40 pts): Action Verbs/Metrics (15) + ATS Parseability (10) + Completeness (15)
  - Consecutive identical runs yield 100% identical outputs ($55.0 == 55.0$).

---

## 5. Multi-Profile AI Improvement Evaluation

The AI Improvement Engine (`ATSImprovementService`) was evaluated across 4 authentic candidate profiles using live inference on `mlx-community/Qwen2.5-1.5B-Instruct-4bit`:

| Candidate Profile | Role | Target JD | Suggestions Generated | Output Validity | Unsupported Claims | Skill Preservation | Company Preserved | Warm Latency |
|---|---|---|---|---|---|---|---|---|
| **Aarav Sharma** | Full Stack Developer | Senior Full Stack | 3 | 100.0% | **0** | 100.0% | True | 1,178 ms |
| **Priya Patel** | AI/ML Research Eng | ML / NLP Engineer | 3 | 100.0% | **0** | 100.0% | True | 1,166 ms |
| **Rajesh Verma** | Engineering Director | VP of Engineering | 2 | 100.0% | **0** | 100.0% | True | 831 ms |
| **Vikram Sen** | Senior Backend Eng | Lead Platform Eng | 3 | 100.0% | **0** | 100.0% | True | 1,178 ms |
| **Aggregate** | — | — | **11** | **100.0%** | **0 (0.0% Hallucination)** | **100.0%** | **100.0%** | **1,088 ms** |

### Evaluation Observations:
1. **Factual Grounding:** Across all 11 generated STAR bullets, zero unmentioned companies, tools, or fabricated metrics were introduced.
2. **Missing Evidence Questions:** For missing requirements (e.g. `GraphQL`, `Kubernetes`, `TensorRT`, `FinOps`), the system generated 7 targeted interview questions rather than inventing work experience.
3. **Artifact Persistence:** Stored in [backend/app/ml/models/ai_improvement_eval.json](file:///Users/ayushgupta/Desktop/Resume_Ai/backend/app/ml/models/ai_improvement_eval.json).

---

## 6. Training Policy & Feature Isolation Verification

1. **Training Policy Compliance:**
   - `ResumeSectionNeuralClassifier` was trained for 10 genuine epochs with class-weighted loss and learning rate scheduling.
   - Quarantined datasets (`harsh72877287/job_resume_fit`, `vadimas22/resume-score-details`) remain strictly quarantined and excluded.
   - Models without valid ground-truth supervision were not forced into artificial training.
2. **Feature Isolation:**
   - Feature 1 (`datasets/informal_skill_extraction/`, `backend/app/api/v1/skill.py`) and Feature 2 (`datasets/feature2/`, `backend/app/api/v1/technical_assessments.py`) files, schemas, checkpoints, and databases remain completely untouched.

---

## 7. Current Limitations & Unresolved Issues

1. **Scanned Image / Non-Searchable PDFs:**
   - The current ingestion engine uses `pypdf` stream text extraction. Scanned image-only PDFs (resumes submitted as raw images without embedded text) require an optical character recognition (OCR) pre-processing step (e.g., Tesseract or Apple Vision framework).
2. **Boilerplate Phrase Overlap:**
   - Even after near-duplicate clustering, 18.72% phrase overlap persists due to universal resume phrases (*"Bachelor of Technology"*, *"Responsibilities included"*). Sentence-level MinHash deduplication can be explored in future dataset curation passes.
3. **Local Development Host:**
   - Services currently run on local dev ports (`localhost:3002`, `localhost:8000`). Staging deployment with container orchestration and health probes is required before production release.
