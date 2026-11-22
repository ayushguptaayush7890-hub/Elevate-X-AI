# Elevate X AI — Resume Builder Model Development Roadmap

**Component:** Feature 3 — Resume Builder & Intelligent Career Matcher  
**Date:** November 21, 2026  
**Status:** Architecture Blueprint & Phased Development Roadmap  

---

## 1. Architectural Philosophy: The Hybrid AI Paradigm

Modern Applicant Tracking Systems (ATS) and AI recruitment systems fail when they rely exclusively on a single AI paradigm:
- **Pure LLM Prompts:** Suffer from non-deterministic scoring, high latency, context-window costs, and hallucinated hiring criteria.
- **Pure Keyword Matching:** Fails to recognize semantic equivalence (e.g., failing to match *"PostgreSQL administration"* with *"relational database management"*).

Elevate X AI adopts a **Three-Tier Hybrid Architecture**:
1. **Deterministic Rule Engine (ATS Core):** Fast, transparent, verifiable constraint checks (keyword coverage, section headers, contact completeness).
2. **Specialized Dense Retrieval & Token Models:** Bi-encoders and fine-tuned transformers for semantic candidate matching and token-level skill extraction.
3. **Generative LLM Layer:** Controlled, schema-constrained bullet point drafting and candidate feedback generation.

```
Candidate Upload (PDF / Narrative)
              │
              ▼
   [Stage 1: Document Parsing & Section Classification]
   - PDFPlumber / LayoutLMv3 + DistilRoBERTa Section Headings
              │
              ▼
   [Stage 2: Entity & Skill Extraction]
   - XLM-RoBERTa (Vocational/Multilingual) + RoBERTa-SkillSpan (Technical)
   - Canonical Ontology Normalization (ESCO / O*NET)
              │
              ▼
   [Stage 3: Hybrid ATS Scoring & Job Matching]
   ┌─────────────────────────────────────────────────────────────┐
   │ Deterministic Layer (60%): Hard Keyword Diff & ATS Health   │
   │ Semantic Layer (40%): Bi-Encoder Dense Similarity (BGE-v1.5)│
   └─────────────────────────────────────────────────────────────┘
              │
              ▼
   [Stage 4: Explainable Feedback & STAR Generation]
   - Schema-constrained Llama-3-8B / Gemini API for STAR bullets
```

---

## 2. Component-by-Component Architecture Recommendations

### 2.1 Task A: Resume Parsing & Section Segmentation
- **Goal:** Transform unstructured resume files (PDF, DOCX, TXT) into a validated JSON hierarchy matching `uhfew/resumes` schema.
- **Recommended Architecture:**
  - **Text Extraction:** `PyMuPDF` (`fitz`) for fast text and layout block extraction.
  - **Section Classifier:** Fine-tuned `DistilRoBERTa-base` trained to classify text blocks into 8 standard categories (`HEADER`, `SUMMARY`, `EXPERIENCE`, `EDUCATION`, `SKILLS`, `PROJECTS`, `CERTIFICATIONS`, `OTHER`).
  - **Fallback:** Rule-based regex header matcher for standard titles (*"Work History"*, *"Technical Proficiencies"*, etc.).
- **Execution Target:** CPU / MPS. Target Latency: $< 150\text{ ms}$.

---

### 2.2 Task B: Skill Extraction & Canonical Linking
- **Goal:** Extract technical, vocational, and soft competencies from resumes and link them to standardized ontologies.
- **Recommended Architecture:**
  - **Informal / Vocational Experience:** Existing fine-tuned `xlm-roberta-base` checkpoint (`best_indian_model`).
  - **Technical Resumes:** Token-classification transformer fine-tuned on combined `tags_skill` + `tags_knowledge` from `SkillSpan` and validated against `uhfew/resumes` skill inventories.
  - **Ontology Resolver:** Exact substring match against ESCO and O*NET catalogues followed by vector search (cosine threshold $\ge 0.75$) using `all-MiniLM-L6-v2`.

---

### 2.3 Task C: Job Description Understanding
- **Goal:** Parse messy job postings into structured requirement tuples:
  $$\text{Requirement} = (\text{Skill}, \text{Criticality: Must-Have / Nice-to-Have}, \text{Min Years})$$
- **Recommended Architecture:**
  - **Pipeline:** Sequence labeling for requirement entities + Zero-Shot NLI (`DeBERTa-v3-base`) to classify sentence modality (*"must possess"*, *"preferred"*, *"plus"*).
  - **Training Data:** `Shresth786/job-resume-matching` (`job_cleaned.csv`, 1,167 postings).

---

### 2.4 Task D: Resume-Job Matching (Two-Stage Architecture)
- **Goal:** Rank thousands of candidate profiles against open roles with low latency and high relevance accuracy.
- **Recommended Architecture:**
  - **Stage 1 — Candidate Filtering (Bi-Encoder Retrieval):**
    - Model: `BAAI/bge-large-en-v1.5` or `sentence-transformers/all-MiniLM-L6-v2`.
    - Function: Pre-compute candidate resume embeddings and job description embeddings. Perform fast cosine vector search using FAISS / HNSW index.
    - Output: Top 50 candidate matches retrieved in $< 10\text{ ms}$.
  - **Stage 2 — Fine-Grained Re-Ranking (Cross-Encoder):**
    - Model: `cross-encoder/ms-marco-MiniLM-L-6-v2` fine-tuned on `Shresth786` match pairs (using disjoint GroupKFold splits and hard negatives).
    - Function: Takes `[CLS] Resume [SEP] Job Description [SEP]` as simultaneous input to model deep cross-attention interactions.
    - Output: Calibrated alignment probability score $[0.0, 1.0]$.

---

### 2.5 Task E: ATS Compatibility Scoring (Hybrid Model)
- **Goal:** Provide transparent, legally defensible, and actionable ATS scores for job applicants.
- **Scoring Formulation:**
  $$\text{ATS Score} = 0.40 \cdot S_{\text{keyword}} + 0.30 \cdot S_{\text{semantic}} + 0.20 \cdot S_{\text{experience}} + 0.10 \cdot S_{\text{format}}$$
  - **$S_{\text{keyword}}$ (40%):** Deterministic Jaccard overlap of extracted candidate skills vs. job must-have skills.
  - **$S_{\text{semantic}}$ (30%):** Cross-encoder alignment score between experience narratives and job duties.
  - **$S_{\text{experience}}$ (20%):** Years of practice and senior/lead title matching.
  - **$S_{\text{format}}$ (10%):** Structural health (standard headings, bullet length, contact details presence).

---

### 2.6 Task F: Resume Content & STAR Bullet Generation
- **Goal:** Help candidates rewrite weak bullet points into high-impact STAR (Situation, Task, Action, Result) accomplishments without hallucinating facts.
- **Recommended Architecture:**
  - **Model:** Open-weights `meta-llama/Meta-Llama-3-8B-Instruct` (or `Mistral-7B-Instruct-v0.3`).
  - **Prompt Guardrails:**
    - Input: Candidate's raw narrative + Target job required skill.
    - Constraints: Strictly require quantified metric slots (`[X% increase]`, `[Y hours saved]`), active strong verbs (`Orchestrated`, `Implemented`, `Architected`), and JSON schema output.
    - Anti-Hallucination Rule: System prompt prohibits fabricating company names, credentials, or technologies not present in input.

---

## 3. Phased Implementation Roadmap

```
Phase 1: Foundation (Weeks 1-2)
├── Data Ingestion: Redacted corpora loaded into local SQLite cache
├── Parser Service: PyMuPDF + Regex section segmenter
└── ATS Baseline: Deterministic keyword & format scoring engine

Phase 2: Embedding & Matching (Weeks 3-4)
├── Dense Embedding: BGE-large bi-encoder integrated for resume search
├── Cross-Encoder: DeBERTa re-ranker fine-tuned on Shresth786 disjoint split
└── Ontology Linking: Real-time mapping to ESCO / O*NET APIs

Phase 3: Generation & Explainability (Weeks 5-6)
├── STAR Bullet Rewriter: Llama-3-8B prompt pipeline with JSON mode
├── Gap Analyzer: Automated comparison UI highlighting missing skills
└── User Feedback Loop: Candidate approval / correction tracking
```

---

## 4. Governance & Training Constraints Checklist

- [x] **Raw Datasets Quarantined:** Stored in `raw/` and excluded from Git tracking via `.gitignore`.
- [x] **PII Redacted in Processed Copies:** Emails, phones, names, and profile links masked with standard tokens.
- [x] **Quarantine Enforced on Dataset 3:** `harsh72877287/job_resume_fit` excluded from training due to unverified license terms.
- [x] **AI Label Warning Enforced on Dataset 4:** `vadimas22/resume-score-details` flagged as GPT-4o synthetic evaluations; restricted to feedback prompt demonstration.
- [x] **Disjoint Splitting Mandatory:** GroupKFold on candidate and job IDs to prevent train/test contamination.
