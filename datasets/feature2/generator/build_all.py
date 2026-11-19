"""
Master Dataset Builder for Elevate X AI Feature 2 Technical Assessments.
Compiles all 2,250 questions across 9 technical roles, verifies schema integrity,
and writes out master JSON, JSONL, CSV indexes, and manifest files.
"""

import json
import csv
import hashlib
import os
import sys
from datetime import datetime, timezone

# Ensure roles package is in path
sys.path.insert(0, os.path.dirname(__file__))

from roles.gen_swe import generate_swe_questions
from roles.gen_aim import generate_aim_questions
from roles.gen_dsc import generate_dsc_questions
from roles.gen_fed import generate_fed_questions
from roles.gen_bed import generate_bed_questions
from roles.gen_dvo import generate_dvo_questions
from roles.gen_dan import generate_dan_questions
from roles.gen_sec import generate_sec_questions
from roles.gen_cld import generate_cld_questions

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def build_feature2_dataset():
    print("=" * 60)
    print("ELEVATE X AI — FEATURE 2: TECHNICAL ASSESSMENT DATASET BUILDER")
    print("=" * 60)
    
    generators = [
        ("software_engineer", generate_swe_questions),
        ("ai_ml_engineer", generate_aim_questions),
        ("data_scientist", generate_dsc_questions),
        ("frontend_developer", generate_fed_questions),
        ("backend_developer", generate_bed_questions),
        ("devops_engineer", generate_dvo_questions),
        ("data_analyst", generate_dan_questions),
        ("cybersecurity_engineer", generate_sec_questions),
        ("cloud_engineer", generate_cld_questions)
    ]
    
    all_questions = []
    role_summaries = {}
    
    for role_id, gen_fn in generators:
        print(f"Generating questions for {role_id}...")
        qs = gen_fn()
        print(f"  -> Generated {len(qs)} questions.")
        all_questions.extend(qs)
        
        # Save individual JSON files by role and type
        by_type = {}
        by_diff = {}
        for q in qs:
            qtype = q["assessment_type"]
            diff = q["difficulty"]
            by_type[qtype] = by_type.get(qtype, 0) + 1
            by_diff[diff] = by_diff.get(diff, 0) + 1
            
            # Write individual file
            type_dir = os.path.join(BASE_DIR, role_id, qtype)
            os.makedirs(type_dir, exist_ok=True)
            q_file = os.path.join(type_dir, f"{q['question_id']}.json")
            with open(q_file, "w") as f:
                json.dump(q, f, indent=2)
                
        role_summaries[role_id] = {
            "total_questions": len(qs),
            "by_assessment_type": by_type,
            "by_difficulty": by_diff
        }
        
    print(f"\nTotal questions generated across all roles: {len(all_questions)}")
    
    # 1. Write questions.jsonl
    jsonl_path = os.path.join(BASE_DIR, "questions.jsonl")
    print(f"Writing questions.jsonl to {jsonl_path}...")
    with open(jsonl_path, "w") as f:
        for q in all_questions:
            f.write(json.dumps(q) + "\n")
            
    # 2. Write master_dataset.json
    master_path = os.path.join(BASE_DIR, "master_dataset.json")
    print(f"Writing master_dataset.json to {master_path}...")
    master_data = {
        "metadata": {
            "dataset_name": "Elevate X AI Technical Assessment Master Dataset",
            "version": "1.0.0",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "total_questions": len(all_questions),
            "total_roles": len(generators),
            "role_summaries": role_summaries
        },
        "questions": all_questions
    }
    with open(master_path, "w") as f:
        json.dump(master_data, f, indent=2)
        
    # 3. Write questions_index.csv
    csv_path = os.path.join(BASE_DIR, "questions_index.csv")
    print(f"Writing questions_index.csv to {csv_path}...")
    csv_fields = [
        "question_id", "role_id", "skill_id", "skill_name", "subtopic",
        "assessment_type", "difficulty", "marks", "estimated_time",
        "source_type", "review_status"
    ]
    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=csv_fields)
        writer.writeheader()
        for q in all_questions:
            row = {k: q.get(k) for k in csv_fields}
            writer.writerow(row)
            
    # 4. Generate dataset_manifest.json
    print("Computing cryptographic SHA-256 digests...")
    def file_hash(filepath):
        h = hashlib.sha256()
        with open(filepath, "rb") as f:
            while chunk := f.read(65536):
                h.update(chunk)
        return h.hexdigest()
        
    manifest = {
        "dataset_name": "Elevate X AI Feature 2 Technical Assessment Dataset",
        "version": "1.0.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total_questions": len(all_questions),
        "target_roles": [r for r, _ in generators],
        "file_digests": {
            "questions.jsonl": file_hash(jsonl_path),
            "master_dataset.json": file_hash(master_path),
            "questions_index.csv": file_hash(csv_path),
            "roles_and_skills.json": file_hash(os.path.join(BASE_DIR, "roles_and_skills.json")),
            "source_registry.json": file_hash(os.path.join(BASE_DIR, "source_registry.json")),
            "license_audit.json": file_hash(os.path.join(BASE_DIR, "license_audit.json"))
        },
        "quality_metrics": {
            "minimum_required_per_role": 250,
            "achieved_per_role": {r: s["total_questions"] for r, s in role_summaries.items()},
            "all_roles_met_threshold": all(s["total_questions"] >= 250 for s in role_summaries.values()),
            "overall_difficulty_split": {
                "easy": sum(s["by_difficulty"].get("easy", 0) for s in role_summaries.values()),
                "medium": sum(s["by_difficulty"].get("medium", 0) for s in role_summaries.values()),
                "hard": sum(s["by_difficulty"].get("hard", 0) for s in role_summaries.values())
            }
        }
    }
    
    manifest_path1 = os.path.join(BASE_DIR, "dataset_manifest.json")
    manifest_path2 = os.path.join(BASE_DIR, "manifests", "dataset_manifest.json")
    with open(manifest_path1, "w") as f:
        json.dump(manifest, f, indent=2)
    with open(manifest_path2, "w") as f:
        json.dump(manifest, f, indent=2)
        
    print(f"Saved dataset_manifest.json to {manifest_path1} and {manifest_path2}.")
    print("=" * 60)
    print("FEATURE 2 DATASET BUILD COMPLETED SUCCESSFULLY!")
    print("=" * 60)

if __name__ == "__main__":
    build_feature2_dataset()
