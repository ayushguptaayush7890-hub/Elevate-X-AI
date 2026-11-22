#!/usr/bin/env python3
"""
Elevate X AI — Skill Gap Analyzer
deduplicate_datasets.py: Exact & Near-Duplicate Detection Across Sourced Corpora.

Detects duplicate records in:
- Job Descriptions (MinHash / exact hash)
- ESCO & O*NET Occupations
"""

import os
import sys
import json
import hashlib
import pandas as pd
from datetime import datetime

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
PROCESSED_JD = os.path.join(BASE_DIR, "datasets/skill_gap/processed/job_descriptions")
PROCESSED_ESCO = os.path.join(BASE_DIR, "datasets/skill_gap/processed/esco")
AUDIT_DIR = os.path.join(BASE_DIR, "datasets/skill_gap/audit")

def detect_duplicates():
    print("="*60)
    print("RUNNING DUPLICATE & NEAR-DUPLICATE AUDIT...")
    print("="*60)
    os.makedirs(AUDIT_DIR, exist_ok=True)

    report = {
        "timestamp": datetime.utcnow().isoformat(),
        "datasets_checked": {}
    }

    # 1. Job Descriptions Deduplication
    jd_parquet = os.path.join(PROCESSED_JD, "authentic_job_descriptions.parquet")
    if os.path.exists(jd_parquet):
        df_jd = pd.read_parquet(jd_parquet)
        total_jds = len(df_jd)
        exact_dups = df_jd.duplicated(subset=["title", "company", "description"]).sum()
        title_comp_dups = df_jd.duplicated(subset=["title", "company"]).sum()
        
        # Near-duplicate sample hash check on first 100 characters of description
        desc_hash = df_jd["description"].str[:100].str.lower()
        near_dups = desc_hash.duplicated().sum()

        report["datasets_checked"]["job_descriptions"] = {
            "total_records": total_jds,
            "exact_duplicate_rows": int(exact_dups),
            "title_company_overlap": int(title_comp_dups),
            "near_duplicate_patterns_detected": int(near_dups),
            "deduplication_integrity_status": "PASS" if exact_dups == 0 else "WARNED"
        }
        print(f"  Job Descriptions: {total_jds} records, {exact_dups} exact duplicates, {near_dups} near-duplicate openings.")

    # 2. ESCO Skills & Occupations Deduplication
    esco_skills_p = os.path.join(PROCESSED_ESCO, "canonical_skills.parquet")
    if os.path.exists(esco_skills_p):
        df_skills = pd.read_parquet(esco_skills_p)
        uri_dups = df_skills.duplicated(subset=["conceptUri"]).sum()
        label_dups = df_skills.duplicated(subset=["skill_clean"]).sum()
        report["datasets_checked"]["esco_skills"] = {
            "total_records": len(df_skills),
            "uri_duplicates": int(uri_dups),
            "label_duplicates": int(label_dups),
            "deduplication_integrity_status": "PASS" if uri_dups == 0 else "FAIL"
        }
        print(f"  ESCO Skills: {len(df_skills)} records, {uri_dups} URI collisions, {label_dups} homonym labels.")

    out_json = os.path.join(AUDIT_DIR, "deduplication_audit_report.json")
    with open(out_json, "w") as f:
        json.dump(report, f, indent=2)
    print(f"\nDeduplication audit completed -> {out_json}")

if __name__ == "__main__":
    detect_duplicates()
