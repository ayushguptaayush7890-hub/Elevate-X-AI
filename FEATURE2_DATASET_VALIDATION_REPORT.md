# FEATURE 2 — DATASET VALIDATION REPORT
**Elevate X AI | Feature 2: Technical Assessment & Career Intelligence Engine**
**Validation Date:** 2026-11-15

---

## Dataset Overview

Feature 2 uses a curated question dataset organized by role and assessment type.

### Dataset Structure
```
datasets/feature2/
├── software_engineer/     mcq/, coding/, sql/, scenario/, debugging/, system_design/
├── ai_ml_engineer/        mcq/, coding/, sql/, scenario/, debugging/, system_design/
├── data_scientist/        mcq/, coding/, sql/, scenario/, debugging/, system_design/
├── frontend_developer/    mcq/, coding/, sql/, scenario/, debugging/, system_design/
├── backend_developer/     mcq/, coding/, sql/, scenario/, debugging/, system_design/
├── devops_engineer/       mcq/, coding/, sql/, scenario/, debugging/, system_design/
├── data_analyst/          mcq/, coding/, sql/, scenario/, debugging/, system_design/
├── cybersecurity_engineer/mcq/, coding/, sql/, scenario/, debugging/, system_design/
└── cloud_engineer/        mcq/, coding/, sql/, scenario/, debugging/, system_design/
```

### Dataset Characteristics

| Property | Value |
|---|---|
| Roles covered | 9 |
| Assessment types per role | 6 |
| Question format | JSON files, one question per file |
| ID format | `Q-{ROLE_CODE}-{TYPE_CODE}-{NNN}` |
| Minimum questions per combination | 2+ (verified by matrix test) |

---

## Dataset Content Validation

### MCQ Questions
- Each question has: `question_text`, `options` (4 choices A/B/C/D), `correct_answer`, `explanation`
- Difficulty levels: easy, medium, hard
- Role-specific content verified by manual inspection of sample questions

### Coding Questions
- Each question has: `question_text`, `sample_input`, `expected_output`, `visible_test_cases`, `coding_language`, `evaluation_rubric`
- Languages: Python (primary), JavaScript, SQL
- Contains literal newline characters in multi-line code blocks (normal for JSON)

### SQL Questions
- Each question has: `SQL_schema`, `sample_database`, `question_text`, `expected_output`
- Covers: JOINs, aggregations, window functions, subqueries, CTEs

### Scenario / System Design Questions
- Each question has: `question_text`, `evaluation_rubric`, `estimated_time`
- Open-ended text responses evaluated by rubric keyword matching

### Debugging Questions
- Each question has: `question_text` (buggy code), `expected_output`, `evaluation_rubric`
- Bugs include: off-by-one errors, type mismatches, logic errors, missing edge cases

---

## Data Quality Checks

| Check | Result |
|---|---|
| Questions served for all 54 role/type combinations | PASS |
| No missing required fields causing 500 errors | PASS |
| JSON parseable without control-character issues (backend) | PASS |
| IDs unique within each role/type | PASS (by naming convention) |
| MCQ options always include correct_answer | PASS (verified by scoring) |
| SQL schema fields populated for SQL questions | PASS |

---

## Limitations

| Limitation | Notes |
|---|---|
| No empirical difficulty calibration | IRT difficulty initialized from labels (easy/medium/hard), not from real candidate response data |
| No inter-rater reliability score | Questions authored without formal rubric validation |
| Dataset size | Adequate for testing; production use should expand to 50+ questions per combination |
| SQL schemas | Use representative but synthetic data, not production database schemas |

---

## Status: DATASET VALID FOR STAGING USE

