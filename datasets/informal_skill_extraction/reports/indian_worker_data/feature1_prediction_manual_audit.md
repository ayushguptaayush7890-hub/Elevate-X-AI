# ELEVATE X AI — FEATURE 1: MANUAL AUDIT OF 100 PREDICTION SAMPLES

## 1. Audit Verification Summary

- **Samples Audited:** `100`
- **Exact Matches Verified:** `179`
- **False Positives Categorized:** `38`
- **False Negatives Categorized:** `37`
- **Character Offset Slices Verified (`text[st:en] == span`):** `217` (0 mismatches)

## 2. Error Taxonomy & Qualitative Insights

1. **Auxiliary Verb Boundary Trimming:** The primary cause of false positives/negatives in exact span evaluation is boundary disagreement on trailing compound light verbs (e.g. *karna*, *hona*, *lagana*).
2. **Category Classification Accuracy:** Over 94% of true positive skill spans were assigned the correct functional category matching the gold taxonomy.
