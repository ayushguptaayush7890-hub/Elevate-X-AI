# ELEVATE X AI — UPDATED FIELD DATA COLLECTION MASTER PLAN
## Comprehensive Multi-Stage Expansion Plan across 10 Indian Vocational Occupations
### Target Allocation: Pilot (100–200) | Main Corpus (1,000–2,000) | Advanced National Scale (5,000+)
### Version 2.0 (November 2026) | Elevate X AI Strategic Roadmap

---

## 1. Executive Summary

This master plan updates and supersedes all preliminary collection documentation. It defines operational quotas, geographic recruitment clusters, enumerator staffing, and verification milestones to build India's premier informal vocational NLP dataset.

```
┌────────────────────────────────────────────────────────┐
│ Phase 1: Pilot Collection (100–200 Descriptions)       │
│ Priority: 10–20 workers per trade across 10 trades     │
│ Timeline: Weeks 1–4 | Geographic Focus: Delhi NCR      │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│ Phase 2: Main Production Dataset (1,000–2,000 Records) │
│ Priority: 100–200 workers per trade across 10 trades   │
│ Timeline: Months 2–4 | Focus: UP, Haryana, Rajasthan   │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│ Phase 3: Advanced National Scale (5,000+ Records)      │
│ Priority: 500+ workers per trade, 8 Indian States      │
│ Timeline: Months 5–9 | Focus: Multi-state dialects     │
└────────────────────────────────────────────────────────┘
```

> [!IMPORTANT]
> **Zero Fabrication Reminder**: The figures above are **operational collection targets**, not existing data counts. At present, **0 genuine worker records exist** in the repository.

---

## 2. Occupational Allocation & Field Deployment Targets

| ID | Trade Occupation | Pilot Target | Main Target | Advanced Target | Primary Field Intercept Locations |
|---|---|---:|---:|---:|---|
| `TRD-01` | Tailor and Garment Worker | 10–20 | 100–200 | 500+ | Karol Bagh, Gandhi Nagar, Chandni Chowk (Delhi) |
| `TRD-02` | Electrician | 10–20 | 100–200 | 500+ | Bhagirath Palace, residential market associations |
| `TRD-03` | Plumber | 10–20 | 100–200 | 500+ | Chawri Bazar sanitary market, local labour nakas |
| `TRD-04` | Motor Mechanic | 10–20 | 100–200 | 500+ | Mayapuri automotive cluster, Kashmiri Gate |
| `TRD-05` | Carpenter | 10–20 | 100–200 | 500+ | Kirti Nagar timber & furniture market |
| `TRD-06` | Welder | 10–20 | 100–200 | 500+ | Okhla & Anand Parbat industrial fabrication clusters |
| `TRD-07` | Mason / Raj Mistri | 10–20 | 100–200 | 500+ | Early morning labor chowks (Noida, Ghaziabad, Gurgaon) |
| `TRD-08` | Painter | 10–20 | 100–200 | 500+ | Local paint retail shops, residential labor nakas |
| `TRD-09` | Agriculture and Irrigation Worker | 10–20 | 100–200 | 500+ | Sonipat, Meerut, Karnal peri-urban farming clusters |
| `TRD-10` | Mobile Repair Technician | 10–20 | 100–200 | 500+ | Gaffar Market (Karol Bagh), Nehru Place hardware hub |
| **Total**| **All 10 Vocational Trades** | **100–200** | **1,000–2,000** | **5,000+** | **National Multi-Cluster Representation** |

---

## 3. Enumerator Staffing & Quality Governance

1. **Enumerator Recruitment**: Field enumerators must be bilingual in Hindi and trade English, and possess familiarity with local artisan terminology.
2. **Double-Annotation Protocol**: At least 20% of transcripts in every batch will be blindly double-annotated by two independent vocational analysts.
3. **Thresholds for Advancement**:
   - Token-level Cohen's $\kappa \ge 0.85$
   - Strict Span $F_1 \ge 0.88$
   - Character offset exactness: 100%
   - Consent documentation: 100%
4. **Worker-Level Isolation**: Splitting for future training will partition strictly on `worker_id` to eliminate multi-utterance leakage.

