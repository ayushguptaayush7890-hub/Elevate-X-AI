#!/usr/bin/env python3
"""
ELEVATE X AI — LANGUAGE & REGIONAL DIVERSITY AUDIT ENGINE
Audits linguistic coverage across:
- Languages: Hindi, Hinglish, English, Multilingual
- Scripts: Devanagari, Latin (Roman), Mixed
- Regions: Delhi NCR, Uttar Pradesh, Rajasthan, Maharashtra, etc.
- 10 Target Occupations

Outputs:
reports/indian_worker_data/language_diversity_audit.csv
"""

import json
import csv
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parents[2]
RAW_DIR = BASE_DIR / "raw" / "indian_worker_data"
SYNTHETIC_PATH = RAW_DIR / "synthetic_test_only" / "synthetic_pipeline_test.jsonl"
REAL_DIR = RAW_DIR / "real"
REPORTS_DIR = BASE_DIR / "reports" / "indian_worker_data"

REPORTS_DIR.mkdir(parents=True, exist_ok=True)

TARGET_OCCUPATIONS = [
    ("TRD-01", "Tailor and Garment Worker"),
    ("TRD-02", "Electrician"),
    ("TRD-03", "Plumber"),
    ("TRD-04", "Motor Mechanic"),
    ("TRD-05", "Carpenter"),
    ("TRD-06", "Welder"),
    ("TRD-07", "Mason / Raj Mistri"),
    ("TRD-08", "Painter"),
    ("TRD-09", "Agriculture and Irrigation Worker"),
    ("TRD-10", "Mobile Repair Technician")
]

LANG_COMBINATIONS = [
    ("hindi", "devanagari"),
    ("hinglish", "latin"),
    ("english", "latin"),
    ("multilingual", "mixed")
]

def run_language_audit():
    print("Auditing language and regional diversity...")
    
    real_records = []
    if REAL_DIR.exists():
        for p in REAL_DIR.glob("*.jsonl"):
            with open(p, "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        real_records.append(json.loads(line))
                        
    synthetic_records = []
    if SYNTHETIC_PATH.exists():
        with open(SYNTHETIC_PATH, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    synthetic_records.append(json.loads(line))

    rows = []
    
    for occ_id, occ_name in TARGET_OCCUPATIONS:
        for lang, script in LANG_COMBINATIONS:
            # Check real records
            matching_real = [
                r for r in real_records 
                if r.get("occupation_id") == occ_id and r.get("original_language") == lang and r.get("script_type") == script
            ]
            
            # Check synthetic stubs
            matching_synth = [
                r for r in synthetic_records 
                if r.get("occupation_id") == occ_id and r.get("original_language") == lang and r.get("script_type") == script
            ]
            
            genuine_count = len(matching_real)
            unique_workers = len(set(r.get("worker_id") for r in matching_real if r.get("worker_id")))
            genuine_spans = sum(len(r.get("skill_spans", [])) for r in matching_real)
            synth_count = len(matching_synth)
            synth_spans = sum(len(r.get("skill_spans", [])) for r in matching_synth)
            
            # Region evaluation
            regions_covered = list(set(r.get("region") for r in matching_real if r.get("region")))
            reg_str = ", ".join(regions_covered) if regions_covered else "None (Field Pending)"
            
            # Missing coverage
            if genuine_count == 0:
                missing_str = "Critical Deficit: 0 Genuine Records"
            elif genuine_count < 10:
                missing_str = "Pilot Incomplete: Need More Real Interviews"
            else:
                missing_str = "Adequate for Pilot"

            row = {
                "occupation_id": occ_id,
                "occupation_name": occ_name,
                "language": lang,
                "script": script,
                "genuine_record_count": genuine_count,
                "unique_genuine_workers": unique_workers,
                "genuine_skill_spans": genuine_spans,
                "synthetic_test_stub_count": synth_count,
                "synthetic_skill_spans": synth_spans,
                "regional_coverage": reg_str,
                "coverage_status": missing_str
            }
            rows.append(row)
            
    out_csv = REPORTS_DIR / "language_diversity_audit.csv"
    with open(out_csv, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"Language diversity audit written to {out_csv}")

if __name__ == "__main__":
    run_language_audit()

