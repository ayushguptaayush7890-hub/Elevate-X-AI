# FEATURE 2 — ML AND ADAPTIVE ALGORITHM TEST REPORT
**Elevate X AI | Feature 2: Technical Assessment & Career Intelligence Engine**
**Test Date:** 2026-11-15

---

## 1. IRT (Item Response Theory) Model

### Model Type
1PL (One-Parameter Logistic) IRT — also known as the Rasch model.

### Mathematical Formulation
The probability of a correct response given candidate ability θ and item difficulty b:

```
P(correct | θ, b) = 1 / (1 + exp(-(θ - b)))
```

After each response, ability is updated using the gradient:
```
θ_new = θ_old + learning_rate * (response - P(correct|θ,b))
```

### Implementation Verification

| Criterion | Expected | Verified |
|---|---|---|
| Ability initialized | 0.0 | ✅ PASS |
| Ability bounds | [-4.0, +4.0] | ✅ PASS (clipping applied) |
| Item difficulty initialized | Varies by label (easy: -1.0, medium: 0.0, hard: 1.0) | ✅ PASS |
| Correct response increases ability | θ increases | ✅ PASS |
| Incorrect response decreases ability | θ decreases | ✅ PASS |
| Numerical stability | No NaN/Inf for extreme values | ✅ PASS (sigmoid bounded) |
| Cold-start behavior | First question at difficulty=0.0 (medium) | ✅ PASS |
| Question selection | Closest difficulty to current ability | ✅ PASS |

> [!NOTE]
> Item difficulty parameters are initialized from question labels (easy/medium/hard), NOT from empirical calibration on real candidate data. These are reasonable starting priors but are not calibrated to actual population response data.

---

## 2. Bayesian Skill Mastery Model

### Model Type
Beta-Bernoulli model with Beta prior and Bayesian posterior update.

### Mathematical Formulation
```
Prior: Beta(α=1.5, β=3.5)   → prior_mastery = α/(α+β) ≈ 0.3
Likelihood: Bernoulli(p)
Posterior: Beta(α + correct, β + incorrect)
Mastery: α_post / (α_post + β_post)
Confidence: 1 - 1/(1 + evidence_count)
```

### Implementation Verification

| Criterion | Expected | Verified |
|---|---|---|
| Prior mastery | ~0.3 | ✅ PASS |
| Correct answer → mastery increase | Yes | ✅ PASS |
| Incorrect answer → mastery decrease | Yes | ✅ PASS |
| `evidence_count` tracks observations | Increments per answer | ✅ PASS |
| Confidence grows with evidence | Low at start, high with many answers | ✅ PASS |
| `mastery_percentage` returned | 0–100 float | ✅ PASS |
| `confidence` returned | 0–1 float | ✅ PASS |
| Skill-specific aggregation | Each skill tracked independently | ✅ PASS |
| Small-sample behavior | Low confidence with 1-2 answers | ✅ PASS |
| Repeated-attempt accumulation | Evidence accumulates across attempts | ✅ PASS |

> [!NOTE]
> Confidence values should be interpreted carefully with small evidence counts (1-3 observations). The formula `1 - 1/(1+n)` grows slowly: at n=1, confidence=0.5; at n=5, confidence=0.83; at n=10, confidence=0.91. This is appropriately conservative.

---

## 3. ML Models

### Scoring Models

| Model | Type | Training | Status |
|---|---|---|---|
| MCQ Scorer | Exact match (option ID == correct_answer) | Rule-based | ✅ Functional |
| SQL Scorer | Keyword + structural analysis | Heuristic | ✅ Functional |
| Coding Scorer | Pattern matching + test case evaluation | Heuristic | ✅ Functional |
| Scenario Scorer | Keyword density + rubric matching | Heuristic | ✅ Functional |
| System Design Scorer | Rubric keyword matching | Heuristic | ✅ Functional |
| Debugging Scorer | Bug identification keyword + fix check | Heuristic | ✅ Functional |

> [!NOTE]
> Scoring models are heuristic/rule-based, not trained ML models with empirical validation datasets. The IRT and Bayesian mastery models are statistical models, not neural networks. This is appropriate for the current scope and clearly disclosed.

### Feature 1 ML Model (Indian XLM-RoBERTa)

| Criterion | Status |
|---|---|
| Model file exists | ✅ `datasets/informal_skill_extraction/models/` |
| Tokenizer loaded | ✅ PASS |
| Inference functional | ✅ PASS |
| Feature 1 regression tests | ✅ 52/52 PASS |
| Feature 2 changes affect F1 | ✅ NO — untouched |

---

## 4. Recommendation Engine

The recommendation engine:
- Identifies skills with mastery < 60% as "gaps"
- Maps skill gaps to curated learning resources per role
- Returns ordered roadmap with estimated completion times
- Verified functional: skill_gaps[] and recommendations[] returned in submit response

✅ FUNCTIONAL

---

## 5. Status: ADAPTIVE ALGORITHMS VERIFIED

