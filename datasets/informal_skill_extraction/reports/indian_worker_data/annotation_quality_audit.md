# ELEVATE X AI — ANNOTATION QUALITY & INTER-ANNOTATOR AGREEMENT AUDIT
**Audit Execution Timestamp**: 2026-11-14 21:20:38  
**Target Feature**: Informal Experience to Skill Extraction  
**Standard**: Exact Substring Invariant & Strict Boundary Verification  

---

## 1. Executive Summary
- **Total Genuine Records Annotated**: **0** (Collection pending)
- **Total Synthetic Stubs Evaluated**: 20 records
- **Total Skill Spans Evaluated**: 40 spans across 10 occupations
- **Character Offset Exactness**: 100.0% Exact Substring Match (0 errors)
- **Category Conformance**: 100.0% of spans belong to the 8 standard functional categories
- **Double-Annotation Protocol**: Established (20% blind double-annotation required on genuine data)

## 2. Eight Core Skill Categories Distribution (Pipeline Test Set)
| Skill Category | Description | Tagged Spans | Proportion |
|---|---|---|---|
| `technical_tactile` | Functional trade competency | 16 | 40.0% |
| `tool_operation` | Functional trade competency | 14 | 35.0% |
| `quality_inspection` | Functional trade competency | 3 | 7.5% |
| `troubleshooting_repair` | Functional trade competency | 5 | 12.5% |
| `safety_compliance` | Functional trade competency | 0 | 0.0% |
| `measurement_planning` | Functional trade competency | 2 | 5.0% |
| `client_communication` | Functional trade competency | 0 | 0.0% |
| `material_handling` | Functional trade competency | 0 | 0.0% |

## 3. Mathematical Agreement Framework for Field Collection
### A. Cohen's Kappa for Discrete Category Agreement
For spans where both annotators agree on the extracted boundary, category assignment agreement is calculated as:
$$\kappa = \frac{P_o - P_e}{1 - P_e}$$
Where $P_o$ is the observed proportion of category agreement, and $P_e$ is the expected chance agreement across the 8 categories.
- **Acceptance Threshold**: $\kappa \ge 0.85$.

### B. Strict Span-Level Precision, Recall, and F1
Because Cohen's Kappa suffers from the 'negative space paradox' on continuous character sequences (overinflating agreement due to thousands of unannotated non-skill characters), boundary agreement is evaluated using **Strict Span F1**:
- **True Positive (TP)**: Both start offset, end offset, and skill category match identically: $(\text{start}_1 = \text{start}_2) \land (\text{end}_1 = \text{end}_2) \land (\text{cat}_1 = \text{cat}_2)$.
- **False Positive (FP)**: Span tagged by Annotator 1 but not matching Annotator 2.
- **False Negative (FN)**: Span tagged by Annotator 2 but not matching Annotator 1.
$$\text{Precision} = \frac{TP}{TP + FP}, \quad \text{Recall} = \frac{TP}{TP + FN}, \quad F_1 = \frac{2 \times \text{Precision} \times \text{Recall}}{\text{Precision} + \text{Recall}}$$
- **Acceptance Threshold**: Strict Span $F_1 \ge 0.88$.

### C. Expert Adjudication Protocol
Any record with overlapping spans ($\text{IoU} < 1.0$) or category discordance is automatically assigned `reviewer_status = 'flagged_for_adjudication'`. Discrepancies are adjudicated by a senior certified ITI master instructor.

## 4. Current Quality Status
> [!IMPORTANT]
> **Ground Truth Verification**: The annotation evaluation math, offset test suites, and adjudication workflows are **operational**. Real agreement metrics will be computed dynamically upon ingestion of the Stage 1 Pilot field batch.
