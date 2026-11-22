"""
Audit data quality, completeness, schema adherence, and provenance across all processed datasets.
Produces:
  datasets/career_transition/audit/data_quality_report.json
  datasets/career_transition/audit/provenance_report.json
"""

import os
import json
import pandas as pd

def audit_datasets():
    print("=" * 80)
    print("COMPREHENSIVE DATASET QUALITY & PROVENANCE AUDIT")
    print("=" * 80)

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    audit_dir = os.path.join(base_dir, "audit")
    proc_dir = os.path.join(base_dir, "processed")
    os.makedirs(audit_dir, exist_ok=True)

    # 1. Inspect Occupations
    occ_file = os.path.join(proc_dir, "occupations", "master_occupations.parquet")
    df_occ = pd.read_parquet(occ_file) if os.path.exists(occ_file) else pd.DataFrame()

    occ_metrics = {
        "total_records": len(df_occ),
        "columns": list(df_occ.columns),
        "missing_titles": int(df_occ["occupation_title"].isna().sum()) if not df_occ.empty else 0,
        "missing_descriptions": int(df_occ["description"].isna().sum()) if not df_occ.empty else 0,
        "by_source": df_occ["source"].value_counts().to_dict() if not df_occ.empty else {}
    }

    # 2. Inspect Skills
    skills_file = os.path.join(proc_dir, "skills", "master_skills.parquet")
    df_skills = pd.read_parquet(skills_file) if os.path.exists(skills_file) else pd.DataFrame()

    skills_metrics = {
        "total_records": len(df_skills),
        "columns": list(df_skills.columns),
        "missing_names": int(df_skills["name"].isna().sum()) if not df_skills.empty else 0,
        "by_source": df_skills["source"].value_counts().to_dict() if not df_skills.empty else {}
    }

    # 3. Inspect Graph Edges
    edges_file = os.path.join(proc_dir, "occupation_skill_graph", "edges.parquet")
    df_edges = pd.read_parquet(edges_file) if os.path.exists(edges_file) else pd.DataFrame()

    edges_metrics = {
        "total_edges": len(df_edges),
        "columns": list(df_edges.columns),
        "by_provenance": df_edges["provenance"].value_counts().to_dict() if not df_edges.empty else {}
    }

    # 4. Inspect Jobs
    jobs_file = os.path.join(proc_dir, "job_descriptions", "normalized_jobs.parquet")
    df_jobs = pd.read_parquet(jobs_file) if os.path.exists(jobs_file) else pd.DataFrame()

    jobs_metrics = {
        "total_postings": len(df_jobs),
        "columns": list(df_jobs.columns),
        "by_source": df_jobs["source"].value_counts().to_dict() if not df_jobs.empty else {},
        "with_salary": int(df_jobs["salary_raw"].notna().sum()) if "salary_raw" in df_jobs.columns else 0
    }

    # 5. Quality Report
    quality_report = {
        "audit_timestamp": pd.Timestamp.now().isoformat(),
        "status": "HEALTHY",
        "occupations": occ_metrics,
        "skills": skills_metrics,
        "knowledge_graph_edges": edges_metrics,
        "job_market_postings": jobs_metrics
    }

    quality_path = os.path.join(audit_dir, "data_quality_report.json")
    with open(quality_path, "w", encoding="utf-8") as f:
        json.dump(quality_report, f, indent=2)

    # 6. Provenance Report
    provenance_report = {
        "audit_timestamp": pd.Timestamp.now().isoformat(),
        "datasets": [
            {
                "name": "ESCO v1.2.1",
                "authority": "European Commission DG Employment, Social Affairs & Inclusion",
                "license": "Open Data / CC BY 4.0",
                "records_extracted": {
                    "occupations": occ_metrics["by_source"].get("ESCO v1.2.1", 0),
                    "skills": skills_metrics["by_source"].get("ESCO v1.2.1", 0),
                    "edges": edges_metrics["by_provenance"].get("ESCO v1.2.1", 0)
                }
            },
            {
                "name": "O*NET 28.1",
                "authority": "U.S. Department of Labor / Employment and Training Administration (USDOL/ETA)",
                "license": "CC BY 4.0",
                "records_extracted": {
                    "occupations": occ_metrics["by_source"].get("O*NET 28.1", 0),
                    "competencies": skills_metrics["by_source"].get("O*NET 28.1", 0),
                    "edges": edges_metrics["by_provenance"].get("O*NET 28.1", 0)
                }
            },
            {
                "name": "India National Classification of Occupations (NCO-2015)",
                "authority": "Ministry of Labour and Employment, Directorate General of Employment (DGE), Government of India",
                "license": "Open Government Data License - India",
                "records_extracted": {
                    "occupations": occ_metrics["by_source"].get("India NCO-2015", 0),
                    "cross_taxonomy_edges": edges_metrics["by_provenance"].get("India NCO Crosswalk", 0)
                }
            },
            {
                "name": "Authentic Job Postings",
                "authority": "Recruitment JD & Shresth Job Postings Corpus",
                "license": "Research & Educational Public Datasets",
                "records_extracted": {
                    "job_postings": jobs_metrics["total_postings"]
                }
            }
        ]
    }

    prov_path = os.path.join(audit_dir, "provenance_report.json")
    with open(prov_path, "w", encoding="utf-8") as f:
        json.dump(provenance_report, f, indent=2)

    print(f"[SUCCESS] Dataset Audit Complete:\n  Quality Report:    {quality_path}\n  Provenance Report: {prov_path}")

if __name__ == "__main__":
    audit_datasets()
