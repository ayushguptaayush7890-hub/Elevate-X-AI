# Elevate X AI — Vocational Career & Skills Intelligence Ecosystem

> **Empowering informal trade artisans and vocational professionals to translate real-world hands-on experience into recognized competencies, verified credentials, and upward career mobility.**

---

## 1. Project Overview

**Elevate X AI** is an end-to-end artificial intelligence ecosystem designed to bridge the gap between informal, uncredentialed trade workers (e.g., tailors, electricians, automotive mechanics, carpenters, plumbers, weavers) and formal corporate career pathways.

While informal artisans possess years of practical expertise with industrial machinery, quality standards, and problem-solving, their colloquial narratives and lack of paper credentials systematically exclude them from automated applicant tracking systems (ATS) and formal recruitment pipelines. Elevate X AI provides:
1. **Colloquial Skill Extraction (Feature 1):** Automatic parsing of spoken or written informal worker testimony into standardized NSQF and ESCO/O*NET competencies.
2. **Adaptive Diagnostic Assessments (Feature 2):** Practical, scenario-based technical evaluations and coding/config sandboxes across 15 vocational roles with verifiable skill badges.
3. **Factuality-Guarded Resume Builder:** Translation of raw workshop experience into impact-driven resume bullets without algorithmic hallucination.
4. **Multilingual AI Career Assistant:** Pedagogical mentoring in Hindi, Hinglish, and English to build candidate interview readiness and career self-efficacy.

---

## 2. Problem Statement

Across developing economies, over **80% of vocational workers operate in the unorganized or informal sector**. Despite deep technical domain expertise:
- **Colloquial Testimony:** Workers describe their trade in regional vernacular (e.g., *"Juki lockstitch machine pe sherwani silta hoon"*), which standard corporate ATS parsers reject.
- **Credential Invisibility:** Artisans lack recognized diplomas, making employer trust difficult without expensive manual vetting.
- **Skill Gap Blindspots:** Workers cannot identify adjacent, high-demand formal roles (e.g., an informal tailor transitioning to an Apparel Quality Assurance Specialist).
- **Language Barriers & Interview Anxiety:** Candidates often experience imposter syndrome when entering formal corporate hiring processes.

---

## 3. Proposed Solution

Elevate X AI provides a structured 5-stage transition pipeline:

```
[ Informal Worker Narrative ] (Colloquial Hindi / English / Hinglish)
            │
            ▼
┌────────────────────────────────────────────────────────┐
│  Feature 1: ML Skill Extraction & ESCO Normalization   │
│  - BIO Token Classification (XLM-RoBERTa)              │
│  - Indian Vocational Taxonomy Mapping (TRD-01 to 06)   │
│  - ESCO / O*NET Canonical Competency Alignment         │
└────────────────────────────────────────────────────────┘
            │
            ▼
┌────────────────────────────────────────────────────────┐
│  Feature 2: Adaptive Diagnostic Assessment Engine      │
│  - 2,250 Curated Practical Scenarios across 15 Roles   │
│  - Multi-Modal Evaluation (MCQ, Sandbox, Design)       │
│  - Real-Time Pedagogical Feedback & Scoring            │
└────────────────────────────────────────────────────────┘
            │
            ▼
┌────────────────────────────────────────────────────────┐
│  Career Transition & Deployment Engine                 │
│  - O*NET Compatible Career Roadmap                     │
│  - Anti-Hallucination Resume Builder (Factuality Guard)│
│  - AI Mock Interview Lab & Multilingual Mentor         │
└────────────────────────────────────────────────────────┘
```

---

## 4. Key Features

- **Colloquial Voice & Text Recognition:** Input trade narratives in natural spoken Hindi, Hinglish, or English with instant competency extraction.
- **Adaptive Diagnostic Testing:** Scenario-driven evaluations that adjust difficulty based on candidate response confidence and accuracy.
- **Secure Code & Query Sandboxes:** Sandboxed execution environments for technical and vocational configuration tasks.
- **Anti-Hallucination Resume Builder:** Strict guardrails ensuring that only verified skills and factual experiences are formatted into formal ATS resumes.
- **Interactive AI Mock Interview Lab:** Simulated conversational interviews calibrated to corporate export and manufacturing industry standards.
- **Admin Prompt Engineering Benchmarking:** Real-time observability dashboard for measuring prompt accuracy, latency, and JSON schema compliance.

---

## 5. System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Next.js 16 Frontend                      │
│        (React 19, Tailwind CSS v4, Lucide Icons, SWR)       │
└──────────────────────────────┬──────────────────────────────┘
                               │ REST / JSON (Port 3002)
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                    FastAPI Backend Engine                   │
│        (Python 3.11+, SQLAlchemy 2.0, Pydantic v2)          │
├──────────────────────────────┬──────────────────────────────┤
│  Feature 1 ML Pipeline       │  Feature 2 Assessment Engine │
│  - BIO Span Tokenizer        │  - Adaptive Engine           │
│  - XLM-RoBERTa Classifier    │  - 2,250 Question Bank       │
│  - ESCO Canonical Matcher    │  - Subprocess Sandboxes      │
└──────────────────────────────┴──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                      Data & Storage                         │
│  - PostgreSQL / SQLite with Alembic Versioning              │
│  - Indexed JSONL Dataset Repositories                       │
│  - O*NET & European Skills (ESCO) Crosswalk Tables          │
└─────────────────────────────────────────────────────────────┘
```

---

## 6. Technology Stack

- **Frontend:** Next.js 16 (App Router), React 19, TypeScript, Tailwind CSS v4, Recharts, Lucide Icons, Sonner.
- **Backend:** FastAPI, Python 3.11+, Pydantic v2, SQLAlchemy 2.0, Alembic, Uvicorn.
- **AI & ML (Feature 1):** PyTorch, Hugging Face Transformers, `xlm-roberta-base`, Token Classification (BIO tagging), Scikit-Learn.
- **Assessment Engine (Feature 2):** 2,250 Diagnostic Items, Subprocess Isolated Code Execution Sandboxes, Pedagogical Rule Engine.
- **Database:** PostgreSQL (Production) / SQLite (Development & Local CI).

---

## 7. Project Directory Structure

```text
Elevate-X-AI/
├── .env.example                 # Sanitized frontend environment template
├── .gitignore                   # Security & large file exclusions
├── package.json                 # Next.js dependencies & scripts
├── tsconfig.json                # TypeScript compiler configuration
├── tailwind.config.ts           # Tailwind CSS styling tokens
│
├── src/                         # Next.js 16 Frontend
│   ├── app/                     # App Router pages (15 routes)
│   │   ├── page.tsx             # Landing page & hero sequence
│   │   ├── experience/          # Feature 1: Experience recognition UI
│   │   ├── assessment/          # Feature 2: Technical assessment UI
│   │   ├── interview/           # AI Mock Interview Simulator
│   │   ├── resume/              # Factuality-Guarded Resume Builder
│   │   ├── roadmap/             # Career Roadmap & Mobility Pathways
│   │   ├── jobs/                # Curated Vocational Job Listings
│   │   └── admin/               # Admin Analytics & Prompt Engineering
│   ├── components/              # UI components, layout shells, cards
│   ├── context/                 # Auth & Language (Hindi/English) providers
│   ├── data/                    # Mock benchmarks & prompt evaluations
│   └── lib/                     # API client & utility helpers
│
├── backend/                     # FastAPI Backend Application
│   ├── .env.example             # Sanitized backend environment template
│   ├── alembic.ini              # Database migration configuration
│   ├── requirements.txt         # Python package dependencies
│   ├── app/
│   │   ├── main.py              # Application entry point & middleware
│   │   ├── api/v1/              # REST API route handlers
│   │   │   ├── skill.py         # Feature 1 skill extraction endpoints
│   │   │   ├── technical_assessments.py # Feature 2 endpoints
│   │   │   ├── auth.py          # JWT authentication endpoints
│   │   │   └── resumes.py       # Resume generation endpoints
│   │   ├── core/                # Configuration, DB engine & security
│   │   ├── models/              # SQLAlchemy ORM entity definitions
│   │   ├── schemas/             # Pydantic request/response schemas
│   │   └── services/            # Sandboxes, question & feedback engines
│   ├── migrations/              # Alembic versioned schema migrations
│   └── tests/                   # Pytest test suites (unit & integration)
│
├── datasets/                    # Vocational Data & ML Pipeline
│   ├── feature2/
│   │   ├── questions.jsonl      # 2,250 Production assessment questions
│   │   └── roles_and_skills.json # 15 Technical vocational role profiles
│   └── informal_skill_extraction/
│       ├── models/              # Model architectures, training scripts
│       ├── processed/           # Processed Indian trade data & ESCO maps
│       ├── raw/                 # Canonical taxonomy source files
│       └── scripts/             # Data preprocessing & evaluation scripts
│
├── public/                      # Static assets, icons, animation frames
└── scripts/                     # Operational verification & benchmark scripts
```

---

## 8. Dataset Information & Licensing

| Dataset | Records / Size | Origin & Licensing | Purpose in Elevate X AI |
| :--- | :--- | :--- | :--- |
| **ESCO Skill Crosswalks** | 37.4 MB CSV | European Commission (Open Data CC BY 4.0) | Standardizes informal trade terms to international skill taxonomy |
| **Indian Vocational Mock Dataset** | 11.4 MB JSONL | Synthetic Indian Worker Narratives | Calibrates multilingual BIO extraction on regional trade vernacular |
| **Feature 2 Diagnostic Question Bank** | 2,250 Questions (JSONL) | Curated Vocational Technical Assessments | Scenario-based diagnostic evaluations across 15 technical roles |

*Note: All datasets are free of Personally Identifiable Information (PII). All candidate test cases are synthetic benchmarks created for vocational evaluation.*

---

## 9. AI/ML Models & Reproducibility (Feature 1)

### Architecture
- **Base Backbone:** `xlm-roberta-base` (Multilingual cross-lingual language model).
- **Head:** Token classification linear layer outputting BIO labels (`B-TECH`, `I-TECH`, `B-TRANS`, `I-TRANS`, `O`).
- **Canonical Matcher:** Cosine similarity retrieval over ESCO/O*NET dense vector embeddings.

### Large Model Checkpoints Notice
Due to GitHub's 100 MB per-file threshold, the **8 raw binary `.safetensors` model checkpoints (~1.06 GB each, 8.46 GB total)** are excluded from Git tracking via `.gitignore`.

To train and reproduce the weights locally:
```bash
cd datasets/informal_skill_extraction/models
python train_indian_model.py --epochs 5 --batch_size 16 --output_dir ./checkpoints/best_indian_model
```
All training pipelines, tokenizer vocabularies, evaluation metrics, and hyperparameter configurations are fully preserved in the repository.

---

## 10. Installation & Setup

### Prerequisites
- Node.js 18+ and `npm`
- Python 3.11+ (recommended: conda or virtual environment)
- Git

### Frontend Setup
```bash
# From repository root
npm install

# Copy environment template
cp .env.example .env.local

# Run frontend development server
npm run dev
```
The frontend will be available at `http://localhost:3000` (or `http://localhost:3002`).

### Backend Setup
```bash
# Navigate to backend directory
cd backend

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env

# Run database migrations
alembic upgrade head

# Start FastAPI server
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
The backend API will be available at `http://localhost:8000`.

---

## 11. API Documentation

Interactive API documentation is automatically generated by FastAPI:
- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`
- **Health Check Endpoint:** `http://localhost:8000/health`

---

## 12. Testing

### Run Frontend Tests & Type Checking
```bash
npx tsc --noEmit
npm run build
```

### Run Backend Pytest Suite
```bash
cd backend
pytest tests/ -v
```

---

## 13. Known Limitations & Future Improvements

- **Offline Inference:** Feature 1 token classification models require approximately 2 GB of RAM during active PyTorch inference.
- **Language Coverage:** Currently optimized for Hindi, Hinglish, and Indian English trade terms; future milestones will expand support for Tamil, Telugu, and Bengali vocational vernacular.
- **Live Video Assessment:** Video-based physical skill verification is currently simulated through scenario-based visual questions.
- **Milestone 2 Scope:** This release represents Milestone 2; cloud deployment configurations and external third-party credential authority integrations are planned for future iterations.

---

## 14. Security & Responsible AI

- **Zero Tolerance for Hallucination:** Resume and assessment generation modules employ explicit factuality guardrails forbidding arbitrary credentials or exaggerated experience metrics.
- **Code Execution Sandboxing:** Assessment code execution employs restricted subprocess environments with system call and socket filtering to prevent arbitrary resource access.
- **Credential Protection:** All `.env` files, JWT secrets, and database passwords are excluded from version control.

---

## 15. Team Members

| Name | Role / Contributions |
| :--- | :--- |
| **Ayush Gupta** | Full-Stack Architecture, Next.js Frontend, Feature 1 Skill Extraction ML Pipeline |
| **Kush Vijay** | Feature 2 Technical Assessment Engine, Question Bank Curation & Sandbox Security |
| **Reity Khurana** | Multilingual Prompt Engineering, Factuality Guardrails & UI/UX Design Tokens |

---

## 16. License

This project is licensed for academic, evaluation, and open-source vocational research purposes. All third-party datasets and pre-trained model backbones belong to their respective copyright holders.
