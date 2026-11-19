# ELEVATE X AI — PREPROCESSING & FEATURE ENGINEERING REPORT

**Dataset**: O*NET Essential Skills Catalog
**Cleaned Output**: `datasets/informal_skill_extraction/processed/essential_skills_cleaned.csv`
**Occupation Mapping Output**: `datasets/informal_skill_extraction/processed/occupation_skill_mapping.csv`
**Skill Catalog Output**: `datasets/informal_skill_extraction/processed/skill_frequency.csv`

---

## 1. Cleaning & Standardization Transformations

1. **Whitespace Cleaning**: Applied `.str.strip()` across all text columns to eliminate trailing or leading space anomalies.
2. **Snake_Case Column Harmonization**: Converted raw verbose headers (`O*NET-SOC Code`, `Data Value`, etc.) into standardized snake_case (`onet_soc_code`, `data_value`, etc.).
3. **SOC Code Integrity Verification**: Validated 100% of occupation codes against the official regex pattern `^\d{2}-\d{4}\.\d{2}$`. 0 invalid codes found.
4. **Range Enforcement & Boundary Checks**:
   - `Importance (IM)`: Verified all values strictly adhere to `[1.00, 5.00]`. 0 outliers found.
   - `Level (LV)`: Verified all values strictly adhere to `[0.00, 7.00]`. 0 outliers found.
5. **Boolean Flag Resolution**:
   - `recommend_suppress_bool`: True for 21 records with high statistical variance.
   - `not_relevant_bool`: True for 298 records where the skill is not applicable to the occupation.

## 2. Feature Engineering & Mathematical Normalization

### Normalized Score (`normalized_score`)
Because Importance and Level use distinct intervals, we mapped both scales onto a unified unit interval $[0.0, 1.0]$:

$$\text{Normalized Importance} = \frac{\text{Data Value} - 1.0}{5.0 - 1.0} = \frac{\text{Data Value} - 1.0}{4.0}$$

$$\text{Normalized Level} = \frac{\text{Data Value} - 0.0}{7.0 - 0.0} = \frac{\text{Data Value}}{7.0}$$

This allows distance algorithms (e.g., Cosine Similarity, Euclidean Distance) to balance importance and difficulty level without scale distortion.

### Wide-Format Transformation (`occupation_skill_mapping.csv`)
- Formatted 910 occupations as distinct rows with 47 columns.
- Provided raw and normalized feature columns for each of the 10 foundational skills.
- Computed derived metrics: `mean_importance_score`, `mean_level_score`, `skill_intensity_index`, `primary_essential_skill`, and `not_relevant_skill_count`.

## 3. Skill Ranking Hierarchy (National Labor Market)

| Rank | Element ID | Skill Name | Category | Mean Importance (1-5) | Mean Level (0-7) | Relevant Occupations (%) |
|---|---|---|---|---|---|---|
| 1 | `2.A.1.b` | **Active Listening** | Basic Skills - Content | 3.60 | 3.56 | 100.0% |
| 2 | `2.A.1.d` | **Speaking** | Basic Skills - Content | 3.54 | 3.47 | 100.0% |
| 3 | `2.A.2.a` | **Critical Thinking** | Basic Skills - Process | 3.52 | 3.58 | 100.0% |
| 4 | `2.A.1.a` | **Reading Comprehension** | Basic Skills - Content | 3.49 | 3.66 | 100.0% |
| 5 | `2.A.2.d` | **Monitoring** | Basic Skills - Process | 3.31 | 3.38 | 100.0% |
| 6 | `2.A.1.c` | **Writing** | Basic Skills - Content | 3.19 | 3.32 | 100.0% |
| 7 | `2.A.2.b` | **Active Learning** | Basic Skills - Process | 3.12 | 3.20 | 100.0% |
| 8 | `2.A.2.c` | **Learning Strategies** | Basic Skills - Process | 2.79 | 2.85 | 99.9% |
| 9 | `2.A.1.e` | **Mathematics** | Basic Skills - Content | 2.55 | 2.55 | 99.6% |
| 10 | `2.A.1.f` | **Science** | Basic Skills - Content | 1.93 | 1.42 | 67.8% |

