# ELEVATE X AI — ESCO v1.2.1 PREPROCESSING REPORT

**Classification**: European Skills, Competences, Qualifications and Occupations (v1.2.1)
**Outputs Directory**: `datasets/informal_skill_extraction/processed/esco`
**Primary Relational Edge Count**: 126,051 occupation-skill relationships

---

## 1. Transformations Applied

1. **Header Normalization**: Transformed camelCase properties (`conceptUri`, `iscoGroup`, `preferredLabel`, etc.) to clean `snake_case` across all tables.
2. **Revision Deduplication**:
   - `occupations_en.csv`: 8 rows with dual revision dates consolidated to 3,039 canonical concepts (sorted by `modified_date` desc).
   - `skills_en.csv`: 42 rows with dual revision dates consolidated to 13,939 canonical concepts.
3. **UUID Key Derivation**: Extracted canonical 36-character hexadecimal UUIDs (`occupation_id`, `skill_id`) from URI paths for seamless indexing in relational databases and search engines.
4. **Vocational Craft Segmentation**: Tagged all occupations in ISCO-08 Major Groups 7 (Crafts), 8 (Machine Operators), and 9 (Elementary Labor) with `is_vocational_craft = True` (817 trade occupations).
5. **Rich Mapping Enrichment**: Enriched `esco_occupation_skill_mapping.csv` with boolean flags (`is_essential`, `is_vocational_craft`) and hierarchical ISCO unit codes.

## 2. Processed Table Summary

| Processed Output File | Records | Features | Primary Key / Identifier | Purpose |
|---|---|---|---|---|
| `esco_occupations_cleaned.csv` | 3,039 | 22 | `concept_uri` / `occupation_id` | Standardized occupation catalog |
| `esco_skills_cleaned.csv` | 13,939 | 17 | `concept_uri` / `skill_id` | Granular skill & competence catalog |
| `esco_occupation_skill_mapping.csv` | 126,051 | 11 | `(occupation_uri, skill_uri)` | Complete occupational skill requirements graph |
| `esco_skill_groups.csv` | 640 | 13 | `concept_uri` / `group_id` | Competency cluster hierarchy |

