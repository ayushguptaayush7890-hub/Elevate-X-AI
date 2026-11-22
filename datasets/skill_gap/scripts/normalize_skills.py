#!/usr/bin/env python3
"""
Elevate X AI — Skill Gap Analyzer
normalize_skills.py: Canonical Skill Normalization & Alias Mapping Engine.

Maps colloquial, informal, or noisy skill phrases to canonical ESCO / O*NET identifiers.
"""

import os
import sys
import json
import re
import pandas as pd
from datetime import datetime

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
PROCESSED_ESCO = os.path.join(BASE_DIR, "datasets/skill_gap/processed/esco")
INTERIM_DIR = os.path.join(BASE_DIR, "datasets/skill_gap/interim")

CANONICAL_ALIASES = {
    "py": "Python",
    "python3": "Python",
    "python programming": "Python",
    "cpp": "C++",
    "c plus plus": "C++",
    "js": "JavaScript",
    "ts": "TypeScript",
    "react": "React.js",
    "reactjs": "React.js",
    "node": "Node.js",
    "nodejs": "Node.js",
    "postgres": "PostgreSQL",
    "mysql db": "MySQL",
    "k8s": "Kubernetes",
    "docker container": "Docker",
    "ml": "Machine Learning",
    "dl": "Deep Learning",
    "ai": "Artificial Intelligence",
    "nlp": "Natural Language Processing",
    "cv": "Computer Vision",
    "llm": "Large Language Models",
    "rag": "Retrieval-Augmented Generation",
    "dsa": "Data Structures and Algorithms",
    "oop": "Object-Oriented Programming",
    "dbms": "Database Management Systems",
    "aws cloud": "Amazon Web Services (AWS)",
    "gcp": "Google Cloud Platform (GCP)",
    "azure": "Microsoft Azure"
}

def normalize_skill_name(raw_name: str) -> str:
    if not raw_name or not isinstance(raw_name, str):
        return ""
    clean = re.sub(r"[^\w\+\#\.\-\s]", "", raw_name).strip().lower()
    clean = re.sub(r"\s+", " ", clean)
    if clean in CANONICAL_ALIASES:
        return CANONICAL_ALIASES[clean]
    return raw_name.strip()

def build_skill_taxonomy():
    print("="*60)
    print("BUILDING UNIFIED CANONICAL SKILL TAXONOMY...")
    print("="*60)
    os.makedirs(INTERIM_DIR, exist_ok=True)

    skills_parquet = os.path.join(PROCESSED_ESCO, "canonical_skills.parquet")
    taxonomy = {}
    
    if os.path.exists(skills_parquet):
        df_esco_skills = pd.read_parquet(skills_parquet)
        print(f"Indexing {len(df_esco_skills)} ESCO skills into canonical taxonomy...")
        for _, row in df_esco_skills.iterrows():
            uri = row["conceptUri"]
            pref = row["preferredLabel"]
            alt = row.get("altLabels", "")
            taxonomy[pref.lower()] = {
                "canonical_name": pref,
                "esco_uri": uri,
                "skill_type": row.get("skillType", "competence"),
                "aliases": [a.strip() for a in alt.split("\n") if a.strip()][:5] if isinstance(alt, str) else []
            }
            
    # Inject canonical tech aliases
    for alias, canonical in CANONICAL_ALIASES.items():
        if alias not in taxonomy:
            taxonomy[alias] = {
                "canonical_name": canonical,
                "esco_uri": None,
                "skill_type": "technical_alias",
                "aliases": [canonical]
            }

    out_taxonomy = os.path.join(INTERIM_DIR, "canonical_skill_taxonomy.json")
    with open(out_taxonomy, "w") as f:
        json.dump(taxonomy, f, indent=2)

    print(f"Taxonomy built: {len(taxonomy)} distinct lookup keys saved to {out_taxonomy}")
    return taxonomy

if __name__ == "__main__":
    build_skill_taxonomy()
