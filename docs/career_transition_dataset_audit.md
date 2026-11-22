# Elevate X AI — Career Transition Dataset Acquisition & Provenance Audit

## 1. Dataset Overview & Source Integrity

All datasets utilized in the Career Transition & Skill Transferability engine are sourced from official government labor agencies and verified public research corpuses. No synthetic workers, synthetic resumes, or fabricated occupation benchmarks were used.

### Download Manifest & Checksums
- Audit File: `datasets/career_transition/audit/download_audit.json`
- Total Raw Files Verified: 29 / 29 (100% SHA256 checksum verification match)

| Dataset | Issuing Agency / Authority | Format | Local Path | Verified Checksum Status |
|---|---|---|---|---|
| **ESCO v1.2.1 Occupations** | European Commission DG EMPL | CSV | `raw/esco/occupations_en.csv` | MATCH |
| **ESCO v1.2.1 Skills** | European Commission DG EMPL | CSV | `raw/esco/skills_en.csv` | MATCH |
| **ESCO v1.2.1 Relations** | European Commission DG EMPL | CSV | `raw/esco/occupationSkillRelations_en.csv` | MATCH |
| **O*NET 28.1 Occupations** | USDOL / ETA | TXT (Tab) | `raw/onet/Occupation Data.txt` | MATCH |
| **O*NET 28.1 Work Activities** | USDOL / ETA | TXT (Tab) | `raw/onet/Work Activities.txt` | MATCH |
| **India NCO-2015 Vol I** | DGE, MoLE, Govt of India | PDF | `raw/nco/National_Classification_of_Occupations_Vol_I-2015.pdf` | MATCH |
| **India NCO-2015 Vol II-A** | DGE, MoLE, Govt of India | PDF | `raw/nco/National_Classification_of_Occupations_Vol_II-A-2015.pdf` | MATCH |
| **India NCO-2015 Vol II-B** | DGE, MoLE, Govt of India | PDF | `raw/nco/National_Classification_of_Occupations_Vol_II-B-2015.pdf` | MATCH |
| **Authentic Job Postings** | Recruitment JD Corpus | Parquet | `raw/job_descriptions/recruitment_jds_english.parquet` | MATCH |
| **Authentic Indian Postings** | Shresth786 Job Dataset | CSV | `raw/job_descriptions/shresth_jobs.csv` | MATCH |
| **Verified Learning Catalog** | Curated Govt/Industry Portals | JSON | `raw/learning_resources/verified_resource_catalog.json` | MATCH |

---

## 2. Extraction & Preprocessing Pipeline

The acquisition and transformation pipeline consists of 20 reproducible scripts in `datasets/career_transition/scripts/`:

1. `download_datasets.py`: Automated download and metadata tagging.
2. `verify_downloads.py`: SHA256 cryptographic verification of all downloads.
3. `inspect_dataset_schemas.py`: Schema validation, null profiling, and column mapping.
4. `extract_india_nco.py`: PyPDF extraction of 1,746 8-digit NCO-2015 codes and definitions from official DGE volumes.
5. `preprocess_esco.py`: Normalization into Parquet (`esco_occupations`, `esco_skills`, `esco_relations`).
6. `preprocess_onet.py`: Extraction of 1,016 O*NET SOC occupations and 40,771 competency weights.
7. `preprocess_nco.py`: Standardizing NCO records with ISCO unit group references.
8. `preprocess_job_descriptions.py`: Cleansing 13,999 authentic job descriptions for salary and demand extraction.
9. `preprocess_learning_resources.py`: Verifying authentic course URLs from SWAYAM, NPTEL, Coursera, MIT OCW.
10. `normalize_occupations.py`: Consolidating 5,805 unified master occupations.
11. `normalize_skills.py`: Consolidating 14,011 unified master skills.
12. `build_occupation_skill_graph.py`: Assembling 183,702 knowledge graph edges.
13. `build_crosswalks.py`: Creating multi-taxonomy crosswalk between ESCO, O*NET, and NCO-2015 (2,762 links).
14. `deduplicate_records.py`: Cross-taxonomy equivalence analysis and deduplication audit.
15. `audit_datasets.py`: Compiling comprehensive quality report (`data_quality_report.json`).

---

## 3. Data Quality & Completeness Audit

- **Total Occupations:** 5,805 (0 null titles, 0 missing canonical IDs).
- **Total Skills:** 14,011 (0 null names, 100% valid taxonomy provenance).
- **Knowledge Graph Density:**
  - Nodes: 22,434
  - Edges: 183,702
  - Average Degree per Occupation: 31.6 skills
- **Job Market Data Grounding:**
  - 13,999 authentic job postings from real recruitment channels.
  - Salary ranges extracted directly from real text (discloses when unavailable rather than fabricating).
