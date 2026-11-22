# ELEVATE X AI — FEATURE 1: INDIAN MOCK DATASET ANNOTATION QUALITY REPORT
**Dataset**: Indian Informal Worker Synthetic Mock Dataset (10 Trades)  
**Safety Classification**: **SYNTHETIC DEVELOPMENT DATA — NOT REAL-WORLD WORKER VALIDATION**  
**Deterministic Seed**: 42  
**Generated Date**: 2026-11-15  

---

## 1. Executive Summary & Quality Gates

| Metric | Target Standard | Achieved Value | Status |
| :--- | :--- | :--- | :--- |
| **Total Synthetic Records** | $\ge 5,000$ | **`5,200`** | **PASSED** |
| **Unique Descriptions** | $100\%$ | **`5,200` (100.0%)** | **PASSED** |
| **Occupations Covered** | Exactly 10 | **`10`** | **PASSED** |
| **Total Skill Spans** | $\ge 8,000$ | **`10,734`** | **PASSED** |
| **Avg Skills per Record** | $1.5 - 2.5$ | **`2.06`** | **PASSED** |
| **Unique Skill Phrases** | $\ge 150$ | **`499`** | **PASSED** |
| **Invalid Character Offsets** | Strict 0 | **`0`** | **PERFECT (100% Invariant)** |
| **Invalid BIO Transitions** | Strict 0 | **`0`** | **PERFECT (Valid Sequences)** |
| **Data Partition Integrity** | 80 / 10 / 10 Split | **Train: 4,150 \| Val: 500 \| Test: 550** | **LEAKAGE-FREE** |

---

## 2. Representation by Trade Domain (10 Occupations)

| Trade ID | Occupation Name | Total Records | Skill Spans | Spans / Record |
| :--- | :--- | :--- | :--- | :--- |
| **TRD-01** | Tailor and Garment Worker | `520` | `1,075` | `2.07` |
| **TRD-02** | Electrician | `520` | `1,068` | `2.05` |
| **TRD-03** | Plumber | `520` | `1,074` | `2.07` |
| **TRD-04** | Motor Mechanic | `520` | `1,074` | `2.07` |
| **TRD-05** | Carpenter | `520` | `1,076` | `2.07` |
| **TRD-06** | Welder | `520` | `1,071` | `2.06` |
| **TRD-07** | Mason | `520` | `1,077` | `2.07` |
| **TRD-08** | Painter | `520` | `1,072` | `2.06` |
| **TRD-09** | Construction Worker | `520` | `1,073` | `2.06` |
| **TRD-10** | Appliance Repair Technician | `520` | `1,074` | `2.07` |

## 3. Linguistic Diversity & Script Distribution

| Linguistic Mode | Script | Total Records | Percentage | Description |
| :--- | :--- | :--- | :--- | :--- |
| **Hindi** | `mixed` | `1,040` | `20.0%` | Native Devanagari script |
| **Roman_hindi** | `mixed` | `1,040` | `20.0%` | Romanized Hindi |
| **Hinglish** | `mixed` | `1,040` | `20.0%` | Code-switched Hinglish |
| **English** | `mixed` | `1,040` | `20.0%` | Technical English |
| **Mixed** | `mixed` | `1,040` | `20.0%` | Mixed Latin + Devanagari |

## 4. Functional Skill Category Distribution

| Functional Skill Category | Total Annotated Spans | Proportion | Supported Trades |
| :--- | :--- | :--- | :--- |
| **`technical_tactile`** | `2,743` | `25.6%` | All 10 trades |
| **`tool_operation`** | `2,087` | `19.4%` | All 10 trades |
| **`troubleshooting_repair`** | `1,421` | `13.2%` | All 10 trades |
| **`safety_compliance`** | `1,371` | `12.8%` | All 10 trades |
| **`quality_inspection`** | `1,306` | `12.2%` | All 10 trades |
| **`measurement_planning`** | `750` | `7.0%` | All 10 trades |
| **`material_handling`** | `716` | `6.7%` | All 10 trades |
| **`client_communication`** | `340` | `3.2%` | All 10 trades |

## 5. Provenance, Governance and Safety Gate Declaration

> [!IMPORTANT]
> **GOVERNANCE & DATASET NATURE DECLARATION**:
> 1. All records in this dataset are explicitly marked `is_synthetic: true` and `source_type: "synthetic_mock_development"`.
> 2. This dataset was constructed strictly for algorithmic architecture prototyping, model convergence benchmarking, and extended training stability validation.
> 3. **It does NOT represent genuine Indian worker field interview data.** Real-world field collection remains gated under verified consent protocols.
