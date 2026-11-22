# Elevate X AI — Milestone 2 Test Input Count Audit Report

**Audit Date:** November 22, 2026  
**Auditor:** Antigravity Engineering  
**Scope:** Complete repository audit of Milestone 2 test artifacts, test execution logs, documentation, and evaluation tables.  
**Strict Inclusion Criterion:** Only test records containing all four mandatory fields are counted:
1. **Specific Test Input** (exact payload, endpoint, or parameters)
2. **Expected Output** (explicit assertion or expected behavior)
3. **Actual Output** (verbatim response payload or runtime observation)
4. **Pass/Fail Status** (explicit execution verdict)

---

## 1. Executive Summary & Verification Counts

Following a strict source-code, artifact, and runtime log audit across all repository files and test artifacts, exactly **12 valid test inputs** meet the four mandatory fields.

### Summary Statistics

| Metric | Count | Details |
| :--- | :---: | :--- |
| **Total Valid Test Inputs** | **12** | Exactly meets all 4 required fields across documented test suites |
| **Normal Input Cases** | **7** | Standard valid payloads across Auth, Health, Assessment, Sandboxes |
| **Edge Cases** | **2** | Boundary inputs: whitespace-only text (`TC-05`), IRT floor score (`TC-09`) |
| **Invalid Cases** | **3** | Unregistered auth (`TC-03`), code injection (`TC-11`), DDL injection (`TC-12`) |
| **Pass Count** | **10** | Verified matching expected behavior / expected security rejection |
| **Fail Count** | **2** | Unhandled 500 error on informal extraction model loading (`TC-04`, `TC-05`) |

---

## 2. Master Table of Valid Test Inputs

The following table records every valid Milestone 2 test input satisfying all four criteria.

| Test ID | Module | Specific Input | Expected Output | Actual Output | Status |
| :--- | :--- | :--- | :--- | :--- | :---: |
| **TC-01** | System Health & Diagnostics | `GET /api/v1/health` (No query/body parameters) | HTTP 200 OK with `status='healthy'`, `version='1.0.0'` | `{"status":"healthy","version":"1.0.0","timestamp":"2026-11-19T20:35:22.412510Z","environment":"development"}` | **PASS** |
| **TC-02** | Authentication & Identity | `{"email": "m2_candidate_3afe24@example.com", "password": "[REDACTED_PASSWORD]", "full_name": "Milestone Test Candidate"}` | HTTP 201 Created on register, HTTP 200 OK on login with valid bearer access_token | `{"token": {"access_token": "eyJh...[REDACTED_ACCESS_TOKEN]", "refresh_token": "eyJh...[REDACTED_REFRESH_TOKEN]", "token_type": "bearer", "expires_in": 86400}, "user": {"id": "d30bfaf3-7b8f-4e5b-a6e3-12e2f005b33c", "email": "m2_candidate_3afe24@example.com", "full_name": "Milestone Test Candidate", "role": "user", "is_active": true, "is_verified": false, "created_at": "2026-11-19T20:35:22"}}` | **PASS** |
| **TC-03** | Authentication & Identity | `{"email": "unregistered_candidate_9921@example.com", "password": "[REDACTED]"}` | HTTP 401 Unauthorized with detail `'Incorrect email or password'` | `{"success":false,"error":{"code":"HTTPException","message":"Incorrect email or password"}}` | **PASS** |
| **TC-04** | Feature 1: Skill Extraction | `{"text": "Maine 5 saal tak Juki single needle lockstitch machine par kaam kiya hai aur cotton fabric cutting aur garment finishing ki hai."}` | HTTP 200 OK with detected_occupation and extracted_skills entities | `{"success":false,"error":{"code":"InternalServerError","message":"No module named 'datasets.informal_skill_extraction.models.model_config'"}}` | **FAIL** |
| **TC-05** | Feature 1: Skill Extraction | `{"text": "   "}` (Pure whitespace / empty narrative string) | HTTP 422 Unprocessable Entity rejecting blank narrative | `{"success":false,"error":{"code":"InternalServerError","message":"No module named 'datasets.informal_skill_extraction.models.model_config'"}}` | **FAIL** |
| **TC-06** | Feature 2: Technical Assessment | `GET /api/v1/technical-assessments/roles` | HTTP 200 OK with list of >=5 technical vocational roles | `[{"role_id":"software_engineer","title":"Software Engineer","category":"Core Engineering","description":"Generalist software engineer specializing in algorithmic problem solving, clean system architecture, concurrency, and robust software craftsmanship.","skill_count":5},{"role_id":"ai_ml_engineer",...}]` | **PASS** |
| **TC-07** | Feature 2: Technical Assessment | `{"role_id": "software_engineer", "difficulty": "adaptive", "question_count": 5}` | HTTP 200 OK returning session_id, role_title, and masked questions | `{"session_id": "1972112e-c820-4968-b39d-1b821c75506d", "role_title": "Software Engineer", "total_questions": 5, "question_sample_id": "Q-SWE-SCN-038"}` | **PASS** |
| **TC-08** | Feature 2: Adaptive IRT Engine | `{"session_id": "1972112e-c820-4968-b39d-1b821c75506d", "question_id": "Q-SWE-SCN-038", "answer": "A"}` | HTTP 200 OK with `is_correct=True`, `points_awarded > 0`, and `current_theta` updated | `{"is_correct":true,"points_awarded":6.0,"explanation":"Under high concurrency in API Architecture & Distributed RPC, thread contention on coarse-grained synchronization locks causes thread convoying...","current_theta":0.2,"recommended_difficulty":"medium","next_question":{...},"is_completed":false}` | **PASS** |
| **TC-09** | Feature 2: Adaptive IRT Engine | `{"session_id": "1972112e-c820-4968-b39d-1b821c75506d", "question_id": "Q-SWE-SCN-005", "answer": "DEFINITELY_INCORRECT_ANSWER_CHOICE_XYZ"}` | HTTP 200 OK with `is_correct=False` and `current_theta` maintained within bounded range [-3.0, 3.0] | `{"is_correct":false,"points_awarded":0.0,"explanation":"Under high concurrency in Data Structures & Algorithms, thread contention...","current_theta":-0.02,"recommended_difficulty":"medium","next_question":{...},"is_completed":false}` | **PASS** |
| **TC-10** | Feature 2: Code Execution Sandbox | `{"language": "python", "code": "def solution(a, b):\n    return a + b\n", "visible_test_cases": [{"input": "2, 3", "output": "5"}, {"input": "10, -2", "output": "8"}]}` | HTTP 200 OK with `passed=True`, `error=None`, `execution_time_ms < 2000` | `{"passed":true,"score":1.0,"total_tests":2,"passed_tests":2,"test_results":[{"test":"2, 3","status":"PASSED"},{"test":"10, -2","status":"PASSED"}],"error":null,"execution_time_ms":43.25}` | **PASS** |
| **TC-11** | Feature 2: Code Sandbox Security | `{"language": "python", "code": "import os\nos.system('echo malicious_call_attempt')\n", "visible_test_cases": []}` | HTTP 200 OK with `passed=False` and Security Alert rejecting restricted os module | `{"passed":false,"score":0.0,"total_tests":0,"passed_tests":0,"test_results":[],"error":"Security Alert: Restricted system call, network operation, or secret inspection detected in submitted code.","execution_time_ms":0.0}` | **PASS** |
| **TC-12** | Feature 2: SQL Sandbox Security | `{"schema_sql": "CREATE TABLE candidates (id INT PRIMARY KEY, name TEXT);", "sample_db_sql": "INSERT INTO candidates VALUES (1, 'Alice');", "candidate_query": "DROP TABLE candidates;"}` | HTTP 200 OK with `passed=False` and error indicating DDL operations (DROP) are disallowed | `{"passed":false,"score":0.0,"actual_rows":[],"error":"Only read-only queries (SELECT / WITH) are permitted. Received: DROP","execution_time_ms":0.0}` | **PASS** |

---

## 3. Exact Source Files and Locations

The authentic data records powering this audit are preserved in the following project locations:

1. **Master Test Report Markdown:**
   - **Path:** `backup_pre_restoration/milestone2_test_report.md` (and artifact `milestone2_test_report`)
   - **Section:** Section 1 (*Executive Summary Table*, lines 13–28) and Section 3 (*Comprehensive Test Case Details*, lines 43–250)
   - **Full Path:** `/Users/ayushgupta/.gemini/antigravity/brain/254c5adc-170f-4e89-9dc1-d44fbc4d0a94/backup_pre_restoration/milestone2_test_report.md`
2. **Raw JSON Test Execution Database:**
   - **Path:** `scratch/m2_results.json`
   - **Full Path:** `/Users/ayushgupta/.gemini/antigravity/brain/254c5adc-170f-4e89-9dc1-d44fbc4d0a94/scratch/m2_results.json`
   - **Contains:** Complete machine-readable dictionary for `TC-01` through `TC-12` with timestamps, verbatim input payloads, HTTP statuses, and JSON responses.

---

## 4. Excluded Tables and Exclusion Rationale

Every other test, evaluation, and benchmark table in the repository was audited against the four-field rule. The following tables were excluded:

| File / Document | Location / Table Description | Missing Required Field(s) | Exclusion Rationale |
| :--- | :--- | :--- | :--- |
| `docs/resume_builder_implementation_report.md` | Line 41 (`\| Operation \| Input Length \| Output Length... \|`) | Specific Input, Expected Output, Actual Output | Records aggregate metadata (character lengths and latency) rather than verbatim input payloads and actual outputs. |
| `docs/skill_gap_frontend_repair_report.md` | Line 93 (`\| Test Scenario \| Input / Action \| Expected Behavior... \|`) | Actual Output | Documents test actions and expected behaviors, but omits verbatim recorded actual system outputs. |
| `docs/feature1_model_only_improvement_report.md` | Line 132 (`\| Test ID \| Input Text \| Extracted Skills... \| Result \|`) | Expected Output | Contains verbatim input text and extracted skills, but lacks a dedicated Expected Output column. |
| `docs/career_roadmap_implementation_report.md` | Line 203 (`\| # \| Test Case \| Target Role / Scenario... \|`) | Specific Input, Expected Output, Actual Output | High-level test summary table lacking raw input payloads, expected responses, and actual response bodies. |
| `docs/career_transition_evaluation_report.md` | Line 46 (`\| Test Case \| Description \| HTTP Status \| Result \|`) | Specific Input, Expected Output, Actual Output | Lists test function names and HTTP status codes, but lacks raw request bodies and actual output responses. |
| `docs/skill_gap_analyzer_repair_report.md` | Line 53 & Line 167 | Expected Output, Actual Output, Pass/Fail Status | Line 53 compares model classifications; Line 167 records request payload and status assertions, but lacks discrete expected vs actual output columns and a Pass/Fail column. |
| `backend/tests/test_feature2_matrix_54.py` & other test scripts | Pytest execution scripts across `backend/tests/` | Tabular Four-Field Record | Pytest source code files and fixtures without a documented four-field static test execution table. |

---

## 5. Final Audit Conclusion

Based on strict adherence to the four-field requirement (Specific Test Input, Expected Output, Actual Output, Pass/Fail Status), only the 12 execution-verified Milestone 2 test cases qualify.

**TOTAL VALID TEST INPUTS: 12**
