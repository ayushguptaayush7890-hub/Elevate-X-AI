# ELEVATE X AI — MASTER INITIAL DATASET 4 AUDIT
**Audit Timestamp**: 2026-11-14 22:49:24  
**Target Dataset**: Dataset 4 — Indian Informal Worker Descriptions  
**Standard**: Full Verifiable File-Level Inspection across All Partitions  

---

## 1. Executive Summary & Ground Truth Verification
> [!IMPORTANT]
> ### INVENTORY GROUND TRUTH SUMMARY
> - **Total Dataset 4 Files Inventoried**: **112 files**
> - **Group A — Genuine Worker Records**: **0** (ZERO)
> - **Group A — Unique Genuine Workers**: **0** (ZERO)
> - **Group A — Genuine Skill Spans**: **0** (ZERO)
> - **Group B — Synthetic Development Stubs**: **20 records** (40 skill spans, quarantined)
> - **Group C — Official Vocational References**: **24 catalogued standards** (10 Occupations, 14 QPs)
> - **Group D — External Sourced / Adapted Records**: **0 records**
> - **Documentation & Audit Reports**: **37 files**
> - **Pipeline Automation Scripts**: **26 scripts**
> 
> **Key Verification**: All synthetic stubs are strictly segregated in `synthetic_test_only/` and `processed/indian_worker_data/all_occupations/synthetic_test_processed.jsonl`. No synthetic record has entered genuine data partitions (`raw/indian_worker_data/real/` or `processed/indian_worker_data/genuine_worker_data/`).

## 2. Partition Group Segregation Audit
| Partition Group | File Count | Records Tracked | Provenance Status | Model Training Eligibility |
|---|---|---|---|---|
| **Group A: Genuine Worker Data** | 1 | 0 | Field Interviews Pending | **NO (0 records)** |
| **Group B: Synthetic Development Data** | 7 | 20 | Verified Test Stubs | **NO (Test Only)** |
| **Group C: Official Vocational Reference** | 9 | 24 | Public NCVET/NSDC Catalogs | **NO (Taxonomy Only)** |
| **Group D: External Research / Adapted** | 2 | 0 | Acquisition Planned | **NO (0 records)** |
| **Documentation & Reports** | 37 | N/A | Markdown Audit Documentation | Reference Only |
| **Pipeline Automation Scripts** | 26 | N/A | Python Automation Engines | Operational |

## 3. Comprehensive File Inventory
| Relative File Path | Format | Partition Group | Size | Records | Valid | Duplicates | Spans | SHA-256 (First 12 chars) |
|---|---|---|---|---|---|---|---|---|
| `datasets/informal_skill_extraction/reports/indian_worker_data/annotation_guidelines.md` | MD | Documentation / Audit Reports | 8,722 B | 128 | 128 | 0 | 0 | `d0a2e32e208a` |
| `datasets/informal_skill_extraction/reports/indian_worker_data/annotation_quality_audit.md` | MD | Documentation / Audit Reports | 3,307 B | 48 | 48 | 0 | 0 | `462afe15ad9e` |
| `datasets/informal_skill_extraction/reports/indian_worker_data/annotation_quality_report.md` | MD | Documentation / Audit Reports | 1,977 B | 31 | 31 | 0 | 0 | `f3cf88203366` |
| `datasets/informal_skill_extraction/reports/indian_worker_data/canonical_skill_coverage_report.md` | MD | Documentation / Audit Reports | 1,748 B | 32 | 32 | 0 | 0 | `ff71d3ae188d` |
| `datasets/informal_skill_extraction/reports/indian_worker_data/collection_plan.md` | MD | Documentation / Audit Reports | 6,363 B | 101 | 101 | 0 | 0 | `45fa077bd7d6` |
| `datasets/informal_skill_extraction/reports/indian_worker_data/collection_progress_report.md` | MD | Documentation / Audit Reports | 3,876 B | 47 | 47 | 0 | 0 | `f5cf467a88e3` |
| `datasets/informal_skill_extraction/reports/indian_worker_data/collection_targets.csv` | CSV | Documentation / Audit Reports | 1,479 B | 10 | 10 | 0 | 0 | `1ee8871194a0` |
| `datasets/informal_skill_extraction/reports/indian_worker_data/consent_form_english.md` | MD | Documentation / Audit Reports | 3,474 B | 52 | 52 | 0 | 0 | `4e25323d6b72` |
| `datasets/informal_skill_extraction/reports/indian_worker_data/consent_form_hindi.md` | MD | Documentation / Audit Reports | 6,708 B | 53 | 53 | 0 | 0 | `f42ad8d040a2` |
| `datasets/informal_skill_extraction/reports/indian_worker_data/data_quality_report.md` | MD | Documentation / Audit Reports | 4,354 B | 71 | 71 | 0 | 0 | `b6f61312be8a` |
| `datasets/informal_skill_extraction/reports/indian_worker_data/dataset_expansion_roadmap.md` | MD | Documentation / Audit Reports | 6,916 B | 98 | 98 | 0 | 0 | `8192f1e08ecf` |
| `datasets/informal_skill_extraction/reports/indian_worker_data/dataset_gap_analysis.md` | MD | Documentation / Audit Reports | 3,606 B | 42 | 42 | 0 | 0 | `dc6c0812182e` |
| `datasets/informal_skill_extraction/reports/indian_worker_data/dataset_quantity_audit.md` | MD | Documentation / Audit Reports | 5,834 B | 68 | 68 | 0 | 0 | `1f1d36516b3c` |
| `datasets/informal_skill_extraction/reports/indian_worker_data/field_collection_guide.md` | MD | Documentation / Audit Reports | 11,674 B | 164 | 164 | 0 | 0 | `35aa935c42cd` |
| `datasets/informal_skill_extraction/reports/indian_worker_data/field_collection_system.md` | MD | Documentation / Audit Reports | 4,052 B | 77 | 77 | 0 | 0 | `9ab8bbca1907` |
| `datasets/informal_skill_extraction/reports/indian_worker_data/final_dataset_audit.md` | MD | Documentation / Audit Reports | 9,179 B | 149 | 149 | 0 | 0 | `09647dd7c043` |
| `datasets/informal_skill_extraction/reports/indian_worker_data/interview_questionnaire_english.md` | MD | Documentation / Audit Reports | 5,738 B | 69 | 69 | 0 | 0 | `7fab0311e2ed` |
| `datasets/informal_skill_extraction/reports/indian_worker_data/interview_questionnaire_hindi.md` | MD | Documentation / Audit Reports | 11,172 B | 69 | 69 | 0 | 0 | `4518ec921fdf` |
| `datasets/informal_skill_extraction/reports/indian_worker_data/language_coverage_report.md` | MD | Documentation / Audit Reports | 5,085 B | 55 | 55 | 0 | 0 | `b8a7ff12c1f9` |
| `datasets/informal_skill_extraction/reports/indian_worker_data/language_diversity_audit.csv` | CSV | Documentation / Audit Reports | 4,499 B | 40 | 40 | 0 | 0 | `e839d7c64cfc` |
| `datasets/informal_skill_extraction/reports/indian_worker_data/master_dataset_metrics.csv` | CSV | Documentation / Audit Reports | 840 B | 14 | 14 | 0 | 0 | `d74ee0efe6b5` |
| `datasets/informal_skill_extraction/reports/indian_worker_data/master_dataset_monitoring_report.md` | MD | Documentation / Audit Reports | 3,864 B | 63 | 63 | 0 | 0 | `ae9a00de3a4e` |
| `datasets/informal_skill_extraction/reports/indian_worker_data/master_file_inventory.csv` | CSV | Documentation / Audit Reports | 27,457 B | 104 | 104 | 0 | 0 | `8aca3b88ce89` |
| `datasets/informal_skill_extraction/reports/indian_worker_data/master_initial_audit.md` | MD | Documentation / Audit Reports | 21,363 B | 142 | 142 | 0 | 0 | `ec15227c716e` |
| `datasets/informal_skill_extraction/reports/indian_worker_data/model_training_readiness.md` | MD | Documentation / Audit Reports | 3,245 B | 53 | 53 | 0 | 0 | `7ab7b89c9cc9` |
| `datasets/informal_skill_extraction/reports/indian_worker_data/occupation_coverage_matrix.csv` | CSV | Documentation / Audit Reports | 1,511 B | 10 | 10 | 0 | 0 | `3a24a985bbe6` |
| `datasets/informal_skill_extraction/reports/indian_worker_data/occupation_specific_collection_modules.md` | MD | Documentation / Audit Reports | 23,046 B | 225 | 225 | 0 | 0 | `7f200e36d163` |
| `datasets/informal_skill_extraction/reports/indian_worker_data/phase1_collection_progress.md` | MD | Documentation / Audit Reports | 3,810 B | 63 | 63 | 0 | 0 | `141923fc636b` |
| `datasets/informal_skill_extraction/reports/indian_worker_data/phase1_occupation_progress.csv` | CSV | Documentation / Audit Reports | 478 B | 4 | 4 | 0 | 0 | `051f9ef0c47d` |
| `datasets/informal_skill_extraction/reports/indian_worker_data/preprocessing_report.md` | MD | Documentation / Audit Reports | 1,746 B | 42 | 42 | 0 | 0 | `a0ac5a4c975f` |
| `datasets/informal_skill_extraction/reports/indian_worker_data/public_dataset_research.md` | MD | Documentation / Audit Reports | 10,977 B | 141 | 141 | 0 | 0 | `076f41eb8c2e` |
| `datasets/informal_skill_extraction/reports/indian_worker_data/skill_mapping_quality_report.md` | MD | Documentation / Audit Reports | 6,518 B | 73 | 73 | 0 | 0 | `6dfe92381ecb` |
| `datasets/informal_skill_extraction/reports/indian_worker_data/source_licence_audit.csv` | CSV | Documentation / Audit Reports | 5,239 B | 11 | 11 | 0 | 0 | `440caa7b6af7` |
| `datasets/informal_skill_extraction/reports/indian_worker_data/trade_specific_questionnaires.md` | MD | Documentation / Audit Reports | 15,799 B | 104 | 104 | 0 | 0 | `ac6e1b4afd6e` |
| `datasets/informal_skill_extraction/reports/indian_worker_data/training_readiness_assessment.md` | MD | Documentation / Audit Reports | 5,005 B | 60 | 60 | 0 | 0 | `e909d067bd4b` |
| `datasets/informal_skill_extraction/reports/indian_worker_data/updated_collection_plan.md` | MD | Documentation / Audit Reports | 4,697 B | 67 | 67 | 0 | 0 | `deb61ed93750` |
| `datasets/informal_skill_extraction/reports/indian_worker_data/validation_report.md` | MD | Documentation / Audit Reports | 2,417 B | 59 | 59 | 0 | 0 | `9cbf08765dda` |
| `datasets/informal_skill_extraction/raw/indian_worker_data/real/pilot_tailor_batch1.jsonl` | JSONL | Group A: Genuine Worker Data | 0 B | 0 | 0 | 0 | 0 | `e3b0c44298fc` |
| `datasets/informal_skill_extraction/interim/indian_worker_data/synthetic_pipeline_test.jsonl` | JSONL | Group B: Synthetic Development Data | 40,575 B | 20 | 20 | 0 | 40 | `c40f7697b8ef` |
| `datasets/informal_skill_extraction/processed/indian_worker_data/all_occupations/synthetic_test_processed.jsonl` | JSONL | Group B: Synthetic Development Data | 41,555 B | 20 | 20 | 0 | 40 | `2944cd1f9fc7` |
| `datasets/informal_skill_extraction/processed/indian_worker_data/synthetic_augmentation/synthetic_augmented_corpus.jsonl` | JSONL | Group B: Synthetic Development Data | 1,155,984 B | 500 | 500 | 0 | 1000 | `132d88cf9c96` |
| `datasets/informal_skill_extraction/raw/indian_worker_data/synthetic_augmentation/synthetic_augmented_corpus.jsonl` | JSONL | Group B: Synthetic Development Data | 1,155,984 B | 500 | 500 | 0 | 1000 | `132d88cf9c96` |
| `datasets/informal_skill_extraction/raw/indian_worker_data/synthetic_test_only/synthetic_pipeline_test.jsonl` | JSONL | Group B: Synthetic Development Data | 40,575 B | 20 | 20 | 0 | 40 | `c40f7697b8ef` |
| `datasets/informal_skill_extraction/reports/indian_worker_data/synthetic_augmentation_quality_report.md` | MD | Group B: Synthetic Development Data | 2,211 B | 41 | 41 | 0 | 0 | `16f56628f821` |
| `datasets/informal_skill_extraction/reports/indian_worker_data/synthetic_quality_audit.md` | MD | Group B: Synthetic Development Data | 2,704 B | 62 | 62 | 0 | 0 | `e7fdccb418b0` |
| `datasets/informal_skill_extraction/processed/indian_worker_data/occupation_taxonomy.csv` | CSV | Group C: Official Vocational Reference | 12,940 B | 10 | 10 | 0 | 0 | `5fab583368cc` |
| `datasets/informal_skill_extraction/processed/indian_worker_data/official_reference_data/dgt_cts_extracted_trades.csv` | CSV | Group C: Official Vocational Reference | 104,415 B | 169 | 169 | 0 | 0 | `8118e5471cfb` |
| `datasets/informal_skill_extraction/processed/indian_worker_data/official_reference_data/dgt_cts_extracted_trades.json` | JSON | Group C: Official Vocational Reference | 162,235 B | 2706 | 2706 | 0 | 0 | `0ab35ac18b9b` |
| `datasets/informal_skill_extraction/processed/indian_worker_data/source_catalog.csv` | CSV | Group C: Official Vocational Reference | 5,582 B | 14 | 14 | 0 | 0 | `e468430688c6` |
| `datasets/informal_skill_extraction/raw/indian_worker_data/occupation_taxonomy.csv` | CSV | Group C: Official Vocational Reference | 12,940 B | 10 | 10 | 0 | 0 | `5fab583368cc` |
| `datasets/informal_skill_extraction/raw/indian_worker_data/official_standards/dgt_cts_trade_directory.html` | HTML | Group C: Official Vocational Reference | 538,833 B | 0 | 0 | 0 | 0 | `a44444e20f0e` |
| `datasets/informal_skill_extraction/raw/indian_worker_data/official_standards/download_manifest.json` | JSON | Group C: Official Vocational Reference | 2,538 B | 59 | 59 | 0 | 0 | `61db63907dd1` |
| `datasets/informal_skill_extraction/raw/indian_worker_data/official_standards/nqr_portal_index.html` | HTML | Group C: Official Vocational Reference | 576,440 B | 0 | 0 | 0 | 0 | `b3a9ca1467b9` |
| `datasets/informal_skill_extraction/raw/indian_worker_data/source_catalog.csv` | CSV | Group C: Official Vocational Reference | 5,582 B | 14 | 14 | 0 | 0 | `e468430688c6` |
| `datasets/informal_skill_extraction/processed/indian_worker_data/external_research_data/ai4bharat_indic_nlp_summary.json` | JSON | Group D: External Research / Adapted Data | 596 B | 21 | 21 | 0 | 0 | `d5f5aa4ad7fc` |
| `datasets/informal_skill_extraction/raw/indian_worker_data/external_sources/ai4bharat_indicbert_readme.md` | MD | Group D: External Research / Adapted Data | 11,158 B | 196 | 196 | 0 | 0 | `311e34d655f4` |
| `datasets/informal_skill_extraction/processed/indian_worker_data/annotation_guidelines.md` | MD | Other | 8,722 B | 128 | 128 | 0 | 0 | `d0a2e32e208a` |
| `datasets/informal_skill_extraction/processed/indian_worker_data/by_language/english_processed.jsonl` | JSONL | Other | 5,889 B | 3 | 3 | 0 | 6 | `88b986dae860` |
| `datasets/informal_skill_extraction/processed/indian_worker_data/by_language/hindi_processed.jsonl` | JSONL | Other | 15,973 B | 7 | 7 | 0 | 14 | `ea6149993830` |
| `datasets/informal_skill_extraction/processed/indian_worker_data/by_language/hinglish_processed.jsonl` | JSONL | Other | 19,693 B | 10 | 10 | 0 | 20 | `2041950d9787` |
| `datasets/informal_skill_extraction/processed/indian_worker_data/canonical_skill_catalogue.csv` | CSV | Other | 26,123 B | 32 | 32 | 0 | 0 | `7992167311bb` |
| `datasets/informal_skill_extraction/processed/indian_worker_data/canonical_skill_catalogue.json` | JSON | Other | 47,010 B | 1420 | 1420 | 0 | 0 | `8a696c6a8d05` |
| `datasets/informal_skill_extraction/processed/indian_worker_data/data_collection_template.csv` | CSV | Other | 2,711 B | 5 | 5 | 0 | 0 | `453f23603974` |
| `datasets/informal_skill_extraction/processed/indian_worker_data/dataset_schema.json` | JSON | Other | 8,304 B | 230 | 230 | 0 | 0 | `df699c223881` |
| `datasets/informal_skill_extraction/processed/indian_worker_data/language_vocabulary/action_verbs_vocabulary.json` | JSON | Other | 1,561 B | 51 | 51 | 0 | 0 | `668afbc99a85` |
| `datasets/informal_skill_extraction/processed/indian_worker_data/language_vocabulary/master_vocabulary_catalogue.csv` | CSV | Other | 2,525 B | 24 | 24 | 0 | 0 | `831e2298f841` |
| `datasets/informal_skill_extraction/processed/indian_worker_data/language_vocabulary/trade_terms_hindi_hinglish.json` | JSON | Other | 6,995 B | 290 | 290 | 0 | 0 | `f3bd0393fa5e` |
| `datasets/informal_skill_extraction/processed/indian_worker_data/occupation_knowledge_base/TRD-01_tailor_garment.json` | JSON | Other | 4,859 B | 141 | 141 | 0 | 0 | `61c30798cdd1` |
| `datasets/informal_skill_extraction/processed/indian_worker_data/occupation_knowledge_base/TRD-02_electrician.json` | JSON | Other | 4,949 B | 133 | 133 | 0 | 0 | `79c965dca112` |
| `datasets/informal_skill_extraction/processed/indian_worker_data/occupation_knowledge_base/TRD-03_plumber.json` | JSON | Other | 4,827 B | 133 | 133 | 0 | 0 | `de2f72c6ef24` |
| `datasets/informal_skill_extraction/processed/indian_worker_data/occupation_knowledge_base/TRD-04_motor_mechanic.json` | JSON | Other | 5,190 B | 136 | 136 | 0 | 0 | `e9690657a664` |
| `datasets/informal_skill_extraction/processed/indian_worker_data/occupation_knowledge_base/TRD-05_carpenter.json` | JSON | Other | 5,098 B | 138 | 138 | 0 | 0 | `685409e4346e` |
| `datasets/informal_skill_extraction/processed/indian_worker_data/occupation_knowledge_base/TRD-06_welder.json` | JSON | Other | 5,135 B | 133 | 133 | 0 | 0 | `28e4d19ec893` |
| `datasets/informal_skill_extraction/processed/indian_worker_data/occupation_knowledge_base/TRD-07_mason.json` | JSON | Other | 5,178 B | 135 | 135 | 0 | 0 | `64f579383b4f` |
| `datasets/informal_skill_extraction/processed/indian_worker_data/occupation_knowledge_base/TRD-08_painter.json` | JSON | Other | 5,385 B | 135 | 135 | 0 | 0 | `db460167a3b5` |
| `datasets/informal_skill_extraction/processed/indian_worker_data/occupation_knowledge_base/TRD-09_agriculture_worker.json` | JSON | Other | 5,476 B | 136 | 136 | 0 | 0 | `1fee63e7a540` |
| `datasets/informal_skill_extraction/processed/indian_worker_data/occupation_knowledge_base/TRD-10_mobile_repair.json` | JSON | Other | 5,921 B | 135 | 135 | 0 | 0 | `6a7393613c02` |
| `datasets/informal_skill_extraction/processed/indian_worker_data/occupation_knowledge_base/master_occupation_catalogue.json` | JSON | Other | 54,750 B | 1357 | 1357 | 0 | 0 | `5dbc029126a2` |
| `datasets/informal_skill_extraction/processed/indian_worker_data/pilot_tailor/pilot_tailor_processed.jsonl` | JSONL | Other | 4,349 B | 2 | 2 | 0 | 4 | `a6a236de9a9e` |
| `datasets/informal_skill_extraction/processed/indian_worker_data/training_exports/bio_sequence_tagging_export.jsonl` | JSONL | Other | 754,544 B | 500 | 500 | 499 | 0 | `ec25f689cc57` |
| `datasets/informal_skill_extraction/processed/indian_worker_data/training_exports/canonical_skill_crosswalk.csv` | CSV | Other | 5,457 B | 32 | 32 | 0 | 0 | `ee51437a5019` |
| `datasets/informal_skill_extraction/processed/indian_worker_data/training_exports/character_spans_export.jsonl` | JSONL | Other | 609,629 B | 500 | 500 | 499 | 0 | `97ef5d8eff20` |
| `datasets/informal_skill_extraction/processed/indian_worker_data/training_exports/occupation_classification_export.jsonl` | JSONL | Other | 301,094 B | 500 | 500 | 499 | 0 | `1adbfcaea37b` |
| `datasets/informal_skill_extraction/processed/indian_worker_data/training_exports/skill_multilabel_classification_export.jsonl` | JSONL | Other | 339,741 B | 500 | 500 | 499 | 0 | `6b6886f5f7b7` |
| `datasets/informal_skill_extraction/raw/indian_worker_data/data_collection_template.csv` | CSV | Other | 2,711 B | 5 | 5 | 0 | 0 | `453f23603974` |
| `datasets/informal_skill_extraction/raw/indian_worker_data/dataset_schema.json` | JSON | Other | 8,304 B | 230 | 230 | 0 | 0 | `df699c223881` |
| `datasets/informal_skill_extraction/scripts/indian_worker_data/__pycache__/collection_dashboard.cpython-313.pyc` | PYC | Pipeline Automation Scripts | 93,220 B | 0 | 0 | 0 | 0 | `cbb3d5fc7fca` |
| `datasets/informal_skill_extraction/scripts/indian_worker_data/annotation_manager.py` | PY | Pipeline Automation Scripts | 6,488 B | 148 | 148 | 0 | 0 | `2c8fb0fc42e8` |
| `datasets/informal_skill_extraction/scripts/indian_worker_data/audit_annotation_quality.py` | PY | Pipeline Automation Scripts | 6,133 B | 123 | 123 | 0 | 0 | `55bc081f88c5` |
| `datasets/informal_skill_extraction/scripts/indian_worker_data/audit_dataset.py` | PY | Pipeline Automation Scripts | 12,116 B | 259 | 259 | 0 | 0 | `8553047d02c4` |
| `datasets/informal_skill_extraction/scripts/indian_worker_data/audit_language_coverage.py` | PY | Pipeline Automation Scripts | 4,464 B | 123 | 123 | 0 | 0 | `64bebae765e9` |
| `datasets/informal_skill_extraction/scripts/indian_worker_data/audit_occupation_coverage.py` | PY | Pipeline Automation Scripts | 10,681 B | 206 | 206 | 0 | 0 | `9ee1f1b3349d` |
| `datasets/informal_skill_extraction/scripts/indian_worker_data/audit_source_downloads.py` | PY | Pipeline Automation Scripts | 13,314 B | 249 | 249 | 0 | 0 | `2f4a865a7257` |
| `datasets/informal_skill_extraction/scripts/indian_worker_data/audit_source_provenance.py` | PY | Pipeline Automation Scripts | 3,617 B | 80 | 80 | 0 | 0 | `8eb93cafb632` |
| `datasets/informal_skill_extraction/scripts/indian_worker_data/audit_synthetic_quality.py` | PY | Pipeline Automation Scripts | 8,785 B | 189 | 189 | 0 | 0 | `dd71cd54394f` |
| `datasets/informal_skill_extraction/scripts/indian_worker_data/build_canonical_skill_catalogue.py` | PY | Pipeline Automation Scripts | 50,823 B | 813 | 813 | 0 | 0 | `26c6a28d77ae` |
| `datasets/informal_skill_extraction/scripts/indian_worker_data/build_language_vocabulary.py` | PY | Pipeline Automation Scripts | 12,130 B | 141 | 141 | 0 | 0 | `67aeb6184d5d` |
| `datasets/informal_skill_extraction/scripts/indian_worker_data/build_occupation_knowledge_base.py` | PY | Pipeline Automation Scripts | 56,952 B | 862 | 862 | 0 | 0 | `76fb8a26beea` |
| `datasets/informal_skill_extraction/scripts/indian_worker_data/check_duplicate_records.py` | PY | Pipeline Automation Scripts | 4,494 B | 133 | 133 | 0 | 0 | `667c4d27eebb` |
| `datasets/informal_skill_extraction/scripts/indian_worker_data/collection_dashboard.py` | PY | Pipeline Automation Scripts | 86,836 B | 1861 | 1861 | 0 | 0 | `06e46cb207b6` |
| `datasets/informal_skill_extraction/scripts/indian_worker_data/download_public_sources.py` | PY | Pipeline Automation Scripts | 5,512 B | 138 | 138 | 0 | 0 | `e9dfe7795f26` |
| `datasets/informal_skill_extraction/scripts/indian_worker_data/extract_official_standards.py` | PY | Pipeline Automation Scripts | 6,988 B | 153 | 153 | 0 | 0 | `6ec3c94e414a` |
| `datasets/informal_skill_extraction/scripts/indian_worker_data/field_collection_tool.py` | PY | Pipeline Automation Scripts | 8,686 B | 218 | 218 | 0 | 0 | `cdcf5e74a6bd` |
| `datasets/informal_skill_extraction/scripts/indian_worker_data/generate_master_dataset_report.py` | PY | Pipeline Automation Scripts | 14,594 B | 258 | 258 | 0 | 0 | `26abc4309676` |
| `datasets/informal_skill_extraction/scripts/indian_worker_data/generate_master_inventory.py` | PY | Pipeline Automation Scripts | 11,270 B | 238 | 238 | 0 | 0 | `56ee59d09255` |
| `datasets/informal_skill_extraction/scripts/indian_worker_data/generate_pipeline_test_stubs.py` | PY | Pipeline Automation Scripts | 51,262 B | 1036 | 1036 | 0 | 0 | `d796a4c4fdb2` |
| `datasets/informal_skill_extraction/scripts/indian_worker_data/generate_synthetic_augmentation.py` | PY | Pipeline Automation Scripts | 35,370 B | 458 | 458 | 0 | 0 | `241e3b0e3948` |
| `datasets/informal_skill_extraction/scripts/indian_worker_data/launch_dashboard.py` | PY | Pipeline Automation Scripts | 1,625 B | 41 | 41 | 0 | 0 | `d2db01bdfb10` |
| `datasets/informal_skill_extraction/scripts/indian_worker_data/prepare_training_exports.py` | PY | Pipeline Automation Scripts | 16,388 B | 324 | 324 | 0 | 0 | `b546386ccfd0` |
| `datasets/informal_skill_extraction/scripts/indian_worker_data/preprocess_indian_worker_data.py` | PY | Pipeline Automation Scripts | 9,749 B | 217 | 217 | 0 | 0 | `6ce7f4bd87d2` |
| `datasets/informal_skill_extraction/scripts/indian_worker_data/test_field_collection_system.py` | PY | Pipeline Automation Scripts | 11,775 B | 283 | 283 | 0 | 0 | `1e51798ccfe2` |
| `datasets/informal_skill_extraction/scripts/indian_worker_data/validate_dataset.py` | PY | Pipeline Automation Scripts | 21,080 B | 461 | 461 | 0 | 0 | `b3bcb7ef5f85` |

## 4. Integrity and Partition Isolation Conclusion
The inventory confirms zero leakage across partition boundaries. Synthetic records carry explicit `source_type: synthetic_test_stub` metadata and are isolated. Genuine worker directories remain ready for field ingestion.
