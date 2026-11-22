#!/usr/bin/env python3
"""
Elevate X AI — Skill Gap Analyzer
preprocess_job_descriptions.py: Preprocess Authentic Job Descriptions.

Processes:
- recruitment_jds_english.parquet (lang-uk / MIT)
- shresth_jobs.csv (Shresth786 / MIT)
"""

import os
import sys
import json
import re
import pandas as pd
from datetime import datetime

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
RAW_JD = os.path.join(BASE_DIR, "datasets/skill_gap/raw/job_descriptions")
PROCESSED_JD = os.path.join(BASE_DIR, "datasets/skill_gap/processed/job_descriptions")

def clean_text(text: str) -> str:
    if not isinstance(text, str):
        return ""
    return re.sub(r"\s+", " ", text).strip()

def preprocess_jds():
    print("="*60)
    print("PREPROCESSING AUTHENTIC JOB DESCRIPTIONS...")
    print("="*60)
    os.makedirs(PROCESSED_JD, exist_ok=True)

    records = []

    # 1. Process Shresth786 Jobs (Categorized & Verified)
    shresth_csv = os.path.join(RAW_JD, "shresth_jobs.csv")
    if os.path.exists(shresth_csv):
        print(f"Reading {shresth_csv}...")
        df_shresth = pd.read_csv(shresth_csv, low_memory=False)
        print(f"  Raw Shresth Jobs: {len(df_shresth)}")
        for idx, row in df_shresth.iterrows():
            pos = clean_text(str(row.get("job_title", "")))
            desc = clean_text(str(row.get("job_description", "")))
            skills = clean_text(str(row.get("skills", "")))
            if pos and len(desc) > 30:
                records.append({
                    "id": f"shresth-{idx}",
                    "source": "Shresth786/job-resume-matching",
                    "license": "MIT",
                    "title": pos,
                    "company": clean_text(str(row.get("company_name", "Industry Employer"))),
                    "description": desc,
                    "extracted_skills": [s.strip() for s in skills.split(",") if s.strip()] if skills else []
                })

    # 2. Process lang-uk recruitment dataset sample (Authentic English JDs)
    lang_parquet = os.path.join(RAW_JD, "recruitment_jds_english.parquet")
    if os.path.exists(lang_parquet):
        print(f"Reading {lang_parquet} (sampling 5,000 diverse roles)...")
        df_lang = pd.read_parquet(lang_parquet)
        print(f"  Raw lang-uk Jobs: {len(df_lang)}")
        
        # Filter English, valid descriptions, sample up to 5,000 for local rapid semantic retrieval
        df_valid = df_lang[df_lang["Long Description"].str.len() > 100].drop_duplicates(subset=["Position", "Company Name"]).head(5000)
        
        for idx, row in df_valid.iterrows():
            pos = clean_text(str(row.get("Position", "")))
            desc = clean_text(str(row.get("Long Description", "")))
            comp = clean_text(str(row.get("Company Name", "Tech Enterprise")))
            kw = clean_text(str(row.get("Primary Keyword", "")))
            if pos and len(desc) > 30:
                records.append({
                    "id": f"languk-{idx}",
                    "source": "lang-uk/recruitment-dataset-job-descriptions-english",
                    "license": "MIT",
                    "title": pos,
                    "company": comp,
                    "description": desc,
                    "extracted_skills": [kw] if kw else []
                })

    print(f"\nTotal Unified Verified Job Descriptions: {len(records)}")
    df_unified = pd.DataFrame(records)
    
    # Save parquet and json sample
    out_parquet = os.path.join(PROCESSED_JD, "authentic_job_descriptions.parquet")
    df_unified.to_parquet(out_parquet, index=False)
    print(f"  Saved Parquet: {out_parquet}")

    # Save index for sample display in UI
    out_sample_json = os.path.join(PROCESSED_JD, "sample_job_descriptions.json")
    sample_records = records[:50]
    with open(out_sample_json, "w") as f:
        json.dump(sample_records, f, indent=2)
    print(f"  Saved Sample UI Index: {len(sample_records)} JDs -> {out_sample_json}")

    summary = {
        "dataset": "Unified Authentic Job Descriptions (lang-uk + Shresth786)",
        "processed_at": datetime.utcnow().isoformat(),
        "total_records": len(records),
        "license": "MIT",
        "distinct_titles": df_unified["title"].nunique(),
        "distinct_companies": df_unified["company"].nunique()
    }
    with open(os.path.join(PROCESSED_JD, "jd_preprocessing_summary.json"), "w") as f:
        json.dump(summary, f, indent=2)
    print("Job Descriptions Preprocessing completed successfully!")

if __name__ == "__main__":
    preprocess_jds()
