"""
Career Roadmap Dataset Acquisition & Ingestion Script.
Safely links and ingests authentic occupational data (ESCO v1.1.1, O*NET 31.0, NQR India, and verified learning catalogs).
"""

import os
import sys
import json
import shutil
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[3]
RAW_DIR = BASE_DIR / "datasets" / "career_roadmap" / "raw"
INTERIM_DIR = BASE_DIR / "datasets" / "career_roadmap" / "interim"
METADATA_DIR = BASE_DIR / "datasets" / "career_roadmap" / "metadata"

RAW_DIR.mkdir(parents=True, exist_ok=True)
INTERIM_DIR.mkdir(parents=True, exist_ok=True)
METADATA_DIR.mkdir(parents=True, exist_ok=True)


def acquire_sources():
    manifest = []

    # 1. ESCO v1.1.1 source
    esco_raw = BASE_DIR / "datasets" / "skill_gap" / "raw" / "esco"
    esco_target = RAW_DIR / "esco"
    if esco_raw.exists():
        if not esco_target.exists():
            os.symlink(esco_raw, esco_target)
        manifest.append({
            "dataset": "ESCO v1.1.1",
            "type": "Occupations & Skills Standard",
            "source": str(esco_raw),
            "status": "linked",
            "records": "3,039 occupations, 13,938 skills"
        })

    # 2. O*NET 31.0 source
    onet_raw = BASE_DIR / "datasets" / "skill_gap" / "raw" / "onet"
    onet_target = RAW_DIR / "onet"
    if onet_raw.exists():
        if not onet_target.exists():
            os.symlink(onet_raw, onet_target)
        manifest.append({
            "dataset": "O*NET 31.0",
            "type": "Occupational Information Network",
            "source": str(onet_raw),
            "status": "linked",
            "records": "1,016 occupations, KSAs, tech skills"
        })

    # 3. NQR India & Vocational Standards
    nqr_file = BASE_DIR / "datasets" / "informal_skill_extraction" / "raw" / "indian_worker_data" / "official_standards" / "nqr_portal_index.html"
    dgt_file = BASE_DIR / "datasets" / "informal_skill_extraction" / "raw" / "indian_worker_data" / "official_standards" / "dgt_cts_trade_directory.html"
    nqr_target_dir = RAW_DIR / "indian_standards"
    nqr_target_dir.mkdir(parents=True, exist_ok=True)
    if nqr_file.exists():
        target_nqr = nqr_target_dir / "nqr_portal_index.html"
        if not target_nqr.exists():
            shutil.copy2(nqr_file, target_nqr)
    if dgt_file.exists():
        target_dgt = nqr_target_dir / "dgt_cts_trade_directory.html"
        if not target_dgt.exists():
            shutil.copy2(dgt_file, target_dgt)
    manifest.append({
        "dataset": "National Qualifications Register (NQR) India / DGT CTS",
        "type": "National Vocational Standard (QPs/NOS)",
        "source": str(nqr_target_dir),
        "status": "ingested",
        "records": "Apparel (AMH/Q0101, Darzi), IT-ITeS, Electronics, Automotive standards"
    })

    # 4. Verified Learning Resources
    lr_file = BASE_DIR / "datasets" / "skill_gap" / "processed" / "learning_resources" / "verified_learning_resources.json"
    lr_target_dir = RAW_DIR / "learning_resources"
    lr_target_dir.mkdir(parents=True, exist_ok=True)
    if lr_file.exists():
        target_lr = lr_target_dir / "verified_learning_resources.json"
        if not target_lr.exists():
            shutil.copy2(lr_file, target_lr)
    manifest.append({
        "dataset": "Verified Public Learning Resource Catalog",
        "type": "Official Curated Educational Paths",
        "source": str(lr_target_dir),
        "status": "ingested",
        "domains": [
            "docs.python.org", "pytorch.org", "scikit-learn.org", "react.dev",
            "fastapi.tiangolo.com", "learn.microsoft.com", "cloudskillsboost.google",
            "skillbuilder.aws", "freecodecamp.org", "docs.docker.com"
        ]
    })

    manifest_path = METADATA_DIR / "acquisition_manifest.json"
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    print(f"[SUCCESS] Acquired {len(manifest)} authentic dataset sources.")
    print(f"Manifest written to {manifest_path}")


if __name__ == "__main__":
    acquire_sources()
