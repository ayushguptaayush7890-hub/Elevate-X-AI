# FEATURE 2: MACHINE LEARNING & STATISTICAL MODEL AUDIT REPORT
**Elevate X AI — Technical Assessment & Career Intelligence Engine**  
**Execution Date:** November 15, 2026  
**Auditor:** Machine Learning Verification Engineer  

---

## 1. Inventory of AI/ML Models in Elevate X AI

Elevate X AI maintains strict architectural boundaries between its ML models:

| Component | Model Class | Purpose | Source / Artifact |
|---|---|---|---|
| **Feature 1** | Indian XLM-RoBERTa Token Classifier | Extracts informal vocational skills from Indian workers across 10 trades | Pretrained checkpoint in `backend/app/models/` |
| **Feature 2** | 1PL Item Response Theory (Rasch Model) | Calibrates candidate ability $\theta \in [-3, 3]$ and dynamically selects next question | Psychometric engine in `adaptive_engine.py` |
| **Feature 2** | Bayesian Skill Mastery Engine | Multi-attempt evidence aggregation with exponential confidence saturation | Analytical service in `skill_mastery_service.py` |
| **Feature 2** | Grounded Narrative & Feedback Service | Generates tailored feedback on candidate strengths and gaps | LLM service with offline deterministic fallback |

---

## 2. Feature 1 Model Protection & Verification

- **Constraint Check:** The Indian XLM-RoBERTa checkpoint was **not modified or retrained**.
- **Model Checkpoint Tests:** All 7 canonical mapping tests and 4 Indian mock model tests in `tests/test_indian_mock_model.py` and `tests/test_experience_recognition_regression.py` passed with 100% fidelity.
- **Zero Regression:** Trade vocabulary for electricians, plumbers, tailors, motor mechanics, welders, and carpenters remains fully protected.

---

## 3. Feature 2 Psychometric & Analytical Model Tests

All 9 tests in [tests/test_feature2_adaptive_irt.py](file:///Users/ayushgupta/Desktop/Resume_Ai/backend/tests/test_feature2_adaptive_irt.py) passed:
1. `test_probability_calculation_at_equilibrium`: Rasch formula verified ($P = 0.5000$ when $\theta = b$).
2. `test_probability_monotonicity`: Probability increases monotonically with higher ability.
3. `test_ability_increases_on_correct_answer`: Latent $\theta$ increases on successful responses.
4. `test_ability_decreases_on_incorrect_answer`: Latent $\theta$ decreases on incorrect responses.
5. `test_numerical_bounds_enforced`: $\theta$ strictly constrained to $[-3.0, +3.0]$ without floating-point overflow.
6. `test_cold_start_recommends_medium`: Cold-start prior $\theta = 0.0$ correctly picks medium items.
7. `test_score_mapping_normalized`: Logistic sigmoid normalizes $\theta$ to $[0, 100]\%$.
8. `test_evidence_volume_increases_confidence`: Confidence saturates smoothly as evidence volume grows ($C = 1 - e^{-0.35N}$).
9. `test_skill_performance_weighting`: Item difficulty weights (1.0, 1.5, 2.0) correctly scale proficiency scores.

---

## 4. LLM Feedback & Offline Fallback Reliability

The `llm_feedback_service.py` evaluates candidate system design and scenario responses:
- When an external LLM API key is absent or unreachable, the system executes a **deterministic rubric-based fallback**.
- Fallback extracts architectural keywords, security considerations, and scalability terms to award partial marks and generate structured recommendations.
- Guarantees that candidate assessment submission never fails due to third-party API downtime.

