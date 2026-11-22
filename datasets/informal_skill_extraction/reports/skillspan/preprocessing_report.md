# ELEVATE X AI — SKILLSPAN PREPROCESSING REPORT

**Dataset**: SkillSpan (Hard/Soft Skill and Knowledge Sequence Labeling)
**Outputs**: `datasets/informal_skill_extraction/processed/skillspan/[cleaned_train.json, cleaned_dev.json, cleaned_test.json]`
**Vocabulary**: `datasets/informal_skill_extraction/processed/skillspan/skill_vocabulary.json`
**Statistics**: `datasets/informal_skill_extraction/processed/skillspan/annotation_statistics.csv`

---

## 1. Cleaning Actions & Standardization Rules

1. **Whitespace Normalization**: Stripped extraneous whitespace from individual token strings while preserving intra-word hyphenation and symbols.
2. **Token-to-Tag Boundary Validation**: Enforced `len(tokens) == len(tags_skill) == len(tags_knowledge)` for all 11,543 records. Zero mismatches encountered.
3. **Preservation of BIO Label Semantics**: Unaltered preservation of `O`, `B`, and `I` tagging layers for both Skill and Knowledge dimensions.
4. **Span Entity Extraction**: Precomputed multi-token entity intervals with token start/end indices, token counts, and plain-text phrases.
5. **Document & Split Partition Preservation**: Maintained exact train, dev, and test split memberships without cross-split leakage.

## 2. Processed Annotation Statistics

| Split | Sentence Count | Total Tokens | Skill Spans | Knowledge Spans | Total Spans | Entity Density (/100 tok) | Entity Sentences (%) |
|---|---|---|---|---|---|---|---|
| **TRAIN** | 4,800 | 93,453 | 2,221 | 2,969 | 5,190 | 5.55 | 33.00% |
| **DEV** | 3,174 | 40,057 | 1,070 | 1,093 | 2,163 | 5.40 | 28.80% |
| **TEST** | 3,569 | 42,786 | 1,091 | 1,174 | 2,265 | 5.29 | 27.29% |
| **TOTAL** | 11,543 | 176,296 | 4,382 | 5,236 | 9,618 | 5.46 | 30.08% |

## 3. Top Action Skills in Vocabulary

| Rank | Skill Phrase | Frequency | Token Length | Observed Splits |
|---|---|---|---|---|
| 1 | **communication skills** | 44 | 2 | dev, test, train |
| 2 | **teaching** | 19 | 1 | dev, test, train |
| 3 | **motivated** | 18 | 1 | dev, test, train |
| 4 | **apply your depth of knowledge and expertise** | 15 | 7 | dev, test, train |
| 5 | **partner continuously with your many stakeholders** | 15 | 6 | dev, test, train |
| 6 | **structured** | 14 | 1 | dev, test, train |
| 7 | **work in large collaborative teams** | 13 | 5 | dev, test, train |
| 8 | **passionate** | 13 | 1 | dev, train |
| 9 | **team player** | 13 | 2 | dev, test, train |
| 10 | **communication** | 13 | 1 | dev, test, train |
| 11 | **building an innovative culture** | 12 | 4 | dev, test, train |
| 12 | **proactive** | 11 | 1 | test, train |
| 13 | **curious** | 11 | 1 | dev, test, train |
| 14 | **ambitious** | 10 | 1 | dev, test, train |
| 15 | **analytical** | 10 | 1 | test, train |

## 4. Top Knowledge Entities in Vocabulary

| Rank | Knowledge Entity | Frequency | Token Length | Observed Splits |
|---|---|---|---|---|
| 1 | **English** | 103 | 1 | dev, test, train |
| 2 | **Java** | 43 | 1 | dev, test, train |
| 3 | **java** | 41 | 1 | dev, test, train |
| 4 | **JavaScript** | 37 | 1 | dev, test, train |
| 5 | **Financial Services** | 37 | 2 | dev, test, train |
| 6 | **Python** | 36 | 1 | dev, test, train |
| 7 | **AWS** | 31 | 1 | dev, test, train |
| 8 | **Docker** | 27 | 1 | dev, test, train |
| 9 | **Kubernetes** | 27 | 1 | dev, test, train |
| 10 | **javascript** | 27 | 1 | dev, test, train |
| 11 | **python** | 27 | 1 | dev, test, train |
| 12 | **React** | 26 | 1 | dev, test, train |
| 13 | **cloud** | 25 | 1 | dev, test, train |
| 14 | **amazon-web-services** | 24 | 1 | dev, test, train |
| 15 | **testing** | 24 | 1 | dev, test, train |

