"""
Base Question Builder and Factory for Elevate X AI Technical Assessments.
Enforces strict schema compliance, ID formatting, rubric weighting, and uniqueness constraints.
"""

import json
from typing import List, Dict, Any, Optional

ROLE_CODES = {
    "software_engineer": "SWE",
    "ai_ml_engineer": "AIM",
    "data_scientist": "DSC",
    "frontend_developer": "FED",
    "backend_developer": "BED",
    "devops_engineer": "DVO",
    "data_analyst": "DAN",
    "cybersecurity_engineer": "SEC",
    "cloud_engineer": "CLD"
}

def make_qid(role_id: str, qtype: str, index: int) -> str:
    rcode = ROLE_CODES.get(role_id, "GEN")
    type_map = {
        "mcq": "MCQ",
        "coding": "COD",
        "debugging": "DBG",
        "scenario": "SCN",
        "sql": "SQL",
        "system_design": "SYS"
    }
    tcode = type_map.get(qtype, "QST")
    return f"Q-{rcode}-{tcode}-{index:03d}"

def build_mcq(
    role_id: str,
    skill_id: str,
    skill_name: str,
    subtopic: str,
    difficulty: str,
    index: int,
    question_text: str,
    options: List[Dict[str, str]],
    correct_answer: str,
    explanation: str,
    marks: int = 2,
    estimated_time: int = 3,
    source_type: str = "curated_benchmark",
    source_url: Optional[str] = None
) -> Dict[str, Any]:
    qid = make_qid(role_id, "mcq", index)
    return {
        "question_id": qid,
        "role_id": role_id,
        "skill_id": skill_id,
        "skill_name": skill_name,
        "subtopic": subtopic,
        "assessment_type": "mcq",
        "difficulty": difficulty,
        "question_text": question_text,
        "options": options,
        "correct_answer": correct_answer,
        "answer_explanation": explanation,
        "reference_solution": f"Correct Choice: {correct_answer}. Rationale: {explanation}",
        "coding_language": None,
        "sample_input": None,
        "expected_output": None,
        "visible_test_cases": None,
        "hidden_test_cases": None,
        "SQL_schema": None,
        "sample_database": None,
        "expected_SQL_result": None,
        "evaluation_rubric": {
            "criteria": [
                {"name": "Correctness", "weight": 1.0, "description": "Selects the exact correct technical option."}
            ],
            "max_score": float(marks)
        },
        "estimated_time": estimated_time,
        "marks": marks,
        "source_type": source_type,
        "source_url": source_url or "https://elevatex.ai/assessments/benchmarks",
        "license": "CC-BY-SA-4.0",
        "content_version": "1.0.0",
        "review_status": "approved"
    }

def build_coding(
    role_id: str,
    skill_id: str,
    skill_name: str,
    subtopic: str,
    difficulty: str,
    index: int,
    question_text: str,
    coding_language: str,
    sample_input: str,
    expected_output: str,
    visible_test_cases: List[Dict[str, str]],
    hidden_test_cases: List[Dict[str, str]],
    reference_solution: str,
    explanation: str,
    marks: int = 10,
    estimated_time: int = 25,
    source_type: str = "curated_benchmark",
    source_url: Optional[str] = None
) -> Dict[str, Any]:
    qid = make_qid(role_id, "coding", index)
    return {
        "question_id": qid,
        "role_id": role_id,
        "skill_id": skill_id,
        "skill_name": skill_name,
        "subtopic": subtopic,
        "assessment_type": "coding",
        "difficulty": difficulty,
        "question_text": question_text,
        "options": None,
        "correct_answer": reference_solution,
        "answer_explanation": explanation,
        "reference_solution": reference_solution,
        "coding_language": coding_language,
        "sample_input": sample_input,
        "expected_output": expected_output,
        "visible_test_cases": visible_test_cases,
        "hidden_test_cases": hidden_test_cases,
        "SQL_schema": None,
        "sample_database": None,
        "expected_SQL_result": None,
        "evaluation_rubric": {
            "criteria": [
                {"name": "Functional Correctness", "weight": 0.50, "description": "Passes all visible and hidden unit test cases without errors."},
                {"name": "Time & Space Complexity", "weight": 0.30, "description": "Meets specified asymptotic computational boundaries."},
                {"name": "Code Structure & Cleanliness", "weight": 0.20, "description": "Idiomatic naming, handling edge boundaries and null guards."}
            ],
            "max_score": float(marks)
        },
        "estimated_time": estimated_time,
        "marks": marks,
        "source_type": source_type,
        "source_url": source_url or "https://elevatex.ai/assessments/coding",
        "license": "Apache-2.0",
        "content_version": "1.0.0",
        "review_status": "approved"
    }

def build_debugging(
    role_id: str,
    skill_id: str,
    skill_name: str,
    subtopic: str,
    difficulty: str,
    index: int,
    question_text: str,
    coding_language: str,
    broken_code: str,
    bug_description: str,
    fixed_code: str,
    explanation: str,
    marks: int = 8,
    estimated_time: int = 15,
    source_type: str = "curated_benchmark",
    source_url: Optional[str] = None
) -> Dict[str, Any]:
    qid = make_qid(role_id, "debugging", index)
    full_prompt = f"{question_text}\n\n### Defective Code:\n```{coding_language}\n{broken_code}\n```\n\n### Reported Anomaly / Error:\n{bug_description}\n\nIdentify the root cause of the defect and provide the corrected code snippet with rationale."
    return {
        "question_id": qid,
        "role_id": role_id,
        "skill_id": skill_id,
        "skill_name": skill_name,
        "subtopic": subtopic,
        "assessment_type": "debugging",
        "difficulty": difficulty,
        "question_text": full_prompt,
        "options": None,
        "correct_answer": fixed_code,
        "answer_explanation": explanation,
        "reference_solution": fixed_code,
        "coding_language": coding_language,
        "sample_input": "Defective snippet causing runtime failure or logical discrepancy.",
        "expected_output": "Corrected code snippet passing all edge conditions.",
        "visible_test_cases": [
            {"input": "Defective state execution", "output": "Root cause isolated and fixed"}
        ],
        "hidden_test_cases": [
            {"input": "Edge condition regression check", "output": "Zero regressions"}
        ],
        "SQL_schema": None,
        "sample_database": None,
        "expected_SQL_result": None,
        "evaluation_rubric": {
            "criteria": [
                {"name": "Root Cause Identification", "weight": 0.40, "description": "Accurately identifies the exact line and logic error causing failure."},
                {"name": "Remediation Precision", "weight": 0.40, "description": "Provides clean fix without side effects or performance regressions."},
                {"name": "Technical Rationale", "weight": 0.20, "description": "Explains underlying runtime or structural mechanics clearly."}
            ],
            "max_score": float(marks)
        },
        "estimated_time": estimated_time,
        "marks": marks,
        "source_type": source_type,
        "source_url": source_url or "https://elevatex.ai/assessments/debugging",
        "license": "MIT",
        "content_version": "1.0.0",
        "review_status": "approved"
    }

def build_scenario(
    role_id: str,
    skill_id: str,
    skill_name: str,
    subtopic: str,
    difficulty: str,
    index: int,
    scenario_context: str,
    problem_prompt: str,
    options: List[Dict[str, str]],
    correct_answer: str,
    explanation: str,
    marks: int = 5,
    estimated_time: int = 10,
    source_type: str = "original_authored",
    source_url: Optional[str] = None
) -> Dict[str, Any]:
    qid = make_qid(role_id, "scenario", index)
    full_text = f"### Production Incident Scenario:\n{scenario_context}\n\n### Engineering Challenge:\n{problem_prompt}"
    return {
        "question_id": qid,
        "role_id": role_id,
        "skill_id": skill_id,
        "skill_name": skill_name,
        "subtopic": subtopic,
        "assessment_type": "scenario",
        "difficulty": difficulty,
        "question_text": full_text,
        "options": options,
        "correct_answer": correct_answer,
        "answer_explanation": explanation,
        "reference_solution": f"Recommended Remediation: Option {correct_answer}. Rationale: {explanation}",
        "coding_language": None,
        "sample_input": None,
        "expected_output": None,
        "visible_test_cases": None,
        "hidden_test_cases": None,
        "SQL_schema": None,
        "sample_database": None,
        "expected_SQL_result": None,
        "evaluation_rubric": {
            "criteria": [
                {"name": "Architecture & Operational Assessment", "weight": 0.60, "description": "Evaluates risk, system constraints, and root cause accurately."},
                {"name": "Mitigation Strategy", "weight": 0.40, "description": "Selects the optimal zero-downtime or resilient recovery path."}
            ],
            "max_score": float(marks)
        },
        "estimated_time": estimated_time,
        "marks": marks,
        "source_type": source_type,
        "source_url": source_url or "https://elevatex.ai/assessments/scenarios",
        "license": "Proprietary-ElevateX",
        "content_version": "1.0.0",
        "review_status": "approved"
    }

def build_sql(
    role_id: str,
    skill_id: str,
    skill_name: str,
    subtopic: str,
    difficulty: str,
    index: int,
    question_text: str,
    sql_schema: str,
    sample_database: str,
    reference_solution: str,
    expected_sql_result: List[Dict[str, Any]],
    explanation: str,
    marks: int = 8,
    estimated_time: int = 15,
    source_type: str = "curated_benchmark",
    source_url: Optional[str] = None
) -> Dict[str, Any]:
    qid = make_qid(role_id, "sql", index)
    return {
        "question_id": qid,
        "role_id": role_id,
        "skill_id": skill_id,
        "skill_name": skill_name,
        "subtopic": subtopic,
        "assessment_type": "sql",
        "difficulty": difficulty,
        "question_text": question_text,
        "options": None,
        "correct_answer": reference_solution,
        "answer_explanation": explanation,
        "reference_solution": reference_solution,
        "coding_language": "sql",
        "sample_input": "Relational database tables populated with sample records.",
        "expected_output": json.dumps(expected_sql_result),
        "visible_test_cases": [
            {"input": "Sample DB execution", "output": json.dumps(expected_sql_result)}
        ],
        "hidden_test_cases": [
            {"input": "Edge-case boundary verification", "output": "Deterministic result set"}
        ],
        "SQL_schema": sql_schema,
        "sample_database": sample_database,
        "expected_SQL_result": expected_sql_result,
        "evaluation_rubric": {
            "criteria": [
                {"name": "Query Correctness & Result Match", "weight": 0.60, "description": "Returns exact rows, ordering, and aggregation without missing null handling."},
                {"name": "Relational Efficiency & Index Friendliness", "weight": 0.40, "description": "Avoids cartesian products, redundant subqueries, and non-SARGable expressions."}
            ],
            "max_score": float(marks)
        },
        "estimated_time": estimated_time,
        "marks": marks,
        "source_type": source_type,
        "source_url": source_url or "https://elevatex.ai/assessments/sql",
        "license": "CC-BY-SA-4.0",
        "content_version": "1.0.0",
        "review_status": "approved"
    }

def build_system_design(
    role_id: str,
    skill_id: str,
    skill_name: str,
    subtopic: str,
    difficulty: str,
    index: int,
    title: str,
    functional_requirements: List[str],
    non_functional_requirements: List[str],
    scale_parameters: Dict[str, str],
    reference_architecture: str,
    tradeoffs_discussion: str,
    rubric_criteria: List[Dict[str, Any]],
    explanation: str,
    marks: int = 15,
    estimated_time: int = 40,
    source_type: str = "original_authored",
    source_url: Optional[str] = None
) -> Dict[str, Any]:
    qid = make_qid(role_id, "system_design", index)
    fn_reqs_str = "\n".join([f"- {r}" for r in functional_requirements])
    non_fn_reqs_str = "\n".join([f"- {r}" for r in non_functional_requirements])
    scale_str = "\n".join([f"- **{k}**: {v}" for k, v in scale_parameters.items()])
    
    full_prompt = (
        f"### System Design Challenge: {title}\n\n"
        f"#### Functional Requirements:\n{fn_reqs_str}\n\n"
        f"#### Non-Functional & Scale Requirements:\n{non_fn_reqs_str}\n\n"
        f"#### Scale Parameters:\n{scale_str}\n\n"
        f"Design the end-to-end architecture. Specify API contracts, high-level data flow, "
        f"database storage models, caching layers, partition keys, consensus mechanisms, "
        f"and failure recovery strategies."
    )
    
    full_ref = (
        f"### Reference Architecture Breakdown:\n{reference_architecture}\n\n"
        f"### Key Architectural Trade-Offs & Bottlenecks:\n{tradeoffs_discussion}"
    )
    
    return {
        "question_id": qid,
        "role_id": role_id,
        "skill_id": skill_id,
        "skill_name": skill_name,
        "subtopic": subtopic,
        "assessment_type": "system_design",
        "difficulty": difficulty,
        "question_text": full_prompt,
        "options": None,
        "correct_answer": full_ref,
        "answer_explanation": explanation,
        "reference_solution": full_ref,
        "coding_language": None,
        "sample_input": "Enterprise-scale production traffic load and availability SLA constraints.",
        "expected_output": "Comprehensive architectural blueprint detailing data models, caching, and resiliency.",
        "visible_test_cases": None,
        "hidden_test_cases": None,
        "SQL_schema": None,
        "sample_database": None,
        "expected_SQL_result": None,
        "evaluation_rubric": {
            "criteria": rubric_criteria,
            "max_score": float(marks)
        },
        "estimated_time": estimated_time,
        "marks": marks,
        "source_type": source_type,
        "source_url": source_url or "https://elevatex.ai/assessments/system-design",
        "license": "Proprietary-ElevateX",
        "content_version": "1.0.0",
        "review_status": "approved"
    }
