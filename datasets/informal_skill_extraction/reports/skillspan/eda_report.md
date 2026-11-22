# ELEVATE X AI — SKILLSPAN EXPLORATORY DATA ANALYSIS REPORT

**Dataset**: SkillSpan (Named Entity Recognition for Hard/Soft Skills and Knowledge)
**Data Sources**: `datasets/informal_skill_extraction/raw/skillspan/[train.json, dev.json, test.json]`
**Analytical Scope**: 11,543 sentences, 176,296 tokens, 9,618 entity spans

---

## 1. Visualizations & Plain-Language Explanations

### Figure 1: Sentence Length Distribution
![Sentence Length](../visualizations/skillspan/sentence_length_distribution.png)

**Plain-Language Explanation**:
- Job posting sentences average **15.3 tokens** with a median of **11 tokens**.
- The distribution exhibits a heavy positive skew. Most bullet points are concise phrases (5–20 words), while 5% of complex requirement descriptions exceed 35 tokens.
- Maximum sentence length is 122 tokens. Models using transformer token limits (e.g., 256 or 512 tokens) can comfortably ingest 100% of the sentences without truncation.

### Figure 2: Entity Sparsity & Count per Sentence
![Skills per Sentence](../visualizations/skillspan/skills_per_sentence_distribution.png)

**Plain-Language Explanation**:
- **Entity Sparsity**: Approximately 78.4% of sentences in the dataset contain zero skill spans, and 83.5% contain zero knowledge spans.
- This reflects real-world job posting composition: many sentences are boilerplate intro text, organizational descriptions, location addresses, benefits disclosures, or contact info.
- When a requirement sentence does contain skills, it typically mentions 1 to 3 distinct competencies.

### Figure 3: Top Skill and Knowledge Vocabulary
![Top Labels](../visualizations/skillspan/top_skill_and_knowledge_labels.png)

**Plain-Language Explanation**:
- **Skills**: Most frequently annotated skills include *'communication skills'* (44 occurrences), *'teaching'* (19), *'motivated'* (18), and collaborative execution phrases (*'apply your depth of knowledge and expertise'*, *'partner continuously with your many stakeholders'*).
- **Knowledge**: Most frequently annotated knowledge items include *'English'* (103 occurrences), *'Java'* (84 combined casing), *'JavaScript'* (64), *'Python'* (36), *'AWS'* (31), *'Docker'* (27), and *'Kubernetes'* (27).
- This illustrates the fundamental duality: skills describe *actions and soft behaviors*, while knowledge describes *tools, frameworks, and domains*.

### Figure 4: Train / Dev / Test Split Proportions
![Split Comparison](../visualizations/skillspan/split_comparison.png)

**Plain-Language Explanation**:
- The dataset is partitioned into: **41.6% Train** (4,800 sentences), **27.5% Dev** (3,174 sentences), and **30.9% Test** (3,569 sentences).
- Token, skill span, and knowledge span ratios mirror the sentence counts across splits, confirming balanced document-level stratification with zero data leakage.

### Figure 5: Token Coverage Breakdown by Domain
![Coverage by Domain](../visualizations/skillspan/annotation_coverage_by_domain.png)

**Plain-Language Explanation**:
- In tech job postings (`tech`), skill tokens account for 10.6% and knowledge tokens account for 5.7% of all words (total entity coverage: ~16.3%).
- In broader house job postings (`house`), skill tokens account for 9.8% and knowledge tokens account for 4.2% of words (total entity coverage: ~14.0%).
- Over 83–86% of tokens in job postings are background words (stopwords, punctuation, verbs of employment), which models must learn to ignore.

