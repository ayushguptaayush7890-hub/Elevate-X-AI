# ELEVATE X AI — ESCO v1.2.1 EXPLORATORY DATA ANALYSIS REPORT

**Dataset**: European Skills, Competences, Qualifications and Occupations (ESCO v1.2.1 English)
**Directory**: `datasets/informal_skill_extraction/raw/esco`
**Analytical Scope**: 3,039 standardized occupations, 13,939 unique skills, 126,051 relational edges

---

## 1. Visualizations & Plain-Language Explanations

### Figure 1: Top Occupations by Associated Skills
![Top Occupations](../visualizations/esco/top_occupations_by_skills.png)

**Plain-Language Explanation**:
- Complex multidisciplinary occupations (such as *directors*, *curators*, *environmental engineers*, and *healthcare specialists*) require between 90 and 130+ distinct skills.
- Across all occupations in ESCO, the median job links to approximately **38 total skills** (~20 essential skills and ~18 optional skills).
- This demonstrates the high granularity of ESCO compared to broader taxonomies like O*NET.

### Figure 2: Most Frequently Linked Skills
![Most Frequently Linked Skills](../visualizations/esco/most_frequently_linked_skills.png)

**Plain-Language Explanation**:
- The most versatile transversal skills across the entire European economy include:
  - *'adapt to change'* (linked to 1,738 occupations)
  - *'work in teams'* (linked to 1,692 occupations)
  - *'communication'* / *'communicate with customers'* (linked to 1,400+ occupations)
  - *'solve problems'* (linked to 1,300+ occupations)
- Knowledge concepts with the highest ubiquity include *'workplace health and safety regulations'*, *'quality standards'*, and *'project management'*.

### Figure 3: Occupational Structure by ISCO-08 Major Groups
![Occupation Hierarchy](../visualizations/esco/occupation_hierarchy_isco.png)

**Plain-Language Explanation**:
- Occupations are mapped to the International Standard Classification of Occupations (ISCO-08):
  - **Group 2: Professionals**: 873 occupations (28.7%)
  - **Group 3: Technicians & Associate Professionals**: 651 occupations (21.4%)
  - **Group 7: Craft & Related Trades Workers**: 394 occupations (13.0%) — *direct vocational crafts*
  - **Group 8: Plant & Machine Operators**: 347 occupations (11.4%) — *industrial machine trades*
  - **Group 9: Elementary Occupations**: 76 occupations (2.5%) — *entry manual labor*
- **Crucial for Elevate X AI**: Over **817 occupations (26.9%)** represent hands-on crafts, machine operations, and manual trades directly relevant to informal and blue-collar upskilling.

### Figure 4: Top Competency Clusters in Skills Pillar
![Skill Groups](../visualizations/esco/skill_group_distribution.png)

**Plain-Language Explanation**:
- Skills cluster into actionable domain groups: *'installing wooden and metal components'*, *'mechanics and metal trades'*, *'food processing'*, *'monitoring quality of products'*, and *'complying with health and safety'*.
- These clusters align closely with vocational trade certifications and modular micro-credentials.

### Figure 5: Relationship and Skill Modality
![Modality](../visualizations/esco/relation_and_skill_types.png)

**Plain-Language Explanation**:
- **53.6% Essential vs 46.4% Optional**: Enables Elevate X AI to differentiate non-negotiable core trade competencies from supplemental specialization options.
- **72.7% Applied Skills vs 27.3% Knowledge**: ESCO heavily emphasizes practical, observable capabilities (*skills/competence*) over pure theoretical knowledge.

### Figure 6: Metadata Completeness
![Missing Values](../visualizations/esco/missing_values_profile.png)

**Plain-Language Explanation**:
- All core identifiers (`conceptUri`, `preferredLabel`, `iscoGroup`, `relationType`) are 100% complete.
- Optional auxiliary fields like `hiddenLabels` (misspellings/abbreviations) and `scopeNote` have expected null rates (~90%) because they are only provided where necessary.

