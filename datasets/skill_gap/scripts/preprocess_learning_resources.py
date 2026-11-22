#!/usr/bin/env python3
"""
Elevate X AI — Skill Gap Analyzer
preprocess_learning_resources.py: Index and Structure Verified Learning Resources.

Builds inverted skill index for rapid, grounded educational recommendations.
"""

import os
import sys
import json
import urllib.parse
from datetime import datetime

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
RAW_RESOURCES = os.path.join(BASE_DIR, "datasets/skill_gap/raw/learning_resources")
PROCESSED_RESOURCES = os.path.join(BASE_DIR, "datasets/skill_gap/processed/learning_resources")

def preprocess_resources():
    print("="*60)
    print("PREPROCESSING & INDEXING VERIFIED LEARNING RESOURCES...")
    print("="*60)
    os.makedirs(PROCESSED_RESOURCES, exist_ok=True)

    catalog_path = os.path.join(RAW_RESOURCES, "learning_resources_catalog.json")
    if not os.path.exists(catalog_path):
        print(f"Catalog not found at {catalog_path}")
        return

    with open(catalog_path, "r") as f:
        catalog = json.load(f)

    # Inverted index: skill -> list of resources
    skill_index = {}
    verified_resources = []

    for item in catalog:
        # Validate URL structure
        parsed_url = urllib.parse.urlparse(item["url"])
        if not parsed_url.scheme or not parsed_url.netloc:
            print(f"  Warning: Invalid URL in resource: {item['title']}")
            continue

        verified_resources.append(item)
        for skill in item.get("skills", []):
            s_clean = skill.strip().lower()
            if s_clean not in skill_index:
                skill_index[s_clean] = []
            skill_index[s_clean].append(item["id"])

    # Output verified processed catalog & skill index
    out_catalog = os.path.join(PROCESSED_RESOURCES, "verified_learning_resources.json")
    with open(out_catalog, "w") as f:
        json.dump(verified_resources, f, indent=2)

    out_index = os.path.join(PROCESSED_RESOURCES, "skill_resource_index.json")
    with open(out_index, "w") as f:
        json.dump(skill_index, f, indent=2)

    summary = {
        "dataset": "Verified Official Learning Resource Catalog",
        "processed_at": datetime.utcnow().isoformat(),
        "total_verified_resources": len(verified_resources),
        "total_indexed_skills": len(skill_index),
        "providers": list(set(r["provider"] for r in verified_resources))
    }
    with open(os.path.join(PROCESSED_RESOURCES, "resources_preprocessing_summary.json"), "w") as f:
        json.dump(summary, f, indent=2)

    print(f"  Saved Verified Resources: {len(verified_resources)} -> {out_catalog}")
    print(f"  Saved Skill Inverted Index: {len(skill_index)} indexed skills -> {out_index}")
    print("Learning Resources Preprocessing completed successfully!")

if __name__ == "__main__":
    preprocess_resources()
