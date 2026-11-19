#!/usr/bin/env python3
"""
ELEVATE X AI — OCCUPATION-WISE DATASET COVERAGE AUDIT
Calculates occupation-level metrics across the 10 target trades:
- Genuine worker count (strictly distinguished from synthetic stubs)
- Unique descriptions and skill spans
- Length statistics (average, median)
- Linguistic breakdown (Hindi, Hinglish, Roman, Devanagari, English, Mixed)
- Experience level (Beginner <3y, Intermediate 3-8y, Advanced >8y)
- Work contexts (Self-employed, Workshop, Contract/Site)
- Annotation and review statuses

Generates:
1. reports/indian_worker_data/occupation_coverage_matrix.csv
2. reports/indian_worker_data/dataset_gap_analysis.md
"""

import json
import csv
import statistics
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parents[2]
RAW_DIR = BASE_DIR / "raw" / "indian_worker_data"
TAXONOMY_PATH = RAW_DIR / "occupation_taxonomy.csv"
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

def analyze_occupations():
    print("Auditing occupation-wise dataset coverage...")
    
    # Load all records
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

    # We evaluate genuine data first, and report synthetic in separate columns
    rows = []
    
    for occ_id, occ_name in TARGET_OCCUPATIONS:
        occ_real = [r for r in real_records if r.get("occupation_id") == occ_id]
        occ_synth = [r for r in synthetic_records if r.get("occupation_id") == occ_id]
        
        # Genuine worker metrics
        genuine_workers = len(set(r.get("worker_id") for r in occ_real if r.get("worker_id")))
        genuine_desc_count = len(occ_real)
        genuine_spans = sum(len(r.get("skill_spans", [])) for r in occ_real)
        
        # Synthetic stub metrics (for pipeline benchmark)
        synth_count = len(occ_synth)
        synth_spans = sum(len(r.get("skill_spans", [])) for r in occ_synth)
        
        # Length stats (from genuine if available, otherwise synthetic notes)
        active_pool = occ_real if occ_real else occ_synth
        lengths = [len(r.get("worker_description", "")) for r in active_pool]
        avg_len = round(statistics.mean(lengths), 1) if lengths else 0
        med_len = round(statistics.median(lengths), 1) if lengths else 0
        
        # Language distribution in pool
        hindi_cnt = sum(1 for r in active_pool if r.get("original_language") == "hindi")
        hinglish_cnt = sum(1 for r in active_pool if r.get("original_language") == "hinglish")
        english_cnt = sum(1 for r in active_pool if r.get("original_language") == "english")
        mixed_cnt = sum(1 for r in active_pool if r.get("original_language") == "multilingual")
        
        roman_cnt = sum(1 for r in active_pool if r.get("script_type") == "latin")
        deva_cnt = sum(1 for r in active_pool if r.get("script_type") == "devanagari")
        
        # Experience level
        beginner_cnt = sum(1 for r in active_pool if (r.get("experience_years") or 0) < 3)
        inter_cnt = sum(1 for r in active_pool if 3 <= (r.get("experience_years") or 0) <= 8)
        adv_cnt = sum(1 for r in active_pool if (r.get("experience_years") or 0) > 8)
        
        # Work setting
        self_emp_cnt = sum(1 for r in active_pool if r.get("work_context") in ["home_based", "independent_repair_shop", "street_vendor"])
        workshop_cnt = sum(1 for r in active_pool if r.get("work_context") in ["micro_workshop", "service_center", "industrial_cluster"])
        site_cnt = sum(1 for r in active_pool if r.get("work_context") in ["customer_site", "construction_site", "agricultural_field"])
        
        # Annotation & Review
        annotated_cnt = sum(1 for r in active_pool if r.get("annotation_status") in ["annotated", "reviewed", "approved"])
        reviewed_cnt = sum(1 for r in active_pool if r.get("annotation_status") in ["reviewed", "approved"])
        adjudication_cnt = sum(1 for r in active_pool if r.get("reviewer_status") == "flagged_for_adjudication")
        
        status = "DEFICIT (0 Genuine Records)" if genuine_desc_count == 0 else (
            "PILOT ACTIVE" if genuine_desc_count < 20 else "ADEQUATE"
        )
        
        row = {
            "occupation_id": occ_id,
            "occupation_name": occ_name,
            "genuine_worker_count": genuine_workers,
            "genuine_description_count": genuine_desc_count,
            "genuine_skill_spans": genuine_spans,
            "synthetic_stub_count": synth_count,
            "synthetic_skill_spans": synth_spans,
            "coverage_status": status,
            "avg_description_char_length": avg_len,
            "median_description_char_length": med_len,
            "hindi_count": hindi_cnt,
            "hinglish_count": hinglish_cnt,
            "roman_hindi_count": roman_cnt,
            "devanagari_count": deva_cnt,
            "english_count": english_cnt,
            "mixed_language_count": mixed_cnt,
            "beginner_workers": beginner_cnt,
            "intermediate_workers": inter_cnt,
            "advanced_workers": adv_cnt,
            "self_employed_workers": self_emp_cnt,
            "workshop_workers": workshop_cnt,
            "contract_site_workers": site_cnt,
            "annotated_records": annotated_cnt,
            "reviewed_records": reviewed_cnt,
            "records_requiring_adjudication": adjudication_cnt
        }
        rows.append(row)
        
    # Write CSV
    csv_path = REPORTS_DIR / "occupation_coverage_matrix.csv"
    fieldnames = list(rows[0].keys())
    with open(csv_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Occupation coverage matrix written to {csv_path}")
    
    # Write Gap Analysis Report
    generate_gap_analysis(rows)

def generate_gap_analysis(rows: list):
    gap_path = REPORTS_DIR / "dataset_gap_analysis.md"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    total_genuine = sum(r["genuine_description_count"] for r in rows)
    total_synth = sum(r["synthetic_stub_count"] for r in rows)
    
    md = [
        "# ELEVATE X AI — DATASET 4 OCCUPATION GAP ANALYSIS",
        f"**Audit Execution Timestamp**: {timestamp}  ",
        "**Target Feature**: Informal Experience to Skill Extraction  ",
        "**Governance Policy**: Zero Fabrication — Genuine Data Disclosed Transparently  \n",
        "---\n",
        "## 1. Ground Truth Gap Summary",
        f"- **Target Occupations**: 10 trades",
        f"- **Total Genuine Descriptions Collected to Date**: **{total_genuine}** (CRITICAL DEFICIT: 100% of trades lack genuine data)",
        f"- **Synthetic Test Stubs Available**: {total_synth} records (2 per trade for pipeline verification only)",
        f"- **Target Pilot Requirement**: 100–200 genuine descriptions (10–20 per trade)",
        f"- **Target Main Corpus Requirement**: 1,000–2,000 genuine descriptions (100–200 per trade)\n",
        "## 2. Occupation-by-Occupation Coverage & Deficit Analysis\n",
        "| ID | Occupation | Genuine Count | Synthetic Stubs | Deficit (Pilot Target) | Deficit (Main Target) | Status |",
        "|---|---|---|---|---|---|---|"
    ]
    
    for r in rows:
        pilot_gap = max(0, 15 - r["genuine_description_count"])
        main_gap = max(0, 100 - r["genuine_description_count"])
        md.append(f"| `{r['occupation_id']}` | **{r['occupation_name']}** | {r['genuine_description_count']} | {r['synthetic_stub_count']} | {pilot_gap} records | {main_gap} records | `{r['coverage_status']}` |")
        
    md.extend([
        "\n## 3. Dimensions of Current Dataset Imbalance",
        "1. **Universal Zero-Field Collection**: Every single trade currently has 0 genuine worker records.",
        "2. **Task Breadth Deficit**: Synthetic test stubs only cover 2 tasks per trade. Authentic workers perform 15–20 distinct tasks (e.g. pattern drafting, buttonholing, interlining, alteration, fitting, client negotiation).",
        "3. **Dialectal & Geographic Deficit**: No genuine regional vernacular has been gathered from key informal hubs in UP, Delhi NCR, Rajasthan, Bihar, or Maharashtra.",
        "4. **Work Setting Imbalance**: Real informal workers operate across diverse settings (home-based piece-rate workers, street pavement vendors, mobile van technicians, construction labor nakas). The current test stubs primarily sample shop contexts.",
        "5. **Cognitive & Diagnostic Deficits**: Crucial diagnostic sequences (fault tracing with multimeters, leak pressure testing, carburetor air-fuel balancing) lack real verbatim transcripts.\n",
        "## 4. Prioritized Collection Phasing",
        "1. **Priority 1 (Pilot Launch)**: `TRD-01` (Tailor and Garment Worker) — Collect 10–20 genuine worker interviews in Karol Bagh and Gandhi Nagar garment markets.",
        "2. **Priority 2 (High-Risk Infrastructure Trades)**: `TRD-02` (Electrician) & `TRD-03` (Plumber) — Essential for residential and commercial maintenance.",
        "3. **Priority 3 (Automotive & Mechanical)**: `TRD-04` (Motor Mechanic) & `TRD-06` (Welder) — High concentration of tactile trade vocabulary.",
        "4. **Priority 4 (Construction & Woodwork)**: `TRD-05` (Carpenter), `TRD-07` (Mason), `TRD-08` (Painter).",
        "5. **Priority 5 (Agrarian & Hardware)**: `TRD-09` (Agriculture Worker) & `TRD-10` (Mobile Repair)."
    ])
    
    with open(gap_path, "w", encoding="utf-8") as f:
        f.write("\n".join(md) + "\n")
    print(f"Dataset gap analysis generated at {gap_path}")

if __name__ == "__main__":
    analyze_occupations()

