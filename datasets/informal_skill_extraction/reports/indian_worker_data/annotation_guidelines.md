# ELEVATE X AI — HUMAN ANNOTATION GUIDELINES & PROTOCOL
## Dataset 4: Indian Informal Worker Descriptions to Standardized Skill Spans
### Version 2.0 (November 2026) | Multi-Span Competency Tagging Architecture

---

## 1. Objective of the Annotation Task

The objective of Dataset 4 is to build an evaluation and training corpus that maps how **real informal workers in India** verbally describe their trade experience (in Hindi, Hinglish, or English trade vernacular) into **verifiable, multi-span trade competencies**.

Informal workers naturally combine multiple technical capabilities, tool operations, and diagnostic routines within a single sentence:
> *"Main single needle machine par pant shirt ki silai karta hu aur overlock se kinari band karta hu."*

In this single sentence, two distinct capabilities must be annotated:
1. `single needle machine par pant shirt ki silai karta hu` (Category: `tool_operation` / `technical_tactile`)
2. `overlock se kinari band karta hu` (Category: `technical_tactile` / `quality_inspection`)

---

## 2. Multi-Span Character Offset Rules

Annotators must adhere to strict zero-indexed, half-open interval character offsets:

1. **Exact 0-Indexed Character Offsets**:
   - `start_offset`: 0-indexed position of the first character in the span.
   - `end_offset`: 0-indexed position immediately following the last character in the span.
   - **Verification Invariant**: In Python, `worker_description[start_offset:end_offset] == extracted_skill` must evaluate to `True`.
2. **Punctuation Stripping**:
   - Do NOT include trailing commas, periods (पूर्णविराम), semicolons, or quotes unless syntactically part of a compound trade term.
3. **No Semantic Normalization of Verbatim Text**:
   - Never correct spelling mistakes or grammatical irregularities inside `worker_description` or `extracted_skill`.
   - Preserve verbatim spoken terms (`silai`, `fevicol`, `jhirri`, `sahul`, `multimeter`).
   - The standardized, professional English nomenclature belongs exclusively in the `canonical_skill` field.

---

## 3. Functional Skill Categories

| Category | Definition | Indian Trade Example |
|---|---|---|
| `technical_tactile` | Hands-on physical craft execution, assembly, or manual fabrication | `bricklaying in cement mortar`, `sooth dekhkar deewar seedhi karna`, `chudi kaatna` |
| `tool_operation` | Safe, competent operation of trade machinery or power equipment | `operating single needle lockstitch machine`, `circular saw chalana`, `SMD rework station chalana` |
| `troubleshooting_repair` | Diagnosing electrical/mechanical faults, tracing leaks, or circuit testing | `multimeter se neutral-phase check karna`, `shorting nikalna DC supply se`, `brake oil bleed karna` |
| `quality_inspection` | Checking dimensions, surface flatness, seam strength, or tolerances | `seam tension check karna`, `spirit level se slope dekhna`, `feeler gauge se tappet napna` |
| `safety_compliance` | Handling earthing, PPE, ventilation, circuit breakers, or gas shutoff | `welding shield aur leather gloves pehanna`, `MCB isolation check`, `earthing pit check karna` |
| `measurement_planning` | Taking body measurements, reading marking chalk, or layout planning | `customer ka naap lena`, `pattern marking karna bakram par`, `water tube level nikalna` |
| `client_communication` | Discussing customer requirements, pricing, or defect complaints | `customer ko fitting trial karwana`, `alteration samajhna`, `customer ko quotation batana` |
| `material_handling` | Preparing, batching, preserving, or handling raw substrates | `masala banana (1:4 cement-sand)`, `sunmica par fevicol lagana`, `pipe solvent cementing` |

---

## 4. Standardized Workflow & Annotation Statuses

Every record transitions through a strictly governed lifecycle:

```
[Unannotated Transcript] ──► pending
                               │
                               ▼
[Primary Annotator]       ──► annotated
                               │
                               ▼
[Blind Secondary Check]   ──► reviewed
                               │
            ┌──────────────────┴──────────────────┐
            ▼                                     ▼
     [Consensus Reached]                 [Discrepancy / Split]
            │                                     │
            ▼                                     ▼
        approved                      flagged_for_adjudication
                                                  │
                                                  ▼
                                      [Lead Vocational Expert]
                                                  │
                                                  ▼
                                         adjudicated / approved
```

- `pending`: Newly ingested verbatim transcript awaiting primary annotation.
- `annotated`: Primary annotator has tagged all skill spans, offsets, categories, and canonical names.
- `reviewed`: Secondary reviewer has verified span boundaries, category tags, and crosswalk IDs.
- `flagged_for_adjudication`: Boundary overlap discrepancy or ambiguous trade idiom detected between annotators.
- `approved`: Formally validated record passing all automated validation checks and quality gates.
- `rejected`: Record rejected due to corrupted transcript, inaudible recording, or missing consent.

---

## 5. Three-Way Crosswalk Mapping Methodology

For every tagged `skill_span`, the annotator must link the informal phrase to standardized taxonomies:

1. **`canonical_skill`**: Concise, standardized title in English (e.g. *Single-Needle Lockstitch Operation*).
2. **`nsqf_reference`**: Reference the official Qualification Pack / National Occupational Standard code from `occupation_taxonomy.csv` (e.g. `AMH/Q1947:NOS-101`).
3. **`esco_uri`**: Concept URI from ESCO v1.2.1 Skills Pillar (e.g. `http://data.europa.eu/esco/skill/08d51185-...`).
4. **`onet_soc_code`**: Associated O*NET occupation code (e.g. `51-6052.00`).
5. **`is_unmapped_skill`**: Set to `true` if the competence is a unique indigenous practice lacking an exact international ontology match (e.g., traditional lime *ghoontai* plastering).

---

## 6. Inter-Annotator Agreement & Mathematical Evaluation

To ensure annotation consistency across linguistically diverse Hindi and Hinglish transcripts, **at least 20% of all field records are independently annotated by two blind annotators**.

### A. Cohen's Kappa Formula
For discrete categorical classification (e.g., evaluating whether Annotator 1 and Annotator 2 assigned the same `skill_category` to an agreed span):

$$\kappa = \frac{P_o - P_e}{1 - P_e}$$

Where:
- $P_o$ is the observed proportionate agreement between the two annotators:
  $$P_o = \frac{\sum_{i=1}^k C_{ii}}{N}$$
- $P_e$ is the hypothetical probability of chance agreement:
  $$P_e = \sum_{i=1}^k \left( \frac{R_i}{N} \times \frac{C_i}{N} \right)$$
  with $R_i$ and $C_i$ denoting row and column marginal totals across $k$ categories for $N$ evaluated spans.

### B. Limitations of Cohen's Kappa for Span-Level Extraction
While Cohen's Kappa is theoretically sound for discrete class labels, it has major limitations when applied to **character-level span boundary extraction**:
1. **The Negative Space Paradox**: In continuous natural language text, the vast majority of characters or tokens are *non-skills* (the "O" tag in BIO schemes). Because $P_e$ is heavily dominated by the high volume of non-skill tokens, $\kappa$ can appear spuriously high even when boundary agreement on actual skill spans is poor.
2. **Arbitrary Boundary Sensitivity**: If Annotator 1 selects `"single needle machine par silai"` (offsets 0–31) and Annotator 2 selects `"single needle machine par pant shirt ki silai"` (offsets 0–42), token-level Kappa treats the overlapping tokens as agreements and the trailing tokens as partial disagreements, failing to evaluate whether the extracted concept is functionally equivalent.

### C. Elevate X AI Dual Agreement Standard
To overcome these limitations, the pipeline evaluates agreement on two complementary levels:
1. **Span-Level Strict F1 Score**:
   A skill span is counted as a true positive if and only if both the character offsets match exactly and the `skill_category` matches. Target: **Span F1 $\ge 0.88$**.
2. **Token-Level Cohen's Kappa**:
   Calculated across all trade-relevant clauses to measure category labeling consistency. Target: **$\kappa \ge 0.85$**.

Any span where $\text{Intersection-over-Union (IoU)} < 1.0$ or category disagreement exists is automatically routed to `flagged_for_adjudication`.
