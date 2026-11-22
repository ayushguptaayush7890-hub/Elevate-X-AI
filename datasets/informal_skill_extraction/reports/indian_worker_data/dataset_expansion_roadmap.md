# ELEVATE X AI — THREE-STAGE DATASET EXPANSION ROADMAP
## Operational Strategy for Dataset 4: Indian Informal Worker Skill Extraction
### Target Horizons: Pilot (100–200) ➔ Main Corpus (1,000–2,000) ➔ Advanced (5,000+)
### Status: Infrastructure Complete | Real Field Collection Launching

---

## 1. Overview & Core Guiding Principles

Elevate X AI seeks to transform informal work experience into recognized national (NSQF) and international (ESCO, O*NET) skill credentials. Because informal workers communicate in mixed Devanagari Hindi, phonetic Roman Hinglish, and specialized workshop loanwords, the dataset must reflect **authentic, unfiltered field narratives**.

```
┌────────────────────────────────────────────────────────┐
│ Stage 1: Initial Pilot (Weeks 1–4)                     │
│ Target: 100–200 Genuine Field Transcripts              │
│ Quota: 10–20 workers per occupation across 10 trades   │
│ Focus: Protocol validation, double-annotation baseline │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│ Stage 2: Main Production Corpus (Months 2–4)           │
│ Target: 1,000–2,000 Genuine Field Transcripts          │
│ Quota: 100–200 workers per occupation across 10 trades │
│ Focus: High linguistic diversity, regional dialects    │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│ Stage 3: Advanced National Scale (Months 5–9)          │
│ Target: 5,000+ Genuine Field Transcripts               │
│ Quota: 500+ workers per occupation, 8+ Indian states   │
│ Focus: Rare diagnostic skills, edge cases, cross-trade │
└────────────────────────────────────────────────────────┘
```

> [!IMPORTANT]
> **Deficit Transparency**: At present, **0 genuine worker records exist** in the repository. The figures above are **operational collection targets**, not existing data counts. No model will be trained until Stage 1 passes all quality gates.

---

## 2. Stage Breakdown & Operational Milestones

### Stage 1: Initial Pilot (Target: 100–200 Genuine Descriptions)
- **Primary Objective**: Validate field intercept logistics, audio-to-text accuracy, and double-annotator consensus.
- **Occupational Allocation**: 10 to 20 genuine workers per trade across all 10 occupations.
  - Priority Pilot Launch: **Tailor & Garment Worker** (10–20 workers in Karol Bagh and Gandhi Nagar, Delhi).
- **Quality Gates to Clear**:
  1. 100% verified DPDP Act consent (signed form or verbal audio confirmation).
  2. Character offset exactness: $\text{worker\_description}[\text{start}:\text{end}] == \text{extracted\_skill}$ for every span.
  3. Inter-annotator agreement: Span-level strict F1 $\ge 0.88$ and category Cohen's $\kappa \ge 0.85$ on a 20% double-annotated subset.
  4. Zero data contamination: Synthetic stubs kept strictly isolated.

### Stage 2: Main Production Dataset (Target: 1,000–2,000 Genuine Descriptions)
- **Primary Objective**: Build a robust, statistically diverse training and evaluation corpus.
- **Occupational Allocation**: 100 to 200 descriptions per occupation.
- **Depth Requirement**: Each interview will capture 3–5 distinct task descriptions per worker (e.g., cutting, assembling, finishing, troubleshooting, and tool maintenance).
- **Linguistic Distribution Target**:
  - 40% Devanagari Hindi (formal & vernacular)
  - 45% Romanized Hinglish (colloquial code-switching)
  - 10% Trade English loanword-rich descriptions
  - 5% Multilingual / regional trade expressions
- **Worker Experience Stratification**:
  - 25% Early Career / Former Apprentices (1–3 years experience)
  - 50% Independent Tradespersons (4–10 years experience)
  - 25% Master Craftsmen / Workshop Ustadjis (10+ years experience)

### Stage 3: Advanced Expansion (Target: 5,000+ Genuine Descriptions)
- **Primary Objective**: Cover rare diagnostic edge cases, diverse state dialects, and complex multi-trade practices.
- **Geographic Representation**:
  - North: Delhi NCR, Uttar Pradesh (Kanpur, Agra, Varanasi), Haryana (Faridabad, Panipat), Punjab (Ludhiana)
  - West: Rajasthan (Jaipur, Jodhpur), Gujarat (Surat, Ahmedabad), Maharashtra (Mumbai, Pune)
  - Central: Madhya Pradesh (Bhopal, Indore), Bihar (Patna)
- **Focus Areas**: Complex troubleshooting narratives, safety near-misses, client negotiation idioms, and traditional unmapped craft competencies (*is_unmapped_skill*).

---

## 3. Worker-Level Split Governance (Leakage Prevention)

To guarantee true generalization, dataset partitioning for future experiments must enforce **strict worker-level isolation**:

$$\text{Worker } w_i \in \text{Train} \implies w_i \notin \text{Validation} \land w_i \notin \text{Test}$$

- **The Multi-Sentence Leakage Hazard**: A single tailor may provide 5 different task descriptions. If 4 are placed in the training set and 1 in the test set, the model may memorize the worker's idiosyncratic vocabulary and syntax, yielding artificially inflated evaluation metrics.
- **Protocol**: Train (70%), Validation (15%), and Test (15%) splits will be partitioned strictly by `worker_id` hashes, ensuring test evaluations measure performance on entirely unseen individuals.

---

## 4. Collection Timeline & Key Milestones

| Timeline | Phase | Deliverables | Governance Checkpoint |
|---|---|---|---|
| **Month 1** | Pilot Field Interviews | 10–20 Tailor interviews + 10 Electrician interviews | DPDP consent verification & offset audit |
| **Month 2** | Pilot Completion | 100–200 descriptions across all 10 trades | Inter-annotator agreement evaluation ($\kappa \ge 0.85$) |
| **Month 3** | Main Scaling | 500 descriptions ingested and validated | Mid-scale vocabulary and script balance audit |
| **Month 4** | Main Dataset Sign-off | 1,000–2,000 descriptions validated | Supervised training readiness gate evaluation |
| **Months 5–9** | National Multi-State Expansion | 5,000+ descriptions across 8 states | National RPL portability benchmark release |

