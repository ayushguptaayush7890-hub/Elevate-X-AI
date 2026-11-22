# Career Transition & Skill Transferability: Official Dataset Provenance

**Document Version:** 2.0.0  
**Effective Date:** November 22, 2026  
**Auditor:** Elevate X AI Core Engineering Team  
**System Scope:** Data-driven occupational mobility, bipartite occupation-competency graph, and skill transferability engine.  
**Compliance Mandate:** Zero synthetic benchmarks, zero fabricated skill mappings, and complete provenance preservation for every occupational and competency entity.

---

## 1. Executive Provenance Summary

The Elevate X AI Career Transition module relies exclusively on authentic, publicly verifiable occupational datasets, official national and international competency standards, authentic job-market postings, and verified educational resources.

| Dataset / Resource | Authority / Source | Local File Location | Version / Release | Authentic Record Count | Primary Role in Career Transition |
| :--- | :--- | :--- | :--- | :---: | :--- |
| **ESCO Occupations** | European Commission (DG EMPL) | `datasets/career_transition/processed/occupations/esco_occupations.parquet` | v1.2.1 | **3,043** | Master international vocational and professional occupation definitions |
| **ESCO Skills & Competencies** | European Commission (DG EMPL) | `datasets/career_transition/processed/skills/esco_skills.parquet` | v1.2.1 | **13,960** | Essential & optional knowledge and skill taxonomy |
| **ESCO Relations Graph** | European Commission (DG EMPL) | `datasets/career_transition/processed/occupation_skill_graph/esco_relations.parquet` | v1.2.1 | **126,051** | Ground-truth bipartite edges between occupations and competencies |
| **O\*NET Occupations** | U.S. Department of Labor (USDOL/ETA) | `datasets/career_transition/processed/occupations/onet_occupations.parquet` | 28.1 | **1,016** | Standard Occupational Classification (SOC) profiles & Job Zones |
| **O\*NET Competencies** | U.S. Department of Labor (USDOL/ETA) | `datasets/career_transition/processed/skills/onet_competencies.parquet` | 28.1 | **51** | Cross-functional generalized work activities, knowledge & abilities |
| **O\*NET Relations Graph** | U.S. Department of Labor (USDOL/ETA) | `datasets/career_transition/processed/occupation_skill_graph/onet_relations.parquet` | 28.1 | **40,771** | Rated importance and level scores for occupational competencies |
| **India NCO-2015** | Ministry of Labour and Employment, Govt. of India | `datasets/career_transition/processed/occupations/nco_occupations.parquet` | 2015 | **1,746** | India-specific trade occupations (Divisions 1 through 9) |
| **Occupation Crosswalks** | Joint US-EU & National Taxonomy Alignment | `datasets/career_transition/processed/crosswalks/occupation_crosswalk.parquet` | 2026.1 | **2,762** | Cross-taxonomy equivalencies across ESCO, O*NET, and NCO |
| **Bipartite Graph Edges** | Unified Multigraph Consolidation | `datasets/career_transition/processed/occupation_skill_graph/edges.parquet` | Consolidated | **192,802** | PyTorch Node2Vec graph embedding training foundation |
| **Normalized Job Postings** | Authentic Aggregated Tech & Vocational Postings | `datasets/career_transition/processed/job_descriptions/normalized_jobs.parquet` | 2026 Ingestion | **13,999** | Empirical market demand, salary distributions, and vacancy volume |
| **Verified Learning Resources** | Curated Courseware & Technical Documentation | `datasets/career_transition/processed/learning_resources/verified_resources.json` | Curated | **50+** | Actionable bridge courses with verified URLs and providers |

---

## 2. In-Depth Dataset Audits & Source Provenance

### A. ESCO (European Skills, Competences, Qualifications and Occupations)
- **Issuing Entity:** Directorate-General for Employment, Social Affairs and Inclusion, European Commission.
- **Official Download URL:** [https://esco.ec.europa.eu/en/use-esco/download](https://esco.ec.europa.eu/en/use-esco/download)
- **License:** Open data under Creative Commons Attribution 4.0 International (CC BY 4.0).
- **Processing Steps:**
  1. Extracted occupation records from official CSV dumps (`occupations_en.csv`).
  2. Extracted skill concept nodes (`skills_en.csv`) and alternative multilingual aliases.
  3. Extracted bipartite mapping relations (`occupationSkillRelations.csv`), isolating `essential` vs. `optional` edge weights.
  4. Deduplicated URIs and normalized UTF-8 text representations.
  5. Serialized to column-oriented Apache Parquet with Snappy compression for low-latency in-memory queries.
- **Mapping Limitations:** Primarily calibrated to international and European occupational standards; cross-referenced with Indian NCO-2015 to support local trade terminology.

### B. O\*NET (Occupational Information Network)
- **Issuing Entity:** National Center for O*NET Development on behalf of the U.S. Department of Labor.
- **Official Source:** [https://www.onetcenter.org/database.html](https://www.onetcenter.org/database.html)
- **Release Version:** O*NET 28.1 Database.
- **Files Ingested:** `Occupation Data.txt`, `Skills.txt`, `Knowledge.txt`, `Abilities.txt`, `Work Activities.txt`, `Job Zones.txt`.
- **Processing Steps:**
  1. Parsed tab-delimited files preserving O*NET-SOC codes (e.g. `15-1252.00`).
  2. Filtered competency importance scores with threshold $\ge 50.0$ on a 100-point scale to eliminate low-relevance noise.
  3. Merged generalized competencies into canonical cross-functional vectors.
  4. Serialized to `onet_occupations.parquet` (1,016 entries) and `onet_relations.parquet` (40,771 edges).

### C. India NCO-2015 (National Classification of Occupations)
- **Issuing Entity:** Directorate General of Employment, Ministry of Labour and Employment, New Delhi, India.
- **Official Source:** Government of India Gazette / Ministry of Labour & Employment publication.
- **Processing Steps:**
  1. Ingested volume files covering Divisions 1 through 9.
  2. Parsed 8-digit and 4-digit occupational classification codes, preserving division, sub-division, group, and family codes.
  3. Cleaned OCR anomalies and standardized vocational task descriptions.
  4. Verified 1,746 distinct occupations.
  5. Constructed cross-walk mappings linking NCO trade codes to corresponding ESCO and O*NET unit groups.

### D. Real-World Job Descriptions & Market Metrics
- **Dataset File:** `datasets/career_transition/processed/job_descriptions/normalized_jobs.parquet`
- **Total Records:** 13,999 job postings across vocational and software domains.
- **Fields Extracted:** `job_id`, `job_title`, `company`, `category`, `location`, `description`, `extracted_skills`, `years_required`.
- **Demand Calculation Methodology:**
  - Occupation titles in candidate queries are matched against the 13,999 job descriptions using semantic cosine similarity and canonical title matching.
  - Active posting frequency determines the `demand_level`:
    - $\ge 25$ postings: **High Demand**
    - $5 - 24$ postings: **Moderate Demand**
    - $< 5$ postings: **Emerging / Specialized Demand**
  - Salary estimates are computed from actual recorded compensation ranges in the normalized corpus.
  - Explicit notification is provided when real-time live API credentials are not configured.

### E. Verified Learning Resources
- **Dataset File:** `datasets/career_transition/processed/learning_resources/verified_resources.json`
- **Authenticity Mandate:** Every included resource has been verified for domain validity, platform provenance (e.g., Coursera, MIT OpenCourseWare, freeCodeCamp, edX, NPTEL, MDN Web Docs, official documentation), and valid URL routing.
- **Zero Fabrication:** No synthetic course names or broken URLs are permitted.

---

## 3. Data Integrity & Verification Checklist

- [x] All 5,805 master occupations are traced to verified source registries (ESCO, O*NET, NCO).
- [x] All 14,011 skills possess official IDs, source attribution, and descriptions.
- [x] All 192,802 graph edges originate from official taxonomy relational mappings.
- [x] No manually fabricated skills or occupations exist in the dataset pipeline.
- [x] Academic competencies are extracted from genuine candidate records (degree, coursework, projects) and explicitly marked as requiring practical workplace demonstration.
