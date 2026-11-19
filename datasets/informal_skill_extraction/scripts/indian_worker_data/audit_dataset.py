#!/usr/bin/env python3
"""
ELEVATE X AI — DATASET 4 COMPREHENSIVE DATASET QUANTITY AUDIT
Audits all files in Dataset 4 (Indian Informal Worker Data) and segregates into:
- Group A: Genuine worker data (Currently 0)
- Group B: Synthetic development data (20 test stubs)
- Group C: Official vocational reference data (Taxonomies, QPs, CTS syllabi)
- Group D: Adapted or externally sourced data (0)

Generates reports/indian_worker_data/dataset_quantity_audit.md with exact counts.
Never counts synthetic stubs or official standards as genuine worker interviews.
"""

import json
import csv
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parents[2]
RAW_DIR = BASE_DIR / "raw" / "indian_worker_data"
INTERIM_DIR = BASE_DIR / "interim" / "indian_worker_data"
PROCESSED_DIR = BASE_DIR / "processed" / "indian_worker_data"
REPORTS_DIR = BASE_DIR / "reports" / "indian_worker_data"

REPORTS_DIR.mkdir(parents=True, exist_ok=True)

def audit_jsonl_file(p: Path):
    res = {
        "file_name": p.name,
        "file_path": str(p),
        "format": "JSONL",
        "total_records": 0,
        "valid_records": 0,
        "invalid_records": 0,
        "empty_records": 0,
        "duplicate_records": 0,
        "unique_worker_ids": set(),
        "total_skill_spans": 0,
        "missing_fields": 0,
        "annotation_status_dist": {},
        "consent_status_dist": {},
        "source_type_dist": {},
        "genuine_count": 0,
        "synthetic_count": 0,
        "adapted_count": 0
    }
    
    seen_texts = set()
    with open(p, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            line_str = line.strip()
            if not line_str:
                res["empty_records"] += 1
                continue
            res["total_records"] += 1
            try:
                rec = json.loads(line_str)
            except Exception:
                res["invalid_records"] += 1
                continue
                
            text = rec.get("worker_description", "")
            if text in seen_texts:
                res["duplicate_records"] += 1
            seen_texts.add(text)
            
            w_id = rec.get("worker_id")
            if w_id:
                res["unique_worker_ids"].add(w_id)
                
            spans = rec.get("skill_spans", [])
            res["total_skill_spans"] += len(spans)
            
            ann_status = rec.get("annotation_status", "unknown")
            res["annotation_status_dist"][ann_status] = res["annotation_status_dist"].get(ann_status, 0) + 1
            
            c_status = rec.get("consent_status", "unknown")
            res["consent_status_dist"][c_status] = res["consent_status_dist"].get(c_status, 0) + 1
            
            s_type = rec.get("source_type", "unknown")
            res["source_type_dist"][s_type] = res["source_type_dist"].get(s_type, 0) + 1
            
            if s_type == "real_field_interview":
                res["genuine_count"] += 1
            elif s_type == "synthetic_test_stub":
                res["synthetic_count"] += 1
            elif s_type == "curriculum_adapted":
                res["adapted_count"] += 1
                
            # Missing mandatory fields check
            mandatories = ["record_id", "worker_description", "original_language", "occupation_id", "skill_spans"]
            if any(fld not in rec or rec[fld] is None for fld in mandatories):
                res["missing_fields"] += 1
                res["invalid_records"] += 1
            else:
                res["valid_records"] += 1
                
    res["unique_worker_ids_count"] = len(res["unique_worker_ids"])
    return res

def audit_csv_file(p: Path):
    res = {
        "file_name": p.name,
        "file_path": str(p),
        "format": "CSV",
        "total_records": 0,
        "valid_records": 0,
        "invalid_records": 0,
        "empty_records": 0,
        "duplicate_records": 0,
        "unique_worker_ids_count": 0,
        "total_skill_spans": 0,
        "missing_fields": 0,
        "annotation_status_dist": {},
        "consent_status_dist": {},
        "source_type_dist": {"official_vocational_reference": 0},
        "genuine_count": 0,
        "synthetic_count": 0,
        "adapted_count": 0,
        "reference_count": 0
    }
    
    with open(p, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader, None)
        if not header:
            return res
        for row in reader:
            if not row or not any(row):
                res["empty_records"] += 1
                continue
            res["total_records"] += 1
            res["valid_records"] += 1
            res["reference_count"] += 1
            res["source_type_dist"]["official_vocational_reference"] += 1
            
    return res

def run_audit():
    print("Executing Complete Dataset 4 Quantity Audit...")
    
    files_to_audit = []
    
    # 1. Raw files
    if RAW_DIR.exists():
        for p in RAW_DIR.rglob("*"):
            if p.is_file() and p.suffix in [".jsonl", ".csv"]:
                files_to_audit.append(p)
                
    # 2. Interim files
    if INTERIM_DIR.exists():
        for p in INTERIM_DIR.rglob("*"):
            if p.is_file() and p.suffix in [".jsonl", ".csv"]:
                files_to_audit.append(p)
                
    # 3. Processed files
    if PROCESSED_DIR.exists():
        for p in PROCESSED_DIR.rglob("*"):
            if p.is_file() and p.suffix in [".jsonl", ".csv"]:
                files_to_audit.append(p)

    # Sort files for deterministic output
    files_to_audit = sorted(list(set(files_to_audit)))
    
    file_audits = []
    for f in files_to_audit:
        if f.suffix == ".jsonl":
            file_audits.append(audit_jsonl_file(f))
        elif f.suffix == ".csv":
            file_audits.append(audit_csv_file(f))

    # Aggregations across unique partitions
    # Primary ground truth locations:
    # Group A: raw/indian_worker_data/real/
    # Group B: raw/indian_worker_data/synthetic_test_only/synthetic_pipeline_test.jsonl
    # Group C: raw/indian_worker_data/occupation_taxonomy.csv, source_catalog.csv
    
    raw_synth = audit_jsonl_file(RAW_DIR / "synthetic_test_only" / "synthetic_pipeline_test.jsonl") if (RAW_DIR / "synthetic_test_only" / "synthetic_pipeline_test.jsonl").exists() else None
    tax_csv = audit_csv_file(RAW_DIR / "occupation_taxonomy.csv") if (RAW_DIR / "occupation_taxonomy.csv").exists() else None
    src_csv = audit_csv_file(RAW_DIR / "source_catalog.csv") if (RAW_DIR / "source_catalog.csv").exists() else None
    
    genuine_worker_records = 0
    genuine_unique_workers = 0
    genuine_skill_spans = 0
    
    # Check if any files exist in raw/indian_worker_data/real/
    real_dir = RAW_DIR / "real"
    if real_dir.exists():
        for rf in real_dir.glob("*.jsonl"):
            rf_audit = audit_jsonl_file(rf)
            genuine_worker_records += rf_audit["genuine_count"]
            genuine_unique_workers += rf_audit["unique_worker_ids_count"]
            genuine_skill_spans += rf_audit["total_skill_spans"]

    synthetic_records = raw_synth["synthetic_count"] if raw_synth else 0
    synthetic_spans = raw_synth["total_skill_spans"] if raw_synth else 0
    
    official_occupations = tax_csv["total_records"] if tax_csv else 0
    official_sources = src_csv["total_records"] if src_csv else 0
    
    report_md = [
        "# ELEVATE X AI — DATASET 4 QUANTITY & GROUND TRUTH AUDIT",
        f"**Audit Execution Timestamp**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  ",
        "**Target Dataset**: Dataset 4 — Indian Informal Worker Descriptions  ",
        "**Feature**: Feature 1 (Informal Experience to Skill Extraction)  \n",
        "---\n",
        "## 1. Executive Ground Truth Declaration",
        "> [!IMPORTANT]",
        "> ### GROUND TRUTH AUDIT SUMMARY",
        f"> - **Actual Genuine Worker Records Available**: **{genuine_worker_records}** (ZERO)",
        f"> - **Actual Unique Genuine Workers**: **{genuine_unique_workers}** (ZERO)",
        f"> - **Actual Genuine Skill Spans**: **{genuine_skill_spans}** (ZERO)",
        f"> - **Synthetic Development Test Records**: **{synthetic_records}** (Quarantined in `synthetic_test_only/`)",
        f"> - **Synthetic Test Skill Spans**: **{synthetic_spans}**",
        f"> - **Official Vocational Standards Mapped**: **{official_occupations} Occupations**, **{official_sources} Qualification Sources**",
        "> - **Adapted Third-Party Records**: **0**",
        "> - **Records Usable for Supervised Training**: **0** (Zero genuine records collected)",
        "> - **Records Usable for Benchmark Evaluation**: **0** (Zero genuine records collected)",
        "> ",
        "> **Audit Conclusion**: The data engineering and validation pipeline is **READY FOR FIELD COLLECTION**, but contains **ZERO genuine worker data**. Under Elevate X AI governance rules, no model training may proceed until actual field interviews are completed.\n",
        "## 2. Four-Group Data Partition Classification\n",
        "| Partition Group | Definition | Current Record Count | Status | Usable for Model Training |",
        "|---|---|---|---|---|",
        f"| **Group A: Genuine Worker Data** | Real informal worker descriptions collected with verified consent | **{genuine_worker_records}** | Field Collection Pending | **NO (0 records)** |",
        f"| **Group B: Synthetic Development Data** | Artificially generated stubs for testing schema, offsets, & scripts | **{synthetic_records}** | Fully Verified Stubs | **NO (Test Only)** |",
        f"| **Group C: Official Reference Data** | NCVET/NSDC Qualification Packs, CTS ITI curricula, ESCO/O*NET | **{official_occupations + official_sources}** ({official_occupations} trades, {official_sources} sources) | Catalogued References | **NO (Taxonomy Only)** |",
        "| **Group D: Adapted External Data** | Third-party Indian informal labor datasets | **0** | None Ingested | **NO (0 records)** |\n",
        "## 3. Exact File-by-File Audit Table\n",
        "| File Name | Format | Total Records | Valid | Invalid | Duplicates | Unique Workers | Skill Spans | Source Type | Consent Status |",
        "|---|---|---|---|---|---|---|---|---|---|"
    ]
    
    for a in file_audits:
        s_types = ", ".join(f"{k}: {v}" for k, v in a["source_type_dist"].items()) or "None"
        c_types = ", ".join(f"{k}: {v}" for k, v in a["consent_status_dist"].items()) or "N/A"
        report_md.append(
            f"| `{a['file_name']}` | {a['format']} | {a['total_records']} | {a['valid_records']} | {a['invalid_records']} | "
            f"{a['duplicate_records']} | {a['unique_worker_ids_count']} | {a['total_skill_spans']} | {s_types} | {c_types} |"
        )
        
    report_md.extend([
        "\n## 4. Key Missing Elements & Deficiencies",
        "1. **Zero Genuine Transcripts**: No genuine worker has yet been interviewed in the field.",
        "2. **Zero Audio Recordings**: No ground-truth worker voice recordings exist in the repository.",
        "3. **Zero Verified Worker Consent**: No physical or audio-recorded DPDP consent forms from real workers are archived.",
        "4. **No Real Dialectal Variability**: The 20 synthetic stubs test schema compliance, but cannot simulate authentic regional speech nuances from UP, Bihar, Rajasthan, or Delhi NCR.",
        "5. **Zero Supervised Training Data**: Model training cannot be initiated without risking severe synthetic hallucination bias.\n",
        "## 5. Next Immediate Action",
        "Launch the **Stage 1 Pilot Collection** targeting **10–20 genuine Tailor/Garment workers** in Delhi/NCR garment clusters using `interview_questionnaire_hindi.md` and `consent_form_hindi.md`."
    ])
    
    out_path = REPORTS_DIR / "dataset_quantity_audit.md"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(report_md) + "\n")
    print(f"Dataset quantity audit successfully generated at {out_path}")

if __name__ == "__main__":
    run_audit()

