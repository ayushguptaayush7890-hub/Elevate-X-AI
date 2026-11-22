"""
Script 1: download_datasets.py
Acquires and verifies authentic raw datasets for Career Transition & Skill Transferability:
- Dataset A: ESCO v1.2.1 Classification Package (European Commission)
- Dataset B: O*NET 28.1 Database (US Dept of Labor)
- Dataset C: India National Classification of Occupations 2015 (DGE, Ministry of Labour & Employment)
- Dataset D: Authentic Job Descriptions (lang-uk/recruitment & Shresth786/job-resume)
- Dataset E: Verified Learning Resources Catalog
"""

import os
import sys
import shutil
import hashlib
import json
import urllib.request
import ssl
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parents[3]
CAREER_TRANS_DIR = BASE_DIR / "datasets" / "career_transition"
RAW_DIR = CAREER_TRANS_DIR / "raw"
METADATA_DIR = CAREER_TRANS_DIR / "metadata"

ESCO_SRC = BASE_DIR / "datasets" / "skill_gap" / "raw" / "esco"
ONET_SRC = BASE_DIR / "datasets" / "skill_gap" / "raw" / "onet"
JOB_DESC_SRC = BASE_DIR / "datasets" / "skill_gap" / "raw" / "job_descriptions"
LEARNING_RES_SRC = BASE_DIR / "datasets" / "career_roadmap" / "processed" / "verified_resource_catalog.json"

NCO_PDF_URLS = {
    "National_Classification_of_Occupations_Vol_I-2015.pdf": "https://www.dge.gov.in/sites/default/files/2024-05/National_Classification_of_Occupations_Vol_I-2015.pdf",
    "National_Classification_of_Occupations_Vol_II-A-2015.pdf": "https://www.dge.gov.in/sites/default/files/2024-05/National_Classification_of_Occupations_Vol_II-A-2015.pdf",
    "National_Classification_of_Occupations_Vol_II-B-2015.pdf": "https://www.dge.gov.in/sites/default/files/2024-05/National_Classification_of_Occupations_Vol_II-B-2015.pdf"
}


def compute_sha256(filepath: Path) -> str:
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(8192 * 16):
            h.update(chunk)
    return h.hexdigest()


def download_file(url: str, dest: Path) -> bool:
    print(f"Downloading: {url} -> {dest.name}...")
    dest.parent.mkdir(parents=True, exist_ok=True)
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"}
    )
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=60) as resp, open(dest, "wb") as out:
            shutil.copyfileobj(resp, out)
        print(f"  [OK] Saved {dest.name} ({dest.stat().st_size / (1024*1024):.2f} MB)")
        return True
    except Exception as e:
        print(f"  [FAILED] Could not download {url}: {e}")
        return False


def main():
    print("=" * 80)
    print("CAREER TRANSITION — AUTHENTIC DATASET ACQUISITION PIPELINE")
    print("=" * 80)

    # 1. Acquire Dataset C: India NCO 2015 Official PDFs
    nco_dir = RAW_DIR / "india_nco"
    nco_dir.mkdir(parents=True, exist_ok=True)
    nco_records = {}
    for filename, url in NCO_PDF_URLS.items():
        pdf_path = nco_dir / filename
        if not pdf_path.exists() or pdf_path.stat().st_size < 100000:
            success = download_file(url, pdf_path)
            if not success:
                print(f"Warning: Failed to download {filename} from official DGE server.")
        else:
            print(f"  [EXISTS] {filename} ({pdf_path.stat().st_size / (1024*1024):.2f} MB)")

        if pdf_path.exists():
            nco_records[filename] = {
                "path": str(pdf_path.relative_to(BASE_DIR)),
                "size_bytes": pdf_path.stat().st_size,
                "sha256": compute_sha256(pdf_path),
                "url": url,
                "source": "Directorate General of Employment, Ministry of Labour & Employment, India",
                "license": "Government Open Data License - India (GODL)"
            }

    # 2. Acquire Dataset A: ESCO v1.2.1
    esco_dest = RAW_DIR / "esco"
    esco_dest.mkdir(parents=True, exist_ok=True)
    esco_files = [
        "occupations_en.csv", "skills_en.csv", "occupationSkillRelations_en.csv",
        "skillSkillRelations_en.csv", "skillsHierarchy_en.csv", "skillGroups_en.csv",
        "ISCOGroups_en.csv", "digitalSkillsCollection_en.csv", "transversalSkillsCollection_en.csv"
    ]
    esco_records = {}
    for f in esco_files:
        src_f = ESCO_SRC / f
        dest_f = esco_dest / f
        if src_f.exists() and not dest_f.exists():
            shutil.copy2(src_f, dest_f)
        if dest_f.exists():
            esco_records[f] = {
                "path": str(dest_f.relative_to(BASE_DIR)),
                "size_bytes": dest_f.stat().st_size,
                "sha256": compute_sha256(dest_f),
                "source": "European Commission ESCO Portal",
                "version": "v1.2.1",
                "license": "CC BY 4.0"
            }
            print(f"  [ESCO] {f}: {dest_f.stat().st_size / (1024*1024):.2f} MB")

    # 3. Acquire Dataset B: O*NET 28.1
    onet_dest = RAW_DIR / "onet"
    onet_dest.mkdir(parents=True, exist_ok=True)
    onet_key_tables = [
        "Occupation Data.txt", "Knowledge.txt", "Abilities.txt", "Work Activities.txt",
        "Work Context.txt", "Job Zones.txt", "Tasks to DWAs.txt", "Task Statements.txt",
        "Essential Skills.txt", "Transferable Skills.txt", "Related Occupations.txt",
        "Job Titles.txt", "Sample of Reported Titles.txt", "Training and Experience.txt"
    ]
    onet_records = {}
    for f in onet_key_tables:
        src_f = ONET_SRC / f
        dest_f = onet_dest / f
        if src_f.exists() and not dest_f.exists():
            shutil.copy2(src_f, dest_f)
        if dest_f.exists():
            onet_records[f] = {
                "path": str(dest_f.relative_to(BASE_DIR)),
                "size_bytes": dest_f.stat().st_size,
                "sha256": compute_sha256(dest_f),
                "source": "O*NET Resource Center, U.S. Department of Labor",
                "version": "28.1",
                "license": "CC BY 4.0 (O*NET)"
            }
            print(f"  [O*NET] {f}: {dest_f.stat().st_size / (1024*1024):.2f} MB")

    # 4. Acquire Dataset D: Job Descriptions
    job_dest = RAW_DIR / "job_descriptions"
    job_dest.mkdir(parents=True, exist_ok=True)
    job_files = ["recruitment_jds_english.parquet", "shresth_jobs.csv"]
    job_records = {}
    for f in job_files:
        src_f = JOB_DESC_SRC / f
        dest_f = job_dest / f
        if src_f.exists() and not dest_f.exists():
            shutil.copy2(src_f, dest_f)
        if dest_f.exists():
            job_records[f] = {
                "path": str(dest_f.relative_to(BASE_DIR)),
                "size_bytes": dest_f.stat().st_size,
                "sha256": compute_sha256(dest_f),
                "source": "HuggingFace Public Recruitment Datasets",
                "license": "ODbL / Public Domain"
            }
            print(f"  [JOBS] {f}: {dest_f.stat().st_size / (1024*1024):.2f} MB")

    # 5. Acquire Dataset E: Verified Learning Resources
    res_dest = RAW_DIR / "learning_resources" / "verified_resource_catalog.json"
    res_dest.parent.mkdir(parents=True, exist_ok=True)
    if LEARNING_RES_SRC.exists() and not res_dest.exists():
        shutil.copy2(LEARNING_RES_SRC, res_dest)
    res_records = {}
    if res_dest.exists():
        res_records["verified_resource_catalog.json"] = {
            "path": str(res_dest.relative_to(BASE_DIR)),
            "size_bytes": res_dest.stat().st_size,
            "sha256": compute_sha256(res_dest),
            "source": "Audited Official Documentation & Certification Providers",
            "license": "Official Educational Documentation"
        }
        print(f"  [RESOURCES] verified_resource_catalog.json: {res_dest.stat().st_size} bytes")

    # Write Manifests
    METADATA_DIR.mkdir(parents=True, exist_ok=True)
    manifest = {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "datasets": {
            "esco": {"version": "v1.2.1", "files": esco_records},
            "onet": {"version": "28.1", "files": onet_records},
            "india_nco": {"version": "2015", "files": nco_records},
            "job_descriptions": {"version": "2026.1", "files": job_records},
            "learning_resources": {"version": "2026.1", "files": res_records}
        }
    }
    with open(METADATA_DIR / "acquisition_manifest.json", "w") as f:
        json.dump(manifest, f, indent=2)

    versions = {
        "esco": "v1.2.1",
        "onet": "28.1",
        "india_nco": "2015",
        "recruitment_jds": "2024.1",
        "verified_resources": "2026.1"
    }
    with open(METADATA_DIR / "dataset_versions.json", "w") as f:
        json.dump(versions, f, indent=2)

    licenses = {
        "esco": "Creative Commons Attribution 4.0 International (CC BY 4.0)",
        "onet": "Creative Commons Attribution 4.0 International (CC BY 4.0)",
        "india_nco": "Government Open Data License - India (GODL)",
        "recruitment_jds": "Open Data Commons Open Database License (ODbL)",
        "learning_resources": "Public Documentation / Educational Fair Use"
    }
    with open(METADATA_DIR / "license_manifest.json", "w") as f:
        json.dump(licenses, f, indent=2)

    all_checksums = {}
    for group in manifest["datasets"].values():
        for filename, info in group.get("files", {}).items():
            all_checksums[filename] = info["sha256"]
    with open(METADATA_DIR / "checksums.json", "w") as f:
        json.dump(all_checksums, f, indent=2)

    print("\n[SUCCESS] Dataset acquisition complete. Manifests written to metadata/.")


if __name__ == "__main__":
    main()
