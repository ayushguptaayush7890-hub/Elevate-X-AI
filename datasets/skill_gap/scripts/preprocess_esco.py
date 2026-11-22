#!/usr/bin/env python3
"""
Elevate X AI — Skill Gap Analyzer
preprocess_esco.py: Normalize and Structure Official ESCO Datasets.

Transforms:
- skills_en.csv -> canonical_skills.parquet
- occupations_en.csv -> canonical_occupations.parquet
- occupationSkillRelations_en.csv -> occupation_skill_profiles.json
"""

import os
import sys
import json
import re
import pandas as pd
from datetime import datetime

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
RAW_ESCO = os.path.join(BASE_DIR, "datasets/skill_gap/raw/esco")
PROCESSED_ESCO = os.path.join(BASE_DIR, "datasets/skill_gap/processed/esco")
INTERIM_DIR = os.path.join(BASE_DIR, "datasets/skill_gap/interim")

def clean_text(text: str) -> str:
    if not isinstance(text, str):
        return ""
    text = re.sub(r"\s+", " ", text).strip()
    return text

def preprocess_esco():
    print("="*60)
    print("PREPROCESSING ESCO V1.1.1 DATASETS...")
    print("="*60)
    os.makedirs(PROCESSED_ESCO, exist_ok=True)
    os.makedirs(INTERIM_DIR, exist_ok=True)

    # 1. Process Skills
    skills_csv = os.path.join(RAW_ESCO, "skills_en.csv")
    print(f"Reading {skills_csv}...")
    df_skills = pd.read_csv(skills_csv, low_memory=False)
    print(f"  Raw Skills Count: {len(df_skills)}")

    # Clean and standardize columns
    df_skills["preferredLabel"] = df_skills["preferredLabel"].apply(clean_text)
    df_skills["skill_clean"] = df_skills["preferredLabel"].str.lower()
    df_skills["description"] = df_skills["description"].fillna("").apply(clean_text)
    df_skills["altLabels"] = df_skills["altLabels"].fillna("")
    
    # Filter valid active skills
    df_skills_clean = df_skills[df_skills["preferredLabel"].str.len() > 1].drop_duplicates(subset=["conceptUri"]).copy()
    
    # Save canonical skills
    skills_parquet = os.path.join(PROCESSED_ESCO, "canonical_skills.parquet")
    skills_json = os.path.join(PROCESSED_ESCO, "canonical_skills.json")
    df_skills_clean[["conceptUri", "skillType", "reuseLevel", "preferredLabel", "skill_clean", "altLabels", "description"]].to_parquet(skills_parquet, index=False)
    print(f"  Processed Canonical Skills: {len(df_skills_clean)} -> {skills_parquet}")

    # 2. Process Occupations
    occ_csv = os.path.join(RAW_ESCO, "occupations_en.csv")
    print(f"\nReading {occ_csv}...")
    df_occ = pd.read_csv(occ_csv, low_memory=False)
    print(f"  Raw Occupations Count: {len(df_occ)}")

    df_occ["preferredLabel"] = df_occ["preferredLabel"].apply(clean_text)
    df_occ["occupation_clean"] = df_occ["preferredLabel"].str.lower()
    df_occ["description"] = df_occ["description"].fillna("").apply(clean_text)
    df_occ["altLabels"] = df_occ["altLabels"].fillna("")
    df_occ["iscoGroup"] = df_occ["iscoGroup"].astype(str).str.strip()

    df_occ_clean = df_occ[df_occ["preferredLabel"].str.len() > 1].drop_duplicates(subset=["conceptUri"]).copy()
    occ_parquet = os.path.join(PROCESSED_ESCO, "canonical_occupations.parquet")
    df_occ_clean[["conceptUri", "iscoGroup", "preferredLabel", "occupation_clean", "altLabels", "description"]].to_parquet(occ_parquet, index=False)
    print(f"  Processed Canonical Occupations: {len(df_occ_clean)} -> {occ_parquet}")

    # 3. Process Occupation-Skill Relations
    rel_csv = os.path.join(RAW_ESCO, "occupationSkillRelations_en.csv")
    print(f"\nReading {rel_csv}...")
    df_rel = pd.read_csv(rel_csv, low_memory=False)
    print(f"  Raw Occupation-Skill Relations Count: {len(df_rel)}")

    # Merge labels for fast lookup
    skill_map = dict(zip(df_skills_clean["conceptUri"], df_skills_clean["preferredLabel"]))
    occ_map = dict(zip(df_occ_clean["conceptUri"], df_occ_clean["preferredLabel"]))

    df_rel_clean = df_rel.dropna(subset=["occupationUri", "skillUri"]).copy()
    df_rel_clean["occupationTitle"] = df_rel_clean["occupationUri"].map(occ_map)
    df_rel_clean["skillTitle"] = df_rel_clean["skillUri"].map(skill_map)
    df_rel_clean = df_rel_clean.dropna(subset=["occupationTitle", "skillTitle"]).copy()

    # Build occupation skill profile dictionary
    occ_profiles = {}
    for occ_title, group in df_rel_clean.groupby("occupationTitle"):
        essential = group[group["relationType"] == "essential"]["skillTitle"].tolist()
        optional = group[group["relationType"] == "optional"]["skillTitle"].tolist()
        occ_profiles[occ_title] = {
            "occupation": occ_title,
            "essential_skills": essential,
            "optional_skills": optional,
            "total_competencies": len(essential) + len(optional)
        }

    profiles_json = os.path.join(PROCESSED_ESCO, "occupation_skill_profiles.json")
    with open(profiles_json, "w") as f:
        json.dump(occ_profiles, f, indent=2)
    print(f"  Processed Occupation Profiles: {len(occ_profiles)} occupations with structured skill maps -> {profiles_json}")

    # Save summary report
    summary = {
        "dataset": "ESCO v1.1.1",
        "processed_at": datetime.utcnow().isoformat(),
        "total_canonical_skills": len(df_skills_clean),
        "total_canonical_occupations": len(df_occ_clean),
        "total_verified_relationships": len(df_rel_clean),
        "mapped_occupations_with_profiles": len(occ_profiles)
    }
    with open(os.path.join(PROCESSED_ESCO, "esco_preprocessing_summary.json"), "w") as f:
        json.dump(summary, f, indent=2)
    print("\nESCO Preprocessing completed successfully!")

if __name__ == "__main__":
    preprocess_esco()
