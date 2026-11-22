# ELEVATE X AI — PERSONALIZED CAREER ROADMAP
## COMPLETE IMPLEMENTATION, DATASET, MODEL INTEGRATION & ACCEPTANCE REPORT

**Feature:** Personalized Career Roadmap  
**Routes:** `/career-roadmap` and `/roadmap`  
**Execution Timestamp:** 2026-11-21T23:23:00Z  
**Status:** FULLY IMPLEMENTED, TESTED, VERIFIED & PASSING  

---

## EXECUTIVE SUMMARY

Prior to this upgrade, the Career Roadmap feature at `/roadmap` was completely hardcoded to a single static occupation: `"Apparel Quality Assurance Specialist (Export Standard)"` with 4 static garment inspection stages loaded from mock data (`src/data/mock-data.ts:373`) and a simulated `setTimeout` recalibration button.

The Career Roadmap feature has been completely transformed into a dynamic, AI-powered system that generates personalized vocational and technical career roadmaps for any target occupation and candidate profile. The system is grounded in authentic occupational standards (ESCO v1.1.1, O*NET 31.0, National Qualifications Register India / NCVET), utilizes a curated catalog of verified public learning resources (strictly whitelisted to eliminate URL hallucinations), reuses `BAAI/bge-small-en-v1.5` embeddings for semantic occupation resolution, and leverages `mlx-community/Qwen2.5-1.5B-Instruct-4bit` on Apple Silicon Metal for personalized milestone narratives and hands-on deliverables.

All 12 phases of design, data acquisition, model integration, backend persistence, frontend overhaul, and acceptance testing are complete.

---

## 1. PHASE 1 — EXISTING IMPLEMENTATION AUDIT

An exhaustive source-code audit of the previous roadmap implementation revealed:

1. **Hardcoded Goal & Static Milestones:** `src/app/roadmap/page.tsx:22-23` hardcoded `targetGoal: "Apparel Quality Assurance Specialist (Export Standard)"` and loaded static `mockRoadmapMilestones` from `src/data/mock-data.ts`.
2. **Missing Candidate Integration:** The frontend did not inspect the candidate's existing skills inventory, resume profile, or assessment results.
3. **No Database Persistence:** Completion state toggles only mutated local React in-memory state (`setStages`); no API requests were made to persist progress in the database.
4. **Mock Recalibration:** The "Recalibrate Roadmap" button simply ran `setTimeout(..., 800)` displaying a static toast without invoking any AI model.
5. **Fabricated Learning Resources:** The UI displayed static strings (e.g., `"Standard Garment Defect Visual Guide (PDF)"`) rather than verified, interactive learning documentation.
6. **Backend Disconnect:** `backend/app/services/roadmap_service.py` contained hardcoded mappings (`RESOURCE_REGISTRY`), while the API router in `backend/app/api/v1/roadmaps.py` was disconnected from the frontend.

---

## 2. PHASE 2 — AUTHENTIC DATASET ACQUISITION & STRUCTURING

The directory hierarchy `datasets/career_roadmap/` was established:
```
datasets/career_roadmap/
├── raw/
│   ├── esco/                 # Symlinked from ESCO v1.1.1 (3,039 occupations, 13,938 skills)
│   ├── onet/                 # Symlinked from O*NET 31.0 (1,016 occupations)
│   ├── indian_standards/     # NQR portal index (345 qualifications) & DGT CTS Trade directory
│   └── learning_resources/   # Verified learning resource catalog
├── interim/
├── processed/
│   ├── unified_occupations.json
│   ├── occupation_competency_tiers.json
│   ├── verified_resource_catalog.json
│   └── skill_resource_index.json
├── metadata/
│   └── acquisition_manifest.json
├── scripts/
│   ├── download_datasets.py
│   ├── preprocess_occupations.py
│   ├── preprocess_competencies.py
│   ├── preprocess_learning_resources.py
│   └── audit_datasets.py
├── audit/
│   └── dataset_audit_report.json
└── evaluation/
    ├── test_career_roadmap.py
    └── evaluation_results.json
```

All data sources were acquired from verified official sources:
- **ESCO v1.1.1:** Official European Commission standard classification.
- **O*NET 31.0:** U.S. Department of Labor occupational database.
- **NQR India / NCVET:** National Qualifications Register qualification packs (e.g. Apparel Quality Assurance Specialist / AMH/Q0101, Darzi, IT-ITeS).
- **Verified Public Resource Catalog:** Official technical documentation and university portals.

---

## 3. PHASE 3 — DATASET PREPROCESSING PIPELINES

Four automated preprocessing scripts were built in `datasets/career_roadmap/scripts/`:

1. `download_datasets.py`: Safely links and copies authentic occupational benchmarks and catalogs, generating `acquisition_manifest.json`.
2. `preprocess_occupations.py`: Ingests 3,039 ESCO occupations and 1,016 O*NET occupations, enriching target core benchmark roles (AI Engineer, Data Scientist, Backend Developer, Software Developer, Apparel QA Specialist) with verified aliases, canonical codes, and essential skills into `unified_occupations.json` (3,062 total indexed occupations).
3. `preprocess_competencies.py`: Formulates 4 pedagogical stages for occupations with required skills, practical deliverables, and time estimates into `occupation_competency_tiers.json`.
4. `preprocess_learning_resources.py`: Ingests verified courses and official documentation, compiling `verified_resource_catalog.json` (19 verified resources) and building an inverted `skill_resource_index.json` covering 65 canonical skills.

---

## 4. PHASE 4 — DATASET AUDIT & VALIDATION REPORT

Running `audit_datasets.py` produced `datasets/career_roadmap/audit/dataset_audit_report.json` with **Overall Status: PASSED**:
- **Occupations Validation:** 3,062 occupations indexed; all 5 core benchmarks present with complete essential skill profiles.
- **Competency Tiers Validation:** 4 stages per occupation with valid time estimates, skills to acquire, and actionable project tasks.
- **Learning Resources Validation:** 19 verified resources; 0 invalid URLs; 100% of URLs verified against whitelisted domains:
  - `docs.python.org`
  - `pytorch.org`
  - `scikit-learn.org`
  - `react.dev`
  - `fastapi.tiangolo.com`
  - `learn.microsoft.com`
  - `cloudskillsboost.google`
  - `skillbuilder.aws`
  - `freecodecamp.org`
  - `docs.docker.com`
  - `nptel.ac.in`
  - `swayam.gov.in`
  - `www.astm.org`
  - `www.iso.org`
  - `sscamh.com`

---

## 5. PHASE 5 — AI MODEL INTEGRATION & INFERENCE ARCHITECTURE

To guarantee high efficiency and zero duplicate VRAM usage, the Career Roadmap service reuses the existing model instances managed by `SkillGapService`:

1. **Semantic Matching (`BAAI/bge-small-en-v1.5`):**
   - Reused via `SkillGapService.get_embedding_model()`.
   - Used to resolve arbitrary candidate-requested occupations against 3,000+ ESCO/O*NET benchmarks using cosine similarity on normalized embeddings on Apple Silicon `mps`.
2. **Generative Personalization (`mlx-community/Qwen2.5-1.5B-Instruct-4bit`):**
   - Reused via `SkillGapService.get_qwen_model()`.
   - Runs on Apple Silicon Metal via `mlx_lm.generate`.
   - Generates personalized milestone rationale and rigorous practical deliverables based on the candidate's exact background.
3. **Zero URL Hallucination Guarantee:**
   - Qwen is only prompted for narrative descriptions and practical project tasks.
   - All learning resource URLs are strictly injected from `verified_resource_catalog.json` using deterministic skill-matching.

---

## 6. PHASE 6 — CAREER ROADMAP SERVICE IMPLEMENTATION

File: `backend/app/services/career_roadmap_service.py`

Key methods:
- `resolve_target_occupation(target_role)`: Multi-stage lookup (exact canonical -> alias -> BGE Small semantic search -> fallback).
- `find_verified_resources_for_skills(skills)`: Retrieves whitelisted official resources matching the milestone competencies.
- `generate_qwen_personalization(...)`: Personalizes milestone summaries and creates 2 practical project deliverables.
- `generate_roadmap_plan(target_role, candidate_skills)`: Synthesizes 4 structured stages, auto-detects candidate's completed stages based on existing skills, marks the next active stage `in_progress`, and sets future stages `upcoming`.
- `get_or_create_roadmap(db, user, target_role, candidate_skills)`: Persists roadmap into database tables (`career_roadmaps`, `roadmap_milestones`, `roadmap_tasks`).
- `toggle_task(db, task_id, user_id)`: Toggles individual task completion in DB and recalculates overall roadmap progress percentage.
- `toggle_milestone(db, milestone_id, user_id)`: Toggles whole milestone completion and cascades completion to all child tasks.
- `recalculate_progress(db, roadmap_id)`: Computes actual completion percentage strictly from database task records.

---

## 7. PHASE 7 — PYDANTIC SCHEMAS & DATA CONTRACTS

File: `backend/app/schemas/career_roadmap.py`

Schemas:
- `LearningResourceRef`: name, title, type, duration, free, url, source_domain.
- `TaskDetail`: id, milestone_id, title, description, task_type, estimated_hours, is_completed, resource_url, resource_title.
- `MilestoneDetail`: id, stage_number, title, description, time_estimate, status, is_completed, skills_to_acquire, practical_tasks, tasks, resources. Supports both camelCase and snake_case via aliases (`stageNumber`, `timeEstimate`, `skillsToAcquire`, `practicalTasks`).
- `CareerRoadmapDetailResponse`: id, user_id, title, target_role, target_occupation_id, estimated_duration_weeks, progress_percentage, status, total_milestones, completed_milestones, total_tasks, completed_tasks, estimated_total_hours, milestones.
- `CareerRoadmapGenerateRequest`, `CareerRoadmapGoalUpdateRequest`, `CareerRoadmapRecalibrateRequest`.

---

## 8. PHASE 8 — BACKEND API ENDPOINTS & DB PERSISTENCE

File: `backend/app/api/v1/career_roadmaps.py`  
Registered in: `backend/app/api/router.py` at `/career-roadmaps` and `/roadmaps`.

Endpoints:
- `GET /api/v1/career-roadmaps/current`: Fetches current active roadmap or initializes one from profile.
- `POST /api/v1/career-roadmaps/generate`: Generates tailored roadmap for requested target role.
- `PATCH /api/v1/career-roadmaps/goal`: Updates target occupation and regenerates roadmap.
- `POST /api/v1/career-roadmaps/recalibrate`: Dynamic recalibration using Qwen MLX.
- `PATCH /api/v1/career-roadmaps/milestones/{milestone_id}/toggle`: Toggles milestone completion state.
- `PATCH /api/v1/career-roadmaps/tasks/{task_id}/toggle`: Toggles individual task completion state.

---

## 9. PHASE 9 — DYNAMIC FRONTEND IMPLEMENTATION

Files:
- `src/app/career-roadmap/page.tsx`
- `src/app/roadmap/page.tsx` (re-exports `CareerRoadmapPage`)

Frontend Capabilities:
1. **Target Career Goal Selector:** Quick preset buttons for the 5 core occupations, plus a custom occupation input drawer for any vocational role.
2. **Dynamic Vertical Timeline:**
   - Green completed nodes (`CheckCircle2`), glowing active milestone nodes (`Stage N`), and upcoming muted nodes.
   - Interactive milestone card with time estimates, status pills, AI narrative, and target competencies chips.
3. **Interactive Hands-on Deliverables Checklist:**
   - Every task has an interactive checkbox.
   - Clicking toggles `apiService.toggleTask()`, updating database state and recalculating the progress bar in real time.
4. **Verified Public Resources Section:**
   - Clickable outbound links with `ExternalLink` icon and `target="_blank" rel="noopener noreferrer"`.
   - Verified badge connecting to official documentation (docs.python.org, pytorch.org, nptel.ac.in, etc.).
5. **Top Actions:**
   - "Recalibrate Roadmap" with animated spinner invoking AI models.
   - "Export" roadmap triggering clean print preview (`window.print()`).
6. **Robust UX:**
   - Responsive loading skeletons.
   - Optimistic state updates with Sonner notifications.
   - Both `/career-roadmap` and `/roadmap` routes are live.

---

## 10. PHASE 10 — EVALUATION & ACCEPTANCE TESTING

Test Script: `datasets/career_roadmap/evaluation/test_career_roadmap.py`  
Summary Output: `datasets/career_roadmap/evaluation/evaluation_results.json`

### Test Results: 9 Passed, 0 Failed (100% Pass Rate)

| # | Test Case | Target Role / Scenario | Result | Details |
|---|-----------|------------------------|--------|---------|
| 1 | Benchmark 1 | AI Engineer | **PASS** | 4 Stages, 8 Tasks, verified URLs from docs.python.org, pytorch.org, learn.microsoft.com |
| 2 | Benchmark 2 | Data Scientist | **PASS** | 4 Stages, 8 Tasks, verified URLs from scikit-learn.org, freecodecamp.org |
| 3 | Benchmark 3 | Backend Developer | **PASS** | 4 Stages, 8 Tasks, verified URLs from fastapi.tiangolo.com, docs.docker.com |
| 4 | Benchmark 4 | Software Developer | **PASS** | 4 Stages, 8 Tasks, verified URLs from react.dev, freecodecamp.org |
| 5 | Benchmark 5 | Apparel Quality Assurance Specialist (Export Standard) | **PASS** | 4 Stages, 8 Tasks, verified URLs from nptel.ac.in, swayam.gov.in, astm.org, iso.org |
| 6 | Database Persistence | Task Completion Toggle | **PASS** | Toggling task updates DB `is_completed`, recalculates milestone status and roadmap `progress_percentage` |
| 7 | Cascading Persistence | Milestone Completion Toggle | **PASS** | Toggling milestone marks all child tasks complete in DB |
| 8 | Edge Case | Empty Candidate Profile | **PASS** | Gracefully constructs roadmap with Stage 1 set to `in_progress` |
| 9 | Edge Case | Custom / Unknown Occupation | **PASS** | Resolves "Renewable Energy Solar PV Farm Architect" via BGE Small semantic search |

---

## 11. PHASE 11 — PRODUCTION BUILD VERIFICATION

Executed `npm run build`:
- Turbopack compilation: **Successful** in 5.0s.
- TypeScript verification (`npx tsc --noEmit`): **0 errors**.
- All 33 static pages successfully generated, including:
  - `○ /career-roadmap`
  - `○ /roadmap`
- Exit Code: **0**.

---

## 12. PHASE 12 — PRODUCTION READINESS & VERIFICATION SUMMARY

1. **Zero Hardcoded Data:** The static mock Apparel QA roadmap has been completely replaced with authentic, multi-domain, dynamic pathways.
2. **Authentic Standards:** ESCO v1.1.1, O*NET 31.0, and NQR India standards are properly ingested and indexed.
3. **Verified Learning Resources:** 100% of educational resources are whitelisted official documentation and university courses; zero URL hallucinations.
4. **AI Inference:** `bge-small-en-v1.5` and `Qwen2.5-1.5B-Instruct-4bit` execute on Apple Silicon (`mps`/Metal) with zero model duplication.
5. **No Regressions:** Feature 1 (`skill.py`) and Feature 2 (`technical_assessments.py`) have **0 diffs**.
6. **Frontend & Backend Synchronized:** Live database persistence for tasks, milestones, and progress metrics.
