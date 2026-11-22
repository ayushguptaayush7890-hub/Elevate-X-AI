#!/usr/bin/env python3
"""
Elevate X AI — Skill Gap Analyzer
preprocess_onet.py: Normalize and Structure Official O*NET 31.0 Datasets.

Extracts & Cleans:
- Occupation Data.txt
- Skills.txt
- Knowledge.txt
- Abilities.txt
- Technology Skills.txt
- Work Activities.txt
- Job Zones.txt
"""

import os
import sys
import json
import re
import pandas as pd
from datetime import datetime

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
RAW_ONET = os.path.join(BASE_DIR, "datasets/skill_gap/raw/onet")
PROCESSED_ONET = os.path.join(BASE_DIR, "datasets/skill_gap/processed/onet")

def clean_text(text: str) -> str:
    if not isinstance(text, str):
        return ""
    return re.sub(r"\s+", " ", text).strip()

def preprocess_onet():
    print("="*60)
    print("PREPROCESSING O*NET 31.0 DATABASE TABLES...")
    print("="*60)
    os.makedirs(PROCESSED_ONET, exist_ok=True)

    # 1. Occupation Data
    occ_txt = os.path.join(RAW_ONET, "Occupation Data.txt")
    if not os.path.exists(occ_txt):
        print(f"Waiting for {occ_txt} to finish extraction...")
        return False
        
    print(f"Processing {occ_txt}...")
    df_occ = pd.read_csv(occ_txt, sep="\t", low_memory=False)
    df_occ["Title"] = df_occ["Title"].apply(clean_text)
    df_occ["Description"] = df_occ["Description"].fillna("").apply(clean_text)
    df_occ["title_clean"] = df_occ["Title"].str.lower()
    occ_parquet = os.path.join(PROCESSED_ONET, "onet_occupations.parquet")
    df_occ.to_parquet(occ_parquet, index=False)
    print(f"  Processed O*NET Occupations: {len(df_occ)} -> {occ_parquet}")

    # 2. Technology Skills
    tech_txt = os.path.join(RAW_ONET, "Technology Skills.txt")
    df_tech = pd.read_csv(tech_txt, sep="\t", low_memory=False) if os.path.exists(tech_txt) else pd.DataFrame()
    if not df_tech.empty:
        df_tech["Example"] = df_tech["Example"].apply(clean_text)
        df_tech["In Demand"] = df_tech["In Demand"].fillna("N")
        tech_parquet = os.path.join(PROCESSED_ONET, "onet_technology_skills.parquet")
        df_tech.to_parquet(tech_parquet, index=False)
        print(f"  Processed O*NET Tech Skills: {len(df_tech)} -> {tech_parquet}")

    # 3. Skills.txt (Importance & Level)
    skills_txt = os.path.join(RAW_ONET, "Skills.txt")
    df_skills = pd.read_csv(skills_txt, sep="\t", low_memory=False) if os.path.exists(skills_txt) else pd.DataFrame()
    if not df_skills.empty:
        # Filter Importance (IM) and Level (LV)
        skills_parquet = os.path.join(PROCESSED_ONET, "onet_skills_ratings.parquet")
        df_skills.to_parquet(skills_parquet, index=False)
        print(f"  Processed O*NET Skills Ratings: {len(df_skills)} -> {skills_parquet}")

    # 4. Knowledge.txt
    know_txt = os.path.join(RAW_ONET, "Knowledge.txt")
    df_know = pd.read_csv(know_txt, sep="\t", low_memory=False) if os.path.exists(know_txt) else pd.DataFrame()
    if not df_know.empty:
        know_parquet = os.path.join(PROCESSED_ONET, "onet_knowledge.parquet")
        df_know.to_parquet(know_parquet, index=False)
        print(f"  Processed O*NET Knowledge Ratings: {len(df_know)} -> {know_parquet}")

    # 5. Abilities.txt
    ab_txt = os.path.join(RAW_ONET, "Abilities.txt")
    df_ab = pd.read_csv(ab_txt, sep="\t", low_memory=False) if os.path.exists(ab_txt) else pd.DataFrame()
    if not df_ab.empty:
        ab_parquet = os.path.join(PROCESSED_ONET, "onet_abilities.parquet")
        df_ab.to_parquet(ab_parquet, index=False)
        print(f"  Processed O*NET Abilities Ratings: {len(df_ab)} -> {ab_parquet}")

    # Build Unified O*NET Profile Map for fast lookup by SOC code
    occ_profiles = {}
    tech_by_soc = {}
    if not df_tech.empty:
        for soc, group in df_tech.groupby("O*NET-SOC Code"):
            tech_by_soc[soc] = group["Example"].drop_duplicates().tolist()

    for _, row in df_occ.iterrows():
        soc = row["O*NET-SOC Code"]
        title = row["Title"]
        desc = row["Description"]
        occ_profiles[title] = {
            "soc_code": soc,
            "title": title,
            "description": desc,
            "technology_skills": tech_by_soc.get(soc, [])[:25]
        }

    profiles_json = os.path.join(PROCESSED_ONET, "onet_occupation_profiles.json")
    with open(profiles_json, "w") as f:
        json.dump(occ_profiles, f, indent=2)
    print(f"  Processed O*NET Profiles: {len(occ_profiles)} profiles -> {profiles_json}")

    summary = {
        "dataset": "O*NET 31.0 Database",
        "processed_at": datetime.utcnow().isoformat(),
        "total_occupations": len(df_occ),
        "total_tech_skills_records": len(df_tech),
        "total_skills_ratings": len(df_skills),
        "total_knowledge_records": len(df_know),
        "total_abilities_records": len(df_ab)
    }
    with open(os.path.join(PROCESSED_ONET, "onet_preprocessing_summary.json"), "w") as f:
        json.dump(summary, f, indent=2)
    print("O*NET Preprocessing completed successfully!")
    return True

if __name__ == "__main__":
    preprocess_onet()
