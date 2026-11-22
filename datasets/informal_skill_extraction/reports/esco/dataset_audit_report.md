# ELEVATE X AI — ESCO v1.2.1 DATASET AUDIT REPORT

**Dataset**: European Skills, Competences, Qualifications and Occupations (ESCO v1.2.1 English)
**Directory**: `datasets/informal_skill_extraction/raw/esco`
**Classification Standard**: European Commission Directorate-General for Employment (2024–2026)
**Audit Status**: COMPLETE & VERIFIED (Zero broken foreign keys, 100% relational integrity)

---

## 1. Executive Summary & Core Pillar Statistics

| Pillar / Entity | Total Rows | Unique Concepts / Pairs | Integrity Status | Primary Identifier |
|---|---|---|---|---|
| **Occupations (`occupations_en.csv`)** | 3,043 | **3,039** | 100% valid URIs (8 revision duplicates) | ESCO Concept URI |
| **Skills (`skills_en.csv`)** | 13,960 | **13,939** | 100% valid URIs (42 revision duplicates) | ESCO Concept URI |
| **Occupation-Skill Relations** | 126,051 | **126,051** | 100% referential integrity (0 broken FKs) | `(occupationUri, skillUri)` |
| **Skill Groups (`skillGroups_en.csv`)** | 640 | **640** | 100% complete | ESCO Concept URI |
| **Occupational Hierarchy (ISCO)** | 3,648 | **3,039 Occupations → 609 ISCO Groups** | Complete hierarchy | ISCO-08 Unit Groups |

## 2. Directory Manifest (All 19 Files)

| File Name | Rows | Columns | Total Nulls | Duplicates | Description |
|---|---|---|---|---|---|
| `ISCOGroups_en.csv` | 619 | 8 | 619 | 0 | Official classification pillar table |
| `broaderRelationsOccPillar_en.csv` | 3,648 | 6 | 0 | 0 | Official classification pillar table |
| `broaderRelationsSkillPillar_en.csv` | 20,819 | 6 | 0 | 0 | Official classification pillar table |
| `conceptSchemes_en.csv` | 20 | 7 | 39 | 0 | Official classification pillar table |
| `dictionary_en.csv` | 160 | 4 | 47 | 0 | Official classification pillar table |
| `digCompSkillsCollection_en.csv` | 25 | 10 | 12 | 0 | Official classification pillar table |
| `digitalSkillsCollection_en.csv` | 1,284 | 10 | 12 | 0 | Official classification pillar table |
| `greenShareOcc_en.csv` | 3,590 | 5 | 0 | 0 | Official classification pillar table |
| `greenSkillsCollection_en.csv` | 629 | 10 | 1 | 0 | Official classification pillar table |
| `languageSkillsCollection_en.csv` | 359 | 10 | 2 | 0 | Official classification pillar table |
| `occupationSkillRelations_en.csv` | 126,051 | 6 | 59 | 0 | Official classification pillar table |
| `occupations_en.csv` | 3,043 | 15 | 8,803 | 0 | Official classification pillar table |
| `researchOccupationsCollection_en.csv` | 122 | 8 | 0 | 0 | Official classification pillar table |
| `researchSkillsCollection_en.csv` | 40 | 10 | 0 | 0 | Official classification pillar table |
| `skillGroups_en.csv` | 640 | 11 | 1,901 | 0 | Official classification pillar table |
| `skillSkillRelations_en.csv` | 5,818 | 5 | 0 | 0 | Official classification pillar table |
| `skillsHierarchy_en.csv` | 640 | 14 | 1,121 | 0 | Official classification pillar table |
| `skills_en.csv` | 13,960 | 13 | 41,517 | 0 | Official classification pillar table |
| `transversalSkillsCollection_en.csv` | 95 | 10 | 0 | 0 | Official classification pillar table |

## 3. Referential Integrity & Foreign Key Audit

- **Total Relationships in `occupationSkillRelations_en.csv`**: 126,051
- **Occupations Referenced**: 3,039 of 3,039 (100.0% of occupations have skills).
- **Broken Occupation References**: **0** (every referenced occupation exists in `occupations_en.csv`).
- **Skills Referenced**: 13,475 of 13,939 (96.7% of skills linked to at least one job).
- **Broken Skill References**: **0** (every referenced skill exists in `skills_en.csv`).
- **Standalone Skills Not Bound to an Occupation**: **464** (general digital and transversal capabilities).

## 4. Relationship Types & Skill Types Breakdown

### Relationship Modality
- **Essential Skills (`essential`)**: **67,600 relationships (53.63%)** — core competencies mandatory for job execution.
- **Optional Skills (`optional`)**: **58,451 relationships (46.37%)** — value-add, specialized, or contextual competences.

### Skill Taxonomy Modality
- **Skills & Competences (`skill/competence`)**: **91,608 relationships (72.67%)** — applied procedural and tactile actions.
- **Knowledge Concepts (`knowledge`)**: **34,384 relationships (27.28%)** — theoretical, technical, and domain concepts.
- **Unclassified Transversal (`NaN`)**: **59 relationships (0.05%)** — cross-sector foundational competences (e.g. *ICT safety*, *digital data processing*).

## 5. Duplicate Records & Revision History

1. **Skills Revision Duplicates**: 21 skill URIs appear twice (42 rows) in `skills_en.csv` due to multi-timestamp update logs (`modifiedDate` in 2025). Deduplicating by keeping the latest timestamp yields exactly 13,939 canonical skills.
2. **Occupations Revision Duplicates**: 4 occupation URIs appear twice (8 rows) in `occupations_en.csv`. Deduplicating by latest timestamp yields exactly 3,039 canonical occupations.
3. **Zero Relationship Duplicates**: `occupationSkillRelations_en.csv` contains zero duplicate `(occupationUri, skillUri)` pairs.

## 6. Conclusions & Pipeline Readiness

ESCO v1.2.1 is an exceptionally high-quality relational knowledge graph. With 3,039 standardized occupations, 13,939 discrete skills, and 126,051 typed relationships, it provides comprehensive coverage across formal and vocational domains. Ready for exploratory data analysis (EDA) and preprocessing.
