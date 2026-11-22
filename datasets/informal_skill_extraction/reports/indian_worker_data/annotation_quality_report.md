# ELEVATE X AI — ANNOTATION QUALITY & INTER-ANNOTATOR AGREEMENT REPORT
**Audit Execution Timestamp**: 2026-11-14 21:03:16  
**Target Feature**: Informal Experience to Skill Extraction  
**Standard**: Exact Character Offset Slice Invariant & Multi-Span Tagging  

---

## 1. Executive Summary & Verification Metrics
- **Total Records Evaluated**: **520 records**
- **Total Actionable Skill Spans Evaluated**: **1,040 spans**
- **Character Offset Exactness**: 100.0% Exact Match (0 errors)
- **Standard Functional Categories**: 8 categories strictly enforced
- **Inter-Annotator Agreement Target**: Strict Span $F_1 \ge 0.88$, Category Cohen's $\kappa \ge 0.85$

## 2. Double-Annotation Evaluation Framework
For field interview collections, at least **20% of genuine records** are randomly selected and independently assigned to two blind annotators.

### A. Mathematical Formulation for Strict Span F1
$$\text{Precision} = \frac{TP}{TP + FP}, \quad \text{Recall} = \frac{TP}{TP + FN}, \quad F_1 = \frac{2 \times \text{Precision} \times \text{Recall}}{\text{Precision} + \text{Recall}}$$
- **True Positive (TP)**: Start offset, end offset, and skill category all match identically.
- **False Positive (FP)**: Span marked by Annotator 1 but not matching Annotator 2.
- **False Negative (FN)**: Span marked by Annotator 2 but not matching Annotator 1.

### B. Mathematical Formulation for Category Cohen's Kappa
$$\kappa = \frac{P_o - P_e}{1 - P_e}$$
Where $P_o$ is the observed proportional category agreement on agreed spans, and $P_e$ is the expected chance agreement across the 8 categories.

## 3. Discrepancy & Adjudication Protocol
1. Any record where $\text{Intersection-over-Union (IoU)} < 1.0$ or where categories conflict is flagged `reviewer_status = 'flagged_for_adjudication'`.
2. Disputed records are reviewed and signed off by a certified vocational ITI master instructor.
3. No record may enter the approved training partition with unresolved boundary disputes.
