"""
Script 5: preprocess_esco.py
Processes authentic ESCO v1.2.1 datasets:
- occupations_en.csv
- skills_en.csv
- occupationSkillRelations_en.csv
Generates canonical:
- processed/occupations/esco_occupations.parquet
- processed/skills/esco_skills.parquet
- processed/occupation_skill_graph/esco_relations.parquet
"""

import sys
import pandas as pd
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parents[3]
RAW_DIR = BASE_DIR / "datasets" / "career_transition" / "raw" / "esco"
PROC_DIR = BASE_DIR / "datasets" / "career_transition" / "processed"


def main():
    print("=" * 80)
    print("PREPROCESS ESCO v1.2.1")
    print("=" * 80)

    # 1. Occupations
    occ_file = RAW_DIR / "occupations_en.csv"
    print(f"Reading {occ_file.name}...")
    df_occ = pd.read_csv(occ_file)
    print(f"  Raw ESCO occupations: {len(df_occ)}")

    # Keep relevant fields
    df_occ = df_occ[[
        "conceptUri", "preferredLabel", "altLabels", "description",
        "iscoGroup", "code"
    ]].rename(columns={
        "conceptUri": "esco_occupation_uri",
        "preferredLabel": "occupation_title",
        "altLabels": "alternative_titles",
        "iscoGroup": "isco_group",
        "code": "esco_code"
    })
    df_occ["source"] = "ESCO v1.2.1"
    df_occ["occupation_title"] = df_occ["occupation_title"].astype(str).str.strip()

    # 2. Skills
    skills_file = RAW_DIR / "skills_en.csv"
    print(f"Reading {skills_file.name}...")
    df_skills = pd.read_csv(skills_file)
    print(f"  Raw ESCO skills: {len(df_skills)}")

    df_skills = df_skills[[
        "conceptUri", "skillType", "preferredLabel", "altLabels", "description"
    ]].rename(columns={
        "conceptUri": "esco_skill_uri",
        "skillType": "skill_type",
        "preferredLabel": "skill_name",
        "altLabels": "alternative_labels"
    })
    df_skills["source"] = "ESCO v1.2.1"
    df_skills["skill_name"] = df_skills["skill_name"].astype(str).str.strip()

    # 3. Relations
    rel_file = RAW_DIR / "occupationSkillRelations_en.csv"
    print(f"Reading {rel_file.name}...")
    df_rel = pd.read_csv(rel_file)
    print(f"  Raw relations: {len(df_rel)}")

    df_rel = df_rel[[
        "occupationUri", "relationType", "skillUri"
    ]].rename(columns={
        "occupationUri": "esco_occupation_uri",
        "relationType": "relation_type",  # essential or optional
        "skillUri": "esco_skill_uri"
    })

    # Save processed files
    (PROC_DIR / "occupations").mkdir(parents=True, exist_ok=True)
    (PROC_DIR / "skills").mkdir(parents=True, exist_ok=True)
    (PROC_DIR / "occupation_skill_graph").mkdir(parents=True, exist_ok=True)

    occ_out = PROC_DIR / "occupations" / "esco_occupations.parquet"
    skills_out = PROC_DIR / "skills" / "esco_skills.parquet"
    rel_out = PROC_DIR / "occupation_skill_graph" / "esco_relations.parquet"

    df_occ.to_parquet(occ_out, index=False)
    df_skills.to_parquet(skills_out, index=False)
    df_rel.to_parquet(rel_out, index=False)

    print(f"\n[SUCCESS] Saved ESCO processed parquets:")
    print(f"  Occupations: {len(df_occ)} records -> {occ_out.relative_to(BASE_DIR)}")
    print(f"  Skills:      {len(df_skills)} records -> {skills_out.relative_to(BASE_DIR)}")
    print(f"  Relations:   {len(df_rel)} records -> {rel_out.relative_to(BASE_DIR)}")


if __name__ == "__main__":
    main()
