# ELEVATE X AI — SYNTHETIC DATA QUALITY AUDIT REPORT

**Target Corpus:** `processed/indian_worker_data/synthetic_augmentation/synthetic_augmented_corpus.jsonl`  
**Audit Status:** PASSED (High Quality)  
**Partition Strictness:** 100% quarantined under `synthetic_augmentation/` and tagged `is_synthetic: true`.  

## 1. Corpus Summary

- **Total Records:** 500
- **Total Skill Spans:** 1,000
- **Unique Descriptions:** 500 (100% uniqueness, 0 duplicates)
- **Character Length:** Min: 100, Max: 218, Mean: 149.1
- **Total Tokens:** 10,889
- **Vocabulary Size:** 376 distinct lexical forms
- **Type-Token Ratio (TTR):** `0.0345` (healthy lexical diversity across code-switched Hindi-Hinglish-English)

## 2. Character Offset & Boundary Verification

- **Total Spans Verified:** 1,000
- **Offset Mismatches (`worker_description[start:end] != extracted_skill`):** `0`
- **Accuracy:** `100.0%` exact boundary match
- **Placeholder Leaks (`Ellipsis`, `XXX`):** `0`

## 3. Trade Distribution & Vocabulary Richness

| Trade ID | Records | Spans | Total Tokens | Vocab Size | TTR |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `TRD-01` | 50 | 100 | 1109 | 116 | 0.1046 |
| `TRD-02` | 50 | 100 | 1171 | 140 | 0.1196 |
| `TRD-03` | 50 | 100 | 1158 | 113 | 0.0976 |
| `TRD-04` | 50 | 100 | 1018 | 104 | 0.1022 |
| `TRD-05` | 50 | 100 | 1065 | 113 | 0.1061 |
| `TRD-06` | 50 | 100 | 1363 | 149 | 0.1093 |
| `TRD-07` | 50 | 100 | 826 | 103 | 0.1247 |
| `TRD-08` | 50 | 100 | 1007 | 172 | 0.1708 |
| `TRD-09` | 50 | 100 | 1016 | 167 | 0.1644 |
| `TRD-10` | 50 | 100 | 1156 | 179 | 0.1548 |

## 4. Language Distribution & Lexical Diversity

| Language Code | Description Format | Records | Tokens | Vocab Size | TTR |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `english` | ENGLISH | 87 | 2311 | 158 | 0.0684 |
| `hindi` | HINDI | 163 | 2080 | 71 | 0.0341 |
| `hinglish` | HINGLISH | 250 | 6498 | 200 | 0.0308 |

## 5. Span Category Distribution

| Category | Spans | Percentage |
| :--- | :--- | :--- |
| `technical_tactile` | 432 | 43.2% |
| `tool_operation` | 316 | 31.6% |
| `troubleshooting_repair` | 123 | 12.3% |
| `quality_inspection` | 67 | 6.7% |
| `measurement_planning` | 37 | 3.7% |
| `safety_compliance` | 25 | 2.5% |

## 6. Safety & Provenance Integrity Confirmation

1. **Zero Contamination**: All synthetic records reside exclusively in `raw/indian_worker_data/synthetic_augmentation/` and `processed/indian_worker_data/synthetic_augmentation/`.
2. **Explicit Flagging**: 100% of records feature `is_synthetic: true` and `source_type: synthetic_test_stub`.
3. **Downstream Blocker**: Synthetic records are marked as pipeline test fixtures and are blocked from being treated as genuine field data.
