# Elevate X AI — Critical Module Bug Fix & End-to-End Audit Report

**Date:** November 22, 2026  
**Auditor:** Elevate X AI Core Engineering Team  
**System Status:** Operational & Production-Ready  
**Automated Tests:** 30 / 30 Passed (100% Pass Rate)  
**TypeScript Typecheck:** 0 Errors (`npx tsc --noEmit` cleanly passed)  
**Target Environment:** Local macOS / Apple Silicon MPS / Next.js 14 App Router + FastAPI Backend  

---

## 1. Executive Summary

A comprehensive investigation, root-cause analysis, and architectural repair was performed across four critical subsystems of the Elevate X AI vocational ecosystem:
1. **Assessment Navigation & Answering Engine (`/assessment`)**: Eliminated question skipping without selection, locked in-app navigation, implemented backend session persistence and reload recovery, and added unanswered question jump-links.
2. **Coding Assessment Sandbox & Contract Enforcement (`datasets/feature2/`)**: Fixed the `defective_routine_12` question and all 35 debugging routines, redefined explicit function contracts and structured test cases, and upgraded `CodeSandbox` with isolated subprocess test execution.
3. **Skill Gap Analyzer (`/skill-gap`)**: Completely purged 27 hardcoded fallback skills (`INITIAL_RAW_SKILLS`), added verified source tracking (`resume_extracted`, `user_added`, `profile_verified`), and introduced an empty-state onboarding banner.
4. **Experience Recognition (`/experience`)**: Resolved the HTTP 500 `"Extraction Error: Failed to fetch"` crash caused by an undefined reference error, integrated automatic zero-shot trade classification for Hindi/Hinglish narratives, and added actionable error states preserving user inputs.
5. **Skill Gap Analyzer React Duplicate Key Fix (`SP-01`)**: Eliminated Next.js console warning `Encountered two children with the same key, 'SP-01'` by resolving identity collisions at the data level with namespaced identifiers (`generateCandidateSkillId`), metadata-merging deduplication (`deduplicateCandidateSkills`), separate preservation of source span IDs in `sourceId`, and deterministic React render keys.

---

## 2. Detailed Root-Cause Analyses & Technical Solutions

### Issue 1: Assessment — Prevent Next Without Selecting an Answer
* **Root Cause:**
  - In `src/app/assessment/page.tsx`, the "Next Question" button did not validate `selectedAnswers[currentQ.id]` before triggering index advancement (`setCurrentIndex(prev => prev + 1)`).
  - Rapid double-clicking could trigger duplicate transitions or race conditions against remote submissions.
  - No mechanism warned candidates about skipped questions prior to final grading.
* **Solution Implemented:**
  - Disabled the "Next Question" button until an answer is selected for MCQ questions (`isNextDisabled = !hasAnswer`).
  - Rendered a visible inline warning message: `"Please select an answer before proceeding."`
  - Re-hydrated previously chosen answers into state upon clicking "Previous".
  - Created an Unanswered Questions Confirmation Modal prior to submission: enumerates unanswered question numbers with one-click direct jump-to-question buttons.
  - Added debounced submission logic preventing duplicate server calls.

### Issue 2: Assessment — Lock In-App Navigation During an Active Test
* **Root Cause:**
  - During a timed assessment, candidates could click the navigation sidebar, brand logo, or browser back button to navigate away without warning.
  - On page refresh, the timer reinitialized to full test duration (`duration_minutes * 60`), resetting the test countdown.
  - No backend session persistence existed for partially completed attempts.
* **Solution Implemented:**
  - **Backend Session Persistence:**
    - `POST /api/v1/assessments/technical/start`: Stores `session_id`, `started_at`, `duration_minutes`, `expiry_timestamp`, `masked_questions`, and initializes `answers={}`.
    - `GET /api/v1/assessments/technical/sessions/{session_id}`: Rehydrates full test state on page reload, dynamically calculating true remaining seconds (`expiry_timestamp - now()`) without resetting the timer.
    - `POST /api/v1/assessments/technical/sessions/{session_id}/progress`: Persists answer updates and `current_index` incrementally.
    - `POST /api/v1/assessments/technical/sessions/{session_id}/cancel`: Releases session lock on explicit exit.
  - **Frontend In-App Navigation Lock:**
    - Added `isLocked` prop to `AppShell`, `DashboardSidebar`, and `DashboardHeader`.
    - Intercepted sidebar and header link navigation with `e.preventDefault()` when `isLocked === true`, displaying an Active Assessment Warning modal.
    - Attached window `beforeunload` event handler warning against closing or reloading the tab.
    - Attached browser `popstate` history event listener to catch back-button presses.

### Issue 3: Coding Assessment — Fix IndexError & Real Sandbox Validation
* **Root Cause:**
  - In `datasets/feature2/software_engineer/debugging/Q-SWE-DBG-001.json` through `035.json`, `defective_routine_12(items)` omitted `target` in its signature yet referenced it inside the loop.
  - When `target` was at the final array index, `items[i + 1]` triggered `IndexError: list index out of range`.
  - The previous `CodeSandbox` implementation was a mock runner that iterated over test cases and hardcoded `"status": "PASSED"` without executing candidate code.
* **Solution Implemented:**
  - **Question & Dataset Contract Repair:**
    - Updated all 35 question files and `datasets/feature2/master_dataset.json` with signature `def defective_routine_N(items, target):`.
    - Explicit contract: returns `items[i + 1]` if followed by another item; returns `None` if `target` is at the final index, missing, or if `items` is empty.
    - Added structured test cases with visible boundary conditions (final index, empty array) and hidden tests.
  - **Subprocess Test Runner in `CodeSandbox`:**
    - Upgraded `backend/app/services/sandboxes.py` to write candidate code and a test harness (`solution_test.py`) to an isolated temporary directory.
    - Passes structured input parameters via `tests.json`.
    - Enforces execution limits (4-second timeout, address space memory limits, restricted module imports).
    - Accurately captures `IndexError`, `SyntaxError`, and value mismatches with detailed error reports.

### Issue 4: Skill Gap Analyzer — Removal of Fake Default Skills
* **Root Cause:**
  - `src/app/skill-gap/page.tsx` initialized candidate skills with `INITIAL_RAW_SKILLS`, a static array of 27 hardcoded technologies (`Python`, `Machine Learning`, `PostgreSQL`, etc.).
  - Accounts with no uploaded resume or profile data falsely displayed a 27-skill portfolio.
* **Solution Implemented:**
  - Completely purged `INITIAL_RAW_SKILLS` and hardcoded defaults.
  - Structured candidate skills with provenance metadata: `source: "resume_extracted" | "profile_verified" | "user_added"`.
  - Empty state check: when candidate skills are empty, displays the required notice:
    > *"No skills found yet. Upload your resume or add skills manually to begin your skill-gap analysis."*
  - Added action buttons: *"Upload Resume"* (opens file dialog) and *"Add Skills Manually"* (opens skill search modal).
  - Maintained candidate isolation: skills from User A never leak to User B.

### Issue 5: Experience Recognition — "Extraction Error: Failed to fetch"
* **Root Cause:**
  - In `backend/app/api/v1/skill.py`, `extract_skills_endpoint` threw `NameError: name 'default_config' is not defined` at line 155 when resolving the compute device string (`default_config.get_device()`).
  - The uncaught `NameError` triggered an HTTP 500 Internal Server Error, which Next.js displayed as a generic `"Extraction Error: Failed to fetch"`.
  - In `datasets/informal_skill_extraction/models/skill_extractor.py`, if no `occupation_hint` was provided, the classifier failed to classify trade text.
* **Solution Implemented:**
  - Fixed `backend/app/api/v1/skill.py`: properly declared `default_config = _get_default_config()` at entry.
  - Integrated `OccupationClassifier` in `skill_extractor.py`: when `occupation_hint` is omitted, the text is automatically classified (e.g. Electrician `TRD-02` with 94.7% confidence).
  - Updated `src/app/experience/page.tsx`:
    - Replaced generic error with contextual messages (422 validation, 500 model error, 401 auth, network timeout).
    - Preserved candidate's typed narrative upon error.
    - Disabled "Save to Profile" until valid skills are extracted.
    - Replaced misleading `"0 Extracted"` badge with `"Extraction Error"` indicator.

### Issue 6: Skill Gap Analyzer — React Duplicate Key Error ('SP-01')
* **Root Cause:**
  - **Span Index Collisions:** In `datasets/informal_skill_extraction/models/bio_tokenizer.py` and `skill_extractor.py`, extracted text spans are assigned sequential indices relative to that specific document: `span_id = f"SP-{idx + 1:02d}"`.
  - **Naive ID Assignment:** In `src/app/experience/page.tsx`, extracted skills were assigned `id: sp.span_id`. When a user ran extraction multiple times (e.g., testing different trade narratives) and saved them to their master profile, multiple distinct skills were stored in `user.skills` sharing the exact same ID (`"SP-01"`).
  - **Direct Key Usage:** In `src/app/skill-gap/page.tsx` line 328, the candidate skills inventory rendered `<span key={skill.id}>`. When candidate profile skills contained multiple items with `id: "SP-01"`, React raised the critical console error: `Encountered two children with the same key, 'SP-01'. Keys should be unique so that components maintain their identity across updates.`
* **Solution Implemented:**
  - **Data-Level Identity Architecture (`src/utils/skill-normalization.ts`):**
    - `generateCandidateSkillId(name, source, sourceId)`: Creates deterministic, namespaced, URI-safe identifiers: `cand-${sourcePrefix}-${baseSlug}` (e.g., `cand-resume-extracted-circuit-breaker-installation`, `cand-profile-verified-python`).
    - `deduplicateCandidateSkills(skills)`: Deduplicates skills by normalized canonical key (`normalizeSkillKey`), preserving distinct technologies (e.g., Java vs JavaScript, C vs C++ vs C#). When duplicate mentions occur, it merges enrichment metadata—retaining the highest confidence score, richest evidence text, and original source provenance.
    - **Taxonomy Preservation:** The original extraction span ID or official taxonomy reference is preserved intact in a dedicated `sourceId` and `canonicalSkillId` property, avoiding pollution or mutation of external taxonomy records.
  - **Experience Recognition & Profile Synchronization:**
    - Updated `src/app/experience/page.tsx`: Assigned namespaced entity IDs (`skill-canon-${canonical_id}` or `skill-span-${span_id}-${slug}`) while keeping `spanId: sp.span_id` as metadata. Deduplicated skills before appending to the master profile.
    - Updated `src/app/profile/page.tsx`: Ensured profile skill list rendering uses unique composite keys (`prof-skill-${createSkillId(skill.name)}-${skill.id || idx}`).
  - **Skill Gap Rendering Key Safety (`src/app/skill-gap/page.tsx`):**
    - Render key updated to: `key={`cand-pill-${skill.source}-${skill.id}`}`.
    - Verified all other `.map()` keys: target roles (`key={r.id}`), competency cards (`key={`card-${createSkillId(comp.skillName)}-${idx}`}`), and learning resources (`key={`res-${createSkillId(comp.skillName)}-${res.id || rIdx}`}`).
  - **Automated & Browser Verification:**
    - Added unit test suite `tests/test_skill_deduplication_and_keys.ts` covering 7 key test scenarios (100% pass).
    - Executed live browser test with simulated `SP-01` collision profile: confirmed 0 duplicate key warnings, flawless tag rendering, manual addition, and item deletion.

---

## 3. Automated Test Suite Execution (30/30 Passed)

The test suite in [test_critical_module_bug_fixes.py](file:///Users/ayushgupta/Desktop/Resume_Ai/backend/tests/test_critical_module_bug_fixes.py) was executed using pytest against the real FastAPI endpoints, SQLite database, and ML inference pipelines.

```
============================= test session starts ==============================
platform darwin -- Python 3.13.5, pytest-8.3.4, pluggy-1.5.0
rootdir: /Users/ayushgupta/Desktop/Resume_Ai/backend
collected 30 items

tests/test_critical_module_bug_fixes.py::test_01_assessment_session_start_and_masked_answers PASSED [  3%]
tests/test_critical_module_bug_fixes.py::test_02_assessment_next_blocked_without_selection_logic PASSED [  6%]
tests/test_critical_module_bug_fixes.py::test_03_assessment_answer_persistence_on_navigation PASSED [ 10%]
tests/test_critical_module_bug_fixes.py::test_04_assessment_submission_requires_all_answers_or_flags_unanswered PASSED [ 13%]
tests/test_critical_module_bug_fixes.py::test_05_assessment_all_answered_submits_successfully PASSED [ 16%]
tests/test_critical_module_bug_fixes.py::test_06_assessment_timer_expiry_state_calculation PASSED [ 20%]
tests/test_critical_module_bug_fixes.py::test_07_assessment_rapid_progress_idempotency PASSED [ 23%]
tests/test_critical_module_bug_fixes.py::test_08_assessment_reload_restores_active_session_state PASSED [ 26%]
tests/test_critical_module_bug_fixes.py::test_09_assessment_cancel_releases_session_lock PASSED [ 30%]
tests/test_critical_module_bug_fixes.py::test_10_sandbox_target_at_final_array_index_no_indexerror PASSED [ 33%]
tests/test_critical_module_bug_fixes.py::test_11_sandbox_empty_array_handled_safely PASSED [ 36%]
tests/test_critical_module_bug_fixes.py::test_12_sandbox_target_not_found_handled_safely PASSED [ 40%]
tests/test_critical_module_bug_fixes.py::test_13_sandbox_syntax_error_caught_safely PASSED [ 43%]
tests/test_critical_module_bug_fixes.py::test_14_sandbox_incorrect_output_fails_test_case PASSED [ 46%]
tests/test_critical_module_bug_fixes.py::test_15_sandbox_correct_implementation_passes_all_tests PASSED [ 50%]
tests/test_critical_module_bug_fixes.py::test_16_new_account_has_zero_candidate_skills PASSED [ 53%]
tests/test_critical_module_bug_fixes.py::test_17_skill_gap_analysis_empty_candidate_skills PASSED [ 56%]
tests/test_critical_module_bug_fixes.py::test_18_profile_skill_addition_source_metadata PASSED [ 60%]
tests/test_critical_module_bug_fixes.py::test_19_resume_parse_failure_no_fake_skills PASSED [ 63%]
tests/test_critical_module_bug_fixes.py::test_20_manually_added_skill_tagged_correctly PASSED [ 66%]
tests/test_critical_module_bug_fixes.py::test_21_gap_analysis_endpoint_graceful_handling PASSED [ 70%]
tests/test_critical_module_bug_fixes.py::test_22_candidate_skills_multi_tenant_isolation PASSED [ 73%]
tests/test_critical_module_bug_fixes.py::test_23_extract_endpoint_accepts_valid_request PASSED [ 76%]
tests/test_critical_module_bug_fixes.py::test_24_english_narrative_extracts_vocational_skills PASSED [ 80%]
tests/test_critical_module_bug_fixes.py::test_25_hindi_hinglish_electrician_narrative_extracts_skills PASSED [ 83%]
tests/test_critical_module_bug_fixes.py::test_26_blank_narrative_returns_validation_error_not_500 PASSED [ 86%]
tests/test_critical_module_bug_fixes.py::test_27_structured_error_response_format PASSED [ 90%]
tests/test_critical_module_bug_fixes.py::test_28_model_extractor_fallback_safeguard PASSED [ 93%]
tests/test_critical_module_bug_fixes.py::test_29_idempotent_extraction_retry PASSED [ 96%]
tests/test_critical_module_bug_fixes.py::test_30_skill_saving_requires_authentication_and_user_confirmation PASSED [100%]

======================= 30 passed, 3 warnings in 12.01s ========================
```

---

## 4. Key Files Inspected and Modified

| File | Change Summary |
|---|---|
| [backend/app/api/v1/skill.py](file:///Users/ayushgupta/Desktop/Resume_Ai/backend/app/api/v1/skill.py) | Fixed `default_config` NameError; added robust try/except error handling |
| [datasets/informal_skill_extraction/models/skill_extractor.py](file:///Users/ayushgupta/Desktop/Resume_Ai/datasets/informal_skill_extraction/models/skill_extractor.py) | Integrated automatic `OccupationClassifier` for trades without hint |
| [backend/app/services/sandboxes.py](file:///Users/ayushgupta/Desktop/Resume_Ai/backend/app/services/sandboxes.py) | Replaced mock runner with subprocess isolated test runner and resource limits |
| [backend/app/schemas/technical_assessment.py](file:///Users/ayushgupta/Desktop/Resume_Ai/backend/app/schemas/technical_assessment.py) | Added `AssessmentSessionProgressRequest` & `AssessmentSessionStateResponse` |
| [backend/app/api/v1/technical_assessments.py](file:///Users/ayushgupta/Desktop/Resume_Ai/backend/app/api/v1/technical_assessments.py) | Added active session tracking, `/sessions/{id}`, `/progress`, `/cancel` |
| [datasets/feature2/master_dataset.json](file:///Users/ayushgupta/Desktop/Resume_Ai/datasets/feature2/master_dataset.json) | Fixed `defective_routine_12` signature, statement, boundary test cases |
| [datasets/feature2/software_engineer/debugging/](file:///Users/ayushgupta/Desktop/Resume_Ai/datasets/feature2/software_engineer/debugging/) | Updated all 35 debugging question JSON definitions |
| [src/services/api-service.ts](file:///Users/ayushgupta/Desktop/Resume_Ai/src/services/api-service.ts) | Added `getAssessmentSession`, `saveAssessmentSessionProgress`, `cancelAssessmentSession` |
| [src/components/layout/AppShell.tsx](file:///Users/ayushgupta/Desktop/Resume_Ai/src/components/layout/AppShell.tsx) | Added `isLocked` prop pass-through to sidebar and header |
| [src/components/layout/DashboardSidebar.tsx](file:///Users/ayushgupta/Desktop/Resume_Ai/src/components/layout/DashboardSidebar.tsx) | Intercepts navigation when test is active with lock indicator |
| [src/components/layout/DashboardHeader.tsx](file:///Users/ayushgupta/Desktop/Resume_Ai/src/components/layout/DashboardHeader.tsx) | Intercepts brand logo click navigation during active test |
| [src/app/experience/page.tsx](file:///Users/ayushgupta/Desktop/Resume_Ai/src/app/experience/page.tsx) | Contextual error messages, narrative preservation, disables save on error, deduplicated profile save with distinct entity IDs |
| [src/app/skill-gap/page.tsx](file:///Users/ayushgupta/Desktop/Resume_Ai/src/app/skill-gap/page.tsx) | Purged 27 fake skills, added empty-state onboarding, source attribution badges, fixed duplicate React keys |
| [src/utils/skill-normalization.ts](file:///Users/ayushgupta/Desktop/Resume_Ai/src/utils/skill-normalization.ts) | Implemented `generateCandidateSkillId` and `deduplicateCandidateSkills` with metadata merging |
| [src/app/profile/page.tsx](file:///Users/ayushgupta/Desktop/Resume_Ai/src/app/profile/page.tsx) | Reinforced unique keys in profile skills rendering |
| [tests/test_skill_deduplication_and_keys.ts](file:///Users/ayushgupta/Desktop/Resume_Ai/tests/test_skill_deduplication_and_keys.ts) | Unit tests verifying span ID collision prevention, skill distinction (Java/JS, C/C++/C#), React key uniqueness |
| [src/app/assessment/page.tsx](file:///Users/ayushgupta/Desktop/Resume_Ai/src/app/assessment/page.tsx) | Disabled Next without selection, session rehydration, back button lock |

---

## 5. Verification Checklist & Visual Evidence

| Verification Target | Live Behavior Observed | Screenshot Reference |
|---|---|---|
| **Experience Recognition** | Hindi/Hinglish narrative extracts skills without 500 error; detects Electrician (TRD-02, 95% conf) | `docs/images/experience_verified.png` |
| **Skill Gap Analyzer** | Zero candidate skills displayed on empty state; authentic onboarding banner rendered | `docs/images/skill_gap_verified.png` |
| **Assessment Answering & Lock** | Next Question button disabled with warning message; sidebar shows `🔒 LOCKED` | `docs/images/assessment_locked_verified.png` |
| **Skill Gap Duplicate Key Fix** | 0 console duplicate-key warnings when rendering multiple skills with span_id `SP-01`; clean manual add and removal | [skill_gap_duplicate_key_fixed.png](file:///Users/ayushgupta/.gemini/antigravity/brain/254c5adc-170f-4e89-9dc1-d44fbc4d0a94/skill_gap_duplicate_key_fixed.png) |

- [x] **Assessment Next Validation:** Next button disabled until option is selected; displays `"Please select an answer before proceeding."`
- [x] **In-App Lock:** Sidebar navigation, brand logo, and browser back button intercepted during active timed assessment.
- [x] **Session Persistence:** Page reloads rehydrate answered questions, current index, and true remaining time from backend.
- [x] **IndexError Fixed:** Correct contract for `defective_routine_12(items, target)` across all 35 question definitions.
- [x] **Real Sandbox Execution:** Candidate code runs in isolated subprocess against real test inputs.
- [x] **Skill Gap Clean State:** Zero skills displayed for new accounts with verified empty state banner.
- [x] **Skill Gap Duplicate Key Elimination:** Unique namespaced identifiers (`cand-[source]-[slug]`), canonical deduplication merging confidence and evidence, and 0 React console warnings.
- [x] **Multi-Tenant Isolation:** Candidate skills from User A never appear for User B.
- [x] **Experience Recognition Fixed:** Hindi/Hinglish narrative extracts skills without 500 error; detects Electrician (TRD-02).
- [x] **Type Safety & Build:** 0 TypeScript compiler errors across entire repository.
