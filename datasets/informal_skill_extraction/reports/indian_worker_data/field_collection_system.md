# ELEVATE X AI — FIELD DATA COLLECTION OPERATIONAL SYSTEM
## Practical Field Ingestion Protocol for Indian Informal Vocational Workers
### Designed for Face-to-Face Field Interviews in Bustling Workshops, Mandis, and Labor Nakas
### Compliance: Digital Personal Data Protection (DPDP) Act 2023 | Version 2.0 (November 2026)

---

## 1. System Architecture & Objective

The primary bottleneck in Indian vocational NLP is the absence of **authentic, unscripted field descriptions** spoken by uncredentialed workers. Formal syllabus documents from NCVET or DGT cannot substitute for how a real tailor, electrician, or motor mechanic speaks.

The Elevate X AI Field Collection System provides a standardized, end-to-end operational framework:

```
[Field Cluster Intercept] (e.g. Karol Bagh, Bhagirath Palace, Mayapuri)
                 │
                 ▼
[Informed Consent First] (DPDP Act 2023 Verbal / Signed Affirmation)
                 │
                 ▼
[Audio-Recorded Interview] (25 Questions across 15 Core Trade Topics)
                 │
                 ▼
[Verbatim Audio Transcription] (Preserving Hindi, Roman Hinglish, and Trade Slang)
                 │
                 ▼
[Automated Ingestion Tool] (field_collection_tool.py — Invariant Checking)
                 │
                 ▼
[Raw Data Partition] (raw/indian_worker_data/real/[batch_name].jsonl)
```

---

## 2. Ethical Protocol & DPDP Act 2023 Compliance

1. **Strict Purpose Limitation**:
   Data collected is strictly restricted to open academic, vocational recognition, and artificial intelligence skill extraction research. It will **never** be monetized, shared with credit bureaus, or used for law enforcement / tax surveillance.
2. **Voluntary Participation**:
   Workers may decline to answer any question or withdraw consent at any time without penalty.
3. **Absolute Anonymization & Data Minimization**:
   - **Zero Collection of Sensitive PII**: No Aadhaar numbers, PAN, bank accounts, residential addresses, or phone numbers are ever recorded.
   - Every participant is assigned a randomized pseudonym (e.g. `WRK-DEL-TLR-012`).
4. **Granular Audio & Photo Consent**:
   Audio recording and workplace photography require separate, optional affirmative checkboxes. If a worker declines audio recording, handwritten verbatim notes are taken.

---

## 3. Step-by-Step Field Interviewer Workflow

### Phase 1: Preparation & Approach
- Interviewers travel in pairs (one primary interviewer, one scribe/audio operator).
- Equip with:
  - Clipboards with printed consent forms (`consent_form_hindi.md`)
  - Printed trade question modules (`occupation_specific_collection_modules.md`)
  - Directional lavalier microphone with windshield to eliminate workshop noise
  - Digital audio recorder / mobile smartphone in airplane mode

### Phase 2: In-Person Interview Execution
- Greet the worker respectfully in Hindi / local dialect (*"Namaste Masterji / Mistriji"*).
- Read the consent terms clearly. Secure physical signature, thumbprint, or recorded verbal consent.
- Administer questions conversationally. Allow workers to explain tasks in their own words.
- Encourage workers to describe **at least 3 to 5 distinct tasks** (e.g., cutting, assembling, finishing, troubleshooting, and maintenance).

### Phase 3: Verbatim Transcription
- Transcribe audio word-for-word.
- Retain colloquial code-switching verbatim (*"Main single needle machine par pant shirt ki silai karta hu aur overlock se kinari band karta hu"*).
- Do not correct non-standard phonetic spellings or informal grammar.

### Phase 4: Ingestion & Validation
- Run the ingestion script:
  ```bash
  backend/.venv/bin/python datasets/informal_skill_extraction/scripts/indian_worker_data/field_collection_tool.py
  ```
- The tool programmatically verifies that all extracted skill spans match exact substring slices (`worker_description[start:end] == extracted_skill`).
- Validated records are appended to `raw/indian_worker_data/real/` and ready for double-blind human annotation.

