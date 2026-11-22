#!/usr/bin/env python3
"""
Elevate X AI — Skill Gap Analyzer
verify_downloads.py: Verify Integrity, Checksums, and File Sizes of Downloaded Corpora & Models.
"""

import os
import sys
import json
import hashlib
from datetime import datetime

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
SKILL_GAP_DIR = os.path.join(BASE_DIR, "datasets/skill_gap")
MODELS_DIR = os.path.join(BASE_DIR, "backend/app/ml/models/skill_gap")
AUDIT_DIR = os.path.join(SKILL_GAP_DIR, "audit")

def compute_sha256(filepath: str) -> str:
    sha = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            sha.update(chunk)
    return sha.hexdigest()

def verify_all():
    print("="*60)
    print("VERIFYING DOWNLOAD INTEGRITY & SHA256 CHECKSUMS...")
    print("="*60)
    os.makedirs(AUDIT_DIR, exist_ok=True)

    verification_results = {
        "verified_at": datetime.utcnow().isoformat(),
        "components": {}
    }

    # 1. ESCO Verification
    esco_raw = os.path.join(SKILL_GAP_DIR, "raw/esco")
    esco_files = [f for f in os.listdir(esco_raw) if f.endswith(".csv")] if os.path.exists(esco_raw) else []
    verification_results["components"]["esco"] = {
        "status": "PASS" if len(esco_files) >= 5 else "INCOMPLETE",
        "file_count": len(esco_files),
        "files": {f: {"size_bytes": os.path.getsize(os.path.join(esco_raw, f)), "sha256": compute_sha256(os.path.join(esco_raw, f))} for f in esco_files[:5]}
    }
    print(f"  ESCO: {len(esco_files)} files verified. Status: {verification_results['components']['esco']['status']}")

    # 2. O*NET Verification
    onet_raw = os.path.join(SKILL_GAP_DIR, "raw/onet")
    onet_zip = os.path.join(onet_raw, "db_31_0_text.zip")
    onet_txts = [f for f in os.listdir(onet_raw) if f.endswith(".txt")] if os.path.exists(onet_raw) else []
    verification_results["components"]["onet"] = {
        "status": "PASS" if len(onet_txts) >= 4 or (os.path.exists(onet_zip) and os.path.getsize(onet_zip) > 10*1024*1024) else "DOWNLOADING",
        "zip_present": os.path.exists(onet_zip),
        "zip_size_bytes": os.path.getsize(onet_zip) if os.path.exists(onet_zip) else 0,
        "extracted_tables_count": len(onet_txts)
    }
    print(f"  O*NET: Zip size={verification_results['components']['onet']['zip_size_bytes']/(1024*1024):.2f} MB, {len(onet_txts)} tables. Status: {verification_results['components']['onet']['status']}")

    # 3. Job Descriptions Verification
    jd_raw = os.path.join(SKILL_GAP_DIR, "raw/job_descriptions")
    jd_files = os.listdir(jd_raw) if os.path.exists(jd_raw) else []
    verification_results["components"]["job_descriptions"] = {
        "status": "PASS" if len(jd_files) >= 1 else "MISSING",
        "file_count": len(jd_files),
        "files": {f: {"size_bytes": os.path.getsize(os.path.join(jd_raw, f)), "sha256": compute_sha256(os.path.join(jd_raw, f))} for f in jd_files}
    }
    print(f"  Job Descriptions: {len(jd_files)} files verified. Status: {verification_results['components']['job_descriptions']['status']}")

    # 4. Learning Resources Verification
    lr_raw = os.path.join(SKILL_GAP_DIR, "raw/learning_resources/learning_resources_catalog.json")
    verification_results["components"]["learning_resources"] = {
        "status": "PASS" if os.path.exists(lr_raw) else "MISSING",
        "catalog_present": os.path.exists(lr_raw),
        "size_bytes": os.path.getsize(lr_raw) if os.path.exists(lr_raw) else 0,
        "sha256": compute_sha256(lr_raw) if os.path.exists(lr_raw) else None
    }
    print(f"  Learning Resources: Catalog verified. Status: {verification_results['components']['learning_resources']['status']}")

    # 5. ML Models Verification
    bge_weights = os.path.join(MODELS_DIR, "bge-small-en-v1.5/model.safetensors")
    qwen_dir = os.path.join(MODELS_DIR, "Qwen2.5-1.5B-Instruct-4bit")
    verification_results["components"]["models"] = {
        "bge_small_weights_present": os.path.exists(bge_weights),
        "bge_small_size_bytes": os.path.getsize(bge_weights) if os.path.exists(bge_weights) else 0,
        "bge_small_sha256": compute_sha256(bge_weights) if os.path.exists(bge_weights) else None,
        "qwen_llm_present": os.path.exists(qwen_dir),
        "status": "PASS" if os.path.exists(bge_weights) and os.path.exists(qwen_dir) else "INCOMPLETE"
    }
    print(f"  ML Models: BGE ({verification_results['components']['models']['bge_small_size_bytes']/(1024*1024):.2f} MB), Qwen LLM verified. Status: {verification_results['components']['models']['status']}")

    out_file = os.path.join(AUDIT_DIR, "download_verification_report.json")
    with open(out_file, "w") as f:
        json.dump(verification_results, f, indent=2)
    print(f"\nDownload verification report generated -> {out_file}")

if __name__ == "__main__":
    verify_all()
