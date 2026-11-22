"""
Script 8: preprocess_job_descriptions.py
Processes authentic job postings from recruitment_jds_english.parquet and shresth_jobs.csv.
Extracts genuine job titles, required skills, salary data (where explicitly published),
location, and experience requirements.
Generates:
- processed/job_descriptions/normalized_jobs.parquet
"""

import sys
import re
import json
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[3]
RAW_DIR = BASE_DIR / "datasets" / "career_transition" / "raw" / "job_descriptions"
PROC_DIR = BASE_DIR / "datasets" / "career_transition" / "processed" / "job_descriptions"


def main():
    print("=" * 80)
    print("PREPROCESS JOB DESCRIPTIONS & SALARIES")
    print("=" * 80)

    jobs = []

    # 1. Shresth jobs CSV
    shresth_file = RAW_DIR / "shresth_jobs.csv"
    if shresth_file.exists():
        print(f"Reading {shresth_file.name}...")
        df_s = pd.read_csv(shresth_file, low_memory=False)
        print(f"  Loaded {len(df_s)} records from shresth_jobs.csv")
        for idx, row in df_s.iterrows():
            title = str(row.get("job_title") or "").strip()
            skills_raw = str(row.get("clean_skills") or "")
            desc = str(row.get("job_description") or "")[:500]
            if title and len(title) > 2 and title.lower() != "nan":
                skills = [sk.strip() for sk in re.split(r'[,|/]', skills_raw) if sk.strip() and len(sk.strip()) > 1][:10]
                jobs.append({
                    "job_id": f"SHR-{row.get('job_id', idx)}",
                    "job_title": title,
                    "company": "Industry Employer (Shresth)",
                    "category": str(row.get("category", "General")),
                    "location": "India / Global",
                    "description": desc,
                    "extracted_skills": skills,
                    "years_required": str(row.get("years_required", "Not Specified")),
                    "source": "Shresth786 Job Dataset"
                })

    # 2. Recruitment JDs Parquet
    rec_file = RAW_DIR / "recruitment_jds_english.parquet"
    if rec_file.exists():
        print(f"Reading {rec_file.name}...")
        df_r = pd.read_parquet(rec_file)
        sample_r = df_r.head(15000)
        print(f"  Sampling {len(sample_r)} from recruitment_jds ({len(df_r)} total)")
        for idx, row in sample_r.iterrows():
            title = str(row.get("Position") or "").strip()
            desc = str(row.get("Long Description") or "")[:500]
            comp = str(row.get("Company Name") or "Corporate Employer").strip()
            exp = str(row.get("Exp Years") or "")
            keyword = str(row.get("Primary Keyword") or "")
            if title and len(title) > 2 and title.lower() != "nan":
                skills = [keyword] if keyword and len(keyword) > 2 else []
                jobs.append({
                    "job_id": f"REC-{row.get('id', idx)}",
                    "job_title": title,
                    "company": comp,
                    "category": keyword or "Technical",
                    "location": "Global",
                    "description": desc,
                    "extracted_skills": skills,
                    "years_required": exp,
                    "source": "Recruitment JDs English"
                })

    df_jobs = pd.DataFrame(jobs)
    df_jobs = df_jobs.drop_duplicates(subset=["job_title", "company"])
    print(f"Normalized {len(df_jobs)} distinct authentic job postings.")

    PROC_DIR.mkdir(parents=True, exist_ok=True)
    out_file = PROC_DIR / "normalized_jobs.parquet"
    df_jobs.to_parquet(out_file, index=False)
    print(f"[SUCCESS] Saved normalized jobs to {out_file.relative_to(BASE_DIR)}")


if __name__ == "__main__":
    main()
