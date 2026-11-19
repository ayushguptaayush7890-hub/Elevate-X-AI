# ELEVATE X AI — FIELD DATA COLLECTION & SAMPLING PLAN
## Operational Strategy for Dataset 4: Indian Informal Worker Skill Extraction
### Version 1.0 (November 2026) | Elevate X AI Vocational Data Pipeline

---

## 1. Executive Summary & Phased Strategy

The informal vocational workforce in India accounts for over 85% of total employment. These workers possess deep tactile, procedural, and diagnostic skills acquired through years of uncredentialed practice. 

To bridge this experiential knowledge with formal national (NSQF) and international (ESCO, O*NET) skill frameworks, Elevate X AI establishes a **two-phased field data collection plan**:

```
┌────────────────────────────────────────────────────────┐
│ Phase 1: Pilot Collection (Tailoring Trade)            │
│ Target: 10–20 Genuine Field Interviews & Transcripts   │
│ Focus: Verify audio-to-text pipeline, multi-span       │
│        annotation schema, and DPDP consent protocols.  │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│ Phase 2: Full Multi-Trade Expansion (10 Occupations)   │
│ Target: 50–100 Genuine Field Interviews per Trade      │
│ Total Corpus Target: 500–1,000 Genuine Descriptions    │
│ Focus: High linguistic diversity (Hindi, Hinglish,      │
│        Devanagari, Romanized trade slang).             │
└────────────────────────────────────────────────────────┘
```

> [!IMPORTANT]
> **Strict Provenance Rule**: The figures above are **operational collection targets**, NOT completed dataset counts. Elevate X AI strictly prohibits generating synthetic text or hallucinating worker responses to artificially reach these targets.

---

## 2. Quantitative Targets by Trade

| Trade ID | Trade Domain | Pilot Target | Expansion Target | Geographic Field Cluster |
|---|---|---|---|---|
| `TRD-01` | Tailor and Garment Worker | **10–20** | **50–100** | Karol Bagh, Gandhi Nagar, Chandni Chowk (Delhi) |
| `TRD-02` | Electrician | — | **50–100** | Bhagirath Palace, residential market associations |
| `TRD-03` | Plumber | — | **50–100** | Chawri Bazar sanitary market, local labour nakas |
| `TRD-04` | Motor Mechanic | — | **50–100** | Mayapuri automotive cluster, Kashmiri Gate |
| `TRD-05` | Carpenter | — | **50–100** | Kirti Nagar timber & furniture market |
| `TRD-06` | Welder | — | **50–100** | Okhla & Anand Parbat industrial areas |
| `TRD-07` | Mason / Raj Mistri | — | **50–100** | Construction labor chowks (Noida, Ghaziabad, Gurgaon) |
| `TRD-08` | Painter | — | **50–100** | Hardware paint stores, residential labor corners |
| `TRD-09` | Agriculture & Irrigation | — | **50–100** | Sonipat, Meerut peri-urban agrarian clusters |
| `TRD-10` | Mobile Repair Tech | — | **50–100** | Gaffar Market (Karol Bagh), Nehru Place |
| **Total** | **All 10 Occupations** | **10–20** | **500–1,000** | **National Multi-Cluster Representation** |

---

## 3. Field Collection Protocol & Interviewer Guidelines

### A. Location & Sampling Strategy
1. **Cluster Intercepts**: Conduct in-person visits to vocational markets, service shops, and labor nakas.
2. **Diversity of Experience**:
   - 30% Early Career (1–3 years experience / former apprentices).
   - 40% Mid-Career (4–10 years experience / independent shopkeepers).
   - 30% Master Craftsmen (10+ years experience / *ustads* / *masterjis*).
3. **Gender Inclusivity**: Active outreach to women tailoring micro-entrepreneurs and home-based garment workers.

### B. Field Interview Workflow
1. **Introduction & Rapport**: Introduce Elevate X AI as a non-profit/research initiative aimed at skill recognition.
2. **Informed Consent**: Read `consent_form_hindi.md` in the worker's spoken dialect. Secure physical signature, thumbprint, or recorded audio affirmative consent.
3. **Audio Capture**: Record using high-definition mobile recorder with directional lavalier microphone to minimize ambient workshop noise.
4. **Semi-Structured Probing**: Administer questions from `interview_questionnaire_hindi.md` and the trade-specific module (`trade_specific_questionnaires.md`).

---

## 4. Transcription & Data Ingestion Pipeline

1. **Verbatim Audio Transcription**:
   - Transcribe strictly what the worker says without grammatical sanitization or literary correction.
   - Retain code-switching verbatim (e.g., *"Single needle machine par naap ke hisaab se suit kaat kar overlock karta hu"*).
2. **Script Partitioning**:
   - If transcribed in Devanagari Hindi: `original_language = "hindi"`, `script_type = "devanagari"`.
   - If transcribed in Romanized Hinglish: `original_language = "hinglish"`, `script_type = "latin"`.
   - If mixed scripts: `script_type = "mixed"`.
3. **File Ingestion Storage**:
   - Store raw audio archives in secure, air-gapped encrypted cold storage (`data/audio_archive/`).
   - Ingest transcribed JSONL records into `datasets/informal_skill_extraction/raw/indian_worker_data/real/`.
   - Tag all verified real records with:
     ```json
     "source_type": "real_field_interview",
     "source_reference": "batch_pilot_tailor_delhi_nov2026",
     "consent_status": "confirmed_dpdp_audio"
     ```

---

## 5. Quality Gates for Transition from Pilot to Full Expansion

Before deploying field enumerators for the 500–1,000 expansion phase, the Pilot Tailor batch must clear four gates:

1. **Gate 1 (Transcription Integrity)**: Zero word insertions, zero grammatical polishing.
2. **Gate 2 (Offset Exactness)**: 100% exact substring match across all annotated spans.
3. **Gate 3 (Double-Blind Agreement)**: Cohen's $\kappa \ge 0.85$ and span F1 $\ge 0.88$ on a 20% double-annotated pilot subset.
4. **Gate 4 (Privacy Audit)**: 100% compliance with DPDP consent confirmation and total scrub of PII.

