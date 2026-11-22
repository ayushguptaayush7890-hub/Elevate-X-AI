# ELEVATE X AI — DATA QUALITY & ETHICAL SOURCING REPORT
## Dataset 4: Indian Informal Worker Descriptions

**Status**: SPECIFICATION & COLLECTION ARCHITECTURE ESTABLISHED  
**Target Population**: Informal, uncredentialed vocational trade workers in India  
**Quality Gate**: ETHICAL SOURCING & TAXONOMY VALIDATION PASSED  

---

## 1. Ethical Sourcing & Ground Truth Integrity

### The Danger of Synthetic Data as Ground Truth
In natural language processing for informal labor markets, generating synthetic descriptions with LLMs (e.g., asking GPT or Claude to "write a plumber description") creates severe **synthetic hallucination bias**:
- LLMs generate idealized, grammatically sanitized text that does NOT match the colloquial vocabulary, trade slangs, or syntactic fragmentation used by real Indian workers on job sites.
- Synthetic data cannot serve as real-world benchmark evaluation data.

### Elevate X AI Integrity Rules
1. **Strict Provenance Labeling**: Every record in Dataset 4 carries an immutable `source_type` attribute (`real_field_interview`, `curriculum_adapted`, or `synthetic_test_stub`).
2. **Zero Fabrication**: No synthetic record may ever be marked as `real_field_interview`.
3. **Informed Consent**: All field interviews must be conducted with explicit worker consent for research and open AI skill benchmarking under DPDP (Digital Personal Data Protection) Act standards.
4. **Anonymization**: All personally identifiable information (worker full name, phone number, exact residential address) is sanitized into anonymized worker aliases (`WRK-CITY-ID`).

---

## 2. Linguistic & Code-Switching Quality Standards

Informal trade workers across India communicate in mixed phonetic scripts (Hinglish, Devanagari Hindi, and trade loanwords from English).

| Challenge | Pipeline Quality Solution |
|---|---|
| **Non-Standard Phonetic Spelling** (`silai` vs `seelai`, `chudi` vs `choori`) | Span boundaries are anchored strictly to **character offsets** (`start_offset`, `end_offset`) of the verbatim string; spelling is mapped to standardized `canonical_skill` without altering source text. |
| **Trade Loanwords** (`overlock`, `diverter`, `carburetor`, `conduit`) | Preserved in original spoken phonetic context; tagged with both technical category and ESCO/NSQF crosswalk. |
| **Colloquial Jargon** (`sahul`, `jhirri`, `fevicol lagana`, `regmar maarna`) | Annotated with `technical_tactile` or `tool_operation` category and mapped to formal vocational equivalents (e.g., *Plumb Bob Alignment*, *Wall Chasing*, *Laminate Adhesive Bonding*, *Surface Abrasive Sanding*). |

---

## 3. Four-Tier Quality Validation Checklist

| Quality Dimension | Standard / Test | Verification Metric |
|---|---|---|
| **Offset Precision** | `text[start:end] == extracted_skill` | 100% exact substring match required by validation script |
| **Schema Conformance** | JSON Schema draft-2020-12 validation | 100% records validate against `dataset_schema.json` |
| **Taxonomy Coverage** | 10 trades represented | Min 100 verified samples per trade in full collection |
| **Linguistic Balance** | Hindi, Hinglish, English representation | Min 30% Hinglish, 30% Hindi, 20% English in target corpus |
| **Inter-Annotator Agreement** | Cohen's Kappa $\ge 0.85$ on 20% double-blind sample | Disagreements adjudicated by senior ITI master instructor |
| **Crosswalk Validation** | Valid ESCO URI and O*NET SOC code | Zero broken or hallucinated URI identifiers |

---

## 4. Crosswalk Alignment Architecture

```
[Verbatim Worker Utterance (Hinglish/Hindi)]
                  │
                  ▼
       [Extracted Vernacular Span]
   ("jhirri kaat kar PVC conduit daalta hu")
                  │
                  ▼
        [Canonical Trade Skill]
   ("Concealed Electrical Conduit Installation")
                  │
    ┌─────────────┼─────────────┐
    ▼             ▼             ▼
[NSDC / NCVET] [ESCO v1.2.1] [O*NET-SOC]
 ELE/Q3104:NOS-102  esco/skill/...  47-2111.00
 (Level 4 QP)     (Install cables) (Electricians)
```

By connecting vernacular trade utterances directly to **NCVET / NSDC QPs**, **ESCO v1.2.1**, and **O*NET**, Elevate X AI enables uncredentialed Indian trade workers to achieve formal credential portability, trade matching, and global recognition.

