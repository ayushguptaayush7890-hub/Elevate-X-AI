# ELEVATE X AI — FEATURE 1: INDIAN MOCK DATASET BENCHMARK REPORT

> **EVALUATION SET:** 550 Records | 10 Occupations (55 each) | 5 Linguistic Modes (110 each)

## 1. Overall Primary Model Performance (Model B: XLM-RoBERTa)

- **Exact Span Precision:** `0.8316`
- **Exact Span Recall:** `0.8352`
- **Exact Span F1 Score:** `0.8334`
- **Partial Overlap F1 Score:** `0.9978`
- **Binary Token F1 Score:** `0.9995`
- **Inference Latency (Mean / Median / p95):** `0.46 ms` / `0.35 ms` / `0.96 ms`

### 3x3 Confusion Matrix (Tokens)

| Gold \ Pred | O | B-SKILL | I-SKILL |
| :--- | :--- | :--- | :--- |
| **O** | 6,690 | 0 | 5 |
| **B-SKILL** | 1 | 1,152 | 6 |
| **I-SKILL** | 0 | 3 | 4,827 |

## 2. Per-Trade Breakdown (10 Occupations)

| Code | Trade Name | Test Records | Exact Span Precision | Exact Span Recall | Exact Span F1 | Partial Overlap F1 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `TRD-01` | Tailor & Garment Worker | 55 | 0.8376 | 0.8522 | **0.8448** | 0.9914 |
| `TRD-02` | Electrician | 55 | 0.7807 | 0.7807 | **0.7807** | 1.0000 |
| `TRD-03` | Plumber | 55 | 0.8421 | 0.8421 | **0.8421** | 1.0000 |
| `TRD-04` | Motor Mechanic | 55 | 0.8145 | 0.8211 | **0.8178** | 0.9960 |
| `TRD-05` | Carpenter | 55 | 0.8512 | 0.8583 | **0.8548** | 0.9959 |
| `TRD-06` | Welder | 55 | 0.8468 | 0.8468 | **0.8468** | 1.0000 |
| `TRD-07` | Mason | 55 | 0.8475 | 0.8475 | **0.8475** | 1.0000 |
| `TRD-08` | Painter | 55 | 0.8190 | 0.8261 | **0.8225** | 0.9957 |
| `TRD-09` | Agriculture Worker | 55 | 0.8475 | 0.8475 | **0.8475** | 1.0000 |
| `TRD-10` | Mobile Repair Technician | 55 | 0.8288 | 0.8288 | **0.8288** | 1.0000 |

## 3. Per-Language Breakdown (5 Linguistic Modes)

| Language Mode | Script / Description | Test Records | Exact Precision | Exact Recall | Exact F1 | Partial F1 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `english` | english | 110 | 0.3983 | 0.4017 | **0.4000** | 0.9957 |
| `hindi` | hindi | 110 | 0.8831 | 0.8831 | **0.8831** | 1.0000 |
| `hinglish` | Hinglish Code-Switched | 110 | 0.9957 | 0.9957 | **0.9957** | 1.0000 |
| `mixed` | Mixed-Script (Devanagari + Latin) | 110 | 0.9336 | 0.9375 | **0.9356** | 0.9979 |
| `roman_hindi` | roman_hindi | 110 | 0.9432 | 0.9515 | **0.9474** | 0.9956 |

## 4. Per-Category Breakdown (8 Skill Taxonomy Dimensions)

| Skill Category | Gold Spans | True Positives | Precision | Recall | F1 Score |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `technical_tactile` | 290 | 239 | 0.9070 | 0.8241 | **0.8636** |
| `tool_operation` | 225 | 195 | 0.8884 | 0.8667 | **0.8774** |
| `quality_inspection` | 144 | 118 | 0.8281 | 0.8194 | **0.8237** |
| `troubleshooting_repair` | 152 | 129 | 0.8404 | 0.8487 | **0.8445** |
| `safety_compliance` | 149 | 120 | 0.8304 | 0.8054 | **0.8177** |
| `measurement_planning` | 87 | 69 | 0.7380 | 0.7931 | **0.7645** |
| `client_communication` | 41 | 36 | 0.5950 | 0.8780 | **0.7094** |
| `material_handling` | 71 | 62 | 0.7168 | 0.8732 | **0.7873** |
