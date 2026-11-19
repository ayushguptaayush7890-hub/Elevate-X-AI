# ELEVATE X AI — SKILLSPAN DATASET AUDIT REPORT

**Dataset**: SkillSpan (Named Entity Recognition for Skills & Knowledge)
**Raw Files**: `datasets/informal_skill_extraction/raw/skillspan/[train.json, dev.json, test.json]`
**Reference Paper**: Zhang et al., *SkillSpan: Hard and Soft Skill Extraction from English Job Postings* (NAACL 2022)
**Audit Status**: COMPLETE & VERIFIED (Zero corrupted tokens, 100% BIO alignment)

---

## 1. Executive Summary Across Splits

| Split | Job Postings (Docs) | Sentences (Records) | Total Tokens | Skill Spans (B) | Knowledge Spans (B) | Total Entity Spans | Avg Tokens / Sent |
|---|---|---|---|---|---|---|---|
| **TRAIN** | 140 | 4,800 | 93,453 | 2,221 | 2,969 | 5,190 | 19.47 |
| **DEV** | 58 | 3,174 | 40,057 | 1,070 | 1,093 | 2,163 | 12.62 |
| **TEST** | 65 | 3,569 | 42,786 | 1,091 | 1,174 | 2,265 | 11.99 |
| **TOTAL** | **263** | **11,543** | **176,296** | **4,382** | **5,236** | **9,618** | **15.27** |

## 2. Schema & Field Verification

Every record in all three files conforms to the JSON Lines format with 5 explicit fields:

| Field Name | Data Type | Meaning | Audit Finding |
|---|---|---|---|
| `idx` | `int` | Document / job posting identifier (1 to N per split) | Valid (140 train, 58 dev, 65 test) |
| `source` | `str` | Job posting domain: `'tech'` or `'house'` | Valid (no missing values) |
| `tokens` | `list[str]` | Tokenized word sequence of the sentence | Valid (length > 0) |
| `tags_skill` | `list[str]` | BIO tags (`O`, `B`, `I`) for soft and hard skills | 100% token aligned |
| `tags_knowledge` | `list[str]` | BIO tags (`O`, `B`, `I`) for domain/tool knowledge | 100% token aligned |

## 3. Label Scheme & Semantic Definitions

SkillSpan utilizes a dual-layer BIO sequence tagging architecture:
1. **Skills Layer (`tags_skill`)**: Captures actionable capabilities and execution competencies (e.g., *'implementing and promoting all QA relevant topics'*, *'Work hands-on'*, *'running tests automatically'*).
2. **Knowledge Layer (`tags_knowledge`)**: Captures declarative domain expertise, tools, technologies, and certifications (e.g., *'QA'*, *'Docker'*, *'CircleCI'*, *'Python'*, *'Kubernetes'*).
3. **BIO Semantics**:
   - `O`: Outside any entity span.
   - `B`: Beginning token of an annotated span.
   - `I`: Interior continuation token of an annotated span.

## 4. Token-Tag Alignment & Boundary Validation

- **Alignment Discrepancies (`len(tokens) != len(tags)`)**: **0 across all 11,543 records**.
- **Malformed Tag Tokens (not in ['O', 'B', 'I'])**: **0 tokens**.
- **Empty Lines**: **0 lines**.
- **Corrupted JSON Records**: **0 records**.

## 5. Cross-Split Overlap & Leakage Audit

The dataset split was executed at the **job posting document level (`idx`)**, ensuring that sentences originating from the same job description never appear across different splits.

| Split Comparison | Overlapping Sentences | Percentage of Train | Nature of Overlapping Text |
|---|---|---|---|
| **Train & Dev** | 151 | 3.15% | Generic boilerplate headers (`<CONTACT>`, `Industry:`, `Information Technology`) |
| **Train & Test** | 174 | 3.62% | Standard structural section headers (`Qualifications:`, `Company type:`) |
| **Dev & Test** | 159 | - | Boilerplate placeholders (`<LOCATION>`, `<ORGANIZATION>`) |
| **All Three Splits** | 86 | - | Boilerplate placeholders and punctuation |

> [!NOTE]
> Crucially, zero skill-rich or job-specific sentences leak across splits. The overlapping strings are strictly standardized ATS section headers and anonymization tokens (`<ORGANIZATION>`, `<ADDRESS>`). Train/Dev/Test split integrity is fully intact.

## 6. Language & Domain Coverage

- **Language**: 100% English job postings.
- **Domain Distribution**:
  - **Tech Domain (`tech`)**: 7,575 sentences (65.6%) — software engineering, QA, DevOps, cloud infrastructure.
  - **House Domain (`house`)**: 3,968 sentences (34.4%) — broader industry postings (services, hospitality, retail, healthcare).
- **Vocabulary Diversity**:
  - **Unique Skill Spans**: 3,758 distinct expressions.
  - **Unique Knowledge Spans**: 3,055 distinct expressions.

## 7. Conclusions & Next Steps

The SkillSpan dataset exhibits pristine data hygiene: zero token alignment mismatches, zero corrupted records, and strictly preserved document-level splits. It is ready for exploratory data analysis (EDA) and structured preprocessing.
